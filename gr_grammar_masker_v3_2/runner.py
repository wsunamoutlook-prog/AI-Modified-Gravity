#!/usr/bin/env python3
"""Run orchestration and file output for GR grammar masker v3.2."""

from __future__ import annotations

import os
import pickle
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, Tuple


def _register_dynamic_functions_for_pickle(obj) -> None:
    """Expose SymPy undefined Function classes on __main__ before stdlib pickle writes."""
    import sympy as sp

    main_module = sys.modules.get("__main__")
    if main_module is None:
        return
    if isinstance(obj, sp.Basic):
        for node in sp.preorder_traversal(obj):
            if getattr(node, "is_Function", False):
                setattr(main_module, node.func.__name__, node.func)
        return
    if isinstance(obj, dict):
        for value in obj.values():
            _register_dynamic_functions_for_pickle(value)
    elif isinstance(obj, (list, tuple)):
        for value in obj:
            _register_dynamic_functions_for_pickle(value)


class _Tee:
    """Mirror stdout to both the terminal and the masker log file."""

    def __init__(self, *streams):
        self.streams = streams

    def write(self, data):
        for stream in self.streams:
            stream.write(data)

    def flush(self):
        for stream in self.streams:
            stream.flush()


def _project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _env_bool(name: str, default: bool) -> bool:
    value = os.environ.get(name)
    if value is None or value.strip() == "":
        return default
    return value.strip().lower() not in {"0", "false", "no", "off"}


def _env_int(name: str, default: int) -> int:
    value = os.environ.get(name)
    if value is None or value.strip() == "":
        return default
    return int(value)


def _env_tuple_int(name: str, default: Tuple[int, ...]) -> Tuple[int, ...]:
    value = os.environ.get(name)
    if value is None or value.strip() == "":
        return default
    parts = [p.strip() for p in value.replace(";", ",").split(",") if p.strip()]
    return tuple(int(p) for p in parts)


def _setup_logging(project_root: Path):
    log_dir = project_root / "log"
    log_dir.mkdir(exist_ok=True)
    log_path = log_dir / (datetime.now().strftime("%Y%m%d_%H%M%S") + ".log")
    log_fh = open(log_path, "w", encoding="utf-8")
    sys.stdout = _Tee(sys.__stdout__, log_fh)
    print(f"[Log] Writing output to: {log_path}\n")
    return log_path, log_fh


def _restore_logging(log_path: Path, log_fh) -> None:
    sys.stdout = sys.__stdout__
    log_fh.close()
    print(f"[Log] Done. Output saved to: {log_path}")


def _build_tensors_dict() -> Dict[str, Any]:
    """Create the tensor dictionary consumed by GravityMasker methods."""
    from .tensor import Gamma, R_scalar, Ricci, Riemann, coords, cov_deriv, g, g_inv, sp, t

    return {
        "g": g,
        "g_inv": g_inv,
        "Gamma": Gamma,
        "Riemann": Riemann,
        "Ricci": Ricci,
        "R_scalar": R_scalar,
        "phi1": sp.Function("phi1")(t),
        "phi2": sp.Function("phi2")(t),
        "coords": coords,
        "cov_deriv": cov_deriv,
    }


def _print_grammar_sanity(masker: GravityMasker, dimensions: Tuple[int, ...]) -> None:
    print("\n--- Grammar sanity check ---")
    for d in dimensions:
        combos = masker.generate_all_combos(d)
        print(f"  dim={d}: {len(combos)} combos")
        for c in combos:
            print(f"    {masker.combo_label(c):40s}  tokens: {masker.combo_to_tokens(c)}")
    print()


def _print_sample_lagrangians(lagrangian_results: Dict[int, list], sample_count: int) -> None:
    from .tensor import tex

    print("\n" + "=" * 70)
    print("SAMPLE LAGRANGIANS")
    print("=" * 70)

    for n_terms in sorted(lagrangian_results.keys()):
        lags = lagrangian_results[n_terms]
        if not lags:
            continue
        print(f"\n{'━' * 70}")
        print(f"  {n_terms}-term Lagrangians: {len(lags)} generated")
        print(f"{'━' * 70}")
        for i, L in enumerate(lags[:sample_count]):
            print(f"\n  ── Sample #{i+1} ──")
            print(f"  Scalar config: {L['scalar_config']}")
            print(f"  Potential types: {L['potential_types']}")
            print("  General form:")
            print(f"    {L['general']}")
            print("  Substituted (FLRW):")
            print(f"    {tex(L['substituted'])}")
            print("  Terms:")
            for ti, tt in enumerate(L["terms"]):
                tag = "  (fixed)" if tt.get("fixed") else ""
                sector_tag = f"  [{tt.get('sector', 'gravity')}]"
                pot_tag = f"  pot={tt['potential_type']}" if "potential_type" in tt else ""
                print(f"    [{ti+1}] {tt['coeff_symbol']}, "
                      f"dim={tt['mass_dim']}, Λ^{tt['lambda_power']}, "
                      f"{tt['candidate']}{tag}{sector_tag}{pot_tag}")


