# Accepted Lagrangians Full

Complete dimension-balanced Lagrangians, best-fit coefficient substitutions, metadata, and Solver paths.
Only the best chi-square representative from each accepted theory family is shown for human inspection.
The full accepted-attempt list is preserved in `accepted_summary.json`.

## 1. task_000273_slot_01_lag_1  chi2=1638.113013

- scalar_config: `phi1_only`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: `124`
- H0_km_s_Mpc: `62.68730712`
- Omega_m0: `0.27861418`
- lambda_H_Lambda_over_H0: `4599.82908252`
- effective_correction_status: `eh_only`
- max_relative_effect_to_EH: `0`
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ]
```

### Term Metadata

```json
[
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
]
```

### Effective Correction Diagnostics

```json
{
  "effective_correction_status": "eh_only",
  "effective_correction_reason": "no non-EH free correction terms",
  "max_relative_effect_to_EH": 0.0,
  "dominant_correction_term": "",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 0,
  "correction_term_count": 0,
  "tiny_correction_fraction": null,
  "term_effects": []
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000273_slot_01/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000273_slot_01/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000273_slot_01/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 2. task_000247_expanded_slot_03_lag_1  chi2=1638.114263

- scalar_config: `phi1_only`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: `1674`
- H0_km_s_Mpc: `69.79384805`
- Omega_m0: `0.27866957`
- lambda_H_Lambda_over_H0: `4435.68904775`
- effective_correction_status: `eh_dominated`
- max_relative_effect_to_EH: `1.00584427e-13`
- dominant_correction_term: `φ1 · R^{ab} · R_{ab}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-3} · φ1 · R^{ab} · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-0.0020278028) Λ^{-3} · φ1 · R^{ab} · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-3} · φ1 · R^{ab} · R_{ab} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -0.0020278028 · Λ^{-3} · φ1 · R^{ab} · R_{ab} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ]
```

### Term Metadata

```json
[
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
    "candidate": "φ1 · R^{ab} · R_{ab}",
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
]
```

### Effective Correction Diagnostics

```json
{
  "effective_correction_status": "eh_dominated",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 1.0058442689354495e-13,
  "dominant_correction_term": "φ1 · R^{ab} · R_{ab}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 1,
  "correction_term_count": 1,
  "tiny_correction_fraction": 1.0,
  "term_effects": [
    {
      "candidate": "φ1 · R^{ab} · R_{ab}",
      "coeff_symbol": "\\beta",
      "coefficient": "-0.002027802815558047",
      "lambda_power": -3,
      "sector": "non-minimal",
      "relative_effect_to_EH": 1.0058442689354495e-13,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000247_expanded_slot_03/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000247_expanded_slot_03/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000247_expanded_slot_03/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 3. task_000229_slot_03_lag_1  chi2=1638.116086

- scalar_config: `phi1_only`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: `1`
- H0_km_s_Mpc: `68.25086958`
- Omega_m0: `0.27841389`
- lambda_H_Lambda_over_H0: `4661.1754962`
- effective_correction_status: `weak`
- max_relative_effect_to_EH: `2.51188643e-06`
- dominant_correction_term: `φ1 · R^{bcd}_{a} · R^{a}_{bcd}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-5.8770521620e+04) Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -5.8770521620e+04 · Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ]
```

### Term Metadata

```json
[
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
    "candidate": "φ1 · R^{bcd}_{a} · R^{a}_{bcd}",
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
]
```

### Effective Correction Diagnostics

```json
{
  "effective_correction_status": "weak",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 2.5118864315095823e-06,
  "dominant_correction_term": "φ1 · R^{bcd}_{a} · R^{a}_{bcd}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 1,
  "tiny_correction_terms": 0,
  "correction_term_count": 1,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "φ1 · R^{bcd}_{a} · R^{a}_{bcd}",
      "coeff_symbol": "\\beta",
      "coefficient": "-58770.521619758234",
      "lambda_power": -3,
      "sector": "non-minimal",
      "relative_effect_to_EH": 2.5118864315095823e-06,
      "effect_class": "weak"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000229_slot_03/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000229_slot_03/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000229_slot_03/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 4. task_000300_slot_07_lag_1  chi2=1638.117759

- scalar_config: `both`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "quadratic", "phi2": "quadratic"}`
- agent_parameter_sample_index: `501`
- H0_km_s_Mpc: `71.23681295`
- Omega_m0: `0.27846224`
- lambda_H_Lambda_over_H0: `4625.50950771`
- effective_correction_status: `eh_only`
- max_relative_effect_to_EH: `0`
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Term Metadata

```json
[
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
  },
  {
    "coeff_symbol": "1",
    "coeff_token": "COEFF_FIXED_1",
    "candidate": "-½ g^{μν} ∇_μφ2 ∇_νφ2",
    "mass_dim": 4,
    "lambda_power": 0,
    "fixed": true,
    "sector": "matter"
  },
  {
    "coeff_symbol": "1",
    "coeff_token": "COEFF_FIXED_1",
    "candidate": "-½ m_2² φ2²",
    "mass_dim": 4,
    "lambda_power": 0,
    "fixed": true,
    "sector": "matter",
    "potential_type": "quadratic"
  }
]
```

### Effective Correction Diagnostics

```json
{
  "effective_correction_status": "eh_only",
  "effective_correction_reason": "no non-EH free correction terms",
  "max_relative_effect_to_EH": 0.0,
  "dominant_correction_term": "",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 0,
  "correction_term_count": 0,
  "tiny_correction_fraction": null,
  "term_effects": []
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000300_slot_07/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000300_slot_07/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000300_slot_07/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 5. task_000245_expanded_slot_07_lag_1  chi2=1638.121478

- scalar_config: `phi1_only`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: `833`
- H0_km_s_Mpc: `72.10066175`
- Omega_m0: `0.27856417`
- lambda_H_Lambda_over_H0: `4189.92587046`
- effective_correction_status: `moderate`
- max_relative_effect_to_EH: `0.00131296`
- dominant_correction_term: `R^{ab} · R_{ab}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-2} · R^{ab} · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (1.1524784183e+04) Λ^{-2} · R^{ab} · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-2} · R^{ab} · R_{ab} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 1.1524784183e+04 · Λ^{-2} · R^{ab} · R_{ab} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ]
```

### Term Metadata

```json
[
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
    "candidate": "R^{ab} · R_{ab}",
    "mass_dim": 4,
    "lambda_power": -2,
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
]
```

### Effective Correction Diagnostics

```json
{
  "effective_correction_status": "moderate",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 0.0013129558372864747,
  "dominant_correction_term": "R^{ab} · R_{ab}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 1,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 0,
  "correction_term_count": 1,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "R^{ab} · R_{ab}",
      "coeff_symbol": "\\beta",
      "coefficient": "11524.784183385676",
      "lambda_power": -2,
      "sector": "gravity",
      "relative_effect_to_EH": 0.0013129558372864747,
      "effect_class": "moderate"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000245_expanded_slot_07/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000245_expanded_slot_07/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000245_expanded_slot_07/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 6. task_000205_slot_05_lag_1  chi2=1638.149023

- scalar_config: `phi1_only`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: `1`
- H0_km_s_Mpc: `67.87096695`
- Omega_m0: `0.27745035`
- lambda_H_Lambda_over_H0: `3790.41584254`
- effective_correction_status: `active`
- max_relative_effect_to_EH: `3.06395626e+04`
- dominant_correction_term: `∇^{a}∇_{a}R · R^{c}_{c}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd}  +  \gamma Λ^{-4} · R · R · R  +  \delta Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{fdh}  +  \epsilon Λ^{-4} · ∇^{a}∇_{a}R · R^{c}_{c}  +  \zeta Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-1.0000000000e-04) Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd}  +  (1.0000000000e+14) Λ^{-4} · R · R · R  +  (-3.1622776602e-09) Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{fdh}  +  (3.1622776602e+18) Λ^{-4} · ∇^{a}∇_{a}R · R^{c}_{c}  +  (-3.1622776602) Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · R · R · R ) ] +
√(-g) [ M_p² ( \delta · Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{fdh} ) ] +
√(-g) [ M_p² ( \epsilon · Λ^{-4} · ∇^{a}∇_{a}R · R^{c}_{c} ) ] +
√(-g) [ M_p² ( \zeta · Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -1.0000000000e-04 · Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( 1.0000000000e+14 · Λ^{-4} · R · R · R ) ] +
√(-g) [ M_p² ( -3.1622776602e-09 · Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{fdh} ) ] +
√(-g) [ M_p² ( 3.1622776602e+18 · Λ^{-4} · ∇^{a}∇_{a}R · R^{c}_{c} ) ] +
√(-g) [ M_p² ( -3.1622776602 · Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ]
```

### Term Metadata

```json
[
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
    "candidate": "R^{bcd}_{a} · R^{a}_{bcd}",
    "mass_dim": 4,
    "lambda_power": -2,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\gamma",
    "coeff_token": "COEFF_2",
    "candidate": "R · R · R",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\delta",
    "coeff_token": "COEFF_3",
    "candidate": "R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{fdh}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\epsilon",
    "coeff_token": "COEFF_4",
    "candidate": "∇^{a}∇_{a}R · R^{c}_{c}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\zeta",
    "coeff_token": "COEFF_5",
    "candidate": "φ1 · R^{bcd}_{a} · R^{a}_{bcd}",
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
]
```

### Effective Correction Diagnostics

```json
{
  "effective_correction_status": "active",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 30639.562614514194,
  "dominant_correction_term": "∇^{a}∇_{a}R · R^{c}_{c}",
  "active_correction_terms": 2,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 3,
  "correction_term_count": 5,
  "tiny_correction_fraction": 0.6,
  "term_effects": [
    {
      "candidate": "R^{bcd}_{a} · R^{a}_{bcd}",
      "coeff_symbol": "\\beta",
      "coefficient": "-0.0001",
      "lambda_power": -2,
      "sector": "gravity",
      "relative_effect_to_EH": 1.3920546280459578e-11,
      "effect_class": "tiny"
    },
    {
      "candidate": "R · R · R",
      "coeff_symbol": "\\gamma",
      "coefficient": "100000000000000.0",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 0.968908043732085,
      "effect_class": "active"
    },
    {
      "candidate": "R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{fdh}",
      "coeff_symbol": "\\delta",
      "coefficient": "-3.1622776601683795e-09",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 3.0639562614514195e-23,
      "effect_class": "tiny"
    },
    {
      "candidate": "∇^{a}∇_{a}R · R^{c}_{c}",
      "coeff_symbol": "\\epsilon",
      "coefficient": "3.1622776601683794e+18",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 30639.562614514194,
      "effect_class": "active"
    },
    {
      "candidate": "φ1 · R^{bcd}_{a} · R^{a}_{bcd}",
      "coeff_symbol": "\\zeta",
      "coefficient": "-3.1622776601683795",
      "lambda_power": -3,
      "sector": "non-minimal",
      "relative_effect_to_EH": 2.5156750881318133e-10,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000205_slot_05/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000205_slot_05/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000205_slot_05/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 7. task_000075_expanded_slot_03_lag_1  chi2=1638.154473

- scalar_config: `phi1_only`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "axion", "phi2": null}`
- agent_parameter_sample_index: `110`
- H0_km_s_Mpc: `64.5286005`
- Omega_m0: `0.30777552`
- lambda_H_Lambda_over_H0: `1652.26052863`
- effective_correction_status: `active`
- max_relative_effect_to_EH: `8513.84990932`
- dominant_correction_term: `R^{ab} · R^{d}_{a} · R_{bd}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · R^{ab} · R^{d}_{a} · R_{bd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-3.1725619119e+16) Λ^{-4} · R^{ab} · R^{d}_{a} · R_{bd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · R^{ab} · R^{d}_{a} · R_{bd} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -3.1725619119e+16 · Λ^{-4} · R^{ab} · R^{d}_{a} · R_{bd} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Term Metadata

```json
[
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
    "candidate": "R^{ab} · R^{d}_{a} · R_{bd}",
    "mass_dim": 6,
    "lambda_power": -4,
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
    "candidate": "-m_1² f_1² (1 - cos(φ1/f_1))",
    "mass_dim": 4,
    "lambda_power": 0,
    "fixed": true,
    "sector": "matter",
    "potential_type": "axion"
  }
]
```

### Effective Correction Diagnostics

```json
{
  "effective_correction_status": "active",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 8513.84990932435,
  "dominant_correction_term": "R^{ab} · R^{d}_{a} · R_{bd}",
  "active_correction_terms": 1,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 0,
  "correction_term_count": 1,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "R^{ab} · R^{d}_{a} · R_{bd}",
      "coeff_symbol": "\\beta",
      "coefficient": "-3.1725619119022024e+16",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 8513.84990932435,
      "effect_class": "active"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000075_expanded_slot_03/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000075_expanded_slot_03/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000075_expanded_slot_03/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 8. task_000058_expanded_slot_07_lag_1  chi2=1638.164106

- scalar_config: `phi1_only`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "axion", "phi2": null}`
- agent_parameter_sample_index: `1050`
- H0_km_s_Mpc: `58`
- Omega_m0: `0.28765161`
- lambda_H_Lambda_over_H0: `1445.2397905`
- effective_correction_status: `weak`
- max_relative_effect_to_EH: `4.15291335e-05`
- dominant_correction_term: `φ1 · R · R`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-3} · φ1 · R · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-7833.2743767738) Λ^{-3} · φ1 · R · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-3} · φ1 · R · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -7833.2743767738 · Λ^{-3} · φ1 · R · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Term Metadata

```json
[
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
    "candidate": "φ1 · R · R",
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
    "candidate": "-m_1² f_1² (1 - cos(φ1/f_1))",
    "mass_dim": 4,
    "lambda_power": 0,
    "fixed": true,
    "sector": "matter",
    "potential_type": "axion"
  }
]
```

### Effective Correction Diagnostics

```json
{
  "effective_correction_status": "weak",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 4.1529133521161204e-05,
  "dominant_correction_term": "φ1 · R · R",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 1,
  "tiny_correction_terms": 0,
  "correction_term_count": 1,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "φ1 · R · R",
      "coeff_symbol": "\\beta",
      "coefficient": "-7833.274376773763",
      "lambda_power": -3,
      "sector": "non-minimal",
      "relative_effect_to_EH": 4.1529133521161204e-05,
      "effect_class": "weak"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000058_expanded_slot_07/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000058_expanded_slot_07/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000058_expanded_slot_07/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 9. task_000078_slot_06_lag_1  chi2=1638.180337

- scalar_config: `phi1_only`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "axion", "phi2": null}`
- agent_parameter_sample_index: `578`
- H0_km_s_Mpc: `69.28439962`
- Omega_m0: `0.3038528`
- lambda_H_Lambda_over_H0: `1457.70152491`
- effective_correction_status: `eh_only`
- max_relative_effect_to_EH: `0`
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Term Metadata

```json
[
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
    "candidate": "-m_1² f_1² (1 - cos(φ1/f_1))",
    "mass_dim": 4,
    "lambda_power": 0,
    "fixed": true,
    "sector": "matter",
    "potential_type": "axion"
  }
]
```

### Effective Correction Diagnostics

```json
{
  "effective_correction_status": "eh_only",
  "effective_correction_reason": "no non-EH free correction terms",
  "max_relative_effect_to_EH": 0.0,
  "dominant_correction_term": "",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 0,
  "correction_term_count": 0,
  "tiny_correction_fraction": null,
  "term_effects": []
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000078_slot_06/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000078_slot_06/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000078_slot_06/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 10. task_000234_expanded_slot_02_lag_1  chi2=1638.26859

- scalar_config: `both`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "axion", "phi2": "quadratic"}`
- agent_parameter_sample_index: `1526`
- H0_km_s_Mpc: `62.50944259`
- Omega_m0: `0.2876433`
- lambda_H_Lambda_over_H0: `4445.19652773`
- effective_correction_status: `eh_dominated`
- max_relative_effect_to_EH: `2.95320368e-13`
- dominant_correction_term: `φ1 · R^{ab} · R_{ab}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-3} · φ1 · R^{ab} · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (0.0059900078) Λ^{-3} · φ1 · R^{ab} · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-3} · φ1 · R^{ab} · R_{ab} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 0.0059900078 · Λ^{-3} · φ1 · R^{ab} · R_{ab} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Term Metadata

```json
[
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
    "candidate": "φ1 · R^{ab} · R_{ab}",
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
    "candidate": "-m_1² f_1² (1 - cos(φ1/f_1))",
    "mass_dim": 4,
    "lambda_power": 0,
    "fixed": true,
    "sector": "matter",
    "potential_type": "axion"
  },
  {
    "coeff_symbol": "1",
    "coeff_token": "COEFF_FIXED_1",
    "candidate": "-½ g^{μν} ∇_μφ2 ∇_νφ2",
    "mass_dim": 4,
    "lambda_power": 0,
    "fixed": true,
    "sector": "matter"
  },
  {
    "coeff_symbol": "1",
    "coeff_token": "COEFF_FIXED_1",
    "candidate": "-½ m_2² φ2²",
    "mass_dim": 4,
    "lambda_power": 0,
    "fixed": true,
    "sector": "matter",
    "potential_type": "quadratic"
  }
]
```

### Effective Correction Diagnostics

```json
{
  "effective_correction_status": "eh_dominated",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 2.9532036822862934e-13,
  "dominant_correction_term": "φ1 · R^{ab} · R_{ab}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 1,
  "correction_term_count": 1,
  "tiny_correction_fraction": 1.0,
  "term_effects": [
    {
      "candidate": "φ1 · R^{ab} · R_{ab}",
      "coeff_symbol": "\\beta",
      "coefficient": "0.005990007789482939",
      "lambda_power": -3,
      "sector": "non-minimal",
      "relative_effect_to_EH": 2.9532036822862934e-13,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000234_expanded_slot_02/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000234_expanded_slot_02/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000234_expanded_slot_02/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 11. task_000064_expanded_slot_08_lag_1  chi2=1638.572595

- scalar_config: `phi1_only`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "axion", "phi2": null}`
- agent_parameter_sample_index: `1120`
- H0_km_s_Mpc: `72.62791799`
- Omega_m0: `0.30926828`
- lambda_H_Lambda_over_H0: `993.95749461`
- effective_correction_status: `moderate`
- max_relative_effect_to_EH: `5.31511088e-04`
- dominant_correction_term: `R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-2} · R · R  +  \gamma Λ^{-4} · R^{ab} · R^{d}_{a} · R_{bd}  +  \delta Λ^{-4} · R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh}  +  \epsilon Λ^{-4} · ∇^{c}R^{ab} · ∇_{b}R_{ac} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-5.1879596706) Λ^{-2} · R · R  +  (-1.4149756362e-10) Λ^{-4} · R^{ab} · R^{d}_{a} · R_{bd}  +  (2.5939021194e+08) Λ^{-4} · R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh}  +  (5.1131760343e-08) Λ^{-4} · ∇^{c}R^{ab} · ∇_{b}R_{ac} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-2} · R · R ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · R^{ab} · R^{d}_{a} · R_{bd} ) ] +
√(-g) [ M_p² ( \delta · Λ^{-4} · R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh} ) ] +
√(-g) [ M_p² ( \epsilon · Λ^{-4} · ∇^{c}R^{ab} · ∇_{b}R_{ac} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -5.1879596706 · Λ^{-2} · R · R ) ] +
√(-g) [ M_p² ( -1.4149756362e-10 · Λ^{-4} · R^{ab} · R^{d}_{a} · R_{bd} ) ] +
√(-g) [ M_p² ( 2.5939021194e+08 · Λ^{-4} · R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh} ) ] +
√(-g) [ M_p² ( 5.1131760343e-08 · Λ^{-4} · ∇^{c}R^{ab} · ∇_{b}R_{ac} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Term Metadata

```json
[
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
    "candidate": "R^{ab} · R^{d}_{a} · R_{bd}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\delta",
    "coeff_token": "COEFF_3",
    "candidate": "R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\epsilon",
    "coeff_token": "COEFF_4",
    "candidate": "∇^{c}R^{ab} · ∇_{b}R_{ac}",
    "mass_dim": 6,
    "lambda_power": -4,
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
    "candidate": "-m_1² f_1² (1 - cos(φ1/f_1))",
    "mass_dim": 4,
    "lambda_power": 0,
    "fixed": true,
    "sector": "matter",
    "potential_type": "axion"
  }
]
```

### Effective Correction Diagnostics

```json
{
  "effective_correction_status": "moderate",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 0.0005315110879021068,
  "dominant_correction_term": "R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 1,
  "weak_correction_terms": 1,
  "tiny_correction_terms": 2,
  "correction_term_count": 4,
  "tiny_correction_fraction": 0.5,
  "term_effects": [
    {
      "candidate": "R · R",
      "coeff_symbol": "\\beta",
      "coefficient": "-5.187959670569256",
      "lambda_power": -2,
      "sector": "gravity",
      "relative_effect_to_EH": 1.0502458197257822e-05,
      "effect_class": "weak"
    },
    {
      "candidate": "R^{ab} · R^{d}_{a} · R_{bd}",
      "coeff_symbol": "\\gamma",
      "coefficient": "-1.4149756361583266e-10",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 2.899397144134833e-22,
      "effect_class": "tiny"
    },
    {
      "candidate": "R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh}",
      "coeff_symbol": "\\delta",
      "coefficient": "259390211.94487092",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 0.0005315110879021068,
      "effect_class": "moderate"
    },
    {
      "candidate": "∇^{c}R^{ab} · ∇_{b}R_{ac}",
      "coeff_symbol": "\\epsilon",
      "coefficient": "5.113176034271071e-08",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 1.0477302656231304e-19,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000064_expanded_slot_08/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000064_expanded_slot_08/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000064_expanded_slot_08/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 12. task_000281_expanded_slot_06_lag_1  chi2=1639.583387

- scalar_config: `both`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "quadratic", "phi2": "quadratic"}`
- agent_parameter_sample_index: `1113`
- H0_km_s_Mpc: `72.13473831`
- Omega_m0: `0.29586466`
- lambda_H_Lambda_over_H0: `4629.40455685`
- effective_correction_status: `eh_only`
- max_relative_effect_to_EH: `0`
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R )  +  \beta Λ^{2} · φ1 · φ1  +  \gamma Λ^{-1} · φ2 · ∇^{a}φ2 · ∇_{a}φ2  +  \delta Λ^{-2} · φ1 · φ2 · ∇^{a}φ2 · ∇_{a}φ2  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R )  +  (1.8312862242e-10) Λ^{2} · φ1 · φ1  +  (5.2342251524e+08) Λ^{-1} · φ2 · ∇^{a}φ2 · ∇_{a}φ2  +  (-3.7349210007e-07) Λ^{-2} · φ1 · φ2 · ∇^{a}φ2 · ∇_{a}φ2  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ \beta · Λ^{2} · φ1 · φ1 ] +
√(-g) [ \gamma · Λ^{-1} · φ2 · ∇^{a}φ2 · ∇_{a}φ2 ] +
√(-g) [ \delta · Λ^{-2} · φ1 · φ2 · ∇^{a}φ2 · ∇_{a}φ2 ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ 1.8312862242e-10 · Λ^{2} · φ1 · φ1 ] +
√(-g) [ 5.2342251524e+08 · Λ^{-1} · φ2 · ∇^{a}φ2 · ∇_{a}φ2 ] +
√(-g) [ -3.7349210007e-07 · Λ^{-2} · φ1 · φ2 · ∇^{a}φ2 · ∇_{a}φ2 ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Term Metadata

```json
[
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
    "candidate": "φ1 · φ1",
    "mass_dim": 2,
    "lambda_power": 2,
    "sector": "scalar"
  },
  {
    "coeff_symbol": "\\gamma",
    "coeff_token": "COEFF_2",
    "candidate": "φ2 · ∇^{a}φ2 · ∇_{a}φ2",
    "mass_dim": 5,
    "lambda_power": -1,
    "sector": "scalar"
  },
  {
    "coeff_symbol": "\\delta",
    "coeff_token": "COEFF_3",
    "candidate": "φ1 · φ2 · ∇^{a}φ2 · ∇_{a}φ2",
    "mass_dim": 6,
    "lambda_power": -2,
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
  },
  {
    "coeff_symbol": "1",
    "coeff_token": "COEFF_FIXED_1",
    "candidate": "-½ g^{μν} ∇_μφ2 ∇_νφ2",
    "mass_dim": 4,
    "lambda_power": 0,
    "fixed": true,
    "sector": "matter"
  },
  {
    "coeff_symbol": "1",
    "coeff_token": "COEFF_FIXED_1",
    "candidate": "-½ m_2² φ2²",
    "mass_dim": 4,
    "lambda_power": 0,
    "fixed": true,
    "sector": "matter",
    "potential_type": "quadratic"
  }
]
```

### Effective Correction Diagnostics

```json
{
  "effective_correction_status": "eh_only",
  "effective_correction_reason": "no non-EH free correction terms",
  "max_relative_effect_to_EH": 0.0,
  "dominant_correction_term": "",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 0,
  "correction_term_count": 0,
  "tiny_correction_fraction": null,
  "term_effects": []
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000281_expanded_slot_06/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000281_expanded_slot_06/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000281_expanded_slot_06/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 13. task_000306_slot_08_lag_1  chi2=1642.062742

- scalar_config: `phi1_only`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: `523`
- H0_km_s_Mpc: `61.43425477`
- Omega_m0: `0.26600709`
- lambda_H_Lambda_over_H0: `3249.4423978`
- effective_correction_status: `eh_dominated`
- max_relative_effect_to_EH: `1.32591455e-07`
- dominant_correction_term: `∇^{c}R^{ab} · ∇_{c}R_{ab}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · ∇^{a}R · ∇_{a}R  +  \gamma Λ^{-4} · ∇^{c}R^{ab} · ∇_{c}R_{ab} )  +  \delta Λ^{2} · φ1 · φ1  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (1.3370460809e-05) Λ^{-4} · ∇^{a}R · ∇_{a}R  +  (7.3913013921e+06) Λ^{-4} · ∇^{c}R^{ab} · ∇_{c}R_{ab} )  +  (1.8490253450e-10) Λ^{2} · φ1 · φ1  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · ∇^{a}R · ∇_{a}R ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · ∇^{c}R^{ab} · ∇_{c}R_{ab} ) ] +
√(-g) [ \delta · Λ^{2} · φ1 · φ1 ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 1.3370460809e-05 · Λ^{-4} · ∇^{a}R · ∇_{a}R ) ] +
√(-g) [ M_p² ( 7.3913013921e+06 · Λ^{-4} · ∇^{c}R^{ab} · ∇_{c}R_{ab} ) ] +
√(-g) [ 1.8490253450e-10 · Λ^{2} · φ1 · φ1 ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ]
```

### Term Metadata

```json
[
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
    "candidate": "∇^{a}R · ∇_{a}R",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\gamma",
    "coeff_token": "COEFF_2",
    "candidate": "∇^{c}R^{ab} · ∇_{c}R_{ab}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\delta",
    "coeff_token": "COEFF_3",
    "candidate": "φ1 · φ1",
    "mass_dim": 2,
    "lambda_power": 2,
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
]
```

### Effective Correction Diagnostics

```json
{
  "effective_correction_status": "eh_dominated",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 1.3259145502154096e-07,
  "dominant_correction_term": "∇^{c}R^{ab} · ∇_{c}R_{ab}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 2,
  "correction_term_count": 2,
  "tiny_correction_fraction": 1.0,
  "term_effects": [
    {
      "candidate": "∇^{a}R · ∇_{a}R",
      "coeff_symbol": "\\beta",
      "coefficient": "1.3370460809348293e-05",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 2.398507054415298e-19,
      "effect_class": "tiny"
    },
    {
      "candidate": "∇^{c}R^{ab} · ∇_{c}R_{ab}",
      "coeff_symbol": "\\gamma",
      "coefficient": "7391301.392074293",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 1.3259145502154096e-07,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000306_slot_08/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000306_slot_08/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000306_slot_08/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 14. task_000094_expanded_slot_02_lag_1  chi2=1643.317532

- scalar_config: `both`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "axion", "phi2": "axion"}`
- agent_parameter_sample_index: `2678`
- H0_km_s_Mpc: `68.56236212`
- Omega_m0: `0.32067976`
- lambda_H_Lambda_over_H0: `1394.1606927`
- effective_correction_status: `eh_dominated`
- max_relative_effect_to_EH: `1.86543806e-08`
- dominant_correction_term: `R · R`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-2} · R · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-0.0181291109) Λ^{-2} · R · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-2} · R · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -0.0181291109 · Λ^{-2} · R · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Term Metadata

```json
[
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
    "candidate": "-m_1² f_1² (1 - cos(φ1/f_1))",
    "mass_dim": 4,
    "lambda_power": 0,
    "fixed": true,
    "sector": "matter",
    "potential_type": "axion"
  },
  {
    "coeff_symbol": "1",
    "coeff_token": "COEFF_FIXED_1",
    "candidate": "-½ g^{μν} ∇_μφ2 ∇_νφ2",
    "mass_dim": 4,
    "lambda_power": 0,
    "fixed": true,
    "sector": "matter"
  },
  {
    "coeff_symbol": "1",
    "coeff_token": "COEFF_FIXED_1",
    "candidate": "-m_2² f_2² (1 - cos(φ2/f_2))",
    "mass_dim": 4,
    "lambda_power": 0,
    "fixed": true,
    "sector": "matter",
    "potential_type": "axion"
  }
]
```

### Effective Correction Diagnostics

```json
{
  "effective_correction_status": "eh_dominated",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 1.865438059852336e-08,
  "dominant_correction_term": "R · R",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 1,
  "correction_term_count": 1,
  "tiny_correction_fraction": 1.0,
  "term_effects": [
    {
      "candidate": "R · R",
      "coeff_symbol": "\\beta",
      "coefficient": "-0.018129110895346263",
      "lambda_power": -2,
      "sector": "gravity",
      "relative_effect_to_EH": 1.865438059852336e-08,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000094_expanded_slot_02/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000094_expanded_slot_02/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000094_expanded_slot_02/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 15. task_000052_slot_05_lag_1  chi2=1644.846792

- scalar_config: `both`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "axion", "phi2": "axion"}`
- agent_parameter_sample_index: `643`
- H0_km_s_Mpc: `69.41175201`
- Omega_m0: `0.32175516`
- lambda_H_Lambda_over_H0: `1475.62038229`
- effective_correction_status: `eh_only`
- max_relative_effect_to_EH: `0`
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Term Metadata

```json
[
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
    "candidate": "-m_1² f_1² (1 - cos(φ1/f_1))",
    "mass_dim": 4,
    "lambda_power": 0,
    "fixed": true,
    "sector": "matter",
    "potential_type": "axion"
  },
  {
    "coeff_symbol": "1",
    "coeff_token": "COEFF_FIXED_1",
    "candidate": "-½ g^{μν} ∇_μφ2 ∇_νφ2",
    "mass_dim": 4,
    "lambda_power": 0,
    "fixed": true,
    "sector": "matter"
  },
  {
    "coeff_symbol": "1",
    "coeff_token": "COEFF_FIXED_1",
    "candidate": "-m_2² f_2² (1 - cos(φ2/f_2))",
    "mass_dim": 4,
    "lambda_power": 0,
    "fixed": true,
    "sector": "matter",
    "potential_type": "axion"
  }
]
```

### Effective Correction Diagnostics

```json
{
  "effective_correction_status": "eh_only",
  "effective_correction_reason": "no non-EH free correction terms",
  "max_relative_effect_to_EH": 0.0,
  "dominant_correction_term": "",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 0,
  "correction_term_count": 0,
  "tiny_correction_fraction": null,
  "term_effects": []
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000052_slot_05/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000052_slot_05/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000052_slot_05/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 16. task_000027_slot_01_lag_1  chi2=1655.498369

- scalar_config: `phi1_only`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "axion", "phi2": null}`
- agent_parameter_sample_index: `504`
- H0_km_s_Mpc: `73.19085008`
- Omega_m0: `0.33535141`
- lambda_H_Lambda_over_H0: `1487.83575661`
- effective_correction_status: `eh_dominated`
- max_relative_effect_to_EH: `1.11755905e-07`
- dominant_correction_term: `φ1 · R^{bcd}_{a} · R^{a}_{bcd}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (18.7529654121) Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 18.7529654121 · Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Term Metadata

```json
[
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
    "candidate": "φ1 · R^{bcd}_{a} · R^{a}_{bcd}",
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
    "candidate": "-m_1² f_1² (1 - cos(φ1/f_1))",
    "mass_dim": 4,
    "lambda_power": 0,
    "fixed": true,
    "sector": "matter",
    "potential_type": "axion"
  }
]
```

### Effective Correction Diagnostics

```json
{
  "effective_correction_status": "eh_dominated",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 1.1175590522398844e-07,
  "dominant_correction_term": "φ1 · R^{bcd}_{a} · R^{a}_{bcd}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 1,
  "correction_term_count": 1,
  "tiny_correction_fraction": 1.0,
  "term_effects": [
    {
      "candidate": "φ1 · R^{bcd}_{a} · R^{a}_{bcd}",
      "coeff_symbol": "\\beta",
      "coefficient": "18.7529654121078",
      "lambda_power": -3,
      "sector": "non-minimal",
      "relative_effect_to_EH": 1.1175590522398844e-07,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000027_slot_01/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000027_slot_01/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000027_slot_01/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 17. task_000034_slot_04_lag_1  chi2=1655.49837

- scalar_config: `both`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "axion", "phi2": "quadratic"}`
- agent_parameter_sample_index: `1`
- H0_km_s_Mpc: `73.19085008`
- Omega_m0: `0.33535141`
- lambda_H_Lambda_over_H0: `1487.83575661`
- effective_correction_status: `eh_dominated`
- max_relative_effect_to_EH: `5.95937244e-13`
- dominant_correction_term: `φ1 · R^{bcd}_{a} · R^{a}_{bcd}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-1.0000000000e-04) Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -1.0000000000e-04 · Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Term Metadata

```json
[
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
    "candidate": "φ1 · R^{bcd}_{a} · R^{a}_{bcd}",
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
    "candidate": "-m_1² f_1² (1 - cos(φ1/f_1))",
    "mass_dim": 4,
    "lambda_power": 0,
    "fixed": true,
    "sector": "matter",
    "potential_type": "axion"
  },
  {
    "coeff_symbol": "1",
    "coeff_token": "COEFF_FIXED_1",
    "candidate": "-½ g^{μν} ∇_μφ2 ∇_νφ2",
    "mass_dim": 4,
    "lambda_power": 0,
    "fixed": true,
    "sector": "matter"
  },
  {
    "coeff_symbol": "1",
    "coeff_token": "COEFF_FIXED_1",
    "candidate": "-½ m_2² φ2²",
    "mass_dim": 4,
    "lambda_power": 0,
    "fixed": true,
    "sector": "matter",
    "potential_type": "quadratic"
  }
]
```

### Effective Correction Diagnostics

```json
{
  "effective_correction_status": "eh_dominated",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 5.95937243886951e-13,
  "dominant_correction_term": "φ1 · R^{bcd}_{a} · R^{a}_{bcd}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 1,
  "correction_term_count": 1,
  "tiny_correction_fraction": 1.0,
  "term_effects": [
    {
      "candidate": "φ1 · R^{bcd}_{a} · R^{a}_{bcd}",
      "coeff_symbol": "\\beta",
      "coefficient": "-0.0001",
      "lambda_power": -3,
      "sector": "non-minimal",
      "relative_effect_to_EH": 5.95937243886951e-13,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000034_slot_04/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000034_slot_04/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000034_slot_04/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 18. task_000016_slot_01_lag_1  chi2=2460.440124

- scalar_config: `both`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "axion", "phi2": "quadratic"}`
- agent_parameter_sample_index: `872`
- H0_km_s_Mpc: `70.10058317`
- Omega_m0: `0.37166786`
- lambda_H_Lambda_over_H0: `6.60812372e+04`
- effective_correction_status: `eh_only`
- max_relative_effect_to_EH: `0`
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Term Metadata

```json
[
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
    "candidate": "-m_1² f_1² (1 - cos(φ1/f_1))",
    "mass_dim": 4,
    "lambda_power": 0,
    "fixed": true,
    "sector": "matter",
    "potential_type": "axion"
  },
  {
    "coeff_symbol": "1",
    "coeff_token": "COEFF_FIXED_1",
    "candidate": "-½ g^{μν} ∇_μφ2 ∇_νφ2",
    "mass_dim": 4,
    "lambda_power": 0,
    "fixed": true,
    "sector": "matter"
  },
  {
    "coeff_symbol": "1",
    "coeff_token": "COEFF_FIXED_1",
    "candidate": "-½ m_2² φ2²",
    "mass_dim": 4,
    "lambda_power": 0,
    "fixed": true,
    "sector": "matter",
    "potential_type": "quadratic"
  }
]
```

### Effective Correction Diagnostics

```json
{
  "effective_correction_status": "eh_only",
  "effective_correction_reason": "no non-EH free correction terms",
  "max_relative_effect_to_EH": 0.0,
  "dominant_correction_term": "",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 0,
  "correction_term_count": 0,
  "tiny_correction_fraction": null,
  "term_effects": []
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000016_slot_01/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000016_slot_01/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000016_slot_01/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 19. task_000002_slot_02_lag_1  chi2=4024.068817

- scalar_config: `both`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "quadratic", "phi2": "axion"}`
- agent_parameter_sample_index: `886`
- H0_km_s_Mpc: `69.73655496`
- Omega_m0: `0.25543082`
- lambda_H_Lambda_over_H0: `854.7110482`
- effective_correction_status: `moderate`
- max_relative_effect_to_EH: `1.02461210e-04`
- dominant_correction_term: `∇^{a}φ1 · ∇^{b}φ2 · R_{ab}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · φ2 · ∇^{a}∇_{a}φ2 · R  +  \gamma Λ^{-4} · ∇^{a}∇_{a}φ1 · φ2 · R  +  \delta Λ^{-4} · ∇^{a}φ1 · ∇^{b}φ2 · R_{ab} )  +  \epsilon Λ^{-1} · φ2 · φ2 · φ2 · φ2 · φ2  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (2.4121452055e+08) Λ^{-4} · φ2 · ∇^{a}∇_{a}φ2 · R  +  (9.5417011933e+08) Λ^{-4} · ∇^{a}∇_{a}φ1 · φ2 · R  +  (-1.0181179880e+10) Λ^{-4} · ∇^{a}φ1 · ∇^{b}φ2 · R_{ab} )  +  (4.4085818941e-05) Λ^{-1} · φ2 · φ2 · φ2 · φ2 · φ2  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · φ2 · ∇^{a}∇_{a}φ2 · R ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · ∇^{a}∇_{a}φ1 · φ2 · R ) ] +
√(-g) [ M_p² ( \delta · Λ^{-4} · ∇^{a}φ1 · ∇^{b}φ2 · R_{ab} ) ] +
√(-g) [ \epsilon · Λ^{-1} · φ2 · φ2 · φ2 · φ2 · φ2 ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 2.4121452055e+08 · Λ^{-4} · φ2 · ∇^{a}∇_{a}φ2 · R ) ] +
√(-g) [ M_p² ( 9.5417011933e+08 · Λ^{-4} · ∇^{a}∇_{a}φ1 · φ2 · R ) ] +
√(-g) [ M_p² ( -1.0181179880e+10 · Λ^{-4} · ∇^{a}φ1 · ∇^{b}φ2 · R_{ab} ) ] +
√(-g) [ 4.4085818941e-05 · Λ^{-1} · φ2 · φ2 · φ2 · φ2 · φ2 ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Term Metadata

```json
[
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
    "candidate": "φ2 · ∇^{a}∇_{a}φ2 · R",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\gamma",
    "coeff_token": "COEFF_2",
    "candidate": "∇^{a}∇_{a}φ1 · φ2 · R",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\delta",
    "coeff_token": "COEFF_3",
    "candidate": "∇^{a}φ1 · ∇^{b}φ2 · R_{ab}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\epsilon",
    "coeff_token": "COEFF_4",
    "candidate": "φ2 · φ2 · φ2 · φ2 · φ2",
    "mass_dim": 5,
    "lambda_power": -1,
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
  },
  {
    "coeff_symbol": "1",
    "coeff_token": "COEFF_FIXED_1",
    "candidate": "-½ g^{μν} ∇_μφ2 ∇_νφ2",
    "mass_dim": 4,
    "lambda_power": 0,
    "fixed": true,
    "sector": "matter"
  },
  {
    "coeff_symbol": "1",
    "coeff_token": "COEFF_FIXED_1",
    "candidate": "-m_2² f_2² (1 - cos(φ2/f_2))",
    "mass_dim": 4,
    "lambda_power": 0,
    "fixed": true,
    "sector": "matter",
    "potential_type": "axion"
  }
]
```

### Effective Correction Diagnostics

```json
{
  "effective_correction_status": "moderate",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 0.00010246120989400175,
  "dominant_correction_term": "∇^{a}φ1 · ∇^{b}φ2 · R_{ab}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 1,
  "weak_correction_terms": 2,
  "tiny_correction_terms": 0,
  "correction_term_count": 3,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "φ2 · ∇^{a}∇_{a}φ2 · R",
      "coeff_symbol": "\\beta",
      "coefficient": "241214520.5519264",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 4.814556015220937e-05,
      "effect_class": "weak"
    },
    {
      "candidate": "∇^{a}∇_{a}φ1 · φ2 · R",
      "coeff_symbol": "\\gamma",
      "coefficient": "954170119.3301673",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 9.602563359199054e-06,
      "effect_class": "weak"
    },
    {
      "candidate": "∇^{a}φ1 · ∇^{b}φ2 · R_{ab}",
      "coeff_symbol": "\\delta",
      "coefficient": "-10181179880.226019",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 0.00010246120989400175,
      "effect_class": "moderate"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000002_slot_02/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000002_slot_02/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000002_slot_02/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 20. task_000145_slot_02_lag_1  chi2=9434.002767

- scalar_config: `phi2_only`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": null, "phi2": "axion"}`
- agent_parameter_sample_index: `669`
- H0_km_s_Mpc: `63.64797328`
- Omega_m0: `0.30504951`
- lambda_H_Lambda_over_H0: `1665.32803996`
- effective_correction_status: `eh_dominated`
- max_relative_effect_to_EH: `8.91038356e-10`
- dominant_correction_term: `φ2 · R`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-1} · φ2 · R )  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (0.0430002354) Λ^{-1} · φ2 · R )  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-1} · φ2 · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 0.0430002354 · Λ^{-1} · φ2 · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Term Metadata

