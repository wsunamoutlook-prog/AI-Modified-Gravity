#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cache loading and scan orchestration for Solver v5.2."""
from __future__ import annotations

from .core import *
from .core import (
    _format_seconds,
    _merge_worker_output,
    _scan_single_model_worker,
    _seed_for_model,
    _write_partial_progress,
)

# =============================================================================
# Solve-from-cache entry point: Stage 2 only
# =============================================================================

def _find_build_cache_path_for_solve() -> Path:
    env_path = os.environ.get("BUILD_CACHE_PATH", "").strip()
    if env_path:
        p = Path(env_path).expanduser()
        if not p.exists():
            raise FileNotFoundError(f"BUILD_CACHE_PATH does not exist: {p}")
        return p.resolve()

    pointer = BASE_OUTPUT_DIR / "latest_built_models_cache_path.txt"
    if pointer.exists():
        p = Path(pointer.read_text(encoding="utf-8").strip()).expanduser()
        if p.exists():
            return p.resolve()

    candidates = []
    if BASE_OUTPUT_DIR.exists():
        candidates.extend(BASE_OUTPUT_DIR.glob("*/built_models_cache.pkl"))
        candidates.extend(BASE_OUTPUT_DIR.glob("built_models_cache.pkl"))
    candidates = [p for p in candidates if p.exists() and p.is_file()]
    if not candidates:
        raise FileNotFoundError(
            "No built_models_cache.pkl found. Run Solver_v4.6_build_cache.py first, "
            "or set BUILD_CACHE_PATH=/path/to/built_models_cache.pkl."
        )
    return max(candidates, key=lambda p: p.stat().st_mtime).resolve()


def _load_built_models_cache(cache_path: Path) -> Tuple[List[Model], Dict[str, Any]]:
    import pickle

    class _ModelCompatUnpickler(pickle.Unpickler):
        """Map historical Solver class locations onto the packaged modules."""

        _CLASS_MAP = {
            ("__main__", "Model"): Model,
            ("__main__", "SampleResult"): SampleResult,
            ("solver_v5_2_core", "Model"): Model,
            ("solver_v5_2_core", "SampleResult"): SampleResult,
            ("solver_v52_lib", "Model"): Model,
            ("solver_v52_lib", "SampleResult"): SampleResult,
            ("builder_v5_2.core", "Model"): Model,
            ("builder_v5_2_core", "Model"): Model,
        }

        def find_class(self, module, name):
            mapped = self._CLASS_MAP.get((module, name))
            if mapped is not None:
                return mapped
            return super().find_class(module, name)

    with cache_path.open("rb") as f:
        payload = _ModelCompatUnpickler(f).load()
    if isinstance(payload, dict) and "built_models" in payload:
        built_models = payload["built_models"]
        metadata = dict(payload.get("metadata", {}))
    elif isinstance(payload, list):
        built_models = payload
        metadata = {"cache_format": "legacy_list_only"}
    else:
        raise TypeError(f"Unsupported build cache structure: {type(payload)}")
    return built_models, metadata


def _warn_if_cache_build_settings_differ(metadata: Dict[str, Any]):
    checks = {
        "mode": MODE,
        "build_simplify_mode": BUILD_SIMPLIFY_MODE,
        "use_linear_rhs_solver": USE_LINEAR_RHS_SOLVER,
        "allow_general_symbolic_solve": ALLOW_GENERAL_SYMBOLIC_SOLVE,
        "rhs_simplify_mode": RHS_SIMPLIFY_MODE,
        "fix_eh_coefficient": FIX_EH_COEFFICIENT,
        "eh_coefficient_value": EH_COEFFICIENT_VALUE,
        "enforce_eft_cutoff": ENFORCE_EFT_CUTOFF,
        "eft_max_h_over_lambda": EFT_MAX_H_OVER_LAMBDA,
    }
    mismatches = []
    for key, current in checks.items():
        if key in metadata and metadata[key] != current:
            mismatches.append((key, metadata[key], current))
    if mismatches:
        print("[WARN] Current symbolic-build settings differ from cache metadata.", flush=True)
        print("[WARN] This solve will use cached equations; rebuild if those differences are intentional:", flush=True)
        for key, cached, current in mismatches:
            print(f"[WARN]   {key}: cache={cached!r}, current={current!r}", flush=True)


