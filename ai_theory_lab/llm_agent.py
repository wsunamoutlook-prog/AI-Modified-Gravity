"""OpenAI-backed proposal helpers for the LangGraph cold-start loop.

The LLM does not inject arbitrary symbolic expressions. It selects from a
batch of token-level Grammar Masker candidates that are already legal enough to
enter the deterministic harness path.
"""

from __future__ import annotations

import json
import os
import random
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

from .cold_start_runner import (
    _choose_entry,
    _direct_candidate_catalog,
    _direct_entry,
    _entry_score,
    _family_key,
    _under_duplicate_limit,
)


DEFAULT_OPENAI_MODEL = "gpt-5-mini"
MAX_LLM_CANDIDATES = 12
DEFAULT_LLM_MAX_RETRIES = 2
DEFAULT_LLM_MAX_OUTPUT_TOKENS = 1800


def _compact_summary(summary: Dict[str, Any]) -> Dict[str, Any]:
    agent_loop = summary.get("agent_loop") if isinstance(summary.get("agent_loop"), dict) else {}
    structure_prior = agent_loop.get("structure_prior") if isinstance(agent_loop.get("structure_prior"), dict) else {}
    return {
        "total_attempts": summary.get("total_attempts", 0),
        "validated_count": summary.get("validated_count", 0),
        "best_chi2": summary.get("best_chi2"),
        "failure_tag_counts": summary.get("failure_tag_counts") or {},
        "preferred_scalar_configs": structure_prior.get("preferred_scalar_configs") or {},
        "preferred_potentials": structure_prior.get("preferred_potentials") or {},
        "preferred_operators": structure_prior.get("preferred_operators") or {},
        "preferred_features": structure_prior.get("preferred_features") or {},
        "avoid_failure_tags": structure_prior.get("avoid_failure_tags") or {},
        "avoid_scalar_configs": structure_prior.get("avoid_scalar_configs") or {},
        "avoid_features": structure_prior.get("avoid_features") or {},
        "avoid_operators": structure_prior.get("avoid_operators") or {},
    }


def _candidate_view(entry: Dict[str, Any], index: int, score: float) -> Dict[str, Any]:
    return {
        "index": index,
        "family_key": _family_key(entry),
        "scalar_config": entry.get("scalar_config"),
        "potential_types": entry.get("potential_types"),
        "operators": entry.get("operators") or [],
        "operator_specs": entry.get("operator_specs") or [],
        "deterministic_score": round(score, 6),
    }


def _content_text(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        text = value.get("text")
        if isinstance(text, str):
            return text
        nested = value.get("content")
        if isinstance(nested, list):
            return "\n".join(part for part in (_content_text(item) for item in nested) if part)
        return ""
    text = getattr(value, "text", None)
    if isinstance(text, str):
        return text
    nested = getattr(value, "content", None)
    if isinstance(nested, list):
        return "\n".join(part for part in (_content_text(item) for item in nested) if part)
    return ""


def _extract_text(response: Any) -> str:
    text = getattr(response, "output_text", None)
    if isinstance(text, str) and text.strip():
        return text
    pieces: List[str] = []
    for item in getattr(response, "output", []) or []:
        item_text = _content_text(item)
        if item_text:
            pieces.append(item_text)
        for content in getattr(item, "content", []) or []:
            content_text = _content_text(content)
            if content_text:
                pieces.append(content_text)
    return "\n".join(pieces)


def _response_debug_payload(response: Any, text: str = "") -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "extracted_text": text,
        "response_type": type(response).__name__,
    }
    for name in ("id", "model", "status", "finish_reason"):
        value = getattr(response, name, None)
        if value is not None:
            payload[name] = value
    try:
        if hasattr(response, "model_dump"):
            payload["response"] = response.model_dump(mode="json")
        elif hasattr(response, "to_dict"):
            payload["response"] = response.to_dict()
        else:
            payload["response_repr"] = repr(response)
    except Exception as exc:
        payload["response_repr"] = repr(response)
        payload["response_dump_error"] = f"{type(exc).__name__}: {exc}"
    return payload


def _write_llm_debug(
    debug_dir: Optional[Path],
    *,
    loop_id: str,
    attempt: int,
    event: str,
    payload: Dict[str, Any],
) -> Optional[Path]:
    if debug_dir is None:
        return None
    debug_dir.mkdir(parents=True, exist_ok=True)
    path = debug_dir / f"{loop_id}_attempt_{attempt:02d}_{event}.json"
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
    return path


