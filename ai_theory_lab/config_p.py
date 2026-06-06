"""Default parameter priors for cold-start agent sampling."""

from __future__ import annotations


PARAMETER_PRIORS = {
    "H0_km_s_Mpc": {"low": 58.0, "high": 74.0, "log10": False},
    "Omega_m0": {"low": 0.22, "high": 0.40, "log10": False},
    "lambda_H_Lambda_over_H0": {"low": 2.0e3, "high": 8.0e4, "log10": True},
    "varphi1_0_phi1_over_Mp": {"low": 0.15, "high": 4.5, "log10": False},
    "mu1_m1_over_H0": {"low": 0.04, "high": 4.0, "log10": True},
    "fbar1_f1_over_Mp": {"low": 0.05, "high": 30.0, "log10": True},
    "varphi2_0_phi2_over_Lambda": {"low": 0.05, "high": 3.0, "log10": False},
    "q2_0_dvarphi2_dln_a": {"low": -2.0, "high": 2.0, "log10": False},
    "mu2_m2_over_Lambda": {"low": 1.0e-4, "high": 1.0, "log10": True},
    "fbar2_f2_over_Lambda": {"low": 0.05, "high": 20.0, "log10": True},
}


COEFFICIENT_PRIOR = {
    "log10_abs_low": -10.0,
    "log10_abs_high": -4.0,
    "signs": [-1.0, 1.0],
}


EH_R_COEFFICIENT = 0.5


PARAMETER_PRIOR_UPDATE = {
    "min_attempts_before_update": 500,
    "min_accepted_samples": 20,
    "fixed_parameters": ["H0_km_s_Mpc"],
    "quantile_low": 0.15,
    "quantile_high": 0.85,
}
