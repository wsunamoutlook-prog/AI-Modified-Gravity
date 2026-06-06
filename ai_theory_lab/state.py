"""LangGraph state schema for AI theory validation."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, TypedDict


class TheoryGraphState(TypedDict, total=False):
    """Shared state passed through the theory-discovery graph."""

    proposal: Dict[str, Any]
    validation_mode: str
    validated: bool
    chi2: Optional[float]
    best_lag_id: Optional[str]
    failed_stage: Optional[str]
    solver_output_dir: Optional[str]
    model_ranking_path: Optional[str]
    scan_report_path: Optional[str]
    harness_result: Dict[str, Any]
    retry_count: int
    max_retries: int
    messages: List[str]