def run_solve_from_cache():
    t0 = time.time()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    sn_data, bao_data = load_current_likelihood_data()
    n_sn = len(sn_data["mu"])
    n_bao = len(bao_data["value"])
    n_total_data = n_sn + n_bao
    cache_path = _find_build_cache_path_for_solve()
    built_models, cache_metadata = _load_built_models_cache(cache_path)
    if MAX_MODELS_TO_BUILD > 0 and len(built_models) > MAX_MODELS_TO_BUILD:
        before_cap = len(built_models)
        built_models = built_models[:MAX_MODELS_TO_BUILD]
        print(
            f"[INFO] MAX_MODELS_TO_BUILD={MAX_MODELS_TO_BUILD}: "
            f"{before_cap} -> {len(built_models)} cached models before solve.",
            flush=True,
        )
    _warn_if_cache_build_settings_differ(cache_metadata)
    models_raw = built_models  # Used only for reporting count below; no EOM parsing/build is performed.
    print(f"[START-SOLVE] Output directory: {OUTPUT_DIR}", flush=True)
    print(f"[START-SOLVE] Loading built model cache: {cache_path}", flush=True)
    print(
        f"[START-SOLVE] N_SAMPLES_PER_MODEL={N_SAMPLES_PER_MODEL}, "
        f"parallel={SOLVER_PARALLEL}, workers={N_WORKERS}, "
        f"parallel_threshold={PARALLEL_SAMPLE_THRESHOLD}, likelihood=DES-SN+DESI-DR2-BAO, "
        f"N_GRID={N_GRID}, RTOL={RTOL:g}, ATOL={ATOL:g}",
        flush=True,
    )
    all_results: List[SampleResult] = []
    best_by_model: Dict[str, SampleResult] = {}
    reject_counts_by_model: Dict[str, Counter] = defaultdict(Counter)

    skipped = [m for m in built_models if m.reject_reason]
    active_models = [m for m in built_models if not m.reject_reason]
    for m in skipped:
        reject_counts_by_model[m.lag_id][m.reject_reason] += N_SAMPLES_PER_MODEL

    print(
        f"[INFO] Built models: total={len(built_models)}, active_IVP={len(active_models)}, "
        f"structurally_skipped={len(skipped)}",
        flush=True,
    )
    print(
        f"[INFO] Total numerical samples scheduled: {len(active_models) * N_SAMPLES_PER_MODEL:,}",
        flush=True,
    )

    # Stable random base seed for reproducibility. RANDOM_SEED=0 chooses a fresh base.
    fallback_seed = int(time.time_ns() % (2**32 - 1))
    scan_t0 = time.time()
    completed = 0
    last_progress_print = scan_t0

    if SOLVER_PARALLEL and len(active_models) > 1 and N_WORKERS > 1:
        ctx = mp.get_context("spawn")
        max_workers = min(N_WORKERS, len(active_models))
        print(f"[SCAN] Starting ProcessPoolExecutor with {max_workers} workers...", flush=True)
        worker_args = [
            (m, MODE, N_SAMPLES_PER_MODEL,
             _seed_for_model(RANDOM_SEED, m.lag_id, fallback_seed), WORKER_SAMPLE_PROGRESS, sn_data, bao_data)
            for m in active_models
        ]
        with ProcessPoolExecutor(max_workers=max_workers, mp_context=ctx) as ex:
            future_to_lag = {ex.submit(_scan_single_model_worker, arg): arg[0].lag_id for arg in worker_args}
            for fut in as_completed(future_to_lag):
                lag_id = future_to_lag[fut]
                try:
                    out = fut.result()
                except Exception as exc:
                    # Worker crashed. Count all samples as rejected for that model.
                    reject_counts_by_model[str(lag_id)][f"worker crashed: {type(exc).__name__}: {exc}"] += N_SAMPLES_PER_MODEL
                    out = {"lag_id": lag_id, "accepted": [], "best": None, "rejects": {}, "elapsed": 0.0, "samples": N_SAMPLES_PER_MODEL, "status": "crashed"}
                _merge_worker_output(out, all_results, best_by_model, reject_counts_by_model)
                completed += 1

                now = time.time()
                should_print = (now - last_progress_print >= PROGRESS_EVERY_SECONDS) or completed == len(active_models)
                if should_print:
                    elapsed = now - scan_t0
                    rate = completed / max(elapsed, 1e-9)
                    eta = (len(active_models) - completed) / rate if rate > 0 else float("nan")
                    accepted_count = len(all_results)
                    best_aic = min((r.aic for r in best_by_model.values()), default=math.inf)
                    print(
                        f"[PROGRESS] completed_models={completed}/{len(active_models)} "
                        f"({100*completed/max(len(active_models),1):.1f}%), "
                        f"accepted_samples={accepted_count}, best_AIC={best_aic:.6g}, "
                        f"elapsed={_format_seconds(elapsed)}, ETA={_format_seconds(eta)}",
                        flush=True,
                    )
                    last_progress_print = now

                if PROGRESS_SAVE_EVERY_MODELS > 0 and (completed % PROGRESS_SAVE_EVERY_MODELS == 0):
                    _write_partial_progress(OUTPUT_DIR, all_results, best_by_model, reject_counts_by_model, label="partial")
                    print(f"[CHECKPOINT] Partial CSVs written in {OUTPUT_DIR}", flush=True)
    else:
        print("[SCAN] Running serial scan with lambdify cached once per model...", flush=True)
        for m in active_models:
            seed = _seed_for_model(RANDOM_SEED, m.lag_id, fallback_seed)
            out = _scan_single_model_worker((m, MODE, N_SAMPLES_PER_MODEL, seed, WORKER_SAMPLE_PROGRESS, sn_data, bao_data))
            _merge_worker_output(out, all_results, best_by_model, reject_counts_by_model)
            completed += 1
            now = time.time()
            elapsed = now - scan_t0
            rate = completed / max(elapsed, 1e-9)
            eta = (len(active_models) - completed) / rate if rate > 0 else float("nan")
            best_aic = min((r.aic for r in best_by_model.values()), default=math.inf)
            print(
                f"[PROGRESS] completed_models={completed}/{len(active_models)} "
                f"({100*completed/max(len(active_models),1):.1f}%), "
                f"L#{m.lag_id} accepted={len(out.get('accepted', []))}, "
                f"best_AIC={best_aic:.6g}, elapsed={_format_seconds(elapsed)}, ETA={_format_seconds(eta)}",
                flush=True,
            )
            if PROGRESS_SAVE_EVERY_MODELS > 0 and (completed % PROGRESS_SAVE_EVERY_MODELS == 0):
                _write_partial_progress(OUTPUT_DIR, all_results, best_by_model, reject_counts_by_model, label="partial")
                print(f"[CHECKPOINT] Partial CSVs written in {OUTPUT_DIR}", flush=True)

    # Final checkpoint before report/plots.
    _write_partial_progress(OUTPUT_DIR, all_results, best_by_model, reject_counts_by_model, label="partial")

    accepted = sorted(all_results, key=lambda r: (r.aic, r.chi2))
    model_best_list = sorted(best_by_model.values(), key=lambda r: (r.aic, r.chi2))
    best = accepted[0] if accepted else None
    lcdm = lcdm_fit_reference(sn_data, bao_data)

    write_csv(OUTPUT_DIR / "accepted_samples_summary.csv", [result_row(r) for r in accepted])
    write_csv(OUTPUT_DIR / "model_ranking.csv", [result_row(r) for r in model_best_list])
    write_best_solution(best, OUTPUT_DIR / "best_solution.csv")
    plot_best(best, OUTPUT_DIR / "best_fit_Hz.png")

    for rank, r in enumerate(model_best_list[:10], 1):
        write_best_solution(r, OUTPUT_DIR / f"top_{rank:02d}_lagrangian_{r.lag_id}_solution.csv")

    rej_rows = []
    for lid, cnt in sorted(reject_counts_by_model.items(), key=lambda kv: int(kv[0])):
        total = sum(cnt.values())
        for reason, n in cnt.most_common(8):
            rej_rows.append({"lag_id": lid, "count": n, "total_rejected_or_skipped": total, "reason": reason})
    write_csv(OUTPUT_DIR / "reject_reasons_by_model.csv", rej_rows)

    lines = []
    lines.append("AI Modified Gravity: DES-SN + DESI-DR2 BAO solve stage (v5.2 — two scalars)")
    lines.append("=" * 78)
    lines.append(f"Base output directory: {BASE_OUTPUT_DIR}")
    lines.append(f"Run output directory: {OUTPUT_DIR}")
    lines.append(f"Run time: {time.time() - t0:.2f} s")
    lines.append(f"Mode: {MODE}")
    lines.append("Likelihood: chi2_total = chi2_DES_SN + chi2_DESI_DR2_BAO")
    lines.append(
        f"DES SN: N_SN={n_sn}; zHD range=[{float(np.min(sn_data['zHD'])):.6g}, {float(np.max(sn_data['zHD'])):.6g}]; "
        f"cov_mode={sn_data['cov_mode']}; observable=MU"
    )
    lines.append(
        f"DESI DR2 BAO: N_BAO={n_bao}; z range=[{float(np.min(bao_data['z'])):.6g}, {float(np.max(bao_data['z'])):.6g}]; "
        f"quantity_counts={dict(Counter(bao_data['quantity'].tolist()))}"
    )
    lines.append(f"Total N_data={n_total_data}")
    lines.append(f"Cached models loaded: {len(models_raw)}")
    lines.append(f"Active nontrivial IVP models: {sum(1 for m in built_models if not m.reject_reason)}")
    lines.append(f"Samples per model: {N_SAMPLES_PER_MODEL}")
    lines.append(f"Parallel enabled: {SOLVER_PARALLEL}; workers={N_WORKERS if SOLVER_PARALLEL else 1}")
    lines.append(f"Parallel auto threshold: N_SAMPLES_PER_MODEL > {PARALLEL_SAMPLE_THRESHOLD}")
    lines.append(f"Cache build simplify mode expected by this run: {BUILD_SIMPLIFY_MODE}")
    lines.append(f"Cache RHS extraction settings expected by this run: linear={USE_LINEAR_RHS_SOLVER}; general={ALLOW_GENERAL_SYMBOLIC_SOLVE}")
    lines.append(f"Accepted samples: {len(accepted)}")
    lines.append("")
    lines.append("Physics conventions")
    lines.append("- Uses x=ln(a)=-ln(1+z), h=H/H0.")
    lines.append("- Scalar field 1: varphi1=phi1/Mp, q1=dvarphi1/dx.  phi1 is Planck-scale.")
    lines.append("- Scalar field 2: varphi2=phi2/Lambda, q2=dvarphi2/dx.  phi2 is EFT-cutoff-scale.")
    lines.append("- Masses: mu1=m1/H0, mu2=m2/Lambda.")
    lines.append("- Decay constants: fbar1=f1/Mp, fbar2=f2/Lambda.")
    lines.append("- EFT cutoff: lambda_H=Lambda/H0.")
    lines.append("- Default physical EFT mode keeps eps_HM=H0/Mp in the dimensionless equations.")
    lines.append("- EOMs are normalized by Mp^2 H0^2 after substitution.")
    lines.append(f"- EFT validity cut: max_x |h|/lambda_H < {EFT_MAX_H_OVER_LAMBDA:g} (enabled={ENFORCE_EFT_CUTOFF}).")
    lines.append(f"- EH coefficient fixed to {EH_COEFFICIENT_VALUE:g} when detected (enabled={FIX_EH_COEFFICIENT}).")
    lines.append("- a0 and h0 are fixed to 1.")
    lines.append("- q1_0 is solved from E_N(x=0)=0 for phi1 models; q2_0 for phi2-only models.")
    lines.append("- rho_m0 is sampled as rho_bar=3 Omega_m0.")
    lines.append("- Mp = 2.435e27 eV (physical reduced Planck mass).")
    lines.append("")
    lines.append("Flat-LambdaCDM reference fit")
    lines.append(
        f"  chi2_total={lcdm['chi2']:.6g}, chi2_DES_SN={lcdm['chi2_sn']:.6g}, "
        f"chi2_DESI_BAO={lcdm['chi2_bao']:.6g}, chi2/N={lcdm['chi2_per_point']:.6g}, "
        f"AIC={lcdm['AIC']:.6g}, BIC={lcdm['BIC']:.6g}"
    )
    lines.append(f"  M_SN_hat={lcdm['sn_offset_hat']}, alpha_BAO_hat={lcdm['bao_alpha_hat']}")
    lines.append(f"  H0={lcdm['H0']:.6g}, Omega_m0={lcdm['Omega_m0']:.6g}")
    lines.append("")

    if best is None:
        lines.append("No accepted model sample was found.  Check reject_reasons_by_model.csv.")
    else:
        bm = next((m for m in built_models if m.lag_id == best.lag_id), None)
        lines.append("Best sample by AIC")
        lines.append(f"  Lagrangian #{best.lag_id}")
        lines.append(
            f"  chi2_total={best.chi2:.6g}, chi2_DES_SN={best.chi2_sn:.6g}, "
            f"chi2_DESI_BAO={best.chi2_bao:.6g}, M_SN_hat={best.sn_offset_hat}, "
            f"alpha_BAO_hat={best.bao_alpha_hat}, "
            f"chi2/N={best.chi2_per_point:.6g}, AIC={best.aic:.6g}, BIC={best.bic:.6g}, k={best.k_params}"
        )
        lines.append(f"  max |constraint|={best.max_abs_constraint:.3e}")
        if bm:
            lines.append(f"  General: {bm.general}")
            lines.append(f"  Scalar config: {bm.scalar_config}")
            lines.append(f"  Ghost-free relations: {bm.gf_relations}")
            lines.append("  Free symbols: " + ", ".join(str(s) for s in bm.free_symbols))
        lines.append("  Parameters:")
        for kk, vv in sorted(best.params.items()):
            lines.append(f"    {kk} = {vv:.12g}")
    lines.append("")
    lines.append("Top models by AIC")
    if not model_best_list:
        lines.append("  None")
    else:
        for rank, r in enumerate(model_best_list[:20], 1):
            lines.append(
                f"  {rank:02d}. L#{r.lag_id}: chi2_total={r.chi2:.6g}, "
                f"chi2_DES_SN={r.chi2_sn:.6g}, chi2_DESI_BAO={r.chi2_bao:.6g}, "
                f"M_SN_hat={r.sn_offset_hat}, alpha_BAO_hat={r.bao_alpha_hat}, AIC={r.aic:.6g}, BIC={r.bic:.6g}, "
                f"k={r.k_params}, maxC={r.max_abs_constraint:.2e}"
            )
            m = next((mm for mm in built_models if mm.lag_id == r.lag_id), None)
            if m:
                lines.append(f"      General: {m.general}")
                lines.append(f"      Config: {m.scalar_config}")
                lines.append(f"      GF: {m.gf_relations}")

    lines.append("")
    lines.append("Skipped / structurally rejected models")
    for m in sorted(built_models, key=lambda mm: int(mm.lag_id)):
        if m.reject_reason:
            lines.append(f"  L#{m.lag_id}: {m.reject_reason}")

    lines.append("")
    lines.append("Files written")
    for fn in ["scan_report.txt", "model_ranking.csv", "accepted_samples_summary.csv",
               "best_solution.csv", "best_fit_Hz.png", "reject_reasons_by_model.csv",
               "accepted_samples_summary_partial.csv", "model_ranking_partial.csv", "reject_reasons_by_model_partial.csv"]:
        lines.append(f"  {OUTPUT_DIR / fn}")
    (OUTPUT_DIR / "scan_report.txt").write_text("\n".join(lines), encoding="utf-8")

    print("\n".join(lines[:45]), flush=True)
    print(f"\nDone. Full report: {OUTPUT_DIR / 'scan_report.txt'}", flush=True)
