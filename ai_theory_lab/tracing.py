"""Optional tracing hooks for external observability services.

Tracing must never be required for discovery runs. If LangSmith is not
configured, these helpers are no-ops.
"""

from __future__ import annotations

import os
import time
from typing import Any, Dict, Optional


def tracing_enabled() -> bool:
    value = (
        os.getenv("LANGSMITH_TRACING")
        or os.getenv("LANGCHAIN_TRACING_V2")
        or os.getenv("AI_THEORY_LAB_TRACING")
        or ""
    ).strip().lower()
    return value in {"1", "true", "yes", "on"}


def trace_event(name: str, payload: Dict[str, Any], *, run_name: Optional[str] = None) -> None:
    """Best-effort LangSmith trace event.

    The implementation intentionally avoids adding LangChain as a hard runtime
    dependency. When the optional langsmith package or API key is missing, this
    silently returns so cluster jobs continue normally.
    """

    if not tracing_enabled():
        return
    try:
        from langsmith import Client
    except Exception:
        return

    api_key = os.getenv("LANGSMITH_API_KEY") or os.getenv("LANGCHAIN_API_KEY")
    if not api_key:
        return
    project_name = os.getenv("LANGSMITH_PROJECT") or os.getenv("LANGCHAIN_PROJECT") or "modified-gravity"
    blocked_keys = {
        "api_key",
        "key",
        "secret",
        "token",
        "authorization",
        "OPENAI_API_KEY",
        "ANTHROPIC_API_KEY",
        "GEMINI_API_KEY",
        "DASHSCOPE_API_KEY",
        "DEEPSEEK_API_KEY",
        "LANGSMITH_API_KEY",
        "LANGCHAIN_API_KEY",
    }
    safe_payload = {
        key: value
        for key, value in payload.items()
        if str(key).lower() not in {item.lower() for item in blocked_keys}
    }
    try:
        client = Client(api_key=api_key)
        trace = client.create_run(
            name=name,
            run_type="chain",
            project_name=project_name,
            inputs={
                "event": name,
                "run_name": run_name,
                "timestamp": safe_payload.get("timestamp") or time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            },
            extra=safe_payload,
        )
        client.update_run(trace.id, outputs=safe_payload)
    except Exception:
        return
