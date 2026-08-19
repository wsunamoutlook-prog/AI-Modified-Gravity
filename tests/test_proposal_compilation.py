from __future__ import annotations

import io
import json
import pickle
import sys
import tempfile
import types
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

import sympy as sp

from ai_theory_lab.proposal import compile_proposal_to_run
from eom_v5_2.runner import _load_lagrangian_pickle


def _minimal_token_context():
    t = sp.Symbol("t", real=True)
    tensors = {
        "coords": (t,),
        "phi1": sp.Function("phi1")(t),
        "phi2": sp.Function("phi2")(t),
    }
    r_candidate = SimpleNamespace(
        mass_dim=2,
        combo_label="R",
        contraction_label="R",
        symbolic_value=sp.Symbol("R_FLRW"),
        general_label="R",
        sector="gravity",
    )
    masker = SimpleNamespace(all_candidates=[r_candidate])
    return {"tensors": tensors, "masker": masker}


class ProposalCompilationTests(unittest.TestCase):
    def test_eom_loader_resolves_agent_module_dynamic_functions(self) -> None:
        module_name = "ai_theory_lab.synthetic_agent_entrypoint"
        fake_module = types.ModuleType(module_name)
        n_function = sp.Function("N", positive=True)
        n_function.__module__ = module_name
        fake_module.N = n_function
        sys.modules[module_name] = fake_module
        try:
            serialized = pickle.dumps({"expr": n_function(sp.Symbol("t"))})
        finally:
            sys.modules.pop(module_name, None)

        restored = _load_lagrangian_pickle(io.BytesIO(serialized))

        self.assertEqual(restored["expr"].func.__name__, "N")
        self.assertTrue(restored["expr"].func.is_positive)

    def test_clean_checkout_compiles_without_root_lagrangian_catalog(self) -> None:
        proposal = {
            "proposal_id": "clean-token-context",
            "theory": {
                "scalar_config": "phi1_only",
                "potential_types": {"phi1": "quadratic", "phi2": None},
                "operators": [{"candidate": "R", "coefficient": "\\alpha"}],
            },
            "parameter_samples": [{"\\alpha": 0.5}],
        }

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            proposal_path = root / "proposal.json"
            run_dir = root / "run"
            proposal_path.write_text(json.dumps(proposal), encoding="utf-8")

            with mock.patch(
                "ai_theory_lab.proposal._load_token_level_context",
                return_value=_minimal_token_context(),
            ):
                metadata = compile_proposal_to_run(proposal_path, run_dir)

            with (run_dir / "agent_lagrangians.pkl").open("rb") as handle:
                payload = pickle.load(handle)
            lagrangian = next(iter(payload.values()))[0]
            parameter_samples = json.loads(
                (run_dir / "agent_parameter_samples.json").read_text(encoding="utf-8")
            )

        self.assertEqual(metadata["source"], "proposal_json_token_context")
        self.assertEqual(metadata["operators"], ["R"])
        self.assertEqual(lagrangian["scalar_config"], "phi1_only")
        self.assertEqual(lagrangian["n_terms"], 3)
        self.assertEqual(lagrangian["terms"][0]["coeff_symbol"], "\\alpha")
        self.assertEqual(parameter_samples[0]["alpha"], 0.5)

    def test_inactive_scalar_potential_is_rejected(self) -> None:
        proposal = {
            "theory": {
                "scalar_config": "phi1_only",
                "potential_types": {"phi1": "quadratic", "phi2": "axion"},
                "operators": [{"candidate": "R", "coefficient": "\\alpha"}],
            }
        }

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            proposal_path = root / "proposal.json"
            proposal_path.write_text(json.dumps(proposal), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "phi2 potential type must be null"):
                compile_proposal_to_run(proposal_path, root / "run")

    def test_explicit_replay_catalog_must_exist(self) -> None:
        proposal = {
            "source_lagrangians_path": "/definitely/missing/lagrangians.pkl",
            "theory": {
                "scalar_config": "none",
                "potential_types": {"phi1": None, "phi2": None},
                "operators": [{"candidate": "R", "coefficient": "\\alpha"}],
            },
        }

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            proposal_path = root / "proposal.json"
            proposal_path.write_text(json.dumps(proposal), encoding="utf-8")
            with self.assertRaisesRegex(FileNotFoundError, "Explicit replay catalog"):
                compile_proposal_to_run(proposal_path, root / "run")


if __name__ == "__main__":
    unittest.main()
