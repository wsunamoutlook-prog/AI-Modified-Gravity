# Agent Reflection Input

Use only the current-loop facts below. Do not use historical `solver_result/`
outputs, old top-10 plots, or remembered best-fit parameters.

The harness is not telling you how to update your proposal policy. Your job is
to infer what to try next from the facts.

If successful low-chi-square attempts share features, such as `phi1_only`, an
`R` anchor, or a simple scalar-curvature coupling, explain whether you will
raise the sampling probability of those features. If the first 1000 samples for
a theory have no accepted chi-square and mostly structural rejection reasons
such as `no_scalar_constraint`, `q_not_determined`, pre-sampling timeout, or
symbolic timeout, explain why you will change structure instead of only adding
more parameter samples.

## Current-Loop Facts

```json
{
  "total_attempts": 104,
  "validated_count": 62,
  "entered_solver_count": 104,
  "failed_stage_counts": {
    "Solver": 42
  },
  "failure_tag_counts": {
    "no_accepted_samples": 88,
    "q_initial_root_failure": 82,
    "h_absurdly_large": 62,
    "constraint_drift": 57,
    "integration_failure": 5,
    "no_scalar_constraint": 1
  },
  "scalar_config_counts": {
    "phi1_only": 98,
    "phi2_only": 5,
    "none": 1
  },
  "theory_track_counts": {
    "eh_anchored": 104
  },
  "accepted_theory_track_counts": {
    "eh_anchored": 62
  },
  "best_chi2": 1638.0428393360799,
  "best_attempt": {
    "timestamp": "2026-06-09T20:00:09-0400",
    "loop_id": "wave_0011_lag_8",
    "validated": true,
    "failed_stage": null,
    "entered_stages": [
      "EOM",
      "Builder",
      "Solver"
    ],
    "entered_solver": true,
    "best_lag_id": "8",
    "chi2": 1638.0428393360799,
    "aic": 1650.0428393360799,
    "bic": 1683.1250948231182,
    "solver_output_dir": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0011/agent_solver_result/agent_solve",
    "model_ranking_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0011/agent_solver_result/agent_solve/model_ranking.csv",
    "scan_report_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0011/agent_solver_result/agent_solve/scan_report.txt",
    "theory": {
      "proposal_id": "cold_start_token_loop_11_batch_lag_8",
      "source_n_terms": 3,
      "source_local_number": 14,
      "scalar_config": "phi1_only",
      "potential_types": {
        "phi1": "quadratic",
        "phi2": null
      },
      "operators": [
        "R"
      ],
      "theory_track": "eh_anchored",
      "parameter_sample_count": 1000
    },
    "theory_track": "eh_anchored",
    "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R",
    "coarse_family_key": "scalar=phi1_only|phi1_potential=quadratic|phi2_potential=None|operator_bucket=R_anchor",
    "failure_tags": [
      "q_initial_root_failure",
      "h_absurdly_large",
      "no_accepted_samples"
    ],
    "top_reject_reasons": [
      {
        "lag_id": "8",
        "count": "606",
        "total_rejected_or_skipped": "904",
        "reason": "H(z) absurdly large"
      },
      {
        "lag_id": "8",
        "count": "298",
        "total_rejected_or_skipped": "904",
        "reason": "no acceptable real q1_0 root from E_N(x=0)=0"
      }
    ],
    "all_samples_summary_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0011/agent_solver_result/agent_solve/all_samples_summary.csv",
    "accepted_samples_summary_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0011/agent_solver_result/agent_solve/accepted_samples_summary.csv",
    "reject_reasons_by_model_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0011/agent_solver_result/agent_solve/reject_reasons_by_model.csv",
    "diagnostic_message": null,
    "agent_lagrangian": {
      "proposal_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/proposals/graph_agent_batch_208_split_v4/wave_0011_lag_8.json",
      "agent_lagrangians_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0011/agent_lagrangians.pkl",
      "agent_parameter_samples_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0011/agent_parameter_samples_by_lag_id.json",
      "proposal_id": "batch_lag_8",
      "source": "batch_token_level_grammar",
      "source_n_terms": 3,
      "source_local_number": 14,
      "batch_lag_id": "8",
      "scalar_config": "phi1_only",
      "potential_types": {
        "phi1": "quadratic",
        "phi2": null
      },
      "operators": [
        "R"
      ],
      "operator_specs": [
        {
          "candidate": "R",
          "coefficient": "\\alpha"
        }
      ],
      "theory_track": "eh_anchored",
      "general": "√(-g) [ M_p² ( \\alpha · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]",
      "lagrangian": {
        "n_terms": 3,
        "general": "√(-g) [ M_p² ( \\alpha · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]",
        "terms": [
          {
            "coeff_symbol": "\\alpha",
            "coeff_token": "COEFF_0",
            "candidate": "R",
            "mass_dim": 2,
            "lambda_power": 0,
            "sector": "gravity"
          },
          {
            "coeff_symbol": "1",
            "coeff_token": "COEFF_FIXED_1",
            "candidate": "-½ g^{μν} ∇_μφ1 ∇_νφ1",
            "mass_dim": 4,
            "lambda_power": 0,
            "fixed": true,
            "sector": "matter"
          },
          {
            "coeff_symbol": "1",
            "coeff_token": "COEFF_FIXED_1",
            "candidate": "-½ m_1² φ1²",
            "mass_dim": 4,
            "lambda_power": 0,
            "fixed": true,
            "sector": "matter",
            "potential_type": "quadratic"
          }
        ],
        "scalar_config": "phi1_only",
        "potential_types": {
          "phi1": "quadratic",
          "phi2": null
        }
      }
    }
  },
  "top_chi2_attempts": [
    {
      "timestamp": "2026-06-09T20:00:09-0400",
      "loop_id": "wave_0011_lag_8",
      "validated": true,
      "failed_stage": null,
      "entered_stages": [
        "EOM",
        "Builder",
        "Solver"
      ],
      "entered_solver": true,
      "best_lag_id": "8",
      "chi2": 1638.0428393360799,
      "aic": 1650.0428393360799,
      "bic": 1683.1250948231182,
      "solver_output_dir": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0011/agent_solver_result/agent_solve",
      "model_ranking_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0011/agent_solver_result/agent_solve/model_ranking.csv",
      "scan_report_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0011/agent_solver_result/agent_solve/scan_report.txt",
      "theory": {
        "proposal_id": "cold_start_token_loop_11_batch_lag_8",
        "source_n_terms": 3,
        "source_local_number": 14,
        "scalar_config": "phi1_only",
        "potential_types": {
          "phi1": "quadratic",
          "phi2": null
        },
        "operators": [
          "R"
        ],
        "theory_track": "eh_anchored",
        "parameter_sample_count": 1000
      },
      "theory_track": "eh_anchored",
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R",
      "coarse_family_key": "scalar=phi1_only|phi1_potential=quadratic|phi2_potential=None|operator_bucket=R_anchor",
      "failure_tags": [
        "q_initial_root_failure",
        "h_absurdly_large",
        "no_accepted_samples"
      ],
      "top_reject_reasons": [
        {
          "lag_id": "8",
          "count": "606",
          "total_rejected_or_skipped": "904",
          "reason": "H(z) absurdly large"
        },
        {
          "lag_id": "8",
          "count": "298",
          "total_rejected_or_skipped": "904",
          "reason": "no acceptable real q1_0 root from E_N(x=0)=0"
        }
      ],
      "all_samples_summary_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0011/agent_solver_result/agent_solve/all_samples_summary.csv",
      "accepted_samples_summary_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0011/agent_solver_result/agent_solve/accepted_samples_summary.csv",
      "reject_reasons_by_model_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0011/agent_solver_result/agent_solve/reject_reasons_by_model.csv",
      "diagnostic_message": null,
      "agent_lagrangian": {
        "proposal_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/proposals/graph_agent_batch_208_split_v4/wave_0011_lag_8.json",
        "agent_lagrangians_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0011/agent_lagrangians.pkl",
        "agent_parameter_samples_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0011/agent_parameter_samples_by_lag_id.json",
        "proposal_id": "batch_lag_8",
        "source": "batch_token_level_grammar",
        "source_n_terms": 3,
        "source_local_number": 14,
        "batch_lag_id": "8",
        "scalar_config": "phi1_only",
        "potential_types": {
          "phi1": "quadratic",
          "phi2": null
        },
        "operators": [
          "R"
        ],
        "operator_specs": [
          {
            "candidate": "R",
            "coefficient": "\\alpha"
          }
        ],
        "theory_track": "eh_anchored",
        "general": "√(-g) [ M_p² ( \\alpha · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]",
        "lagrangian": {
          "n_terms": 3,
          "general": "√(-g) [ M_p² ( \\alpha · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]",
          "terms": [
            {
              "coeff_symbol": "\\alpha",
              "coeff_token": "COEFF_0",
              "candidate": "R",
              "mass_dim": 2,
              "lambda_power": 0,
              "sector": "gravity"
            },
            {
              "coeff_symbol": "1",
              "coeff_token": "COEFF_FIXED_1",
              "candidate": "-½ g^{μν} ∇_μφ1 ∇_νφ1",
              "mass_dim": 4,
              "lambda_power": 0,
              "fixed": true,
              "sector": "matter"
            },
            {
              "coeff_symbol": "1",
              "coeff_token": "COEFF_FIXED_1",
              "candidate": "-½ m_1² φ1²",
              "mass_dim": 4,
              "lambda_power": 0,
              "fixed": true,
              "sector": "matter",
              "potential_type": "quadratic"
            }
          ],
          "scalar_config": "phi1_only",
          "potential_types": {
            "phi1": "quadratic",
            "phi2": null
          }
        }
      }
    },
    {
      "timestamp": "2026-06-09T17:53:45-0400",
      "loop_id": "wave_0004_lag_8",
      "validated": true,
      "failed_stage": null,
      "entered_stages": [
        "EOM",
        "Builder",
        "Solver"
      ],
      "entered_solver": true,
      "best_lag_id": "8",
      "chi2": 1639.0299359874105,
      "aic": 1651.0299359874105,
      "bic": 1684.1121914744488,
      "solver_output_dir": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0004/agent_solver_result/agent_solve",
      "model_ranking_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0004/agent_solver_result/agent_solve/model_ranking.csv",
      "scan_report_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0004/agent_solver_result/agent_solve/scan_report.txt",
      "theory": {
        "proposal_id": "cold_start_token_loop_04_batch_lag_8",
        "source_n_terms": 4,
        "source_local_number": 19,
        "scalar_config": "phi1_only",
        "potential_types": {
          "phi1": "quadratic",
          "phi2": null
        },
        "operators": [
          "R",
          "φ1 · ∇^{a}∇_{a}R"
        ],
        "theory_track": "eh_anchored",
        "parameter_sample_count": 1000
      },
      "theory_track": "eh_anchored",
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+φ1 · ∇^{a}∇_{a}R",
      "coarse_family_key": "scalar=phi1_only|phi1_potential=quadratic|phi2_potential=None|operator_bucket=R_anchor+derivative+scalar_curvature",
      "failure_tags": [
        "q_initial_root_failure",
        "h_absurdly_large",
        "constraint_drift",
        "no_accepted_samples"
      ],
      "top_reject_reasons": [
        {
          "lag_id": "8",
          "count": "582",
          "total_rejected_or_skipped": "869",
          "reason": "H(z) absurdly large"
        },
        {
          "lag_id": "8",
          "count": "286",
          "total_rejected_or_skipped": "869",
          "reason": "no acceptable real q1_0 root from E_N(x=0)=0"
        },
        {
          "lag_id": "8",
          "count": "1",
          "total_rejected_or_skipped": "869",
          "reason": "constraint drift too large: max|C|=1.087e-04"
        }
      ],
      "all_samples_summary_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0004/agent_solver_result/agent_solve/all_samples_summary.csv",
      "accepted_samples_summary_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0004/agent_solver_result/agent_solve/accepted_samples_summary.csv",
      "reject_reasons_by_model_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0004/agent_solver_result/agent_solve/reject_reasons_by_model.csv",
      "diagnostic_message": null,
      "agent_lagrangian": {
        "proposal_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/proposals/graph_agent_batch_208_split_v4/wave_0004_lag_8.json",
        "agent_lagrangians_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0004/agent_lagrangians.pkl",
        "agent_parameter_samples_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0004/agent_parameter_samples_by_lag_id.json",
        "proposal_id": "batch_lag_8",
        "source": "batch_token_level_grammar",
        "source_n_terms": 4,
        "source_local_number": 19,
        "batch_lag_id": "8",
        "scalar_config": "phi1_only",
        "potential_types": {
          "phi1": "quadratic",
          "phi2": null
        },
        "operators": [
          "R",
          "φ1 · ∇^{a}∇_{a}R"
        ],
        "operator_specs": [
          {
            "candidate": "R",
            "coefficient": "\\alpha"
          },
          {
            "candidate": "φ1 · ∇^{a}∇_{a}R",
            "coefficient": "\\beta"
          }
        ],
        "theory_track": "eh_anchored",
        "general": "√(-g) [ M_p² ( \\alpha · R  +  \\beta Λ^{-3} · φ1 · ∇^{a}∇_{a}R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]",
        "lagrangian": {
          "n_terms": 4,
          "general": "√(-g) [ M_p² ( \\alpha · R  +  \\beta Λ^{-3} · φ1 · ∇^{a}∇_{a}R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]",
          "terms": [
            {
              "coeff_symbol": "\\alpha",
              "coeff_token": "COEFF_0",
              "candidate": "R",
              "mass_dim": 2,
              "lambda_power": 0,
              "sector": "gravity"
            },
            {
              "coeff_symbol": "\\beta",
              "coeff_token": "COEFF_1",
              "candidate": "φ1 · ∇^{a}∇_{a}R",
              "mass_dim": 5,
              "lambda_power": -3,
              "sector": "non-minimal"
            },
            {
              "coeff_symbol": "1",
              "coeff_token": "COEFF_FIXED_1",
              "candidate": "-½ g^{μν} ∇_μφ1 ∇_νφ1",
              "mass_dim": 4,
              "lambda_power": 0,
              "fixed": true,
              "sector": "matter"
            },
            {
              "coeff_symbol": "1",
              "coeff_token": "COEFF_FIXED_1",
              "candidate": "-½ m_1² φ1²",
              "mass_dim": 4,
              "lambda_power": 0,
              "fixed": true,
              "sector": "matter",
              "potential_type": "quadratic"
            }
          ],
          "scalar_config": "phi1_only",
          "potential_types": {
            "phi1": "quadratic",
            "phi2": null
          }
        }
      }
    },
    {
      "timestamp": "2026-06-09T18:09:21-0400",
      "loop_id": "wave_0005_lag_4",
      "validated": true,
      "failed_stage": null,
      "entered_stages": [
        "EOM",
        "Builder",
        "Solver"
      ],
      "entered_solver": true,
      "best_lag_id": "4",
      "chi2": 1640.842038437672,
      "aic": 1652.842038437672,
      "bic": 1685.9242939247104,
      "solver_output_dir": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0005/agent_solver_result/agent_solve",
      "model_ranking_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0005/agent_solver_result/agent_solve/model_ranking.csv",
      "scan_report_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0005/agent_solver_result/agent_solve/scan_report.txt",
      "theory": {
        "proposal_id": "cold_start_token_loop_05_batch_lag_4",
        "source_n_terms": 3,
        "source_local_number": 14,
        "scalar_config": "phi1_only",
        "potential_types": {
          "phi1": "quadratic",
          "phi2": null
        },
        "operators": [
          "R"
        ],
        "theory_track": "eh_anchored",
        "parameter_sample_count": 1000
      },
      "theory_track": "eh_anchored",
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R",
      "coarse_family_key": "scalar=phi1_only|phi1_potential=quadratic|phi2_potential=None|operator_bucket=R_anchor",
      "failure_tags": [
        "q_initial_root_failure",
        "h_absurdly_large",
        "constraint_drift"
      ],
      "top_reject_reasons": [
        {
          "lag_id": "4",
          "count": "578",
          "total_rejected_or_skipped": "875",
          "reason": "H(z) absurdly large"
        },
        {
          "lag_id": "4",
          "count": "295",
          "total_rejected_or_skipped": "875",
          "reason": "no acceptable real q1_0 root from E_N(x=0)=0"
        },
        {
          "lag_id": "4",
          "count": "1",
          "total_rejected_or_skipped": "875",
          "reason": "constraint drift too large: max|C|=1.021e-04"
        },
        {
          "lag_id": "4",
          "count": "1",
          "total_rejected_or_skipped": "875",
          "reason": "constraint drift too large: max|C|=1.095e-04"
        }
      ],
      "all_samples_summary_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0005/agent_solver_result/agent_solve/all_samples_summary.csv",
      "accepted_samples_summary_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0005/agent_solver_result/agent_solve/accepted_samples_summary.csv",
      "reject_reasons_by_model_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0005/agent_solver_result/agent_solve/reject_reasons_by_model.csv",
      "diagnostic_message": null,
      "agent_lagrangian": {
        "proposal_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/proposals/graph_agent_batch_208_split_v4/wave_0005_lag_4.json",
        "agent_lagrangians_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0005/agent_lagrangians.pkl",
        "agent_parameter_samples_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0005/agent_parameter_samples_by_lag_id.json",
        "proposal_id": "batch_lag_4",
        "source": "batch_token_level_grammar",
        "source_n_terms": 3,
        "source_local_number": 14,
        "batch_lag_id": "4",
        "scalar_config": "phi1_only",
        "potential_types": {
          "phi1": "quadratic",
          "phi2": null
        },
        "operators": [
          "R"
        ],
        "operator_specs": [
          {
            "candidate": "R",
            "coefficient": "\\alpha"
          }
        ],
        "theory_track": "eh_anchored",
        "general": "√(-g) [ M_p² ( \\alpha · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]",
        "lagrangian": {
          "n_terms": 3,
          "general": "√(-g) [ M_p² ( \\alpha · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]",
          "terms": [
            {
              "coeff_symbol": "\\alpha",
              "coeff_token": "COEFF_0",
              "candidate": "R",
              "mass_dim": 2,
              "lambda_power": 0,
              "sector": "gravity"
            },
            {
              "coeff_symbol": "1",
              "coeff_token": "COEFF_FIXED_1",
              "candidate": "-½ g^{μν} ∇_μφ1 ∇_νφ1",
              "mass_dim": 4,
              "lambda_power": 0,
              "fixed": true,
              "sector": "matter"
            },
            {
              "coeff_symbol": "1",
              "coeff_token": "COEFF_FIXED_1",
              "candidate": "-½ m_1² φ1²",
              "mass_dim": 4,
              "lambda_power": 0,
              "fixed": true,
              "sector": "matter",
              "potential_type": "quadratic"
            }
          ],
          "scalar_config": "phi1_only",
          "potential_types": {
            "phi1": "quadratic",
            "phi2": null
          }
        }
      }
    },
    {
      "timestamp": "2026-06-09T18:09:43-0400",
      "loop_id": "wave_0005_lag_7",
      "validated": true,
      "failed_stage": null,
      "entered_stages": [
        "EOM",
        "Builder",
        "Solver"
      ],
      "entered_solver": true,
      "best_lag_id": "7",
      "chi2": 1640.9593449034116,
      "aic": 1652.9593449034116,
      "bic": 1686.04160039045,
      "solver_output_dir": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0005/agent_solver_result/agent_solve",
      "model_ranking_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0005/agent_solver_result/agent_solve/model_ranking.csv",
      "scan_report_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0005/agent_solver_result/agent_solve/scan_report.txt",
      "theory": {
        "proposal_id": "cold_start_token_loop_05_batch_lag_7",
        "source_n_terms": 5,
        "source_local_number": 41,
        "scalar_config": "phi1_only",
        "potential_types": {
          "phi1": "quadratic",
          "phi2": null
        },
        "operators": [
          "R",
          "R · R",
          "∇^{a}φ1 · ∇^{b}φ1 · R_{ab}"
        ],
        "theory_track": "eh_anchored",
        "parameter_sample_count": 1000
      },
      "theory_track": "eh_anchored",
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R · R+∇^{a}φ1 · ∇^{b}φ1 · R_{ab}",
      "coarse_family_key": "scalar=phi1_only|phi1_potential=quadratic|phi2_potential=None|operator_bucket=R_anchor+derivative+high_curvature+scalar_curvature",
      "failure_tags": [
        "q_initial_root_failure",
        "h_absurdly_large",
        "constraint_drift"
      ],
      "top_reject_reasons": [
        {
          "lag_id": "7",
          "count": "579",
          "total_rejected_or_skipped": "868",
          "reason": "H(z) absurdly large"
        },
        {
          "lag_id": "7",
          "count": "288",
          "total_rejected_or_skipped": "868",
          "reason": "no acceptable real q1_0 root from E_N(x=0)=0"
        },
        {
          "lag_id": "7",
          "count": "1",
          "total_rejected_or_skipped": "868",
          "reason": "constraint drift too large: max|C|=1.156e-04"
        }
      ],
      "all_samples_summary_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0005/agent_solver_result/agent_solve/all_samples_summary.csv",
      "accepted_samples_summary_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0005/agent_solver_result/agent_solve/accepted_samples_summary.csv",
      "reject_reasons_by_model_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0005/agent_solver_result/agent_solve/reject_reasons_by_model.csv",
      "diagnostic_message": null,
      "agent_lagrangian": {
        "proposal_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/proposals/graph_agent_batch_208_split_v4/wave_0005_lag_7.json",
        "agent_lagrangians_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0005/agent_lagrangians.pkl",
        "agent_parameter_samples_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0005/agent_parameter_samples_by_lag_id.json",
        "proposal_id": "batch_lag_7",
        "source": "batch_token_level_grammar",
        "source_n_terms": 5,
        "source_local_number": 41,
        "batch_lag_id": "7",
        "scalar_config": "phi1_only",
        "potential_types": {
          "phi1": "quadratic",
          "phi2": null
        },
        "operators": [
          "R",
          "R · R",
          "∇^{a}φ1 · ∇^{b}φ1 · R_{ab}"
        ],
        "operator_specs": [
          {
            "candidate": "R",
            "coefficient": "\\alpha"
          },
          {
            "candidate": "R · R",
            "coefficient": "\\beta"
          },
          {
            "candidate": "∇^{a}φ1 · ∇^{b}φ1 · R_{ab}",
            "coefficient": "\\gamma"
          }
        ],
        "theory_track": "eh_anchored",
        "general": "√(-g) [ M_p² ( \\alpha · R  +  \\beta Λ^{-2} · R · R  +  \\gamma Λ^{-4} · ∇^{a}φ1 · ∇^{b}φ1 · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]",
        "lagrangian": {
          "n_terms": 5,
          "general": "√(-g) [ M_p² ( \\alpha · R  +  \\beta Λ^{-2} · R · R  +  \\gamma Λ^{-4} · ∇^{a}φ1 · ∇^{b}φ1 · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]",
          "terms": [
            {
              "coeff_symbol": "\\alpha",
              "coeff_token": "COEFF_0",
              "candidate": "R",
              "mass_dim": 2,
              "lambda_power": 0,
              "sector": "gravity"
            },
            {
              "coeff_symbol": "\\beta",
              "coeff_token": "COEFF_1",
              "candidate": "R · R",
              "mass_dim": 4,
              "lambda_power": -2,
              "sector": "gravity"
            },
            {
              "coeff_symbol": "\\gamma",
              "coeff_token": "COEFF_2",
              "candidate": "∇^{a}φ1 · ∇^{b}φ1 · R_{ab}",
              "mass_dim": 6,
              "lambda_power": -4,
              "sector": "non-minimal"
            },
            {
              "coeff_symbol": "1",
              "coeff_token": "COEFF_FIXED_1",
              "candidate": "-½ g^{μν} ∇_μφ1 ∇_νφ1",
              "mass_dim": 4,
              "lambda_power": 0,
              "fixed": true,
              "sector": "matter"
            },
            {
              "coeff_symbol": "1",
              "coeff_token": "COEFF_FIXED_1",
              "candidate": "-½ m_1² φ1²",
              "mass_dim": 4,
              "lambda_power": 0,
              "fixed": true,
              "sector": "matter",
              "potential_type": "quadratic"
            }
          ],
          "scalar_config": "phi1_only",
          "potential_types": {
            "phi1": "quadratic",
            "phi2": null
          }
        }
      }
    },
    {
      "timestamp": "2026-06-09T17:15:24-0400",
      "loop_id": "wave_0001_lag_14",
      "validated": true,
      "failed_stage": null,
      "entered_stages": [
        "EOM",
        "Builder",
        "Solver"
      ],
      "entered_solver": true,
      "best_lag_id": "14",
      "chi2": 1641.3645973979567,
      "aic": 1653.3645973979567,
      "bic": 1686.446852884995,
      "solver_output_dir": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0001/agent_solver_result/agent_solve",
      "model_ranking_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0001/agent_solver_result/agent_solve/model_ranking.csv",
      "scan_report_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0001/agent_solver_result/agent_solve/scan_report.txt",
      "theory": {
        "proposal_id": "cold_start_token_loop_01_batch_lag_14",
        "source_n_terms": 7,
        "source_local_number": 49,
        "scalar_config": "phi1_only",
        "potential_types": {
          "phi1": "quadratic",
          "phi2": null
        },
        "operators": [
          "R",
          "R^{b}_{a} · R^{cd} · R^{a}_{cbd}",
          "∇^{c}R^{ab} · ∇_{b}R_{ac}",
          "φ1 · φ1 · R^{ab} · R_{ab}",
          "∇^{a}φ1 · ∇^{b}φ1 · R_{ab}"
        ],
        "theory_track": "eh_anchored",
        "parameter_sample_count": 1000
      },
      "theory_track": "eh_anchored",
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R^{b}_{a} · R^{cd} · R^{a}_{cbd}+∇^{c}R^{ab} · ∇_{b}R_{ac}+φ1 · φ1 · R^{ab} · R_{ab}+∇^{a}φ1 · ∇^{b}φ1 · R_{ab}",
      "coarse_family_key": "scalar=phi1_only|phi1_potential=quadratic|phi2_potential=None|operator_bucket=R_anchor+derivative+high_curvature+scalar_curvature",
      "failure_tags": [
        "q_initial_root_failure",
        "h_absurdly_large",
        "no_accepted_samples"
      ],
      "top_reject_reasons": [
        {
          "lag_id": "14",
          "count": "576",
          "total_rejected_or_skipped": "869",
          "reason": "H(z) absurdly large"
        },
        {
          "lag_id": "14",
          "count": "293",
          "total_rejected_or_skipped": "869",
          "reason": "no acceptable real q1_0 root from E_N(x=0)=0"
        }
      ],
      "all_samples_summary_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0001/agent_solver_result/agent_solve/all_samples_summary.csv",
      "accepted_samples_summary_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0001/agent_solver_result/agent_solve/accepted_samples_summary.csv",
      "reject_reasons_by_model_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0001/agent_solver_result/agent_solve/reject_reasons_by_model.csv",
      "diagnostic_message": null,
      "agent_lagrangian": {
        "proposal_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/proposals/graph_agent_batch_208_split_v4/wave_0001_lag_14.json",
        "agent_lagrangians_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0001/agent_lagrangians.pkl",
        "agent_parameter_samples_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0001/agent_parameter_samples_by_lag_id.json",
        "proposal_id": "batch_lag_14",
        "source": "batch_token_level_grammar",
        "source_n_terms": 7,
        "source_local_number": 49,
        "batch_lag_id": "14",
        "scalar_config": "phi1_only",
        "potential_types": {
          "phi1": "quadratic",
          "phi2": null
        },
        "operators": [
          "R",
          "R^{b}_{a} · R^{cd} · R^{a}_{cbd}",
          "∇^{c}R^{ab} · ∇_{b}R_{ac}",
          "φ1 · φ1 · R^{ab} · R_{ab}",
          "∇^{a}φ1 · ∇^{b}φ1 · R_{ab}"
        ],
        "operator_specs": [
          {
            "candidate": "R",
            "coefficient": "\\alpha"
          },
          {
            "candidate": "R^{b}_{a} · R^{cd} · R^{a}_{cbd}",
            "coefficient": "\\beta"
          },
          {
            "candidate": "∇^{c}R^{ab} · ∇_{b}R_{ac}",
            "coefficient": "\\gamma"
          },
          {
            "candidate": "φ1 · φ1 · R^{ab} · R_{ab}",
            "coefficient": "\\delta"
          },
          {
            "candidate": "∇^{a}φ1 · ∇^{b}φ1 · R_{ab}",
            "coefficient": "\\epsilon"
          }
        ],
        "theory_track": "eh_anchored",
        "general": "√(-g) [ M_p² ( \\alpha · R  +  \\beta Λ^{-4} · R^{b}_{a} · R^{cd} · R^{a}_{cbd}  +  \\gamma Λ^{-4} · ∇^{c}R^{ab} · ∇_{b}R_{ac}  +  \\delta Λ^{-4} · φ1 · φ1 · R^{ab} · R_{ab}  +  \\epsilon Λ^{-4} · ∇^{a}φ1 · ∇^{b}φ1 · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]",
        "lagrangian": {
          "n_terms": 7,
          "general": "√(-g) [ M_p² ( \\alpha · R  +  \\beta Λ^{-4} · R^{b}_{a} · R^{cd} · R^{a}_{cbd}  +  \\gamma Λ^{-4} · ∇^{c}R^{ab} · ∇_{b}R_{ac}  +  \\delta Λ^{-4} · φ1 · φ1 · R^{ab} · R_{ab}  +  \\epsilon Λ^{-4} · ∇^{a}φ1 · ∇^{b}φ1 · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]",
          "terms": [
            {
              "coeff_symbol": "\\alpha",
              "coeff_token": "COEFF_0",
              "candidate": "R",
              "mass_dim": 2,
              "lambda_power": 0,
              "sector": "gravity"
            },
            {
              "coeff_symbol": "\\beta",
              "coeff_token": "COEFF_1",
              "candidate": "R^{b}_{a} · R^{cd} · R^{a}_{cbd}",
              "mass_dim": 6,
              "lambda_power": -4,
              "sector": "gravity"
            },
            {
              "coeff_symbol": "\\gamma",
              "coeff_token": "COEFF_2",
              "candidate": "∇^{c}R^{ab} · ∇_{b}R_{ac}",
              "mass_dim": 6,
              "lambda_power": -4,
              "sector": "gravity"
            },
            {
              "coeff_symbol": "\\delta",
              "coeff_token": "COEFF_3",
              "candidate": "φ1 · φ1 · R^{ab} · R_{ab}",
              "mass_dim": 6,
              "lambda_power": -4,
              "sector": "non-minimal"
            },
            {
              "coeff_symbol": "\\epsilon",
              "coeff_token": "COEFF_4",
              "candidate": "∇^{a}φ1 · ∇^{b}φ1 · R_{ab}",
              "mass_dim": 6,
              "lambda_power": -4,
              "sector": "non-minimal"
            },
            {
              "coeff_symbol": "1",
              "coeff_token": "COEFF_FIXED_1",
              "candidate": "-½ g^{μν} ∇_μφ1 ∇_νφ1",
              "mass_dim": 4,
              "lambda_power": 0,
              "fixed": true,
              "sector": "matter"
            },
            {
              "coeff_symbol": "1",
              "coeff_token": "COEFF_FIXED_1",
              "candidate": "-½ m_1² φ1²",
              "mass_dim": 4,
              "lambda_power": 0,
              "fixed": true,
              "sector": "matter",
              "potential_type": "quadratic"
            }
          ],
          "scalar_config": "phi1_only",
          "potential_types": {
            "phi1": "quadratic",
            "phi2": null
          }
        }
      }
    },
    {
      "timestamp": "2026-06-09T19:16:59-0400",
      "loop_id": "wave_0009_lag_10",
      "validated": true,
      "failed_stage": null,
      "entered_stages": [
        "EOM",
        "Builder",
        "Solver"
      ],
      "entered_solver": true,
      "best_lag_id": "10",
      "chi2": 1642.6351829275716,
      "aic": 1654.6351829275716,
      "bic": 1687.71743841461,
      "solver_output_dir": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0009/agent_solver_result/agent_solve",
      "model_ranking_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0009/agent_solver_result/agent_solve/model_ranking.csv",
      "scan_report_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0009/agent_solver_result/agent_solve/scan_report.txt",
      "theory": {
        "proposal_id": "cold_start_token_loop_09_batch_lag_10",
        "source_n_terms": 7,
        "source_local_number": 30,
        "scalar_config": "phi1_only",
        "potential_types": {
          "phi1": "quadratic",
          "phi2": null
        },
        "operators": [
          "R",
          "R · R",
          "∇^{a}∇_{a}R",
          "R^{ab} · R^{d}_{a} · R_{bd}",
          "∇^{a}φ1 · ∇^{b}φ1 · R_{ab}"
        ],
        "theory_track": "eh_anchored",
        "parameter_sample_count": 1000
      },
      "theory_track": "eh_anchored",
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R · R+∇^{a}∇_{a}R+R^{ab} · R^{d}_{a} · R_{bd}+∇^{a}φ1 · ∇^{b}φ1 · R_{ab}",
      "coarse_family_key": "scalar=phi1_only|phi1_potential=quadratic|phi2_potential=None|operator_bucket=R_anchor+derivative+high_curvature+scalar_curvature",
      "failure_tags": [
        "q_initial_root_failure",
        "h_absurdly_large",
        "no_accepted_samples"
      ],
      "top_reject_reasons": [
        {
          "lag_id": "10",
          "count": "537",
          "total_rejected_or_skipped": "869",
          "reason": "H(z) absurdly large"
        },
        {
          "lag_id": "10",
          "count": "332",
          "total_rejected_or_skipped": "869",
          "reason": "no acceptable real q1_0 root from E_N(x=0)=0"
        }
      ],
      "all_samples_summary_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0009/agent_solver_result/agent_solve/all_samples_summary.csv",
      "accepted_samples_summary_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0009/agent_solver_result/agent_solve/accepted_samples_summary.csv",
      "reject_reasons_by_model_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0009/agent_solver_result/agent_solve/reject_reasons_by_model.csv",
      "diagnostic_message": null,
      "agent_lagrangian": {
        "proposal_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/proposals/graph_agent_batch_208_split_v4/wave_0009_lag_10.json",
        "agent_lagrangians_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0009/agent_lagrangians.pkl",
        "agent_parameter_samples_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0009/agent_parameter_samples_by_lag_id.json",
        "proposal_id": "batch_lag_10",
        "source": "batch_token_level_grammar",
        "source_n_terms": 7,
        "source_local_number": 30,
        "batch_lag_id": "10",
        "scalar_config": "phi1_only",
        "potential_types": {
          "phi1": "quadratic",
          "phi2": null
        },
        "operators": [
          "R",
          "R · R",
          "∇^{a}∇_{a}R",
          "R^{ab} · R^{d}_{a} · R_{bd}",
          "∇^{a}φ1 · ∇^{b}φ1 · R_{ab}"
        ],
        "operator_specs": [
          {
            "candidate": "R",
            "coefficient": "\\alpha"
          },
          {
            "candidate": "R · R",
            "coefficient": "\\beta"
          },
          {
            "candidate": "∇^{a}∇_{a}R",
            "coefficient": "\\gamma"
          },
          {
            "candidate": "R^{ab} · R^{d}_{a} · R_{bd}",
            "coefficient": "\\delta"
          },
          {
            "candidate": "∇^{a}φ1 · ∇^{b}φ1 · R_{ab}",
            "coefficient": "\\epsilon"
          }
        ],
        "theory_track": "eh_anchored",
        "general": "√(-g) [ M_p² ( \\alpha · R  +  \\beta Λ^{-2} · R · R  +  \\gamma Λ^{-2} · ∇^{a}∇_{a}R  +  \\delta Λ^{-4} · R^{ab} · R^{d}_{a} · R_{bd}  +  \\epsilon Λ^{-4} · ∇^{a}φ1 · ∇^{b}φ1 · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]",
        "lagrangian": {
          "n_terms": 7,
          "general": "√(-g) [ M_p² ( \\alpha · R  +  \\beta Λ^{-2} · R · R  +  \\gamma Λ^{-2} · ∇^{a}∇_{a}R  +  \\delta Λ^{-4} · R^{ab} · R^{d}_{a} · R_{bd}  +  \\epsilon Λ^{-4} · ∇^{a}φ1 · ∇^{b}φ1 · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]",
          "terms": [
            {
              "coeff_symbol": "\\alpha",
              "coeff_token": "COEFF_0",
              "candidate": "R",
              "mass_dim": 2,
              "lambda_power": 0,
              "sector": "gravity"
            },
            {
              "coeff_symbol": "\\beta",
              "coeff_token": "COEFF_1",
              "candidate": "R · R",
              "mass_dim": 4,
              "lambda_power": -2,
              "sector": "gravity"
            },
            {
              "coeff_symbol": "\\gamma",
              "coeff_token": "COEFF_2",
              "candidate": "∇^{a}∇_{a}R",
              "mass_dim": 4,
              "lambda_power": -2,
              "sector": "gravity"
            },
            {
              "coeff_symbol": "\\delta",
              "coeff_token": "COEFF_3",
              "candidate": "R^{ab} · R^{d}_{a} · R_{bd}",
              "mass_dim": 6,
              "lambda_power": -4,
              "sector": "gravity"
            },
            {
              "coeff_symbol": "\\epsilon",
              "coeff_token": "COEFF_4",
              "candidate": "∇^{a}φ1 · ∇^{b}φ1 · R_{ab}",
              "mass_dim": 6,
              "lambda_power": -4,
              "sector": "non-minimal"
            },
            {
              "coeff_symbol": "1",
              "coeff_token": "COEFF_FIXED_1",
              "candidate": "-½ g^{μν} ∇_μφ1 ∇_νφ1",
              "mass_dim": 4,
              "lambda_power": 0,
              "fixed": true,
              "sector": "matter"
            },
            {
              "coeff_symbol": "1",
              "coeff_token": "COEFF_FIXED_1",
              "candidate": "-½ m_1² φ1²",
              "mass_dim": 4,
              "lambda_power": 0,
              "fixed": true,
              "sector": "matter",
              "potential_type": "quadratic"
            }
          ],
          "scalar_config": "phi1_only",
          "potential_types": {
            "phi1": "quadratic",
            "phi2": null
          }
        }
      }
    },
    {
      "timestamp": "2026-06-09T18:10:47-0400",
      "loop_id": "wave_0005_lag_11",
      "validated": true,
      "failed_stage": null,
      "entered_stages": [
        "EOM",
        "Builder",
        "Solver"
      ],
      "entered_solver": true,
      "best_lag_id": "11",
      "chi2": 1643.4845278706275,
      "aic": 1655.4845278706275,
      "bic": 1688.5667833576658,
      "solver_output_dir": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0005/agent_solver_result/agent_solve",
      "model_ranking_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0005/agent_solver_result/agent_solve/model_ranking.csv",
      "scan_report_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0005/agent_solver_result/agent_solve/scan_report.txt",
      "theory": {
        "proposal_id": "cold_start_token_loop_05_batch_lag_11",
        "source_n_terms": 7,
        "source_local_number": 32,
        "scalar_config": "phi1_only",
        "potential_types": {
          "phi1": "quadratic",
          "phi2": null
        },
        "operators": [
          "R",
          "R_{ab} · R^{adef} · R^{b}_{def}",
          "φ1 · R^{ab} · R_{ab}",
          "∇^{a}φ1 · ∇_{a}φ1 · R",
          "∇^{a}φ1 · ∇^{b}φ1 · R_{ab}"
        ],
        "theory_track": "eh_anchored",
        "parameter_sample_count": 1000
      },
      "theory_track": "eh_anchored",
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R_{ab} · R^{adef} · R^{b}_{def}+φ1 · R^{ab} · R_{ab}+∇^{a}φ1 · ∇_{a}φ1 · R+∇^{a}φ1 · ∇^{b}φ1 · R_{ab}",
      "coarse_family_key": "scalar=phi1_only|phi1_potential=quadratic|phi2_potential=None|operator_bucket=R_anchor+derivative+high_curvature+scalar_curvature",
      "failure_tags": [
        "q_initial_root_failure",
        "h_absurdly_large"
      ],
      "top_reject_reasons": [
        {
          "lag_id": "11",
          "count": "582",
          "total_rejected_or_skipped": "868",
          "reason": "H(z) absurdly large"
        },
        {
          "lag_id": "11",
          "count": "286",
          "total_rejected_or_skipped": "868",
          "reason": "no acceptable real q1_0 root from E_N(x=0)=0"
        }
      ],
      "all_samples_summary_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0005/agent_solver_result/agent_solve/all_samples_summary.csv",
      "accepted_samples_summary_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0005/agent_solver_result/agent_solve/accepted_samples_summary.csv",
      "reject_reasons_by_model_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0005/agent_solver_result/agent_solve/reject_reasons_by_model.csv",
      "diagnostic_message": null,
      "agent_lagrangian": {
        "proposal_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/proposals/graph_agent_batch_208_split_v4/wave_0005_lag_11.json",
        "agent_lagrangians_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0005/agent_lagrangians.pkl",
        "agent_parameter_samples_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0005/agent_parameter_samples_by_lag_id.json",
        "proposal_id": "batch_lag_11",
        "source": "batch_token_level_grammar",
        "source_n_terms": 7,
        "source_local_number": 32,
        "batch_lag_id": "11",
        "scalar_config": "phi1_only",
        "potential_types": {
          "phi1": "quadratic",
          "phi2": null
        },
        "operators": [
          "R",
          "R_{ab} · R^{adef} · R^{b}_{def}",
          "φ1 · R^{ab} · R_{ab}",
          "∇^{a}φ1 · ∇_{a}φ1 · R",
          "∇^{a}φ1 · ∇^{b}φ1 · R_{ab}"
        ],
        "operator_specs": [
          {
            "candidate": "R",
            "coefficient": "\\alpha"
          },
          {
            "candidate": "R_{ab} · R^{adef} · R^{b}_{def}",
            "coefficient": "\\beta"
          },
          {
            "candidate": "φ1 · R^{ab} · R_{ab}",
            "coefficient": "\\gamma"
          },
          {
            "candidate": "∇^{a}φ1 · ∇_{a}φ1 · R",
            "coefficient": "\\delta"
          },
          {
            "candidate": "∇^{a}φ1 · ∇^{b}φ1 · R_{ab}",
            "coefficient": "\\epsilon"
          }
        ],
        "theory_track": "eh_anchored",
        "general": "√(-g) [ M_p² ( \\alpha · R  +  \\beta Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def}  +  \\gamma Λ^{-3} · φ1 · R^{ab} · R_{ab}  +  \\delta Λ^{-4} · ∇^{a}φ1 · ∇_{a}φ1 · R  +  \\epsilon Λ^{-4} · ∇^{a}φ1 · ∇^{b}φ1 · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]",
        "lagrangian": {
          "n_terms": 7,
          "general": "√(-g) [ M_p² ( \\alpha · R  +  \\beta Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def}  +  \\gamma Λ^{-3} · φ1 · R^{ab} · R_{ab}  +  \\delta Λ^{-4} · ∇^{a}φ1 · ∇_{a}φ1 · R  +  \\epsilon Λ^{-4} · ∇^{a}φ1 · ∇^{b}φ1 · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]",
          "terms": [
            {
              "coeff_symbol": "\\alpha",
              "coeff_token": "COEFF_0",
              "candidate": "R",
              "mass_dim": 2,
              "lambda_power": 0,
              "sector": "gravity"
            },
            {
              "coeff_symbol": "\\beta",
              "coeff_token": "COEFF_1",
              "candidate": "R_{ab} · R^{adef} · R^{b}_{def}",
              "mass_dim": 6,
              "lambda_power": -4,
              "sector": "gravity"
            },
            {
              "coeff_symbol": "\\gamma",
              "coeff_token": "COEFF_2",
              "candidate": "φ1 · R^{ab} · R_{ab}",
              "mass_dim": 5,
              "lambda_power": -3,
              "sector": "non-minimal"
            },
            {
              "coeff_symbol": "\\delta",
              "coeff_token": "COEFF_3",
              "candidate": "∇^{a}φ1 · ∇_{a}φ1 · R",
              "mass_dim": 6,
              "lambda_power": -4,
              "sector": "non-minimal"
            },
            {
              "coeff_symbol": "\\epsilon",
              "coeff_token": "COEFF_4",
              "candidate": "∇^{a}φ1 · ∇^{b}φ1 · R_{ab}",
              "mass_dim": 6,
              "lambda_power": -4,
              "sector": "non-minimal"
            },
            {
              "coeff_symbol": "1",
              "coeff_token": "COEFF_FIXED_1",
              "candidate": "-½ g^{μν} ∇_μφ1 ∇_νφ1",
              "mass_dim": 4,
              "lambda_power": 0,
              "fixed": true,
              "sector": "matter"
            },
            {
              "coeff_symbol": "1",
              "coeff_token": "COEFF_FIXED_1",
              "candidate": "-½ m_1² φ1²",
              "mass_dim": 4,
              "lambda_power": 0,
              "fixed": true,
              "sector": "matter",
              "potential_type": "quadratic"
            }
          ],
          "scalar_config": "phi1_only",
          "potential_types": {
            "phi1": "quadratic",
            "phi2": null
          }
        }
      }
    },
    {
      "timestamp": "2026-06-09T17:56:11-0400",
      "loop_id": "wave_0004_lag_12",
      "validated": true,
      "failed_stage": null,
      "entered_stages": [
        "EOM",
        "Builder",
        "Solver"
      ],
      "entered_solver": true,
      "best_lag_id": "12",
      "chi2": 1643.4936037562254,
      "aic": 1655.4936037562254,
      "bic": 1688.5758592432637,
      "solver_output_dir": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0004/agent_solver_result/agent_solve",
      "model_ranking_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0004/agent_solver_result/agent_solve/model_ranking.csv",
      "scan_report_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0004/agent_solver_result/agent_solve/scan_report.txt",
      "theory": {
        "proposal_id": "cold_start_token_loop_04_batch_lag_12",
        "source_n_terms": 4,
        "source_local_number": 22,
        "scalar_config": "phi1_only",
        "potential_types": {
          "phi1": "quadratic",
          "phi2": null
        },
        "operators": [
          "R",
          "∇^{a}φ1 · ∇_{a}φ1 · R"
        ],
        "theory_track": "eh_anchored",
        "parameter_sample_count": 1000
      },
      "theory_track": "eh_anchored",
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+∇^{a}φ1 · ∇_{a}φ1 · R",
      "coarse_family_key": "scalar=phi1_only|phi1_potential=quadratic|phi2_potential=None|operator_bucket=R_anchor+derivative+scalar_curvature",
      "failure_tags": [
        "q_initial_root_failure",
        "h_absurdly_large",
        "no_accepted_samples"
      ],
      "top_reject_reasons": [
        {
          "lag_id": "12",
          "count": "551",
          "total_rejected_or_skipped": "868",
          "reason": "H(z) absurdly large"
        },
        {
          "lag_id": "12",
          "count": "317",
          "total_rejected_or_skipped": "868",
          "reason": "no acceptable real q1_0 root from E_N(x=0)=0"
        }
      ],
      "all_samples_summary_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0004/agent_solver_result/agent_solve/all_samples_summary.csv",
      "accepted_samples_summary_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0004/agent_solver_result/agent_solve/accepted_samples_summary.csv",
      "reject_reasons_by_model_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0004/agent_solver_result/agent_solve/reject_reasons_by_model.csv",
      "diagnostic_message": null,
      "agent_lagrangian": {
        "proposal_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/proposals/graph_agent_batch_208_split_v4/wave_0004_lag_12.json",
        "agent_lagrangians_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0004/agent_lagrangians.pkl",
        "agent_parameter_samples_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0004/agent_parameter_samples_by_lag_id.json",
        "proposal_id": "batch_lag_12",
        "source": "batch_token_level_grammar",
        "source_n_terms": 4,
        "source_local_number": 22,
        "batch_lag_id": "12",
        "scalar_config": "phi1_only",
        "potential_types": {
          "phi1": "quadratic",
          "phi2": null
        },
        "operators": [
          "R",
          "∇^{a}φ1 · ∇_{a}φ1 · R"
        ],
        "operator_specs": [
          {
            "candidate": "R",
            "coefficient": "\\alpha"
          },
          {
            "candidate": "∇^{a}φ1 · ∇_{a}φ1 · R",
            "coefficient": "\\beta"
          }
        ],
        "theory_track": "eh_anchored",
        "general": "√(-g) [ M_p² ( \\alpha · R  +  \\beta Λ^{-4} · ∇^{a}φ1 · ∇_{a}φ1 · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]",
        "lagrangian": {
          "n_terms": 4,
          "general": "√(-g) [ M_p² ( \\alpha · R  +  \\beta Λ^{-4} · ∇^{a}φ1 · ∇_{a}φ1 · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]",
          "terms": [
            {
              "coeff_symbol": "\\alpha",
              "coeff_token": "COEFF_0",
              "candidate": "R",
              "mass_dim": 2,
              "lambda_power": 0,
              "sector": "gravity"
            },
            {
              "coeff_symbol": "\\beta",
              "coeff_token": "COEFF_1",
              "candidate": "∇^{a}φ1 · ∇_{a}φ1 · R",
              "mass_dim": 6,
              "lambda_power": -4,
              "sector": "non-minimal"
            },
            {
              "coeff_symbol": "1",
              "coeff_token": "COEFF_FIXED_1",
              "candidate": "-½ g^{μν} ∇_μφ1 ∇_νφ1",
              "mass_dim": 4,
              "lambda_power": 0,
              "fixed": true,
              "sector": "matter"
            },
            {
              "coeff_symbol": "1",
              "coeff_token": "COEFF_FIXED_1",
              "candidate": "-½ m_1² φ1²",
              "mass_dim": 4,
              "lambda_power": 0,
              "fixed": true,
              "sector": "matter",
              "potential_type": "quadratic"
            }
          ],
          "scalar_config": "phi1_only",
          "potential_types": {
            "phi1": "quadratic",
            "phi2": null
          }
        }
      }
    },
    {
      "timestamp": "2026-06-09T17:29:06-0400",
      "loop_id": "wave_0002_lag_4",
      "validated": true,
      "failed_stage": null,
      "entered_stages": [
        "EOM",
        "Builder",
        "Solver"
      ],
      "entered_solver": true,
      "best_lag_id": "4",
      "chi2": 1643.8926784757662,
      "aic": 1655.8926784757662,
      "bic": 1688.9749339628045,
      "solver_output_dir": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0002/agent_solver_result/agent_solve",
      "model_ranking_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0002/agent_solver_result/agent_solve/model_ranking.csv",
      "scan_report_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0002/agent_solver_result/agent_solve/scan_report.txt",
      "theory": {
        "proposal_id": "cold_start_token_loop_02_batch_lag_4",
        "source_n_terms": 4,
        "source_local_number": 28,
        "scalar_config": "phi1_only",
        "potential_types": {
          "phi1": "quadratic",
          "phi2": null
        },
        "operators": [
          "R",
          "φ1 · φ1 · R^{ab} · R_{ab}"
        ],
        "theory_track": "eh_anchored",
        "parameter_sample_count": 1000
      },
      "theory_track": "eh_anchored",
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+φ1 · φ1 · R^{ab} · R_{ab}",
      "coarse_family_key": "scalar=phi1_only|phi1_potential=quadratic|phi2_potential=None|operator_bucket=R_anchor+high_curvature+scalar_curvature",
      "failure_tags": [
        "q_initial_root_failure",
        "h_absurdly_large"
      ],
      "top_reject_reasons": [
        {
          "lag_id": "4",
          "count": "573",
          "total_rejected_or_skipped": "864",
          "reason": "H(z) absurdly large"
        },
        {
          "lag_id": "4",
          "count": "291",
          "total_rejected_or_skipped": "864",
          "reason": "no acceptable real q1_0 root from E_N(x=0)=0"
        }
      ],
      "all_samples_summary_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0002/agent_solver_result/agent_solve/all_samples_summary.csv",
      "accepted_samples_summary_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0002/agent_solver_result/agent_solve/accepted_samples_summary.csv",
      "reject_reasons_by_model_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0002/agent_solver_result/agent_solve/reject_reasons_by_model.csv",
      "diagnostic_message": null,
      "agent_lagrangian": {
        "proposal_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/proposals/graph_agent_batch_208_split_v4/wave_0002_lag_4.json",
        "agent_lagrangians_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0002/agent_lagrangians.pkl",
        "agent_parameter_samples_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0002/agent_parameter_samples_by_lag_id.json",
        "proposal_id": "batch_lag_4",
        "source": "batch_token_level_grammar",
        "source_n_terms": 4,
        "source_local_number": 28,
        "batch_lag_id": "4",
        "scalar_config": "phi1_only",
        "potential_types": {
          "phi1": "quadratic",
          "phi2": null
        },
        "operators": [
          "R",
          "φ1 · φ1 · R^{ab} · R_{ab}"
        ],
        "operator_specs": [
          {
            "candidate": "R",
            "coefficient": "\\alpha"
          },
          {
            "candidate": "φ1 · φ1 · R^{ab} · R_{ab}",
            "coefficient": "\\beta"
          }
        ],
        "theory_track": "eh_anchored",
        "general": "√(-g) [ M_p² ( \\alpha · R  +  \\beta Λ^{-4} · φ1 · φ1 · R^{ab} · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]",
        "lagrangian": {
          "n_terms": 4,
          "general": "√(-g) [ M_p² ( \\alpha · R  +  \\beta Λ^{-4} · φ1 · φ1 · R^{ab} · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]",
          "terms": [
            {
              "coeff_symbol": "\\alpha",
              "coeff_token": "COEFF_0",
              "candidate": "R",
              "mass_dim": 2,
              "lambda_power": 0,
              "sector": "gravity"
            },
            {
              "coeff_symbol": "\\beta",
              "coeff_token": "COEFF_1",
              "candidate": "φ1 · φ1 · R^{ab} · R_{ab}",
              "mass_dim": 6,
              "lambda_power": -4,
              "sector": "non-minimal"
            },
            {
              "coeff_symbol": "1",
              "coeff_token": "COEFF_FIXED_1",
              "candidate": "-½ g^{μν} ∇_μφ1 ∇_νφ1",
              "mass_dim": 4,
              "lambda_power": 0,
              "fixed": true,
              "sector": "matter"
            },
            {
              "coeff_symbol": "1",
              "coeff_token": "COEFF_FIXED_1",
              "candidate": "-½ m_1² φ1²",
              "mass_dim": 4,
              "lambda_power": 0,
              "fixed": true,
              "sector": "matter",
              "potential_type": "quadratic"
            }
          ],
          "scalar_config": "phi1_only",
          "potential_types": {
            "phi1": "quadratic",
            "phi2": null
          }
        }
      }
    },
    {
      "timestamp": "2026-06-09T18:13:08-0400",
      "loop_id": "wave_0005_lag_6",
      "validated": true,
      "failed_stage": null,
      "entered_stages": [
        "EOM",
        "Builder",
        "Solver"
      ],
      "entered_solver": true,
      "best_lag_id": "6",
      "chi2": 1644.8034172595212,
      "aic": 1658.8034172595212,
      "bic": 1697.3993819943992,
      "solver_output_dir": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0005/agent_solver_result/agent_solve",
      "model_ranking_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0005/agent_solver_result/agent_solve/model_ranking.csv",
      "scan_report_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0005/agent_solver_result/agent_solve/scan_report.txt",
      "theory": {
        "proposal_id": "cold_start_token_loop_05_batch_lag_6",
        "source_n_terms": 4,
        "source_local_number": 32,
        "scalar_config": "phi1_only",
        "potential_types": {
          "phi1": "quadratic",
          "phi2": null
        },
        "operators": [
          "R",
          "φ1 · ∇^{a}∇_{a}φ1"
        ],
        "theory_track": "eh_anchored",
        "parameter_sample_count": 1000
      },
      "theory_track": "eh_anchored",
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+φ1 · ∇^{a}∇_{a}φ1",
      "coarse_family_key": "scalar=phi1_only|phi1_potential=quadratic|phi2_potential=None|operator_bucket=R_anchor+derivative",
      "failure_tags": [
        "q_initial_root_failure",
        "h_absurdly_large",
        "constraint_drift"
      ],
      "top_reject_reasons": [
        {
          "lag_id": "6",
          "count": "585",
          "total_rejected_or_skipped": "861",
          "reason": "H(z) absurdly large"
        },
        {
          "lag_id": "6",
          "count": "275",
          "total_rejected_or_skipped": "861",
          "reason": "no acceptable real q1_0 root from E_N(x=0)=0"
        },
        {
          "lag_id": "6",
          "count": "1",
          "total_rejected_or_skipped": "861",
          "reason": "constraint drift too large: max|C|=1.157e-04"
        }
      ],
      "all_samples_summary_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0005/agent_solver_result/agent_solve/all_samples_summary.csv",
      "accepted_samples_summary_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0005/agent_solver_result/agent_solve/accepted_samples_summary.csv",
      "reject_reasons_by_model_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0005/agent_solver_result/agent_solve/reject_reasons_by_model.csv",
      "diagnostic_message": null,
      "agent_lagrangian": {
        "proposal_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/proposals/graph_agent_batch_208_split_v4/wave_0005_lag_6.json",
        "agent_lagrangians_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0005/agent_lagrangians.pkl",
        "agent_parameter_samples_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0005/agent_parameter_samples_by_lag_id.json",
        "proposal_id": "batch_lag_6",
        "source": "batch_token_level_grammar",
        "source_n_terms": 4,
        "source_local_number": 32,
        "batch_lag_id": "6",
        "scalar_config": "phi1_only",
        "potential_types": {
          "phi1": "quadratic",
          "phi2": null
        },
        "operators": [
          "R",
          "φ1 · ∇^{a}∇_{a}φ1"
        ],
        "operator_specs": [
          {
            "candidate": "R",
            "coefficient": "\\alpha"
          },
          {
            "candidate": "φ1 · ∇^{a}∇_{a}φ1",
            "coefficient": "\\beta"
          }
        ],
        "theory_track": "eh_anchored",
        "general": "√(-g) [ M_p² ( \\alpha · R )  +  \\beta · φ1 · ∇^{a}∇_{a}φ1  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]",
        "lagrangian": {
          "n_terms": 4,
          "general": "√(-g) [ M_p² ( \\alpha · R )  +  \\beta · φ1 · ∇^{a}∇_{a}φ1  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]",
          "terms": [
            {
              "coeff_symbol": "\\alpha",
              "coeff_token": "COEFF_0",
              "candidate": "R",
              "mass_dim": 2,
              "lambda_power": 0,
              "sector": "gravity"
            },
            {
              "coeff_symbol": "\\beta",
              "coeff_token": "COEFF_1",
              "candidate": "φ1 · ∇^{a}∇_{a}φ1",
              "mass_dim": 4,
              "lambda_power": 0,
              "sector": "scalar"
            },
            {
              "coeff_symbol": "1",
              "coeff_token": "COEFF_FIXED_1",
              "candidate": "-½ g^{μν} ∇_μφ1 ∇_νφ1",
              "mass_dim": 4,
              "lambda_power": 0,
              "fixed": true,
              "sector": "matter"
            },
            {
              "coeff_symbol": "1",
              "coeff_token": "COEFF_FIXED_1",
              "candidate": "-½ m_1² φ1²",
              "mass_dim": 4,
              "lambda_power": 0,
              "fixed": true,
              "sector": "matter",
              "potential_type": "quadratic"
            }
          ],
          "scalar_config": "phi1_only",
          "potential_types": {
            "phi1": "quadratic",
            "phi2": null
          }
        }
      }
    }
  ],
  "by_family": [
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R",
      "attempts": 10,
      "validated": 10,
      "entered_solver": 10,
      "failed_stage_counts": {},
      "failure_tag_counts": {
        "q_initial_root_failure": 10,
        "h_absurdly_large": 10,
        "no_accepted_samples": 8,
        "constraint_drift": 4
      },
      "best_chi2": 1638.0428393360799
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'axion', 'phi2': None}|operators=R",
      "attempts": 2,
      "validated": 2,
      "entered_solver": 2,
      "failed_stage_counts": {},
      "failure_tag_counts": {
        "q_initial_root_failure": 2,
        "h_absurdly_large": 2,
        "no_accepted_samples": 1
      },
      "best_chi2": 1656.395923088284
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+φ1 · ∇^{a}∇_{a}R",
      "attempts": 1,
      "validated": 1,
      "entered_solver": 1,
      "failed_stage_counts": {},
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "h_absurdly_large": 1,
        "constraint_drift": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": 1639.0299359874105
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R · R+∇^{a}φ1 · ∇^{b}φ1 · R_{ab}",
      "attempts": 1,
      "validated": 1,
      "entered_solver": 1,
      "failed_stage_counts": {},
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "h_absurdly_large": 1,
        "constraint_drift": 1
      },
      "best_chi2": 1640.9593449034116
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R^{b}_{a} · R^{cd} · R^{a}_{cbd}+∇^{c}R^{ab} · ∇_{b}R_{ac}+φ1 · φ1 · R^{ab} · R_{ab}+∇^{a}φ1 · ∇^{b}φ1 · R_{ab}",
      "attempts": 1,
      "validated": 1,
      "entered_solver": 1,
      "failed_stage_counts": {},
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "h_absurdly_large": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": 1641.3645973979567
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R · R+∇^{a}∇_{a}R+R^{ab} · R^{d}_{a} · R_{bd}+∇^{a}φ1 · ∇^{b}φ1 · R_{ab}",
      "attempts": 1,
      "validated": 1,
      "entered_solver": 1,
      "failed_stage_counts": {},
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "h_absurdly_large": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": 1642.6351829275716
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R_{ab} · R^{adef} · R^{b}_{def}+φ1 · R^{ab} · R_{ab}+∇^{a}φ1 · ∇_{a}φ1 · R+∇^{a}φ1 · ∇^{b}φ1 · R_{ab}",
      "attempts": 1,
      "validated": 1,
      "entered_solver": 1,
      "failed_stage_counts": {},
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "h_absurdly_large": 1
      },
      "best_chi2": 1643.4845278706275
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+∇^{a}φ1 · ∇_{a}φ1 · R",
      "attempts": 1,
      "validated": 1,
      "entered_solver": 1,
      "failed_stage_counts": {},
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "h_absurdly_large": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": 1643.4936037562254
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+φ1 · φ1 · R^{ab} · R_{ab}",
      "attempts": 1,
      "validated": 1,
      "entered_solver": 1,
      "failed_stage_counts": {},
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "h_absurdly_large": 1
      },
      "best_chi2": 1643.8926784757662
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+φ1 · ∇^{a}∇_{a}φ1",
      "attempts": 1,
      "validated": 1,
      "entered_solver": 1,
      "failed_stage_counts": {},
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "h_absurdly_large": 1,
        "constraint_drift": 1
      },
      "best_chi2": 1644.8034172595212
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+∇^{a}φ1 · ∇^{b}φ1 · R_{ab}",
      "attempts": 1,
      "validated": 1,
      "entered_solver": 1,
      "failed_stage_counts": {},
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "h_absurdly_large": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": 1645.3623050218675
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+∇^{c}R^{ab} · ∇_{b}R_{ac}",
      "attempts": 1,
      "validated": 1,
      "entered_solver": 1,
      "failed_stage_counts": {},
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "h_absurdly_large": 1,
        "constraint_drift": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": 1645.4406385861453
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+∇^{a}∇_{a}R+∇^{a}φ1 · ∇_{a}φ1",
      "attempts": 1,
      "validated": 1,
      "entered_solver": 1,
      "failed_stage_counts": {},
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "h_absurdly_large": 1
      },
      "best_chi2": 1646.3239580615752
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R · R+φ1 · φ1 · R · R",
      "attempts": 1,
      "validated": 1,
      "entered_solver": 1,
      "failed_stage_counts": {},
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "h_absurdly_large": 1,
        "constraint_drift": 1
      },
      "best_chi2": 1647.009655113607
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R^{ab} · R_{ab}",
      "attempts": 1,
      "validated": 1,
      "entered_solver": 1,
      "failed_stage_counts": {},
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "h_absurdly_large": 1
      },
      "best_chi2": 1647.0380923153227
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'axion', 'phi2': None}|operators=R+∇^{a}∇_{a}φ1 · R+φ1 · ∇^{a}∇_{a}φ1 · R+∇^{a}φ1 · ∇_{a}φ1 · R",
      "attempts": 1,
      "validated": 1,
      "entered_solver": 1,
      "failed_stage_counts": {},
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "h_absurdly_large": 1,
        "constraint_drift": 1
      },
      "best_chi2": 1647.3876439579699
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R · R^{bcd}_{a} · R^{a}_{bcd}",
      "attempts": 1,
      "validated": 1,
      "entered_solver": 1,
      "failed_stage_counts": {},
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "h_absurdly_large": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": 1648.0789432823628
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'axion', 'phi2': None}|operators=R+∇^{a}φ1 · ∇_{a}φ1",
      "attempts": 1,
      "validated": 1,
      "entered_solver": 1,
      "failed_stage_counts": {},
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "h_absurdly_large": 1,
        "constraint_drift": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": 1651.9561626509249
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+∇^{a}∇^{b}φ1 · R_{ab}+∇^{a}φ1 · ∇_{a}φ1 · R",
      "attempts": 1,
      "validated": 1,
      "entered_solver": 1,
      "failed_stage_counts": {},
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "h_absurdly_large": 1,
        "constraint_drift": 1
      },
      "best_chi2": 1652.48397719067
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R · R+R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh}+∇^{c}R^{ab} · ∇_{b}R_{ac}+φ1 · R^{bcd}_{a} · R^{a}_{bcd}+φ1 · φ1 · ∇^{a}∇_{a}R+∇^{a}φ1 · ∇_{a}φ1 · R+φ1 · ∇^{a}∇_{a}φ1",
      "attempts": 1,
      "validated": 1,
      "entered_solver": 1,
      "failed_stage_counts": {},
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "h_absurdly_large": 1,
        "constraint_drift": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": 1654.4503043576042
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+∇^{a}∇_{a}R+∇^{c}R^{ab} · ∇_{b}R_{ac}",
      "attempts": 1,
      "validated": 1,
      "entered_solver": 1,
      "failed_stage_counts": {},
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "h_absurdly_large": 1,
        "constraint_drift": 1
      },
      "best_chi2": 1655.8172908708184
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+∇^{a}φ1 · ∇_{a}R+φ1 · φ1 · R^{ab} · R_{ab}",
      "attempts": 1,
      "validated": 1,
      "entered_solver": 1,
      "failed_stage_counts": {},
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "h_absurdly_large": 1,
        "constraint_drift": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": 1657.377147319971
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R_{ab} · R^{adef} · R^{b}_{def}+∇^{c}R^{ab} · ∇_{c}R_{ab}",
      "attempts": 1,
      "validated": 1,
      "entered_solver": 1,
      "failed_stage_counts": {},
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "h_absurdly_large": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": 1657.9150168492877
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+φ1 · R^{bcd}_{a} · R^{a}_{bcd}",
      "attempts": 1,
      "validated": 1,
      "entered_solver": 1,
      "failed_stage_counts": {},
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "h_absurdly_large": 1,
        "constraint_drift": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": 1659.2520646320763
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R^{ab} · R_{ab}+φ1 · R^{ab} · R_{ab}",
      "attempts": 1,
      "validated": 1,
      "entered_solver": 1,
      "failed_stage_counts": {},
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "h_absurdly_large": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": 1659.639068169537
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R · R+∇^{a}∇_{a}R",
      "attempts": 1,
      "validated": 1,
      "entered_solver": 1,
      "failed_stage_counts": {},
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "h_absurdly_large": 1,
        "constraint_drift": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": 1662.2489089415174
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R^{bcd}_{a} · R^{a}_{bcd}+φ1 · R · R",
      "attempts": 1,
      "validated": 1,
      "entered_solver": 1,
      "failed_stage_counts": {},
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "h_absurdly_large": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": 1663.3800643727589
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R_{ab} · R^{adef} · R^{b}_{def}",
      "attempts": 1,
      "validated": 1,
      "entered_solver": 1,
      "failed_stage_counts": {},
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "h_absurdly_large": 1,
        "constraint_drift": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": 1665.6260267604534
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R^{bcd}_{a} · R^{a}_{bcd}+φ1 · ∇^{a}∇_{a}R+∇^{a}φ1 · ∇_{a}R+∇^{a}φ1 · ∇^{b}φ1 · R_{ab}+φ1 · φ1",
      "attempts": 1,
      "validated": 1,
      "entered_solver": 1,
      "failed_stage_counts": {},
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "h_absurdly_large": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": 1667.279645805869
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+φ1 · R · R",
      "attempts": 1,
      "validated": 1,
      "entered_solver": 1,
      "failed_stage_counts": {},
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "h_absurdly_large": 1,
        "constraint_drift": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": 1674.133155921741
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+φ1 · ∇^{a}∇_{a}R+∇^{a}φ1 · ∇_{a}φ1",
      "attempts": 1,
      "validated": 1,
      "entered_solver": 1,
      "failed_stage_counts": {},
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "h_absurdly_large": 1,
        "constraint_drift": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": 1674.5684154814971
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+φ1 · R^{ab} · R_{ab}",
      "attempts": 1,
      "validated": 1,
      "entered_solver": 1,
      "failed_stage_counts": {},
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "h_absurdly_large": 1,
        "constraint_drift": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": 1678.5620032280685
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+∇^{a}R · ∇_{a}R",
      "attempts": 1,
      "validated": 1,
      "entered_solver": 1,
      "failed_stage_counts": {},
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "h_absurdly_large": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": 1691.8814696705708
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+∇^{a}φ1 · ∇_{a}φ1 · R+∇^{a}φ1 · ∇^{b}φ1 · R_{ab}",
      "attempts": 1,
      "validated": 1,
      "entered_solver": 1,
      "failed_stage_counts": {},
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "h_absurdly_large": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": 1691.9087862874312
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R · R^{ab} · R_{ab}",
      "attempts": 1,
      "validated": 1,
      "entered_solver": 1,
      "failed_stage_counts": {},
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "h_absurdly_large": 1,
        "constraint_drift": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": 1691.9969478142632
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R · R+R^{ab} · R_{ab}+∇^{a}∇_{a}R+∇^{a}∇_{a}R · R^{c}_{c}+φ1 · R^{ab} · R_{ab}+∇^{a}φ1 · ∇_{a}φ1 · R+φ1 · ∇^{a}∇_{a}φ1",
      "attempts": 1,
      "validated": 1,
      "entered_solver": 1,
      "failed_stage_counts": {},
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "h_absurdly_large": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": 1693.3569227180426
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R^{b}_{a} · R^{cd} · R^{a}_{cbd}",
      "attempts": 1,
      "validated": 1,
      "entered_solver": 1,
      "failed_stage_counts": {},
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "h_absurdly_large": 1,
        "constraint_drift": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": 1693.848344636445
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+φ1 · φ1 · R · R",
      "attempts": 1,
      "validated": 1,
      "entered_solver": 1,
      "failed_stage_counts": {},
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "h_absurdly_large": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": 1693.8778372526913
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R^{ab} · R_{ab}+∇^{a}φ1 · ∇^{b}φ1 · R_{ab}",
      "attempts": 1,
      "validated": 1,
      "entered_solver": 1,
      "failed_stage_counts": {},
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "h_absurdly_large": 1,
        "constraint_drift": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": 1693.8971889891395
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd}",
      "attempts": 1,
      "validated": 1,
      "entered_solver": 1,
      "failed_stage_counts": {},
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "h_absurdly_large": 1,
        "constraint_drift": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": 1699.8853293012148
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh}+φ1 · φ1 · R^{ab} · R_{ab}",
      "attempts": 1,
      "validated": 1,
      "entered_solver": 1,
      "failed_stage_counts": {},
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "h_absurdly_large": 1
      },
      "best_chi2": 1705.2566176844957
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R · R",
      "attempts": 1,
      "validated": 1,
      "entered_solver": 1,
      "failed_stage_counts": {},
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "h_absurdly_large": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": 1709.2958786255485
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+∇^{a}∇_{a}R",
      "attempts": 1,
      "validated": 1,
      "entered_solver": 1,
      "failed_stage_counts": {},
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "h_absurdly_large": 1,
        "constraint_drift": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": 1736.4074500477848
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R^{ab} · R^{d}_{a} · R_{bd}",
      "attempts": 1,
      "validated": 1,
      "entered_solver": 1,
      "failed_stage_counts": {},
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "h_absurdly_large": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": 1743.1583902138543
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+∇^{a}R · ∇_{a}R+∇^{a}φ1 · ∇^{b}φ1 · R_{ab}",
      "attempts": 1,
      "validated": 1,
      "entered_solver": 1,
      "failed_stage_counts": {},
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "h_absurdly_large": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": 1765.754508418696
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+∇^{a}∇_{a}R+∇^{c}R^{ab} · ∇_{b}R_{ac}+∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}+∇^{a}φ1 · ∇^{b}φ1 · R_{ab}",
      "attempts": 1,
      "validated": 1,
      "entered_solver": 1,
      "failed_stage_counts": {},
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "h_absurdly_large": 1
      },
      "best_chi2": 1776.1505636476381
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R · R+φ1 · R · R",
      "attempts": 1,
      "validated": 1,
      "entered_solver": 1,
      "failed_stage_counts": {},
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "h_absurdly_large": 1,
        "constraint_drift": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": 1803.3160906439384
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+∇^{c}R^{ab} · ∇_{b}R_{ac}+∇^{a}∇_{a}φ1",
      "attempts": 1,
      "validated": 1,
      "entered_solver": 1,
      "failed_stage_counts": {},
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "h_absurdly_large": 1,
        "constraint_drift": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": 1844.468086628849
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+φ1 · φ1 · R · R+∇^{a}φ1 · ∇^{b}φ1 · R_{ab}",
      "attempts": 1,
      "validated": 1,
      "entered_solver": 1,
      "failed_stage_counts": {},
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "h_absurdly_large": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": 1921.2519845841928
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}+φ1 · R^{ab} · R_{ab}+φ1 · ∇^{a}∇^{b}φ1 · R_{ab}+∇^{a}φ1 · ∇^{b}φ1 · R_{ab}",
      "attempts": 1,
      "validated": 1,
      "entered_solver": 1,
      "failed_stage_counts": {},
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "h_absurdly_large": 1
      },
      "best_chi2": 1941.1404074636632
    },
    {
      "family_key": "scalar=phi2_only|potential={'phi1': None, 'phi2': 'axion'}|operators=R+φ2 · R^{ab} · R_{ab}+∇^{a}∇_{a}φ2 · R+φ2 · φ2 · φ2 · φ2 · R+φ2 · φ2 · R^{ab} · R_{ab}+φ2 · φ2 · R^{bcd}_{a} · R^{a}_{bcd}+∇^{a}φ2 · ∇_{a}φ2 · R+∇^{a}∇_{a}φ2",
      "attempts": 1,
      "validated": 1,
      "entered_solver": 1,
      "failed_stage_counts": {},
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "constraint_drift": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": 9431.93283437729
    },
    {
      "family_key": "scalar=phi2_only|potential={'phi1': None, 'phi2': 'axion'}|operators=R+φ2 · φ2 · φ2 · R+∇^{a}∇_{a}φ2",
      "attempts": 1,
      "validated": 1,
      "entered_solver": 1,
      "failed_stage_counts": {},
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "constraint_drift": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": 9434.007984426724
    },
    {
      "family_key": "scalar=phi2_only|potential={'phi1': None, 'phi2': 'axion'}|operators=R+∇^{a}∇_{a}R+φ2 · ∇^{a}∇_{a}R+φ2 · φ2 · R^{ab} · R_{ab}",
      "attempts": 1,
      "validated": 0,
      "entered_solver": 1,
      "failed_stage_counts": {
        "Solver": 1
      },
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": null
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R · R^{ab} · R_{ab}+R^{b}_{a} · R^{cd} · R^{a}_{cbd}+φ1 · φ1 · φ1 · φ1+φ1 · ∇^{a}φ1 · ∇_{a}φ1",
      "attempts": 1,
      "validated": 0,
      "entered_solver": 1,
      "failed_stage_counts": {
        "Solver": 1
      },
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": null
    },
    {
      "family_key": "scalar=phi2_only|potential={'phi1': None, 'phi2': 'quadratic'}|operators=R+R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh}+φ2 · R^{bcd}_{a} · R^{a}_{bcd}",
      "attempts": 1,
      "validated": 0,
      "entered_solver": 1,
      "failed_stage_counts": {
        "Solver": 1
      },
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": null
    },
    {
      "family_key": "scalar=phi2_only|potential={'phi1': None, 'phi2': 'quadratic'}|operators=R+φ2 · φ2 · φ2 · φ2+∇^{a}φ2 · ∇_{a}φ2",
      "attempts": 1,
      "validated": 0,
      "entered_solver": 1,
      "failed_stage_counts": {
        "Solver": 1
      },
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": null
    },
    {
      "family_key": "scalar=none|potential={'phi1': None, 'phi2': None}|operators=R",
      "attempts": 1,
      "validated": 0,
      "entered_solver": 1,
      "failed_stage_counts": {
        "Solver": 1
      },
      "failure_tag_counts": {
        "no_scalar_constraint": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": null
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R^{ab} · R^{d}_{a} · R_{bd}+∇^{c}R^{ab} · ∇_{b}R_{ac}+∇^{c}R^{ab} · ∇_{c}R_{ab}+∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}+φ1 · φ1 · R+φ1 · R^{ab} · R_{ab}+φ1 · φ1 · R · R",
      "attempts": 1,
      "validated": 0,
      "entered_solver": 1,
      "failed_stage_counts": {
        "Solver": 1
      },
      "failure_tag_counts": {
        "constraint_drift": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": null
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf}+φ1 · φ1 · R^{ab} · R_{ab}+∇^{a}φ1 · ∇^{b}φ1 · R_{ab}+φ1 · φ1 · φ1 · φ1 · φ1+φ1 · ∇^{a}φ1 · ∇_{a}φ1",
      "attempts": 1,
      "validated": 0,
      "entered_solver": 1,
      "failed_stage_counts": {
        "Solver": 1
      },
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": null
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R^{b}_{a} · R^{cd} · R^{a}_{cbd}+∇^{a}∇_{a}R · R^{c}_{c}+φ1 · ∇^{a}∇_{a}R+φ1 · φ1 · φ1 · φ1 · R",
      "attempts": 1,
      "validated": 0,
      "entered_solver": 1,
      "failed_stage_counts": {
        "Solver": 1
      },
      "failure_tag_counts": {
        "constraint_drift": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": null
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R^{b}_{a} · R^{cd} · R^{a}_{cbd}+∇^{c}R^{ab} · ∇_{b}R_{ac}+φ1 · φ1 · R+φ1 · φ1",
      "attempts": 1,
      "validated": 0,
      "entered_solver": 1,
      "failed_stage_counts": {
        "Solver": 1
      },
      "failure_tag_counts": {
        "constraint_drift": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": null
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R^{b}_{a} · R^{cd} · R^{a}_{cbd}+φ1 · R",
      "attempts": 1,
      "validated": 0,
      "entered_solver": 1,
      "failed_stage_counts": {
        "Solver": 1
      },
      "failure_tag_counts": {
        "constraint_drift": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": null
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+φ1 · R",
      "attempts": 1,
      "validated": 0,
      "entered_solver": 1,
      "failed_stage_counts": {
        "Solver": 1
      },
      "failure_tag_counts": {
        "constraint_drift": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": null
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh}+R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{fdh}+R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf}+∇^{a}∇^{b}R · R_{ab}+∇^{c}R^{ab} · ∇_{b}R_{ac}+φ1 · R · R+φ1 · φ1 · ∇^{a}∇_{a}φ1",
      "attempts": 1,
      "validated": 0,
      "entered_solver": 1,
      "failed_stage_counts": {
        "Solver": 1
      },
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "constraint_drift": 1,
        "no_accepted_samples": 1,
        "integration_failure": 1
      },
      "best_chi2": null
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+φ1 · φ1 · R+φ1 · φ1 · φ1 · R",
      "attempts": 1,
      "validated": 0,
      "entered_solver": 1,
      "failed_stage_counts": {
        "Solver": 1
      },
      "failure_tag_counts": {
        "constraint_drift": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": null
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh}+∇^{a}R · ∇_{a}R+∇^{c}R^{ab} · ∇_{b}R_{ac}+φ1 · R^{ab} · R_{ab}+∇^{a}φ1 · ∇^{b}φ1 · R_{ab}+φ1 · φ1 · φ1 · φ1 · φ1+φ1 · φ1 · φ1 · φ1 · φ1 · φ1",
      "attempts": 1,
      "validated": 0,
      "entered_solver": 1,
      "failed_stage_counts": {
        "Solver": 1
      },
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": null
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}+φ1 · R^{ab} · R_{ab}+φ1 · R^{bcd}_{a} · R^{a}_{bcd}+φ1 · ∇^{a}∇_{a}R",
      "attempts": 1,
      "validated": 0,
      "entered_solver": 1,
      "failed_stage_counts": {
        "Solver": 1
      },
      "failure_tag_counts": {
        "constraint_drift": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": null
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}+φ1 · R+φ1 · ∇^{a}∇_{a}R+∇^{a}φ1 · ∇^{b}φ1 · R_{ab}",
      "attempts": 1,
      "validated": 0,
      "entered_solver": 1,
      "failed_stage_counts": {
        "Solver": 1
      },
      "failure_tag_counts": {
        "constraint_drift": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": null
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+φ1 · φ1 · R",
      "attempts": 1,
      "validated": 0,
      "entered_solver": 1,
      "failed_stage_counts": {
        "Solver": 1
      },
      "failure_tag_counts": {
        "constraint_drift": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": null
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R · R · R+φ1 · φ1 · R+∇^{a}∇_{a}φ1 · R+φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd}+∇^{a}φ1 · ∇^{b}φ1 · R_{ab}",
      "attempts": 1,
      "validated": 0,
      "entered_solver": 1,
      "failed_stage_counts": {
        "Solver": 1
      },
      "failure_tag_counts": {
        "constraint_drift": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": null
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+φ1 · R · R+∇^{a}φ1 · ∇^{b}φ1 · R_{ab}+φ1 · φ1 · φ1+∇^{a}φ1 · ∇_{a}φ1+φ1 · φ1 · φ1 · ∇^{a}∇_{a}φ1",
      "attempts": 1,
      "validated": 0,
      "entered_solver": 1,
      "failed_stage_counts": {
        "Solver": 1
      },
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": null
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+φ1 · φ1 · φ1 · R",
      "attempts": 1,
      "validated": 0,
      "entered_solver": 1,
      "failed_stage_counts": {
        "Solver": 1
      },
      "failure_tag_counts": {
        "constraint_drift": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": null
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'axion', 'phi2': None}|operators=R+φ1 · R",
      "attempts": 1,
      "validated": 0,
      "entered_solver": 1,
      "failed_stage_counts": {
        "Solver": 1
      },
      "failure_tag_counts": {
        "constraint_drift": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": null
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+φ1 · φ1 · φ1 · φ1 · R",
      "attempts": 1,
      "validated": 0,
      "entered_solver": 1,
      "failed_stage_counts": {
        "Solver": 1
      },
      "failure_tag_counts": {
        "constraint_drift": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": null
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf}+φ1 · ∇^{a}∇_{a}R+∇^{a}φ1 · ∇^{b}φ1 · R_{ab}+φ1 · φ1 · φ1 · φ1+φ1 · ∇^{a}φ1 · ∇_{a}φ1",
      "attempts": 1,
      "validated": 0,
      "entered_solver": 1,
      "failed_stage_counts": {
        "Solver": 1
      },
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": null
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{fdh}+φ1 · φ1 · R",
      "attempts": 1,
      "validated": 0,
      "entered_solver": 1,
      "failed_stage_counts": {
        "Solver": 1
      },
      "failure_tag_counts": {
        "constraint_drift": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": null
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'axion', 'phi2': None}|operators=R+R · R+∇^{a}∇_{a}R+φ1 · φ1 · φ1 · R+φ1 · R · R+∇^{a}φ1 · ∇^{b}φ1 · R_{ab}+φ1 · φ1 · ∇^{a}∇_{a}φ1",
      "attempts": 1,
      "validated": 0,
      "entered_solver": 1,
      "failed_stage_counts": {
        "Solver": 1
      },
      "failure_tag_counts": {
        "constraint_drift": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": null
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf}+φ1 · φ1 · R+φ1 · φ1 · φ1 · R",
      "attempts": 1,
      "validated": 0,
      "entered_solver": 1,
      "failed_stage_counts": {
        "Solver": 1
      },
      "failure_tag_counts": {
        "constraint_drift": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": null
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}+φ1 · φ1 · R^{ab} · R_{ab}+φ1 · ∇^{a}φ1 · ∇_{a}R+∇^{a}φ1 · ∇^{b}φ1 · R_{ab}+φ1 · φ1+φ1 · φ1 · ∇^{a}φ1 · ∇_{a}φ1",
      "attempts": 1,
      "validated": 0,
      "entered_solver": 1,
      "failed_stage_counts": {
        "Solver": 1
      },
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "h_absurdly_large": 1,
        "constraint_drift": 1,
        "no_accepted_samples": 1,
        "integration_failure": 1
      },
      "best_chi2": null
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{fdh}+φ1 · R+∇^{a}φ1 · ∇_{a}R+∇^{a}φ1 · ∇^{b}φ1 · R_{ab}+φ1 · ∇^{a}φ1 · ∇_{a}φ1",
      "attempts": 1,
      "validated": 0,
      "entered_solver": 1,
      "failed_stage_counts": {
        "Solver": 1
      },
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "h_absurdly_large": 1,
        "constraint_drift": 1,
        "no_accepted_samples": 1,
        "integration_failure": 1
      },
      "best_chi2": null
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R^{ab} · R^{d}_{a} · R_{bd}+R^{b}_{a} · R^{cd} · R^{a}_{cbd}+φ1 · φ1 · φ1 · R+φ1 · φ1 · R^{ab} · R_{ab}+φ1 · ∇^{a}∇^{b}φ1 · R_{ab}+φ1 · φ1+φ1 · φ1 · φ1",
      "attempts": 1,
      "validated": 0,
      "entered_solver": 1,
      "failed_stage_counts": {
        "Solver": 1
      },
      "failure_tag_counts": {
        "constraint_drift": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": null
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+∇^{a}∇_{a}R · R^{c}_{c}+∇^{c}R^{ab} · ∇_{b}R_{ac}+∇^{c}R^{ab} · ∇_{c}R_{ab}+∇^{a}φ1 · ∇^{b}φ1 · R_{ab}+∇^{a}∇_{a}φ1+φ1 · φ1 · ∇^{a}∇_{a}φ1+φ1 · φ1 · ∇^{a}φ1 · ∇_{a}φ1",
      "attempts": 1,
      "validated": 0,
      "entered_solver": 1,
      "failed_stage_counts": {
        "Solver": 1
      },
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "constraint_drift": 1,
        "no_accepted_samples": 1,
        "integration_failure": 1
      },
      "best_chi2": null
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+φ1 · ∇^{a}∇_{a}R+φ1 · φ1 · R^{ab} · R_{ab}+φ1 · φ1 · φ1 · φ1+φ1 · ∇^{a}∇_{a}φ1",
      "attempts": 1,
      "validated": 0,
      "entered_solver": 1,
      "failed_stage_counts": {
        "Solver": 1
      },
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": null
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R^{b}_{a} · R^{cd} · R^{a}_{cbd}+φ1 · φ1 · R+φ1 · φ1 · φ1 · R+φ1 · ∇^{a}φ1 · ∇_{a}R+∇^{a}φ1 · ∇^{b}φ1 · R_{ab}+φ1 · φ1 · ∇^{a}φ1 · ∇_{a}φ1",
      "attempts": 1,
      "validated": 0,
      "entered_solver": 1,
      "failed_stage_counts": {
        "Solver": 1
      },
      "failure_tag_counts": {
        "constraint_drift": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": null
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R^{ab} · R^{d}_{a} · R_{bd}+φ1 · R^{ab} · R_{ab}+φ1 · φ1 · φ1 · φ1",
      "attempts": 1,
      "validated": 0,
      "entered_solver": 1,
      "failed_stage_counts": {
        "Solver": 1
      },
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": null
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'axion', 'phi2': None}|operators=R+φ1 · φ1 · R",
      "attempts": 1,
      "validated": 0,
      "entered_solver": 1,
      "failed_stage_counts": {
        "Solver": 1
      },
      "failure_tag_counts": {
        "constraint_drift": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": null
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+∇^{a}∇_{a}R+φ1 · R",
      "attempts": 1,
      "validated": 0,
      "entered_solver": 1,
      "failed_stage_counts": {
        "Solver": 1
      },
      "failure_tag_counts": {
        "constraint_drift": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": null
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+∇^{a}∇_{a}R+∇^{c}R^{ab} · ∇_{b}R_{ac}+φ1 · R+φ1 · ∇^{a}∇_{a}φ1 · R+∇^{a}φ1 · ∇^{b}φ1 · R_{ab}",
      "attempts": 1,
      "validated": 0,
      "entered_solver": 1,
      "failed_stage_counts": {
        "Solver": 1
      },
      "failure_tag_counts": {
        "constraint_drift": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": null
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+φ1 · R^{ab} · R_{ab}+φ1 · φ1 · R^{ab} · R_{ab}+φ1 · φ1 · φ1 · φ1+∇^{a}φ1 · ∇_{a}φ1",
      "attempts": 1,
      "validated": 0,
      "entered_solver": 1,
      "failed_stage_counts": {
        "Solver": 1
      },
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": null
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+φ1 · ∇^{a}∇_{a}R+∇^{a}φ1 · ∇_{a}φ1 · R+∇^{a}φ1 · ∇^{b}φ1 · R_{ab}+φ1 · φ1 · φ1 · φ1+φ1 · φ1 · ∇^{a}∇_{a}φ1",
      "attempts": 1,
      "validated": 0,
      "entered_solver": 1,
      "failed_stage_counts": {
        "Solver": 1
      },
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": null
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R · R+φ1 · φ1 · R^{ab} · R_{ab}+∇^{a}φ1 · ∇^{b}φ1 · R_{ab}+φ1 · ∇^{a}φ1 · ∇_{a}φ1",
      "attempts": 1,
      "validated": 0,
      "entered_solver": 1,
      "failed_stage_counts": {
        "Solver": 1
      },
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "constraint_drift": 1,
        "no_accepted_samples": 1,
        "integration_failure": 1
      },
      "best_chi2": null
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+φ1 · φ1 · φ1 · φ1 · R+φ1 · φ1 · φ1 · φ1 · φ1 · φ1",
      "attempts": 1,
      "validated": 0,
      "entered_solver": 1,
      "failed_stage_counts": {
        "Solver": 1
      },
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "constraint_drift": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": null
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R^{ab} · R_{ab}+φ1 · R+φ1 · φ1 · φ1 · φ1 · φ1",
      "attempts": 1,
      "validated": 0,
      "entered_solver": 1,
      "failed_stage_counts": {
        "Solver": 1
      },
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": null
    },
    {
      "family_key": "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+φ1 · φ1 · φ1 · φ1",
      "attempts": 1,
      "validated": 0,
      "entered_solver": 1,
      "failed_stage_counts": {
        "Solver": 1
      },
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": null
    }
  ],
  "by_coarse_family": [
    {
      "coarse_family_key": "scalar=phi1_only|phi1_potential=quadratic|phi2_potential=None|operator_bucket=R_anchor+derivative+high_curvature+scalar_curvature",
      "attempts": 37,
      "validated": 16,
      "entered_solver": 37,
      "failed_stage_counts": {
        "Solver": 21
      },
      "failure_tag_counts": {
        "no_accepted_samples": 32,
        "q_initial_root_failure": 28,
        "constraint_drift": 19,
        "h_absurdly_large": 18,
        "integration_failure": 5
      },
      "best_chi2": 1640.9593449034116
    },
    {
      "coarse_family_key": "scalar=phi1_only|phi1_potential=quadratic|phi2_potential=None|operator_bucket=R_anchor",
      "attempts": 12,
      "validated": 11,
      "entered_solver": 12,
      "failed_stage_counts": {
        "Solver": 1
      },
      "failure_tag_counts": {
        "q_initial_root_failure": 12,
        "h_absurdly_large": 11,
        "no_accepted_samples": 10,
        "constraint_drift": 5
      },
      "best_chi2": 1638.0428393360799
    },
    {
      "coarse_family_key": "scalar=phi1_only|phi1_potential=quadratic|phi2_potential=None|operator_bucket=R_anchor+high_curvature+scalar_curvature",
      "attempts": 11,
      "validated": 9,
      "entered_solver": 11,
      "failed_stage_counts": {
        "Solver": 2
      },
      "failure_tag_counts": {
        "q_initial_root_failure": 11,
        "h_absurdly_large": 9,
        "no_accepted_samples": 8,
        "constraint_drift": 4
      },
      "best_chi2": 1643.8926784757662
    },
    {
      "coarse_family_key": "scalar=phi1_only|phi1_potential=quadratic|phi2_potential=None|operator_bucket=R_anchor+scalar_curvature",
      "attempts": 11,
      "validated": 2,
      "entered_solver": 11,
      "failed_stage_counts": {
        "Solver": 9
      },
      "failure_tag_counts": {
        "constraint_drift": 11,
        "no_accepted_samples": 11,
        "q_initial_root_failure": 3,
        "h_absurdly_large": 2
      },
      "best_chi2": 1659.2520646320763
    },
    {
      "coarse_family_key": "scalar=phi1_only|phi1_potential=quadratic|phi2_potential=None|operator_bucket=R_anchor+derivative+high_curvature",
      "attempts": 6,
      "validated": 5,
      "entered_solver": 6,
      "failed_stage_counts": {
        "Solver": 1
      },
      "failure_tag_counts": {
        "q_initial_root_failure": 6,
        "no_accepted_samples": 5,
        "h_absurdly_large": 5,
        "constraint_drift": 4
      },
      "best_chi2": 1645.4406385861453
    },
    {
      "coarse_family_key": "scalar=phi1_only|phi1_potential=quadratic|phi2_potential=None|operator_bucket=R_anchor+high_curvature",
      "attempts": 6,
      "validated": 6,
      "entered_solver": 6,
      "failed_stage_counts": {},
      "failure_tag_counts": {
        "q_initial_root_failure": 6,
        "h_absurdly_large": 6,
        "no_accepted_samples": 5,
        "constraint_drift": 2
      },
      "best_chi2": 1647.0380923153227
    },
    {
      "coarse_family_key": "scalar=phi1_only|phi1_potential=quadratic|phi2_potential=None|operator_bucket=R_anchor+derivative+scalar_curvature",
      "attempts": 4,
      "validated": 3,
      "entered_solver": 4,
      "failed_stage_counts": {
        "Solver": 1
      },
      "failure_tag_counts": {
        "no_accepted_samples": 4,
        "q_initial_root_failure": 3,
        "h_absurdly_large": 3,
        "constraint_drift": 3
      },
      "best_chi2": 1639.0299359874105
    },
    {
      "coarse_family_key": "scalar=phi1_only|phi1_potential=quadratic|phi2_potential=None|operator_bucket=R_anchor+derivative",
      "attempts": 4,
      "validated": 4,
      "entered_solver": 4,
      "failed_stage_counts": {},
      "failure_tag_counts": {
        "q_initial_root_failure": 4,
        "h_absurdly_large": 4,
        "constraint_drift": 2,
        "no_accepted_samples": 2
      },
      "best_chi2": 1644.8034172595212
    },
    {
      "coarse_family_key": "scalar=phi1_only|phi1_potential=axion|phi2_potential=None|operator_bucket=R_anchor",
      "attempts": 2,
      "validated": 2,
      "entered_solver": 2,
      "failed_stage_counts": {},
      "failure_tag_counts": {
        "q_initial_root_failure": 2,
        "h_absurdly_large": 2,
        "no_accepted_samples": 1
      },
      "best_chi2": 1656.395923088284
    },
    {
      "coarse_family_key": "scalar=phi2_only|phi1_potential=None|phi2_potential=axion|operator_bucket=R_anchor+derivative+high_curvature+scalar_curvature",
      "attempts": 2,
      "validated": 1,
      "entered_solver": 2,
      "failed_stage_counts": {
        "Solver": 1
      },
      "failure_tag_counts": {
        "q_initial_root_failure": 2,
        "no_accepted_samples": 2,
        "constraint_drift": 1
      },
      "best_chi2": 9431.93283437729
    },
    {
      "coarse_family_key": "scalar=phi1_only|phi1_potential=axion|phi2_potential=None|operator_bucket=R_anchor+scalar_curvature",
      "attempts": 2,
      "validated": 0,
      "entered_solver": 2,
      "failed_stage_counts": {
        "Solver": 2
      },
      "failure_tag_counts": {
        "constraint_drift": 2,
        "no_accepted_samples": 2
      },
      "best_chi2": null
    },
    {
      "coarse_family_key": "scalar=phi1_only|phi1_potential=axion|phi2_potential=None|operator_bucket=R_anchor+derivative+scalar_curvature",
      "attempts": 1,
      "validated": 1,
      "entered_solver": 1,
      "failed_stage_counts": {},
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "h_absurdly_large": 1,
        "constraint_drift": 1
      },
      "best_chi2": 1647.3876439579699
    },
    {
      "coarse_family_key": "scalar=phi1_only|phi1_potential=axion|phi2_potential=None|operator_bucket=R_anchor+derivative",
      "attempts": 1,
      "validated": 1,
      "entered_solver": 1,
      "failed_stage_counts": {},
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "h_absurdly_large": 1,
        "constraint_drift": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": 1651.9561626509249
    },
    {
      "coarse_family_key": "scalar=phi2_only|phi1_potential=None|phi2_potential=axion|operator_bucket=R_anchor+derivative+scalar_curvature",
      "attempts": 1,
      "validated": 1,
      "entered_solver": 1,
      "failed_stage_counts": {},
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "constraint_drift": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": 9434.007984426724
    },
    {
      "coarse_family_key": "scalar=phi2_only|phi1_potential=None|phi2_potential=quadratic|operator_bucket=R_anchor+scalar_curvature",
      "attempts": 1,
      "validated": 0,
      "entered_solver": 1,
      "failed_stage_counts": {
        "Solver": 1
      },
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": null
    },
    {
      "coarse_family_key": "scalar=phi2_only|phi1_potential=None|phi2_potential=quadratic|operator_bucket=R_anchor+derivative",
      "attempts": 1,
      "validated": 0,
      "entered_solver": 1,
      "failed_stage_counts": {
        "Solver": 1
      },
      "failure_tag_counts": {
        "q_initial_root_failure": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": null
    },
    {
      "coarse_family_key": "scalar=none|phi1_potential=None|phi2_potential=None|operator_bucket=R_anchor",
      "attempts": 1,
      "validated": 0,
      "entered_solver": 1,
      "failed_stage_counts": {
        "Solver": 1
      },
      "failure_tag_counts": {
        "no_scalar_constraint": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": null
    },
    {
      "coarse_family_key": "scalar=phi1_only|phi1_potential=axion|phi2_potential=None|operator_bucket=R_anchor+derivative+high_curvature+scalar_curvature",
      "attempts": 1,
      "validated": 0,
      "entered_solver": 1,
      "failed_stage_counts": {
        "Solver": 1
      },
      "failure_tag_counts": {
        "constraint_drift": 1,
        "no_accepted_samples": 1
      },
      "best_chi2": null
    }
  ],
  "by_theory_track": {
    "eh_anchored": {
      "attempts": 104,
      "validated": 62,
      "accepted_rate": 0.5961538461538461,
      "best_chi2": 1638.0428393360799,
      "failure_tag_counts": {
        "no_accepted_samples": 88,
        "q_initial_root_failure": 82,
        "h_absurdly_large": 62,
        "constraint_drift": 57,
        "integration_failure": 5,
        "no_scalar_constraint": 1
      }
    }
  },
  "policy": {
    "record_count": 104,
    "global_mean_reward": 3.596566911459426,
    "by_feature": {
      "scalar_config": {
        "phi2_only": {
          "count": 5,
          "mean_reward": -3.4
        },
        "phi1_only": {
          "count": 98,
          "mean_reward": 4.020846518283472
        },
        "none": {
          "count": 1,
          "mean_reward": -3.0
        }
      },
      "theory_track": {
        "eh_anchored": {
          "count": 104,
          "mean_reward": 3.596566911459426
        }
      },
      "phi1_potential": {
        "None": {
          "count": 6,
          "mean_reward": -3.3333333333333335
        },
        "quadratic": {
          "count": 91,
          "mean_reward": 4.006557158729911
        },
        "axion": {
          "count": 7,
          "mean_reward": 4.206608192479773
        }
      },
      "phi2_potential": {
        "axion": {
          "count": 3,
          "mean_reward": -3.6666666666666665
        },
        "None": {
          "count": 99,
          "mean_reward": 3.949928876684649
        },
        "quadratic": {
          "count": 2,
          "mean_reward": -3.0
        }
      },
      "operator_count": {
        "3": {
          "count": 26,
          "mean_reward": 4.577370065838421
        },
        "4": {
          "count": 5,
          "mean_reward": -0.015393268451342479
        },
        "5": {
          "count": 13,
          "mean_reward": 1.4235296835449818
        },
        "8": {
          "count": 8,
          "mean_reward": -0.9765361353782338
        },
        "1": {
          "count": 13,
          "mean_reward": 7.941329062347567
        },
        "2": {
          "count": 28,
          "mean_reward": 6.031021951460555
        },
        "6": {
          "count": 8,
          "mean_reward": -1.961398229029345
        },
        "7": {
          "count": 3,
          "mean_reward": -4.0
        }
      },
      "has_R_anchor": {
        "True": {
          "count": 104,
          "mean_reward": 3.596566911459426
        }
      },
      "has_scalar": {
        "True": {
          "count": 103,
          "mean_reward": 3.660611250405634
        },
        "False": {
          "count": 1,
          "mean_reward": -3.0
        }
      },
      "has_phi1": {
        "False": {
          "count": 6,
          "mean_reward": -3.3333333333333335
        },
        "True": {
          "count": 98,
          "mean_reward": 4.020846518283472
        }
      },
      "has_phi2": {
        "True": {
          "count": 5,
          "mean_reward": -3.4
        },
        "False": {
          "count": 99,
          "mean_reward": 3.949928876684649
        }
      },
      "has_both_scalars": {
        "False": {
          "count": 104,
          "mean_reward": 3.596566911459426
        }
      },
      "is_no_scalar": {
        "False": {
          "count": 103,
          "mean_reward": 3.660611250405634
        },
        "True": {
          "count": 1,
          "mean_reward": -3.0
        }
      },
      "has_scalar_curvature": {
        "True": {
          "count": 103,
          "mean_reward": 3.660611250405634
        },
        "False": {
          "count": 1,
          "mean_reward": -3.0
        }
      },
      "has_derivative_operator": {
        "True": {
          "count": 58,
          "mean_reward": 2.8376104137297484
        },
        "False": {
          "count": 46,
          "mean_reward": 4.553512060770758
        }
      },
      "has_box_operator": {
        "True": {
          "count": 30,
          "mean_reward": 2.3525149641371357
        },
        "False": {
          "count": 74,
          "mean_reward": 4.100912295509002
        }
      },
      "has_high_curvature": {
        "False": {
          "count": 41,
          "mean_reward": 4.120971662312367
        },
        "True": {
          "count": 63,
          "mean_reward": 3.2552876291583055
        }
      },
      "has_pure_scalar_operator": {
        "True": {
          "count": 32,
          "mean_reward": -0.6753424548215698
        },
        "False": {
          "count": 72,
          "mean_reward": 5.495193296473201
        }
      }
    },
    "by_operator": {
      "R": {
        "count": 104,
        "mean_reward": 3.596566911459426
      },
      "φ2 · φ2 · φ2 · R": {
        "count": 1,
        "mean_reward": -4.0
      },
      "∇^{a}∇_{a}φ2": {
        "count": 2,
        "mean_reward": -4.0
      },
      "∇^{a}∇_{a}R": {
        "count": 11,
        "mean_reward": 4.395150008232464
      },
      "φ2 · ∇^{a}∇_{a}R": {
        "count": 1,
        "mean_reward": -3.0
      },
      "φ2 · φ2 · R^{ab} · R_{ab}": {
        "count": 2,
        "mean_reward": -3.5
      },
      "R · R^{ab} · R_{ab}": {
        "count": 2,
        "mean_reward": 2.160061043714736
      },
      "R^{b}_{a} · R^{cd} · R^{a}_{cbd}": {
        "count": 8,
        "mean_reward": 0.39439292432142337
      },
      "φ1 · φ1 · φ1 · φ1": {
        "count": 7,
        "mean_reward": -3.0
      },
      "φ1 · ∇^{a}φ1 · ∇_{a}φ1": {
        "count": 5,
        "mean_reward": -4.4
      },
      "φ2 · R^{ab} · R_{ab}": {
        "count": 1,
        "mean_reward": -4.0
      },
      "∇^{a}∇_{a}φ2 · R": {
        "count": 1,
        "mean_reward": -4.0
      },
      "φ2 · φ2 · φ2 · φ2 · R": {
        "count": 1,
        "mean_reward": -4.0
      },
      "φ2 · φ2 · R^{bcd}_{a} · R^{a}_{bcd}": {
        "count": 1,
        "mean_reward": -4.0
      },
      "∇^{a}φ2 · ∇_{a}φ2 · R": {
        "count": 1,
        "mean_reward": -4.0
      },
      "R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh}": {
        "count": 5,
        "mean_reward": 0.5738843297701752
      },
      "φ2 · R^{bcd}_{a} · R^{a}_{bcd}": {
        "count": 1,
        "mean_reward": -3.0
      },
      "φ2 · φ2 · φ2 · φ2": {
        "count": 1,
        "mean_reward": -3.0
      },
      "∇^{a}φ2 · ∇_{a}φ2": {
        "count": 1,
        "mean_reward": -3.0
      },
      "∇^{c}R^{ab} · ∇_{b}R_{ac}": {
        "count": 12,
        "mean_reward": 2.328586240693778
      },
      "φ1 · φ1 · R^{ab} · R_{ab}": {
        "count": 10,
        "mean_reward": 1.3034386846445873
      },
      "∇^{a}φ1 · ∇^{b}φ1 · R_{ab}": {
        "count": 26,
        "mean_reward": 1.7299703725097806
      },
      "R^{ab} · R^{d}_{a} · R_{bd}": {
        "count": 5,
        "mean_reward": 1.7918684112078012
      },
      "∇^{c}R^{ab} · ∇_{c}R_{ab}": {
        "count": 3,
        "mean_reward": 0.09446644200949746
      },
      "∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}": {
        "count": 6,
        "mean_reward": -0.8788182851855023
      },
      "φ1 · φ1 · R": {
        "count": 9,
        "mean_reward": -2.5
      },
      "φ1 · R^{ab} · R_{ab}": {
        "count": 10,
        "mean_reward": 2.5105068619728477
      },
      "φ1 · φ1 · R · R": {
        "count": 4,
        "mean_reward": 4.990200040606865
      },
      "R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf}": {
        "count": 4,
        "mean_reward": -3.625
      },
      "φ1 · φ1 · φ1 · φ1 · φ1": {
        "count": 3,
        "mean_reward": -3.0
      },
      "φ1 · ∇^{a}∇^{b}φ1 · R_{ab}": {
        "count": 2,
        "mean_reward": 0.6942979626816839
      },
      "∇^{a}∇_{a}R · R^{c}_{c}": {
        "count": 3,
        "mean_reward": -0.4114256362405679
      },
      "φ1 · ∇^{a}∇_{a}R": {
        "count": 9,
        "mean_reward": 1.274278559377721
      },
      "φ1 · φ1 · φ1 · φ1 · R": {
        "count": 3,
        "mean_reward": -3.1666666666666665
      },
      "R^{bcd}_{a} · R^{a}_{bcd}": {
        "count": 2,
        "mean_reward": 8.536805796427444
      },
      "φ1 · R · R": {
        "count": 6,
        "mean_reward": 1.7610517136301034
      },
      "∇^{a}φ1 · ∇_{a}R": {
        "count": 3,
        "mean_reward": 3.3712427583221323
      },
      "∇^{a}φ1 · ∇_{a}φ1": {
        "count": 5,
        "mean_reward": 4.495449209050409
      },
      "φ1 · φ1": {
        "count": 4,
        "mean_reward": -0.92279645805869
      },
      "φ1 · R": {
        "count": 8,
        "mean_reward": -3.125
      },
      "∇^{a}∇_{a}φ1": {
        "count": 2,
        "mean_reward": -0.7223404331442453
      },
      "R · R": {
        "count": 10,
        "mean_reward": 6.170586082455299
      },
      "φ1 · R^{bcd}_{a} · R^{a}_{bcd}": {
        "count": 3,
        "mean_reward": 5.1173017468042605
      },
      "φ1 · φ1 · ∇^{a}∇_{a}R": {
        "count": 1,
        "mean_reward": 8.921987825695833
      },
      "∇^{a}φ1 · ∇_{a}φ1 · R": {
        "count": 8,
        "mean_reward": 7.986561162258362
      },
      "φ1 · ∇^{a}∇_{a}φ1": {
        "count": 4,
        "mean_reward": 6.136915524745243
      },
      "φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd}": {
        "count": 2,
        "mean_reward": 2.302293413975703
      },
      "R_{ab} · R^{adef} · R^{b}_{def}": {
        "count": 3,
        "mean_reward": 9.54571690486713
      },
      "R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{fdh}": {
        "count": 3,
        "mean_reward": -5.166666666666667
      },
      "∇^{a}∇^{b}R · R_{ab}": {
        "count": 1,
        "mean_reward": -6.0
      },
      "φ1 · φ1 · ∇^{a}∇_{a}φ1": {
        "count": 4,
        "mean_reward": -4.375
      },
      "φ1 · φ1 · φ1 · R": {
        "count": 6,
        "mean_reward": -2.5
      },
      "∇^{a}R · ∇_{a}R": {
        "count": 3,
        "mean_reward": 3.222398709663402
      },
      "φ1 · φ1 · φ1 · φ1 · φ1 · φ1": {
        "count": 2,
        "mean_reward": -3.75
      },
      "R · R^{bcd}_{a} · R^{a}_{bcd}": {
        "count": 1,
        "mean_reward": 11.313157953109101
      },
      "R · R · R": {
        "count": 1,
        "mean_reward": -2.5
      },
      "∇^{a}∇_{a}φ1 · R": {
        "count": 2,
        "mean_reward": 4.461516828871644
      },
      "φ1 · φ1 · φ1": {
        "count": 2,
        "mean_reward": -2.75
      },
      "φ1 · φ1 · φ1 · ∇^{a}∇_{a}φ1": {
        "count": 1,
        "mean_reward": -3.0
      },
      "R^{ab} · R_{ab}": {
        "count": 5,
        "mean_reward": 6.330460011513896
      },
      "φ1 · ∇^{a}φ1 · ∇_{a}R": {
        "count": 2,
        "mean_reward": -4.75
      },
      "φ1 · φ1 · ∇^{a}φ1 · ∇_{a}φ1": {
        "count": 3,
        "mean_reward": -5.166666666666667
      },
      "φ1 · ∇^{a}∇_{a}φ1 · R": {
        "count": 2,
        "mean_reward": 4.461516828871644
      },
      "∇^{a}∇^{b}φ1 · R_{ab}": {
        "count": 1,
        "mean_reward": 9.0006409123732
      }
    },
    "by_family": {
      "scalar=phi2_only|potential={'phi1': None, 'phi2': 'axion'}|operators=R+φ2 · φ2 · φ2 · R+∇^{a}∇_{a}φ2": {
        "count": 1,
        "mean_reward": -4.0
      },
      "scalar=phi2_only|potential={'phi1': None, 'phi2': 'axion'}|operators=R+∇^{a}∇_{a}R+φ2 · ∇^{a}∇_{a}R+φ2 · φ2 · R^{ab} · R_{ab}": {
        "count": 1,
        "mean_reward": -3.0
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R · R^{ab} · R_{ab}+R^{b}_{a} · R^{cd} · R^{a}_{cbd}+φ1 · φ1 · φ1 · φ1+φ1 · ∇^{a}φ1 · ∇_{a}φ1": {
        "count": 1,
        "mean_reward": -3.0
      },
      "scalar=phi2_only|potential={'phi1': None, 'phi2': 'axion'}|operators=R+φ2 · R^{ab} · R_{ab}+∇^{a}∇_{a}φ2 · R+φ2 · φ2 · φ2 · φ2 · R+φ2 · φ2 · R^{ab} · R_{ab}+φ2 · φ2 · R^{bcd}_{a} · R^{a}_{bcd}+∇^{a}φ2 · ∇_{a}φ2 · R+∇^{a}∇_{a}φ2": {
        "count": 1,
        "mean_reward": -4.0
      },
      "scalar=phi2_only|potential={'phi1': None, 'phi2': 'quadratic'}|operators=R+R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh}+φ2 · R^{bcd}_{a} · R^{a}_{bcd}": {
        "count": 1,
        "mean_reward": -3.0
      },
      "scalar=phi2_only|potential={'phi1': None, 'phi2': 'quadratic'}|operators=R+φ2 · φ2 · φ2 · φ2+∇^{a}φ2 · ∇_{a}φ2": {
        "count": 1,
        "mean_reward": -3.0
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R^{b}_{a} · R^{cd} · R^{a}_{cbd}+∇^{c}R^{ab} · ∇_{b}R_{ac}+φ1 · φ1 · R^{ab} · R_{ab}+∇^{a}φ1 · ∇^{b}φ1 · R_{ab}": {
        "count": 1,
        "mean_reward": 11.40907718002919
      },
      "scalar=none|potential={'phi1': None, 'phi2': None}|operators=R": {
        "count": 1,
        "mean_reward": -3.0
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh}+φ1 · φ1 · R^{ab} · R_{ab}": {
        "count": 1,
        "mean_reward": 5.947433823155043
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R^{ab} · R^{d}_{a} · R_{bd}+∇^{c}R^{ab} · ∇_{b}R_{ac}+∇^{c}R^{ab} · ∇_{c}R_{ab}+∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}+φ1 · φ1 · R+φ1 · R^{ab} · R_{ab}+φ1 · φ1 · R · R": {
        "count": 1,
        "mean_reward": -2.5
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+∇^{a}∇_{a}R+∇^{c}R^{ab} · ∇_{b}R_{ac}": {
        "count": 1,
        "mean_reward": 8.867308365167263
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+φ1 · φ1 · R^{ab} · R_{ab}": {
        "count": 1,
        "mean_reward": 11.372961736060484
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R": {
        "count": 10,
        "mean_reward": 8.963580761486623
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf}+φ1 · φ1 · R^{ab} · R_{ab}+∇^{a}φ1 · ∇^{b}φ1 · R_{ab}+φ1 · φ1 · φ1 · φ1 · φ1+φ1 · ∇^{a}φ1 · ∇_{a}φ1": {
        "count": 1,
        "mean_reward": -3.0
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}+φ1 · R^{ab} · R_{ab}+φ1 · ∇^{a}∇^{b}φ1 · R_{ab}+∇^{a}φ1 · ∇^{b}φ1 · R_{ab}": {
        "count": 1,
        "mean_reward": 3.8885959253633677
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R^{b}_{a} · R^{cd} · R^{a}_{cbd}+∇^{a}∇_{a}R · R^{c}_{c}+φ1 · ∇^{a}∇_{a}R+φ1 · φ1 · φ1 · φ1 · R": {
        "count": 1,
        "mean_reward": -2.5
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R^{bcd}_{a} · R^{a}_{bcd}+φ1 · R · R": {
        "count": 1,
        "mean_reward": 8.764797425089647
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+∇^{c}R^{ab} · ∇_{b}R_{ac}": {
        "count": 1,
        "mean_reward": 11.350848020197924
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+∇^{a}φ1 · ∇_{a}R+φ1 · φ1 · R^{ab} · R_{ab}": {
        "count": 1,
        "mean_reward": 8.804914107201157
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+φ1 · ∇^{a}∇_{a}R+∇^{a}φ1 · ∇_{a}φ1": {
        "count": 1,
        "mean_reward": 8.117263380740114
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R^{b}_{a} · R^{cd} · R^{a}_{cbd}+∇^{c}R^{ab} · ∇_{b}R_{ac}+φ1 · φ1 · R+φ1 · φ1": {
        "count": 1,
        "mean_reward": -2.5
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R^{b}_{a} · R^{cd} · R^{a}_{cbd}+φ1 · R": {
        "count": 1,
        "mean_reward": -2.5
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+∇^{a}∇_{a}R": {
        "count": 1,
        "mean_reward": 5.935925499522152
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+∇^{c}R^{ab} · ∇_{b}R_{ac}+∇^{a}∇_{a}φ1": {
        "count": 1,
        "mean_reward": 4.555319133711509
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+φ1 · ∇^{a}∇_{a}R": {
        "count": 1,
        "mean_reward": 11.542429485894136
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R · R+R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh}+∇^{c}R^{ab} · ∇_{b}R_{ac}+φ1 · R^{bcd}_{a} · R^{a}_{bcd}+φ1 · φ1 · ∇^{a}∇_{a}R+∇^{a}φ1 · ∇_{a}φ1 · R+φ1 · ∇^{a}∇_{a}φ1": {
        "count": 1,
        "mean_reward": 8.921987825695833
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd}": {
        "count": 1,
        "mean_reward": 7.104586827951406
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+φ1 · R": {
        "count": 1,
        "mean_reward": -2.5
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+∇^{a}φ1 · ∇_{a}φ1 · R": {
        "count": 1,
        "mean_reward": 11.378662803482495
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R^{b}_{a} · R^{cd} · R^{a}_{cbd}": {
        "count": 1,
        "mean_reward": 7.246066214542197
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R · R+∇^{a}φ1 · ∇^{b}φ1 · R_{ab}": {
        "count": 1,
        "mean_reward": 11.414866501379834
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+∇^{a}∇_{a}R+∇^{a}φ1 · ∇_{a}φ1": {
        "count": 1,
        "mean_reward": 11.438229170548924
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R_{ab} · R^{adef} · R^{b}_{def}+φ1 · R^{ab} · R_{ab}+∇^{a}φ1 · ∇_{a}φ1 · R+∇^{a}φ1 · ∇^{b}φ1 · R_{ab}": {
        "count": 1,
        "mean_reward": 11.478792458991036
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh}+R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{fdh}+R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf}+∇^{a}∇^{b}R · R_{ab}+∇^{c}R^{ab} · ∇_{b}R_{ac}+φ1 · R · R+φ1 · φ1 · ∇^{a}∇_{a}φ1": {
        "count": 1,
        "mean_reward": -6.0
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+φ1 · φ1 · R+φ1 · φ1 · φ1 · R": {
        "count": 1,
        "mean_reward": -2.5
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh}+∇^{a}R · ∇_{a}R+∇^{c}R^{ab} · ∇_{b}R_{ac}+φ1 · R^{ab} · R_{ab}+∇^{a}φ1 · ∇^{b}φ1 · R_{ab}+φ1 · φ1 · φ1 · φ1 · φ1+φ1 · φ1 · φ1 · φ1 · φ1 · φ1": {
        "count": 1,
        "mean_reward": -3.0
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+φ1 · ∇^{a}∇_{a}φ1": {
        "count": 1,
        "mean_reward": 11.35995118200684
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}+φ1 · R^{ab} · R_{ab}+φ1 · R^{bcd}_{a} · R^{a}_{bcd}+φ1 · ∇^{a}∇_{a}R": {
        "count": 1,
        "mean_reward": -2.5
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R · R^{bcd}_{a} · R^{a}_{bcd}": {
        "count": 1,
        "mean_reward": 11.313157953109101
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}+φ1 · R+φ1 · ∇^{a}∇_{a}R+∇^{a}φ1 · ∇^{b}φ1 · R_{ab}": {
        "count": 1,
        "mean_reward": -2.5
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R · R^{ab} · R_{ab}": {
        "count": 1,
        "mean_reward": 7.320122087429472
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R_{ab} · R^{adef} · R^{b}_{def}": {
        "count": 1,
        "mean_reward": 8.374958929581862
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+∇^{a}φ1 · ∇^{b}φ1 · R_{ab}": {
        "count": 1,
        "mean_reward": 11.351967071116178
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+∇^{a}R · ∇_{a}R+∇^{a}φ1 · ∇^{b}φ1 · R_{ab}": {
        "count": 1,
        "mean_reward": 5.342454915813039
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R_{ab} · R^{adef} · R^{b}_{def}+∇^{c}R^{ab} · ∇_{c}R_{ab}": {
        "count": 1,
        "mean_reward": 8.783399326028492
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+φ1 · φ1 · R": {
        "count": 1,
        "mean_reward": -2.5
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R · R · R+φ1 · φ1 · R+∇^{a}∇_{a}φ1 · R+φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd}+∇^{a}φ1 · ∇^{b}φ1 · R_{ab}": {
        "count": 1,
        "mean_reward": -2.5
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+φ1 · R^{ab} · R_{ab}": {
        "count": 1,
        "mean_reward": 7.857519870877258
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+φ1 · R · R+∇^{a}φ1 · ∇^{b}φ1 · R_{ab}+φ1 · φ1 · φ1+∇^{a}φ1 · ∇_{a}φ1+φ1 · φ1 · φ1 · ∇^{a}∇_{a}φ1": {
        "count": 1,
        "mean_reward": -3.0
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+φ1 · φ1 · φ1 · R": {
        "count": 1,
        "mean_reward": -2.5
      },
      "scalar=phi1_only|potential={'phi1': 'axion', 'phi2': None}|operators=R+φ1 · R": {
        "count": 1,
        "mean_reward": -2.5
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+φ1 · φ1 · φ1 · φ1 · R": {
        "count": 1,
        "mean_reward": -2.5
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf}+φ1 · ∇^{a}∇_{a}R+∇^{a}φ1 · ∇^{b}φ1 · R_{ab}+φ1 · φ1 · φ1 · φ1+φ1 · ∇^{a}φ1 · ∇_{a}φ1": {
        "count": 1,
        "mean_reward": -3.0
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R · R+R^{ab} · R_{ab}+∇^{a}∇_{a}R+∇^{a}∇_{a}R · R^{c}_{c}+φ1 · R^{ab} · R_{ab}+∇^{a}φ1 · ∇_{a}φ1 · R+φ1 · ∇^{a}∇_{a}φ1": {
        "count": 1,
        "mean_reward": 7.265723091278296
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{fdh}+φ1 · φ1 · R": {
        "count": 1,
        "mean_reward": -2.5
      },
      "scalar=phi1_only|potential={'phi1': 'axion', 'phi2': None}|operators=R+R · R+∇^{a}∇_{a}R+φ1 · φ1 · φ1 · R+φ1 · R · R+∇^{a}φ1 · ∇^{b}φ1 · R_{ab}+φ1 · φ1 · ∇^{a}∇_{a}φ1": {
        "count": 1,
        "mean_reward": -2.5
      },
      "scalar=phi1_only|potential={'phi1': 'axion', 'phi2': None}|operators=R+∇^{a}φ1 · ∇_{a}φ1": {
        "count": 1,
        "mean_reward": 8.921753493963006
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf}+φ1 · φ1 · R+φ1 · φ1 · φ1 · R": {
        "count": 1,
        "mean_reward": -2.5
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R · R+∇^{a}∇_{a}R+R^{ab} · R^{d}_{a} · R_{bd}+∇^{a}φ1 · ∇^{b}φ1 · R_{ab}": {
        "count": 1,
        "mean_reward": 11.390925958177549
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R · R": {
        "count": 1,
        "mean_reward": 5.907041213744515
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R · R+φ1 · R · R": {
        "count": 1,
        "mean_reward": 5.266839093560615
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}+φ1 · φ1 · R^{ab} · R_{ab}+φ1 · ∇^{a}φ1 · ∇_{a}R+∇^{a}φ1 · ∇^{b}φ1 · R_{ab}+φ1 · φ1+φ1 · φ1 · ∇^{a}φ1 · ∇_{a}φ1": {
        "count": 1,
        "mean_reward": -7.0
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{fdh}+φ1 · R+∇^{a}φ1 · ∇_{a}R+∇^{a}φ1 · ∇^{b}φ1 · R_{ab}+φ1 · ∇^{a}φ1 · ∇_{a}φ1": {
        "count": 1,
        "mean_reward": -7.0
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R^{bcd}_{a} · R^{a}_{bcd}+φ1 · ∇^{a}∇_{a}R+∇^{a}φ1 · ∇_{a}R+∇^{a}φ1 · ∇^{b}φ1 · R_{ab}+φ1 · φ1": {
        "count": 1,
        "mean_reward": 8.30881416776524
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R^{ab} · R^{d}_{a} · R_{bd}+R^{b}_{a} · R^{cd} · R^{a}_{cbd}+φ1 · φ1 · φ1 · R+φ1 · φ1 · R^{ab} · R_{ab}+φ1 · ∇^{a}∇^{b}φ1 · R_{ab}+φ1 · φ1+φ1 · φ1 · φ1": {
        "count": 1,
        "mean_reward": -2.5
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R^{ab} · R^{d}_{a} · R_{bd}": {
        "count": 1,
        "mean_reward": 5.568416097861457
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+φ1 · R^{bcd}_{a} · R^{a}_{bcd}": {
        "count": 1,
        "mean_reward": 8.929917414716948
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+φ1 · φ1 · R · R": {
        "count": 1,
        "mean_reward": 7.244886509892349
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+∇^{a}R · ∇_{a}R": {
        "count": 1,
        "mean_reward": 7.324741213177167
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+∇^{a}∇_{a}R · R^{c}_{c}+∇^{c}R^{ab} · ∇_{b}R_{ac}+∇^{c}R^{ab} · ∇_{c}R_{ab}+∇^{a}φ1 · ∇^{b}φ1 · R_{ab}+∇^{a}∇_{a}φ1+φ1 · φ1 · ∇^{a}∇_{a}φ1+φ1 · φ1 · ∇^{a}φ1 · ∇_{a}φ1": {
        "count": 1,
        "mean_reward": -6.0
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+φ1 · ∇^{a}∇_{a}R+φ1 · φ1 · R^{ab} · R_{ab}+φ1 · φ1 · φ1 · φ1+φ1 · ∇^{a}∇_{a}φ1": {
        "count": 1,
        "mean_reward": -3.0
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R^{b}_{a} · R^{cd} · R^{a}_{cbd}+φ1 · φ1 · R+φ1 · φ1 · φ1 · R+φ1 · ∇^{a}φ1 · ∇_{a}R+∇^{a}φ1 · ∇^{b}φ1 · R_{ab}+φ1 · φ1 · ∇^{a}φ1 · ∇_{a}φ1": {
        "count": 1,
        "mean_reward": -2.5
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R^{ab} · R^{d}_{a} · R_{bd}+φ1 · R^{ab} · R_{ab}+φ1 · φ1 · φ1 · φ1": {
        "count": 1,
        "mean_reward": -3.0
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+∇^{a}φ1 · ∇_{a}φ1 · R+∇^{a}φ1 · ∇^{b}φ1 · R_{ab}": {
        "count": 1,
        "mean_reward": 7.423648548502751
      },
      "scalar=phi1_only|potential={'phi1': 'axion', 'phi2': None}|operators=R+φ1 · φ1 · R": {
        "count": 1,
        "mean_reward": -2.5
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+φ1 · φ1 · R · R+∇^{a}φ1 · ∇^{b}φ1 · R_{ab}": {
        "count": 1,
        "mean_reward": 3.7874801541580725
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R · R+∇^{a}∇_{a}R": {
        "count": 1,
        "mean_reward": 8.610043642339305
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+∇^{a}∇_{a}R+φ1 · R": {
        "count": 1,
        "mean_reward": -2.5
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+φ1 · R · R": {
        "count": 1,
        "mean_reward": 8.034673763130359
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+∇^{a}∇_{a}R+∇^{c}R^{ab} · ∇_{b}R_{ac}+φ1 · R+φ1 · ∇^{a}∇_{a}φ1 · R+∇^{a}φ1 · ∇^{b}φ1 · R_{ab}": {
        "count": 1,
        "mean_reward": -2.5
      },
      "scalar=phi1_only|potential={'phi1': 'axion', 'phi2': None}|operators=R": {
        "count": 2,
        "mean_reward": 8.30073509782606
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+φ1 · R^{ab} · R_{ab}+φ1 · φ1 · R^{ab} · R_{ab}+φ1 · φ1 · φ1 · φ1+∇^{a}φ1 · ∇_{a}φ1": {
        "count": 1,
        "mean_reward": -3.0
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+φ1 · ∇^{a}∇_{a}R+∇^{a}φ1 · ∇_{a}φ1 · R+∇^{a}φ1 · ∇^{b}φ1 · R_{ab}+φ1 · φ1 · φ1 · φ1+φ1 · φ1 · ∇^{a}∇_{a}φ1": {
        "count": 1,
        "mean_reward": -3.0
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R · R+φ1 · φ1 · R^{ab} · R_{ab}+∇^{a}φ1 · ∇^{b}φ1 · R_{ab}+φ1 · ∇^{a}φ1 · ∇_{a}φ1": {
        "count": 1,
        "mean_reward": -6.0
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R^{ab} · R_{ab}+φ1 · R^{ab} · R_{ab}": {
        "count": 1,
        "mean_reward": 8.614437273218519
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R^{ab} · R_{ab}+∇^{a}φ1 · ∇^{b}φ1 · R_{ab}": {
        "count": 1,
        "mean_reward": 7.344112440434419
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+φ1 · φ1 · φ1 · φ1 · R+φ1 · φ1 · φ1 · φ1 · φ1 · φ1": {
        "count": 1,
        "mean_reward": -4.5
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+∇^{a}∇^{b}φ1 · R_{ab}+∇^{a}φ1 · ∇_{a}φ1 · R": {
        "count": 1,
        "mean_reward": 9.0006409123732
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R^{ab} · R_{ab}+φ1 · R+φ1 · φ1 · φ1 · φ1 · φ1": {
        "count": 1,
        "mean_reward": -3.0
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+φ1 · φ1 · φ1 · φ1": {
        "count": 1,
        "mean_reward": -3.0
      },
      "scalar=phi1_only|potential={'phi1': 'axion', 'phi2': None}|operators=R+∇^{a}∇_{a}φ1 · R+φ1 · ∇^{a}∇_{a}φ1 · R+∇^{a}φ1 · ∇_{a}φ1 · R": {
        "count": 1,
        "mean_reward": 11.423033657743288
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R · R+φ1 · φ1 · R · R": {
        "count": 1,
        "mean_reward": 11.428433498377041
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+∇^{a}∇_{a}R+∇^{c}R^{ab} · ∇_{b}R_{ac}+∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}+∇^{a}φ1 · ∇^{b}φ1 · R_{ab}": {
        "count": 1,
        "mean_reward": 5.338494363523618
      },
      "scalar=phi1_only|potential={'phi1': 'quadratic', 'phi2': None}|operators=R+R^{ab} · R_{ab}": {
        "count": 1,
        "mean_reward": 11.428027252638246
      }
    },
    "accepted_feature_counts": {
      "scalar_config=phi1_only": 48,
      "theory_track=eh_anchored": 48,
      "has_R_anchor": 48,
      "has_scalar": 48,
      "has_phi1": 48,
      "has_scalar_curvature": 48,
      "phi1_potential=quadratic": 44,
      "has_high_curvature": 27,
      "has_derivative_operator": 24,
      "has_box_operator": 11,
      "has_pure_scalar_operator": 7,
      "phi1_potential=axion": 4
    },
    "excellent_feature_counts": {
      "scalar_config=phi1_only": 19,
      "theory_track=eh_anchored": 19,
      "has_R_anchor": 19,
      "has_scalar": 19,
      "has_phi1": 19,
      "has_scalar_curvature": 19,
      "phi1_potential=quadratic": 18,
      "has_derivative_operator": 11,
      "has_high_curvature": 10,
      "has_box_operator": 5,
      "has_pure_scalar_operator": 2,
      "phi1_potential=axion": 1
    },
    "competitive_feature_counts": {
      "scalar_config=phi1_only": 29,
      "theory_track=eh_anchored": 29,
      "has_R_anchor": 29,
      "has_scalar": 29,
      "has_phi1": 29,
      "has_scalar_curvature": 29,
      "phi1_potential=quadratic": 26,
      "has_high_curvature": 17,
      "has_derivative_operator": 13,
      "has_box_operator": 6,
      "has_pure_scalar_operator": 5,
      "phi1_potential=axion": 3
    }
  },
  "agent_loop": {
    "reflection_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/memory/graph_agent_batch_208_split_v4/tracks/eh_anchored/agent_reflections.jsonl",
    "structure_prior_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/memory/graph_agent_batch_208_split_v4/tracks/eh_anchored/structure_prior.json",
    "parameter_prior_path": "/oscar/home/wsun47/Modify_GR/ai_theory_lab/memory/graph_agent_batch_208_split_v4/tracks/eh_anchored/parameter_prior.json",
    "latest_reflection": {
      "timestamp": "2026-06-09T20:50:05-0400",
      "loop_id": "wave_0013_lag_6",
      "observations": [
        "total_attempts=104",
        "validated_count=62",
        "best_chi2=1638.0428393360799",
        "last_loop_id=wave_0013_lag_6",
        "last_tags=['q_initial_root_failure', 'h_absurdly_large']",
        "preferred_scalar_configs={'phi1_only': 35.0}",
        "scalar_family_metrics={'none': {'attempts': 1, 'validated_attempts': 0, 'entered_solver_attempts': 1, 'validated_attempt_rate': 0.0, 'entered_solver_attempt_rate': 1.0, 'sample_count': 5000, 'accepted_sample_count': 131, 'accepted_sample_rate': 0.0262, 'q_initial_root_failure_count': 0, 'q_initial_root_failure_rate': 0.0, 'q_not_determined_attempts': 0, 'q_not_determined_attempt_rate': 0.0, 'no_scalar_constraint_count': 50, 'no_scalar_constraint_rate': 0.01, 'constraint_drift_count': 0, 'constraint_drift_rate': 0.0, 'integration_failure_count': 0, 'integration_failure_rate': 0.0, 'best_chi2': None, 'median_chi2': None, 'chi2_quality_counts': {}, 'operator_family_counts': {'scalar_config=none': 1, 'theory_track=eh_anchored': 1, 'has_R_anchor': 1, 'is_no_scalar': 1}}, 'phi1_only': {'attempts': 98, 'validated_attempts': 60, 'entered_solver_attempts': 98, 'validated_attempt_rate': 0.6122448979591837, 'entered_solver_attempt_rate': 1.0, 'sample_count': 490000, 'accepted_sample_count': 31382, 'accepted_sample_rate': 0.06404489795918368, 'q_initial_root_failure_count': 30174, 'q_initial_root_failure_rate': 0.06157959183673469, 'q_not_determined_attempts': 0, 'q_not_determined_attempt_rate': 0.0, 'no_scalar_constraint_count': 0, 'no_scalar_constraint_rate': 0.0, 'constraint_drift_count': 488, 'constraint_drift_rate': 0.0009959183673469388, 'integration_failure_count': 622, 'integration_failure_rate': 0.0012693877551020409, 'best_chi2': 1638.0428393360799, 'median_chi2': 1662.814486657138, 'chi2_quality_counts': {'competitive': 29, 'excellent': 19, 'weak_accept': 12}, 'operator_family_counts': {'scalar_config=phi1_only': 98, 'theory_track=eh_anchored': 98, 'has_R_anchor': 98, 'has_scalar': 98, 'has_phi1': 98, 'has_scalar_curvature': 98, 'phi1_potential=quadratic': 91, 'has_high_curvature': 61, 'has_derivative_operator': 54, 'has_pure_scalar_operator': 29, 'has_box_operator': 27, 'phi1_potential=axion': 7}}, 'phi2_only': {'attempts': 5, 'validated_attempts': 2, 'entered_solver_attempts': 5, 'validated_attempt_rate': 0.4, 'entered_solver_attempt_rate': 1.0, 'sample_count': 25000, 'accepted_sample_count': 655, 'accepted_sample_rate': 0.0262, 'q_initial_root_failure_count': 3200, 'q_initial_root_failure_rate': 0.128, 'q_not_determined_attempts': 0, 'q_not_determined_attempt_rate': 0.0, 'no_scalar_constraint_count': 0, 'no_scalar_constraint_rate': 0.0, 'constraint_drift_count': 21, 'constraint_drift_rate': 0.00084, 'integration_failure_count': 0, 'integration_failure_rate': 0.0, 'best_chi2': 9431.93283437729, 'median_chi2': 9432.970409402007, 'chi2_quality_counts': {'poor_accept': 2}, 'operator_family_counts': {'scalar_config=phi2_only': 5, 'theory_track=eh_anchored': 5, 'has_R_anchor': 5, 'has_scalar': 5, 'has_phi2': 5, 'has_scalar_curvature': 5, 'has_derivative_operator': 4, 'phi2_potential=axion': 3, 'has_box_operator': 3, 'has_pure_scalar_operator': 3, 'has_high_curvature': 2, 'phi2_potential=quadratic': 2}}, 'both': {'attempts': 0, 'validated_attempts': 0, 'entered_solver_attempts': 0, 'validated_attempt_rate': None, 'entered_solver_attempt_rate': None, 'sample_count': 0, 'accepted_sample_count': 0, 'accepted_sample_rate': None, 'q_initial_root_failure_count': 0, 'q_initial_root_failure_rate': None, 'q_not_determined_attempts': 0, 'q_not_determined_attempt_rate': None, 'no_scalar_constraint_count': 0, 'no_scalar_constraint_rate': None, 'constraint_drift_count': 0, 'constraint_drift_rate': None, 'integration_failure_count': 0, 'integration_failure_rate': None, 'best_chi2': None, 'median_chi2': None, 'chi2_quality_counts': {}, 'operator_family_counts': {}}}",
        "accepted_parameter_samples=32168"
      ],
      "next_actions": [
        "bias structure generation toward accepted scalar configurations and operators",
        "compare scalar-family root-success metrics and adjust the nearby structure/parameter prior without banning the family"
      ],
      "information_used": [
        "attempt_history.jsonl",
        "feedback_summary.json",
        "all_samples_summary.csv paths from current loop"
      ],
      "information_not_used": [
        "historical solver_result/top10 outputs"
      ]
    },
    "structure_prior": {
      "source": "current_loop_feedback",
      "scalar_family_learning": {
        "principle": "same metrics and soft scoring are applied to none, phi1_only, phi2_only, and both; no scalar family is banned from exploration",
        "min_exploration_probability_per_family": 0.08,
        "metrics": {
          "none": {
            "attempts": 1,
            "validated_attempts": 0,
            "entered_solver_attempts": 1,
            "validated_attempt_rate": 0.0,
            "entered_solver_attempt_rate": 1.0,
            "sample_count": 5000,
            "accepted_sample_count": 131,
            "accepted_sample_rate": 0.0262,
            "q_initial_root_failure_count": 0,
            "q_initial_root_failure_rate": 0.0,
            "q_not_determined_attempts": 0,
            "q_not_determined_attempt_rate": 0.0,
            "no_scalar_constraint_count": 50,
            "no_scalar_constraint_rate": 0.01,
            "constraint_drift_count": 0,
            "constraint_drift_rate": 0.0,
            "integration_failure_count": 0,
            "integration_failure_rate": 0.0,
            "best_chi2": null,
            "median_chi2": null,
            "chi2_quality_counts": {},
            "operator_family_counts": {
              "scalar_config=none": 1,
              "theory_track=eh_anchored": 1,
              "has_R_anchor": 1,
              "is_no_scalar": 1
            }
          },
          "phi1_only": {
            "attempts": 98,
            "validated_attempts": 60,
            "entered_solver_attempts": 98,
            "validated_attempt_rate": 0.6122448979591837,
            "entered_solver_attempt_rate": 1.0,
            "sample_count": 490000,
            "accepted_sample_count": 31382,
            "accepted_sample_rate": 0.06404489795918368,
            "q_initial_root_failure_count": 30174,
            "q_initial_root_failure_rate": 0.06157959183673469,
            "q_not_determined_attempts": 0,
            "q_not_determined_attempt_rate": 0.0,
            "no_scalar_constraint_count": 0,
            "no_scalar_constraint_rate": 0.0,
            "constraint_drift_count": 488,
            "constraint_drift_rate": 0.0009959183673469388,
            "integration_failure_count": 622,
            "integration_failure_rate": 0.0012693877551020409,
            "best_chi2": 1638.0428393360799,
            "median_chi2": 1662.814486657138,
            "chi2_quality_counts": {
              "competitive": 29,
              "excellent": 19,
              "weak_accept": 12
            },
            "operator_family_counts": {
              "scalar_config=phi1_only": 98,
              "theory_track=eh_anchored": 98,
              "has_R_anchor": 98,
              "has_scalar": 98,
              "has_phi1": 98,
              "has_scalar_curvature": 98,
              "phi1_potential=quadratic": 91,
              "has_high_curvature": 61,
              "has_derivative_operator": 54,
              "has_pure_scalar_operator": 29,
              "has_box_operator": 27,
              "phi1_potential=axion": 7
            }
          },
          "phi2_only": {
            "attempts": 5,
            "validated_attempts": 2,
            "entered_solver_attempts": 5,
            "validated_attempt_rate": 0.4,
            "entered_solver_attempt_rate": 1.0,
            "sample_count": 25000,
            "accepted_sample_count": 655,
            "accepted_sample_rate": 0.0262,
            "q_initial_root_failure_count": 3200,
            "q_initial_root_failure_rate": 0.128,
            "q_not_determined_attempts": 0,
            "q_not_determined_attempt_rate": 0.0,
            "no_scalar_constraint_count": 0,
            "no_scalar_constraint_rate": 0.0,
            "constraint_drift_count": 21,
            "constraint_drift_rate": 0.00084,
            "integration_failure_count": 0,
            "integration_failure_rate": 0.0,
            "best_chi2": 9431.93283437729,
            "median_chi2": 9432.970409402007,
            "chi2_quality_counts": {
              "poor_accept": 2
            },
            "operator_family_counts": {
              "scalar_config=phi2_only": 5,
              "theory_track=eh_anchored": 5,
              "has_R_anchor": 5,
              "has_scalar": 5,
              "has_phi2": 5,
              "has_scalar_curvature": 5,
              "has_derivative_operator": 4,
              "phi2_potential=axion": 3,
              "has_box_operator": 3,
              "has_pure_scalar_operator": 3,
              "has_high_curvature": 2,
              "phi2_potential=quadratic": 2
            }
          },
          "both": {
            "attempts": 0,
            "validated_attempts": 0,
            "entered_solver_attempts": 0,
            "validated_attempt_rate": null,
            "entered_solver_attempt_rate": null,
            "sample_count": 0,
            "accepted_sample_count": 0,
            "accepted_sample_rate": null,
            "q_initial_root_failure_count": 0,
            "q_initial_root_failure_rate": null,
            "q_not_determined_attempts": 0,
            "q_not_determined_attempt_rate": null,
            "no_scalar_constraint_count": 0,
            "no_scalar_constraint_rate": null,
            "constraint_drift_count": 0,
            "constraint_drift_rate": null,
            "integration_failure_count": 0,
            "integration_failure_rate": null,
            "best_chi2": null,
            "median_chi2": null,
            "chi2_quality_counts": {},
            "operator_family_counts": {}
          }
        }
      },
      "accepted_attempt_count": 62,
      "quality_accepted_attempt_count": 60,
      "accepted_quality_counts": {
        "competitive": 29,
        "excellent": 19,
        "weak_accept": 12,
        "poor_accept": 2
      },
      "preferred_scalar_configs": {
        "phi1_only": 35.0
      },
      "preferred_potentials": {
        "phi1:quadratic": 35.0
      },
      "preferred_operators": {
        "R": 35.0,
        "∇^{a}φ1 · ∇^{b}φ1 · R_{ab}": 14.0,
        "R · R": 7.0,
        "φ1 · φ1 · R^{ab} · R_{ab}": 7.0,
        "∇^{a}φ1 · ∇_{a}φ1 · R": 7.0,
        "φ1 · ∇^{a}∇_{a}R": 3.5,
        "R^{b}_{a} · R^{cd} · R^{a}_{cbd}": 3.5,
        "∇^{c}R^{ab} · ∇_{b}R_{ac}": 3.5,
        "∇^{a}∇_{a}R": 3.5,
        "R^{ab} · R^{d}_{a} · R_{bd}": 3.5,
        "R_{ab} · R^{adef} · R^{b}_{def}": 3.5,
        "φ1 · R^{ab} · R_{ab}": 3.5,
        "φ1 · ∇^{a}∇_{a}φ1": 3.5
      },
      "preferred_features": {
        "scalar_config=phi1_only": 35.0,
        "theory_track=eh_anchored": 35.0,
        "phi1_potential=quadratic": 35.0,
        "has_R_anchor": 35.0,
        "has_scalar": 35.0,
        "has_phi1": 35.0,
        "has_scalar_curvature": 35.0,
        "has_derivative_operator": 24.5,
        "has_high_curvature": 17.5,
        "has_box_operator": 10.5,
        "has_pure_scalar_operator": 3.5
      },
      "avoid_scalar_configs": {
        "phi1_only": 17,
        "phi2_only": 3,
        "none": 1
      },
      "avoid_features": {
        "has_phi1_with_q_failure": 17,
        "derivative_with_numerical_failure": 16,
        "high_curvature_with_numerical_failure": 15,
        "has_phi2_with_q_failure": 3,
        "is_no_scalar_with_constraint_failure": 1
      },
      "avoid_operators": {},
      "avoid_failure_tags": {
        "q_initial_root_failure": 82,
        "constraint_drift": 57,
        "integration_failure": 5,
        "no_scalar_constraint": 1
      },
      "best_chi2": 1638.0428393360799
    },
    "parameter_prior": {
      "source": "accepted_all_samples",
      "active": false,
      "attempt_count": 104,
      "accepted_sample_count": 32168,
      "min_attempts_before_update": 150,
      "min_accepted_samples": 20,
      "fixed_parameters": [
        "H0_km_s_Mpc"
      ],
      "parameters": {},
      "message": "Parameter prior evidence is recorded, but defaults remain active until update thresholds are met."
    }
  }
}
```

## Required Reflection Output

Write a JSON object with these fields before generating the next proposal:

```json
{
  "observations": ["facts noticed from the current-loop summary"],
  "hypotheses_about_failures": ["your own explanation of why failures happened"],
  "hypotheses_about_successes": ["your own explanation of why any successful low-chi2 attempts worked"],
  "next_proposal_plan": "what you will try next and why",
  "information_used": ["paths or facts used; must be current-loop only"],
  "information_not_used": ["confirm historical solver_result/top10 data was not used"]
}
```
