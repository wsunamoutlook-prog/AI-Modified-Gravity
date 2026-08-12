from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import sympy as sp

from ai_theory_lab.dataset import (
    attempt_to_training_record,
    consolidate_structure_attempts,
    parameter_reward_for_attempt,
    structure_reward_for_attempt,
    structure_score_for_attempt,
    summarize_policy,
    training_records_for_attempts,
)
from ai_theory_lab.harness import read_best_result
from ai_theory_lab.agent_loop import _structure_prior_from_attempts
from ai_theory_lab.llm_agent import _choice_prompt, _compact_summary
from ai_theory_lab.report import _parse_lcdm_reference
from solver_v5_2.core import (
    LCDM_EFFECTIVE_PARAMETER_NAMES,
    Model,
    effective_parameter_names,
    eps_HM_sym,
    fbar2_sym,
    lambda_H_sym,
    mu1_sym,
    q2_sym,
    varphi1_sym,
    varphi2_sym,
)


def _attempt(
    loop_id: str,
    *,
    chi2: float | None,
    aic: float | None,
    stage: str = "initial",
    trial: str | None = None,
    group: str = "non_eh",
) -> dict:
    return {
        "loop_id": loop_id,
        "timestamp": loop_id,
        "validated": chi2 is not None,
        "entered_solver": True,
        "chi2": chi2,
        "aic": aic,
        "bic": None,
        "k_params": None if chi2 is None or aic is None else int(round((aic - chi2) / 2.0)),
        "validation_stage": stage,
        "structure_trial_id": trial or loop_id,
        "family_key": "scalar=phi2_only|operators=phi2R",
        "failure_tags": [] if chi2 is not None else ["no_accepted_samples"],
        "theory": {
            "proposal_group": group,
            "theory_track": "non_eh",
            "scalar_config": "phi2_only",
            "potential_types": {"phi1": None, "phi2": "quadratic"},
            "operators": ["φ2 · R"],
        },
    }


class HybridRewardTests(unittest.TestCase):
    def test_structure_uses_aic_while_parameter_reward_keeps_chi2(self) -> None:
        compact = _attempt("compact", chi2=1640.0, aic=1654.0)
        large = _attempt("large", chi2=1640.0, aic=1674.0)

        self.assertEqual(parameter_reward_for_attempt(compact), parameter_reward_for_attempt(large))
        self.assertLess(structure_score_for_attempt(compact), structure_score_for_attempt(large))
        self.assertGreater(structure_reward_for_attempt(compact), structure_reward_for_attempt(large))

        record = attempt_to_training_record(compact)
        self.assertEqual(record["result"]["parameter_reward"], parameter_reward_for_attempt(compact))
        self.assertEqual(record["result"]["structure_reward"], structure_reward_for_attempt(compact))
        self.assertEqual(record["result"]["reward"], record["result"]["structure_reward"])

    def test_non_eh_poor_fit_remains_negative_under_aic_reward(self) -> None:
        poor = _attempt("poor", chi2=9434.0, aic=9450.0)
        self.assertLess(structure_reward_for_attempt(poor), 0.0)

    def test_multistage_lineage_updates_structure_policy_once(self) -> None:
        initial = _attempt("task_1", chi2=1690.0, aic=1710.0, trial="task_1")
        expanded = _attempt(
            "task_1_expanded",
            chi2=1660.0,
            aic=1680.0,
            stage="expanded",
            trial="task_1",
        )
        independent = _attempt("task_2", chi2=1700.0, aic=1716.0, trial="task_2")

        consolidated = consolidate_structure_attempts([initial, expanded, independent])
        self.assertEqual(len(consolidated), 2)
        first = next(row for row in consolidated if row["structure_trial_id"] == "task_1")
        self.assertEqual(first["loop_id"], "task_1_expanded")

        records = training_records_for_attempts([initial, expanded, independent])
        self.assertEqual(sum(r["result"]["is_structure_representative"] for r in records), 2)
        policy = summarize_policy(records)
        self.assertEqual(policy["record_count"], 2)
        self.assertEqual(policy["raw_stage_record_count"], 3)

    def test_multistage_parameter_samples_all_remain_in_scalar_metrics(self) -> None:
        initial = _attempt("task_1", chi2=1690.0, aic=1710.0, trial="task_1")
        expanded = _attempt(
            "task_1_expanded",
            chi2=1660.0,
            aic=1680.0,
            stage="expanded",
            trial="task_1",
        )

        def counts(attempt: dict) -> dict[str, int]:
            if attempt["validation_stage"] == "expanded":
                return {
                    "total": 300,
                    "accepted": 60,
                    "q_initial_root_failure": 20,
                    "no_scalar_constraint": 0,
                    "constraint_drift": 10,
                    "integration_failure": 5,
                }
            return {
                "total": 100,
                "accepted": 10,
                "q_initial_root_failure": 15,
                "no_scalar_constraint": 0,
                "constraint_drift": 5,
                "integration_failure": 0,
            }

        with patch("ai_theory_lab.agent_loop._attempt_sample_counts", side_effect=counts):
            prior = _structure_prior_from_attempts([initial, expanded], {})

        metrics = prior["scalar_family_learning"]["metrics"]["phi2_only"]
        self.assertEqual(metrics["attempts"], 1)
        self.assertEqual(metrics["sample_count"], 400)
        self.assertEqual(metrics["accepted_sample_count"], 70)
        self.assertAlmostEqual(metrics["accepted_sample_rate"], 70 / 400)
        self.assertEqual(metrics["q_initial_root_failure_count"], 35)


