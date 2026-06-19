# Accepted Lagrangians Full

Complete dimension-balanced Lagrangians, best-fit coefficient substitutions, metadata, and Solver paths.
Only the best chi-square representative from each accepted theory family is shown for human inspection.
The full accepted-attempt list is preserved in `accepted_summary.json`.

## 1. task_000313_expanded_refine_slot_01_lag_1  chi2=1637.959888

- best_validation_stage: `refine`
- validation_stage_counts: `{"refine": 1, "initial": 1, "expanded": 1}`
- family_accepted_records: `3`
- delta_chi2_vs_LCDM: `-7.3201124`
- delta_AIC_vs_LCDM: `-1.3201124`
- delta_BIC_vs_LCDM: `15.22585233`
- scalar_config: `phi1_only`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "axion", "phi2": null}`
- agent_parameter_sample_index: `537`
- H0_km_s_Mpc: `63.31187027`
- Omega_m0: `0.27576975`
- lambda_H_Lambda_over_H0: `6380.43818399`
- effective_correction_status: `weak`
- max_relative_effect_to_EH: `9.77418690e-05`
- dominant_correction_term: `R^{b}_{a} · R^{cd} · R^{a}_{cbd}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · R · R^{ab} · R_{ab}  +  \gamma Λ^{-4} · R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh}  +  \delta Λ^{-4} · R^{b}_{a} · R^{cd} · R^{a}_{cbd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (4.2911517491e+10) Λ^{-4} · R · R^{ab} · R_{ab}  +  (-2.9217173990e+09) Λ^{-4} · R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh}  +  (8.0993965989e+10) Λ^{-4} · R^{b}_{a} · R^{cd} · R^{a}_{cbd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · R · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh} ) ] +
√(-g) [ M_p² ( \delta · Λ^{-4} · R^{b}_{a} · R^{cd} · R^{a}_{cbd} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 4.2911517491e+10 · Λ^{-4} · R · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( -2.9217173990e+09 · Λ^{-4} · R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh} ) ] +
√(-g) [ M_p² ( 8.0993965989e+10 · Λ^{-4} · R^{b}_{a} · R^{cd} · R^{a}_{cbd} ) ] +
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
    "candidate": "R · R^{ab} · R_{ab}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\gamma",
    "coeff_token": "COEFF_2",
    "candidate": "R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\delta",
    "coeff_token": "COEFF_3",
    "candidate": "R^{b}_{a} · R^{cd} · R^{a}_{cbd}",
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
  "effective_correction_status": "weak",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 9.774186901584253e-05,
  "dominant_correction_term": "R^{b}_{a} · R^{cd} · R^{a}_{cbd}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 3,
  "tiny_correction_terms": 0,
  "correction_term_count": 3,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "R · R^{ab} · R_{ab}",
      "coeff_symbol": "\\beta",
      "coefficient": "42911517491.29559",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 5.1784745575528986e-05,
      "effect_class": "weak"
    },
    {
      "candidate": "R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh}",
      "coeff_symbol": "\\gamma",
      "coefficient": "-2921717398.9952545",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 3.5258690672325013e-06,
      "effect_class": "weak"
    },
    {
      "candidate": "R^{b}_{a} · R^{cd} · R^{a}_{cbd}",
      "coeff_symbol": "\\delta",
      "coefficient": "80993965989.22858",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 9.774186901584253e-05,
      "effect_class": "weak"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000313_expanded_refine_slot_01/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000313_expanded_refine_slot_01/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000313_expanded_refine_slot_01/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 2. task_000398_slot_12_lag_1  chi2=1637.959888

- best_validation_stage: `initial`
- validation_stage_counts: `{"initial": 1, "expanded": 1, "refine": 1}`
- family_accepted_records: `3`
- delta_chi2_vs_LCDM: `-7.3201124`
- delta_AIC_vs_LCDM: `-1.3201124`
- delta_BIC_vs_LCDM: `15.22585233`
- scalar_config: `phi1_only`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "axion", "phi2": null}`
- agent_parameter_sample_index: `1`
- H0_km_s_Mpc: `63.31187027`
- Omega_m0: `0.27576975`
- lambda_H_Lambda_over_H0: `6380.43818399`
- effective_correction_status: `weak`
- max_relative_effect_to_EH: `2.51188643e-06`
- dominant_correction_term: `φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-9.4102236300e+08) Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -9.4102236300e+08 · Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
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
    "candidate": "φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd}",
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
  "max_relative_effect_to_EH": 2.5118864315095823e-06,
  "dominant_correction_term": "φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 1,
  "tiny_correction_terms": 0,
  "correction_term_count": 1,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd}",
      "coeff_symbol": "\\beta",
      "coefficient": "-941022362.9954636",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 2.5118864315095823e-06,
      "effect_class": "weak"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000398_slot_12/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000398_slot_12/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000398_slot_12/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 3. task_000444_slot_01_lag_1  chi2=1637.959888

- best_validation_stage: `initial`
- validation_stage_counts: `{"initial": 1, "expanded": 1, "refine": 1}`
- family_accepted_records: `3`
- delta_chi2_vs_LCDM: `-7.3201124`
- delta_AIC_vs_LCDM: `-1.3201124`
- delta_BIC_vs_LCDM: `15.22585233`
- scalar_config: `phi1_only`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "axion", "phi2": null}`
- agent_parameter_sample_index: `1`
- H0_km_s_Mpc: `63.31187027`
- Omega_m0: `0.27576975`
- lambda_H_Lambda_over_H0: `6380.43818399`
- effective_correction_status: `weak`
- max_relative_effect_to_EH: `3.98107171e-05`
- dominant_correction_term: `R_{ab} · R^{adef} · R^{b}_{def}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · R · R · R  +  \gamma Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-2.0814789634e+09) Λ^{-4} · R · R · R  +  (3.2989218394e+10) Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · R · R · R ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -2.0814789634e+09 · Λ^{-4} · R · R · R ) ] +
√(-g) [ M_p² ( 3.2989218394e+10 · Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def} ) ] +
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
    "candidate": "R · R · R",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\gamma",
    "coeff_token": "COEFF_2",
    "candidate": "R_{ab} · R^{adef} · R^{b}_{def}",
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
  "effective_correction_status": "weak",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 3.9810717055349695e-05,
  "dominant_correction_term": "R_{ab} · R^{adef} · R^{b}_{def}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 2,
  "tiny_correction_terms": 0,
  "correction_term_count": 2,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "R · R · R",
      "coeff_symbol": "\\beta",
      "coefficient": "-2081478963.426778",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 2.5118864315095823e-06,
      "effect_class": "weak"
    },
    {
      "candidate": "R_{ab} · R^{adef} · R^{b}_{def}",
      "coeff_symbol": "\\gamma",
      "coefficient": "32989218393.861103",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 3.9810717055349695e-05,
      "effect_class": "weak"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000444_slot_01/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000444_slot_01/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000444_slot_01/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 4. task_000448_slot_05_lag_1  chi2=1637.959888

- best_validation_stage: `initial`
- validation_stage_counts: `{"initial": 1, "expanded": 1, "refine": 1}`
- family_accepted_records: `3`
- delta_chi2_vs_LCDM: `-7.3201124`
- delta_AIC_vs_LCDM: `-1.3201124`
- delta_BIC_vs_LCDM: `15.22585233`
- scalar_config: `phi1_only`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "axion", "phi2": null}`
- agent_parameter_sample_index: `1`
- H0_km_s_Mpc: `63.31187027`
- Omega_m0: `0.27576975`
- lambda_H_Lambda_over_H0: `6380.43818399`
- effective_correction_status: `weak`
- max_relative_effect_to_EH: `2.51188643e-06`
- dominant_correction_term: `R · R^{ab} · R_{ab}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · R · R^{ab} · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-2.0814789634e+09) Λ^{-4} · R · R^{ab} · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · R · R^{ab} · R_{ab} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -2.0814789634e+09 · Λ^{-4} · R · R^{ab} · R_{ab} ) ] +
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
    "candidate": "R · R^{ab} · R_{ab}",
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
  "effective_correction_status": "weak",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 2.5118864315095823e-06,
  "dominant_correction_term": "R · R^{ab} · R_{ab}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 1,
  "tiny_correction_terms": 0,
  "correction_term_count": 1,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "R · R^{ab} · R_{ab}",
      "coeff_symbol": "\\beta",
      "coefficient": "-2081478963.426778",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 2.5118864315095823e-06,
      "effect_class": "weak"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000448_slot_05/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000448_slot_05/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000448_slot_05/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 5. task_000504_slot_05_lag_1  chi2=1637.959888

- best_validation_stage: `initial`
- validation_stage_counts: `{"initial": 1, "expanded": 1, "refine": 1}`
- family_accepted_records: `3`
- delta_chi2_vs_LCDM: `-7.3201124`
- delta_AIC_vs_LCDM: `-1.3201124`
- delta_BIC_vs_LCDM: `15.22585233`
- scalar_config: `phi1_only`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "axion", "phi2": null}`
- agent_parameter_sample_index: `1`
- H0_km_s_Mpc: `63.31187027`
- Omega_m0: `0.27576975`
- lambda_H_Lambda_over_H0: `6380.43818399`
- effective_correction_status: `weak`
- max_relative_effect_to_EH: `2.51188643e-06`
- dominant_correction_term: `R_{ab} · R^{adef} · R^{b}_{def}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-2.0814789634e+09) Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -2.0814789634e+09 · Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def} ) ] +
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
    "candidate": "R_{ab} · R^{adef} · R^{b}_{def}",
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
  "effective_correction_status": "weak",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 2.5118864315095823e-06,
  "dominant_correction_term": "R_{ab} · R^{adef} · R^{b}_{def}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 1,
  "tiny_correction_terms": 0,
  "correction_term_count": 1,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "R_{ab} · R^{adef} · R^{b}_{def}",
      "coeff_symbol": "\\beta",
      "coefficient": "-2081478963.426778",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 2.5118864315095823e-06,
      "effect_class": "weak"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000504_slot_05/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000504_slot_05/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000504_slot_05/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 6. task_000536_slot_03_lag_1  chi2=1637.959888

- best_validation_stage: `initial`
- validation_stage_counts: `{"initial": 1, "expanded": 1, "refine": 1}`
- family_accepted_records: `3`
- delta_chi2_vs_LCDM: `-7.3201124`
- delta_AIC_vs_LCDM: `-1.3201124`
- delta_BIC_vs_LCDM: `15.22585233`
- scalar_config: `phi1_only`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "axion", "phi2": null}`
- agent_parameter_sample_index: `1`
- H0_km_s_Mpc: `63.31187027`
- Omega_m0: `0.27576975`
- lambda_H_Lambda_over_H0: `6380.43818399`
- effective_correction_status: `weak`
- max_relative_effect_to_EH: `2.51188643e-06`
- dominant_correction_term: `R · R`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-2} · R · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-51.129437537) Λ^{-2} · R · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-2} · R · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -51.129437537 · Λ^{-2} · R · R ) ] +
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
  "max_relative_effect_to_EH": 2.5118864315095823e-06,
  "dominant_correction_term": "R · R",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 1,
  "tiny_correction_terms": 0,
  "correction_term_count": 1,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "R · R",
      "coeff_symbol": "\\beta",
      "coefficient": "-51.12943753702144",
      "lambda_power": -2,
      "sector": "gravity",
      "relative_effect_to_EH": 2.5118864315095823e-06,
      "effect_class": "weak"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000536_slot_03/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000536_slot_03/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000536_slot_03/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 7. task_000600_slot_10_lag_1  chi2=1637.959888

- best_validation_stage: `initial`
- validation_stage_counts: `{"initial": 1, "expanded": 1, "refine": 1}`
- family_accepted_records: `3`
- delta_chi2_vs_LCDM: `-7.3201124`
- delta_AIC_vs_LCDM: `-1.3201124`
- delta_BIC_vs_LCDM: `15.22585233`
- scalar_config: `phi1_only`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "axion", "phi2": null}`
- agent_parameter_sample_index: `1`
- H0_km_s_Mpc: `63.31187027`
- Omega_m0: `0.27576975`
- lambda_H_Lambda_over_H0: `6380.43818399`
- effective_correction_status: `weak`
- max_relative_effect_to_EH: `3.98107171e-05`
- dominant_correction_term: `∇^{a}∇_{a}R`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd}  +  \gamma Λ^{-2} · ∇^{a}∇_{a}R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-51.129437537) Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd}  +  (810.3469748679) Λ^{-2} · ∇^{a}∇_{a}R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-2} · ∇^{a}∇_{a}R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -51.129437537 · Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( 810.3469748679 · Λ^{-2} · ∇^{a}∇_{a}R ) ] +
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
    "candidate": "R^{bcd}_{a} · R^{a}_{bcd}",
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
  "max_relative_effect_to_EH": 3.9810717055349695e-05,
  "dominant_correction_term": "∇^{a}∇_{a}R",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 2,
  "tiny_correction_terms": 0,
  "correction_term_count": 2,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "R^{bcd}_{a} · R^{a}_{bcd}",
      "coeff_symbol": "\\beta",
      "coefficient": "-51.12943753702144",
      "lambda_power": -2,
      "sector": "gravity",
      "relative_effect_to_EH": 2.5118864315095823e-06,
      "effect_class": "weak"
    },
    {
      "candidate": "∇^{a}∇_{a}R",
      "coeff_symbol": "\\gamma",
      "coefficient": "810.3469748679087",
      "lambda_power": -2,
      "sector": "gravity",
      "relative_effect_to_EH": 3.9810717055349695e-05,
      "effect_class": "weak"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000600_slot_10/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000600_slot_10/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000600_slot_10/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 8. task_000511_slot_13_lag_1  chi2=1637.964818

- best_validation_stage: `initial`
- validation_stage_counts: `{"initial": 7, "expanded": 7, "refine": 2}`
- family_accepted_records: `16`
- delta_chi2_vs_LCDM: `-7.31518194`
- delta_AIC_vs_LCDM: `-1.31518194`
- delta_BIC_vs_LCDM: `15.2307828`
- scalar_config: `phi1_only`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "axion", "phi2": null}`
- agent_parameter_sample_index: `806`
- H0_km_s_Mpc: `61.3166919`
- Omega_m0: `0.28095783`
- lambda_H_Lambda_over_H0: `3301.8942931`
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000511_slot_13/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000511_slot_13/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000511_slot_13/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 9. task_000391_expanded_slot_02_lag_1  chi2=1637.972658

- best_validation_stage: `expanded`
- validation_stage_counts: `{"expanded": 1, "refine": 1, "initial": 1}`
- family_accepted_records: `3`
- delta_chi2_vs_LCDM: `-7.30734197`
- delta_AIC_vs_LCDM: `8.69265803`
- delta_BIC_vs_LCDM: `52.807169`
- scalar_config: `both`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "axion", "phi2": "axion"}`
- agent_parameter_sample_index: `1708`
- H0_km_s_Mpc: `66.32807774`
- Omega_m0: `0.28029337`
- lambda_H_Lambda_over_H0: `6397.71423116`
- effective_correction_status: `active`
- max_relative_effect_to_EH: `0.28061264`
- dominant_correction_term: `φ1 · φ2 · R · R`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · φ1 · φ2 · R · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-6.0147753212e+17) Λ^{-4} · φ1 · φ2 · R · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · φ1 · φ2 · R · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -6.0147753212e+17 · Λ^{-4} · φ1 · φ2 · R · R ) ] +
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
    "candidate": "φ1 · φ2 · R · R",
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
  "effective_correction_status": "active",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 0.28061263697297356,
  "dominant_correction_term": "φ1 · φ2 · R · R",
  "active_correction_terms": 1,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 0,
  "correction_term_count": 1,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "φ1 · φ2 · R · R",
      "coeff_symbol": "\\beta",
      "coefficient": "-6.01477532122797e+17",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 0.28061263697297356,
      "effect_class": "active"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000391_expanded_slot_02/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000391_expanded_slot_02/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000391_expanded_slot_02/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 10. task_000319_slot_08_lag_1  chi2=1637.977566

- best_validation_stage: `initial`
- validation_stage_counts: `{"initial": 1, "expanded": 1, "refine": 1}`
- family_accepted_records: `3`
- delta_chi2_vs_LCDM: `-7.30243419`
- delta_AIC_vs_LCDM: `-1.30243419`
- delta_BIC_vs_LCDM: `15.24353054`
- scalar_config: `phi1_only`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "axion", "phi2": null}`
- agent_parameter_sample_index: `196`
- H0_km_s_Mpc: `60.8058522`
- Omega_m0: `0.27946461`
- lambda_H_Lambda_over_H0: `6994.08731071`
- effective_correction_status: `eh_dominated`
- max_relative_effect_to_EH: `3.26121042e-10`
- dominant_correction_term: `R · R^{bcd}_{a} · R^{a}_{bcd}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · R · R^{ab} · R_{ab}  +  \gamma Λ^{-4} · R · R^{bcd}_{a} · R^{a}_{bcd}  +  \delta Λ^{-4} · ∇^{a}∇^{b}R · R_{ab}  +  \epsilon Λ^{-4} · ∇^{c}R^{ab} · ∇_{b}R_{ac} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-14.3658979563) Λ^{-4} · R · R^{ab} · R_{ab}  +  (-3.9018720469e+05) Λ^{-4} · R · R^{bcd}_{a} · R^{a}_{bcd}  +  (6.8686999586e-07) Λ^{-4} · ∇^{a}∇^{b}R · R_{ab}  +  (7.1176174350e-05) Λ^{-4} · ∇^{c}R^{ab} · ∇_{b}R_{ac} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · R · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · R · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( \delta · Λ^{-4} · ∇^{a}∇^{b}R · R_{ab} ) ] +
√(-g) [ M_p² ( \epsilon · Λ^{-4} · ∇^{c}R^{ab} · ∇_{b}R_{ac} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -14.3658979563 · Λ^{-4} · R · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( -3.9018720469e+05 · Λ^{-4} · R · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( 6.8686999586e-07 · Λ^{-4} · ∇^{a}∇^{b}R · R_{ab} ) ] +
√(-g) [ M_p² ( 7.1176174350e-05 · Λ^{-4} · ∇^{c}R^{ab} · ∇_{b}R_{ac} ) ] +
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
    "candidate": "R · R^{ab} · R_{ab}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\gamma",
    "coeff_token": "COEFF_2",
    "candidate": "R · R^{bcd}_{a} · R^{a}_{bcd}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\delta",
    "coeff_token": "COEFF_3",
    "candidate": "∇^{a}∇^{b}R · R_{ab}",
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
  "effective_correction_status": "eh_dominated",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 3.2612104190145004e-10,
  "dominant_correction_term": "R · R^{bcd}_{a} · R^{a}_{bcd}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 4,
  "correction_term_count": 4,
  "tiny_correction_fraction": 1.0,
  "term_effects": [
    {
      "candidate": "R · R^{ab} · R_{ab}",
      "coeff_symbol": "\\beta",
      "coefficient": "-14.365897956298898",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 1.2007112363159595e-14,
      "effect_class": "tiny"
    },
    {
      "candidate": "R · R^{bcd}_{a} · R^{a}_{bcd}",
      "coeff_symbol": "\\gamma",
      "coefficient": "-390187.20468817826",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 3.2612104190145004e-10,
      "effect_class": "tiny"
    },
    {
      "candidate": "∇^{a}∇^{b}R · R_{ab}",
      "coeff_symbol": "\\delta",
      "coefficient": "6.868699958598274e-07",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 5.740904776200067e-22,
      "effect_class": "tiny"
    },
    {
      "candidate": "∇^{c}R^{ab} · ∇_{b}R_{ac}",
      "coeff_symbol": "\\epsilon",
      "coefficient": "7.117617434997331e-05",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 5.948951646459726e-20,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000319_slot_08/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000319_slot_08/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000319_slot_08/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 11. task_000484_expanded_refine_slot_08_lag_1  chi2=1637.987078

- best_validation_stage: `refine`
- validation_stage_counts: `{"refine": 1, "initial": 1, "expanded": 1}`
- family_accepted_records: `3`
- delta_chi2_vs_LCDM: `-7.29292241`
- delta_AIC_vs_LCDM: `-1.29292241`
- delta_BIC_vs_LCDM: `15.25304233`
- scalar_config: `phi1_only`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "axion", "phi2": null}`
- agent_parameter_sample_index: `4654`
- H0_km_s_Mpc: `62.45020824`
- Omega_m0: `0.28284385`
- lambda_H_Lambda_over_H0: `6871.65882734`
- effective_correction_status: `weak`
- max_relative_effect_to_EH: `2.62239660e-05`
- dominant_correction_term: `R^{bcd}_{a} · R^{a}_{bcd}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-619.1438393348) Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -619.1438393348 · Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
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
    "candidate": "R^{bcd}_{a} · R^{a}_{bcd}",
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
  }
]
```

### Effective Correction Diagnostics

```json
{
  "effective_correction_status": "weak",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 2.622396603019838e-05,
  "dominant_correction_term": "R^{bcd}_{a} · R^{a}_{bcd}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 1,
  "tiny_correction_terms": 0,
  "correction_term_count": 1,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "R^{bcd}_{a} · R^{a}_{bcd}",
      "coeff_symbol": "\\beta",
      "coefficient": "-619.1438393348188",
      "lambda_power": -2,
      "sector": "gravity",
      "relative_effect_to_EH": 2.622396603019838e-05,
      "effect_class": "weak"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000484_expanded_refine_slot_08/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000484_expanded_refine_slot_08/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000484_expanded_refine_slot_08/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 12. task_000472_slot_09_lag_1  chi2=1637.991597

- best_validation_stage: `initial`
- validation_stage_counts: `{"initial": 1, "expanded": 1, "refine": 1}`
- family_accepted_records: `3`
- delta_chi2_vs_LCDM: `-7.28840295`
- delta_AIC_vs_LCDM: `-1.28840295`
- delta_BIC_vs_LCDM: `15.25756178`
- scalar_config: `phi1_only`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "axion", "phi2": null}`
- agent_parameter_sample_index: `577`
- H0_km_s_Mpc: `72.48923092`
- Omega_m0: `0.28031791`
- lambda_H_Lambda_over_H0: `1.46093308e+04`
- effective_correction_status: `moderate`
- max_relative_effect_to_EH: `0.00363596`
- dominant_correction_term: `R^{b}_{a} · R^{cd} · R^{a}_{cbd}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · R^{b}_{a} · R^{cd} · R^{a}_{cbd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (8.2815188514e+13) Λ^{-4} · R^{b}_{a} · R^{cd} · R^{a}_{cbd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · R^{b}_{a} · R^{cd} · R^{a}_{cbd} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 8.2815188514e+13 · Λ^{-4} · R^{b}_{a} · R^{cd} · R^{a}_{cbd} ) ] +
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
    "candidate": "R^{b}_{a} · R^{cd} · R^{a}_{cbd}",
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
  "max_relative_effect_to_EH": 0.0036359566647509046,
  "dominant_correction_term": "R^{b}_{a} · R^{cd} · R^{a}_{cbd}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 1,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 0,
  "correction_term_count": 1,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "R^{b}_{a} · R^{cd} · R^{a}_{cbd}",
      "coeff_symbol": "\\beta",
      "coefficient": "82815188513501.0",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 0.0036359566647509046,
      "effect_class": "moderate"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000472_slot_09/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000472_slot_09/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000472_slot_09/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 13. task_000263_expanded_slot_10_lag_1  chi2=1638.005237

