"""Minimal LangGraph wrapper around the strict validation harness.

This graph deliberately keeps validation centralized: the only node allowed to
assign `validated` or `chi2` is `validate_with_harness`, which calls the harness.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from langgraph.graph import END, StateGraph

from .harness import (
    read_existing_output,
    read_latest_only,
    validate_agent_sample_pipeline,
    validate_current_pipeline,
)
from .state import TheoryGraphState


def _append_message(state: TheoryGraphState, message: str) -> List[str]:
    return [*state.get("messages", []), message]


def propose_theory(state: TheoryGraphState) -> Dict[str, Any]:
    """Carry a proposal into the graph.

    A future LLM node can replace this function, but it still must pass through
    `validate_with_harness` before any score is trusted.
    """

    proposal = state.get("proposal") or {
        "source": "placeholder",
        "description": "No LLM proposal attached yet; validate current pipeline artifacts.",
    }
    return {
        "proposal": proposal,
        "messages": _append_message(state, "Proposal received. Validation must use the harness."),
    }


def validate_with_harness(state: TheoryGraphState) -> Dict[str, Any]:
    """Run the only trusted validation path."""

    mode = state.get("validation_mode", "read_latest")
    if mode == "run":
        result = validate_current_pipeline()
    elif mode == "agent_sample":
        result = validate_agent_sample_pipeline()
    elif mode.startswith("output_dir:"):
        result = read_existing_output(Path(mode.split(":", 1)[1]))
    else:
        result = read_latest_only()

    data = result.to_dict()
    message = "Harness validation completed." if result.validated else "Harness did not validate a new theory."
    if result.failed_stage:
        message = f"Harness failed at {result.failed_stage}; return diagnostics to the proposal agent."

    return {
        "validated": result.validated,
        "chi2": result.chi2,
        "best_lag_id": result.best_lag_id,
        "failed_stage": result.failed_stage,
        "solver_output_dir": result.solver_output_dir,
        "model_ranking_path": result.model_ranking_path,
        "scan_report_path": result.scan_report_path,
        "harness_result": data,
        "messages": _append_message(state, message),
    }


def reflect_or_retry(state: TheoryGraphState) -> Dict[str, Any]:
    """Decide what the proposal agent should do after harness output."""

    retry_count = int(state.get("retry_count", 0))
    if state.get("validated"):
        msg = (
            f"Validated by real EOM/Builder/Solver. "
            f"best_lag_id={state.get('best_lag_id')}, chi2={state.get('chi2')}."
        )
        return {"messages": _append_message(state, msg)}

    failed_stage = state.get("failed_stage")
    if failed_stage:
        msg = f"Not validated. Revise proposal using harness diagnostics from {failed_stage}."
        return {"retry_count": retry_count + 1, "messages": _append_message(state, msg)}

    msg = (
        "Read-only harness result available. This is useful for inspection, "
        "but a theory is not validated until validation_mode='run'."
    )
    return {"messages": _append_message(state, msg)}


def route_after_reflection(state: TheoryGraphState) -> str:
    """Retry only for real failed validation, not for read-only inspection."""

    if state.get("validated"):
        return END
    if not state.get("failed_stage"):
        return END
    if int(state.get("retry_count", 0)) >= int(state.get("max_retries", 0)):
        return END
    return "propose_theory"


def build_graph():
    graph = StateGraph(TheoryGraphState)
    graph.add_node("propose_theory", propose_theory)
    graph.add_node("validate_with_harness", validate_with_harness)
    graph.add_node("reflect_or_retry", reflect_or_retry)

    graph.set_entry_point("propose_theory")
    graph.add_edge("propose_theory", "validate_with_harness")
    graph.add_edge("validate_with_harness", "reflect_or_retry")
    graph.add_conditional_edges("reflect_or_retry", route_after_reflection)
    return graph.compile()


def run_graph(
    *,
    validation_mode: str,
    proposal: Optional[Dict[str, Any]] = None,
    max_retries: int = 0,
) -> TheoryGraphState:
    app = build_graph()
    initial: TheoryGraphState = {
        "proposal": proposal or {},
        "validation_mode": validation_mode,
        "retry_count": 0,
        "max_retries": max_retries,
        "messages": [],
    }
    return app.invoke(initial)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Run the minimal theory-validation LangGraph.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--run-validation",
        action="store_true",
        help="Actually run the current batch EOM, Builder, and Solver through the harness.",
    )
    mode.add_argument(
        "--agent-sample",
        action="store_true",
        help="Sample one existing Lagrangian and validate only that isolated agent_lagrangians.pkl.",
    )
    mode.add_argument(
        "--read-latest-only",
        action="store_true",
        help="Read latest Solver output only. This does not validate a new theory.",
    )
    mode.add_argument(
        "--output-dir",
        type=Path,
        help="Read one existing Solver output directory. This does not validate a new theory.",
    )
    parser.add_argument("--proposal-json", help="Optional JSON object for the proposal state.")
    parser.add_argument("--max-retries", type=int, default=0)
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args(argv)

    if args.run_validation:
        validation_mode = "run"
    elif args.agent_sample:
        validation_mode = "agent_sample"
    elif args.output_dir is not None:
        validation_mode = f"output_dir:{args.output_dir.expanduser().resolve()}"
    else:
        validation_mode = "read_latest"

    proposal = json.loads(args.proposal_json) if args.proposal_json else None
    result = run_graph(
        validation_mode=validation_mode,
        proposal=proposal,
        max_retries=args.max_retries,
    )
    print(json.dumps(result, indent=2 if args.pretty else None, ensure_ascii=False))
    return 0 if result.get("validated") or validation_mode != "run" else 1


if __name__ == "__main__":
    raise SystemExit(main())
