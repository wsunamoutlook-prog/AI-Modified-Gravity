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


DEFAULT_SPECS = [
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


def _redacted_env_status(name: str | None) -> str:
    if not name:
        return "n/a"
    return "set" if os.getenv(name) else "missing"


def _call_openai_native(spec: ApiSpec, timeout: float) -> str:
    from openai import OpenAI

    client = OpenAI(api_key=os.environ[spec.key_env], timeout=timeout)
    response = client.responses.create(
        model=spec.model,
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
    response = client.chat.completions.create(
        model=spec.model,
        messages=[{"role": "user", "content": "Return exactly: ok"}],
        max_tokens=16,
    )
    return (response.choices[0].message.content or "").strip()


def _call_anthropic(spec: ApiSpec, timeout: float) -> str:
    try:
        import anthropic
    except Exception:
        anthropic = None

    if anthropic is not None:
        client = anthropic.Anthropic(api_key=os.environ[spec.key_env], timeout=timeout)
        response = client.messages.create(
            model=spec.model,
            max_tokens=16,
            messages=[{"role": "user", "content": "Return exactly: ok"}],
        )
        parts = []
        for block in getattr(response, "content", []) or []:
            text = getattr(block, "text", None)
            if text:
                parts.append(text)
        return "\n".join(parts).strip()

    payload = json.dumps(
        {
            "model": spec.model,
            "max_tokens": 16,
            "messages": [{"role": "user", "content": "Return exactly: ok"}],
        }
    ).encode("utf-8")
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
    with urllib.request.urlopen(request, timeout=timeout) as response:
        data = json.loads(response.read().decode("utf-8"))
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
        "model": spec.model,
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
        "--include-official-deepseek",
        action="store_true",
        help="Also check a separate official DeepSeek endpoint via DEEPSEEK_API_KEY.",
    )
    args = parser.parse_args(argv)

    specs = [*DEFAULT_SPECS, *(OPTIONAL_SPECS if args.include_official_deepseek else [])]
    results = [check_spec(spec, live=args.live, timeout=args.timeout) for spec in specs]
    results.append(_check_langsmith(live=args.live, timeout=args.timeout))

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for row in results:
            status = "OK" if row.get("ready") else "MISSING"
            live = row.get("live_status")
            suffix = f" live={live}" if live else ""
            print(f"{row['name']:17s} {status:7s}{suffix}")
            if row.get("error"):
                print(f"  error: {row['error']}")
            if row.get("response_preview"):
                print(f"  response: {row['response_preview']}")
    missing = [row["name"] for row in results if not row.get("ready")]
    if missing:
        print("missing:", ", ".join(missing), file=sys.stderr)
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