- best_validation_stage: `expanded`
- validation_stage_counts: `{"expanded": 5, "initial": 6}`
- family_accepted_records: `11`
- delta_chi2_vs_LCDM: `-7.27476316`
- delta_AIC_vs_LCDM: `8.72523684`
- delta_BIC_vs_LCDM: `52.83974781`
- scalar_config: `both`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "axion", "phi2": "axion"}`
- agent_parameter_sample_index: `691`
- H0_km_s_Mpc: `71.8104283`
- Omega_m0: `0.27373238`
- lambda_H_Lambda_over_H0: `1700.54982518`
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000263_expanded_slot_10/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000263_expanded_slot_10/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000263_expanded_slot_10/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 14. task_000400_slot_16_lag_1  chi2=1638.005237

- best_validation_stage: `initial`
- validation_stage_counts: `{"initial": 1, "expanded": 1}`
- family_accepted_records: `2`
- delta_chi2_vs_LCDM: `-7.27476316`
- delta_AIC_vs_LCDM: `8.72523684`
- delta_BIC_vs_LCDM: `52.83974781`
- scalar_config: `both`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "axion", "phi2": "axion"}`
- agent_parameter_sample_index: `1`
- H0_km_s_Mpc: `71.8104283`
- Omega_m0: `0.27373238`
- lambda_H_Lambda_over_H0: `1700.54982518`
- effective_correction_status: `eh_dominated`
- max_relative_effect_to_EH: `2.39151193e-17`
- dominant_correction_term: `∇^{a}∇^{b}R · R_{ab}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · ∇^{a}∇^{b}R · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-1.0000000000e-04) Λ^{-4} · ∇^{a}∇^{b}R · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · ∇^{a}∇^{b}R · R_{ab} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -1.0000000000e-04 · Λ^{-4} · ∇^{a}∇^{b}R · R_{ab} ) ] +
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
    "candidate": "∇^{a}∇^{b}R · R_{ab}",
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
  "max_relative_effect_to_EH": 2.3915119289085725e-17,
  "dominant_correction_term": "∇^{a}∇^{b}R · R_{ab}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 1,
  "correction_term_count": 1,
  "tiny_correction_fraction": 1.0,
  "term_effects": [
    {
      "candidate": "∇^{a}∇^{b}R · R_{ab}",
      "coeff_symbol": "\\beta",
      "coefficient": "-0.0001",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 2.3915119289085725e-17,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000400_slot_16/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000400_slot_16/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000400_slot_16/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 15. task_000334_expanded_slot_03_lag_1  chi2=1638.024829

- best_validation_stage: `expanded`
- validation_stage_counts: `{"expanded": 5, "initial": 5}`
- family_accepted_records: `10`
- delta_chi2_vs_LCDM: `-7.25517104`
- delta_AIC_vs_LCDM: `6.74482896`
- delta_BIC_vs_LCDM: `45.34563069`
- scalar_config: `both`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "axion", "phi2": "quadratic"}`
- agent_parameter_sample_index: `2463`
- H0_km_s_Mpc: `58`
- Omega_m0: `0.27923064`
- lambda_H_Lambda_over_H0: `1034.73644085`
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000334_expanded_slot_03/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000334_expanded_slot_03/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000334_expanded_slot_03/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 16. task_000474_expanded_slot_14_lag_1  chi2=1638.028947

- best_validation_stage: `expanded`
- validation_stage_counts: `{"expanded": 5, "initial": 5}`
- family_accepted_records: `10`
- delta_chi2_vs_LCDM: `-7.25105291`
- delta_AIC_vs_LCDM: `6.74894709`
- delta_BIC_vs_LCDM: `45.34974882`
- scalar_config: `both`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "quadratic", "phi2": "axion"}`
- agent_parameter_sample_index: `1819`
- H0_km_s_Mpc: `59.05562565`
- Omega_m0: `0.27040674`
- lambda_H_Lambda_over_H0: `858.11620208`
- effective_correction_status: `eh_only`
- max_relative_effect_to_EH: `0`
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000474_expanded_slot_14/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000474_expanded_slot_14/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000474_expanded_slot_14/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 17. task_000242_expanded_slot_09_lag_1  chi2=1638.034284

- best_validation_stage: `expanded`
- validation_stage_counts: `{"expanded": 1, "initial": 1}`
- family_accepted_records: `2`
- delta_chi2_vs_LCDM: `-7.24571606`
- delta_AIC_vs_LCDM: `8.75428394`
- delta_BIC_vs_LCDM: `52.86879492`
- scalar_config: `both`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "axion", "phi2": "axion"}`
- agent_parameter_sample_index: `2951`
- H0_km_s_Mpc: `64.58939711`
- Omega_m0: `0.27067424`
- lambda_H_Lambda_over_H0: `4622.10177669`
- effective_correction_status: `eh_dominated`
- max_relative_effect_to_EH: `1.41480401e-19`
- dominant_correction_term: `R · R^{ab} · R_{ab}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · R · R^{ab} · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-3.2286747945e-05) Λ^{-4} · R · R^{ab} · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · R · R^{ab} · R_{ab} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -3.2286747945e-05 · Λ^{-4} · R · R^{ab} · R_{ab} ) ] +
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
    "candidate": "R · R^{ab} · R_{ab}",
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
  "max_relative_effect_to_EH": 1.414804009892768e-19,
  "dominant_correction_term": "R · R^{ab} · R_{ab}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 1,
  "correction_term_count": 1,
  "tiny_correction_fraction": 1.0,
  "term_effects": [
    {
      "candidate": "R · R^{ab} · R_{ab}",
      "coeff_symbol": "\\beta",
      "coefficient": "-3.2286747944654246e-05",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 1.414804009892768e-19,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000242_expanded_slot_09/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000242_expanded_slot_09/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000242_expanded_slot_09/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 18. task_000282_slot_14_lag_1  chi2=1638.034284

- best_validation_stage: `initial`
- validation_stage_counts: `{"initial": 1, "expanded": 1}`
- family_accepted_records: `2`
- delta_chi2_vs_LCDM: `-7.24571606`
- delta_AIC_vs_LCDM: `6.75428394`
- delta_BIC_vs_LCDM: `45.35508567`
- scalar_config: `both`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "axion", "phi2": "quadratic"}`
- agent_parameter_sample_index: `1`
- H0_km_s_Mpc: `64.58939711`
- Omega_m0: `0.27067424`
- lambda_H_Lambda_over_H0: `4622.10177669`
- effective_correction_status: `eh_dominated`
- max_relative_effect_to_EH: `9.36161954e-12`
- dominant_correction_term: `R^{ab} · R_{ab}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-2} · R^{ab} · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-1.0000000000e-04) Λ^{-2} · R^{ab} · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-2} · R^{ab} · R_{ab} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -1.0000000000e-04 · Λ^{-2} · R^{ab} · R_{ab} ) ] +
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
  "max_relative_effect_to_EH": 9.361619539277274e-12,
  "dominant_correction_term": "R^{ab} · R_{ab}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 1,
  "correction_term_count": 1,
  "tiny_correction_fraction": 1.0,
  "term_effects": [
    {
      "candidate": "R^{ab} · R_{ab}",
      "coeff_symbol": "\\beta",
      "coefficient": "-0.0001",
      "lambda_power": -2,
      "sector": "gravity",
      "relative_effect_to_EH": 9.361619539277274e-12,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000282_slot_14/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000282_slot_14/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000282_slot_14/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 19. task_000377_slot_14_lag_1  chi2=1638.034284

- best_validation_stage: `initial`
- validation_stage_counts: `{"initial": 1, "expanded": 1}`
- family_accepted_records: `2`
- delta_chi2_vs_LCDM: `-7.24571606`
- delta_AIC_vs_LCDM: `6.75428394`
- delta_BIC_vs_LCDM: `45.35508567`
- scalar_config: `both`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "axion", "phi2": "quadratic"}`
- agent_parameter_sample_index: `1`
- H0_km_s_Mpc: `64.58939711`
- Omega_m0: `0.27067424`
- lambda_H_Lambda_over_H0: `4622.10177669`
- effective_correction_status: `eh_dominated`
- max_relative_effect_to_EH: `4.38199602e-19`
- dominant_correction_term: `R · R^{ab} · R_{ab}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · R · R^{ab} · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-1.0000000000e-04) Λ^{-4} · R · R^{ab} · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · R · R^{ab} · R_{ab} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -1.0000000000e-04 · Λ^{-4} · R · R^{ab} · R_{ab} ) ] +
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
    "candidate": "R · R^{ab} · R_{ab}",
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
  "max_relative_effect_to_EH": 4.381996019908901e-19,
  "dominant_correction_term": "R · R^{ab} · R_{ab}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 1,
  "correction_term_count": 1,
  "tiny_correction_fraction": 1.0,
  "term_effects": [
    {
      "candidate": "R · R^{ab} · R_{ab}",
      "coeff_symbol": "\\beta",
      "coefficient": "-0.0001",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 4.381996019908901e-19,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000377_slot_14/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000377_slot_14/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000377_slot_14/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 20. task_000154_slot_07_lag_1  chi2=1638.092992

- best_validation_stage: `initial`
- validation_stage_counts: `{"initial": 1, "expanded": 1}`
- family_accepted_records: `2`
- delta_chi2_vs_LCDM: `-7.18700784`
- delta_AIC_vs_LCDM: `-1.18700784`
- delta_BIC_vs_LCDM: `15.35895689`
- scalar_config: `phi1_only`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "axion", "phi2": null}`
- agent_parameter_sample_index: `574`
- H0_km_s_Mpc: `58.9134907`
- Omega_m0: `0.30325602`
- lambda_H_Lambda_over_H0: `2581.6590916`
- effective_correction_status: `active`
- max_relative_effect_to_EH: `2.98061606e+08`
- dominant_correction_term: `φ1 · R^{bcd}_{a} · R^{a}_{bcd}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · R · R^{ab} · R_{ab}  +  \gamma Λ^{-4} · R · R^{bcd}_{a} · R^{a}_{bcd}  +  \delta Λ^{-4} · ∇^{a}∇^{b}R · R_{ab}  +  \epsilon Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd}  +  \zeta Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-7.9630243857e+11) Λ^{-4} · R · R^{ab} · R_{ab}  +  (237.4722557953) Λ^{-4} · R · R^{bcd}_{a} · R^{a}_{bcd}  +  (4.4512084263e+14) Λ^{-4} · ∇^{a}∇^{b}R · R_{ab}  +  (1.7940005745e+18) Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd}  +  (5.4395413977e+11) Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · R · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · R · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( \delta · Λ^{-4} · ∇^{a}∇^{b}R · R_{ab} ) ] +
√(-g) [ M_p² ( \epsilon · Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( \zeta · Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -7.9630243857e+11 · Λ^{-4} · R · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( 237.4722557953 · Λ^{-4} · R · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( 4.4512084263e+14 · Λ^{-4} · ∇^{a}∇^{b}R · R_{ab} ) ] +
√(-g) [ M_p² ( 1.7940005745e+18 · Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( 5.4395413977e+11 · Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
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
    "candidate": "R · R^{ab} · R_{ab}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\gamma",
    "coeff_token": "COEFF_2",
    "candidate": "R · R^{bcd}_{a} · R^{a}_{bcd}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\delta",
    "coeff_token": "COEFF_3",
    "candidate": "∇^{a}∇^{b}R · R_{ab}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\epsilon",
    "coeff_token": "COEFF_4",
    "candidate": "φ1 · R^{bcd}_{a} · R^{a}_{bcd}",
    "mass_dim": 5,
    "lambda_power": -3,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\zeta",
    "coeff_token": "COEFF_5",
    "candidate": "φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd}",
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
  "max_relative_effect_to_EH": 298061606.2101402,
  "dominant_correction_term": "φ1 · R^{bcd}_{a} · R^{a}_{bcd}",
  "active_correction_terms": 4,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 1,
  "correction_term_count": 5,
  "tiny_correction_fraction": 0.2,
  "term_effects": [
    {
      "candidate": "R · R^{ab} · R_{ab}",
      "coeff_symbol": "\\beta",
      "coefficient": "-796302438568.8721",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 0.035851924159361566,
      "effect_class": "active"
    },
    {
      "candidate": "R · R^{bcd}_{a} · R^{a}_{bcd}",
      "coeff_symbol": "\\gamma",
      "coefficient": "237.4722557953268",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 1.0691713213923816e-11,
      "effect_class": "tiny"
    },
    {
      "candidate": "∇^{a}∇^{b}R · R_{ab}",
      "coeff_symbol": "\\delta",
      "coefficient": "445120842633193.6",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 20.040675400312907,
      "effect_class": "active"
    },
    {
      "candidate": "φ1 · R^{bcd}_{a} · R^{a}_{bcd}",
      "coeff_symbol": "\\epsilon",
      "coefficient": "1.7940005744553172e+18",
      "lambda_power": -3,
      "sector": "non-minimal",
      "relative_effect_to_EH": 298061606.2101402,
      "effect_class": "active"
    },
    {
      "candidate": "φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd}",
      "coeff_symbol": "\\zeta",
      "coefficient": "543954139771.1596",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 0.05003766050521473,
      "effect_class": "active"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000154_slot_07/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000154_slot_07/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000154_slot_07/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 21. task_000198_slot_02_lag_1  chi2=1638.160165

- best_validation_stage: `initial`
- validation_stage_counts: `{"initial": 1, "expanded": 1}`
- family_accepted_records: `2`
- delta_chi2_vs_LCDM: `-7.11983528`
- delta_AIC_vs_LCDM: `6.88016472`
- delta_BIC_vs_LCDM: `45.48096645`
- scalar_config: `both`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "quadratic", "phi2": "axion"}`
- agent_parameter_sample_index: `1`
- H0_km_s_Mpc: `59.66609063`
- Omega_m0: `0.26872797`
- lambda_H_Lambda_over_H0: `1599.64064583`
- effective_correction_status: `eh_dominated`
- max_relative_effect_to_EH: `6.42426541e-19`
- dominant_correction_term: `φ2 · R^{ab} · R_{ab}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-3} · φ2 · R^{ab} · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-1.0000000000e-04) Λ^{-3} · φ2 · R^{ab} · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-3} · φ2 · R^{ab} · R_{ab} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -1.0000000000e-04 · Λ^{-3} · φ2 · R^{ab} · R_{ab} ) ] +
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
    "candidate": "φ2 · R^{ab} · R_{ab}",
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
  "max_relative_effect_to_EH": 6.424265406086272e-19,
  "dominant_correction_term": "φ2 · R^{ab} · R_{ab}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 1,
  "correction_term_count": 1,
  "tiny_correction_fraction": 1.0,
  "term_effects": [
    {
      "candidate": "φ2 · R^{ab} · R_{ab}",
      "coeff_symbol": "\\beta",
      "coefficient": "-0.0001",
      "lambda_power": -3,
      "sector": "non-minimal",
      "relative_effect_to_EH": 6.424265406086272e-19,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000198_slot_02/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000198_slot_02/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000198_slot_02/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 22. task_000299_slot_08_lag_1  chi2=1638.160165

- best_validation_stage: `initial`
- validation_stage_counts: `{"initial": 1, "expanded": 1}`
- family_accepted_records: `2`
- delta_chi2_vs_LCDM: `-7.11983528`
- delta_AIC_vs_LCDM: `6.88016472`
- delta_BIC_vs_LCDM: `45.48096645`
- scalar_config: `both`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "quadratic", "phi2": "axion"}`
- agent_parameter_sample_index: `13`
- H0_km_s_Mpc: `59.66609063`
- Omega_m0: `0.26872797`
- lambda_H_Lambda_over_H0: `1599.64064583`
- effective_correction_status: `moderate`
- max_relative_effect_to_EH: `0.00331514`
- dominant_correction_term: `φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-3.1622776602e+09) Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -3.1622776602e+09 · Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
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
    "candidate": "φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd}",
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
  "max_relative_effect_to_EH": 0.003315142969493544,
  "dominant_correction_term": "φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 1,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 0,
  "correction_term_count": 1,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd}",
      "coeff_symbol": "\\beta",
      "coefficient": "-3162277660.1683793",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 0.003315142969493544,
      "effect_class": "moderate"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000299_slot_08/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000299_slot_08/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000299_slot_08/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 23. task_000157_expanded_slot_10_lag_1  chi2=1638.160165

- best_validation_stage: `expanded`
- validation_stage_counts: `{"expanded": 1, "initial": 1}`
- family_accepted_records: `2`
- delta_chi2_vs_LCDM: `-7.11983528`
- delta_AIC_vs_LCDM: `4.88016472`
- delta_BIC_vs_LCDM: `37.9672572`
- scalar_config: `both`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "quadratic", "phi2": "quadratic"}`
- agent_parameter_sample_index: `959`
- H0_km_s_Mpc: `59.66609063`
- Omega_m0: `0.26872797`
- lambda_H_Lambda_over_H0: `1599.64064583`
- effective_correction_status: `active`
- max_relative_effect_to_EH: `2.45343504e+07`
- dominant_correction_term: `φ1 · R^{bcd}_{a} · R^{a}_{bcd}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-2.7103842542e+16) Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -2.7103842542e+16 · Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
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
  "effective_correction_status": "active",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 24534350.426541094,
  "dominant_correction_term": "φ1 · R^{bcd}_{a} · R^{a}_{bcd}",
  "active_correction_terms": 1,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 0,
  "correction_term_count": 1,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "φ1 · R^{bcd}_{a} · R^{a}_{bcd}",
      "coeff_symbol": "\\beta",
      "coefficient": "-2.7103842542243636e+16",
      "lambda_power": -3,
      "sector": "non-minimal",
      "relative_effect_to_EH": 24534350.426541094,
      "effect_class": "active"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000157_expanded_slot_10/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000157_expanded_slot_10/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000157_expanded_slot_10/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 24. task_000149_expanded_slot_02_lag_1  chi2=1638.255077

- best_validation_stage: `expanded`
- validation_stage_counts: `{"expanded": 5, "initial": 5}`
- family_accepted_records: `10`
- delta_chi2_vs_LCDM: `-7.02492337`
- delta_AIC_vs_LCDM: `4.97507663`
- delta_BIC_vs_LCDM: `38.06216911`
- scalar_config: `both`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "quadratic", "phi2": "quadratic"}`
- agent_parameter_sample_index: `182`
- H0_km_s_Mpc: `59.11675891`
- Omega_m0: `0.26495755`
- lambda_H_Lambda_over_H0: `1736.81290479`
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000149_expanded_slot_02/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000149_expanded_slot_02/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000149_expanded_slot_02/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 25. task_000085_expanded_slot_05_lag_1  chi2=1638.270775

- best_validation_stage: `expanded`
- validation_stage_counts: `{"expanded": 1, "initial": 1}`
- family_accepted_records: `2`
- delta_chi2_vs_LCDM: `-7.00922487`
- delta_AIC_vs_LCDM: `4.99077513`
- delta_BIC_vs_LCDM: `38.07786761`
- scalar_config: `both`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "quadratic", "phi2": "quadratic"}`
- agent_parameter_sample_index: `1379`
- H0_km_s_Mpc: `62.67033371`
- Omega_m0: `0.26720259`
- lambda_H_Lambda_over_H0: `1477.15019907`
- effective_correction_status: `active`
- max_relative_effect_to_EH: `2.07587175`
- dominant_correction_term: `φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-3} · φ2 · R^{ab} · R_{ab}  +  \gamma Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd}  +  \delta Λ^{-4} · φ1 · φ2 · R · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (3.4785751343e-06) Λ^{-3} · φ2 · R^{ab} · R_{ab}  +  (-1.4774574693e+12) Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd}  +  (5.2028001170e+04) Λ^{-4} · φ1 · φ2 · R · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-3} · φ2 · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( \delta · Λ^{-4} · φ1 · φ2 · R · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 3.4785751343e-06 · Λ^{-3} · φ2 · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( -1.4774574693e+12 · Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( 5.2028001170e+04 · Λ^{-4} · φ1 · φ2 · R · R ) ] +
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
    "candidate": "φ2 · R^{ab} · R_{ab}",
    "mass_dim": 5,
    "lambda_power": -3,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\gamma",
    "coeff_token": "COEFF_2",
    "candidate": "φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\delta",
    "coeff_token": "COEFF_3",
    "candidate": "φ1 · φ2 · R · R",
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
  "effective_correction_status": "active",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 2.075871745281104,
  "dominant_correction_term": "φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd}",
  "active_correction_terms": 1,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 2,
  "correction_term_count": 3,
  "tiny_correction_fraction": 0.6666666666666666,
  "term_effects": [
    {
      "candidate": "φ2 · R^{ab} · R_{ab}",
      "coeff_symbol": "\\beta",
      "coefficient": "3.4785751342872008e-06",
      "lambda_power": -3,
      "sector": "non-minimal",
      "relative_effect_to_EH": 2.1585266343554458e-20,
      "effect_class": "tiny"
    },
    {
      "candidate": "φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd}",
      "coeff_symbol": "\\gamma",
      "coefficient": "-1477457469339.2056",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 2.075871745281104,
      "effect_class": "active"
    },
    {
      "candidate": "φ1 · φ2 · R · R",
      "coeff_symbol": "\\delta",
      "coefficient": "52028.00117024968",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 3.997105299090604e-13,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000085_expanded_slot_05/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000085_expanded_slot_05/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000085_expanded_slot_05/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 26. task_000418_expanded_slot_11_lag_1  chi2=1638.418776

- best_validation_stage: `expanded`
- validation_stage_counts: `{"expanded": 1, "initial": 1}`
- family_accepted_records: `2`
- delta_chi2_vs_LCDM: `-6.86122363`
- delta_AIC_vs_LCDM: `3.13877637`
- delta_BIC_vs_LCDM: `30.7121596`
- scalar_config: `phi1_only`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "axion", "phi2": null}`
- agent_parameter_sample_index: `964`
- H0_km_s_Mpc: `68.29367083`
- Omega_m0: `0.26932994`
- lambda_H_Lambda_over_H0: `6454.95344256`
- effective_correction_status: `active`
- max_relative_effect_to_EH: `6.24659803e+04`
- dominant_correction_term: `φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · R · R^{ab} · R_{ab}  +  \gamma Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} )  +  \delta Λ^{2} · φ1 · φ1  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-214.2265549672) Λ^{-4} · R · R^{ab} · R_{ab}  +  (-2.3924796402e+19) Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} )  +  (-1.3545398860e-10) Λ^{2} · φ1 · φ1  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · R · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ \delta · Λ^{2} · φ1 · φ1 ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -214.2265549672 · Λ^{-4} · R · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( -2.3924796402e+19 · Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ -1.3545398860e-10 · Λ^{2} · φ1 · φ1 ] +
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
    "candidate": "R · R^{ab} · R_{ab}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\gamma",
    "coeff_token": "COEFF_2",
    "candidate": "φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "non-minimal"
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
  "max_relative_effect_to_EH": 62465.98028619244,
  "dominant_correction_term": "φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd}",
  "active_correction_terms": 1,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 1,
  "correction_term_count": 2,
  "tiny_correction_fraction": 0.5,
  "term_effects": [
    {
      "candidate": "R · R^{ab} · R_{ab}",
      "coeff_symbol": "\\beta",
      "coefficient": "-214.2265549672108",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 2.4679186659015637e-13,
      "effect_class": "tiny"
    },
    {
      "candidate": "φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd}",
      "coeff_symbol": "\\gamma",
      "coefficient": "-2.392479640173984e+19",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 62465.98028619244,
      "effect_class": "active"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000418_expanded_slot_11/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000418_expanded_slot_11/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000418_expanded_slot_11/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 27. task_000097_slot_11_lag_1  chi2=1638.485177

- best_validation_stage: `initial`
- validation_stage_counts: `{"initial": 1, "expanded": 1}`
- family_accepted_records: `2`
- delta_chi2_vs_LCDM: `-6.79482343`
- delta_AIC_vs_LCDM: `5.20517657`
- delta_BIC_vs_LCDM: `38.29226904`
- scalar_config: `both`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "quadratic", "phi2": "quadratic"}`
- agent_parameter_sample_index: `98`
- H0_km_s_Mpc: `64.59120606`
- Omega_m0: `0.25135005`
- lambda_H_Lambda_over_H0: `1446.15564031`
- effective_correction_status: `active`
- max_relative_effect_to_EH: `6.53158434`
- dominant_correction_term: `R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (1.4283962018e+13) Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 1.4283962018e+13 · Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf} ) ] +
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
    "candidate": "R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf}",
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
  "effective_correction_status": "active",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 6.531584343160863,
  "dominant_correction_term": "R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf}",
  "active_correction_terms": 1,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 0,
  "correction_term_count": 1,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf}",
      "coeff_symbol": "\\beta",
      "coefficient": "14283962017547.975",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 6.531584343160863,
      "effect_class": "active"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000097_slot_11/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000097_slot_11/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000097_slot_11/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 28. task_000361_slot_09_lag_1  chi2=1638.491445

