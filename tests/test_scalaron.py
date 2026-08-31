import contextlib
import io
import json
import math
import pickle
import random
import tempfile
import unittest
from pathlib import Path

import sympy as sp

from eom_v5_2.core import compute_all_eom, find_high_order_derivs, process_lagrangian
from eom_v5_2.scalaron import (
    Lambda,
    Mp,
    N,
    R_flrw,
    a,
    chi,
    classify_scalaron_sector,
    evaluate_scalaron_health,
    phi1,
    phi2,
    scalarize_lagrangian_data,
    sqrt_mg,
    t,
    verify_legendre_equivalence,
)


def _term(coeff, candidate, dim, lambda_power, sector="gravity"):
    return {
        "coeff_symbol": str(coeff),
        "candidate": candidate,
        "mass_dim": dim,
        "lambda_power": lambda_power,
        "sector": sector,
    }


def _all_second_order(eoms):
    return all(not find_high_order_derivs(eom, max_allowed=2) for eom in eoms.values())


class ScalaronClassificationTests(unittest.TestCase):
    def test_unrelated_operators_are_ordinary_and_expression_is_unchanged(self):
        ordinary_labels = [
            ("R", "gravity"),
            ("φ1 · R", "non-minimal"),
            ("φ1 · φ2 · R", "non-minimal"),
            ("φ1 · ∇^{a}∇_{a}R", "non-minimal"),
            ("R^{ab} · R_{ab}", "gravity"),
            ("∇^{a}R · ∇_{a}R", "gravity"),
        ]
        alpha = sp.Symbol(r"\alpha")
        for label, sector in ordinary_labels:
            with self.subTest(label=label):
                raw = sqrt_mg * alpha * (R_flrw + 1)
                data = {
                    "general": label,
                    "substituted": raw,
                    "terms": [_term(alpha, label, 4, 0, sector)],
                }
                transformed = scalarize_lagrangian_data(data)
                self.assertEqual(transformed["scalaron"]["classification"], "ordinary")
                self.assertFalse(transformed["scalaron"]["enabled"])
                self.assertEqual(sp.expand(transformed["substituted"] - raw), 0)
                self.assertNotIn("raw_substituted", transformed)

    def test_only_exact_algebraic_nonlinear_r_monomials_are_selected(self):
        labels = [
            "R · R",
            "φ1 · R · R",
            "φ2 · R · R",
            "φ1 · φ1 · R · R",
            "φ1 · φ2 · R · R",
            "φ2 · φ2 · R · R",
            "R · R · R",
        ]
        alpha = sp.Symbol(r"\alpha")
        for label in labels:
            with self.subTest(label=label):
                result = classify_scalaron_sector([_term(alpha, label, 6, -4)])
                self.assertTrue(result["enabled"])
                self.assertEqual(result["classification"], "scalarizable")

        for label in ["R · R^{ab} · R_{ab}", "□R", "∇^{a}∇_{a}R · R^{c}_{c}"]:
            with self.subTest(label=label):
                result = classify_scalaron_sector([_term(alpha, label, 6, -4)])
                self.assertFalse(result["enabled"])

    def test_hybrid_classification_preserves_residual_operator(self):
        alpha, beta = sp.symbols(r"\alpha \beta")
        residual = sp.diff(R_flrw, t) ** 2
        raw = sqrt_mg * Mp**2 * (
            alpha * Lambda**-2 * R_flrw**2 + beta * Lambda**-4 * residual
        )
        data = {
            "general": "hybrid",
            "substituted": raw,
            "terms": [
                _term(alpha, "R · R", 4, -2),
                _term(beta, "∇^{a}R · ∇_{a}R", 6, -4),
            ],
        }
        transformed = scalarize_lagrangian_data(data)
        self.assertEqual(transformed["scalaron"]["classification"], "hybrid")
        expected_residual = sqrt_mg * Mp**2 * beta * Lambda**-4 * residual
        recovered_residual = transformed["substituted"] - (
            sqrt_mg * Mp**2 * transformed["scalaron"]["scalarized_sector"]
        )
        self.assertEqual(sp.simplify(recovered_residual - expected_residual), 0)


