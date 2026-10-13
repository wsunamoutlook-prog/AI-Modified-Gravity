from __future__ import annotations

import math
import unittest

import numpy as np

from solver_v5_2.identifiability import audit_background_identifiability
import solver_v5_2.core as core


class BackgroundIdentifiabilityTests(unittest.TestCase):
    def test_exact_parameter_combination_reduces_rank(self) -> None:
        base = {"a": 2.0, "b": 3.0, "c": 5.0}

        def feature(sample):
            shared = sample["a"] + 2.0 * sample["b"]
            return True, np.asarray([shared, 3.0 * shared, sample["c"]]), "ok"

        ok, baseline, _ = feature(base)
        self.assertTrue(ok)
        audit = audit_background_identifiability(
            parameter_names=["a", "b", "c", "M_SN", "alpha_BAO"],
            base_sample=base,
            baseline_feature=baseline,
            evaluator=feature,
            profiled_parameter_names=("M_SN", "alpha_BAO"),
            rank_rtol=1.0e-8,
        )

        self.assertEqual(audit["status"], "ok")
        self.assertEqual(audit["dynamic_parameter_count"], 3)
        self.assertEqual(audit["dynamic_rank"], 2)
        self.assertEqual(audit["k_nominal"], 5)
        self.assertEqual(audit["k_identifiable"], 4)
        self.assertTrue(audit["null_combinations"])

    def test_failed_perturbation_is_counted_conservatively(self) -> None:
        base = {"a": 2.0}

        def feature(sample):
            return True, np.asarray([sample["a"]]), "ok"

        audit = audit_background_identifiability(
            parameter_names=["a", "missing", "M_SN", "alpha_BAO"],
            base_sample=base,
            baseline_feature=np.asarray([2.0]),
            evaluator=feature,
            profiled_parameter_names=("M_SN", "alpha_BAO"),
            rank_rtol=1.0e-8,
        )

        self.assertEqual(audit["status"], "partial_conservative")
        self.assertEqual(audit["unresolved_parameter_names"], ["missing"])
        self.assertEqual(audit["k_nominal"], 4)
        self.assertEqual(audit["k_identifiable"], 4)

    def test_report_and_use_rank_modes_are_distinct(self) -> None:
        audit = {
            "status": "ok",
            "k_nominal": 5,
            "k_identifiable": 4,
            "dynamic_rank": 2,
            "dynamic_parameter_count": 3,
            "condition_number": math.inf,
            "singular_values": [1.0, 0.5, 0.0],
            "null_combinations": [{"a": 1.0, "b": -1.0}],
            "unresolved_parameter_names": [],
            "solver_evaluations": 6,
        }
        original_mode = core.IDENTIFIABILITY_MODE
        try:
            report_result = core.SampleResult(
                lag_id="1", success=True, reason="ok", chi2=10.0,
                aic=20.0, bic=30.0, k_params=5,
                k_parameter_names=["a", "b", "c", "M_SN", "alpha_BAO"],
                n_sn=10, n_bao=2,
            )
            core.IDENTIFIABILITY_MODE = "report"
            core._apply_identifiability_audit([report_result], report_result, audit)
            self.assertEqual(report_result.k_params, 5)
            self.assertEqual(report_result.aic, 20.0)
            self.assertEqual(report_result.k_params_identifiable, 4)
            self.assertEqual(report_result.aic_identifiable, 18.0)

            rank_result = core.SampleResult(
                lag_id="1", success=True, reason="ok", chi2=10.0,
                aic=20.0, bic=30.0, k_params=5,
                k_parameter_names=["a", "b", "c", "M_SN", "alpha_BAO"],
                n_sn=10, n_bao=2,
            )
            core.IDENTIFIABILITY_MODE = "use_rank"
            core._apply_identifiability_audit([rank_result], rank_result, audit)
            self.assertEqual(rank_result.k_params, 4)
            self.assertEqual(rank_result.aic, 18.0)
        finally:
            core.IDENTIFIABILITY_MODE = original_mode


if __name__ == "__main__":
    unittest.main()
