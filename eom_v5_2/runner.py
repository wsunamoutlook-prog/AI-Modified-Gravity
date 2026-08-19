#!/usr/bin/env python3
"""Run orchestration and file output for EOM v5.2."""

from __future__ import annotations

import io
import os
import pickle
import sys
import time as _time
from datetime import datetime
from multiprocessing import Pool
from pathlib import Path
from typing import Any, Dict, Optional

import multiprocessing as _mp
import sympy as sp
import sympy.core.function as _sympy_function

from .core import (
    DYN_FUNCS,
    DYN_NAMES,
    detect_max_order,
    process_lagrangian,
    self_test,
    t_sym,
    tex,
)


def _install_sympy_pickle_compat() -> None:
    """Support older lagrangians.pkl files made by SymPy versions with _rebuild_undef."""
    main_module = sys.modules.get("__main__")
    if main_module is not None:
        for func in DYN_FUNCS:
            setattr(main_module, func.__name__, func)

    if hasattr(_sympy_function, "_rebuild_undef"):
        return

    def _rebuild_undef(name, assumptions):
        return sp.Function(name, **assumptions)

    _sympy_function._rebuild_undef = _rebuild_undef


class _DynamicFunctionUnpickler(pickle.Unpickler):
    """Resolve FLRW function classes serialized by any agent entry module."""

    _functions = dict(zip(DYN_NAMES, DYN_FUNCS))

    def find_class(self, module: str, name: str):
        function = self._functions.get(name)
        if function is not None and (module == "__main__" or module.startswith("ai_theory_lab.")):
            return function
        return super().find_class(module, name)


def _load_lagrangian_pickle(file_obj):
    return _DynamicFunctionUnpickler(file_obj).load()


def _register_dynamic_functions_for_pickle(obj) -> None:
    """Expose old dynamic Function classes on __main__ so stdlib pickle can write them."""
    main_module = sys.modules.get("__main__")
    if main_module is None:
        return
    for node in sp.preorder_traversal(obj) if isinstance(obj, sp.Basic) else []:
        if getattr(node, "is_Function", False):
            setattr(main_module, node.func.__name__, node.func)
    if isinstance(obj, dict):
        for value in obj.values():
            _register_dynamic_functions_for_pickle(value)
    elif isinstance(obj, (list, tuple)):
        for value in obj:
            _register_dynamic_functions_for_pickle(value)


class _Tee:
    """Mirror stdout to both the terminal and the EOM log file."""

    def __init__(self, *streams):
        self.streams = streams

    def write(self, data):
        for stream in self.streams:
            stream.write(data)

    def flush(self):
        for stream in self.streams:
            stream.flush()


def _project_root() -> Path:
    """Return the project directory that contains the v5.2 entry script."""
    return Path(__file__).resolve().parents[1]


def _env_bool(name: str, default: bool) -> bool:
    value = os.environ.get(name)
    if value is None or value == "":
        return default
    return value.strip().lower() not in {"0", "false", "no", "off"}


def _env_int(name: str, default: Optional[int]) -> Optional[int]:
    value = os.environ.get(name)
    if value is None or value.strip() == "":
        return default
    if value.strip().lower() in {"none", "all"}:
        return None
    return int(value)