class ScalaronEomTests(unittest.TestCase):
    def _quadratic_data(self):
        alpha = sp.Symbol(r"\alpha")
        beta = sp.Symbol(r"\beta")
        raw = sqrt_mg * Mp**2 * (
            alpha * R_flrw + beta * Lambda**-2 * R_flrw**2
        )
        return {
            "general": "sqrt(-g) M_p^2 (alpha R + beta Lambda^-2 R^2)",
            "substituted": raw,
            "terms": [
                _term(alpha, "R", 2, 0),
                _term(beta, "R · R", 4, -2),
            ],
            "scalar_config": "none",
            "potential_types": {"phi1": None, "phi2": None},
        }

    def test_quadratic_raw_is_higher_order_but_scalaron_form_is_second_order(self):
        data = self._quadratic_data()
        transformed = scalarize_lagrangian_data(data)
        self.assertTrue(verify_legendre_equivalence(transformed))
        self.assertNotEqual(sp.simplify(transformed["scalaron"]["f_RR"]), 0)

        with contextlib.redirect_stdout(io.StringIO()):
            raw_eoms = compute_all_eom(data["substituted"])
            scalarized_eoms = compute_all_eom(transformed["substituted"])

        self.assertTrue(any(find_high_order_derivs(eq, max_allowed=2) for eq in raw_eoms.values()))
        self.assertEqual(set(scalarized_eoms), {"N", "a", "chi"})
        self.assertTrue(_all_second_order(scalarized_eoms))

    def test_mixed_f_of_r_phi1_phi2_is_equivalent_and_second_order(self):
        alpha, beta = sp.symbols(r"\alpha \beta")
        phi1_dot = sp.diff(phi1, t)
        phi2_dot = sp.diff(phi2, t)
        gravity = alpha * R_flrw + beta * Lambda**-4 * phi1 * phi2 * R_flrw**2
        matter = (phi1_dot**2 + phi2_dot**2) / (2 * N**2)
        raw = sqrt_mg * (Mp**2 * gravity + matter)
        data = {
            "general": "mixed f(R,phi1,phi2)",
            "substituted": raw,
            "terms": [
                _term(alpha, "R", 2, 0),
                _term(beta, "φ1 · φ2 · R · R", 6, -4, "non-minimal"),
            ],
            "scalar_config": "both",
            "potential_types": {"phi1": "quadratic", "phi2": "quadratic"},
        }
        transformed = scalarize_lagrangian_data(data)
        self.assertTrue(verify_legendre_equivalence(transformed))
        with contextlib.redirect_stdout(io.StringIO()):
            eoms = compute_all_eom(transformed["substituted"])
        self.assertEqual(set(eoms), {"N", "a", "phi1", "phi2", "chi"})
        self.assertTrue(_all_second_order(eoms))

    def test_every_supported_nonlinear_r_family_has_second_order_scalaron_eoms(self):
        alpha, beta = sp.symbols(r"\alpha \beta")
        families = [
            ("R · R", R_flrw**2, -2, "none", set()),
            ("R · R · R", R_flrw**3, -4, "none", set()),
            ("φ1 · R · R", phi1 * R_flrw**2, -3, "phi1_only", {"phi1"}),
            ("φ2 · R · R", phi2 * R_flrw**2, -3, "phi2_only", {"phi2"}),
            ("φ1 · φ1 · R · R", phi1**2 * R_flrw**2, -4, "phi1_only", {"phi1"}),
            ("φ1 · φ2 · R · R", phi1 * phi2 * R_flrw**2, -4, "both", {"phi1", "phi2"}),
            ("φ2 · φ2 · R · R", phi2**2 * R_flrw**2, -4, "phi2_only", {"phi2"}),
        ]
        for label, nonlinear, lambda_power, scalar_config, matter_fields in families:
            with self.subTest(label=label):
                matter = 0
                if "phi1" in matter_fields:
                    matter += sp.diff(phi1, t) ** 2 / (2 * N**2)
                if "phi2" in matter_fields:
                    matter += sp.diff(phi2, t) ** 2 / (2 * N**2)
                data = {
                    "general": label,
                    "substituted": sqrt_mg * (
                        Mp**2 * (alpha * R_flrw + beta * Lambda**lambda_power * nonlinear)
                        + matter
                    ),
                    "terms": [
                        _term(alpha, "R", 2, 0),
                        _term(beta, label, 2 - lambda_power, lambda_power),
                    ],
                    "scalar_config": scalar_config,
                }
                transformed = scalarize_lagrangian_data(data)
                self.assertTrue(verify_legendre_equivalence(transformed))
                with contextlib.redirect_stdout(io.StringIO()):
                    eoms = compute_all_eom(transformed["substituted"])
                self.assertEqual(set(eoms), {"N", "a", "chi", *matter_fields})
                self.assertTrue(_all_second_order(eoms))
                health = evaluate_scalaron_health(
                    transformed,
                    {
                        alpha: sp.Rational(1, 2),
                        beta: sp.Rational(1, 100),
                        Lambda: 1,
                        chi: 1,
                        phi1: 1,
                        phi2: 1,
                    },
                )
                self.assertTrue(health["healthy"])

    def test_process_lagrangian_applies_scalaron_before_order_filter(self):
        with contextlib.redirect_stdout(io.StringIO()):
            result = process_lagrangian(self._quadratic_data(), 1, max_allowed=2)
        self.assertIsNotNone(result)
        self.assertFalse(result["trivial"])
        self.assertTrue(result["is_clean"])
        self.assertTrue(result["L_data"]["scalaron"]["enabled"])

    def test_positive_quadratic_branch_passes_local_health_checks(self):
        data = scalarize_lagrangian_data(self._quadratic_data())
        alpha = sp.Symbol(r"\alpha")
        beta = sp.Symbol(r"\beta")
        health = evaluate_scalaron_health(data, {
            alpha: sp.Rational(1, 2),
            beta: sp.Rational(1, 10),
            Lambda: 1,
            chi: 2,
        })
        self.assertTrue(health["healthy"])
        self.assertTrue(health["effective_planck_mass_positive"])
        self.assertTrue(health["dolgov_kawasaki_stable"])
        self.assertTrue(health["scalaron_mass_squared_positive"])

    def test_negative_quadratic_branch_fails_local_health_checks(self):
        data = scalarize_lagrangian_data(self._quadratic_data())
        alpha = sp.Symbol(r"\alpha")
        beta = sp.Symbol(r"\beta")
        health = evaluate_scalaron_health(data, {
            alpha: 1,
            beta: -sp.Rational(1, 10),
            Lambda: 1,
            chi: 2,
        })
        self.assertFalse(health["healthy"])
        self.assertFalse(health["dolgov_kawasaki_stable"])

    def test_ordinary_eh_scalar_path_does_not_gain_a_chi_equation(self):
        alpha = sp.Symbol(r"\alpha")
        raw = sqrt_mg * (Mp**2 * alpha * R_flrw + sp.diff(phi1, t) ** 2 / (2 * N**2))
        data = {
            "general": "EH plus scalar",
            "substituted": raw,
            "terms": [_term(alpha, "R", 2, 0)],
        }
        transformed = scalarize_lagrangian_data(data)
        with contextlib.redirect_stdout(io.StringIO()):
            eoms = compute_all_eom(transformed["substituted"])
        self.assertEqual(set(eoms), {"N", "a", "phi1"})
        self.assertTrue(_all_second_order(eoms))
        self.assertFalse(transformed["substituted"].has(chi))