```json
[
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
    "candidate": "φ2 · R",
    "mass_dim": 3,
    "lambda_power": -1,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "1",
    "coeff_token": "COEFF_FIXED_1",
    "candidate": "-½ g^{μν} ∇_μφ2 ∇_νφ2",
    "mass_dim": 4,
    "lambda_power": 0,
    "fixed": true,
    "sector": "matter"
  },
  {
    "coeff_symbol": "1",
    "coeff_token": "COEFF_FIXED_1",
    "candidate": "-m_2² f_2² (1 - cos(φ2/f_2))",
    "mass_dim": 4,
    "lambda_power": 0,
    "fixed": true,
    "sector": "matter",
    "potential_type": "axion"
  }
]
```

### Effective Correction Diagnostics

```json
{
  "effective_correction_status": "eh_dominated",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 8.910383558778898e-10,
  "dominant_correction_term": "φ2 · R",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 1,
  "correction_term_count": 1,
  "tiny_correction_fraction": 1.0,
  "term_effects": [
    {
      "candidate": "φ2 · R",
      "coeff_symbol": "\\beta",
      "coefficient": "0.043000235352152937",
      "lambda_power": -1,
      "sector": "non-minimal",
      "relative_effect_to_EH": 8.910383558778898e-10,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000145_slot_02/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000145_slot_02/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000145_slot_02/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 21. task_000062_slot_05_lag_1  chi2=9434.0031

- scalar_config: `phi2_only`
- proposal_group: `non_eh`
- theory_track: `non_eh`
- potential_types: `{"phi1": null, "phi2": "axion"}`
- agent_parameter_sample_index: `524`
- H0_km_s_Mpc: `62.47746455`
- Omega_m0: `0.30854204`
- lambda_H_Lambda_over_H0: `824.25820341`
- effective_correction_status: `unclear`
- max_relative_effect_to_EH: ``
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha Λ^{-2} · R · R  +  \beta Λ^{-4} · ∇^{a}∇^{b}R · R_{ab}  +  \gamma Λ^{-1} · φ2 · R  +  \delta Λ^{-4} · φ2 · ∇^{a}φ2 · ∇_{a}R  +  \epsilon Λ^{-4} · ∇^{a}φ2 · ∇^{b}φ2 · R_{ab} )  +  \zeta Λ^{1} · φ2 · φ2 · φ2  +  \eta Λ^{-1} · φ2 · ∇^{a}φ2 · ∇_{a}φ2  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (3.9619395776e+05) Λ^{-2} · R · R  +  (-8.3906608190e+08) Λ^{-4} · ∇^{a}∇^{b}R · R_{ab}  +  (0.1977402047) Λ^{-1} · φ2 · R  +  (-3.8307407422e-06) Λ^{-4} · φ2 · ∇^{a}φ2 · ∇_{a}R  +  (1.7830155089e+09) Λ^{-4} · ∇^{a}φ2 · ∇^{b}φ2 · R_{ab} )  +  (-1.9626372606e+16) Λ^{1} · φ2 · φ2 · φ2  +  (8.3500307616e-10) Λ^{-1} · φ2 · ∇^{a}φ2 · ∇_{a}φ2  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · Λ^{-2} · R · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · ∇^{a}∇^{b}R · R_{ab} ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-1} · φ2 · R ) ] +
√(-g) [ M_p² ( \delta · Λ^{-4} · φ2 · ∇^{a}φ2 · ∇_{a}R ) ] +
√(-g) [ M_p² ( \epsilon · Λ^{-4} · ∇^{a}φ2 · ∇^{b}φ2 · R_{ab} ) ] +
√(-g) [ \zeta · Λ^{1} · φ2 · φ2 · φ2 ] +
√(-g) [ \eta · Λ^{-1} · φ2 · ∇^{a}φ2 · ∇_{a}φ2 ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 3.9619395776e+05 · Λ^{-2} · R · R ) ] +
√(-g) [ M_p² ( -8.3906608190e+08 · Λ^{-4} · ∇^{a}∇^{b}R · R_{ab} ) ] +
√(-g) [ M_p² ( 0.1977402047 · Λ^{-1} · φ2 · R ) ] +
√(-g) [ M_p² ( -3.8307407422e-06 · Λ^{-4} · φ2 · ∇^{a}φ2 · ∇_{a}R ) ] +
√(-g) [ M_p² ( 1.7830155089e+09 · Λ^{-4} · ∇^{a}φ2 · ∇^{b}φ2 · R_{ab} ) ] +
√(-g) [ -1.9626372606e+16 · Λ^{1} · φ2 · φ2 · φ2 ] +
√(-g) [ 8.3500307616e-10 · Λ^{-1} · φ2 · ∇^{a}φ2 · ∇_{a}φ2 ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Term Metadata

```json
[
  {
    "coeff_symbol": "\\alpha",
    "coeff_token": "COEFF_0",
    "candidate": "R · R",
    "mass_dim": 4,
    "lambda_power": -2,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\beta",
    "coeff_token": "COEFF_1",
    "candidate": "∇^{a}∇^{b}R · R_{ab}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\gamma",
    "coeff_token": "COEFF_2",
    "candidate": "φ2 · R",
    "mass_dim": 3,
    "lambda_power": -1,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\delta",
    "coeff_token": "COEFF_3",
    "candidate": "φ2 · ∇^{a}φ2 · ∇_{a}R",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\epsilon",
    "coeff_token": "COEFF_4",
    "candidate": "∇^{a}φ2 · ∇^{b}φ2 · R_{ab}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\zeta",
    "coeff_token": "COEFF_5",
    "candidate": "φ2 · φ2 · φ2",
    "mass_dim": 3,
    "lambda_power": 1,
    "sector": "scalar"
  },
  {
    "coeff_symbol": "\\eta",
    "coeff_token": "COEFF_6",
    "candidate": "φ2 · ∇^{a}φ2 · ∇_{a}φ2",
    "mass_dim": 5,
    "lambda_power": -1,
    "sector": "scalar"
  },
  {
    "coeff_symbol": "1",
    "coeff_token": "COEFF_FIXED_1",
    "candidate": "-½ g^{μν} ∇_μφ2 ∇_νφ2",
    "mass_dim": 4,
    "lambda_power": 0,
    "fixed": true,
    "sector": "matter"
  },
  {
    "coeff_symbol": "1",
    "coeff_token": "COEFF_FIXED_1",
    "candidate": "-m_2² f_2² (1 - cos(φ2/f_2))",
    "mass_dim": 4,
    "lambda_power": 0,
    "fixed": true,
    "sector": "matter",
    "potential_type": "axion"
  }
]
```

### Effective Correction Diagnostics

```json
{
  "effective_correction_status": "unclear",
  "effective_correction_reason": "missing EH R reference term",
  "max_relative_effect_to_EH": null,
  "dominant_correction_term": "",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 0,
  "correction_term_count": 0,
  "tiny_correction_fraction": null,
  "term_effects": []
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000062_slot_05/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000062_slot_05/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000062_slot_05/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 22. task_000178_slot_02_lag_1  chi2=9434.003103

- scalar_config: `phi2_only`
- proposal_group: `non_eh`
- theory_track: `non_eh`
- potential_types: `{"phi1": null, "phi2": "axion"}`
- agent_parameter_sample_index: `806`
- H0_km_s_Mpc: `64.50577829`
- Omega_m0: `0.30032759`
- lambda_H_Lambda_over_H0: `1719.87559409`
- effective_correction_status: `unclear`
- max_relative_effect_to_EH: ``
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha Λ^{-1} · φ2 · R )  +  \beta Λ^{2} · φ2 · φ2  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.1912800509) Λ^{-1} · φ2 · R )  +  (3.3519477777e+15) Λ^{2} · φ2 · φ2  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · Λ^{-1} · φ2 · R ) ] +
√(-g) [ \beta · Λ^{2} · φ2 · φ2 ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.1912800509 · Λ^{-1} · φ2 · R ) ] +
√(-g) [ 3.3519477777e+15 · Λ^{2} · φ2 · φ2 ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Term Metadata

```json
[
  {
    "coeff_symbol": "\\alpha",
    "coeff_token": "COEFF_0",
    "candidate": "φ2 · R",
    "mass_dim": 3,
    "lambda_power": -1,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\beta",
    "coeff_token": "COEFF_1",
    "candidate": "φ2 · φ2",
    "mass_dim": 2,
    "lambda_power": 2,
    "sector": "scalar"
  },
  {
    "coeff_symbol": "1",
    "coeff_token": "COEFF_FIXED_1",
    "candidate": "-½ g^{μν} ∇_μφ2 ∇_νφ2",
    "mass_dim": 4,
    "lambda_power": 0,
    "fixed": true,
    "sector": "matter"
  },
  {
    "coeff_symbol": "1",
    "coeff_token": "COEFF_FIXED_1",
    "candidate": "-m_2² f_2² (1 - cos(φ2/f_2))",
    "mass_dim": 4,
    "lambda_power": 0,
    "fixed": true,
    "sector": "matter",
    "potential_type": "axion"
  }
]
```

### Effective Correction Diagnostics

```json
{
  "effective_correction_status": "unclear",
  "effective_correction_reason": "missing EH R reference term",
  "max_relative_effect_to_EH": null,
  "dominant_correction_term": "",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 0,
  "correction_term_count": 0,
  "tiny_correction_fraction": null,
  "term_effects": []
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000178_slot_02/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000178_slot_02/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000178_slot_02/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 23. task_000277_slot_08_lag_1  chi2=9434.003114

- scalar_config: `phi2_only`
- proposal_group: `non_eh`
- theory_track: `non_eh`
- potential_types: `{"phi1": null, "phi2": "quadratic"}`
- agent_parameter_sample_index: `684`
- H0_km_s_Mpc: `70.64941355`
- Omega_m0: `0.27242964`
- lambda_H_Lambda_over_H0: `3394.4207629`
- effective_correction_status: `unclear`
- max_relative_effect_to_EH: ``
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha Λ^{-4} · R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh}  +  \beta Λ^{-4} · ∇^{c}R^{ab} · ∇_{c}R_{ab}  +  \gamma Λ^{-4} · ∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}  +  \delta Λ^{-1} · φ2 · R  +  \epsilon Λ^{-3} · ∇^{a}∇^{b}φ2 · R_{ab}  +  \zeta Λ^{-4} · φ2 · ∇^{a}∇_{a}φ2 · R )  +  \eta Λ^{1} · φ2 · φ2 · φ2  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (1.2710595472e+11) Λ^{-4} · R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh}  +  (1.2123738594e+07) Λ^{-4} · ∇^{c}R^{ab} · ∇_{c}R_{ab}  +  (-6.2433407425e+04) Λ^{-4} · ∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}  +  (-0.1780434295) Λ^{-1} · φ2 · R  +  (9.5361434833e-05) Λ^{-3} · ∇^{a}∇^{b}φ2 · R_{ab}  +  (-2.0247480853e+07) Λ^{-4} · φ2 · ∇^{a}∇_{a}φ2 · R )  +  (2.4478668317e+17) Λ^{1} · φ2 · φ2 · φ2  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · Λ^{-4} · R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh} ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · ∇^{c}R^{ab} · ∇_{c}R_{ab} ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · ∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( \delta · Λ^{-1} · φ2 · R ) ] +
√(-g) [ M_p² ( \epsilon · Λ^{-3} · ∇^{a}∇^{b}φ2 · R_{ab} ) ] +
√(-g) [ M_p² ( \zeta · Λ^{-4} · φ2 · ∇^{a}∇_{a}φ2 · R ) ] +
√(-g) [ \eta · Λ^{1} · φ2 · φ2 · φ2 ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 1.2710595472e+11 · Λ^{-4} · R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh} ) ] +
√(-g) [ M_p² ( 1.2123738594e+07 · Λ^{-4} · ∇^{c}R^{ab} · ∇_{c}R_{ab} ) ] +
√(-g) [ M_p² ( -6.2433407425e+04 · Λ^{-4} · ∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( -0.1780434295 · Λ^{-1} · φ2 · R ) ] +
√(-g) [ M_p² ( 9.5361434833e-05 · Λ^{-3} · ∇^{a}∇^{b}φ2 · R_{ab} ) ] +
√(-g) [ M_p² ( -2.0247480853e+07 · Λ^{-4} · φ2 · ∇^{a}∇_{a}φ2 · R ) ] +
√(-g) [ 2.4478668317e+17 · Λ^{1} · φ2 · φ2 · φ2 ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Term Metadata

```json
[
  {
    "coeff_symbol": "\\alpha",
    "coeff_token": "COEFF_0",
    "candidate": "R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\beta",
    "coeff_token": "COEFF_1",
    "candidate": "∇^{c}R^{ab} · ∇_{c}R_{ab}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\gamma",
    "coeff_token": "COEFF_2",
    "candidate": "∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\delta",
    "coeff_token": "COEFF_3",
    "candidate": "φ2 · R",
    "mass_dim": 3,
    "lambda_power": -1,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\epsilon",
    "coeff_token": "COEFF_4",
    "candidate": "∇^{a}∇^{b}φ2 · R_{ab}",
    "mass_dim": 5,
    "lambda_power": -3,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\zeta",
    "coeff_token": "COEFF_5",
    "candidate": "φ2 · ∇^{a}∇_{a}φ2 · R",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\eta",
    "coeff_token": "COEFF_6",
    "candidate": "φ2 · φ2 · φ2",
    "mass_dim": 3,
    "lambda_power": 1,
    "sector": "scalar"
  },
  {
    "coeff_symbol": "1",
    "coeff_token": "COEFF_FIXED_1",
    "candidate": "-½ g^{μν} ∇_μφ2 ∇_νφ2",
    "mass_dim": 4,
    "lambda_power": 0,
    "fixed": true,
    "sector": "matter"
  },
  {
    "coeff_symbol": "1",
    "coeff_token": "COEFF_FIXED_1",
    "candidate": "-½ m_2² φ2²",
    "mass_dim": 4,
    "lambda_power": 0,
    "fixed": true,
    "sector": "matter",
    "potential_type": "quadratic"
  }
]
```

### Effective Correction Diagnostics

```json
{
  "effective_correction_status": "unclear",
  "effective_correction_reason": "missing EH R reference term",
  "max_relative_effect_to_EH": null,
  "dominant_correction_term": "",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 0,
  "correction_term_count": 0,
  "tiny_correction_fraction": null,
  "term_effects": []
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000277_slot_08/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000277_slot_08/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000277_slot_08/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 24. task_000026_slot_04_lag_1  chi2=9434.003135

- scalar_config: `phi2_only`
- proposal_group: `non_eh`
- theory_track: `non_eh`
- potential_types: `{"phi1": null, "phi2": "quadratic"}`
- agent_parameter_sample_index: `915`
- H0_km_s_Mpc: `73.26811495`
- Omega_m0: `0.32877543`
- lambda_H_Lambda_over_H0: `1610.26770014`
- effective_correction_status: `unclear`
- max_relative_effect_to_EH: ``
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha Λ^{-1} · φ2 · R )  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (-0.0203643928) Λ^{-1} · φ2 · R )  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · Λ^{-1} · φ2 · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( -0.0203643928 · Λ^{-1} · φ2 · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Term Metadata

```json
[
  {
    "coeff_symbol": "\\alpha",
    "coeff_token": "COEFF_0",
    "candidate": "φ2 · R",
    "mass_dim": 3,
    "lambda_power": -1,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "1",
    "coeff_token": "COEFF_FIXED_1",
    "candidate": "-½ g^{μν} ∇_μφ2 ∇_νφ2",
    "mass_dim": 4,
    "lambda_power": 0,
    "fixed": true,
    "sector": "matter"
  },
  {
    "coeff_symbol": "1",
    "coeff_token": "COEFF_FIXED_1",
    "candidate": "-½ m_2² φ2²",
    "mass_dim": 4,
    "lambda_power": 0,
    "fixed": true,
    "sector": "matter",
    "potential_type": "quadratic"
  }
]
```

### Effective Correction Diagnostics

```json
{
  "effective_correction_status": "unclear",
  "effective_correction_reason": "missing EH R reference term",
  "max_relative_effect_to_EH": null,
  "dominant_correction_term": "",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 0,
  "correction_term_count": 0,
  "tiny_correction_fraction": null,
  "term_effects": []
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000026_slot_04/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000026_slot_04/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000026_slot_04/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 25. task_000275_slot_03_lag_1  chi2=9434.006612

- scalar_config: `both`
- proposal_group: `non_eh`
- theory_track: `non_eh`
- potential_types: `{"phi1": "quadratic", "phi2": "quadratic"}`
- agent_parameter_sample_index: `783`
- H0_km_s_Mpc: `70.0184052`
- Omega_m0: `0.29279024`
- lambda_H_Lambda_over_H0: `4534.60004226`
- effective_correction_status: `unclear`
- max_relative_effect_to_EH: ``
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha Λ^{-1} · φ2 · R )  +  \beta Λ^{-1} · φ2 · ∇^{a}φ2 · ∇_{a}φ2  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (-1561.1549994888) Λ^{-1} · φ2 · R )  +  (1662.4485654267) Λ^{-1} · φ2 · ∇^{a}φ2 · ∇_{a}φ2  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · Λ^{-1} · φ2 · R ) ] +
√(-g) [ \beta · Λ^{-1} · φ2 · ∇^{a}φ2 · ∇_{a}φ2 ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( -1561.1549994888 · Λ^{-1} · φ2 · R ) ] +
√(-g) [ 1662.4485654267 · Λ^{-1} · φ2 · ∇^{a}φ2 · ∇_{a}φ2 ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Term Metadata

```json
[
  {
    "coeff_symbol": "\\alpha",
    "coeff_token": "COEFF_0",
    "candidate": "φ2 · R",
    "mass_dim": 3,
    "lambda_power": -1,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\beta",
    "coeff_token": "COEFF_1",
    "candidate": "φ2 · ∇^{a}φ2 · ∇_{a}φ2",
    "mass_dim": 5,
    "lambda_power": -1,
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
  },
  {
    "coeff_symbol": "1",
    "coeff_token": "COEFF_FIXED_1",
    "candidate": "-½ g^{μν} ∇_μφ2 ∇_νφ2",
    "mass_dim": 4,
    "lambda_power": 0,
    "fixed": true,
    "sector": "matter"
  },
  {
    "coeff_symbol": "1",
    "coeff_token": "COEFF_FIXED_1",
    "candidate": "-½ m_2² φ2²",
    "mass_dim": 4,
    "lambda_power": 0,
    "fixed": true,
    "sector": "matter",
    "potential_type": "quadratic"
  }
]
```

### Effective Correction Diagnostics

```json
{
  "effective_correction_status": "unclear",
  "effective_correction_reason": "missing EH R reference term",
  "max_relative_effect_to_EH": null,
  "dominant_correction_term": "",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 0,
  "correction_term_count": 0,
  "tiny_correction_fraction": null,
  "term_effects": []
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000275_slot_03/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000275_slot_03/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000275_slot_03/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 26. task_000181_slot_07_lag_1  chi2=9434.007467

- scalar_config: `phi2_only`
- proposal_group: `non_eh`
- theory_track: `non_eh`
- potential_types: `{"phi1": null, "phi2": "axion"}`
- agent_parameter_sample_index: `617`
- H0_km_s_Mpc: `63.94205093`
- Omega_m0: `0.30229341`
- lambda_H_Lambda_over_H0: `2480.92266061`
- effective_correction_status: `unclear`
- max_relative_effect_to_EH: ``
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha Λ^{-3} · φ2 · φ2 · φ2 · R  +  \beta Λ^{-3} · ∇^{a}φ2 · ∇_{a}R  +  \gamma Λ^{-4} · φ2 · φ2 · φ2 · φ2 · R )  +  \delta Λ^{2} · φ2 · φ2  +  \epsilon Λ^{1} · φ2 · φ2 · φ2  +  \zeta Λ^{1} · ∇^{a}∇_{a}φ2  +  \eta Λ^{-1} · φ2 · φ2 · ∇^{a}∇_{a}φ2  +  \theta Λ^{-2} · φ2 · φ2 · ∇^{a}φ2 · ∇_{a}φ2  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (-3.1779510651e+13) Λ^{-3} · φ2 · φ2 · φ2 · R  +  (0.0152101558) Λ^{-3} · ∇^{a}φ2 · ∇_{a}R  +  (4.7830040327e-06) Λ^{-4} · φ2 · φ2 · φ2 · φ2 · R )  +  (-0.0116130113) Λ^{2} · φ2 · φ2  +  (1.7643847544e+07) Λ^{1} · φ2 · φ2 · φ2  +  (2.1951598720e+12) Λ^{1} · ∇^{a}∇_{a}φ2  +  (2.4910900738e+19) Λ^{-1} · φ2 · φ2 · ∇^{a}∇_{a}φ2  +  (-2.5446467593e+16) Λ^{-2} · φ2 · φ2 · ∇^{a}φ2 · ∇_{a}φ2  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · Λ^{-3} · φ2 · φ2 · φ2 · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-3} · ∇^{a}φ2 · ∇_{a}R ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · φ2 · φ2 · φ2 · φ2 · R ) ] +
√(-g) [ \delta · Λ^{2} · φ2 · φ2 ] +
√(-g) [ \epsilon · Λ^{1} · φ2 · φ2 · φ2 ] +
√(-g) [ \zeta · Λ^{1} · ∇^{a}∇_{a}φ2 ] +
√(-g) [ \eta · Λ^{-1} · φ2 · φ2 · ∇^{a}∇_{a}φ2 ] +
√(-g) [ \theta · Λ^{-2} · φ2 · φ2 · ∇^{a}φ2 · ∇_{a}φ2 ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( -3.1779510651e+13 · Λ^{-3} · φ2 · φ2 · φ2 · R ) ] +
√(-g) [ M_p² ( 0.0152101558 · Λ^{-3} · ∇^{a}φ2 · ∇_{a}R ) ] +
√(-g) [ M_p² ( 4.7830040327e-06 · Λ^{-4} · φ2 · φ2 · φ2 · φ2 · R ) ] +
√(-g) [ -0.0116130113 · Λ^{2} · φ2 · φ2 ] +
√(-g) [ 1.7643847544e+07 · Λ^{1} · φ2 · φ2 · φ2 ] +
√(-g) [ 2.1951598720e+12 · Λ^{1} · ∇^{a}∇_{a}φ2 ] +
√(-g) [ 2.4910900738e+19 · Λ^{-1} · φ2 · φ2 · ∇^{a}∇_{a}φ2 ] +
√(-g) [ -2.5446467593e+16 · Λ^{-2} · φ2 · φ2 · ∇^{a}φ2 · ∇_{a}φ2 ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Term Metadata

```json
[
  {
    "coeff_symbol": "\\alpha",
    "coeff_token": "COEFF_0",
    "candidate": "φ2 · φ2 · φ2 · R",
    "mass_dim": 5,
    "lambda_power": -3,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\beta",
    "coeff_token": "COEFF_1",
    "candidate": "∇^{a}φ2 · ∇_{a}R",
    "mass_dim": 5,
    "lambda_power": -3,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\gamma",
    "coeff_token": "COEFF_2",
    "candidate": "φ2 · φ2 · φ2 · φ2 · R",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\delta",
    "coeff_token": "COEFF_3",
    "candidate": "φ2 · φ2",
    "mass_dim": 2,
    "lambda_power": 2,
    "sector": "scalar"
  },
  {
    "coeff_symbol": "\\epsilon",
    "coeff_token": "COEFF_4",
    "candidate": "φ2 · φ2 · φ2",
    "mass_dim": 3,
    "lambda_power": 1,
    "sector": "scalar"
  },
  {
    "coeff_symbol": "\\zeta",
    "coeff_token": "COEFF_5",
    "candidate": "∇^{a}∇_{a}φ2",
    "mass_dim": 3,
    "lambda_power": 1,
    "sector": "scalar"
  },
  {
    "coeff_symbol": "\\eta",
    "coeff_token": "COEFF_6",
    "candidate": "φ2 · φ2 · ∇^{a}∇_{a}φ2",
    "mass_dim": 5,
    "lambda_power": -1,
    "sector": "scalar"
  },
  {
    "coeff_symbol": "\\theta",
    "coeff_token": "COEFF_7",
    "candidate": "φ2 · φ2 · ∇^{a}φ2 · ∇_{a}φ2",
    "mass_dim": 6,
    "lambda_power": -2,
    "sector": "scalar"
  },
  {
    "coeff_symbol": "1",
    "coeff_token": "COEFF_FIXED_1",
    "candidate": "-½ g^{μν} ∇_μφ2 ∇_νφ2",
    "mass_dim": 4,
    "lambda_power": 0,
    "fixed": true,
    "sector": "matter"
  },
  {
    "coeff_symbol": "1",
    "coeff_token": "COEFF_FIXED_1",
    "candidate": "-m_2² f_2² (1 - cos(φ2/f_2))",
    "mass_dim": 4,
    "lambda_power": 0,
    "fixed": true,
    "sector": "matter",
    "potential_type": "axion"
  }
]
```

### Effective Correction Diagnostics

```json
{
  "effective_correction_status": "unclear",
  "effective_correction_reason": "missing EH R reference term",
  "max_relative_effect_to_EH": null,
  "dominant_correction_term": "",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 0,
  "correction_term_count": 0,
  "tiny_correction_fraction": null,
  "term_effects": []
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000181_slot_07/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000181_slot_07/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000181_slot_07/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 27. task_000260_slot_01_lag_1  chi2=9434.007547

- scalar_config: `both`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "quadratic", "phi2": "axion"}`
- agent_parameter_sample_index: `273`
- H0_km_s_Mpc: `58.7053187`
- Omega_m0: `0.29811965`
- lambda_H_Lambda_over_H0: `7880.60131939`
- effective_correction_status: `active`
- max_relative_effect_to_EH: `365.43517143`
- dominant_correction_term: `φ2 · φ2 · R^{ab} · R_{ab}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd}  +  \gamma Λ^{-2} · φ2 · φ2 · R  +  \delta Λ^{-4} · φ2 · φ2 · R^{ab} · R_{ab} )  +  \epsilon Λ^{1} · φ1 · φ2 · φ2  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (1.4610369646e-08) Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd}  +  (1.3964439639e-04) Λ^{-2} · φ2 · φ2 · R  +  (-5.8647215670e+14) Λ^{-4} · φ2 · φ2 · R^{ab} · R_{ab} )  +  (11.9722324676) Λ^{1} · φ1 · φ2 · φ2  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-2} · φ2 · φ2 · R ) ] +
√(-g) [ M_p² ( \delta · Λ^{-4} · φ2 · φ2 · R^{ab} · R_{ab} ) ] +
√(-g) [ \epsilon · Λ^{1} · φ1 · φ2 · φ2 ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 1.4610369646e-08 · Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( 1.3964439639e-04 · Λ^{-2} · φ2 · φ2 · R ) ] +
√(-g) [ M_p² ( -5.8647215670e+14 · Λ^{-4} · φ2 · φ2 · R^{ab} · R_{ab} ) ] +
√(-g) [ 11.9722324676 · Λ^{1} · φ1 · φ2 · φ2 ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Term Metadata

```json
[
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
    "candidate": "R^{bcd}_{a} · R^{a}_{bcd}",
    "mass_dim": 4,
    "lambda_power": -2,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\gamma",
    "coeff_token": "COEFF_2",
    "candidate": "φ2 · φ2 · R",
    "mass_dim": 4,
    "lambda_power": -2,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\delta",
    "coeff_token": "COEFF_3",
    "candidate": "φ2 · φ2 · R^{ab} · R_{ab}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\epsilon",
    "coeff_token": "COEFF_4",
    "candidate": "φ1 · φ2 · φ2",
    "mass_dim": 3,
    "lambda_power": 1,
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
  },
  {
    "coeff_symbol": "1",
    "coeff_token": "COEFF_FIXED_1",
    "candidate": "-½ g^{μν} ∇_μφ2 ∇_νφ2",
    "mass_dim": 4,
    "lambda_power": 0,
    "fixed": true,
    "sector": "matter"
  },
  {
    "coeff_symbol": "1",
    "coeff_token": "COEFF_FIXED_1",
    "candidate": "-m_2² f_2² (1 - cos(φ2/f_2))",
    "mass_dim": 4,
    "lambda_power": 0,
    "fixed": true,
    "sector": "matter",
    "potential_type": "axion"
  }
]
```

### Effective Correction Diagnostics

```json
{
  "effective_correction_status": "active",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 365.435171432826,
  "dominant_correction_term": "φ2 · φ2 · R^{ab} · R_{ab}",
  "active_correction_terms": 1,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 2,
  "correction_term_count": 3,
  "tiny_correction_fraction": 0.6666666666666666,
  "term_effects": [
    {
      "candidate": "R^{bcd}_{a} · R^{a}_{bcd}",
      "coeff_symbol": "\\beta",
      "coefficient": "1.4610369645881249e-08",
      "lambda_power": -2,
      "sector": "gravity",
      "relative_effect_to_EH": 4.705139297306315e-16,
      "effect_class": "tiny"
    },
    {
      "candidate": "φ2 · φ2 · R",
      "coeff_symbol": "\\gamma",
      "coefficient": "0.00013964439638564452",
      "lambda_power": -2,
      "sector": "non-minimal",
      "relative_effect_to_EH": 5.403873483224279e-09,
      "effect_class": "tiny"
    },
    {
      "candidate": "φ2 · φ2 · R^{ab} · R_{ab}",
      "coeff_symbol": "\\delta",
      "coefficient": "-586472156698046.0",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 365.435171432826,
      "effect_class": "active"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000260_slot_01/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000260_slot_01/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000260_slot_01/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 28. task_000291_slot_01_lag_1  chi2=9434.007596

- scalar_config: `phi2_only`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": null, "phi2": "quadratic"}`
- agent_parameter_sample_index: `582`
- H0_km_s_Mpc: `69.15312397`
- Omega_m0: `0.26941368`
- lambda_H_Lambda_over_H0: `6063.5654051`
- effective_correction_status: `eh_dominated`
- max_relative_effect_to_EH: `3.61554563e-10`
- dominant_correction_term: `φ2 · φ2 · R`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-2} · φ2 · φ2 · R )  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (3.2919930649e+07) Λ^{-2} · φ2 · φ2 · R )  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-2} · φ2 · φ2 · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 3.2919930649e+07 · Λ^{-2} · φ2 · φ2 · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Term Metadata