def _parse_json_object(text: str) -> Dict[str, Any]:
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = stripped.strip("`")
        if stripped.lower().startswith("json"):
            stripped = stripped[4:].strip()
    try:
        data = json.loads(stripped)
    except json.JSONDecodeError:
        start = stripped.find("{")
        end = stripped.rfind("}")
        if start < 0 or end <= start:
            raise
        data = json.loads(stripped[start : end + 1])
    if not isinstance(data, dict):
        raise TypeError("LLM response must be a JSON object")
    return data


def _generate_candidate_entries(
    context: Dict[str, Any],
    summary: Dict[str, Any],
    rng: random.Random,
    seed: int,
    *,
    max_batches: int = 3,
) -> List[Dict[str, Any]]:
    skeletons = _direct_candidate_catalog(context)
    entries = [entry for entry in skeletons if entry.get("operator_specs") and _under_duplicate_limit(entry, summary)]
    if not entries:
        entries = [entry for entry in skeletons if entry.get("operator_specs")]
    if not entries:
        return []
    # Keep a deterministic high-scoring beam, then shuffle a prefix lightly so
    # repeated LLM calls do not see exactly the same candidate ordering.
    ranked = sorted(entries, key=lambda entry: _entry_score(entry, summary, rng), reverse=True)
    beam_size = min(len(ranked), max(MAX_LLM_CANDIDATES * max(1, max_batches), MAX_LLM_CANDIDATES))
    beam = list(ranked[:beam_size])
    random.Random(seed + 65537).shuffle(beam)
    ranked = sorted(beam[: MAX_LLM_CANDIDATES * 2], key=lambda entry: _entry_score(entry, summary, rng), reverse=True)
    return ranked[:MAX_LLM_CANDIDATES]


def _call_openai_for_choice(
    *,
    candidates: Sequence[Dict[str, Any]],
    summary: Dict[str, Any],
    model: str,
    api_timeout: float,
    max_output_tokens: int,
    debug_dir: Optional[Path],
    loop_id: str,
    attempt: int,
) -> Tuple[int, str, Dict[str, Any]]:
    from openai import OpenAI

    candidate_views = [
        _candidate_view(entry, i, _entry_score(entry, summary, random.Random(12345 + i)))
        for i, entry in enumerate(candidates)
    ]
    system = (
        "You are a cautious modified-gravity theory proposal agent. "
        "Choose exactly one candidate from the provided grammar-generated list. "
        "Do not invent operators, coefficients, fields, parameter values, or historical results. "
        "Prefer candidates that can survive EOM/Builder/Solver and improve chi-square, while preserving exploration."
    )
    user = {
        "task": "Select one candidate index for the next cold-start validation attempt.",
        "current_loop_feedback": _compact_summary(summary),
        "candidates": candidate_views,
        "output_schema": {
            "candidate_index": "integer index from candidates",
            "rationale": "one concise paragraph using only current-loop feedback and candidate features",
        },
    }
    schema = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "candidate_index": {
                "type": "integer",
                "description": "Index of the selected candidate from the candidates array.",
            },
            "rationale": {
                "type": "string",
                "description": "One concise paragraph using only current-loop feedback and candidate features.",
            },
        },
        "required": ["candidate_index", "rationale"],
    }
    client = OpenAI(timeout=api_timeout)
    response = client.responses.create(
        model=model,
        input=[
            {"role": "system", "content": system},
            {"role": "user", "content": json.dumps(user, ensure_ascii=False)},
        ],
        text={
            "format": {
                "type": "json_schema",
                "name": "candidate_choice",
                "strict": True,
                "schema": schema,
            }
        },
        max_output_tokens=max_output_tokens,
    )
    text = _extract_text(response)
    if not text.strip():
        debug_path = _write_llm_debug(
            debug_dir,
            loop_id=loop_id,
            attempt=attempt,
            event="empty_output",
            payload=_response_debug_payload(response, text),
        )
        suffix = f"; debug={debug_path}" if debug_path else ""
        raise RuntimeError(f"OpenAI response contained no output_text{suffix}")
    try:
        data = _parse_json_object(text)
    except json.JSONDecodeError as exc:
        debug_path = _write_llm_debug(
            debug_dir,
            loop_id=loop_id,
            attempt=attempt,
            event="json_decode_error",
            payload={
                **_response_debug_payload(response, text),
                "error": f"{type(exc).__name__}: {exc}",
            },
        )
        suffix = f"; debug={debug_path}" if debug_path else ""
        raise json.JSONDecodeError(f"{exc.msg}{suffix}", exc.doc, exc.pos) from exc
    index = int(data["candidate_index"])
    if index < 0 or index >= len(candidates):
        raise ValueError(f"LLM candidate_index out of range: {index}")
    rationale = str(data.get("rationale") or "LLM selected this grammar-generated candidate.")
    return index, rationale, data


