import unittest

from ai_theory_lab.audit_scalaron_run import (
    TrialAudit,
    _bookkeeping_issues,
    _verdict,
    classify_operator_labels,
)


class ScalaronRunAuditTests(unittest.TestCase):
    def test_operator_classification_matches_supported_boundary(self):
        ordinary = classify_operator_labels(["R", "R^{ab} · R_{ab}"])
        scalarizable = classify_operator_labels(["R", "R · R", "φ1 · R · R"])
        hybrid = classify_operator_labels(["R", "R · R", "R^{ab} · R_{ab}"])

        self.assertEqual(ordinary["classification"], "ordinary")
        self.assertFalse(ordinary["enabled"])
        self.assertEqual(scalarizable["classification"], "scalarizable")
        self.assertTrue(scalarizable["enabled"])
        self.assertEqual(hybrid["classification"], "hybrid")
        self.assertTrue(hybrid["enabled"])

    def test_consistent_aic_and_parameter_names_pass(self):
        record = {
            "validated": True,
            "chi2": 100.0,
            "aic": 108.0,
            "k_params": 4,
            "k_parameter_names": ["Omega_m0", "beta", "M_SN", "alpha_BAO"],
        }
        self.assertEqual(_bookkeeping_issues(record), [])

    def test_aic_and_k_name_mismatches_are_reported(self):
        record = {
            "validated": True,
            "chi2": 100.0,
            "aic": 106.0,
            "k_params": 4,
            "k_parameter_names": ["Omega_m0", "M_SN", "alpha_BAO"],
        }
        issues = _bookkeeping_issues(record)
        self.assertTrue(any("AIC bookkeeping mismatch" in issue for issue in issues))
        self.assertTrue(any("parameter names" in issue for issue in issues))

    def test_missing_rejection_reason_is_not_called_reasonable(self):
        audit = TrialAudit(
            trial_id="task_1",
            best_record={
                "aic": None,
                "failed_stage": "Solver",
                "failure_tags": ["no_accepted_samples"],
                "top_reject_reasons": [],
            },
            stages=["initial"],
            proposal_path=None,
            structural={},
            issues=[],
        )
        verdict, _explanation = _verdict(audit)
        self.assertEqual(verdict, "rejection_diagnostic_incomplete")


if __name__ == "__main__":
    unittest.main()