- best_validation_stage: `initial`
- validation_stage_counts: `{"initial": 1, "expanded": 1}`
- family_accepted_records: `2`
- delta_chi2_vs_LCDM: `-6.78855498`
- delta_AIC_vs_LCDM: `9.21144502`
- delta_BIC_vs_LCDM: `53.325956`
- scalar_config: `both`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "axion", "phi2": "quadratic"}`
- agent_parameter_sample_index: `484`
- H0_km_s_Mpc: `64.91841645`
- Omega_m0: `0.27429385`
- lambda_H_Lambda_over_H0: `1471.28352136`
- effective_correction_status: `active`
- max_relative_effect_to_EH: `200.60342199`
- dominant_correction_term: `φ2 · φ2 · R^{bcd}_{a} · R^{a}_{bcd}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · φ2 · φ2 · R · R  +  \gamma Λ^{-4} · φ2 · φ2 · R^{bcd}_{a} · R^{a}_{bcd} )  +  \delta Λ^{2} · φ1 · φ1  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (1.0000000000e-04) Λ^{-4} · φ2 · φ2 · R · R  +  (-1.0000000000e+14) Λ^{-4} · φ2 · φ2 · R^{bcd}_{a} · R^{a}_{bcd} )  +  (3.1622776602e-09) Λ^{2} · φ1 · φ1  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · φ2 · φ2 · R · R ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · φ2 · φ2 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ \delta · Λ^{2} · φ1 · φ1 ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 1.0000000000e-04 · Λ^{-4} · φ2 · φ2 · R · R ) ] +
√(-g) [ M_p² ( -1.0000000000e+14 · Λ^{-4} · φ2 · φ2 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ 3.1622776602e-09 · Λ^{2} · φ1 · φ1 ] +
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
    "candidate": "φ2 · φ2 · R · R",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\gamma",
    "coeff_token": "COEFF_2",
    "candidate": "φ2 · φ2 · R^{bcd}_{a} · R^{a}_{bcd}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "non-minimal"
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
  "effective_correction_status": "active",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 200.60342199067506,
  "dominant_correction_term": "φ2 · φ2 · R^{bcd}_{a} · R^{a}_{bcd}",
  "active_correction_terms": 1,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 1,
  "correction_term_count": 2,
  "tiny_correction_fraction": 0.5,
  "term_effects": [
    {
      "candidate": "φ2 · φ2 · R · R",
      "coeff_symbol": "\\beta",
      "coefficient": "0.0001",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 2.0060342199067506e-16,
      "effect_class": "tiny"
    },
    {
      "candidate": "φ2 · φ2 · R^{bcd}_{a} · R^{a}_{bcd}",
      "coeff_symbol": "\\gamma",
      "coefficient": "-100000000000000.0",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 200.60342199067506,
      "effect_class": "active"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000361_slot_09/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000361_slot_09/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000361_slot_09/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 29. task_000087_expanded_slot_10_lag_1  chi2=1638.586797

- best_validation_stage: `expanded`
- validation_stage_counts: `{"expanded": 1, "initial": 1}`
- family_accepted_records: `2`
- delta_chi2_vs_LCDM: `-6.69320328`
- delta_AIC_vs_LCDM: `-2.69320328`
- delta_BIC_vs_LCDM: `8.33905221`
- scalar_config: `phi1_only`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: `404`
- H0_km_s_Mpc: `66.0380146`
- Omega_m0: `0.24835297`
- lambda_H_Lambda_over_H0: `1436.28460908`
- effective_correction_status: `eh_dominated`
- max_relative_effect_to_EH: `2.82717802e-15`
- dominant_correction_term: `R · R`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-2} · R · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (2.9161118239e-09) Λ^{-2} · R · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-2} · R · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 2.9161118239e-09 · Λ^{-2} · R · R ) ] +
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
  "max_relative_effect_to_EH": 2.827178022362646e-15,
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
      "coefficient": "2.9161118239105e-09",
      "lambda_power": -2,
      "sector": "gravity",
      "relative_effect_to_EH": 2.827178022362646e-15,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000087_expanded_slot_10/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000087_expanded_slot_10/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000087_expanded_slot_10/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 30. task_000108_expanded_slot_15_lag_1  chi2=1638.619632

- best_validation_stage: `expanded`
- validation_stage_counts: `{"expanded": 5, "initial": 5}`
- family_accepted_records: `10`
- delta_chi2_vs_LCDM: `-6.66036837`
- delta_AIC_vs_LCDM: `-2.66036837`
- delta_BIC_vs_LCDM: `8.37188711`
- scalar_config: `phi1_only`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: `2434`
- H0_km_s_Mpc: `58.73405082`
- Omega_m0: `0.29218253`
- lambda_H_Lambda_over_H0: `5670.94933636`
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000108_expanded_slot_15/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000108_expanded_slot_15/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000108_expanded_slot_15/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 31. task_000248_expanded_slot_02_lag_1  chi2=1638.639254

- best_validation_stage: `expanded`
- validation_stage_counts: `{"expanded": 1, "initial": 1}`
- family_accepted_records: `2`
- delta_chi2_vs_LCDM: `-6.64074591`
- delta_AIC_vs_LCDM: `9.35925409`
- delta_BIC_vs_LCDM: `53.47376506`
- scalar_config: `both`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "axion", "phi2": "quadratic"}`
- agent_parameter_sample_index: `1377`
- H0_km_s_Mpc: `71.49857188`
- Omega_m0: `0.30740212`
- lambda_H_Lambda_over_H0: `4280.24474793`
- effective_correction_status: `eh_dominated`
- max_relative_effect_to_EH: `6.80266667e-20`
- dominant_correction_term: `φ2 · R^{ab} · R_{ab}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-3} · φ2 · R^{ab} · R_{ab} )  +  \gamma · φ2 · φ2 · φ2 · φ2  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-3.7612228541e-05) Λ^{-3} · φ2 · R^{ab} · R_{ab} )  +  (-2.6653716396e+08) · φ2 · φ2 · φ2 · φ2  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-3} · φ2 · R^{ab} · R_{ab} ) ] +
√(-g) [ \gamma · φ2 · φ2 · φ2 · φ2 ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -3.7612228541e-05 · Λ^{-3} · φ2 · R^{ab} · R_{ab} ) ] +
√(-g) [ -2.6653716396e+08 · φ2 · φ2 · φ2 · φ2 ] +
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
    "candidate": "φ2 · R^{ab} · R_{ab}",
    "mass_dim": 5,
    "lambda_power": -3,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\gamma",
    "coeff_token": "COEFF_2",
    "candidate": "φ2 · φ2 · φ2 · φ2",
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
  "max_relative_effect_to_EH": 6.802666666363673e-20,
  "dominant_correction_term": "φ2 · R^{ab} · R_{ab}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 1,
  "correction_term_count": 1,
  "tiny_correction_fraction": 1.0,
  "term_effects": [
    {
      "candidate": "φ2 · R^{ab} · R_{ab}",
      "coeff_symbol": "\\beta",
      "coefficient": "-3.761222854121877e-05",
      "lambda_power": -3,
      "sector": "non-minimal",
      "relative_effect_to_EH": 6.802666666363673e-20,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000248_expanded_slot_02/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000248_expanded_slot_02/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000248_expanded_slot_02/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 32. task_000194_expanded_slot_12_lag_1  chi2=1638.973234

- best_validation_stage: `expanded`
- validation_stage_counts: `{"expanded": 1, "initial": 1}`
- family_accepted_records: `2`
- delta_chi2_vs_LCDM: `-6.30676647`
- delta_AIC_vs_LCDM: `-2.30676647`
- delta_BIC_vs_LCDM: `8.72548902`
- scalar_config: `phi1_only`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: `1736`
- H0_km_s_Mpc: `58.61748363`
- Omega_m0: `0.30497138`
- lambda_H_Lambda_over_H0: `1451.08986071`
- effective_correction_status: `active`
- max_relative_effect_to_EH: `6.00034886e+08`
- dominant_correction_term: `R^{bcd}_{a} · R^{a}_{bcd}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd}  +  \gamma Λ^{-2} · ∇^{a}∇_{a}R  +  \delta Λ^{-4} · R · R^{bcd}_{a} · R^{a}_{bcd}  +  \epsilon Λ^{-3} · φ1 · R · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-6.3173526435e+14) Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd}  +  (0.0903752826) Λ^{-2} · ∇^{a}∇_{a}R  +  (-2.9977630487e+11) Λ^{-4} · R · R^{bcd}_{a} · R^{a}_{bcd}  +  (3.4752398697e+09) Λ^{-3} · φ1 · R · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-2} · ∇^{a}∇_{a}R ) ] +
√(-g) [ M_p² ( \delta · Λ^{-4} · R · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( \epsilon · Λ^{-3} · φ1 · R · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -6.3173526435e+14 · Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( 0.0903752826 · Λ^{-2} · ∇^{a}∇_{a}R ) ] +
√(-g) [ M_p² ( -2.9977630487e+11 · Λ^{-4} · R · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( 3.4752398697e+09 · Λ^{-3} · φ1 · R · R ) ] +
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
    "candidate": "∇^{a}∇_{a}R",
    "mass_dim": 4,
    "lambda_power": -2,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\delta",
    "coeff_token": "COEFF_3",
    "candidate": "R · R^{bcd}_{a} · R^{a}_{bcd}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\epsilon",
    "coeff_token": "COEFF_4",
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
  "max_relative_effect_to_EH": 600034886.1314312,
  "dominant_correction_term": "R^{bcd}_{a} · R^{a}_{bcd}",
  "active_correction_terms": 3,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 1,
  "correction_term_count": 4,
  "tiny_correction_fraction": 0.25,
  "term_effects": [
    {
      "candidate": "R^{bcd}_{a} · R^{a}_{bcd}",
      "coeff_symbol": "\\beta",
      "coefficient": "-631735264354169.1",
      "lambda_power": -2,
      "sector": "gravity",
      "relative_effect_to_EH": 600034886.1314312,
      "effect_class": "active"
    },
    {
      "candidate": "∇^{a}∇_{a}R",
      "coeff_symbol": "\\gamma",
      "coefficient": "0.09037528260051142",
      "lambda_power": -2,
      "sector": "gravity",
      "relative_effect_to_EH": 8.584026484532579e-08,
      "effect_class": "tiny"
    },
    {
      "candidate": "R · R^{bcd}_{a} · R^{a}_{bcd}",
      "coeff_symbol": "\\delta",
      "coefficient": "-299776304871.93054",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 0.1352228445556041,
      "effect_class": "active"
    },
    {
      "candidate": "φ1 · R · R",
      "coeff_symbol": "\\epsilon",
      "coefficient": "3475239869.6813703",
      "lambda_power": -3,
      "sector": "non-minimal",
      "relative_effect_to_EH": 4.8288820496643154,
      "effect_class": "active"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000194_expanded_slot_12/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000194_expanded_slot_12/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000194_expanded_slot_12/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 33. task_000044_expanded_slot_06_lag_1  chi2=1638.978697

- best_validation_stage: `expanded`
- validation_stage_counts: `{"expanded": 1, "initial": 1}`
- family_accepted_records: `2`
- delta_chi2_vs_LCDM: `-6.30130336`
- delta_AIC_vs_LCDM: `5.69869664`
- delta_BIC_vs_LCDM: `38.78578912`
- scalar_config: `both`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "quadratic", "phi2": "quadratic"}`
- agent_parameter_sample_index: `2815`
- H0_km_s_Mpc: `60.63906813`
- Omega_m0: `0.29155609`
- lambda_H_Lambda_over_H0: `1122.68590927`
- effective_correction_status: `weak`
- max_relative_effect_to_EH: `8.25533882e-05`
- dominant_correction_term: `R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · R · R · R  +  \gamma Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf}  +  \delta Λ^{-4} · φ1 · φ1 · R^{ab} · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (3.6718843208e+06) Λ^{-4} · R · R · R  +  (-6.5574953979e+07) Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf}  +  (-5.5638856926e+05) Λ^{-4} · φ1 · φ1 · R^{ab} · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · R · R · R ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf} ) ] +
√(-g) [ M_p² ( \delta · Λ^{-4} · φ1 · φ1 · R^{ab} · R_{ab} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 3.6718843208e+06 · Λ^{-4} · R · R · R ) ] +
√(-g) [ M_p² ( -6.5574953979e+07 · Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf} ) ] +
√(-g) [ M_p² ( -5.5638856926e+05 · Λ^{-4} · φ1 · φ1 · R^{ab} · R_{ab} ) ] +
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
    "candidate": "R · R · R",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\gamma",
    "coeff_token": "COEFF_2",
    "candidate": "R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf}",
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
  "effective_correction_status": "weak",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 8.255338821351517e-05,
  "dominant_correction_term": "R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 3,
  "tiny_correction_terms": 0,
  "correction_term_count": 3,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "R · R · R",
      "coeff_symbol": "\\beta",
      "coefficient": "3671884.3208325193",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 4.622595570736535e-06,
      "effect_class": "weak"
    },
    {
      "candidate": "R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf}",
      "coeff_symbol": "\\gamma",
      "coefficient": "-65574953.97861686",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 8.255338821351517e-05,
      "effect_class": "weak"
    },
    {
      "candidate": "φ1 · φ1 · R^{ab} · R_{ab}",
      "coeff_symbol": "\\delta",
      "coefficient": "-556388.569257355",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 1.8196611809790252e-06,
      "effect_class": "weak"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000044_expanded_slot_06/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000044_expanded_slot_06/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000044_expanded_slot_06/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 34. task_000058_expanded_slot_13_lag_1  chi2=1639.038897

- best_validation_stage: `expanded`
- validation_stage_counts: `{"expanded": 1, "initial": 1}`
- family_accepted_records: `2`
- delta_chi2_vs_LCDM: `-6.24110322`
- delta_AIC_vs_LCDM: `-0.24110322`
- delta_BIC_vs_LCDM: `16.30486152`
- scalar_config: `phi1_only`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "axion", "phi2": null}`
- agent_parameter_sample_index: `1043`
- H0_km_s_Mpc: `69.97669956`
- Omega_m0: `0.30995249`
- lambda_H_Lambda_over_H0: `952.15551567`
- effective_correction_status: `weak`
- max_relative_effect_to_EH: `7.76571592e-05`
- dominant_correction_term: `R^{bcd}_{a} · R^{a}_{bcd}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-2} · R · R  +  \gamma Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd}  +  \delta Λ^{-4} · R · R^{ab} · R_{ab}  +  \epsilon Λ^{-3} · φ1 · R · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-28.469514525) Λ^{-2} · R · R  +  (35.2019951486) Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd}  +  (3.2041317933e+06) Λ^{-4} · R · R^{ab} · R_{ab}  +  (8154.8949148428) Λ^{-3} · φ1 · R · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-2} · R · R ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( \delta · Λ^{-4} · R · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( \epsilon · Λ^{-3} · φ1 · R · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -28.469514525 · Λ^{-2} · R · R ) ] +
√(-g) [ M_p² ( 35.2019951486 · Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( 3.2041317933e+06 · Λ^{-4} · R · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( 8154.8949148428 · Λ^{-3} · φ1 · R · R ) ] +
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
    "candidate": "R^{bcd}_{a} · R^{a}_{bcd}",
    "mass_dim": 4,
    "lambda_power": -2,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\delta",
    "coeff_token": "COEFF_3",
    "candidate": "R · R^{ab} · R_{ab}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\epsilon",
    "coeff_token": "COEFF_4",
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
  "max_relative_effect_to_EH": 7.765715917866938e-05,
  "dominant_correction_term": "R^{bcd}_{a} · R^{a}_{bcd}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 4,
  "tiny_correction_terms": 0,
  "correction_term_count": 4,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "R · R",
      "coeff_symbol": "\\beta",
      "coefficient": "-28.46951452499332",
      "lambda_power": -2,
      "sector": "gravity",
      "relative_effect_to_EH": 6.280500897380699e-05,
      "effect_class": "weak"
    },
    {
      "candidate": "R^{bcd}_{a} · R^{a}_{bcd}",
      "coeff_symbol": "\\gamma",
      "coefficient": "35.201995148649566",
      "lambda_power": -2,
      "sector": "gravity",
      "relative_effect_to_EH": 7.765715917866938e-05,
      "effect_class": "weak"
    },
    {
      "candidate": "R · R^{ab} · R_{ab}",
      "coeff_symbol": "\\delta",
      "coefficient": "3204131.793271105",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 7.796663968469565e-06,
      "effect_class": "weak"
    },
    {
      "candidate": "φ1 · R · R",
      "coeff_symbol": "\\epsilon",
      "coefficient": "8154.894914842825",
      "lambda_power": -3,
      "sector": "non-minimal",
      "relative_effect_to_EH": 2.9957415819920222e-05,
      "effect_class": "weak"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000058_expanded_slot_13/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000058_expanded_slot_13/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000058_expanded_slot_13/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 35. task_000089_expanded_slot_13_lag_1  chi2=1639.043139

- best_validation_stage: `expanded`
- validation_stage_counts: `{"expanded": 1, "initial": 1}`
- family_accepted_records: `2`
- delta_chi2_vs_LCDM: `-6.23686057`
- delta_AIC_vs_LCDM: `-0.23686057`
- delta_BIC_vs_LCDM: `16.30910416`
- scalar_config: `phi1_only`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: `775`
- H0_km_s_Mpc: `69.8383275`
- Omega_m0: `0.27836983`
- lambda_H_Lambda_over_H0: `1488.55921135`
- effective_correction_status: `active`
- max_relative_effect_to_EH: `3.44972407e+09`
- dominant_correction_term: `R · R`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-2} · R · R  +  \gamma Λ^{-4} · R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh}  +  \delta Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf} )  +  \epsilon · ∇^{a}φ1 · ∇_{a}φ1  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-3.8219639979e+15) Λ^{-2} · R · R  +  (-0.0010754241) Λ^{-4} · R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh}  +  (5.6424813300e+04) Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf} )  +  (-1.0517746551e-04) · ∇^{a}φ1 · ∇_{a}φ1  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-2} · R · R ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh} ) ] +
√(-g) [ M_p² ( \delta · Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf} ) ] +
√(-g) [ \epsilon · ∇^{a}φ1 · ∇_{a}φ1 ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -3.8219639979e+15 · Λ^{-2} · R · R ) ] +
√(-g) [ M_p² ( -0.0010754241 · Λ^{-4} · R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh} ) ] +
√(-g) [ M_p² ( 5.6424813300e+04 · Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf} ) ] +
√(-g) [ -1.0517746551e-04 · ∇^{a}φ1 · ∇_{a}φ1 ] +
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
    "candidate": "R · R",
    "mass_dim": 4,
    "lambda_power": -2,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\gamma",
    "coeff_token": "COEFF_2",
    "candidate": "R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\delta",
    "coeff_token": "COEFF_3",
    "candidate": "R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\epsilon",
    "coeff_token": "COEFF_4",
    "candidate": "∇^{a}φ1 · ∇_{a}φ1",
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
]
```

### Effective Correction Diagnostics

```json
{
  "effective_correction_status": "active",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 3449724065.556063,
  "dominant_correction_term": "R · R",
  "active_correction_terms": 1,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 2,
  "correction_term_count": 3,
  "tiny_correction_fraction": 0.6666666666666666,
  "term_effects": [
    {
      "candidate": "R · R",
      "coeff_symbol": "\\beta",
      "coefficient": "-3821963997873631.0",
      "lambda_power": -2,
      "sector": "gravity",
      "relative_effect_to_EH": 3449724065.556063,
      "effect_class": "active"
    },
    {
      "candidate": "R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh}",
      "coeff_symbol": "\\gamma",
      "coefficient": "-0.0010754241152715585",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 4.3807181126326914e-16,
      "effect_class": "tiny"
    },
    {
      "candidate": "R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf}",
      "coeff_symbol": "\\delta",
      "coefficient": "56424.81329969094",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 2.2984532159338607e-08,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000089_expanded_slot_13/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000089_expanded_slot_13/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000089_expanded_slot_13/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 36. task_000517_expanded_slot_06_lag_1  chi2=1639.69492

- best_validation_stage: `expanded`
- validation_stage_counts: `{"expanded": 1, "initial": 1}`
- family_accepted_records: `2`
- delta_chi2_vs_LCDM: `-5.58508031`
- delta_AIC_vs_LCDM: `4.41491969`
- delta_BIC_vs_LCDM: `31.98830292`
- scalar_config: `phi1_only`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "axion", "phi2": null}`
- agent_parameter_sample_index: `2858`
- H0_km_s_Mpc: `58.05158205`
- Omega_m0: `0.30434703`
- lambda_H_Lambda_over_H0: `3154.19100582`
- effective_correction_status: `active`
- max_relative_effect_to_EH: `8.97689910e+04`
- dominant_correction_term: `R_{ab} · R^{adef} · R^{b}_{def}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def} )  +  \gamma Λ^{2} · φ1 · φ1  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (4.4427134650e+18) Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def} )  +  (1.1382223625e-09) Λ^{2} · φ1 · φ1  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def} ) ] +
√(-g) [ \gamma · Λ^{2} · φ1 · φ1 ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 4.4427134650e+18 · Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def} ) ] +
√(-g) [ 1.1382223625e-09 · Λ^{2} · φ1 · φ1 ] +
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
    "candidate": "R_{ab} · R^{adef} · R^{b}_{def}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\gamma",
    "coeff_token": "COEFF_2",
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
  "max_relative_effect_to_EH": 89768.99099279297,
  "dominant_correction_term": "R_{ab} · R^{adef} · R^{b}_{def}",
  "active_correction_terms": 1,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 0,
  "correction_term_count": 1,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "R_{ab} · R^{adef} · R^{b}_{def}",
      "coeff_symbol": "\\beta",
      "coefficient": "4.4427134650478013e+18",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 89768.99099279297,
      "effect_class": "active"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000517_expanded_slot_06/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000517_expanded_slot_06/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000517_expanded_slot_06/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 37. task_000059_expanded_slot_15_lag_1  chi2=1639.995424

- best_validation_stage: `expanded`
- validation_stage_counts: `{"expanded": 1, "initial": 1}`
- family_accepted_records: `2`
- delta_chi2_vs_LCDM: `-5.28457614`
- delta_AIC_vs_LCDM: `6.71542386`
- delta_BIC_vs_LCDM: `39.80251634`
- scalar_config: `both`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "quadratic", "phi2": "quadratic"}`
- agent_parameter_sample_index: `2466`
- H0_km_s_Mpc: `59.10501428`
- Omega_m0: `0.30510016`
- lambda_H_Lambda_over_H0: `705.49786995`
- effective_correction_status: `moderate`
- max_relative_effect_to_EH: `0.00298376`
- dominant_correction_term: `φ1 · R^{ab} · R_{ab}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-3} · φ1 · R^{ab} · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (3.6635958408e+05) Λ^{-3} · φ1 · R^{ab} · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-3} · φ1 · R^{ab} · R_{ab} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 3.6635958408e+05 · Λ^{-3} · φ1 · R^{ab} · R_{ab} ) ] +
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
  "effective_correction_status": "moderate",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 0.0029837573821451303,
  "dominant_correction_term": "φ1 · R^{ab} · R_{ab}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 1,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 0,
  "correction_term_count": 1,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "φ1 · R^{ab} · R_{ab}",
      "coeff_symbol": "\\beta",
      "coefficient": "366359.5840828383",
      "lambda_power": -3,
      "sector": "non-minimal",
      "relative_effect_to_EH": 0.0029837573821451303,
      "effect_class": "moderate"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000059_expanded_slot_15/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000059_expanded_slot_15/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000059_expanded_slot_15/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 38. task_000021_expanded_slot_06_lag_1  chi2=1643.146829

- best_validation_stage: `expanded`
- validation_stage_counts: `{"expanded": 1, "initial": 1}`
- family_accepted_records: `2`
- delta_chi2_vs_LCDM: `-2.13317083`
- delta_AIC_vs_LCDM: `1.86682917`
- delta_BIC_vs_LCDM: `12.89908466`
- scalar_config: `phi1_only`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: `2203`
- H0_km_s_Mpc: `60.1663384`
- Omega_m0: `0.29433378`
- lambda_H_Lambda_over_H0: `829.25916338`
- effective_correction_status: `weak`
- max_relative_effect_to_EH: `7.11032194e-06`
- dominant_correction_term: `R · R^{ab} · R_{ab}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · R · R^{ab} · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-1.6812038913e+06) Λ^{-4} · R · R^{ab} · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · R · R^{ab} · R_{ab} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -1.6812038913e+06 · Λ^{-4} · R · R^{ab} · R_{ab} ) ] +
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
    "candidate": "R · R^{ab} · R_{ab}",
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
  "max_relative_effect_to_EH": 7.110321944544759e-06,
  "dominant_correction_term": "R · R^{ab} · R_{ab}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 1,
  "tiny_correction_terms": 0,
  "correction_term_count": 1,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "R · R^{ab} · R_{ab}",
      "coeff_symbol": "\\beta",
      "coefficient": "-1681203.8912524204",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 7.110321944544759e-06,
      "effect_class": "weak"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000021_expanded_slot_06/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000021_expanded_slot_06/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000021_expanded_slot_06/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 39. task_000316_expanded_slot_04_lag_1  chi2=1651.17631