def propose_entry_with_llm(
    context: Dict[str, Any],
    summary: Dict[str, Any],
    rng: random.Random,
    seed: int,
    *,
    model: Optional[str] = None,
    max_candidate_batches: int = 3,
    api_timeout: float = 120.0,
    max_retries: int = DEFAULT_LLM_MAX_RETRIES,
    max_output_tokens: int = DEFAULT_LLM_MAX_OUTPUT_TOKENS,
    debug_dir: Optional[Path | str] = None,
    loop_id: str = "loop_unknown",
) -> Dict[str, Any]:
    """Generate legal candidates and let the OpenAI API select one.

    Raises on missing credentials, API failures, or invalid responses so the
    caller can fall back to deterministic proposal generation.
    """

    selected_model = model or os.getenv("OPENAI_MODEL") or DEFAULT_OPENAI_MODEL
    candidates = _generate_candidate_entries(
        context,
        summary,
        rng,
        seed,
        max_batches=max_candidate_batches,
    )
    if not candidates:
        raise RuntimeError("No grammar-generated candidates available for LLM selection")
    debug_path = Path(debug_dir) if debug_dir is not None else None
    errors: List[str] = []
    total_attempts = max(1, int(max_retries) + 1)
    for attempt in range(1, total_attempts + 1):
        try:
            index, rationale, raw_choice = _call_openai_for_choice(
                candidates=candidates,
                summary=summary,
                model=selected_model,
                api_timeout=api_timeout,
                max_output_tokens=max_output_tokens,
                debug_dir=debug_path,
                loop_id=loop_id,
                attempt=attempt,
            )
            break
        except Exception as exc:
            message = f"attempt {attempt}/{total_attempts}: {type(exc).__name__}: {exc}"
            errors.append(message)
            print(f"[LLMProposal] {loop_id} {message}", flush=True)
            _write_llm_debug(
                debug_path,
                loop_id=loop_id,
                attempt=attempt,
                event="failure",
                payload={
                    "error": message,
                    "model": selected_model,
                    "api_timeout": api_timeout,
                    "max_output_tokens": max_output_tokens,
                    "candidate_count": len(candidates),
                },
            )
            if attempt >= total_attempts:
                raise RuntimeError("LLM proposal failed after retries: " + " | ".join(errors)) from exc
            time.sleep(min(2.0 * attempt, 5.0))
    selected = dict(candidates[index])
    candidate_objects = selected.pop("_candidate_objects", None)
    if not candidate_objects:
        raise RuntimeError("LLM-selected direct candidate was missing candidate objects")
    entry = _direct_entry(
        tensors=context["tensors"],
        scalar_config=str(selected["scalar_config"]),
        potential_types=dict(selected["potential_types"]),
        candidates=candidate_objects,
        local_number=int(selected["local_number"]),
    )
    entry["proposal_mode"] = "llm"
    entry["llm_model"] = selected_model
    entry["llm_rationale"] = rationale
    entry["llm_choice"] = {
        "candidate_index": index,
        "candidate_count": len(candidates),
        "raw_choice": raw_choice,
        "attempts_used": attempt,
        "retry_errors": errors,
    }
    required = ("scalar_config", "potential_types", "operators", "operator_specs", "n_terms", "lagrangian")
    missing = [key for key in required if key not in entry]
    if missing:
        raise RuntimeError(f"LLM-selected candidate compiled to incomplete entry; missing keys={missing}")
    return entry


def fallback_entry(
    candidates: Sequence[Dict[str, Any]],
    summary: Dict[str, Any],
    rng: random.Random,
) -> Dict[str, Any]:
    entry = dict(_choose_entry(candidates, summary, rng))
    entry["proposal_mode"] = "deterministic_fallback"
    return entry