class EffectiveParameterCountTests(unittest.TestCase):
    @staticmethod
    def _model(expression: sp.Expr, *, has_phi1: bool = False, has_phi2: bool = False) -> Model:
        return Model(
            lag_id="1",
            general="test",
            has_phi1=has_phi1,
            has_phi2=has_phi2,
            scalar_config="both" if has_phi1 and has_phi2 else "none",
            gf_relations="",
            eom_strings={},
            eom_exprs={},
            free_symbols=[],
            eh_symbol=None,
            dimless_exprs={"N": expression},
            rhs_exprs={"hx": expression},
        )

    def test_lcdm_reference_counts_nominal_effective_parameters(self) -> None:
        self.assertEqual(LCDM_EFFECTIVE_PARAMETER_NAMES, ("Omega_m0", "M_SN", "alpha_BAO"))

    def test_h0_is_not_counted_when_profiled_absolute_scale_cancels(self) -> None:
        coupling = sp.Symbol("zeta")
        model = self._model(lambda_H_sym + coupling)
        names = effective_parameter_names(model, [coupling], "eft")

        self.assertNotIn("H0_km_s_Mpc", names)
        self.assertIn("lambda_H_Lambda_over_H0", names)
        self.assertIn("zeta", names)
        self.assertEqual(len(names), 5)

    def test_h0_and_only_used_scalar_parameters_are_counted(self) -> None:
        free_after_ghost = sp.Symbol("iota")
        cancelled_coefficient = sp.Symbol("cancelled")
        expression = (
            eps_HM_sym
            + mu1_sym
            + fbar2_sym
            + free_after_ghost
            + varphi1_sym
            + varphi2_sym
            + q2_sym
        )
        model = self._model(expression, has_phi1=True, has_phi2=True)
        names = effective_parameter_names(model, [free_after_ghost, cancelled_coefficient], "eft")

        self.assertIn("H0_km_s_Mpc", names)
        self.assertIn("mu1_m1_over_H0", names)
        self.assertIn("fbar2_f2_over_Lambda", names)
        self.assertNotIn("mu2_m2_over_Lambda", names)
        self.assertNotIn("fbar1_f1_over_Mp", names)
        self.assertIn("q2_0_dvarphi2_dln_a", names)
        self.assertEqual(names.count("iota"), 1)
        self.assertNotIn("cancelled", names)

    def test_shift_symmetric_initial_field_is_not_counted(self) -> None:
        model = self._model(q2_sym, has_phi2=True)
        names = effective_parameter_names(model, [], "eft")

        self.assertNotIn("varphi2_0_phi2_over_Lambda", names)
        self.assertNotIn("q2_0_dvarphi2_dln_a", names)


class LLMStructureMetricTests(unittest.TestCase):
    def test_compact_feedback_exposes_both_fit_and_structure_metrics(self) -> None:
        summary = {
            "best_chi2": 1638.0,
            "best_structure_score": 1646.0,
            "agent_loop": {
                "structure_prior": {"structure_reward_metric": "AIC-2*k_LCDM"},
            },
        }
        compact = _compact_summary(summary)

        self.assertEqual(compact["best_chi2"], 1638.0)
        self.assertEqual(compact["best_structure_score"], 1646.0)
        self.assertEqual(compact["structure_learning_metric"], "AIC-2*k_LCDM")

    def test_llm_prompt_distinguishes_structure_and_parameter_metrics(self) -> None:
        system, _, _ = _choice_prompt([], {})
        self.assertIn("AIC-adjusted cross-Lagrangian", system)
        self.assertIn("Raw chi-square", system)


class BackwardCompatibilityTests(unittest.TestCase):
    def test_old_ranking_without_k_recovers_it_from_aic(self) -> None:
        with TemporaryDirectory() as tmp:
            out = Path(tmp)
            (out / "model_ranking.csv").write_text(
                "lag_id,chi2,AIC,BIC\n1,1640,1654,1700\n",
                encoding="utf-8",
            )
            best = read_best_result(out)
        self.assertEqual(best["k_params"], 7)
        self.assertEqual(best["k_parameter_names"], [])

    def test_lcdm_report_preserves_effective_k(self) -> None:
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "scan_report.txt"
            path.write_text(
                "Flat-LambdaCDM reference fit\n"
                "chi2_total=1645.28, chi2_DES_SN=1500, chi2_DESI_BAO=145.28, "
                "chi2/N=0.9, AIC=1651.28, BIC=1668.0, k=3\n"
                "Effective parameters: Omega_m0, M_SN, alpha_BAO "
                "(H0 is not an independent fit direction after profiling).\n"
                "M_SN_hat=0.1, alpha_BAO_hat=30\n"
                "H0=70, Omega_m0=0.3\n",
                encoding="utf-8",
            )
            lcdm = _parse_lcdm_reference(path)
        self.assertIsNotNone(lcdm)
        self.assertEqual(lcdm["k_params"], 3.0)
        self.assertEqual(lcdm["k_parameter_names"], ["Omega_m0", "M_SN", "alpha_BAO"])


if __name__ == "__main__":
    unittest.main()
