"""Check configured LLM and tracing API connections.

This is a lightweight preflight helper for cluster runs. By default it only
checks environment variables. Pass ``--live`` to send one tiny request to each
configured API.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ApiSpec:
    name: str
    provider: str
    model: str
    key_env: str
    base_url_env: str | None = None
    default_base_url: str | None = None
    model_env: str | None = None


FRONTIER6_SPECS = [
    ApiSpec("openai", "openai", "gpt-5.6-sol", "OPENAI_API_KEY"),
    ApiSpec("claude", "anthropic", "claude-sonnet-5", "ANTHROPIC_API_KEY"),
    ApiSpec(
        "gemini",
        "openai_compatible",
        "gemini-3.6-flash",
        "GEMINI_API_KEY",
        "GEMINI_BASE_URL",
        "https://generativelanguage.googleapis.com/v1beta/openai/",
    ),
    ApiSpec(
        "qwen",
        "openai_compatible",
        "qwen3.7-max",
        "DASHSCOPE_API_KEY",
        "QWEN_BASE_URL",
    ),
    ApiSpec(
        "deepseek_ali",
        "openai_compatible",
        "deepseek-v4-pro",
        "DASHSCOPE_API_KEY",
        "QWEN_BASE_URL",
    ),
    ApiSpec(
        "kimi",
        "openai_compatible",
        "kimi-k3",
        "MOONSHOT_API_KEY",
        "KIMI_BASE_URL",
        "https://api.moonshot.ai/v1",
        model_env="KIMI_MODEL",
    ),
]

LEGACY5_SPECS = [
    ApiSpec("openai", "openai", "gpt-5.4-mini", "OPENAI_API_KEY"),
    ApiSpec("claude", "anthropic", "claude-sonnet-4-6", "ANTHROPIC_API_KEY"),
    ApiSpec(
        "gemini",
        "openai_compatible",
        "gemini-3.5-flash",
        "GEMINI_API_KEY",
        "GEMINI_BASE_URL",
        "https://generativelanguage.googleapis.com/v1beta/openai/",
    ),
    ApiSpec(
        "qwen",
        "openai_compatible",
        "qwen3.7-plus",
        "DASHSCOPE_API_KEY",
        "QWEN_BASE_URL",
    ),
    ApiSpec(
        "deepseek_ali",
        "openai_compatible",
        "deepseek-v4-pro",
        "DASHSCOPE_API_KEY",
        "QWEN_BASE_URL",
    ),
]

CLAUDE5_SPECS = [
    ApiSpec("claude_opus5", "anthropic", "claude-opus-5", "ANTHROPIC_API_KEY"),
    ApiSpec("claude_fable5", "anthropic", "claude-fable-5", "ANTHROPIC_API_KEY"),
]

API_PRESETS = {
    "frontier6": FRONTIER6_SPECS,
    "claude5": CLAUDE5_SPECS,
    "legacy5": LEGACY5_SPECS,
}

OPTIONAL_SPECS = [
    ApiSpec(
        "deepseek_official",
        "openai_compatible",
        "deepseek-v4-pro",
        "DEEPSEEK_API_KEY",
        "DEEPSEEK_BASE_URL",
        "https://api.deepseek.com",
    ),
]


def _is_set(name: str | None) -> bool:
    return bool(name and os.getenv(name))


def _base_url(spec: ApiSpec) -> str | None:
    if spec.base_url_env and os.getenv(spec.base_url_env):
        return os.getenv(spec.base_url_env)
    return spec.default_base_url


def _model(spec: ApiSpec) -> str:
    if spec.model_env and os.getenv(spec.model_env):
        return str(os.getenv(spec.model_env))
    return spec.model


def _redacted_env_status(name: str | None) -> str:
    if not name:
        return "n/a"
    return "set" if os.getenv(name) else "missing"


def _call_openai_native(spec: ApiSpec, timeout: float) -> str:
    from openai import OpenAI

    client = OpenAI(api_key=os.environ[spec.key_env], timeout=timeout)
    response = client.responses.create(
        model=_model(spec),
        input="Return exactly: ok",
        max_output_tokens=16,
    )
    text = getattr(response, "output_text", "") or ""
    return text.strip()


def _call_openai_compatible(spec: ApiSpec, timeout: float) -> str:
    from openai import OpenAI

    base_url = _base_url(spec)
    if not base_url:
        raise RuntimeError(f"missing base URL env {spec.base_url_env}")
    client = OpenAI(api_key=os.environ[spec.key_env], base_url=base_url, timeout=timeout)
    model = _model(spec)
    request_kwargs: dict[str, Any] = {
        "model": model,
        "messages": [{"role": "user", "content": "Return exactly: ok"}],
    }
    if model == "kimi-k3":
        request_kwargs["reasoning_effort"] = "low"
        request_kwargs["max_completion_tokens"] = 64
    else:
        request_kwargs["max_tokens"] = 16
    response = client.chat.completions.create(**request_kwargs)
    return (response.choices[0].message.content or "").strip()


def _call_anthropic(spec: ApiSpec, timeout: float) -> str:
    from ai_theory_lab.llm_agent import _anthropic_request_options

    model = _model(spec)
    body: dict[str, Any] = {
        "model": model,
        "max_tokens": 64,
        "messages": [{"role": "user", "content": "Return exactly: ok"}],
        **_anthropic_request_options(model),
    }

    payload = json.dumps(body).encode("utf-8")
    request = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=payload,
        headers={
            "content-type": "application/json",
            "x-api-key": os.environ[spec.key_env],
            "anthropic-version": "2023-06-01",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Anthropic API HTTP {exc.code}: {detail[:1000]}") from exc
    if data.get("stop_reason") == "refusal":
        details = data.get("stop_details") or {}
        category = details.get("category") if isinstance(details, dict) else None
        suffix = f" ({category})" if category else ""
        raise RuntimeError(f"Anthropic API refused connectivity probe{suffix}")
    return "\n".join(block.get("text", "") for block in data.get("content", [])).strip()


def _live_call(spec: ApiSpec, timeout: float) -> str:
    if spec.provider == "openai":
        return _call_openai_native(spec, timeout)
    if spec.provider == "anthropic":
        return _call_anthropic(spec, timeout)
    if spec.provider == "openai_compatible":
        return _call_openai_compatible(spec, timeout)
    raise RuntimeError(f"unsupported provider {spec.provider}")


def _check_langsmith(live: bool, timeout: float) -> dict[str, Any]:
    result: dict[str, Any] = {
        "name": "langsmith",
        "env": {
            "LANGSMITH_TRACING": os.getenv("LANGSMITH_TRACING") or "",
            "LANGSMITH_API_KEY": _redacted_env_status("LANGSMITH_API_KEY"),
            "LANGSMITH_PROJECT": os.getenv("LANGSMITH_PROJECT") or "",
        },
        "ready": _is_set("LANGSMITH_API_KEY") and (os.getenv("LANGSMITH_TRACING") or "").lower() in {"1", "true", "yes", "on"},
    }
    if live:
        try:
            from ai_theory_lab.tracing import trace_event, tracing_enabled

            trace_event("ai_theory_lab.api_connection_check", {"event": "api_connection_check"})
            result["live_status"] = "ok" if tracing_enabled() else "disabled"
        except Exception as exc:
            result["live_status"] = "error"
            result["error"] = f"{type(exc).__name__}: {exc}"
    return result


def check_spec(spec: ApiSpec, live: bool, timeout: float) -> dict[str, Any]:
    base_url = _base_url(spec)
    ready = _is_set(spec.key_env) and (spec.provider != "openai_compatible" or bool(base_url))
    result: dict[str, Any] = {
        "name": spec.name,
        "provider": spec.provider,
        "model": _model(spec),
        "model_env": spec.model_env or "",
        "key_env": spec.key_env,
        "key_status": _redacted_env_status(spec.key_env),
        "base_url_env": spec.base_url_env or "",
        "base_url_status": "set" if base_url else ("n/a" if spec.provider != "openai_compatible" else "missing"),
        "ready": ready,
    }
    if live and ready:
        try:
            text = _live_call(spec, timeout)
            result["live_status"] = "ok"
            result["response_preview"] = text[:80]
        except Exception as exc:
            result["live_status"] = "error"
            result["error"] = f"{type(exc).__name__}: {exc}"
    elif live:
        result["live_status"] = "skipped"
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check LLM provider and LangSmith API configuration.")
    parser.add_argument("--live", action="store_true", help="Send one tiny request to each configured API.")
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--json", action="store_true", help="Print JSON instead of a compact table.")
    parser.add_argument(
        "--preset",
        choices=sorted(API_PRESETS),
        default="frontier6",
        help=(
            "API/model set to check. frontier6 is the six-model production set; "
            "claude5 checks the matched Opus 5/Fable 5 extension; legacy5 "
            "reproduces the previous comparison set."
        ),
    )
    parser.add_argument(
        "--include-official-deepseek",
        action="store_true",
        help="Also check a separate official DeepSeek endpoint via DEEPSEEK_API_KEY.",
    )
    args = parser.parse_args(argv)

    specs = [*API_PRESETS[args.preset], *(OPTIONAL_SPECS if args.include_official_deepseek else [])]
    results = [check_spec(spec, live=args.live, timeout=args.timeout) for spec in specs]
    results.append(_check_langsmith(live=args.live, timeout=args.timeout))

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for row in results:
            status = "OK" if row.get("ready") else "MISSING"
            live = row.get("live_status")
            suffix = f" live={live}" if live else ""
            model = row.get("model")
            model_suffix = f" model={model}" if model else ""
            print(f"{row['name']:17s} {status:7s}{suffix}{model_suffix}")
            if row.get("error"):
                print(f"  error: {row['error']}")
            if row.get("response_preview"):
                print(f"  response: {row['response_preview']}")
    missing = [row["name"] for row in results if not row.get("ready")]
    if missing:
        print("missing:", ", ".join(missing), file=sys.stderr)
    live_errors = [row["name"] for row in results if row.get("live_status") == "error"]
    if live_errors:
        print("live errors:", ", ".join(live_errors), file=sys.stderr)
    return 1 if missing or live_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
