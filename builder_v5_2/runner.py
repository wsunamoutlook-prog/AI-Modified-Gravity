#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build-cache orchestration for Builder v5.2."""
from __future__ import annotations

from .core import *
from .core import build_dimless_model_with_timeout, load_eom_summary, parse_models, select_data


def _format_seconds(seconds: float) -> str:
    """Human-readable elapsed/ETA formatting used by build progress logs."""
    seconds = max(0.0, float(seconds))
    if seconds < 60:
        return f"{seconds:.0f}s"
    if seconds < 3600:
        return f"{seconds/60:.1f}m"
    return f"{seconds/3600:.2f}h"


RESULT_SUMMARY_COLUMNS = [
    "lag_id", "scalar_config", "usable", "reject_reason",
    "rhs_solve_method", "general", "free_symbols",
]


def write_csv(path: Path, rows: List[Dict[str, Any]]):
    """Write a small CSV while preserving the first-seen column order."""
    if not rows:
        with path.open("w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=RESULT_SUMMARY_COLUMNS).writeheader()
        return
    keys = []
    for row in rows:
        for k in row.keys():
            if k not in keys:
                keys.append(k)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for row in rows:
            w.writerow(row)


def run_build_cache():
    t0 = time.time()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    data = select_data(DATA_CHOICE)
    print(f"[START] Output directory: {OUTPUT_DIR}", flush=True)
    print(
        f"[START] N_SAMPLES_PER_MODEL={N_SAMPLES_PER_MODEL}, "
        f"parallel={SOLVER_PARALLEL}, workers={N_WORKERS}, "
        f"parallel_threshold={PARALLEL_SAMPLE_THRESHOLD}, "
        f"skip_trivial_dust={SKIP_TRIVIAL_DUST_MODELS}, "
        f"scalar_filter={SCALAR_CONFIG_FILTER}, "
        f"build_simplify={BUILD_SIMPLIFY_MODE}, "
        f"linear_rhs={USE_LINEAR_RHS_SOLVER}, general_solve={ALLOW_GENERAL_SYMBOLIC_SOLVE}, "
        f"build_timeout={BUILD_TIMEOUT_SECONDS:g}s",
        flush=True,
    )

    summary_text = load_eom_summary()
    models_raw = parse_models(summary_text)

    # Optional scalar-configuration filter before symbolic build.
    if SCALAR_CONFIG_FILTER.lower() not in {"", "all"}:
        allowed_configs = {s.strip() for s in SCALAR_CONFIG_FILTER.split(",") if s.strip()}
        before_filter = len(models_raw)
        models_raw = [m for m in models_raw if m.scalar_config in allowed_configs]
        print(
            f"[INFO] scalar_config filter={sorted(allowed_configs)}: "
            f"{before_filter} -> {len(models_raw)} models before build.",
            flush=True,
        )

    # Optional hard cap for quick debugging / chunked scans.
    if MAX_MODELS_TO_BUILD > 0 and len(models_raw) > MAX_MODELS_TO_BUILD:
        before_cap = len(models_raw)
        models_raw = models_raw[:MAX_MODELS_TO_BUILD]
        print(
            f"[INFO] MAX_MODELS_TO_BUILD={MAX_MODELS_TO_BUILD}: "
            f"{before_cap} -> {len(models_raw)} models before build.",
            flush=True,
        )

    print(f"[INFO] Parsed {len(models_raw)} Lagrangian sections from EOM summary.", flush=True)

    # Symbolic dimensionless build can also be slow; make it visible.
    built_models: List[Model] = []
    build_t0 = time.time()
    last_build_print = build_t0
    recent_build_times = []
    for i, m in enumerate(models_raw, 1):
        t_model = time.time()
        bm = build_dimless_model_with_timeout(m, mode=MODE, timeout_seconds=BUILD_TIMEOUT_SECONDS)
        dt_model = time.time() - t_model
        built_models.append(bm)
        recent_build_times.append(dt_model)
        if len(recent_build_times) > 50:
            recent_build_times.pop(0)

        if dt_model >= SLOW_BUILD_SECONDS:
            method = getattr(bm, "rhs_solve_method", "rejected") if not bm.reject_reason else "rejected"
            print(
                f"[SLOW_BUILD] L#{m.lag_id}, scalar_config={m.scalar_config}, "
                f"elapsed={_format_seconds(dt_model)}, method={method}, "
                f"reject={bm.reject_reason}",
                flush=True,
            )

        now = time.time()
        if i == 1 or i == len(models_raw) or now - last_build_print >= PROGRESS_EVERY_SECONDS:
            elapsed = now - build_t0
            rate = i / max(elapsed, 1e-9)
            eta_avg = (len(models_raw) - i) / rate if rate > 0 else float("nan")
            if recent_build_times:
                med_recent = float(np.median(recent_build_times))
                eta_recent = (len(models_raw) - i) * med_recent
            else:
                eta_recent = eta_avg
            n_ready = sum(1 for mm in built_models if not mm.reject_reason)
            n_linear = sum(1 for mm in built_models if getattr(mm, "rhs_solve_method", None) == "linear")
            n_general = sum(1 for mm in built_models if getattr(mm, "rhs_solve_method", None) == "general")
            print(
                f"[BUILD] {i}/{len(models_raw)} models built "
                f"({100*i/max(len(models_raw),1):.1f}%), usable_so_far={n_ready}, "
                f"linear={n_linear}, general={n_general}, "
                f"elapsed={_format_seconds(elapsed)}, ETA_avg={_format_seconds(eta_avg)}, "
                f"ETA_recent={_format_seconds(eta_recent)}",
                flush=True,
            )
            last_build_print = now


    import pickle
    env_cache_path = os.environ.get("BUILD_CACHE_PATH", "").strip()
    cache_path = Path(env_cache_path if env_cache_path else str(OUTPUT_DIR / "built_models_cache.pkl")).expanduser()
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    active_models = [m for m in built_models if not m.reject_reason]
    skipped = [m for m in built_models if m.reject_reason]
    metadata = {
        "cache_format": "built_models_cache_v1",
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "source_script": os.environ.get("BUILDER_SOURCE_SCRIPT", Path(__file__).name),
        "output_dir": str(OUTPUT_DIR),
        "mode": MODE,
        "data_choice_at_build_time": DATA_CHOICE,
        "skip_trivial_dust_models": SKIP_TRIVIAL_DUST_MODELS,
        "scalar_config_filter": SCALAR_CONFIG_FILTER,
        "max_models_to_build": MAX_MODELS_TO_BUILD,
        "build_simplify_mode": BUILD_SIMPLIFY_MODE,
        "use_linear_rhs_solver": USE_LINEAR_RHS_SOLVER,
        "allow_general_symbolic_solve": ALLOW_GENERAL_SYMBOLIC_SOLVE,
        "rhs_simplify_mode": RHS_SIMPLIFY_MODE,
        "build_timeout_seconds": BUILD_TIMEOUT_SECONDS,
        "fix_eh_coefficient": FIX_EH_COEFFICIENT,
        "eh_coefficient_value": EH_COEFFICIENT_VALUE,
        "enforce_eft_cutoff": ENFORCE_EFT_CUTOFF,
        "eft_max_h_over_lambda": EFT_MAX_H_OVER_LAMBDA,
        "built_models_total": len(built_models),
        "active_ivp_models": len(active_models),
        "structurally_skipped_models": len(skipped),
        "run_time_seconds": time.time() - t0,
    }
    payload = {"metadata": metadata, "built_models": built_models}
    with cache_path.open("wb") as f:
        pickle.dump(payload, f, protocol=pickle.HIGHEST_PROTOCOL)

    build_rows = []
    for m in sorted(built_models, key=lambda mm: int(mm.lag_id)):
        build_rows.append({
            "lag_id": m.lag_id,
            "scalar_config": m.scalar_config,
            "usable": not bool(m.reject_reason),
            "reject_reason": m.reject_reason or "",
            "rhs_solve_method": getattr(m, "rhs_solve_method", "") or "",
            "general": m.general,
            "free_symbols": ", ".join(str(s) for s in m.free_symbols),
        })
    write_csv(OUTPUT_DIR / "build_models_summary.csv", build_rows)

    lines = []
    lines.append("AI Modified Gravity: symbolic build cache report")
    lines.append("=" * 78)
    lines.append(f"Cache path: {cache_path}")
    lines.append(f"Run output directory: {OUTPUT_DIR}")
    lines.append(f"Run time: {time.time() - t0:.2f} s")
    lines.append(f"Mode: {MODE}")
    lines.append(f"Parser fast-skip trivial dust models: {SKIP_TRIVIAL_DUST_MODELS}")
    lines.append(f"Scalar config filter: {SCALAR_CONFIG_FILTER}")
    lines.append(f"Built models total: {len(built_models)}")
    lines.append(f"Active IVP models: {len(active_models)}")
    lines.append(f"Structurally skipped / timed out: {len(skipped)}")
    lines.append(f"Build simplify mode: {BUILD_SIMPLIFY_MODE}")
    lines.append(f"Use linear RHS solver: {USE_LINEAR_RHS_SOLVER}; allow general solve: {ALLOW_GENERAL_SYMBOLIC_SOLVE}")
    lines.append(f"Build timeout seconds: {BUILD_TIMEOUT_SECONDS:g}")
    lines.append("")
    lines.append("Skipped / structurally rejected models")
    for m in sorted(skipped, key=lambda mm: int(mm.lag_id)):
        lines.append(f"  L#{m.lag_id}: {m.reject_reason}")
    (OUTPUT_DIR / "build_cache_report.txt").write_text("\n".join(lines), encoding="utf-8")

    try:
        (BASE_OUTPUT_DIR / "latest_built_models_cache_path.txt").write_text(str(cache_path), encoding="utf-8")
    except Exception as exc:
        print(f"[WARN] Could not write latest cache pointer: {type(exc).__name__}: {exc}", flush=True)

    print("\n".join(lines[:15]), flush=True)
    print(f"\nDone. Build cache written to: {cache_path}", flush=True)
    print(f"Build report: {OUTPUT_DIR / 'build_cache_report.txt'}", flush=True)
    print(f"Build summary CSV: {OUTPUT_DIR / 'build_models_summary.csv'}", flush=True)
