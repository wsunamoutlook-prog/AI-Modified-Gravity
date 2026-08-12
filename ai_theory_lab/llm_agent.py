"""LLM-backed proposal helpers for the LangGraph cold-start loop.

The LLM does not inject arbitrary symbolic expressions. It selects from a
batch of token-level Grammar Masker candidates that are already legal enough to
enter the deterministic harness path.
"""

from __future__ import annotations

import json
import os
import random
import re
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

from .cold_start_runner import (
    _choose_entry,
    _direct_candidate_catalog,
    _direct_entry,
    _diversity_metadata,
    _entry_score,
    _family_key,
    _sample_operator_policy,
    _under_duplicate_limit,
    theory_track_from_operators,
)


DEFAULT_OPENAI_MODEL = "gpt-5.6-sol"
DEFAULT_ANTHROPIC_MODEL = "claude-sonnet-5"
DEFAULT_LLM_PROVIDER = "openai"
OPENAI_COMPATIBLE_PROVIDER = "openai_compatible"
ANTHROPIC_PROVIDER = "anthropic"
SUPPORTED_LLM_PROVIDERS = (DEFAULT_LLM_PROVIDER, OPENAI_COMPATIBLE_PROVIDER, ANTHROPIC_PROVIDER)
MAX_LLM_CANDIDATES = 12
DEFAULT_LLM_MAX_RETRIES = 2
DEFAULT_LLM_MAX_OUTPUT_TOKENS = 1800