- best_validation_stage: `expanded`
- validation_stage_counts: `{"expanded": 1, "initial": 1}`
- family_accepted_records: `2`
- delta_chi2_vs_LCDM: `5.89631008`
- delta_AIC_vs_LCDM: `31.89631008`
- delta_BIC_vs_LCDM: `103.5793673`
- scalar_config: `both`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "axion", "phi2": "axion"}`
- agent_parameter_sample_index: `46`
- H0_km_s_Mpc: `59.4420245`
- Omega_m0: `0.30283928`
- lambda_H_Lambda_over_H0: `3895.59039468`
- effective_correction_status: `active`
- max_relative_effect_to_EH: `1.54925001e+08`
- dominant_correction_term: `φ1 · R^{bcd}_{a} · R^{a}_{bcd}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd}  +  \gamma Λ^{-4} · φ1 · φ2 · R · R )  +  \delta Λ^{-1} · φ1 · φ2 · ∇^{a}∇_{a}φ2  +  \epsilon Λ^{-1} · φ1 · ∇^{a}φ1 · ∇_{a}φ2  +  \zeta Λ^{-1} · ∇^{a}φ1 · φ2 · ∇_{a}φ2  +  \eta Λ^{-1} · ∇^{a}∇_{a}φ1 · φ2 · φ2  +  \theta Λ^{-2} · φ2 · φ2 · φ2 · φ2 · φ2 · φ2  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (3.1622776602e+18) Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd}  +  (-3.1622776602) Λ^{-4} · φ1 · φ2 · R · R )  +  (3.1622776602e+09) Λ^{-1} · φ1 · φ2 · ∇^{a}∇_{a}φ2  +  (-1.0000000000e+05) Λ^{-1} · φ1 · ∇^{a}φ1 · ∇_{a}φ2  +  (1.0000000000e-04) Λ^{-1} · ∇^{a}φ1 · φ2 · ∇_{a}φ2  +  (-1.0000000000e+14) Λ^{-1} · ∇^{a}∇_{a}φ1 · φ2 · φ2  +  (3.1622776602e-09) Λ^{-2} · φ2 · φ2 · φ2 · φ2 · φ2 · φ2  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · φ1 · φ2 · R · R ) ] +
√(-g) [ \delta · Λ^{-1} · φ1 · φ2 · ∇^{a}∇_{a}φ2 ] +
√(-g) [ \epsilon · Λ^{-1} · φ1 · ∇^{a}φ1 · ∇_{a}φ2 ] +
√(-g) [ \zeta · Λ^{-1} · ∇^{a}φ1 · φ2 · ∇_{a}φ2 ] +
√(-g) [ \eta · Λ^{-1} · ∇^{a}∇_{a}φ1 · φ2 · φ2 ] +
√(-g) [ \theta · Λ^{-2} · φ2 · φ2 · φ2 · φ2 · φ2 · φ2 ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 3.1622776602e+18 · Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( -3.1622776602 · Λ^{-4} · φ1 · φ2 · R · R ) ] +
√(-g) [ 3.1622776602e+09 · Λ^{-1} · φ1 · φ2 · ∇^{a}∇_{a}φ2 ] +
√(-g) [ -1.0000000000e+05 · Λ^{-1} · φ1 · ∇^{a}φ1 · ∇_{a}φ2 ] +
√(-g) [ 1.0000000000e-04 · Λ^{-1} · ∇^{a}φ1 · φ2 · ∇_{a}φ2 ] +
√(-g) [ -1.0000000000e+14 · Λ^{-1} · ∇^{a}∇_{a}φ1 · φ2 · φ2 ] +
√(-g) [ 3.1622776602e-09 · Λ^{-2} · φ2 · φ2 · φ2 · φ2 · φ2 · φ2 ] +
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
    "candidate": "φ1 · R^{bcd}_{a} · R^{a}_{bcd}",
    "mass_dim": 5,
    "lambda_power": -3,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\gamma",
    "coeff_token": "COEFF_2",
    "candidate": "φ1 · φ2 · R · R",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\delta",
    "coeff_token": "COEFF_3",
    "candidate": "φ1 · φ2 · ∇^{a}∇_{a}φ2",
    "mass_dim": 5,
    "lambda_power": -1,
    "sector": "scalar"
  },
  {
    "coeff_symbol": "\\epsilon",
    "coeff_token": "COEFF_4",
    "candidate": "φ1 · ∇^{a}φ1 · ∇_{a}φ2",
    "mass_dim": 5,
    "lambda_power": -1,
    "sector": "scalar"
  },
  {
    "coeff_symbol": "\\zeta",
    "coeff_token": "COEFF_5",
    "candidate": "∇^{a}φ1 · φ2 · ∇_{a}φ2",
    "mass_dim": 5,
    "lambda_power": -1,
    "sector": "scalar"
  },
  {
    "coeff_symbol": "\\eta",
    "coeff_token": "COEFF_6",
    "candidate": "∇^{a}∇_{a}φ1 · φ2 · φ2",
    "mass_dim": 5,
    "lambda_power": -1,
    "sector": "scalar"
  },
  {
    "coeff_symbol": "\\theta",
    "coeff_token": "COEFF_7",
    "candidate": "φ2 · φ2 · φ2 · φ2 · φ2 · φ2",
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
  "effective_correction_status": "active",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 154925000.93535954,
  "dominant_correction_term": "φ1 · R^{bcd}_{a} · R^{a}_{bcd}",
  "active_correction_terms": 1,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 1,
  "correction_term_count": 2,
  "tiny_correction_fraction": 0.5,
  "term_effects": [
    {
      "candidate": "φ1 · R^{bcd}_{a} · R^{a}_{bcd}",
      "coeff_symbol": "\\beta",
      "coefficient": "3.1622776601683794e+18",
      "lambda_power": -3,
      "sector": "non-minimal",
      "relative_effect_to_EH": 154925000.93535954,
      "effect_class": "active"
    },
    {
      "candidate": "φ1 · φ2 · R · R",
      "coeff_symbol": "\\gamma",
      "coefficient": "-3.1622776601683795",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 8.642755859468915e-17,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000316_expanded_slot_04/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000316_expanded_slot_04/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000316_expanded_slot_04/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 40. task_000041_expanded_slot_03_lag_1  chi2=1651.845497

- best_validation_stage: `expanded`
- validation_stage_counts: `{"expanded": 1, "initial": 1}`
- family_accepted_records: `2`
- delta_chi2_vs_LCDM: `6.56549693`
- delta_AIC_vs_LCDM: `10.56549693`
- delta_BIC_vs_LCDM: `21.59775242`
- scalar_config: `phi1_only`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: `1681`
- H0_km_s_Mpc: `63.49253558`
- Omega_m0: `0.32727522`
- lambda_H_Lambda_over_H0: `767.89528517`
- effective_correction_status: `moderate`
- max_relative_effect_to_EH: `0.00456862`
- dominant_correction_term: `φ1 · R^{ab} · R_{ab}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-2} · R · R  +  \gamma Λ^{-3} · φ1 · R · R  +  \delta Λ^{-3} · φ1 · R^{ab} · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-22.1305335851) Λ^{-2} · R · R  +  (-8.8771063935e+04) Λ^{-3} · φ1 · R · R  +  (7.1760412029e+05) Λ^{-3} · φ1 · R^{ab} · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-2} · R · R ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-3} · φ1 · R · R ) ] +
√(-g) [ M_p² ( \delta · Λ^{-3} · φ1 · R^{ab} · R_{ab} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -22.1305335851 · Λ^{-2} · R · R ) ] +
√(-g) [ M_p² ( -8.8771063935e+04 · Λ^{-3} · φ1 · R · R ) ] +
√(-g) [ M_p² ( 7.1760412029e+05 · Λ^{-3} · φ1 · R^{ab} · R_{ab} ) ] +
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
    "candidate": "R · R",
    "mass_dim": 4,
    "lambda_power": -2,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\gamma",
    "coeff_token": "COEFF_2",
    "candidate": "φ1 · R · R",
    "mass_dim": 5,
    "lambda_power": -3,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\delta",
    "coeff_token": "COEFF_3",
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
  "effective_correction_status": "moderate",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 0.004568624290162595,
  "dominant_correction_term": "φ1 · R^{ab} · R_{ab}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 2,
  "weak_correction_terms": 1,
  "tiny_correction_terms": 0,
  "correction_term_count": 3,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "R · R",
      "coeff_symbol": "\\beta",
      "coefficient": "-22.130533585125963",
      "lambda_power": -2,
      "sector": "gravity",
      "relative_effect_to_EH": 7.506161059069273e-05,
      "effect_class": "weak"
    },
    {
      "candidate": "φ1 · R · R",
      "coeff_symbol": "\\gamma",
      "coefficient": "-88771.06393522423",
      "lambda_power": -3,
      "sector": "non-minimal",
      "relative_effect_to_EH": 0.0005651606888694651,
      "effect_class": "moderate"
    },
    {
      "candidate": "φ1 · R^{ab} · R_{ab}",
      "coeff_symbol": "\\delta",
      "coefficient": "717604.1202889015",
      "lambda_power": -3,
      "sector": "non-minimal",
      "relative_effect_to_EH": 0.004568624290162595,
      "effect_class": "moderate"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000041_expanded_slot_03/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000041_expanded_slot_03/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000041_expanded_slot_03/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 41. task_000036_expanded_slot_12_lag_1  chi2=1658.209666

- best_validation_stage: `expanded`
- validation_stage_counts: `{"expanded": 1, "initial": 1}`
- family_accepted_records: `2`
- delta_chi2_vs_LCDM: `12.92966637`
- delta_AIC_vs_LCDM: `16.92966637`
- delta_BIC_vs_LCDM: `27.96192185`
- scalar_config: `phi1_only`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: `2940`
- H0_km_s_Mpc: `63.77166801`
- Omega_m0: `0.32565335`
- lambda_H_Lambda_over_H0: `865.20181929`
- effective_correction_status: `moderate`
- max_relative_effect_to_EH: `0.00170009`
- dominant_correction_term: `φ1 · R^{ab} · R_{ab}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-3} · φ1 · R^{ab} · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-4.5440866469e+05) Λ^{-3} · φ1 · R^{ab} · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
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
√(-g) [ M_p² ( -4.5440866469e+05 · Λ^{-3} · φ1 · R^{ab} · R_{ab} ) ] +
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
  "effective_correction_status": "moderate",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 0.0017000871761635654,
  "dominant_correction_term": "φ1 · R^{ab} · R_{ab}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 1,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 0,
  "correction_term_count": 1,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "φ1 · R^{ab} · R_{ab}",
      "coeff_symbol": "\\beta",
      "coefficient": "-454408.66469483194",
      "lambda_power": -3,
      "sector": "non-minimal",
      "relative_effect_to_EH": 0.0017000871761635654,
      "effect_class": "moderate"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000036_expanded_slot_12/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000036_expanded_slot_12/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000036_expanded_slot_12/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 42. task_000019_expanded_slot_04_lag_1  chi2=1698.460079

- best_validation_stage: `expanded`
- validation_stage_counts: `{"expanded": 1, "initial": 1}`
- family_accepted_records: `2`
- delta_chi2_vs_LCDM: `53.18007935`
- delta_AIC_vs_LCDM: `57.18007935`
- delta_BIC_vs_LCDM: `68.21233484`
- scalar_config: `phi1_only`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: `2192`
- H0_km_s_Mpc: `64.6318941`
- Omega_m0: `0.33345336`
- lambda_H_Lambda_over_H0: `1938.53647393`
- effective_correction_status: `moderate`
- max_relative_effect_to_EH: `0.00448088`
- dominant_correction_term: `φ1 · R · R`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd}  +  \gamma Λ^{-4} · R · R^{ab} · R_{ab}  +  \delta Λ^{-3} · φ1 · R · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-443.4918654802) Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd}  +  (-2.1280709675e+10) Λ^{-4} · R · R^{ab} · R_{ab}  +  (1.8474912295e+07) Λ^{-3} · φ1 · R · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · R · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( \delta · Λ^{-3} · φ1 · R · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -443.4918654802 · Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( -2.1280709675e+10 · Λ^{-4} · R · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( 1.8474912295e+07 · Λ^{-3} · φ1 · R · R ) ] +
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
    "candidate": "R · R^{ab} · R_{ab}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\delta",
    "coeff_token": "COEFF_3",
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
  "max_relative_effect_to_EH": 0.004480884892710594,
  "dominant_correction_term": "φ1 · R · R",
  "active_correction_terms": 0,
  "moderate_correction_terms": 3,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 0,
  "correction_term_count": 3,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "R^{bcd}_{a} · R^{a}_{bcd}",
      "coeff_symbol": "\\beta",
      "coefficient": "-443.4918654802495",
      "lambda_power": -2,
      "sector": "gravity",
      "relative_effect_to_EH": 0.00023603026858123917,
      "effect_class": "moderate"
    },
    {
      "candidate": "R · R^{ab} · R_{ab}",
      "coeff_symbol": "\\gamma",
      "coefficient": "-21280709675.489502",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 0.0030138400202109217,
      "effect_class": "moderate"
    },
    {
      "candidate": "φ1 · R · R",
      "coeff_symbol": "\\delta",
      "coefficient": "18474912.29523269",
      "lambda_power": -3,
      "sector": "non-minimal",
      "relative_effect_to_EH": 0.004480884892710594,
      "effect_class": "moderate"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000019_expanded_slot_04/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000019_expanded_slot_04/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000019_expanded_slot_04/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 43. task_000596_expanded_refine_slot_06_lag_1  chi2=1929.396619

- best_validation_stage: `refine`
- validation_stage_counts: `{"refine": 1, "expanded": 1, "initial": 1}`
- family_accepted_records: `3`
- delta_chi2_vs_LCDM: `284.11661855`
- delta_AIC_vs_LCDM: `298.11661855`
- delta_BIC_vs_LCDM: `336.71742028`
- scalar_config: `phi2_only`
- proposal_group: `non_eh`
- theory_track: `non_eh`
- potential_types: `{"phi1": null, "phi2": "axion"}`
- agent_parameter_sample_index: `4241`
- H0_km_s_Mpc: `59.68972583`
- Omega_m0: `0.23409922`
- lambda_H_Lambda_over_H0: `9523.5000465`
- effective_correction_status: `not_applicable_non_eh`
- max_relative_effect_to_EH: ``
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha Λ^{-3} · φ2 · φ2 · φ2 · R  +  \beta Λ^{-3} · φ2 · ∇^{a}∇_{a}R  +  \gamma Λ^{-3} · ∇^{a}∇^{b}φ2 · R_{ab}  +  \delta Λ^{-4} · φ2 · φ2 · φ2 · φ2 · R  +  \epsilon Λ^{-4} · φ2 · φ2 · R^{ab} · R_{ab}  +  \zeta Λ^{-4} · φ2 · φ2 · R^{bcd}_{a} · R^{a}_{bcd}  +  \eta Λ^{-4} · ∇^{a}φ2 · ∇_{a}φ2 · R  +  \theta Λ^{-4} · φ2 · ∇^{a}∇^{b}φ2 · R_{ab} )  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (-1.1716980261e-05) Λ^{-3} · φ2 · φ2 · φ2 · R  +  (74.5028322818) Λ^{-3} · φ2 · ∇^{a}∇_{a}R  +  (-0.0036651178) Λ^{-3} · ∇^{a}∇^{b}φ2 · R_{ab}  +  (-4.0889065035e+10) Λ^{-4} · φ2 · φ2 · φ2 · φ2 · R  +  (1.5456592115e+10) Λ^{-4} · φ2 · φ2 · R^{ab} · R_{ab}  +  (-1.5969772246e+13) Λ^{-4} · φ2 · φ2 · R^{bcd}_{a} · R^{a}_{bcd}  +  (-0.4056036414) Λ^{-4} · ∇^{a}φ2 · ∇_{a}φ2 · R  +  (2.1172418358e-10) Λ^{-4} · φ2 · ∇^{a}∇^{b}φ2 · R_{ab} )  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · Λ^{-3} · φ2 · φ2 · φ2 · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-3} · φ2 · ∇^{a}∇_{a}R ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-3} · ∇^{a}∇^{b}φ2 · R_{ab} ) ] +
√(-g) [ M_p² ( \delta · Λ^{-4} · φ2 · φ2 · φ2 · φ2 · R ) ] +
√(-g) [ M_p² ( \epsilon · Λ^{-4} · φ2 · φ2 · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( \zeta · Λ^{-4} · φ2 · φ2 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( \eta · Λ^{-4} · ∇^{a}φ2 · ∇_{a}φ2 · R ) ] +
√(-g) [ M_p² ( \theta · Λ^{-4} · φ2 · ∇^{a}∇^{b}φ2 · R_{ab} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( -1.1716980261e-05 · Λ^{-3} · φ2 · φ2 · φ2 · R ) ] +
√(-g) [ M_p² ( 74.5028322818 · Λ^{-3} · φ2 · ∇^{a}∇_{a}R ) ] +
√(-g) [ M_p² ( -0.0036651178 · Λ^{-3} · ∇^{a}∇^{b}φ2 · R_{ab} ) ] +
√(-g) [ M_p² ( -4.0889065035e+10 · Λ^{-4} · φ2 · φ2 · φ2 · φ2 · R ) ] +
√(-g) [ M_p² ( 1.5456592115e+10 · Λ^{-4} · φ2 · φ2 · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( -1.5969772246e+13 · Λ^{-4} · φ2 · φ2 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( -0.4056036414 · Λ^{-4} · ∇^{a}φ2 · ∇_{a}φ2 · R ) ] +
√(-g) [ M_p² ( 2.1172418358e-10 · Λ^{-4} · φ2 · ∇^{a}∇^{b}φ2 · R_{ab} ) ] +
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
    "candidate": "φ2 · ∇^{a}∇_{a}R",
    "mass_dim": 5,
    "lambda_power": -3,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\gamma",
    "coeff_token": "COEFF_2",
    "candidate": "∇^{a}∇^{b}φ2 · R_{ab}",
    "mass_dim": 5,
    "lambda_power": -3,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\delta",
    "coeff_token": "COEFF_3",
    "candidate": "φ2 · φ2 · φ2 · φ2 · R",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\epsilon",
    "coeff_token": "COEFF_4",
    "candidate": "φ2 · φ2 · R^{ab} · R_{ab}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\zeta",
    "coeff_token": "COEFF_5",
    "candidate": "φ2 · φ2 · R^{bcd}_{a} · R^{a}_{bcd}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\eta",
    "coeff_token": "COEFF_6",
    "candidate": "∇^{a}φ2 · ∇_{a}φ2 · R",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\theta",
    "coeff_token": "COEFF_7",
    "candidate": "φ2 · ∇^{a}∇^{b}φ2 · R_{ab}",
    "mass_dim": 6,
    "lambda_power": -4,
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
  "effective_correction_status": "not_applicable_non_eh",
  "effective_correction_reason": "EH-relative correction diagnostic applies only to EH-anchored theories",
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000596_expanded_refine_slot_06/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000596_expanded_refine_slot_06/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000596_expanded_refine_slot_06/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 44. task_000074_expanded_slot_03_lag_1  chi2=1942.422359

- best_validation_stage: `expanded`
- validation_stage_counts: `{"expanded": 1, "initial": 1}`
- family_accepted_records: `2`
- delta_chi2_vs_LCDM: `297.14235879`
- delta_AIC_vs_LCDM: `311.14235879`
- delta_BIC_vs_LCDM: `349.74316051`
- scalar_config: `phi2_only`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": null, "phi2": "quadratic"}`
- agent_parameter_sample_index: `2375`
- H0_km_s_Mpc: `60.80070855`
- Omega_m0: `0.3219895`
- lambda_H_Lambda_over_H0: `641.23448004`
- effective_correction_status: `weak`
- max_relative_effect_to_EH: `2.66367033e-05`
- dominant_correction_term: `φ2 · φ2 · R^{bcd}_{a} · R^{a}_{bcd}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · ∇^{a}∇^{b}R · R_{ab}  +  \gamma Λ^{-4} · ∇^{c}R^{ab} · ∇_{c}R_{ab}  +  \delta Λ^{-1} · φ2 · R  +  \epsilon Λ^{-2} · φ2 · φ2 · R  +  \zeta Λ^{-4} · φ2 · φ2 · R^{ab} · R_{ab}  +  \eta Λ^{-4} · φ2 · φ2 · R^{bcd}_{a} · R^{a}_{bcd} )  +  \theta Λ^{-2} · φ2 · φ2 · φ2 · φ2 · φ2 · φ2  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-1.6850687990e+05) Λ^{-4} · ∇^{a}∇^{b}R · R_{ab}  +  (-3.9225441151e+05) Λ^{-4} · ∇^{c}R^{ab} · ∇_{c}R_{ab}  +  (-0.0012914527) Λ^{-1} · φ2 · R  +  (2.7877793084) Λ^{-2} · φ2 · φ2 · R  +  (1.0826550315e+06) Λ^{-4} · φ2 · φ2 · R^{ab} · R_{ab}  +  (1.1995617253e+07) Λ^{-4} · φ2 · φ2 · R^{bcd}_{a} · R^{a}_{bcd} )  +  (0.5159657665) Λ^{-2} · φ2 · φ2 · φ2 · φ2 · φ2 · φ2  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · ∇^{a}∇^{b}R · R_{ab} ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · ∇^{c}R^{ab} · ∇_{c}R_{ab} ) ] +
√(-g) [ M_p² ( \delta · Λ^{-1} · φ2 · R ) ] +
√(-g) [ M_p² ( \epsilon · Λ^{-2} · φ2 · φ2 · R ) ] +
√(-g) [ M_p² ( \zeta · Λ^{-4} · φ2 · φ2 · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( \eta · Λ^{-4} · φ2 · φ2 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ \theta · Λ^{-2} · φ2 · φ2 · φ2 · φ2 · φ2 · φ2 ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -1.6850687990e+05 · Λ^{-4} · ∇^{a}∇^{b}R · R_{ab} ) ] +
√(-g) [ M_p² ( -3.9225441151e+05 · Λ^{-4} · ∇^{c}R^{ab} · ∇_{c}R_{ab} ) ] +
√(-g) [ M_p² ( -0.0012914527 · Λ^{-1} · φ2 · R ) ] +
√(-g) [ M_p² ( 2.7877793084 · Λ^{-2} · φ2 · φ2 · R ) ] +
√(-g) [ M_p² ( 1.0826550315e+06 · Λ^{-4} · φ2 · φ2 · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( 1.1995617253e+07 · Λ^{-4} · φ2 · φ2 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ 0.5159657665 · Λ^{-2} · φ2 · φ2 · φ2 · φ2 · φ2 · φ2 ] +
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
    "candidate": "∇^{a}∇^{b}R · R_{ab}",
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
    "candidate": "φ2 · R",
    "mass_dim": 3,
    "lambda_power": -1,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\epsilon",
    "coeff_token": "COEFF_4",
    "candidate": "φ2 · φ2 · R",
    "mass_dim": 4,
    "lambda_power": -2,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\zeta",
    "coeff_token": "COEFF_5",
    "candidate": "φ2 · φ2 · R^{ab} · R_{ab}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\eta",
    "coeff_token": "COEFF_6",
    "candidate": "φ2 · φ2 · R^{bcd}_{a} · R^{a}_{bcd}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\theta",
    "coeff_token": "COEFF_7",
    "candidate": "φ2 · φ2 · φ2 · φ2 · φ2 · φ2",
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
  "effective_correction_status": "weak",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 2.6636703256395826e-05,
  "dominant_correction_term": "φ2 · φ2 · R^{bcd}_{a} · R^{a}_{bcd}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 6,
  "tiny_correction_terms": 0,
  "correction_term_count": 6,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "∇^{a}∇^{b}R · R_{ab}",
      "coeff_symbol": "\\beta",
      "coefficient": "-168506.87990050585",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 1.993334416379997e-06,
      "effect_class": "weak"
    },
    {
      "candidate": "∇^{c}R^{ab} · ∇_{c}R_{ab}",
      "coeff_symbol": "\\gamma",
      "coefficient": "-392254.411514603",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 4.64013231335484e-06,
      "effect_class": "weak"
    },
    {
      "candidate": "φ2 · R",
      "coeff_symbol": "\\delta",
      "coefficient": "-0.0012914526901588194",
      "lambda_power": -1,
      "sector": "non-minimal",
      "relative_effect_to_EH": 1.7451762826364565e-06,
      "effect_class": "weak"
    },
    {
      "candidate": "φ2 · φ2 · R",
      "coeff_symbol": "\\epsilon",
      "coefficient": "2.7877793083692186",
      "lambda_power": -2,
      "sector": "non-minimal",
      "relative_effect_to_EH": 2.545364580543238e-06,
      "effect_class": "weak"
    },
    {
      "candidate": "φ2 · φ2 · R^{ab} · R_{ab}",
      "coeff_symbol": "\\zeta",
      "coefficient": "1082655.031494618",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 2.404074771224838e-06,
      "effect_class": "weak"
    },
    {
      "candidate": "φ2 · φ2 · R^{bcd}_{a} · R^{a}_{bcd}",
      "coeff_symbol": "\\eta",
      "coefficient": "11995617.252899885",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 2.6636703256395826e-05,
      "effect_class": "weak"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000074_expanded_slot_03/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000074_expanded_slot_03/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000074_expanded_slot_03/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 45. task_000323_expanded_slot_14_lag_1  chi2=1946.870851

- best_validation_stage: `expanded`
- validation_stage_counts: `{"expanded": 1, "initial": 1}`
- family_accepted_records: `2`
- delta_chi2_vs_LCDM: `301.59085051`
- delta_AIC_vs_LCDM: `311.59085051`
- delta_BIC_vs_LCDM: `339.16423374`
- scalar_config: `phi2_only`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": null, "phi2": "axion"}`
- agent_parameter_sample_index: `2818`
- H0_km_s_Mpc: `67.83886959`
- Omega_m0: `0.30209823`
- lambda_H_Lambda_over_H0: `1416.13957251`
- effective_correction_status: `weak`
- max_relative_effect_to_EH: `4.27917527e-05`
- dominant_correction_term: `φ2 · φ2 · R · R`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-3} · φ2 · R · R  +  \gamma Λ^{-3} · φ2 · R^{ab} · R_{ab}  +  \delta Λ^{-3} · φ2 · R^{bcd}_{a} · R^{a}_{bcd}  +  \epsilon Λ^{-4} · φ2 · φ2 · R · R  +  \zeta Λ^{-4} · φ2 · φ2 · R^{ab} · R_{ab} )  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (2.1379369128e+06) Λ^{-3} · φ2 · R · R  +  (-3.3055496261e+05) Λ^{-3} · φ2 · R^{ab} · R_{ab}  +  (2.1790973490e+05) Λ^{-3} · φ2 · R^{bcd}_{a} · R^{a}_{bcd}  +  (-2.9785886133e+11) Λ^{-4} · φ2 · φ2 · R · R  +  (1.7799311983e+10) Λ^{-4} · φ2 · φ2 · R^{ab} · R_{ab} )  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-3} · φ2 · R · R ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-3} · φ2 · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( \delta · Λ^{-3} · φ2 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( \epsilon · Λ^{-4} · φ2 · φ2 · R · R ) ] +
√(-g) [ M_p² ( \zeta · Λ^{-4} · φ2 · φ2 · R^{ab} · R_{ab} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 2.1379369128e+06 · Λ^{-3} · φ2 · R · R ) ] +
√(-g) [ M_p² ( -3.3055496261e+05 · Λ^{-3} · φ2 · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( 2.1790973490e+05 · Λ^{-3} · φ2 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( -2.9785886133e+11 · Λ^{-4} · φ2 · φ2 · R · R ) ] +
√(-g) [ M_p² ( 1.7799311983e+10 · Λ^{-4} · φ2 · φ2 · R^{ab} · R_{ab} ) ] +
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
    "candidate": "φ2 · R · R",
    "mass_dim": 5,
    "lambda_power": -3,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\gamma",
    "coeff_token": "COEFF_2",
    "candidate": "φ2 · R^{ab} · R_{ab}",
    "mass_dim": 5,
    "lambda_power": -3,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\delta",
    "coeff_token": "COEFF_3",
    "candidate": "φ2 · R^{bcd}_{a} · R^{a}_{bcd}",
    "mass_dim": 5,
    "lambda_power": -3,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\epsilon",
    "coeff_token": "COEFF_4",
    "candidate": "φ2 · φ2 · R · R",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\zeta",
    "coeff_token": "COEFF_5",
    "candidate": "φ2 · φ2 · R^{ab} · R_{ab}",
    "mass_dim": 6,
    "lambda_power": -4,
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
  "effective_correction_status": "weak",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 4.279175273693981e-05,
  "dominant_correction_term": "φ2 · φ2 · R · R",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 5,
  "tiny_correction_terms": 0,
  "correction_term_count": 5,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "φ2 · R · R",
      "coeff_symbol": "\\beta",
      "coefficient": "2137936.912807243",
      "lambda_power": -3,
      "sector": "non-minimal",
      "relative_effect_to_EH": 2.559048989424113e-05,
      "effect_class": "weak"
    },
    {
      "candidate": "φ2 · R^{ab} · R_{ab}",
      "coeff_symbol": "\\gamma",
      "coefficient": "-330554.96260903723",
      "lambda_power": -3,
      "sector": "non-minimal",
      "relative_effect_to_EH": 3.956647822236508e-06,
      "effect_class": "weak"
    },
    {
      "candidate": "φ2 · R^{bcd}_{a} · R^{a}_{bcd}",
      "coeff_symbol": "\\delta",
      "coefficient": "217909.73489545105",
      "lambda_power": -3,
      "sector": "non-minimal",
      "relative_effect_to_EH": 2.608316847561524e-06,
      "effect_class": "weak"
    },
    {
      "candidate": "φ2 · φ2 · R · R",
      "coeff_symbol": "\\epsilon",
      "coefficient": "-297858861331.7111",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 4.279175273693981e-05,
      "effect_class": "weak"
    },
    {
      "candidate": "φ2 · φ2 · R^{ab} · R_{ab}",
      "coeff_symbol": "\\zeta",
      "coefficient": "17799311982.694416",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 2.557129755501485e-06,
      "effect_class": "weak"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000323_expanded_slot_14/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000323_expanded_slot_14/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000323_expanded_slot_14/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 46. task_000381_expanded_slot_03_lag_1  chi2=1946.870851

- best_validation_stage: `expanded`
- validation_stage_counts: `{"expanded": 1, "initial": 1}`
- family_accepted_records: `2`
- delta_chi2_vs_LCDM: `301.59085081`
- delta_AIC_vs_LCDM: `321.59085081`
- delta_BIC_vs_LCDM: `376.73278028`
- scalar_config: `both`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "axion", "phi2": "axion"}`
- agent_parameter_sample_index: `237`
- H0_km_s_Mpc: `69.20387071`
- Omega_m0: `0.27546411`
- lambda_H_Lambda_over_H0: `6543.77335344`
- effective_correction_status: `weak`
- max_relative_effect_to_EH: `3.98107171e-05`
- dominant_correction_term: `φ2 · φ2 · R^{ab} · R_{ab}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh}  +  \gamma Λ^{-4} · φ1 · φ1 · R^{ab} · R_{ab}  +  \delta Λ^{-4} · φ2 · φ2 · R · R  +  \epsilon Λ^{-4} · φ2 · φ2 · R^{ab} · R_{ab}  +  \zeta Λ^{-4} · φ2 · φ2 · R^{bcd}_{a} · R^{a}_{bcd} )  +  \eta Λ^{-2} · φ1 · φ2 · φ2 · φ2 · φ2 · φ2  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-1.8292918526e+10) Λ^{-4} · R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh}  +  (3.7162875650e+09) Λ^{-4} · φ1 · φ1 · R^{ab} · R_{ab}  +  (-2.0977630542e+06) Λ^{-4} · φ2 · φ2 · R · R  +  (3.3247303841e+07) Λ^{-4} · φ2 · φ2 · R^{ab} · R_{ab}  +  (-1.0513720620e+06) Λ^{-4} · φ2 · φ2 · R^{bcd}_{a} · R^{a}_{bcd} )  +  (3.1622776602e+18) Λ^{-2} · φ1 · φ2 · φ2 · φ2 · φ2 · φ2  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh} ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · φ1 · φ1 · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( \delta · Λ^{-4} · φ2 · φ2 · R · R ) ] +
√(-g) [ M_p² ( \epsilon · Λ^{-4} · φ2 · φ2 · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( \zeta · Λ^{-4} · φ2 · φ2 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ \eta · Λ^{-2} · φ1 · φ2 · φ2 · φ2 · φ2 · φ2 ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -1.8292918526e+10 · Λ^{-4} · R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh} ) ] +
√(-g) [ M_p² ( 3.7162875650e+09 · Λ^{-4} · φ1 · φ1 · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( -2.0977630542e+06 · Λ^{-4} · φ2 · φ2 · R · R ) ] +
√(-g) [ M_p² ( 3.3247303841e+07 · Λ^{-4} · φ2 · φ2 · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( -1.0513720620e+06 · Λ^{-4} · φ2 · φ2 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ 3.1622776602e+18 · Λ^{-2} · φ1 · φ2 · φ2 · φ2 · φ2 · φ2 ] +
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
    "candidate": "R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\gamma",
    "coeff_token": "COEFF_2",
    "candidate": "φ1 · φ1 · R^{ab} · R_{ab}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\delta",
    "coeff_token": "COEFF_3",
    "candidate": "φ2 · φ2 · R · R",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\epsilon",
    "coeff_token": "COEFF_4",
    "candidate": "φ2 · φ2 · R^{ab} · R_{ab}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\zeta",
    "coeff_token": "COEFF_5",
    "candidate": "φ2 · φ2 · R^{bcd}_{a} · R^{a}_{bcd}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\eta",
    "coeff_token": "COEFF_6",
    "candidate": "φ1 · φ2 · φ2 · φ2 · φ2 · φ2",
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
  "effective_correction_status": "weak",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 3.9810717055349695e-05,
  "dominant_correction_term": "φ2 · φ2 · R^{ab} · R_{ab}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 5,
  "tiny_correction_terms": 0,
  "correction_term_count": 5,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh}",
      "coeff_symbol": "\\beta",
      "coefficient": "-18292918525.52326",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 1.9952623149688786e-05,
      "effect_class": "weak"
    },
    {
      "candidate": "φ1 · φ1 · R^{ab} · R_{ab}",
      "coeff_symbol": "\\gamma",
      "coefficient": "3716287565.0299177",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 9.999999999999999e-06,
      "effect_class": "weak"
    },
    {
      "candidate": "φ2 · φ2 · R · R",
      "coeff_symbol": "\\delta",
      "coefficient": "-2097763.054233114",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 2.5118864315095823e-06,
      "effect_class": "weak"
    },
    {
      "candidate": "φ2 · φ2 · R^{ab} · R_{ab}",
      "coeff_symbol": "\\epsilon",
      "coefficient": "33247303.840504903",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 3.9810717055349695e-05,
      "effect_class": "weak"
    },
    {
      "candidate": "φ2 · φ2 · R^{bcd}_{a} · R^{a}_{bcd}",
      "coeff_symbol": "\\zeta",
      "coefficient": "-1051372.06195659",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 1.2589254117941661e-06,
      "effect_class": "weak"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000381_expanded_slot_03/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000381_expanded_slot_03/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000381_expanded_slot_03/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 47. task_000043_expanded_refine_slot_05_lag_1  chi2=1946.870857

- best_validation_stage: `refine`
- validation_stage_counts: `{"refine": 1, "expanded": 1, "initial": 1}`
- family_accepted_records: `3`
- delta_chi2_vs_LCDM: `301.59085729`
- delta_AIC_vs_LCDM: `311.59085729`
- delta_BIC_vs_LCDM: `339.16424052`
- scalar_config: `phi2_only`
- proposal_group: `non_eh`
- theory_track: `non_eh`
- potential_types: `{"phi1": null, "phi2": "quadratic"}`
- agent_parameter_sample_index: `4000`
- H0_km_s_Mpc: `66.92593594`
- Omega_m0: `0.29089619`
- lambda_H_Lambda_over_H0: `765.74273772`
- effective_correction_status: `not_applicable_non_eh`
- max_relative_effect_to_EH: ``
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha Λ^{-4} · R · R^{ab} · R_{ab}  +  \beta Λ^{-3} · φ2 · R^{ab} · R_{ab}  +  \gamma Λ^{-3} · φ2 · R^{bcd}_{a} · R^{a}_{bcd}  +  \delta Λ^{-3} · ∇^{a}∇^{b}φ2 · R_{ab}  +  \epsilon Λ^{-4} · φ2 · ∇^{a}φ2 · ∇_{a}R )  +  \zeta · ∇^{a}φ2 · ∇_{a}φ2  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (-4.7181464011e+05) Λ^{-4} · R · R^{ab} · R_{ab}  +  (7.8297775041e+04) Λ^{-3} · φ2 · R^{ab} · R_{ab}  +  (2294.0060603603) Λ^{-3} · φ2 · R^{bcd}_{a} · R^{a}_{bcd}  +  (-1.6377269741e+05) Λ^{-3} · ∇^{a}∇^{b}φ2 · R_{ab}  +  (-2.0854444536e+08) Λ^{-4} · φ2 · ∇^{a}φ2 · ∇_{a}R )  +  (9.6167499291) · ∇^{a}φ2 · ∇_{a}φ2  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · Λ^{-4} · R · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( \beta · Λ^{-3} · φ2 · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-3} · φ2 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( \delta · Λ^{-3} · ∇^{a}∇^{b}φ2 · R_{ab} ) ] +
√(-g) [ M_p² ( \epsilon · Λ^{-4} · φ2 · ∇^{a}φ2 · ∇_{a}R ) ] +
√(-g) [ \zeta · ∇^{a}φ2 · ∇_{a}φ2 ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( -4.7181464011e+05 · Λ^{-4} · R · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( 7.8297775041e+04 · Λ^{-3} · φ2 · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( 2294.0060603603 · Λ^{-3} · φ2 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( -1.6377269741e+05 · Λ^{-3} · ∇^{a}∇^{b}φ2 · R_{ab} ) ] +
√(-g) [ M_p² ( -2.0854444536e+08 · Λ^{-4} · φ2 · ∇^{a}φ2 · ∇_{a}R ) ] +
√(-g) [ 9.6167499291 · ∇^{a}φ2 · ∇_{a}φ2 ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Term Metadata

```json
[
  {
    "coeff_symbol": "\\alpha",
    "coeff_token": "COEFF_0",
    "candidate": "R · R^{ab} · R_{ab}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\beta",
    "coeff_token": "COEFF_1",
    "candidate": "φ2 · R^{ab} · R_{ab}",
    "mass_dim": 5,
    "lambda_power": -3,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\gamma",
    "coeff_token": "COEFF_2",
    "candidate": "φ2 · R^{bcd}_{a} · R^{a}_{bcd}",
    "mass_dim": 5,
    "lambda_power": -3,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\delta",
    "coeff_token": "COEFF_3",
    "candidate": "∇^{a}∇^{b}φ2 · R_{ab}",
    "mass_dim": 5,
    "lambda_power": -3,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\epsilon",
    "coeff_token": "COEFF_4",
    "candidate": "φ2 · ∇^{a}φ2 · ∇_{a}R",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\zeta",
    "coeff_token": "COEFF_5",
    "candidate": "∇^{a}φ2 · ∇_{a}φ2",
    "mass_dim": 4,
    "lambda_power": 0,
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
  "effective_correction_status": "not_applicable_non_eh",
  "effective_correction_reason": "EH-relative correction diagnostic applies only to EH-anchored theories",
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000043_expanded_refine_slot_05/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000043_expanded_refine_slot_05/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000043_expanded_refine_slot_05/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 48. task_000025_slot_10_lag_1  chi2=2199.207158

- best_validation_stage: `initial`
- validation_stage_counts: `{"initial": 1}`
- family_accepted_records: `1`
- delta_chi2_vs_LCDM: `553.92715777`
- delta_AIC_vs_LCDM: `569.92715777`
- delta_BIC_vs_LCDM: `614.04166874`
- scalar_config: `both`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "axion", "phi2": "axion"}`
- agent_parameter_sample_index: `898`
- H0_km_s_Mpc: `62.37432846`
- Omega_m0: `0.28037889`
- lambda_H_Lambda_over_H0: `1.12624210e+04`
- effective_correction_status: `moderate`
- max_relative_effect_to_EH: `0.00296482`
- dominant_correction_term: `R^{ab} · R_{ab}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-2} · R^{ab} · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (1.8803212979e+05) Λ^{-2} · R^{ab} · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-2} · R^{ab} · R_{ab} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 1.8803212979e+05 · Λ^{-2} · R^{ab} · R_{ab} ) ] +
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
  "effective_correction_status": "moderate",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 0.002964821481769406,
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
      "coefficient": "188032.12979013348",
      "lambda_power": -2,
      "sector": "gravity",
      "relative_effect_to_EH": 0.002964821481769406,
      "effect_class": "moderate"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000025_slot_10/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000025_slot_10/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000025_slot_10/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 49. task_000545_slot_01_lag_1  chi2=3667.454736

- best_validation_stage: `initial`
- validation_stage_counts: `{"initial": 1}`
- family_accepted_records: `1`
- delta_chi2_vs_LCDM: `2022.1747362`
- delta_AIC_vs_LCDM: `2046.1747362`
- delta_BIC_vs_LCDM: `2112.34408416`
- scalar_config: `both`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "axion", "phi2": "axion"}`
- agent_parameter_sample_index: `984`
- H0_km_s_Mpc: `71.9041225`
- Omega_m0: `0.28660256`
- lambda_H_Lambda_over_H0: `982.19841332`
- effective_correction_status: `eh_only`
- max_relative_effect_to_EH: `0`
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R )  +  \beta Λ^{2} · φ1 · φ1  +  \gamma Λ^{2} · φ2 · φ2  +  \delta Λ^{-1} · φ1 · ∇^{a}φ1 · ∇_{a}φ2  +  \epsilon Λ^{-2} · φ1 · φ2 · φ2 · φ2 · φ2 · φ2  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R )  +  (-3.3312394672e-09) Λ^{2} · φ1 · φ1  +  (-1.0139373755e-05) Λ^{2} · φ2 · φ2  +  (1.4465985631e+04) Λ^{-1} · φ1 · ∇^{a}φ1 · ∇_{a}φ2  +  (12.5859418501) Λ^{-2} · φ1 · φ2 · φ2 · φ2 · φ2 · φ2  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ \beta · Λ^{2} · φ1 · φ1 ] +
√(-g) [ \gamma · Λ^{2} · φ2 · φ2 ] +
√(-g) [ \delta · Λ^{-1} · φ1 · ∇^{a}φ1 · ∇_{a}φ2 ] +
√(-g) [ \epsilon · Λ^{-2} · φ1 · φ2 · φ2 · φ2 · φ2 · φ2 ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ -3.3312394672e-09 · Λ^{2} · φ1 · φ1 ] +
√(-g) [ -1.0139373755e-05 · Λ^{2} · φ2 · φ2 ] +
√(-g) [ 1.4465985631e+04 · Λ^{-1} · φ1 · ∇^{a}φ1 · ∇_{a}φ2 ] +
√(-g) [ 12.5859418501 · Λ^{-2} · φ1 · φ2 · φ2 · φ2 · φ2 · φ2 ] +
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
    "candidate": "φ1 · φ1",
    "mass_dim": 2,
    "lambda_power": 2,
    "sector": "scalar"
  },
  {
    "coeff_symbol": "\\gamma",
    "coeff_token": "COEFF_2",
    "candidate": "φ2 · φ2",
    "mass_dim": 2,
    "lambda_power": 2,
    "sector": "scalar"
  },
  {
    "coeff_symbol": "\\delta",
    "coeff_token": "COEFF_3",
    "candidate": "φ1 · ∇^{a}φ1 · ∇_{a}φ2",
    "mass_dim": 5,
    "lambda_power": -1,
    "sector": "scalar"
  },
  {
    "coeff_symbol": "\\epsilon",
    "coeff_token": "COEFF_4",
    "candidate": "φ1 · φ2 · φ2 · φ2 · φ2 · φ2",
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000545_slot_01/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000545_slot_01/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000545_slot_01/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 50. task_000002_slot_02_lag_1  chi2=4024.068817

- best_validation_stage: `initial`
- validation_stage_counts: `{"initial": 1}`
- family_accepted_records: `1`
- delta_chi2_vs_LCDM: `2378.78881696`
- delta_AIC_vs_LCDM: `2394.78881696`
- delta_BIC_vs_LCDM: `2438.90332793`
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000002_slot_02/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000002_slot_02/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000002_slot_02/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 51. task_000144_slot_11_lag_1  chi2=4181.706685

- best_validation_stage: `initial`
- validation_stage_counts: `{"initial": 1}`
- family_accepted_records: `1`
- delta_chi2_vs_LCDM: `2536.4266848`
- delta_AIC_vs_LCDM: `2546.4266848`
- delta_BIC_vs_LCDM: `2574.00006803`
- scalar_config: `phi1_only`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "axion", "phi2": null}`
- agent_parameter_sample_index: `969`
- H0_km_s_Mpc: `70.67373889`
- Omega_m0: `0.31070317`
- lambda_H_Lambda_over_H0: `1939.253502`
- effective_correction_status: `eh_only`
- max_relative_effect_to_EH: `0`
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R )  +  \beta Λ^{2} · φ1 · φ1  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R )  +  (4.8920748440e-09) Λ^{2} · φ1 · φ1  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ \beta · Λ^{2} · φ1 · φ1 ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ 4.8920748440e-09 · Λ^{2} · φ1 · φ1 ] +
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000144_slot_11/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000144_slot_11/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000144_slot_11/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 52. task_000408_slot_11_lag_1  chi2=9325.039046

- best_validation_stage: `initial`
- validation_stage_counts: `{"initial": 1}`
- family_accepted_records: `1`
- delta_chi2_vs_LCDM: `7679.75904626`
- delta_AIC_vs_LCDM: `7699.75904626`
- delta_BIC_vs_LCDM: `7754.90097573`
- scalar_config: `both`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "axion", "phi2": "axion"}`
- agent_parameter_sample_index: `928`
- H0_km_s_Mpc: `64.45567243`
- Omega_m0: `0.28838007`
- lambda_H_Lambda_over_H0: `4426.08328618`
- effective_correction_status: `eh_dominated`
- max_relative_effect_to_EH: `4.85321097e-07`
- dominant_correction_term: `φ2 · R`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-1} · φ2 · R )  +  \gamma · φ1 · φ1 · φ2 · φ2  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-0.1015989744) Λ^{-1} · φ2 · R )  +  (-3.5338172351e-10) · φ1 · φ1 · φ2 · φ2  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-1} · φ2 · R ) ] +
√(-g) [ \gamma · φ1 · φ1 · φ2 · φ2 ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -0.1015989744 · Λ^{-1} · φ2 · R ) ] +
√(-g) [ -3.5338172351e-10 · φ1 · φ1 · φ2 · φ2 ] +
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
    "candidate": "φ2 · R",
    "mass_dim": 3,
    "lambda_power": -1,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\gamma",
    "coeff_token": "COEFF_2",
    "candidate": "φ1 · φ1 · φ2 · φ2",
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
  "max_relative_effect_to_EH": 4.853210968618287e-07,
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
      "coefficient": "-0.10159897437129688",
      "lambda_power": -1,
      "sector": "non-minimal",
      "relative_effect_to_EH": 4.853210968618287e-07,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000408_slot_11/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000408_slot_11/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000408_slot_11/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 53. task_000335_slot_04_lag_1  chi2=9434.002732