def _write_lagrangian_text_files(output_dir: Path, lagrangian_results: Dict[int, list]) -> None:
    from .tensor import tex

    output_dir.mkdir(parents=True, exist_ok=True)
    for n_terms in sorted(lagrangian_results.keys()):
        lags = lagrangian_results[n_terms]
        out_path = output_dir / f"lagrangians_{n_terms}terms.txt"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(f"# Lagrangians with {n_terms} terms\n")
            f.write(f"# Total: {len(lags)}\n\n")
            for i, L in enumerate(lags):
                f.write(f"[Lagrangian #{i+1}]\n")
                f.write(f"General:     {L['general']}\n")
                f.write(f"Substituted: {tex(L['substituted'])}\n")
                f.write(f"scalar_config: {L['scalar_config']}\n")
                f.write(f"potential_types: {L['potential_types']}\n")
                for ti, tt in enumerate(L["terms"]):
                    tag = "  (fixed)" if tt.get("fixed") else ""
                    sector_tag = f"  [{tt.get('sector', 'gravity')}]"
                    pot_tag = f"  pot={tt['potential_type']}" if "potential_type" in tt else ""
                    f.write(f"  term[{ti+1}]: coeff={tt['coeff_symbol']}, "
                            f"dim={tt['mass_dim']}, Λ^{tt['lambda_power']}, "
                            f"{tt['candidate']}{tag}{sector_tag}{pot_tag}\n")
                f.write("\n")
        print(f"  Saved: {out_path}")


def run_masker(settings: Optional[Dict[str, Any]] = None) -> Dict[int, list]:
    """Generate grammar-guided Lagrangians and write text/pickle outputs."""
    settings = settings or {}
    project_root = Path(settings.get("PROJECT_ROOT") or os.environ.get("MASKER_PROJECT_ROOT") or _project_root())
    log_path, log_fh = _setup_logging(project_root)

    try:
        from .grammar import GravityMasker
        from .tensor import tex

        max_derivatives = _env_int("MASKER_MAX_DERIVATIVES", int(settings.get("MAX_DERIVATIVES", 2)))
        dimensions = _env_tuple_int("MASKER_DIMENSIONS", tuple(settings.get("DIMENSIONS", (2, 3, 4, 5, 6))))
        n_terms_list = _env_tuple_int("MASKER_N_TERMS_LIST", tuple(settings.get("N_TERMS_LIST", tuple(range(1, 13)))))
        n_samples = _env_int("MASKER_N_SAMPLES", int(settings.get("N_SAMPLES", 100)))
        seed = _env_int("MASKER_RANDOM_SEED", int(settings.get("RANDOM_SEED", 42)))
        sample_print_count = _env_int("MASKER_SAMPLE_PRINT_COUNT", int(settings.get("SAMPLE_PRINT_COUNT", 3)))
        print_sanity = _env_bool("MASKER_PRINT_GRAMMAR_SANITY", bool(settings.get("PRINT_GRAMMAR_SANITY", True)))
        verbose_dimensions = _env_bool("MASKER_VERBOSE_DIMENSIONS", bool(settings.get("VERBOSE_DIMENSIONS", True)))

        tensors_dict = _build_tensors_dict()
        masker = GravityMasker(max_derivatives=max_derivatives)

        if print_sanity:
            _print_grammar_sanity(masker, dimensions)

        if verbose_dimensions:
            for d in dimensions:
                masker.process_dimension(d, tensors_dict, verbose=True, tex_fn=tex)

        masker.collect_candidates(tensors_dict, dims=dimensions, tex_fn=tex)
        lagrangian_results = masker.generate_lagrangians(
            tensors_dict,
            n_terms_list=n_terms_list,
            n_samples=n_samples,
            seed=seed,
        )

        if sample_print_count > 0:
            _print_sample_lagrangians(lagrangian_results, sample_print_count)

        output_dir = Path(settings.get("OUTPUT_DIR") or os.environ.get("MASKER_OUTPUT_DIR") or project_root / "lagrangians")
        _write_lagrangian_text_files(output_dir, lagrangian_results)

        pkl_path = Path(settings.get("PICKLE_PATH") or os.environ.get("MASKER_PICKLE_PATH") or project_root / "lagrangians.pkl")
        pkl_path.parent.mkdir(parents=True, exist_ok=True)
        _register_dynamic_functions_for_pickle(lagrangian_results)
        with open(pkl_path, "wb") as pkl_file:
            pickle.dump(lagrangian_results, pkl_file)
        print(f"  Pickled to: {pkl_path}")
        return lagrangian_results
    finally:
        _restore_logging(log_path, log_fh)