def _setup_logging(project_root: Path):
    """Create the timestamped EOM log and redirect stdout through it."""
    log_dir = project_root / "log"
    log_dir.mkdir(exist_ok=True)
    log_path = log_dir / ("eom_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".log")
    log_fh = open(log_path, "w", encoding="utf-8")
    sys.stdout = _Tee(sys.__stdout__, log_fh)
    print(f"[EOM Log] Writing to: {log_path}\n")
    return log_path, log_fh


def _restore_logging(log_path: Path, log_fh) -> None:
    """Restore stdout and close the log file opened by _setup_logging."""
    sys.stdout = sys.__stdout__
    log_fh.close()
    print(f"[EOM Log] Done. Log saved to: {log_path}")


def _process_one(args):
    """Process one Lagrangian while capturing its verbose symbolic output."""
    L_data, global_idx, n_terms, seed, max_allowed = args
    buf = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = buf
    t0 = _time.time()
    try:
        result = process_lagrangian(L_data, global_idx, tex, max_allowed=max_allowed, seed=seed)
    finally:
        dt = _time.time() - t0
        sys.stdout = old_stdout

    summary = None
    if result is not None:
        if result.get("trivial"):
            summary = f"  #{global_idx:3d}  ({n_terms}-term)  TRIVIAL (all zero)  [{dt:.1f}s]"
        else:
            n_free = len(result["free_params"])
            n_det = len([g for g in result["sym_solution"] if g not in result["free_params"]])
            tag = "✓ CLEAN" if result["is_clean"] else "⚠ GHOST"
            sc = result["L_data"].get("scalar_config", "?")
            summary = (f"  #{global_idx:3d}  ({n_terms}-term, {sc})  "
                       f"det={n_det}  free={n_free}  {tag}  [{dt:.1f}s]")
    return result, summary, buf.getvalue()


def _write_summary(out_path: Path, all_results, tex_fn=tex) -> None:
    """Write the human-readable EOM summary consumed by the Builder stage."""
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("EOM Ghost-Free Analysis Results (v5.2 — two scalar fields)\n")
        f.write(f"Date: {datetime.now().isoformat()}\n\n")
        for r in all_results:
            idx = r["index"]
            f.write(f"{'═' * 60}\n")
            f.write(f"Lagrangian #{idx}\n")

            L_data = r.get("L_data")
            if L_data:
                f.write(f"  General:        {L_data['general']}\n")
                f.write(f"  FLRW:           {tex_fn(L_data['substituted'])}\n")
                sc = L_data.get("scalar_config", None)
                if sc is not None:
                    f.write(f"  scalar_config:  {sc}\n")
                    f.write(f"  potential_types: {L_data.get('potential_types', {})}\n")
                else:
                    f.write(f"  has_phi:        {L_data.get('has_phi', False)}\n")
                f.write("  Terms:\n")
                for ti, tt in enumerate(L_data["terms"]):
                    tag = "  (fixed)" if tt.get("fixed") else ""
                    sector_tag = f"  [{tt.get('sector', 'gravity')}]"
                    pot_tag = f"  pot={tt['potential_type']}" if "potential_type" in tt else ""
                    f.write(f"    [{ti+1}] {tt['coeff_symbol']:10s}  "
                            f"dim={tt['mass_dim']}  Λ^{tt['lambda_power']}  "
                            f"{tt['candidate']}{tag}{sector_tag}{pot_tag}\n")

            if r.get("raw_eom"):
                f.write("  Raw EOM:\n")
                for name, eq in r["raw_eom"].items():
                    f.write(f"    E_{name} = {tex_fn(eq)}\n")
                    for fn, fc in zip(DYN_NAMES, DYN_FUNCS):
                        o = detect_max_order(eq, fc, t_sym)
                        if o >= 0:
                            f.write(f"      max order of {fn}: {o}\n")

            if r.get("trivial"):
                f.write("  → TRIVIAL (all coefficients must be zero)\n\n")
                continue

            f.write("  Ghost-free coefficient relations:\n")
            sym_sol = r.get("sym_solution", {})
            for g, val in sym_sol.items():
                tag = "(free)" if g in r["free_params"] else "(determined)"
                f.write(f"    {g} = {val}  {tag}\n")

            if r.get("symbolic_gauged"):
                f.write("  Final EOM (N=1 gauge, ghost-free, symbolic):\n")
                for name, eq in r["symbolic_gauged"].items():
                    f.write(f"    E_{name} = {tex_fn(eq)}\n")
                    for fn, fc in zip(DYN_NAMES, DYN_FUNCS):
                        o = detect_max_order(eq, fc, t_sym)
                        if o >= 0:
                            f.write(f"      max order of {fn}: {o}\n")

            if r.get("symbolic_gauged_matter"):
                f.write("  Final EOM (N=1 gauge, ghost-free, symbolic, +dust):\n")
                for name, eq in r["symbolic_gauged_matter"].items():
                    f.write(f"    E_{name} = {tex_fn(eq)}\n")
                    for fn, fc in zip(DYN_NAMES, DYN_FUNCS):
                        o = detect_max_order(eq, fc, t_sym)
                        if o >= 0:
                            f.write(f"      max order of {fn}: {o}\n")

            f.write(f"  Ghost-free: {'YES' if r['is_clean'] else 'NO'}\n")
            f.write("\n")


def run_eom(settings: Optional[Dict[str, Any]] = None) -> None:
    """Load lagrangians.pkl, compute EOMs, and write summary/pickle outputs."""
    settings = settings or {}
    _install_sympy_pickle_compat()
    project_root = Path(settings.get("PROJECT_ROOT") or os.environ.get("EOM_PROJECT_ROOT") or _project_root())
    log_path, log_fh = _setup_logging(project_root)

    try:
        if _env_bool("EOM_RUN_SELF_TEST", bool(settings.get("RUN_SELF_TEST", True))):
            self_test()

        default_lagrangians = project_root / "lagrangians.pkl"
        pkl_path = Path(settings.get("LAGRANGIANS_PATH") or os.environ.get("EOM_LAGRANGIANS_PATH") or default_lagrangians)
        if not pkl_path.exists():
            print("=" * 70)
            print("  ERROR: lagrangians.pkl not found")
            print(f"  Expected at: {pkl_path}")
            print()
            print("  Please run GR_grammar_masker_v3.2.py first to generate it:")
            print("    python3 GR_grammar_masker_v3.2.py")
            print("=" * 70)
            sys.exit(1)

        print("=" * 70)
        print(f"  Loading Lagrangians from: {pkl_path}")
        print("=" * 70)

        t0_load = _time.time()
        with open(pkl_path, "rb") as f:
            lagrangian_results = _load_lagrangian_pickle(f)
        _register_dynamic_functions_for_pickle(lagrangian_results)
        dt_load = _time.time() - t0_load

        total_count = sum(len(v) for v in lagrangian_results.values())
        print(f"  Loaded {total_count} Lagrangians in {dt_load:.2f}s")

        max_terms = _env_int("EOM_MAX_TERMS", settings.get("MAX_TERMS", 12))
        n_samples = _env_int("EOM_N_SAMPLES", settings.get("N_SAMPLES", None))
        n_workers = _env_int("EOM_N_WORKERS", settings.get("N_WORKERS", 1)) or 1
        max_allowed = _env_int("EOM_MAX_ALLOWED_ORDER", settings.get("MAX_ALLOWED_ORDER", 2)) or 2
        seed_base = _env_int("EOM_SEED_BASE", settings.get("SEED_BASE", 42)) or 42

        print("\n  Available Lagrangians:")
        for nt in sorted(lagrangian_results.keys()):
            tag = "  ← skip" if max_terms is not None and nt > max_terms else ""
            print(f"    {nt}-term : {len(lagrangian_results[nt])} Lagrangians{tag}")
        print(f"\n  Config:  MAX_TERMS = {max_terms},  N_SAMPLES = {n_samples}, "
              f"MAX_ALLOWED_ORDER = {max_allowed}")

        jobs = []
        for n_terms in sorted(lagrangian_results.keys()):
            if max_terms is not None and n_terms > max_terms:
                continue
            lags = lagrangian_results[n_terms]
            if not lags:
                continue
            for i, L_data in enumerate(lags[:n_samples]):
                global_idx = sum(len(lagrangian_results.get(k, []))
                                 for k in sorted(lagrangian_results.keys()) if k < n_terms) + i + 1
                jobs.append((L_data, global_idx, n_terms, seed_base + i, max_allowed))

        print(f"\n  Jobs: {len(jobs)} Lagrangians to process")
        try:
            _mp.set_start_method("fork")
        except RuntimeError:
            pass
        print(f"  Workers: {n_workers}")

        t0_all = _time.time()
        if n_workers > 1 and len(jobs) > 1:
            print(f"\n  Parallel processing with {n_workers} workers ...")
            with Pool(n_workers) as pool:
                raw = pool.map(_process_one, jobs)
        else:
            print("\n  Running sequentially ...")
            raw = [_process_one(j) for j in jobs]
        dt_all = _time.time() - t0_all

        all_results = []
        summary_lines = []
        for result, summary, captured in raw:
            print(captured, end="")
            if result is not None:
                all_results.append(result)
            if summary is not None:
                summary_lines.append(summary)

        print(f"\n  Total EOM time: {dt_all:.1f}s  ({dt_all/max(len(jobs),1):.1f}s per Lagrangian)")
        print(f"\n\n{'═' * 70}")
        print("  SUMMARY")
        print(f"{'═' * 70}")
        for line in summary_lines:
            print(line)
        print()

        n_clean = sum(1 for r in all_results if r.get("is_clean"))
        n_trivial = sum(1 for r in all_results if r.get("trivial"))
        n_ghost = sum(1 for r in all_results if not r.get("trivial") and not r.get("is_clean"))
        print(f"  Total processed : {len(all_results)}")
        print(f"  Ghost-free      : {n_clean}")
        print(f"  Trivial (all 0) : {n_trivial}")
        print(f"  Still has ghost : {n_ghost}")

        out_dir = Path(settings.get("OUTPUT_DIR") or os.environ.get("EOM_OUTPUT_DIR") or project_root / "eom_results")
        out_dir.mkdir(exist_ok=True)
        out_path = out_dir / "eom_summary.txt"
        _write_summary(out_path, all_results, tex)
        print(f"\n  Results saved to: {out_path}")

        pkl_out = out_dir / "eom_results.pkl"
        _register_dynamic_functions_for_pickle(all_results)
        with open(pkl_out, "wb") as f:
            pickle.dump(all_results, f, protocol=pickle.HIGHEST_PROTOCOL)
        print(f"  Pickle saved to: {pkl_out}")
    finally:
        _restore_logging(log_path, log_fh)