- best_validation_stage: `initial`
- validation_stage_counts: `{"initial": 1}`
- family_accepted_records: `1`
- delta_chi2_vs_LCDM: `7788.7227318`
- delta_AIC_vs_LCDM: `7798.7227318`
- delta_BIC_vs_LCDM: `7826.29611503`
- scalar_config: `phi2_only`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": null, "phi2": "axion"}`
- agent_parameter_sample_index: `927`
- H0_km_s_Mpc: `66.08028745`
- Omega_m0: `0.2968339`
- lambda_H_Lambda_over_H0: `565.25084431`
- effective_correction_status: `weak`
- max_relative_effect_to_EH: `1.11526634e-05`
- dominant_correction_term: `φ2 · R`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-1} · φ2 · R )  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (0.0461961381) Λ^{-1} · φ2 · R )  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
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
√(-g) [ M_p² ( 0.0461961381 · Λ^{-1} · φ2 · R ) ] +
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
  "effective_correction_status": "weak",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 1.1152663445786806e-05,
  "dominant_correction_term": "φ2 · R",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 1,
  "tiny_correction_terms": 0,
  "correction_term_count": 1,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "φ2 · R",
      "coeff_symbol": "\\beta",
      "coefficient": "0.04619613811334283",
      "lambda_power": -1,
      "sector": "non-minimal",
      "relative_effect_to_EH": 1.1152663445786806e-05,
      "effect_class": "weak"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000335_slot_04/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000335_slot_04/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000335_slot_04/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 54. task_000078_slot_07_lag_1  chi2=9434.002753