```json
[
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
    "candidate": "φ2 · φ2 · R",
    "mass_dim": 4,
    "lambda_power": -2,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "1",
    "coeff_token": "COEFF_FIXED_1",
    "candidate": "-½ g^{μν} ∇_μφ2 ∇_νφ2",
    "mass_dim": 4,
    "lambda_power": 0,
    "fixed": true,
    "sector": "matter"
  },
  {
    "coeff_symbol": "1",
    "coeff_token": "COEFF_FIXED_1",
    "candidate": "-½ m_2² φ2²",
    "mass_dim": 4,
    "lambda_power": 0,
    "fixed": true,
    "sector": "matter",
    "potential_type": "quadratic"
  }
]
```

### Effective Correction Diagnostics

```json
{
  "effective_correction_status": "eh_dominated",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 3.61554563097415e-10,
  "dominant_correction_term": "φ2 · φ2 · R",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 1,
  "correction_term_count": 1,
  "tiny_correction_fraction": 1.0,
  "term_effects": [
    {
      "candidate": "φ2 · φ2 · R",
      "coeff_symbol": "\\beta",
      "coefficient": "32919930.6494137",
      "lambda_power": -2,
      "sector": "non-minimal",
      "relative_effect_to_EH": 3.61554563097415e-10,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000291_slot_01/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000291_slot_01/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_312_sector_async_v6_task_000291_slot_01/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`