class ScalaronPipelineTests(unittest.TestCase):
    def _processed_quadratic(self):
        alpha = sp.Symbol(r"\alpha")
        beta = sp.Symbol(r"\beta")
        data = {
            "general": "√(-g) [ M_p² ( \\alpha · R + \\beta Λ^{-2} · R · R ) ]",
            "substituted": sqrt_mg * Mp**2 * (
                alpha * R_flrw + beta * Lambda**-2 * R_flrw**2
            ),
            "terms": [
                _term(alpha, "R", 2, 0),
                _term(beta, "R · R", 4, -2),
            ],
            "scalar_config": "none",
            "potential_types": {"phi1": None, "phi2": None},
        }
        with contextlib.redirect_stdout(io.StringIO()):
            return process_lagrangian(data, 1, max_allowed=2)

    def _built_quadratic(self):
        import builder_v5_2.core as builder
        from eom_v5_2.runner import _write_summary

        result = self._processed_quadratic()
        with tempfile.TemporaryDirectory() as directory:
            summary_path = Path(directory) / "eom_summary.txt"
            _write_summary(summary_path, [result])
            with contextlib.redirect_stdout(io.StringIO()):
                models = builder.parse_models(summary_path.read_text(encoding="utf-8"))
        self.assertEqual(len(models), 1)
        old_fix = builder.FIX_EH_COEFFICIENT
        try:
            builder.FIX_EH_COEFFICIENT = True
            model = builder.build_dimless_model(models[0], mode="eft")
        finally:
            builder.FIX_EH_COEFFICIENT = old_fix
        return model

    def test_builder_constructs_scalarons_ivp_and_health_expressions(self):
        model = self._built_quadratic()
        self.assertTrue(model.has_scalaron)
        self.assertIsNone(model.reject_reason)
        self.assertEqual(set(model.rhs_exprs), {"hx", "qchix"})
        self.assertIn("scalaron_F", model.dimless_exprs)
        self.assertIn("scalaron_f_RR", model.dimless_exprs)
        self.assertIn("scalaron_mass_squared", model.dimless_exprs)

    def test_solver_accepts_one_healthy_complete_scalaron_trajectory(self):
        import numpy as np
        import solver_v5_2.core as solver

        model = self._built_quadratic()
        with contextlib.redirect_stdout(io.StringIO()):
            sn_data, bao_data = solver.load_current_likelihood_data()
        chi0 = 6.0 + math.sqrt(36.0 + 2.1 * 10.0**2 / 100.0)
        sample = {
            "H0_km_s_Mpc": 70.0,
            "Omega_m0": 0.3,
            "lambda_H_Lambda_over_H0": 10.0,
            "beta": 100.0,
            "chi_bar_0_R_over_H0sq": chi0,
        }
        result = solver.evaluate_sample(
            model,
            np.random.default_rng(1),
            "eft",
            sn_data=sn_data,
            bao_data=bao_data,
            agent_sample=sample,
        )
        self.assertTrue(result.success, result.reason)
        self.assertTrue(math.isfinite(result.chi2))
        self.assertIsNotNone(result.chi_bar_grid)
        self.assertIsNotNone(result.qchi_grid)

    def test_agent_sampler_adds_scalaron_initial_data_only_when_needed(self):
        from ai_theory_lab.cold_start_runner import _parameter_sample

        base = {
            "scalar_config": "phi1_only",
            "operator_specs": [
                {"candidate": "R", "coefficient": r"\alpha"},
                {"candidate": "R · R", "coefficient": r"\beta"},
            ],
            "lagrangian": {
                "terms": [
                    _term(sp.Symbol(r"\alpha"), "R", 2, 0),
                    _term(sp.Symbol(r"\beta"), "R · R", 4, -2),
                ],
            },
        }
        scalaron_entry = {
            **base,
            "scalaron": {"enabled": True, "classification": "scalarizable"},
        }
        ordinary_entry = {
            **base,
            "scalaron": {"enabled": False, "classification": "ordinary"},
        }
        scalaron_sample = _parameter_sample(scalaron_entry, random.Random(1), 0, {})
        ordinary_sample = _parameter_sample(ordinary_entry, random.Random(1), 0, {})
        self.assertIn("chi_bar_0_R_over_H0sq", scalaron_sample)
        self.assertIn("q1_0_dvarphi1_dln_a", scalaron_sample)
        self.assertNotIn("chi_bar_0_R_over_H0sq", ordinary_sample)
        self.assertNotIn("q1_0_dvarphi1_dln_a", ordinary_sample)

    def test_fresh_proposal_json_compiles_without_legacy_catalog_entry(self):
        from ai_theory_lab.proposal import compile_proposal_to_run

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            proposal_path = root / "proposal.json"
            run_dir = root / "run"
            proposal_path.write_text(json.dumps({
                "proposal_id": "fresh-r-plus-r2",
                "source_lagrangians_path": str(root / "missing-legacy-catalog.pkl"),
                "theory": {
                    "scalar_config": "none",
                    "potential_types": {"phi1": None, "phi2": None},
                    "operators": [
                        {"candidate": "R", "coefficient": r"\alpha"},
                        {"candidate": "R · R", "coefficient": r"\beta"},
                    ],
                },
                "parameter_samples": [{
                    "H0_km_s_Mpc": 70.0,
                    "Omega_m0": 0.3,
                    "lambda_H_Lambda_over_H0": 10.0,
                    "chi_bar_0_R_over_H0sq": 12.0,
                    r"\alpha": 0.5,
                    r"\beta": 100.0,
                }],
            }), encoding="utf-8")

            metadata = compile_proposal_to_run(proposal_path, run_dir)
            self.assertEqual(metadata["source"], "proposal_json_token_catalog")
            self.assertTrue(metadata["scalaron"]["enabled"])
            self.assertEqual(metadata["scalaron"]["classification"], "scalarizable")
            with (run_dir / "agent_lagrangians.pkl").open("rb") as handle:
                payload = pickle.load(handle)
            lagrangian = next(iter(payload.values()))[0]
            self.assertTrue(lagrangian["scalaron"]["enabled"])
            self.assertTrue(verify_legendre_equivalence(lagrangian))

    def test_parameter_memory_retains_scalaron_initial_data(self):
        from ai_theory_lab.joint_parameter_prior import _sample_vector

        vector = _sample_vector(
            {
                "chi_bar_0_R_over_H0sq": "12.5",
                "q1_0_dvarphi1_dln_a": "-0.25",
            }
        )
        self.assertEqual(vector["chi_bar_0_R_over_H0sq"], 12.5)
        self.assertEqual(vector["q1_0_dvarphi1_dln_a"], -0.25)

    def test_scalaron_root_failure_is_tagged_without_false_timeout(self):
        from ai_theory_lab.memory import _failure_tags
        from ai_theory_lab.validation_result import StageResult, ValidationResult

        result = ValidationResult(
            validated=False,
            diagnostics={
                "top_reject_reasons": [
                    {
                        "reason": "no acceptable real qchi_0 root from E_N(x=0)=0",
                        "count": 3,
                    }
                ]
            },
            stages=[
                StageResult(
                    stage="Builder",
                    cmd=["builder"],
                    returncode=0,
                    elapsed_seconds=1.0,
                    stdout_tail=(
                        "Structurally skipped / timed out: 0\n"
                        "Build timeout seconds: 60"
                    ),
                )
            ],
        )
        tags = _failure_tags(result)
        self.assertIn("q_initial_root_failure", tags)
        self.assertNotIn("symbolic_timeout", tags)

        result.stages[0].stderr_tail = "TIMEOUT after 120 seconds."
        self.assertIn("symbolic_timeout", _failure_tags(result))

    def test_no_scalar_skip_message_uses_actual_initial_budget(self):
        from ai_theory_lab.cold_start_runner import _structural_expansion_skip_reason

        attempt = {
            "theory": {"scalar_config": "none", "parameter_sample_count": 3},
            "failure_tags": ["missing_ranking", "no_accepted_samples"],
        }
        reason = _structural_expansion_skip_reason(attempt, None)
        self.assertEqual(
            reason,
            "no-scalar empty ranking after 3 initial samples; no expanded sampling",
        )

    def test_langgraph_places_scalaron_transform_before_validation(self):
        from ai_theory_lab.graph_agent import build_graph

        graph = build_graph().get_graph()
        edges = {(edge.source, edge.target) for edge in graph.edges}
        self.assertIn(("propose_theory", "scalarize_theory"), edges)
        self.assertIn(("scalarize_theory", "validate_initial"), edges)


if __name__ == "__main__":
    unittest.main()