- best_validation_stage: `initial`
- validation_stage_counts: `{"initial": 1}`
- family_accepted_records: `1`
- delta_chi2_vs_LCDM: `7788.72275328`
- delta_AIC_vs_LCDM: `7802.72275328`
- delta_BIC_vs_LCDM: `7841.32355501`
- scalar_config: `phi2_only`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": null, "phi2": "axion"}`
- agent_parameter_sample_index: `162`
- H0_km_s_Mpc: `60.94148172`
- Omega_m0: `0.32705007`
- lambda_H_Lambda_over_H0: `1215.76425732`
- effective_correction_status: `weak`
- max_relative_effect_to_EH: `3.98107171e-05`
- dominant_correction_term: `R_{ab} · R^{adef} · R^{b}_{def}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · R · R · R  +  \gamma Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def}  +  \delta Λ^{-1} · φ2 · R )  +  \epsilon Λ^{2} · φ2 · φ2  +  \zeta Λ^{-1} · φ2 · φ2 · φ2 · φ2 · φ2  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (2.7438950068e+06) Λ^{-4} · R · R · R  +  (-4.3487805171e+07) Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def}  +  (0.3339465536) Λ^{-1} · φ2 · R )  +  (-3.1622776602e+18) Λ^{2} · φ2 · φ2  +  (3.1622776602) Λ^{-1} · φ2 · φ2 · φ2 · φ2 · φ2  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · R · R · R ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def} ) ] +
√(-g) [ M_p² ( \delta · Λ^{-1} · φ2 · R ) ] +
√(-g) [ \epsilon · Λ^{2} · φ2 · φ2 ] +
√(-g) [ \zeta · Λ^{-1} · φ2 · φ2 · φ2 · φ2 · φ2 ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 2.7438950068e+06 · Λ^{-4} · R · R · R ) ] +
√(-g) [ M_p² ( -4.3487805171e+07 · Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def} ) ] +
√(-g) [ M_p² ( 0.3339465536 · Λ^{-1} · φ2 · R ) ] +
√(-g) [ -3.1622776602e+18 · Λ^{2} · φ2 · φ2 ] +
√(-g) [ 3.1622776602 · Λ^{-1} · φ2 · φ2 · φ2 · φ2 · φ2 ] +
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
    "candidate": "R · R · R",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\gamma",
    "coeff_token": "COEFF_2",
    "candidate": "R_{ab} · R^{adef} · R^{b}_{def}",
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
    "candidate": "φ2 · φ2",
    "mass_dim": 2,
    "lambda_power": 2,
    "sector": "scalar"
  },
  {
    "coeff_symbol": "\\zeta",
    "coeff_token": "COEFF_5",
    "candidate": "φ2 · φ2 · φ2 · φ2 · φ2",
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
  "effective_correction_status": "weak",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 3.9810717055349695e-05,
  "dominant_correction_term": "R_{ab} · R^{adef} · R^{b}_{def}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 3,
  "tiny_correction_terms": 0,
  "correction_term_count": 3,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "R · R · R",
      "coeff_symbol": "\\beta",
      "coefficient": "2743895.0068030227",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 2.5118864315095823e-06,
      "effect_class": "weak"
    },
    {
      "candidate": "R_{ab} · R^{adef} · R^{b}_{def}",
      "coeff_symbol": "\\gamma",
      "coefficient": "-43487805.17110144",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 3.9810717055349695e-05,
      "effect_class": "weak"
    },
    {
      "candidate": "φ2 · R",
      "coeff_symbol": "\\delta",
      "coefficient": "0.33394655364716297",
      "lambda_power": -1,
      "sector": "non-minimal",
      "relative_effect_to_EH": 1.2589254117941661e-06,
      "effect_class": "weak"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000078_slot_07/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000078_slot_07/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000078_slot_07/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 55. task_000584_slot_06_lag_1  chi2=9434.00278

- best_validation_stage: `initial`
- validation_stage_counts: `{"initial": 1}`
- family_accepted_records: `1`
- delta_chi2_vs_LCDM: `7788.72277985`
- delta_AIC_vs_LCDM: `7802.72277985`
- delta_BIC_vs_LCDM: `7841.32358158`
- scalar_config: `phi2_only`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": null, "phi2": "quadratic"}`
- agent_parameter_sample_index: `758`
- H0_km_s_Mpc: `67.42077805`
- Omega_m0: `0.30064041`
- lambda_H_Lambda_over_H0: `1034.78327253`
- effective_correction_status: `weak`
- max_relative_effect_to_EH: `1.21360903e-05`
- dominant_correction_term: `R · R^{ab} · R_{ab}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd}  +  \gamma Λ^{-4} · R · R^{ab} · R_{ab}  +  \delta Λ^{-1} · φ2 · R )  +  \epsilon · ∇^{a}φ2 · ∇_{a}φ2  +  \zeta Λ^{-1} · φ2 · ∇^{a}φ2 · ∇_{a}φ2  +  \eta Λ^{-2} · φ2 · φ2 · φ2 · ∇^{a}∇_{a}φ2  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (5.1029936429) Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd}  +  (-6.9573908351e+06) Λ^{-4} · R · R^{ab} · R_{ab}  +  (-0.0737276642) Λ^{-1} · φ2 · R )  +  (-9.5041013501e+08) · ∇^{a}φ2 · ∇_{a}φ2  +  (1.7350448762e+09) Λ^{-1} · φ2 · ∇^{a}φ2 · ∇_{a}φ2  +  (1.0704034938e+07) Λ^{-2} · φ2 · φ2 · φ2 · ∇^{a}∇_{a}φ2  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · R · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( \delta · Λ^{-1} · φ2 · R ) ] +
√(-g) [ \epsilon · ∇^{a}φ2 · ∇_{a}φ2 ] +
√(-g) [ \zeta · Λ^{-1} · φ2 · ∇^{a}φ2 · ∇_{a}φ2 ] +
√(-g) [ \eta · Λ^{-2} · φ2 · φ2 · φ2 · ∇^{a}∇_{a}φ2 ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 5.1029936429 · Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( -6.9573908351e+06 · Λ^{-4} · R · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( -0.0737276642 · Λ^{-1} · φ2 · R ) ] +
√(-g) [ -9.5041013501e+08 · ∇^{a}φ2 · ∇_{a}φ2 ] +
√(-g) [ 1.7350448762e+09 · Λ^{-1} · φ2 · ∇^{a}φ2 · ∇_{a}φ2 ] +
√(-g) [ 1.0704034938e+07 · Λ^{-2} · φ2 · φ2 · φ2 · ∇^{a}∇_{a}φ2 ] +
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
    "candidate": "R^{bcd}_{a} · R^{a}_{bcd}",
    "mass_dim": 4,
    "lambda_power": -2,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\gamma",
    "coeff_token": "COEFF_2",
    "candidate": "R · R^{ab} · R_{ab}",
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
    "candidate": "∇^{a}φ2 · ∇_{a}φ2",
    "mass_dim": 4,
    "lambda_power": 0,
    "sector": "scalar"
  },
  {
    "coeff_symbol": "\\zeta",
    "coeff_token": "COEFF_5",
    "candidate": "φ2 · ∇^{a}φ2 · ∇_{a}φ2",
    "mass_dim": 5,
    "lambda_power": -1,
    "sector": "scalar"
  },
  {
    "coeff_symbol": "\\eta",
    "coeff_token": "COEFF_6",
    "candidate": "φ2 · φ2 · φ2 · ∇^{a}∇_{a}φ2",
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
  "effective_correction_status": "weak",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 1.2136090261823952e-05,
  "dominant_correction_term": "R · R^{ab} · R_{ab}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 3,
  "tiny_correction_terms": 0,
  "correction_term_count": 3,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "R^{bcd}_{a} · R^{a}_{bcd}",
      "coeff_symbol": "\\beta",
      "coefficient": "5.102993642864165",
      "lambda_power": -2,
      "sector": "gravity",
      "relative_effect_to_EH": 9.531389638985216e-06,
      "effect_class": "weak"
    },
    {
      "candidate": "R · R^{ab} · R_{ab}",
      "coeff_symbol": "\\gamma",
      "coefficient": "-6957390.835069511",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 1.2136090261823952e-05,
      "effect_class": "weak"
    },
    {
      "candidate": "φ2 · R",
      "coeff_symbol": "\\delta",
      "coefficient": "-0.07372766417058024",
      "lambda_power": -1,
      "sector": "non-minimal",
      "relative_effect_to_EH": 5.98476382680305e-06,
      "effect_class": "weak"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000584_slot_06/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000584_slot_06/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000584_slot_06/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 56. task_000500_slot_16_lag_1  chi2=9434.002785

- best_validation_stage: `initial`
- validation_stage_counts: `{"initial": 1}`
- family_accepted_records: `1`
- delta_chi2_vs_LCDM: `7788.72278472`
- delta_AIC_vs_LCDM: `7796.72278472`
- delta_BIC_vs_LCDM: `7818.7824587`
- scalar_config: `phi2_only`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": null, "phi2": "quadratic"}`
- agent_parameter_sample_index: `809`
- H0_km_s_Mpc: `71.44453711`
- Omega_m0: `0.29872459`
- lambda_H_Lambda_over_H0: `6604.7042513`
- effective_correction_status: `weak`
- max_relative_effect_to_EH: `1.04905424e-06`
- dominant_correction_term: `φ2 · R`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-1} · φ2 · R )  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-0.0256458056) Λ^{-1} · φ2 · R )  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-1} · φ2 · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -0.0256458056 · Λ^{-1} · φ2 · R ) ] +
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
  "effective_correction_status": "weak",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 1.049054239595025e-06,
  "dominant_correction_term": "φ2 · R",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 1,
  "tiny_correction_terms": 0,
  "correction_term_count": 1,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "φ2 · R",
      "coeff_symbol": "\\beta",
      "coefficient": "-0.02564580560594258",
      "lambda_power": -1,
      "sector": "non-minimal",
      "relative_effect_to_EH": 1.049054239595025e-06,
      "effect_class": "weak"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000500_slot_16/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000500_slot_16/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000500_slot_16/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 57. task_000300_slot_09_lag_1  chi2=9434.0031

- best_validation_stage: `initial`
- validation_stage_counts: `{"initial": 1}`
- family_accepted_records: `1`
- delta_chi2_vs_LCDM: `7788.72309991`
- delta_AIC_vs_LCDM: `7798.72309991`
- delta_BIC_vs_LCDM: `7826.29648314`
- scalar_config: `phi2_only`
- proposal_group: `non_eh`
- theory_track: `non_eh`
- potential_types: `{"phi1": null, "phi2": "quadratic"}`
- agent_parameter_sample_index: `824`
- H0_km_s_Mpc: `68.66568913`
- Omega_m0: `0.2729692`
- lambda_H_Lambda_over_H0: `884.92142928`
- effective_correction_status: `not_applicable_non_eh`
- max_relative_effect_to_EH: ``
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha Λ^{-1} · φ2 · R )  +  \beta Λ^{1} · φ2 · φ2 · φ2  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (-0.0671147399) Λ^{-1} · φ2 · R )  +  (-5.1680752474e+12) Λ^{1} · φ2 · φ2 · φ2  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · Λ^{-1} · φ2 · R ) ] +
√(-g) [ \beta · Λ^{1} · φ2 · φ2 · φ2 ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( -0.0671147399 · Λ^{-1} · φ2 · R ) ] +
√(-g) [ -5.1680752474e+12 · Λ^{1} · φ2 · φ2 · φ2 ] +
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
  "effective_correction_status": "not_applicable_non_eh",
  "effective_correction_reason": "EH-relative correction diagnostic applies only to EH-anchored theories",
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000300_slot_09/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000300_slot_09/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000300_slot_09/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 58. task_000240_slot_06_lag_1  chi2=9434.0031

- best_validation_stage: `initial`
- validation_stage_counts: `{"initial": 1}`
- family_accepted_records: `1`
- delta_chi2_vs_LCDM: `7788.72310021`
- delta_AIC_vs_LCDM: `7798.72310021`
- delta_BIC_vs_LCDM: `7826.29648344`
- scalar_config: `phi2_only`
- proposal_group: `non_eh`
- theory_track: `non_eh`
- potential_types: `{"phi1": null, "phi2": "quadratic"}`
- agent_parameter_sample_index: `756`
- H0_km_s_Mpc: `59.89657208`
- Omega_m0: `0.27889276`
- lambda_H_Lambda_over_H0: `587.64835769`
- effective_correction_status: `not_applicable_non_eh`
- max_relative_effect_to_EH: ``
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha Λ^{-1} · φ2 · R )  +  \beta Λ^{-1} · φ2 · φ2 · ∇^{a}∇_{a}φ2  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (-0.0425378217) Λ^{-1} · φ2 · R )  +  (2.8180113673e+17) Λ^{-1} · φ2 · φ2 · ∇^{a}∇_{a}φ2  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · Λ^{-1} · φ2 · R ) ] +
√(-g) [ \beta · Λ^{-1} · φ2 · φ2 · ∇^{a}∇_{a}φ2 ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( -0.0425378217 · Λ^{-1} · φ2 · R ) ] +
√(-g) [ 2.8180113673e+17 · Λ^{-1} · φ2 · φ2 · ∇^{a}∇_{a}φ2 ] +
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
    "candidate": "φ2 · φ2 · ∇^{a}∇_{a}φ2",
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
  "effective_correction_status": "not_applicable_non_eh",
  "effective_correction_reason": "EH-relative correction diagnostic applies only to EH-anchored theories",
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000240_slot_06/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000240_slot_06/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000240_slot_06/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 59. task_000308_slot_09_lag_1  chi2=9434.003101