def _compact_summary(summary: Dict[str, Any]) -> Dict[str, Any]:
    agent_loop = summary.get("agent_loop") if isinstance(summary.get("agent_loop"), dict) else {}
    structure_prior = agent_loop.get("structure_prior") if isinstance(agent_loop.get("structure_prior"), dict) else {}
    policy = summary.get("policy") if isinstance(summary.get("policy"), dict) else {}
    return {
        "total_attempts": summary.get("total_attempts", 0),
        "validated_count": summary.get("validated_count", 0),
        "best_chi2": summary.get("best_chi2"),
        "best_structure_score": summary.get("best_structure_score"),
        "structure_learning_metric": (
            structure_prior.get("structure_reward_metric")
            or policy.get("reward_metric")
            or "AIC-2*k_LCDM"
        ),
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


def _candidate_view(entry: Dict[str, Any], index: int, score: float, summary: Dict[str, Any]) -> Dict[str, Any]:
    diversity = _diversity_metadata(entry, summary)
    return {
        "index": index,
        "family_key": _family_key(entry),
        "scalar_config": entry.get("scalar_config"),
        "potential_types": entry.get("potential_types"),
        "operators": entry.get("operators") or [],
        "operator_specs": entry.get("operator_specs") or [],
        "theory_track": entry.get("theory_track") or theory_track_from_operators(entry.get("operators") or []),
        "deterministic_score": round(score, 6),
        "coarse_family_key": diversity.get("diversity_coarse_family_key"),
        "diversity_repetition_penalty": diversity.get("diversity_repetition_penalty"),
        "exact_family_attempts": diversity.get("diversity_exact_family_attempts"),
        "coarse_family_attempts": diversity.get("diversity_coarse_family_attempts"),
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
    if isinstance(response, dict):
        payload["response"] = response
        return payload
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


def _choice_prompt(
    candidates: Sequence[Dict[str, Any]],
    summary: Dict[str, Any],
) -> Tuple[str, Dict[str, Any], Dict[str, Any]]:
    candidate_views = [
        _candidate_view(entry, i, _entry_score(entry, summary, random.Random(12345 + i)), summary)
        for i, entry in enumerate(candidates)
    ]
    system = (
        "You are a cautious modified-gravity theory proposal agent. "
        "Choose exactly one candidate from the provided grammar-generated list. "
        "Do not invent operators, coefficients, fields, parameter values, or historical results. "
        "Prefer candidates that can survive EOM/Builder/Solver and improve the AIC-adjusted cross-Lagrangian "
        "structure score, while preserving exploration. Raw chi-square remains the parameter-search signal. "
        "Return only a JSON object matching the requested schema."
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
    return system, user, schema


def _provider_key(provider: str) -> str:
    normalized = provider.strip().lower().replace("-", "_")
    aliases = {
        "openai_native": "openai",
        "responses": "openai",
        "compatible": OPENAI_COMPATIBLE_PROVIDER,
        "openai_compat": OPENAI_COMPATIBLE_PROVIDER,
        "openrouter": OPENAI_COMPATIBLE_PROVIDER,
        "requesty": OPENAI_COMPATIBLE_PROVIDER,
        "deepseek": OPENAI_COMPATIBLE_PROVIDER,
        "ollama": OPENAI_COMPATIBLE_PROVIDER,
        "claude": ANTHROPIC_PROVIDER,
        "anthropic_native": ANTHROPIC_PROVIDER,
    }
    normalized = aliases.get(normalized, normalized)
    if normalized not in SUPPORTED_LLM_PROVIDERS:
        raise ValueError(
            f"Unsupported llm_provider={provider!r}; supported providers are {', '.join(SUPPORTED_LLM_PROVIDERS)}."
        )
    return normalized


def _default_api_key_env(provider: str, base_url: Optional[str]) -> str:
    if provider == "openai":
        return "OPENAI_API_KEY"
    if provider == ANTHROPIC_PROVIDER:
        return "ANTHROPIC_API_KEY"
    url = (base_url or os.getenv("LLM_BASE_URL") or os.getenv("OPENAI_BASE_URL") or "").lower()
    if "generativelanguage.googleapis.com" in url or "googleapis.com" in url:
        return "GEMINI_API_KEY"
    if "dashscope" in url or "aliyuncs.com/compatible-mode" in url:
        return "DASHSCOPE_API_KEY"
    if "openrouter" in url:
        return "OPENROUTER_API_KEY"
    if "requesty" in url:
        return "REQUESTY_API_KEY"
    if "deepseek" in url:
        return "DEEPSEEK_API_KEY"
    if "moonshot" in url or "kimi" in url:
        return "MOONSHOT_API_KEY"
    if "localhost" in url or "127.0.0.1" in url:
        return "OLLAMA_API_KEY"
    return "OPENAI_COMPATIBLE_API_KEY"


def _resolved_api_key(api_key_env: str, provider: str, base_url: Optional[str]) -> Optional[str]:
    env_names = [api_key_env] if api_key_env else []
    fallback = _default_api_key_env(provider, base_url)
    if fallback not in env_names:
        env_names.append(fallback)
    if provider == OPENAI_COMPATIBLE_PROVIDER:
        for name in (
            "OPENAI_COMPATIBLE_API_KEY",
            "OPENROUTER_API_KEY",
            "REQUESTY_API_KEY",
            "GEMINI_API_KEY",
            "DASHSCOPE_API_KEY",
            "DEEPSEEK_API_KEY",
            "MOONSHOT_API_KEY",
            "KIMI_API_KEY",
            "OPENAI_API_KEY",
        ):
            if name not in env_names:
                env_names.append(name)
    if provider == ANTHROPIC_PROVIDER and "ANTHROPIC_API_KEY" not in env_names:
        env_names.append("ANTHROPIC_API_KEY")
    for name in env_names:
        value = os.getenv(name)
        if value:
            return value
    if provider == OPENAI_COMPATIBLE_PROVIDER:
        url = (base_url or "").lower()
        if "localhost" in url or "127.0.0.1" in url:
            return "ollama"
    return None


def _default_model(provider: str) -> str:
    if provider == ANTHROPIC_PROVIDER:
        return os.getenv("ANTHROPIC_MODEL") or DEFAULT_ANTHROPIC_MODEL
    if provider == OPENAI_COMPATIBLE_PROVIDER:
        return os.getenv("OPENAI_COMPATIBLE_MODEL") or os.getenv("LLM_MODEL") or DEFAULT_OPENAI_MODEL
    return os.getenv("OPENAI_MODEL") or DEFAULT_OPENAI_MODEL


def _openai_compatible_text(response: Any) -> str:
    choices = getattr(response, "choices", None) or []
    if not choices:
        return ""
    message = getattr(choices[0], "message", None)
    content = getattr(message, "content", None)
    if isinstance(content, str):
        return content
    return _content_text(content)


def _openai_compatible_request_options(
    *,
    model: str,
    base_url: str,
    max_output_tokens: int,
) -> Dict[str, Any]:
    """Keep short candidate-selection calls out of expensive reasoning mode."""

    model_key = model.lower()
    url_key = base_url.lower()
    options: Dict[str, Any] = {}
    if "aliyuncs.com" in url_key or "dashscope" in url_key:
        options["max_completion_tokens"] = max_output_tokens
        options["extra_body"] = {"enable_thinking": False}
    elif "googleapis.com" in url_key or "generativelanguage" in url_key:
        options["max_completion_tokens"] = max_output_tokens
        options["reasoning_effort"] = "low"
    elif "moonshot" in url_key or model_key.startswith("kimi"):
        options["max_completion_tokens"] = max_output_tokens
        options["reasoning_effort"] = "low"
    else:
        options["max_tokens"] = max_output_tokens
    return options


def _anthropic_endpoint(base_url: Optional[str]) -> str:
    url = (base_url or os.getenv("ANTHROPIC_BASE_URL") or "https://api.anthropic.com/v1").rstrip("/")
    if url.endswith("/messages"):
        return url
    return f"{url}/messages"


def _call_anthropic_messages(
    *,
    system: str,
    user: Dict[str, Any],
    model: str,
    base_url: Optional[str],
    api_key: str,
    api_timeout: float,
    max_output_tokens: int,
) -> Tuple[str, Dict[str, Any]]:
    body = {
        "model": model,
        "max_tokens": max_output_tokens,
        "thinking": {"type": "disabled"},
        "system": system,
        "messages": [
            {
                "role": "user",
                "content": (
                    json.dumps(user, ensure_ascii=False)
                    + "\n\nReturn only valid JSON. Do not wrap it in markdown fences."
                ),
            }
        ],
    }
    request = urllib.request.Request(
        _anthropic_endpoint(base_url),
        data=json.dumps(body).encode("utf-8"),
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=api_timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Anthropic API HTTP {exc.code}: {detail[:1000]}") from exc
    content = payload.get("content") or []
    pieces = []
    for block in content:
        if isinstance(block, dict) and block.get("type") == "text":
            pieces.append(str(block.get("text") or ""))
    return "\n".join(pieces), payload


def _response_usage_payload(response: Any) -> Optional[Dict[str, Any]]:
    if isinstance(response, dict):
        usage = response.get("usage")
        return dict(usage) if isinstance(usage, dict) else None
    usage = getattr(response, "usage", None)
    if usage is None:
        return None
    try:
        if hasattr(usage, "model_dump"):
            return usage.model_dump(mode="json")
        if hasattr(usage, "to_dict"):
            return usage.to_dict()
    except Exception:
        return {"repr": repr(usage)}
    if isinstance(usage, dict):
        return dict(usage)
    return {"repr": repr(usage)}


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


def _parse_candidate_choice(text: str) -> Dict[str, Any]:
    """Parse a choice, recovering an explicit index from truncated rationale."""

    stripped = text.strip()
    if re.fullmatch(r"-?\d+", stripped):
        return {"candidate_index": int(stripped), "parse_recovered": True}
    try:
        return _parse_json_object(stripped)
    except json.JSONDecodeError:
        match = re.search(r'["\']?candidate_index["\']?\s*:\s*(-?\d+)', stripped)
        if match is None:
            raise
        return {
            "candidate_index": int(match.group(1)),
            "parse_recovered": True,
            "raw_truncated_output": stripped,
        }


def _generate_candidate_entries(
    context: Dict[str, Any],
    summary: Dict[str, Any],
    rng: random.Random,
    seed: int,
    *,
    max_batches: int = 3,
    track: Optional[str] = None,
    scalar_config: Optional[str] = None,
    required_operator_substring: Optional[str] = None,
    required_operator_contains_curvature: bool = False,
) -> List[Dict[str, Any]]:
    target_operator_count, force_r_only = _sample_operator_policy(summary, random.Random(seed + 8191))
    if track == "non_eh" or required_operator_substring:
        force_r_only = False
    if track == "eh_anchored" and required_operator_substring:
        target_operator_count = max(2, target_operator_count)
    skeletons = _direct_candidate_catalog(
        context,
        rng=random.Random(seed + 131071),
        target_operator_count=target_operator_count,
        force_r_only=force_r_only,
    )
    if track and track != "mixed":
        skeletons = [
            entry
            for entry in skeletons
            if theory_track_from_operators(entry.get("operators") or []) == track
        ]
    if scalar_config and scalar_config != "mixed":
        skeletons = [
            entry
            for entry in skeletons
            if str(entry.get("scalar_config")) == scalar_config
        ]
    if required_operator_substring:
        skeletons = [
            entry
            for entry in skeletons
            if any(
                required_operator_substring in str(operator)
                and (not required_operator_contains_curvature or "R" in str(operator))
                for operator in entry.get("operators") or []
            )
        ]
    elif required_operator_contains_curvature:
        skeletons = [
            entry
            for entry in skeletons
            if any("R" in str(operator) for operator in entry.get("operators") or [])
        ]
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
    selected = ranked[:MAX_LLM_CANDIDATES]
    for entry in selected:
        entry["target_operator_count"] = target_operator_count
        entry["baseline_control"] = force_r_only
        entry["theory_track"] = track or theory_track_from_operators(entry.get("operators") or [])
        if scalar_config:
            entry["proposal_scalar_constraint"] = scalar_config
        if required_operator_substring:
            entry["proposal_required_operator_substring"] = required_operator_substring
        if required_operator_contains_curvature:
            entry["proposal_required_operator_contains_curvature"] = True
    return selected


def _call_llm_for_choice(
    *,
    candidates: Sequence[Dict[str, Any]],
    summary: Dict[str, Any],
    provider: str,
    model: str,
    base_url: Optional[str],
    api_key_env: str,
    api_timeout: float,
    max_output_tokens: int,
    debug_dir: Optional[Path],
    loop_id: str,
    attempt: int,
) -> Tuple[int, str, Dict[str, Any], Dict[str, Any]]:
    from openai import OpenAI

    provider = _provider_key(provider)
    system, user, schema = _choice_prompt(candidates, summary)
    resolved_key_env = api_key_env or _default_api_key_env(provider, base_url)
    api_key = _resolved_api_key(resolved_key_env, provider, base_url)
    metadata: Dict[str, Any] = {
        "provider": provider,
        "model": model,
        "base_url": base_url,
        "api_key_env": resolved_key_env,
    }
    start = time.monotonic()
    if provider == "openai":
        client_kwargs: Dict[str, Any] = {"timeout": api_timeout}
        if api_key:
            client_kwargs["api_key"] = api_key
        response = OpenAI(**client_kwargs).responses.create(
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
    elif provider == OPENAI_COMPATIBLE_PROVIDER:
        if not base_url:
            raise ValueError("llm_provider=openai_compatible requires --llm-base-url or LLM_BASE_URL.")
        if not api_key:
            raise ValueError(
                f"Missing API key for openai_compatible provider. Set {resolved_key_env} "
                "or pass --llm-api-key-env with a populated environment variable."
            )
        client = OpenAI(api_key=api_key, base_url=base_url, timeout=api_timeout)
        request_options = _openai_compatible_request_options(
            model=model,
            base_url=base_url,
            max_output_tokens=max_output_tokens,
        )
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {
                    "role": "user",
                    "content": (
                        json.dumps(user, ensure_ascii=False)
                        + "\n\nReturn only valid JSON. Do not wrap it in markdown fences."
                    ),
                },
            ],
            **request_options,
        )
        text = _openai_compatible_text(response)
    elif provider == ANTHROPIC_PROVIDER:
        if not api_key:
            raise ValueError(
                f"Missing API key for anthropic provider. Set {resolved_key_env} "
                "or pass --llm-api-key-env with a populated environment variable."
            )
        text, response = _call_anthropic_messages(
            system=system,
            user=user,
            model=model,
            base_url=base_url,
            api_key=api_key,
            api_timeout=api_timeout,
            max_output_tokens=max_output_tokens,
        )
    else:
        raise ValueError(f"Unsupported llm_provider={provider!r}")
    metadata["latency_sec"] = round(time.monotonic() - start, 3)
    usage = _response_usage_payload(response)
    if usage is not None:
        metadata["usage"] = usage
    if not text.strip():
        debug_path = _write_llm_debug(
            debug_dir,
            loop_id=loop_id,
            attempt=attempt,
            event="empty_output",
            payload={**metadata, **_response_debug_payload(response, text)},
        )
        suffix = f"; debug={debug_path}" if debug_path else ""
        raise RuntimeError(f"{provider} response contained no output_text{suffix}")
    try:
        data = _parse_candidate_choice(text)
    except json.JSONDecodeError as exc:
        debug_path = _write_llm_debug(
            debug_dir,
            loop_id=loop_id,
            attempt=attempt,
            event="json_decode_error",
            payload={
                **metadata,
                **_response_debug_payload(response, text),
                "error": f"{type(exc).__name__}: {exc}",
            },
        )
        suffix = f"; debug={debug_path}" if debug_path else ""
        raise json.JSONDecodeError(f"{exc.msg}{suffix}", exc.doc, exc.pos) from exc
    index = int(data["candidate_index"])
    if index < 0 or index >= len(candidates):
        raise ValueError(f"LLM candidate_index out of range: {index}")
    rationale = str(data.get("rationale") or "LLM selected this grammar-generated candidate index.")
    return index, rationale, data, metadata


def propose_entry_with_llm(
    context: Dict[str, Any],
    summary: Dict[str, Any],
    rng: random.Random,
    seed: int,
    *,
    provider: str = DEFAULT_LLM_PROVIDER,
    model: Optional[str] = None,
    base_url: Optional[str] = None,
    api_key_env: str = "",
    max_candidate_batches: int = 3,
    api_timeout: float = 120.0,
    max_retries: int = DEFAULT_LLM_MAX_RETRIES,
    max_output_tokens: int = DEFAULT_LLM_MAX_OUTPUT_TOKENS,
    debug_dir: Optional[Path | str] = None,
    loop_id: str = "loop_unknown",
    track: Optional[str] = None,
    scalar_config: Optional[str] = None,
    required_operator_substring: Optional[str] = None,
    required_operator_contains_curvature: bool = False,
) -> Dict[str, Any]:
    """Generate legal candidates and let an LLM API select one.

    Raises on missing credentials, API failures, or invalid responses so the
    caller can fall back to deterministic proposal generation.
    """

    selected_provider = _provider_key(provider or os.getenv("LLM_PROVIDER") or DEFAULT_LLM_PROVIDER)
    selected_base_url = base_url or os.getenv("LLM_BASE_URL") or os.getenv("OPENAI_BASE_URL") or None
    selected_key_env = api_key_env or os.getenv("LLM_API_KEY_ENV") or _default_api_key_env(selected_provider, selected_base_url)
    selected_model = model or os.getenv("LLM_MODEL") or _default_model(selected_provider)
    candidates = _generate_candidate_entries(
        context,
        summary,
        rng,
        seed,
        max_batches=max_candidate_batches,
        track=track,
        scalar_config=scalar_config,
        required_operator_substring=required_operator_substring,
        required_operator_contains_curvature=required_operator_contains_curvature,
    )
    if not candidates:
        raise RuntimeError("No grammar-generated candidates available for LLM selection")
    debug_path = Path(debug_dir) if debug_dir is not None else None
    errors: List[str] = []
    total_attempts = max(1, int(max_retries) + 1)
    for attempt in range(1, total_attempts + 1):
        try:
            index, rationale, raw_choice, api_metadata = _call_llm_for_choice(
                candidates=candidates,
                summary=summary,
                provider=selected_provider,
                model=selected_model,
                base_url=selected_base_url,
                api_key_env=selected_key_env,
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
                    "provider": selected_provider,
                    "model": selected_model,
                    "base_url": selected_base_url,
                    "api_key_env": selected_key_env,
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
    entry["llm_provider"] = selected_provider
    entry["llm_model"] = selected_model
    entry["llm_base_url"] = selected_base_url
    entry["llm_api_key_env"] = selected_key_env
    entry["llm_latency_sec"] = api_metadata.get("latency_sec")
    if api_metadata.get("usage") is not None:
        entry["llm_usage"] = api_metadata.get("usage")
    entry["llm_rationale"] = rationale
    entry["target_operator_count"] = selected.get("target_operator_count")
    entry["baseline_control"] = bool(selected.get("baseline_control", False))
    entry["theory_track"] = track or theory_track_from_operators(entry.get("operators") or [])
    entry.update(_diversity_metadata(selected, summary))
    if scalar_config:
        entry["proposal_scalar_constraint"] = scalar_config
    if required_operator_substring:
        entry["proposal_required_operator_substring"] = required_operator_substring
    if required_operator_contains_curvature:
        entry["proposal_required_operator_contains_curvature"] = True
    entry["llm_choice"] = {
        "candidate_index": index,
        "candidate_count": len(candidates),
        "raw_choice": raw_choice,
        "attempts_used": attempt,
        "retry_errors": errors,
        "api_metadata": api_metadata,
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
