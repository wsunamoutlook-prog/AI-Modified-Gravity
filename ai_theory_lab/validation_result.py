"""Structured result objects for end-to-end theory validation."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class StageResult:
    """Result of running one pipeline stage command."""

    stage: str
    cmd: List[str]
    returncode: int
    elapsed_seconds: float
    stdout_tail: str = ""
    stderr_tail: str = ""
    output_dir: Optional[str] = None

    @property
    def ok(self) -> bool:
        return self.returncode == 0


@dataclass
class ValidationResult:
    """End-to-end validation result produced by the harness."""

    validated: bool
    failed_stage: Optional[str] = None
    best_lag_id: Optional[str] = None
    chi2: Optional[float] = None
    aic: Optional[float] = None
    bic: Optional[float] = None
    k_params: Optional[int] = None
    k_parameter_names: List[str] = field(default_factory=list)
    solver_output_dir: Optional[str] = None
    model_ranking_path: Optional[str] = None
    scan_report_path: Optional[str] = None
    stages: List[StageResult] = field(default_factory=list)
    diagnostics: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