- best_validation_stage: `initial`
- validation_stage_counts: `{"initial": 2}`
- family_accepted_records: `2`
- delta_chi2_vs_LCDM: `7788.72310132`
- delta_AIC_vs_LCDM: `7796.72310132`
- delta_BIC_vs_LCDM: `7818.7827753`
- scalar_config: `phi2_only`
- proposal_group: `non_eh`
- theory_track: `non_eh`
- potential_types: `{"phi1": null, "phi2": "quadratic"}`
- agent_parameter_sample_index: `286`
- H0_km_s_Mpc: `66.88501353`
- Omega_m0: `0.28868974`
- lambda_H_Lambda_over_H0: `510.31922929`
- effective_correction_status: `not_applicable_non_eh`
- max_relative_effect_to_EH: ``
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha Λ^{-1} · φ2 · R )  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (-0.0297017359) Λ^{-1} · φ2 · R )  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · Λ^{-1} · φ2 · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( -0.0297017359 · Λ^{-1} · φ2 · R ) ] +
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
  "effective_correction_status": "not_applicable_non_eh",
  "effective_correction_reason": "EH-relative correction diagnostic applies only to EH-anchored theories",
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000308_slot_09/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000308_slot_09/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000308_slot_09/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 60. task_000312_slot_16_lag_1  chi2=9434.003132

- best_validation_stage: `initial`
- validation_stage_counts: `{"initial": 1}`
- family_accepted_records: `1`
- delta_chi2_vs_LCDM: `7788.72313188`
- delta_AIC_vs_LCDM: `7796.72313188`
- delta_BIC_vs_LCDM: `7818.78280587`
- scalar_config: `phi2_only`
- proposal_group: `non_eh`
- theory_track: `non_eh`
- potential_types: `{"phi1": null, "phi2": "quadratic"}`
- agent_parameter_sample_index: `379`
- H0_km_s_Mpc: `60.99463618`
- Omega_m0: `0.28580262`
- lambda_H_Lambda_over_H0: `1100.9475009`
- effective_correction_status: `not_applicable_non_eh`
- max_relative_effect_to_EH: ``
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha Λ^{-4} · ∇^{a}∇_{a}R · R^{c}_{c}  +  \beta Λ^{-1} · φ2 · R )  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (7.3457550814e+06) Λ^{-4} · ∇^{a}∇_{a}R · R^{c}_{c}  +  (-0.0236781615) Λ^{-1} · φ2 · R )  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · Λ^{-4} · ∇^{a}∇_{a}R · R^{c}_{c} ) ] +
√(-g) [ M_p² ( \beta · Λ^{-1} · φ2 · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 7.3457550814e+06 · Λ^{-4} · ∇^{a}∇_{a}R · R^{c}_{c} ) ] +
√(-g) [ M_p² ( -0.0236781615 · Λ^{-1} · φ2 · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Term Metadata

```json
[
  {
    "coeff_symbol": "\\alpha",
    "coeff_token": "COEFF_0",
    "candidate": "∇^{a}∇_{a}R · R^{c}_{c}",
    "mass_dim": 6,
    "lambda_power": -4,
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
  "effective_correction_status": "not_applicable_non_eh",
  "effective_correction_reason": "EH-relative correction diagnostic applies only to EH-anchored theories",
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000312_slot_16/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000312_slot_16/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000312_slot_16/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 61. task_000031_slot_03_lag_1  chi2=9434.003467

- best_validation_stage: `initial`
- validation_stage_counts: `{"initial": 1}`
- family_accepted_records: `1`
- delta_chi2_vs_LCDM: `7788.72346727`
- delta_AIC_vs_LCDM: `7802.72346727`
- delta_BIC_vs_LCDM: `7841.32426899`
- scalar_config: `phi2_only`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": null, "phi2": "quadratic"}`
- agent_parameter_sample_index: `252`
- H0_km_s_Mpc: `59.87141761`
- Omega_m0: `0.28014146`
- lambda_H_Lambda_over_H0: `3265.67117037`
- effective_correction_status: `moderate`
- max_relative_effect_to_EH: `1.04653082e-04`
- dominant_correction_term: `R · R^{ab} · R_{ab}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-2} · R^{ab} · R_{ab}  +  \gamma Λ^{-4} · R · R^{ab} · R_{ab}  +  \delta Λ^{-1} · φ2 · R  +  \epsilon Λ^{-3} · φ2 · φ2 · φ2 · R )  +  \zeta Λ^{2} · φ2 · φ2  +  \eta Λ^{-1} · φ2 · φ2 · ∇^{a}∇_{a}φ2  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (0.0017618552) Λ^{-2} · R^{ab} · R_{ab}  +  (5.9512999168e+09) Λ^{-4} · R · R^{ab} · R_{ab}  +  (-0.2368510007) Λ^{-1} · φ2 · R  +  (-2.3620193175e-09) Λ^{-3} · φ2 · φ2 · φ2 · R )  +  (6.1466682171e-10) Λ^{2} · φ2 · φ2  +  (-3.4512423723e+16) Λ^{-1} · φ2 · φ2 · ∇^{a}∇_{a}φ2  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-2} · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · R · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( \delta · Λ^{-1} · φ2 · R ) ] +
√(-g) [ M_p² ( \epsilon · Λ^{-3} · φ2 · φ2 · φ2 · R ) ] +
√(-g) [ \zeta · Λ^{2} · φ2 · φ2 ] +
√(-g) [ \eta · Λ^{-1} · φ2 · φ2 · ∇^{a}∇_{a}φ2 ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 0.0017618552 · Λ^{-2} · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( 5.9512999168e+09 · Λ^{-4} · R · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( -0.2368510007 · Λ^{-1} · φ2 · R ) ] +
√(-g) [ M_p² ( -2.3620193175e-09 · Λ^{-3} · φ2 · φ2 · φ2 · R ) ] +
√(-g) [ 6.1466682171e-10 · Λ^{2} · φ2 · φ2 ] +
√(-g) [ -3.4512423723e+16 · Λ^{-1} · φ2 · φ2 · ∇^{a}∇_{a}φ2 ] +
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
    "candidate": "R^{ab} · R_{ab}",
    "mass_dim": 4,
    "lambda_power": -2,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\gamma",
    "coeff_token": "COEFF_2",
    "candidate": "R · R^{ab} · R_{ab}",
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
    "candidate": "φ2 · φ2 · φ2 · R",
    "mass_dim": 5,
    "lambda_power": -3,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\zeta",
    "coeff_token": "COEFF_5",
    "candidate": "φ2 · φ2",
    "mass_dim": 2,
    "lambda_power": 2,
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
  "effective_correction_status": "moderate",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 0.00010465308225476114,
  "dominant_correction_term": "R · R^{ab} · R_{ab}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 1,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 3,
  "correction_term_count": 4,
  "tiny_correction_fraction": 0.75,
  "term_effects": [
    {
      "candidate": "R^{ab} · R_{ab}",
      "coeff_symbol": "\\beta",
      "coefficient": "0.0017618552452568419",
      "lambda_power": -2,
      "sector": "gravity",
      "relative_effect_to_EH": 3.304116219508316e-10,
      "effect_class": "tiny"
    },
    {
      "candidate": "R · R^{ab} · R_{ab}",
      "coeff_symbol": "\\gamma",
      "coefficient": "5951299916.760467",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 0.00010465308225476114,
      "effect_class": "moderate"
    },
    {
      "candidate": "φ2 · R",
      "coeff_symbol": "\\delta",
      "coefficient": "-0.23685100067596057",
      "lambda_power": -1,
      "sector": "non-minimal",
      "relative_effect_to_EH": 8.572163644799029e-07,
      "effect_class": "tiny"
    },
    {
      "candidate": "φ2 · φ2 · φ2 · R",
      "coeff_symbol": "\\epsilon",
      "coefficient": "-2.362019317534992e-09",
      "lambda_power": -3,
      "sector": "non-minimal",
      "relative_effect_to_EH": 2.799426966226442e-26,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000031_slot_03/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000031_slot_03/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000031_slot_03/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 62. task_000099_slot_01_lag_1  chi2=9434.005409

- best_validation_stage: `initial`
- validation_stage_counts: `{"initial": 1}`
- family_accepted_records: `1`
- delta_chi2_vs_LCDM: `7788.72540904`
- delta_AIC_vs_LCDM: `7802.72540904`
- delta_BIC_vs_LCDM: `7841.32621077`
- scalar_config: `both`
- proposal_group: `non_eh`
- theory_track: `non_eh`
- potential_types: `{"phi1": "quadratic", "phi2": "quadratic"}`
- agent_parameter_sample_index: `26`
- H0_km_s_Mpc: `68.13600191`
- Omega_m0: `0.31206374`
- lambda_H_Lambda_over_H0: `2291.31584314`
- effective_correction_status: `not_applicable_non_eh`
- max_relative_effect_to_EH: ``
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd}  +  \beta Λ^{-1} · φ2 · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (566.6279295511) Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd}  +  (2.6132454978e+04) Λ^{-1} · φ2 · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( \beta · Λ^{-1} · φ2 · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 566.6279295511 · Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( 2.6132454978e+04 · Λ^{-1} · φ2 · R ) ] +
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
    "candidate": "R^{bcd}_{a} · R^{a}_{bcd}",
    "mass_dim": 4,
    "lambda_power": -2,
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
  "effective_correction_status": "not_applicable_non_eh",
  "effective_correction_reason": "EH-relative correction diagnostic applies only to EH-anchored theories",
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000099_slot_01/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000099_slot_01/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000099_slot_01/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 63. task_000218_slot_09_lag_1  chi2=9434.006364

- best_validation_stage: `initial`
- validation_stage_counts: `{"initial": 1}`
- family_accepted_records: `1`
- delta_chi2_vs_LCDM: `7788.7263636`
- delta_AIC_vs_LCDM: `7798.7263636`
- delta_BIC_vs_LCDM: `7826.29974683`
- scalar_config: `phi2_only`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": null, "phi2": "axion"}`
- agent_parameter_sample_index: `17`
- H0_km_s_Mpc: `62.04010258`
- Omega_m0: `0.31301828`
- lambda_H_Lambda_over_H0: `715.61939639`
- effective_correction_status: `weak`
- max_relative_effect_to_EH: `1.25892541e-06`
- dominant_correction_term: `φ2 · φ2 · R`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-2} · φ2 · φ2 · R )  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-2.1716456939) Λ^{-2} · φ2 · φ2 · R )  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-2} · φ2 · φ2 · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -2.1716456939 · Λ^{-2} · φ2 · φ2 · R ) ] +
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
  "effective_correction_status": "weak",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 1.2589254117941661e-06,
  "dominant_correction_term": "φ2 · φ2 · R",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 1,
  "tiny_correction_terms": 0,
  "correction_term_count": 1,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "φ2 · φ2 · R",
      "coeff_symbol": "\\beta",
      "coefficient": "-2.171645693872574",
      "lambda_power": -2,
      "sector": "non-minimal",
      "relative_effect_to_EH": 1.2589254117941661e-06,
      "effect_class": "weak"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000218_slot_09/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000218_slot_09/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000218_slot_09/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 64. task_000146_slot_13_lag_1  chi2=9434.006431

- best_validation_stage: `initial`
- validation_stage_counts: `{"initial": 1}`
- family_accepted_records: `1`
- delta_chi2_vs_LCDM: `7788.72643069`
- delta_AIC_vs_LCDM: `7798.72643069`
- delta_BIC_vs_LCDM: `7826.29981392`
- scalar_config: `phi2_only`
- proposal_group: `non_eh`
- theory_track: `non_eh`
- potential_types: `{"phi1": null, "phi2": "axion"}`
- agent_parameter_sample_index: `868`
- H0_km_s_Mpc: `74`
- Omega_m0: `0.22496515`
- lambda_H_Lambda_over_H0: `2112.48002952`
- effective_correction_status: `not_applicable_non_eh`
- max_relative_effect_to_EH: ``
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha Λ^{-3} · φ2 · φ2 · φ2 · R )  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (1.1493536048e+13) Λ^{-3} · φ2 · φ2 · φ2 · R )  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · Λ^{-3} · φ2 · φ2 · φ2 · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 1.1493536048e+13 · Λ^{-3} · φ2 · φ2 · φ2 · R ) ] +
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
  "effective_correction_status": "not_applicable_non_eh",
  "effective_correction_reason": "EH-relative correction diagnostic applies only to EH-anchored theories",
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000146_slot_13/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000146_slot_13/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000146_slot_13/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 65. task_000434_slot_03_lag_1  chi2=9434.00644

