"""Default parameter priors for cold-start agent sampling."""

from __future__ import annotations


PARAMETER_PRIORS = {
    "H0_km_s_Mpc": {"low": 58.0, "high": 74.0, "log10": False},
    "Omega_m0": {"low": 0.22, "high": 0.40, "log10": False},
    "lambda_H_Lambda_over_H0": {"low": 5.0e2, "high": 8.0e4, "log10": True},
    "varphi1_0_phi1_over_Mp": {"low": 1.0e-3, "high": 1.0e1, "log10": True},
    "mu1_m1_over_H0": {"low": 1.0e-2, "high": 1.0e2, "log10": True},
    "fbar1_f1_over_Mp": {"low": 1.0e-2, "high": 1.0e2, "log10": True},
    "varphi2_0_phi2_over_Lambda": {"low": 1.0e-5, "high": 1.0e5, "signed_log10": True},
    "chi_bar_0_R_over_H0sq": {"low": 1.0e-2, "high": 1.0e3, "log10": True},
    "q1_0_dvarphi1_dln_a": {"low": 1.0e-5, "high": 1.0e2, "signed_log10": True},
    "q2_0_dvarphi2_dln_a": {"low": 1.0e-5, "high": 1.0e5, "signed_log10": True},
    "mu2_m2_over_Lambda": {"low": 1.0e-5, "high": 1.0e5, "log10": True},
    "fbar2_f2_over_Lambda": {"low": 1.0e-5, "high": 1.0e5, "log10": True},
}


COEFFICIENT_PRIOR = {
    "log10_abs_low": -10.0,
    "log10_abs_high": 20.0,
    "signs": [-1.0, 1.0],
}


EH_R_COEFFICIENT = 0.5


CORRECTION_SAMPLING = {
    "mode_weights": {
        "baseline": 0.10,
        "weak": 0.30,
        "moderate": 0.30,
        "active_probe": 0.30,
    },
    "min_mode_probability": {
        "baseline": 0.05,
        "weak": 0.10,
        "moderate": 0.10,
        "active_probe": 0.10,
    },
    "target_relative_effect": {
        "baseline": {"low": 0.0, "high": 0.0, "log10": False},
        "weak": {"low": 1.0e-6, "high": 1.0e-4, "log10": True},
        "moderate": {"low": 1.0e-4, "high": 1.0e-2, "log10": True},
        "active_probe": {"low": 1.0e-2, "high": 1.0e2, "log10": True},
    },
    "coefficient_abs_min": 1.0e-10,
    "coefficient_abs_max": 1.0e20,
    "coefficient_log10_scatter": 0.35,
}


PARAMETER_SAMPLE_POLICY = {
    "agent_exact_fraction": 0.50,
    "joint_prior_usage_fraction": 0.80,
    "agent_exact_source_code": 1.0,
    "learned_random_source_code": 0.0,
}


PARAMETER_PRIOR_UPDATE = {
    "min_attempts_before_update": 10,
    "min_accepted_samples": 100,
    "fixed_parameters": ["H0_km_s_Mpc"],
    "quantile_low": 0.10,
    "quantile_high": 0.90,
}