- best_validation_stage: `initial`
- validation_stage_counts: `{"initial": 1}`
- family_accepted_records: `1`
- delta_chi2_vs_LCDM: `7788.7264401`
- delta_AIC_vs_LCDM: `7798.7264401`
- delta_BIC_vs_LCDM: `7826.29982333`
- scalar_config: `phi2_only`
- proposal_group: `non_eh`
- theory_track: `non_eh`
- potential_types: `{"phi1": null, "phi2": "axion"}`
- agent_parameter_sample_index: `533`
- H0_km_s_Mpc: `74`
- Omega_m0: `0.36025505`
- lambda_H_Lambda_over_H0: `500`
- effective_correction_status: `not_applicable_non_eh`
- max_relative_effect_to_EH: ``
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha Λ^{-2} · R · R  +  \beta Λ^{-2} · R^{ab} · R_{ab}  +  \gamma Λ^{-4} · R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh}  +  \delta Λ^{-4} · ∇^{a}R · ∇_{a}R  +  \epsilon Λ^{-2} · φ2 · φ2 · R  +  \zeta Λ^{-4} · φ2 · φ2 · R^{ab} · R_{ab} )  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (-1.455111906) Λ^{-2} · R · R  +  (3.2714564719) Λ^{-2} · R^{ab} · R_{ab}  +  (8.5553328298e+04) Λ^{-4} · R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh}  +  (-1.1455357193e+05) Λ^{-4} · ∇^{a}R · ∇_{a}R  +  (9563.7986071382) Λ^{-2} · φ2 · φ2 · R  +  (-1.3965044927e+10) Λ^{-4} · φ2 · φ2 · R^{ab} · R_{ab} )  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · Λ^{-2} · R · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-2} · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh} ) ] +
√(-g) [ M_p² ( \delta · Λ^{-4} · ∇^{a}R · ∇_{a}R ) ] +
√(-g) [ M_p² ( \epsilon · Λ^{-2} · φ2 · φ2 · R ) ] +
√(-g) [ M_p² ( \zeta · Λ^{-4} · φ2 · φ2 · R^{ab} · R_{ab} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( -1.455111906 · Λ^{-2} · R · R ) ] +
√(-g) [ M_p² ( 3.2714564719 · Λ^{-2} · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( 8.5553328298e+04 · Λ^{-4} · R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh} ) ] +
√(-g) [ M_p² ( -1.1455357193e+05 · Λ^{-4} · ∇^{a}R · ∇_{a}R ) ] +
√(-g) [ M_p² ( 9563.7986071382 · Λ^{-2} · φ2 · φ2 · R ) ] +
√(-g) [ M_p² ( -1.3965044927e+10 · Λ^{-4} · φ2 · φ2 · R^{ab} · R_{ab} ) ] +
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
    "candidate": "R^{ab} · R_{ab}",
    "mass_dim": 4,
    "lambda_power": -2,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\gamma",
    "coeff_token": "COEFF_2",
    "candidate": "R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\delta",
    "coeff_token": "COEFF_3",
    "candidate": "∇^{a}R · ∇_{a}R",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\epsilon",
    "coeff_token": "COEFF_4",
    "candidate": "φ2 · φ2 · R",
    "mass_dim": 4,
    "lambda_power": -2,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\zeta",
    "coeff_token": "COEFF_5",
    "candidate": "φ2 · φ2 · R^{ab} · R_{ab}",
    "mass_dim": 6,
    "lambda_power": -4,
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
  "effective_correction_status": "not_applicable_non_eh",
  "effective_correction_reason": "EH-relative correction diagnostic applies only to EH-anchored theories",
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000434_slot_03/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000434_slot_03/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000434_slot_03/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 66. task_000376_slot_11_lag_1  chi2=9434.006826

- best_validation_stage: `initial`
- validation_stage_counts: `{"initial": 1}`
- family_accepted_records: `1`
- delta_chi2_vs_LCDM: `7788.72682583`
- delta_AIC_vs_LCDM: `7806.72682583`
- delta_BIC_vs_LCDM: `7856.35504605`
- scalar_config: `both`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "axion", "phi2": "axion"}`
- agent_parameter_sample_index: `958`
- H0_km_s_Mpc: `65.0884228`
- Omega_m0: `0.27602017`
- lambda_H_Lambda_over_H0: `2812.64572142`
- effective_correction_status: `eh_dominated`
- max_relative_effect_to_EH: `1.71768224e-11`
- dominant_correction_term: `φ2 · φ2 · φ2 · R`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-3} · φ2 · φ2 · φ2 · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-1.9703027976e+07) Λ^{-3} · φ2 · φ2 · φ2 · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-3} · φ2 · φ2 · φ2 · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -1.9703027976e+07 · Λ^{-3} · φ2 · φ2 · φ2 · R ) ] +
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
    "candidate": "φ2 · φ2 · φ2 · R",
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
  "max_relative_effect_to_EH": 1.7176822385903876e-11,
  "dominant_correction_term": "φ2 · φ2 · φ2 · R",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 1,
  "correction_term_count": 1,
  "tiny_correction_fraction": 1.0,
  "term_effects": [
    {
      "candidate": "φ2 · φ2 · φ2 · R",
      "coeff_symbol": "\\beta",
      "coefficient": "-19703027.976091877",
      "lambda_power": -3,
      "sector": "non-minimal",
      "relative_effect_to_EH": 1.7176822385903876e-11,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000376_slot_11/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000376_slot_11/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000376_slot_11/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 67. task_000519_slot_08_lag_1  chi2=9434.006957

- best_validation_stage: `initial`
- validation_stage_counts: `{"initial": 1}`
- family_accepted_records: `1`
- delta_chi2_vs_LCDM: `7788.7269569`
- delta_AIC_vs_LCDM: `7796.7269569`
- delta_BIC_vs_LCDM: `7818.78663089`
- scalar_config: `phi2_only`
- proposal_group: `non_eh`
- theory_track: `non_eh`
- potential_types: `{"phi1": null, "phi2": "quadratic"}`
- agent_parameter_sample_index: `713`
- H0_km_s_Mpc: `71.22149865`
- Omega_m0: `0.28703085`
- lambda_H_Lambda_over_H0: `4073.89380167`
- effective_correction_status: `not_applicable_non_eh`
- max_relative_effect_to_EH: ``
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha Λ^{-3} · φ2 · φ2 · φ2 · R  +  \beta Λ^{-4} · ∇^{a}φ2 · ∇_{a}φ2 · R )  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (6.3990063317) Λ^{-3} · φ2 · φ2 · φ2 · R  +  (-2.2577793924e+16) Λ^{-4} · ∇^{a}φ2 · ∇_{a}φ2 · R )  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · Λ^{-3} · φ2 · φ2 · φ2 · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · ∇^{a}φ2 · ∇_{a}φ2 · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 6.3990063317 · Λ^{-3} · φ2 · φ2 · φ2 · R ) ] +
√(-g) [ M_p² ( -2.2577793924e+16 · Λ^{-4} · ∇^{a}φ2 · ∇_{a}φ2 · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
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
    "candidate": "∇^{a}φ2 · ∇_{a}φ2 · R",
    "mass_dim": 6,
    "lambda_power": -4,
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
  "effective_correction_status": "not_applicable_non_eh",
  "effective_correction_reason": "EH-relative correction diagnostic applies only to EH-anchored theories",
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000519_slot_08/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000519_slot_08/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000519_slot_08/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 68. task_000579_slot_15_lag_1  chi2=9434.006971

- best_validation_stage: `initial`
- validation_stage_counts: `{"initial": 1}`
- family_accepted_records: `1`
- delta_chi2_vs_LCDM: `7788.72697114`
- delta_AIC_vs_LCDM: `7800.72697114`
- delta_BIC_vs_LCDM: `7833.81406361`
- scalar_config: `phi2_only`
- proposal_group: `non_eh`
- theory_track: `non_eh`
- potential_types: `{"phi1": null, "phi2": "axion"}`
- agent_parameter_sample_index: `589`
- H0_km_s_Mpc: `62.12837716`
- Omega_m0: `0.33179561`
- lambda_H_Lambda_over_H0: `541.35558148`
- effective_correction_status: `not_applicable_non_eh`
- max_relative_effect_to_EH: ``
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha Λ^{-2} · φ2 · φ2 · R )  +  \beta Λ^{-2} · φ2 · φ2 · φ2 · ∇^{a}∇_{a}φ2  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (-4.0081086622) Λ^{-2} · φ2 · φ2 · R )  +  (717.5780832464) Λ^{-2} · φ2 · φ2 · φ2 · ∇^{a}∇_{a}φ2  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · Λ^{-2} · φ2 · φ2 · R ) ] +
√(-g) [ \beta · Λ^{-2} · φ2 · φ2 · φ2 · ∇^{a}∇_{a}φ2 ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( -4.0081086622 · Λ^{-2} · φ2 · φ2 · R ) ] +
√(-g) [ 717.5780832464 · Λ^{-2} · φ2 · φ2 · φ2 · ∇^{a}∇_{a}φ2 ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Term Metadata

```json
[
  {
    "coeff_symbol": "\\alpha",
    "coeff_token": "COEFF_0",
    "candidate": "φ2 · φ2 · R",
    "mass_dim": 4,
    "lambda_power": -2,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\beta",
    "coeff_token": "COEFF_1",
    "candidate": "φ2 · φ2 · φ2 · ∇^{a}∇_{a}φ2",
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
  "effective_correction_status": "not_applicable_non_eh",
  "effective_correction_reason": "EH-relative correction diagnostic applies only to EH-anchored theories",
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000579_slot_15/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000579_slot_15/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000579_slot_15/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 69. task_000236_slot_02_lag_1  chi2=9434.006977

- best_validation_stage: `initial`
- validation_stage_counts: `{"initial": 1}`
- family_accepted_records: `1`
- delta_chi2_vs_LCDM: `7788.72697691`
- delta_AIC_vs_LCDM: `7804.72697691`
- delta_BIC_vs_LCDM: `7848.84148788`
- scalar_config: `both`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "quadratic", "phi2": "axion"}`
- agent_parameter_sample_index: `243`
- H0_km_s_Mpc: `66.18241761`
- Omega_m0: `0.28069777`
- lambda_H_Lambda_over_H0: `1670.46151165`
- effective_correction_status: `moderate`
- max_relative_effect_to_EH: `0.00664833`
- dominant_correction_term: `φ2 · R`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-1} · φ2 · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-267.3338685606) Λ^{-1} · φ2 · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-1} · φ2 · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -267.3338685606 · Λ^{-1} · φ2 · R ) ] +
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
    "candidate": "φ2 · R",
    "mass_dim": 3,
    "lambda_power": -1,
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
  "max_relative_effect_to_EH": 0.006648331041877831,
  "dominant_correction_term": "φ2 · R",
  "active_correction_terms": 0,
  "moderate_correction_terms": 1,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 0,
  "correction_term_count": 1,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "φ2 · R",
      "coeff_symbol": "\\beta",
      "coefficient": "-267.3338685605572",
      "lambda_power": -1,
      "sector": "non-minimal",
      "relative_effect_to_EH": 0.006648331041877831,
      "effect_class": "moderate"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000236_slot_02/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000236_slot_02/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000236_slot_02/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 70. task_000445_slot_02_lag_1  chi2=9434.00698

- best_validation_stage: `initial`
- validation_stage_counts: `{"initial": 2}`
- family_accepted_records: `2`
- delta_chi2_vs_LCDM: `7788.72698037`
- delta_AIC_vs_LCDM: `7796.72698037`
- delta_BIC_vs_LCDM: `7818.78665435`
- scalar_config: `phi2_only`
- proposal_group: `non_eh`
- theory_track: `non_eh`
- potential_types: `{"phi1": null, "phi2": "quadratic"}`
- agent_parameter_sample_index: `865`
- H0_km_s_Mpc: `61.29409813`
- Omega_m0: `0.33614026`
- lambda_H_Lambda_over_H0: `873.97230832`
- effective_correction_status: `not_applicable_non_eh`
- max_relative_effect_to_EH: ``
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha Λ^{-2} · φ2 · φ2 · R )  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (-1.0399219285) Λ^{-2} · φ2 · φ2 · R )  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · Λ^{-2} · φ2 · φ2 · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( -1.0399219285 · Λ^{-2} · φ2 · φ2 · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Term Metadata

```json
[
  {
    "coeff_symbol": "\\alpha",
    "coeff_token": "COEFF_0",
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
  "effective_correction_status": "not_applicable_non_eh",
  "effective_correction_reason": "EH-relative correction diagnostic applies only to EH-anchored theories",
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000445_slot_02/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000445_slot_02/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000445_slot_02/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 71. task_000117_slot_09_lag_1  chi2=9434.006983

- best_validation_stage: `initial`
- validation_stage_counts: `{"initial": 1}`
- family_accepted_records: `1`
- delta_chi2_vs_LCDM: `7788.72698292`
- delta_AIC_vs_LCDM: `7800.72698292`
- delta_BIC_vs_LCDM: `7833.8140754`
- scalar_config: `phi2_only`
- proposal_group: `non_eh`
- theory_track: `non_eh`
- potential_types: `{"phi1": null, "phi2": "quadratic"}`
- agent_parameter_sample_index: `625`
- H0_km_s_Mpc: `61.85340639`
- Omega_m0: `0.34259857`
- lambda_H_Lambda_over_H0: `500`
- effective_correction_status: `not_applicable_non_eh`
- max_relative_effect_to_EH: ``
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha Λ^{-2} · ∇^{a}∇_{a}R  +  \beta Λ^{-4} · R · R^{bcd}_{a} · R^{a}_{bcd}  +  \gamma Λ^{-2} · φ2 · φ2 · R )  +  \delta Λ^{2} · φ2 · φ2  +  \epsilon · φ2 · ∇^{a}∇_{a}φ2  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.7279174516) Λ^{-2} · ∇^{a}∇_{a}R  +  (-1.9803464968e+05) Λ^{-4} · R · R^{bcd}_{a} · R^{a}_{bcd}  +  (-3.0264633424) Λ^{-2} · φ2 · φ2 · R )  +  (0.4737631093) Λ^{2} · φ2 · φ2  +  (0.5028987585) · φ2 · ∇^{a}∇_{a}φ2  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · Λ^{-2} · ∇^{a}∇_{a}R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · R · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-2} · φ2 · φ2 · R ) ] +
√(-g) [ \delta · Λ^{2} · φ2 · φ2 ] +
√(-g) [ \epsilon · φ2 · ∇^{a}∇_{a}φ2 ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.7279174516 · Λ^{-2} · ∇^{a}∇_{a}R ) ] +
√(-g) [ M_p² ( -1.9803464968e+05 · Λ^{-4} · R · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( -3.0264633424 · Λ^{-2} · φ2 · φ2 · R ) ] +
√(-g) [ 0.4737631093 · Λ^{2} · φ2 · φ2 ] +
√(-g) [ 0.5028987585 · φ2 · ∇^{a}∇_{a}φ2 ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Term Metadata

```json
[
  {
    "coeff_symbol": "\\alpha",
    "coeff_token": "COEFF_0",
    "candidate": "∇^{a}∇_{a}R",
    "mass_dim": 4,
    "lambda_power": -2,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\beta",
    "coeff_token": "COEFF_1",
    "candidate": "R · R^{bcd}_{a} · R^{a}_{bcd}",
    "mass_dim": 6,
    "lambda_power": -4,
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
    "candidate": "φ2 · φ2",
    "mass_dim": 2,
    "lambda_power": 2,
    "sector": "scalar"
  },
  {
    "coeff_symbol": "\\epsilon",
    "coeff_token": "COEFF_4",
    "candidate": "φ2 · ∇^{a}∇_{a}φ2",
    "mass_dim": 4,
    "lambda_power": 0,
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
  "effective_correction_status": "not_applicable_non_eh",
  "effective_correction_reason": "EH-relative correction diagnostic applies only to EH-anchored theories",
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000117_slot_09/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000117_slot_09/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000117_slot_09/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 72. task_000281_slot_12_lag_1  chi2=9434.007052

- best_validation_stage: `initial`
- validation_stage_counts: `{"initial": 1}`
- family_accepted_records: `1`
- delta_chi2_vs_LCDM: `7788.72705232`
- delta_AIC_vs_LCDM: `7796.72705232`
- delta_BIC_vs_LCDM: `7818.78672631`
- scalar_config: `phi2_only`
- proposal_group: `non_eh`
- theory_track: `non_eh`
- potential_types: `{"phi1": null, "phi2": "quadratic"}`
- agent_parameter_sample_index: `423`
- H0_km_s_Mpc: `71.64294206`
- Omega_m0: `0.3103626`
- lambda_H_Lambda_over_H0: `652.4846051`
- effective_correction_status: `not_applicable_non_eh`
- max_relative_effect_to_EH: ``
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha Λ^{-2} · R · R  +  \beta Λ^{-2} · φ2 · φ2 · R  +  \gamma Λ^{-3} · φ2 · R · R  +  \delta Λ^{-4} · φ2 · φ2 · R^{ab} · R_{ab} )  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (8.4744309009) Λ^{-2} · R · R  +  (-136.019520231) Λ^{-2} · φ2 · φ2 · R  +  (2.4855709246e+05) Λ^{-3} · φ2 · R · R  +  (-2.3053760507e+08) Λ^{-4} · φ2 · φ2 · R^{ab} · R_{ab} )  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · Λ^{-2} · R · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-2} · φ2 · φ2 · R ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-3} · φ2 · R · R ) ] +
√(-g) [ M_p² ( \delta · Λ^{-4} · φ2 · φ2 · R^{ab} · R_{ab} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 8.4744309009 · Λ^{-2} · R · R ) ] +
√(-g) [ M_p² ( -136.019520231 · Λ^{-2} · φ2 · φ2 · R ) ] +
√(-g) [ M_p² ( 2.4855709246e+05 · Λ^{-3} · φ2 · R · R ) ] +
√(-g) [ M_p² ( -2.3053760507e+08 · Λ^{-4} · φ2 · φ2 · R^{ab} · R_{ab} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
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
    "candidate": "φ2 · φ2 · R",
    "mass_dim": 4,
    "lambda_power": -2,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\gamma",
    "coeff_token": "COEFF_2",
    "candidate": "φ2 · R · R",
    "mass_dim": 5,
    "lambda_power": -3,
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
  "effective_correction_status": "not_applicable_non_eh",
  "effective_correction_reason": "EH-relative correction diagnostic applies only to EH-anchored theories",
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000281_slot_12/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000281_slot_12/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000281_slot_12/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 73. task_000315_slot_03_lag_1  chi2=9434.00708

- best_validation_stage: `initial`
- validation_stage_counts: `{"initial": 1}`
- family_accepted_records: `1`
- delta_chi2_vs_LCDM: `7788.72708046`
- delta_AIC_vs_LCDM: `7804.72708046`
- delta_BIC_vs_LCDM: `7848.84159143`
- scalar_config: `both`
- proposal_group: `non_eh`
- theory_track: `non_eh`
- potential_types: `{"phi1": "axion", "phi2": "quadratic"}`
- agent_parameter_sample_index: `68`
- H0_km_s_Mpc: `72.92841098`
- Omega_m0: `0.23129546`
- lambda_H_Lambda_over_H0: `2751.41173367`
- effective_correction_status: `not_applicable_non_eh`
- max_relative_effect_to_EH: ``
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha Λ^{-1} · φ2 · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (158.6931293444) Λ^{-1} · φ2 · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · Λ^{-1} · φ2 · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 158.6931293444 · Λ^{-1} · φ2 · R ) ] +
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
    "candidate": "φ2 · R",
    "mass_dim": 3,
    "lambda_power": -1,
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
  "effective_correction_status": "not_applicable_non_eh",
  "effective_correction_reason": "EH-relative correction diagnostic applies only to EH-anchored theories",
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000315_slot_03/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000315_slot_03/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000315_slot_03/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 74. task_000424_slot_05_lag_1  chi2=9434.00728

- best_validation_stage: `initial`
- validation_stage_counts: `{"initial": 1}`
- family_accepted_records: `1`
- delta_chi2_vs_LCDM: `7788.72728028`
- delta_AIC_vs_LCDM: `7806.72728028`
- delta_BIC_vs_LCDM: `7856.35550051`
- scalar_config: `both`
- proposal_group: `non_eh`
- theory_track: `non_eh`
- potential_types: `{"phi1": "axion", "phi2": "axion"}`
- agent_parameter_sample_index: `753`
- H0_km_s_Mpc: `72.567209`
- Omega_m0: `0.26782759`
- lambda_H_Lambda_over_H0: `1803.27529578`
- effective_correction_status: `not_applicable_non_eh`
- max_relative_effect_to_EH: ``
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha Λ^{-1} · φ2 · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.1819907854) Λ^{-1} · φ2 · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · Λ^{-1} · φ2 · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.1819907854 · Λ^{-1} · φ2 · R ) ] +
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
    "candidate": "φ2 · R",
    "mass_dim": 3,
    "lambda_power": -1,
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
  "effective_correction_status": "not_applicable_non_eh",
  "effective_correction_reason": "EH-relative correction diagnostic applies only to EH-anchored theories",
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000424_slot_05/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000424_slot_05/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000424_slot_05/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 75. task_000092_slot_01_lag_1  chi2=9434.007353

- best_validation_stage: `initial`
- validation_stage_counts: `{"initial": 1}`
- family_accepted_records: `1`
- delta_chi2_vs_LCDM: `7788.7273534`
- delta_AIC_vs_LCDM: `7804.7273534`
- delta_BIC_vs_LCDM: `7848.84186437`
- scalar_config: `both`
- proposal_group: `non_eh`
- theory_track: `non_eh`
- potential_types: `{"phi1": "quadratic", "phi2": "axion"}`
- agent_parameter_sample_index: `709`
- H0_km_s_Mpc: `61.22496296`
- Omega_m0: `0.29413771`
- lambda_H_Lambda_over_H0: `1644.50588899`
- effective_correction_status: `not_applicable_non_eh`
- max_relative_effect_to_EH: ``
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha Λ^{-1} · φ2 · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (6.0971037931e+04) Λ^{-1} · φ2 · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · Λ^{-1} · φ2 · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 6.0971037931e+04 · Λ^{-1} · φ2 · R ) ] +
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
    "candidate": "φ2 · R",
    "mass_dim": 3,
    "lambda_power": -1,
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
  "effective_correction_status": "not_applicable_non_eh",
  "effective_correction_reason": "EH-relative correction diagnostic applies only to EH-anchored theories",
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000092_slot_01/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000092_slot_01/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000092_slot_01/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 76. task_000592_slot_02_lag_1  chi2=9434.007446

- best_validation_stage: `initial`
- validation_stage_counts: `{"initial": 1}`
- family_accepted_records: `1`
- delta_chi2_vs_LCDM: `7788.72744586`
- delta_AIC_vs_LCDM: `7804.72744586`
- delta_BIC_vs_LCDM: `7848.84195683`
- scalar_config: `both`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "axion", "phi2": "quadratic"}`
- agent_parameter_sample_index: `617`
- H0_km_s_Mpc: `70.17893965`
- Omega_m0: `0.30811923`
- lambda_H_Lambda_over_H0: `4654.17776614`
- effective_correction_status: `eh_dominated`
- max_relative_effect_to_EH: `7.23877120e-08`
- dominant_correction_term: `φ2 · R`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-1} · φ2 · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (2.2104772216) Λ^{-1} · φ2 · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-1} · φ2 · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 2.2104772216 · Λ^{-1} · φ2 · R ) ] +
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
    "candidate": "φ2 · R",
    "mass_dim": 3,
    "lambda_power": -1,
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
  "max_relative_effect_to_EH": 7.238771195135713e-08,
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
      "coefficient": "2.2104772216450668",
      "lambda_power": -1,
      "sector": "non-minimal",
      "relative_effect_to_EH": 7.238771195135713e-08,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000592_slot_02/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000592_slot_02/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000592_slot_02/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 77. task_000265_slot_15_lag_1  chi2=9434.007467

- best_validation_stage: `initial`
- validation_stage_counts: `{"initial": 1}`
- family_accepted_records: `1`
- delta_chi2_vs_LCDM: `7788.7274671`
- delta_AIC_vs_LCDM: `7804.7274671`
- delta_BIC_vs_LCDM: `7848.84197807`
- scalar_config: `both`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "axion", "phi2": "quadratic"}`
- agent_parameter_sample_index: `599`
- H0_km_s_Mpc: `58.91114134`
- Omega_m0: `0.27345676`
- lambda_H_Lambda_over_H0: `2615.23697764`
- effective_correction_status: `eh_dominated`
- max_relative_effect_to_EH: `1.59749303e-10`
- dominant_correction_term: `φ2 · φ2 · R`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-2} · φ2 · φ2 · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (1.5433476395e+06) Λ^{-2} · φ2 · φ2 · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-2} · φ2 · φ2 · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 1.5433476395e+06 · Λ^{-2} · φ2 · φ2 · R ) ] +
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
    "candidate": "φ2 · φ2 · R",
    "mass_dim": 4,
    "lambda_power": -2,
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
  "max_relative_effect_to_EH": 1.5974930286648978e-10,
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
      "coefficient": "1543347.639470034",
      "lambda_power": -2,
      "sector": "non-minimal",
      "relative_effect_to_EH": 1.5974930286648978e-10,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000265_slot_15/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000265_slot_15/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000265_slot_15/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 78. task_000132_slot_12_lag_1  chi2=9434.007473

- best_validation_stage: `initial`
- validation_stage_counts: `{"initial": 1}`
- family_accepted_records: `1`
- delta_chi2_vs_LCDM: `7788.72747338`
- delta_AIC_vs_LCDM: `7804.72747338`
- delta_BIC_vs_LCDM: `7848.84198435`
- scalar_config: `both`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "quadratic", "phi2": "axion"}`
- agent_parameter_sample_index: `105`
- H0_km_s_Mpc: `62.04496256`
- Omega_m0: `0.2857804`
- lambda_H_Lambda_over_H0: `1737.97469309`
- effective_correction_status: `eh_dominated`
- max_relative_effect_to_EH: `5.04111475e-10`
- dominant_correction_term: `φ2 · φ2 · R`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-2} · φ2 · φ2 · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (7.6134847888e+06) Λ^{-2} · φ2 · φ2 · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-2} · φ2 · φ2 · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 7.6134847888e+06 · Λ^{-2} · φ2 · φ2 · R ) ] +
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
    "candidate": "φ2 · φ2 · R",
    "mass_dim": 4,
    "lambda_power": -2,
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
  "max_relative_effect_to_EH": 5.041114750813064e-10,
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
      "coefficient": "7613484.788844187",
      "lambda_power": -2,
      "sector": "non-minimal",
      "relative_effect_to_EH": 5.041114750813064e-10,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000132_slot_12/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000132_slot_12/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000132_slot_12/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 79. task_000275_slot_01_lag_1  chi2=9434.007504

- best_validation_stage: `initial`
- validation_stage_counts: `{"initial": 1}`
- family_accepted_records: `1`
- delta_chi2_vs_LCDM: `7788.72750405`
- delta_AIC_vs_LCDM: `7804.72750405`
- delta_BIC_vs_LCDM: `7848.84201502`
- scalar_config: `phi2_only`
- proposal_group: `non_eh`
- theory_track: `non_eh`
- potential_types: `{"phi1": null, "phi2": "axion"}`
- agent_parameter_sample_index: `813`
- H0_km_s_Mpc: `63.18905637`
- Omega_m0: `0.30105982`
- lambda_H_Lambda_over_H0: `1449.28610328`
- effective_correction_status: `not_applicable_non_eh`
- max_relative_effect_to_EH: ``
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf}  +  \beta Λ^{-3} · φ2 · φ2 · φ2 · R  +  \gamma Λ^{-3} · φ2 · R^{bcd}_{a} · R^{a}_{bcd}  +  \delta Λ^{-4} · φ2 · φ2 · R^{ab} · R_{ab} )  +  \epsilon Λ^{1} · ∇^{a}∇_{a}φ2  +  \zeta · φ2 · φ2 · φ2 · φ2  +  \eta Λ^{-1} · φ2 · φ2 · ∇^{a}∇_{a}φ2  +  \theta Λ^{-2} · φ2 · φ2 · φ2 · ∇^{a}∇_{a}φ2  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (5.3240978108e+09) Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf}  +  (-149.1439668864) Λ^{-3} · φ2 · φ2 · φ2 · R  +  (-1053.542535135) Λ^{-3} · φ2 · R^{bcd}_{a} · R^{a}_{bcd}  +  (-3.1848502985e-06) Λ^{-4} · φ2 · φ2 · R^{ab} · R_{ab} )  +  (-984.2254811036) Λ^{1} · ∇^{a}∇_{a}φ2  +  (-8.5564353371e+16) · φ2 · φ2 · φ2 · φ2  +  (1.0845026769e+19) Λ^{-1} · φ2 · φ2 · ∇^{a}∇_{a}φ2  +  (497.5457896739) Λ^{-2} · φ2 · φ2 · φ2 · ∇^{a}∇_{a}φ2  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf} ) ] +
√(-g) [ M_p² ( \beta · Λ^{-3} · φ2 · φ2 · φ2 · R ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-3} · φ2 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( \delta · Λ^{-4} · φ2 · φ2 · R^{ab} · R_{ab} ) ] +
√(-g) [ \epsilon · Λ^{1} · ∇^{a}∇_{a}φ2 ] +
√(-g) [ \zeta · φ2 · φ2 · φ2 · φ2 ] +
√(-g) [ \eta · Λ^{-1} · φ2 · φ2 · ∇^{a}∇_{a}φ2 ] +
√(-g) [ \theta · Λ^{-2} · φ2 · φ2 · φ2 · ∇^{a}∇_{a}φ2 ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 5.3240978108e+09 · Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf} ) ] +
√(-g) [ M_p² ( -149.1439668864 · Λ^{-3} · φ2 · φ2 · φ2 · R ) ] +
√(-g) [ M_p² ( -1053.542535135 · Λ^{-3} · φ2 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( -3.1848502985e-06 · Λ^{-4} · φ2 · φ2 · R^{ab} · R_{ab} ) ] +
√(-g) [ -984.2254811036 · Λ^{1} · ∇^{a}∇_{a}φ2 ] +
√(-g) [ -8.5564353371e+16 · φ2 · φ2 · φ2 · φ2 ] +
√(-g) [ 1.0845026769e+19 · Λ^{-1} · φ2 · φ2 · ∇^{a}∇_{a}φ2 ] +
√(-g) [ 497.5457896739 · Λ^{-2} · φ2 · φ2 · φ2 · ∇^{a}∇_{a}φ2 ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Term Metadata

```json
[
  {
    "coeff_symbol": "\\alpha",
    "coeff_token": "COEFF_0",
    "candidate": "R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\beta",
    "coeff_token": "COEFF_1",
    "candidate": "φ2 · φ2 · φ2 · R",
    "mass_dim": 5,
    "lambda_power": -3,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\gamma",
    "coeff_token": "COEFF_2",
    "candidate": "φ2 · R^{bcd}_{a} · R^{a}_{bcd}",
    "mass_dim": 5,
    "lambda_power": -3,
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
    "candidate": "∇^{a}∇_{a}φ2",
    "mass_dim": 3,
    "lambda_power": 1,
    "sector": "scalar"
  },
  {
    "coeff_symbol": "\\zeta",
    "coeff_token": "COEFF_5",
    "candidate": "φ2 · φ2 · φ2 · φ2",
    "mass_dim": 4,
    "lambda_power": 0,
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
    "candidate": "φ2 · φ2 · φ2 · ∇^{a}∇_{a}φ2",
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
  "effective_correction_status": "not_applicable_non_eh",
  "effective_correction_reason": "EH-relative correction diagnostic applies only to EH-anchored theories",
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000275_slot_01/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000275_slot_01/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000275_slot_01/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 80. task_000561_slot_08_lag_1  chi2=9434.00751

- best_validation_stage: `initial`
- validation_stage_counts: `{"initial": 1}`
- family_accepted_records: `1`
- delta_chi2_vs_LCDM: `7788.72750951`
- delta_AIC_vs_LCDM: `7802.72750951`
- delta_BIC_vs_LCDM: `7841.32831123`
- scalar_config: `both`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "quadratic", "phi2": "quadratic"}`
- agent_parameter_sample_index: `541`
- H0_km_s_Mpc: `63.59191733`
- Omega_m0: `0.27971055`
- lambda_H_Lambda_over_H0: `1414.15004494`
- effective_correction_status: `eh_dominated`
- max_relative_effect_to_EH: `1.73572510e-12`
- dominant_correction_term: `φ2 · φ2 · R`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-2} · φ2 · φ2 · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (5871.4992991681) Λ^{-2} · φ2 · φ2 · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-2} · φ2 · φ2 · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 5871.4992991681 · Λ^{-2} · φ2 · φ2 · R ) ] +
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
    "candidate": "φ2 · φ2 · R",
    "mass_dim": 4,
    "lambda_power": -2,
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
  "max_relative_effect_to_EH": 1.7357251011937962e-12,
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
      "coefficient": "5871.499299168138",
      "lambda_power": -2,
      "sector": "non-minimal",
      "relative_effect_to_EH": 1.7357251011937962e-12,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000561_slot_08/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000561_slot_08/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_600_sector_async_v9b_nodiv16_task_000561_slot_08/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`
