# Accepted Lagrangians Full

Complete dimension-balanced Lagrangians, best-fit coefficient substitutions, metadata, and Solver paths.
Only the best chi-square representative from each accepted theory family is shown for human inspection.
The full accepted-attempt list is preserved in `accepted_summary.json`.

## 1. wave_0026_lag_5  chi2=1637.965278

- scalar_config: `both`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "quadratic", "phi2": "axion"}`
- agent_parameter_sample_index: `955`
- H0_km_s_Mpc: `59.98435974`
- Omega_m0: `0.26957893`
- lambda_H_Lambda_over_H0: `3637.02175191`
- effective_correction_status: `moderate`
- max_relative_effect_to_EH: `5.00336855e-04`
- dominant_correction_term: `φ1 · R · R`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-3} · φ1 · R · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-6.1252876482e+06) Λ^{-3} · φ1 · R · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-3} · φ1 · R · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -6.1252876482e+06 · Λ^{-3} · φ1 · R · R ) ] +
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
  "max_relative_effect_to_EH": 0.0005003368551221841,
  "dominant_correction_term": "φ1 · R · R",
  "active_correction_terms": 0,
  "moderate_correction_terms": 1,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 0,
  "correction_term_count": 1,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "φ1 · R · R",
      "coeff_symbol": "\\beta",
      "coefficient": "-6125287.648216381",
      "lambda_power": -3,
      "sector": "non-minimal",
      "relative_effect_to_EH": 0.0005003368551221841,
      "effect_class": "moderate"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0026/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0026/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0026/agent_solver_result/agent_solve/top_01_lagrangian_5_solution.csv`

## 2. wave_0035_lag_8  chi2=1638.005659

- scalar_config: `both`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "quadratic", "phi2": "axion"}`
- agent_parameter_sample_index: `433`
- H0_km_s_Mpc: `66.1236658`
- Omega_m0: `0.27599042`
- lambda_H_Lambda_over_H0: `2168.68508081`
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0035/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0035/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0035/agent_solver_result/agent_solve/top_01_lagrangian_8_solution.csv`

## 3. wave_0033_lag_6  chi2=1638.016747

- scalar_config: `both`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "quadratic", "phi2": "quadratic"}`
- agent_parameter_sample_index: `335`
- H0_km_s_Mpc: `61.2533993`
- Omega_m0: `0.27520364`
- lambda_H_Lambda_over_H0: `8746.5947359`
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0033/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0033/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0033/agent_solver_result/agent_solve/top_01_lagrangian_6_solution.csv`

## 4. wave_0028_lag_9  chi2=1638.028326

- scalar_config: `both`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "quadratic", "phi2": "quadratic"}`
- agent_parameter_sample_index: `453`
- H0_km_s_Mpc: `65.31857005`
- Omega_m0: `0.27551857`
- lambda_H_Lambda_over_H0: `4479.02398934`
- effective_correction_status: `weak`
- max_relative_effect_to_EH: `2.11105701e-05`
- dominant_correction_term: `R · R · R`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · R · R · R  +  \gamma Λ^{-4} · φ1 · φ1 · R · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (4.2481859679e+09) Λ^{-4} · R · R · R  +  (7.3704063973e+08) Λ^{-4} · φ1 · φ1 · R · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · R · R · R ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · φ1 · φ1 · R · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 4.2481859679e+09 · Λ^{-4} · R · R · R ) ] +
√(-g) [ M_p² ( 7.3704063973e+08 · Λ^{-4} · φ1 · φ1 · R · R ) ] +
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
    "candidate": "φ1 · φ1 · R · R",
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
  "max_relative_effect_to_EH": 2.1110570098862808e-05,
  "dominant_correction_term": "R · R · R",
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
      "coefficient": "4248185967.89104",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 2.1110570098862808e-05,
      "effect_class": "weak"
    },
    {
      "candidate": "φ1 · φ1 · R · R",
      "coeff_symbol": "\\gamma",
      "coefficient": "737040639.7255176",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 1.546106371052126e-05,
      "effect_class": "weak"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0028/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0028/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0028/agent_solver_result/agent_solve/top_01_lagrangian_9_solution.csv`

## 5. wave_0025_lag_7  chi2=1638.061462

- scalar_config: `phi1_only`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: `954`
- H0_km_s_Mpc: `71.61832652`
- Omega_m0: `0.26870566`
- lambda_H_Lambda_over_H0: `2601.88860686`
- effective_correction_status: `weak`
- max_relative_effect_to_EH: `5.07106838e-05`
- dominant_correction_term: `φ1 · R · R`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · R^{b}_{a} · R^{cd} · R^{a}_{cbd}  +  \gamma Λ^{-3} · φ1 · R · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-1.1407621706e+08) Λ^{-4} · R^{b}_{a} · R^{cd} · R^{a}_{cbd}  +  (-2.3334560605e+05) Λ^{-3} · φ1 · R · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · R^{b}_{a} · R^{cd} · R^{a}_{cbd} ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-3} · φ1 · R · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -1.1407621706e+08 · Λ^{-4} · R^{b}_{a} · R^{cd} · R^{a}_{cbd} ) ] +
√(-g) [ M_p² ( -2.3334560605e+05 · Λ^{-3} · φ1 · R · R ) ] +
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
    "candidate": "R^{b}_{a} · R^{cd} · R^{a}_{cbd}",
    "mass_dim": 6,
    "lambda_power": -4,
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
  "max_relative_effect_to_EH": 5.07106838252883e-05,
  "dominant_correction_term": "φ1 · R · R",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 2,
  "tiny_correction_terms": 0,
  "correction_term_count": 2,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "R^{b}_{a} · R^{cd} · R^{a}_{cbd}",
      "coeff_symbol": "\\beta",
      "coefficient": "-114076217.06392239",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 4.978176712107163e-06,
      "effect_class": "weak"
    },
    {
      "candidate": "φ1 · R · R",
      "coeff_symbol": "\\gamma",
      "coefficient": "-233345.60605122114",
      "lambda_power": -3,
      "sector": "non-minimal",
      "relative_effect_to_EH": 5.07106838252883e-05,
      "effect_class": "weak"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0025/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0025/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0025/agent_solver_result/agent_solve/top_01_lagrangian_7_solution.csv`

## 6. wave_0002_lag_7  chi2=1638.234639

- scalar_config: `phi1_only`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: `491`
- H0_km_s_Mpc: `62.63197523`
- Omega_m0: `0.28162076`
- lambda_H_Lambda_over_H0: `787.17006789`
- effective_correction_status: `eh_dominated`
- max_relative_effect_to_EH: `4.23592543e-16`
- dominant_correction_term: `∇^{a}φ1 · ∇_{a}φ1 · R`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · ∇^{a}φ1 · ∇_{a}φ1 · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (1.7302359794e-05) Λ^{-4} · ∇^{a}φ1 · ∇_{a}φ1 · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · ∇^{a}φ1 · ∇_{a}φ1 · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 1.7302359794e-05 · Λ^{-4} · ∇^{a}φ1 · ∇_{a}φ1 · R ) ] +
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
]
```

### Effective Correction Diagnostics

```json
{
  "effective_correction_status": "eh_dominated",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 4.235925425682954e-16,
  "dominant_correction_term": "∇^{a}φ1 · ∇_{a}φ1 · R",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 1,
  "correction_term_count": 1,
  "tiny_correction_fraction": 1.0,
  "term_effects": [
    {
      "candidate": "∇^{a}φ1 · ∇_{a}φ1 · R",
      "coeff_symbol": "\\beta",
      "coefficient": "1.7302359793954542e-05",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 4.235925425682954e-16,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0002/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0002/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0002/agent_solver_result/agent_solve/top_01_lagrangian_7_solution.csv`

## 7. wave_0030_lag_13  chi2=1638.272256

- scalar_config: `both`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "quadratic", "phi2": "quadratic"}`
- agent_parameter_sample_index: `876`
- H0_km_s_Mpc: `66.18905314`
- Omega_m0: `0.26585633`
- lambda_H_Lambda_over_H0: `1.05016103e+04`
- effective_correction_status: `moderate`
- max_relative_effect_to_EH: `2.93889761e-04`
- dominant_correction_term: `φ2 · R^{bcd}_{a} · R^{a}_{bcd}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-3} · φ2 · R^{bcd}_{a} · R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-2.3863048254e+11) Λ^{-3} · φ2 · R^{bcd}_{a} · R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-3} · φ2 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -2.3863048254e+11 · Λ^{-3} · φ2 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
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
    "candidate": "φ2 · R^{bcd}_{a} · R^{a}_{bcd}",
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
  "max_relative_effect_to_EH": 0.00029388976122623876,
  "dominant_correction_term": "φ2 · R^{bcd}_{a} · R^{a}_{bcd}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 1,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 0,
  "correction_term_count": 1,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "φ2 · R^{bcd}_{a} · R^{a}_{bcd}",
      "coeff_symbol": "\\beta",
      "coefficient": "-238630482543.56152",
      "lambda_power": -3,
      "sector": "non-minimal",
      "relative_effect_to_EH": 0.00029388976122623876,
      "effect_class": "moderate"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0030/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0030/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0030/agent_solver_result/agent_solve/top_01_lagrangian_13_solution.csv`

## 8. wave_0022_lag_15  chi2=1638.272973

- scalar_config: `phi1_only`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: `504`
- H0_km_s_Mpc: `63.1146128`
- Omega_m0: `0.3055954`
- lambda_H_Lambda_over_H0: `9433.64231298`
- effective_correction_status: `weak`
- max_relative_effect_to_EH: `7.90392916e-06`
- dominant_correction_term: `φ1 · φ1 · R^{ab} · R_{ab}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · R · R · R  +  \gamma Λ^{-4} · R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh}  +  \delta Λ^{-4} · ∇^{c}R^{ab} · ∇_{c}R_{ab}  +  \epsilon Λ^{-4} · φ1 · φ1 · R^{ab} · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-7.2932432415e+09) Λ^{-4} · R · R · R  +  (-4.0755367971e+09) Λ^{-4} · R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh}  +  (-1.3114133473e+10) Λ^{-4} · ∇^{c}R^{ab} · ∇_{c}R_{ab}  +  (-9.8369932421e+09) Λ^{-4} · φ1 · φ1 · R^{ab} · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · R · R · R ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh} ) ] +
√(-g) [ M_p² ( \delta · Λ^{-4} · ∇^{c}R^{ab} · ∇_{c}R_{ab} ) ] +
√(-g) [ M_p² ( \epsilon · Λ^{-4} · φ1 · φ1 · R^{ab} · R_{ab} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -7.2932432415e+09 · Λ^{-4} · R · R · R ) ] +
√(-g) [ M_p² ( -4.0755367971e+09 · Λ^{-4} · R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh} ) ] +
√(-g) [ M_p² ( -1.3114133473e+10 · Λ^{-4} · ∇^{c}R^{ab} · ∇_{c}R_{ab} ) ] +
√(-g) [ M_p² ( -9.8369932421e+09 · Λ^{-4} · φ1 · φ1 · R^{ab} · R_{ab} ) ] +
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
    "candidate": "R · R · R",
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
    "candidate": "∇^{c}R^{ab} · ∇_{c}R_{ab}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\epsilon",
    "coeff_token": "COEFF_4",
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
]
```

### Effective Correction Diagnostics

```json
{
  "effective_correction_status": "weak",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 7.90392916480432e-06,
  "dominant_correction_term": "φ1 · φ1 · R^{ab} · R_{ab}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 4,
  "tiny_correction_terms": 0,
  "correction_term_count": 4,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "R · R · R",
      "coeff_symbol": "\\beta",
      "coefficient": "-7293243241.465362",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 1.8417601503795565e-06,
      "effect_class": "weak"
    },
    {
      "candidate": "R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh}",
      "coeff_symbol": "\\gamma",
      "coefficient": "-4075536797.0925984",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 1.0291938738056593e-06,
      "effect_class": "weak"
    },
    {
      "candidate": "∇^{c}R^{ab} · ∇_{c}R_{ab}",
      "coeff_symbol": "\\delta",
      "coefficient": "-13114133472.69107",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 3.311707512981321e-06,
      "effect_class": "weak"
    },
    {
      "candidate": "φ1 · φ1 · R^{ab} · R_{ab}",
      "coeff_symbol": "\\epsilon",
      "coefficient": "-9836993242.054716",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 7.90392916480432e-06,
      "effect_class": "weak"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0022/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0022/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0022/agent_solver_result/agent_solve/top_02_lagrangian_15_solution.csv`

## 9. wave_0022_lag_12  chi2=1638.565709

- scalar_config: `phi1_only`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: `446`
- H0_km_s_Mpc: `57.02419496`
- Omega_m0: `0.29422895`
- lambda_H_Lambda_over_H0: `9239.6154651`
- effective_correction_status: `moderate`
- max_relative_effect_to_EH: `2.82155437e-04`
- dominant_correction_term: `∇^{a}∇_{a}R`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-2} · R · R  +  \gamma Λ^{-2} · ∇^{a}∇_{a}R  +  \delta Λ^{-4} · ∇^{a}∇_{a}R · R^{c}_{c} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (9199.5194209158) Λ^{-2} · R · R  +  (1.2043874492e+04) Λ^{-2} · ∇^{a}∇_{a}R  +  (-1.0000000000e+12) Λ^{-4} · ∇^{a}∇_{a}R · R^{c}_{c} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-2} · R · R ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-2} · ∇^{a}∇_{a}R ) ] +
√(-g) [ M_p² ( \delta · Λ^{-4} · ∇^{a}∇_{a}R · R^{c}_{c} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 9199.5194209158 · Λ^{-2} · R · R ) ] +
√(-g) [ M_p² ( 1.2043874492e+04 · Λ^{-2} · ∇^{a}∇_{a}R ) ] +
√(-g) [ M_p² ( -1.0000000000e+12 · Λ^{-4} · ∇^{a}∇_{a}R · R^{c}_{c} ) ] +
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
    "candidate": "∇^{a}∇_{a}R",
    "mass_dim": 4,
    "lambda_power": -2,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\delta",
    "coeff_token": "COEFF_3",
    "candidate": "∇^{a}∇_{a}R · R^{c}_{c}",
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
  "effective_correction_status": "moderate",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 0.00028215543652256324,
  "dominant_correction_term": "∇^{a}∇_{a}R",
  "active_correction_terms": 0,
  "moderate_correction_terms": 3,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 0,
  "correction_term_count": 3,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "R · R",
      "coeff_symbol": "\\beta",
      "coefficient": "9199.519420915825",
      "lambda_power": -2,
      "sector": "gravity",
      "relative_effect_to_EH": 0.00021551988271408776,
      "effect_class": "moderate"
    },
    {
      "candidate": "∇^{a}∇_{a}R",
      "coeff_symbol": "\\gamma",
      "coefficient": "12043.874492312127",
      "lambda_power": -2,
      "sector": "gravity",
      "relative_effect_to_EH": 0.00028215543652256324,
      "effect_class": "moderate"
    },
    {
      "candidate": "∇^{a}∇_{a}R · R^{c}_{c}",
      "coeff_symbol": "\\delta",
      "coefficient": "-1000000000000.0",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 0.00027441914523908126,
      "effect_class": "moderate"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0022/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0022/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0022/agent_solver_result/agent_solve/top_03_lagrangian_12_solution.csv`

## 10. wave_0027_lag_22  chi2=1638.707271

- scalar_config: `both`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "axion", "phi2": "quadratic"}`
- agent_parameter_sample_index: `474`
- H0_km_s_Mpc: `58.63996795`
- Omega_m0: `0.30372009`
- lambda_H_Lambda_over_H0: `5514.8410745`
- effective_correction_status: `weak`
- max_relative_effect_to_EH: `2.30840257e-05`
- dominant_correction_term: `φ1 · R^{ab} · R_{ab}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd}  +  \gamma Λ^{-3} · φ1 · R^{ab} · R_{ab}  +  \delta Λ^{-4} · φ2 · φ2 · R · R  +  \epsilon Λ^{-4} · φ2 · φ2 · R^{ab} · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (137.1349723013) Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd}  +  (1.0513534499e+06) Λ^{-3} · φ1 · R^{ab} · R_{ab}  +  (-1.0000000000e+12) Λ^{-4} · φ2 · φ2 · R · R  +  (-1.0000000000e+12) Λ^{-4} · φ2 · φ2 · R^{ab} · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-3} · φ1 · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( \delta · Λ^{-4} · φ2 · φ2 · R · R ) ] +
√(-g) [ M_p² ( \epsilon · Λ^{-4} · φ2 · φ2 · R^{ab} · R_{ab} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 137.1349723013 · Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( 1.0513534499e+06 · Λ^{-3} · φ1 · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( -1.0000000000e+12 · Λ^{-4} · φ2 · φ2 · R · R ) ] +
√(-g) [ M_p² ( -1.0000000000e+12 · Λ^{-4} · φ2 · φ2 · R^{ab} · R_{ab} ) ] +
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
    "candidate": "R^{bcd}_{a} · R^{a}_{bcd}",
    "mass_dim": 4,
    "lambda_power": -2,
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
  "effective_correction_status": "weak",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 2.3084025725566318e-05,
  "dominant_correction_term": "φ1 · R^{ab} · R_{ab}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 2,
  "tiny_correction_terms": 2,
  "correction_term_count": 4,
  "tiny_correction_fraction": 0.5,
  "term_effects": [
    {
      "candidate": "R^{bcd}_{a} · R^{a}_{bcd}",
      "coeff_symbol": "\\beta",
      "coefficient": "137.13497230125222",
      "lambda_power": -2,
      "sector": "gravity",
      "relative_effect_to_EH": 9.018041212398607e-06,
      "effect_class": "weak"
    },
    {
      "candidate": "φ1 · R^{ab} · R_{ab}",
      "coeff_symbol": "\\gamma",
      "coefficient": "1051353.4498960008",
      "lambda_power": -3,
      "sector": "non-minimal",
      "relative_effect_to_EH": 2.3084025725566318e-05,
      "effect_class": "weak"
    },
    {
      "candidate": "φ2 · φ2 · R · R",
      "coeff_symbol": "\\delta",
      "coefficient": "-1000000000000.0",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 2.0407094786641193e-09,
      "effect_class": "tiny"
    },
    {
      "candidate": "φ2 · φ2 · R^{ab} · R_{ab}",
      "coeff_symbol": "\\epsilon",
      "coefficient": "-1000000000000.0",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 2.0407094786641193e-09,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0027/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0027/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0027/agent_solver_result/agent_solve/top_04_lagrangian_22_solution.csv`

## 11. wave_0029_lag_9  chi2=1638.712887

- scalar_config: `both`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "axion", "phi2": "quadratic"}`
- agent_parameter_sample_index: `429`
- H0_km_s_Mpc: `66.45002561`
- Omega_m0: `0.30168319`
- lambda_H_Lambda_over_H0: `8909.18483219`
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0029/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0029/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0029/agent_solver_result/agent_solve/top_03_lagrangian_9_solution.csv`

## 12. wave_0003_lag_11  chi2=1639.138203

- scalar_config: `phi1_only`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: `514`
- H0_km_s_Mpc: `66.73071322`
- Omega_m0: `0.29737646`
- lambda_H_Lambda_over_H0: `7.27369882e+04`
- effective_correction_status: `eh_dominated`
- max_relative_effect_to_EH: `7.14510704e-08`
- dominant_correction_term: `R^{ab} · R^{d}_{a} · R_{bd}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · R^{ab} · R^{d}_{a} · R_{bd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (1.0000000000e+12) Λ^{-4} · R^{ab} · R^{d}_{a} · R_{bd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · R^{ab} · R^{d}_{a} · R_{bd} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 1.0000000000e+12 · Λ^{-4} · R^{ab} · R^{d}_{a} · R_{bd} ) ] +
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
  "max_relative_effect_to_EH": 7.145107039700721e-08,
  "dominant_correction_term": "R^{ab} · R^{d}_{a} · R_{bd}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 1,
  "correction_term_count": 1,
  "tiny_correction_fraction": 1.0,
  "term_effects": [
    {
      "candidate": "R^{ab} · R^{d}_{a} · R_{bd}",
      "coeff_symbol": "\\beta",
      "coefficient": "1000000000000.0",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 7.145107039700721e-08,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0003/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0003/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0003/agent_solver_result/agent_solve/top_01_lagrangian_11_solution.csv`

## 13. wave_0032_lag_12  chi2=1639.175776

- scalar_config: `both`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "axion", "phi2": "axion"}`
- agent_parameter_sample_index: `561`
- H0_km_s_Mpc: `58.25190787`
- Omega_m0: `0.29880957`
- lambda_H_Lambda_over_H0: `4738.3834517`
- effective_correction_status: `eh_dominated`
- max_relative_effect_to_EH: `3.61400324e-11`
- dominant_correction_term: `φ1 · R · R`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-3} · φ1 · R · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (0.9661937215) Λ^{-3} · φ1 · R · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-3} · φ1 · R · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 0.9661937215 · Λ^{-3} · φ1 · R · R ) ] +
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
  "max_relative_effect_to_EH": 3.614003236743961e-11,
  "dominant_correction_term": "φ1 · R · R",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 1,
  "correction_term_count": 1,
  "tiny_correction_fraction": 1.0,
  "term_effects": [
    {
      "candidate": "φ1 · R · R",
      "coeff_symbol": "\\beta",
      "coefficient": "0.9661937215330317",
      "lambda_power": -3,
      "sector": "non-minimal",
      "relative_effect_to_EH": 3.614003236743961e-11,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0032/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0032/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0032/agent_solver_result/agent_solve/top_02_lagrangian_12_solution.csv`

## 14. wave_0003_lag_5  chi2=1639.577769

- scalar_config: `phi1_only`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: `408`
- H0_km_s_Mpc: `67.48567049`
- Omega_m0: `0.29391482`
- lambda_H_Lambda_over_H0: `2410.02817407`
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0003/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0003/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0003/agent_solver_result/agent_solve/top_02_lagrangian_5_solution.csv`

## 15. wave_0015_lag_14  chi2=1639.788171

- scalar_config: `phi1_only`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: `282`
- H0_km_s_Mpc: `68.1169227`
- Omega_m0: `0.31064135`
- lambda_H_Lambda_over_H0: `2.54763821e+04`
- effective_correction_status: `weak`
- max_relative_effect_to_EH: `2.61374078e-05`
- dominant_correction_term: `φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh}  +  \gamma Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-6.3398286682e+11) Λ^{-4} · R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh}  +  (9.3844025363e+11) Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh} ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -6.3398286682e+11 · Λ^{-4} · R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh} ) ] +
√(-g) [ M_p² ( 9.3844025363e+11 · Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
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
    "candidate": "R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh}",
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
  "max_relative_effect_to_EH": 2.613740779515317e-05,
  "dominant_correction_term": "φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 2,
  "tiny_correction_terms": 0,
  "correction_term_count": 2,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh}",
      "coeff_symbol": "\\beta",
      "coefficient": "-633982866820.7372",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 3.009930733970195e-06,
      "effect_class": "weak"
    },
    {
      "candidate": "φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd}",
      "coeff_symbol": "\\gamma",
      "coefficient": "938440253634.841",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 2.613740779515317e-05,
      "effect_class": "weak"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0015/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0015/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0015/agent_solver_result/agent_solve/top_01_lagrangian_14_solution.csv`

## 16. wave_0031_lag_3  chi2=1640.213883

- scalar_config: `both`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "axion", "phi2": "axion"}`
- agent_parameter_sample_index: `894`
- H0_km_s_Mpc: `60.33380196`
- Omega_m0: `0.28161478`
- lambda_H_Lambda_over_H0: `4660.83112229`
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0031/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0031/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0031/agent_solver_result/agent_solve/top_02_lagrangian_3_solution.csv`

## 17. wave_0022_lag_8  chi2=1642.208375

- scalar_config: `phi1_only`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "axion", "phi2": null}`
- agent_parameter_sample_index: `793`
- H0_km_s_Mpc: `62.03496341`
- Omega_m0: `0.22663647`
- lambda_H_Lambda_over_H0: `1150.88567169`
- effective_correction_status: `weak`
- max_relative_effect_to_EH: `9.01716829e-06`
- dominant_correction_term: `φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def}  +  \gamma Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (1.6849827828e+06) Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def}  +  (-2.4124404263e+06) Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def} ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 1.6849827828e+06 · Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def} ) ] +
√(-g) [ M_p² ( -2.4124404263e+06 · Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
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
  "max_relative_effect_to_EH": 9.017168285472189e-06,
  "dominant_correction_term": "φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 2,
  "tiny_correction_terms": 0,
  "correction_term_count": 2,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "R_{ab} · R^{adef} · R^{b}_{def}",
      "coeff_symbol": "\\beta",
      "coefficient": "1684982.782788899",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 1.9208645004330342e-06,
      "effect_class": "weak"
    },
    {
      "candidate": "φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd}",
      "coeff_symbol": "\\gamma",
      "coefficient": "-2412440.426284302",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 9.017168285472189e-06,
      "effect_class": "weak"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0022/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0022/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0022/agent_solver_result/agent_solve/top_05_lagrangian_8_solution.csv`

## 18. wave_0011_lag_6  chi2=1642.39756

- scalar_config: `phi1_only`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "axion", "phi2": null}`
- agent_parameter_sample_index: `812`
- H0_km_s_Mpc: `64.37076587`
- Omega_m0: `0.27272258`
- lambda_H_Lambda_over_H0: `3987.70357975`
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0011/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0011/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0011/agent_solver_result/agent_solve/top_02_lagrangian_6_solution.csv`

## 19. wave_0010_lag_19  chi2=1642.56837

- scalar_config: `phi1_only`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: `288`
- H0_km_s_Mpc: `62.63479072`
- Omega_m0: `0.30907133`
- lambda_H_Lambda_over_H0: `6072.7578563`
- effective_correction_status: `moderate`
- max_relative_effect_to_EH: `1.89369403e-04`
- dominant_correction_term: `R^{b}_{a} · R^{cd} · R^{a}_{cbd}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · R^{b}_{a} · R^{cd} · R^{a}_{cbd}  +  \gamma Λ^{-4} · ∇^{a}R · ∇_{a}R )  +  \delta Λ^{2} · φ1 · φ1  +  \epsilon · ∇^{a}φ1 · ∇_{a}φ1  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (1.2877266138e+11) Λ^{-4} · R^{b}_{a} · R^{cd} · R^{a}_{cbd}  +  (-8.0537709149e+10) Λ^{-4} · ∇^{a}R · ∇_{a}R )  +  (-5.1725954297e-09) Λ^{2} · φ1 · φ1  +  (-5.1297179749e-08) · ∇^{a}φ1 · ∇_{a}φ1  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · R^{b}_{a} · R^{cd} · R^{a}_{cbd} ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · ∇^{a}R · ∇_{a}R ) ] +
√(-g) [ \delta · Λ^{2} · φ1 · φ1 ] +
√(-g) [ \epsilon · ∇^{a}φ1 · ∇_{a}φ1 ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 1.2877266138e+11 · Λ^{-4} · R^{b}_{a} · R^{cd} · R^{a}_{cbd} ) ] +
√(-g) [ M_p² ( -8.0537709149e+10 · Λ^{-4} · ∇^{a}R · ∇_{a}R ) ] +
√(-g) [ -5.1725954297e-09 · Λ^{2} · φ1 · φ1 ] +
√(-g) [ -5.1297179749e-08 · ∇^{a}φ1 · ∇_{a}φ1 ] +
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
    "candidate": "R^{b}_{a} · R^{cd} · R^{a}_{cbd}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\gamma",
    "coeff_token": "COEFF_2",
    "candidate": "∇^{a}R · ∇_{a}R",
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
  "effective_correction_status": "moderate",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 0.0001893694025890947,
  "dominant_correction_term": "R^{b}_{a} · R^{cd} · R^{a}_{cbd}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 2,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 0,
  "correction_term_count": 2,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "R^{b}_{a} · R^{cd} · R^{a}_{cbd}",
      "coeff_symbol": "\\beta",
      "coefficient": "128772661382.78615",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 0.0001893694025890947,
      "effect_class": "moderate"
    },
    {
      "candidate": "∇^{a}R · ∇_{a}R",
      "coeff_symbol": "\\gamma",
      "coefficient": "-80537709148.6865",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 0.00011843645773573936,
      "effect_class": "moderate"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0010/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0010/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0010/agent_solver_result/agent_solve/top_01_lagrangian_19_solution.csv`

## 20. wave_0034_lag_24  chi2=1677.836496

- scalar_config: `both`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "axion", "phi2": "quadratic"}`
- agent_parameter_sample_index: `314`
- H0_km_s_Mpc: `73.07284891`
- Omega_m0: `0.29004504`
- lambda_H_Lambda_over_H0: `1.07096321e+04`
- effective_correction_status: `weak`
- max_relative_effect_to_EH: `1.26679183e-06`
- dominant_correction_term: `φ1 · φ1 · R · R`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · φ1 · φ1 · R · R  +  \gamma Λ^{-4} · φ1 · φ2 · R^{ab} · R_{ab} )  +  \delta · ∇^{a}φ1 · ∇_{a}φ1  +  \epsilon · ∇^{a}φ1 · ∇_{a}φ2  +  \zeta Λ^{-1} · φ1 · ∇^{a}∇_{a}φ1 · φ2  +  \eta Λ^{-2} · φ2 · φ2 · φ2 · ∇^{a}∇_{a}φ2  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-1.9690629002e+09) Λ^{-4} · φ1 · φ1 · R · R  +  (-1.0000000000e+12) Λ^{-4} · φ1 · φ2 · R^{ab} · R_{ab} )  +  (2056.1386058544) · ∇^{a}φ1 · ∇_{a}φ1  +  (-6.9838110735e+05) · ∇^{a}φ1 · ∇_{a}φ2  +  (5.1093560834e+07) Λ^{-1} · φ1 · ∇^{a}∇_{a}φ1 · φ2  +  (1.9269624116) Λ^{-2} · φ2 · φ2 · φ2 · ∇^{a}∇_{a}φ2  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · φ1 · φ1 · R · R ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · φ1 · φ2 · R^{ab} · R_{ab} ) ] +
√(-g) [ \delta · ∇^{a}φ1 · ∇_{a}φ1 ] +
√(-g) [ \epsilon · ∇^{a}φ1 · ∇_{a}φ2 ] +
√(-g) [ \zeta · Λ^{-1} · φ1 · ∇^{a}∇_{a}φ1 · φ2 ] +
√(-g) [ \eta · Λ^{-2} · φ2 · φ2 · φ2 · ∇^{a}∇_{a}φ2 ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -1.9690629002e+09 · Λ^{-4} · φ1 · φ1 · R · R ) ] +
√(-g) [ M_p² ( -1.0000000000e+12 · Λ^{-4} · φ1 · φ2 · R^{ab} · R_{ab} ) ] +
√(-g) [ 2056.1386058544 · ∇^{a}φ1 · ∇_{a}φ1 ] +
√(-g) [ -6.9838110735e+05 · ∇^{a}φ1 · ∇_{a}φ2 ] +
√(-g) [ 5.1093560834e+07 · Λ^{-1} · φ1 · ∇^{a}∇_{a}φ1 · φ2 ] +
√(-g) [ 1.9269624116 · Λ^{-2} · φ2 · φ2 · φ2 · ∇^{a}∇_{a}φ2 ] +
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
    "candidate": "φ1 · φ1 · R · R",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\gamma",
    "coeff_token": "COEFF_2",
    "candidate": "φ1 · φ2 · R^{ab} · R_{ab}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\delta",
    "coeff_token": "COEFF_3",
    "candidate": "∇^{a}φ1 · ∇_{a}φ1",
    "mass_dim": 4,
    "lambda_power": 0,
    "sector": "scalar"
  },
  {
    "coeff_symbol": "\\epsilon",
    "coeff_token": "COEFF_4",
    "candidate": "∇^{a}φ1 · ∇_{a}φ2",
    "mass_dim": 4,
    "lambda_power": 0,
    "sector": "scalar"
  },
  {
    "coeff_symbol": "\\zeta",
    "coeff_token": "COEFF_5",
    "candidate": "φ1 · ∇^{a}∇_{a}φ1 · φ2",
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
  "effective_correction_status": "weak",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 1.266791832241216e-06,
  "dominant_correction_term": "φ1 · φ1 · R · R",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 1,
  "tiny_correction_terms": 1,
  "correction_term_count": 2,
  "tiny_correction_fraction": 0.5,
  "term_effects": [
    {
      "candidate": "φ1 · φ1 · R · R",
      "coeff_symbol": "\\beta",
      "coefficient": "-1969062900.2117627",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 1.266791832241216e-06,
      "effect_class": "weak"
    },
    {
      "candidate": "φ1 · φ2 · R^{ab} · R_{ab}",
      "coeff_symbol": "\\gamma",
      "coefficient": "-1000000000000.0",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 1.287415072003794e-07,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0034/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0034/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0034/agent_solver_result/agent_solve/top_03_lagrangian_24_solution.csv`

## 21. wave_0016_lag_9  chi2=1681.488332

- scalar_config: `phi1_only`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "axion", "phi2": null}`
- agent_parameter_sample_index: `895`
- H0_km_s_Mpc: `62.74094544`
- Omega_m0: `0.20893629`
- lambda_H_Lambda_over_H0: `659.93044364`
- effective_correction_status: `moderate`
- max_relative_effect_to_EH: `7.67708069e-04`
- dominant_correction_term: `φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (7.8109528032e+06) Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
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
√(-g) [ M_p² ( 7.8109528032e+06 · Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
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
  "effective_correction_status": "moderate",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 0.000767708068704651,
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
      "coefficient": "7810952.803154067",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 0.000767708068704651,
      "effect_class": "moderate"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0016/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0016/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0016/agent_solver_result/agent_solve/top_04_lagrangian_9_solution.csv`

## 22. wave_0004_lag_8  chi2=1681.557549

- scalar_config: `phi1_only`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "axion", "phi2": null}`
- agent_parameter_sample_index: `713`
- H0_km_s_Mpc: `71.10428115`
- Omega_m0: `0.28759146`
- lambda_H_Lambda_over_H0: `1.02756080e+04`
- effective_correction_status: `eh_dominated`
- max_relative_effect_to_EH: `9.29525622e-07`
- dominant_correction_term: `φ1 · ∇^{a}φ1 · ∇_{a}R`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · φ1 · ∇^{a}φ1 · ∇_{a}R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-5.8528977467e+09) Λ^{-4} · φ1 · ∇^{a}φ1 · ∇_{a}R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · φ1 · ∇^{a}φ1 · ∇_{a}R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -5.8528977467e+09 · Λ^{-4} · φ1 · ∇^{a}φ1 · ∇_{a}R ) ] +
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
    "candidate": "φ1 · ∇^{a}φ1 · ∇_{a}R",
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
  "effective_correction_status": "eh_dominated",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 9.295256215450964e-07,
  "dominant_correction_term": "φ1 · ∇^{a}φ1 · ∇_{a}R",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 1,
  "correction_term_count": 1,
  "tiny_correction_fraction": 1.0,
  "term_effects": [
    {
      "candidate": "φ1 · ∇^{a}φ1 · ∇_{a}R",
      "coeff_symbol": "\\beta",
      "coefficient": "-5852897746.680259",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 9.295256215450964e-07,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0004/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0004/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0004/agent_solver_result/agent_solve/top_05_lagrangian_8_solution.csv`

## 23. wave_0009_lag_20  chi2=1835.787666

- scalar_config: `phi1_only`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "axion", "phi2": null}`
- agent_parameter_sample_index: `823`
- H0_km_s_Mpc: `66.01094556`
- Omega_m0: `0.38039545`
- lambda_H_Lambda_over_H0: `788.18575041`
- effective_correction_status: `weak`
- max_relative_effect_to_EH: `8.94565910e-05`
- dominant_correction_term: `R^{ab} · R^{d}_{a} · R_{bd}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · R · R^{bcd}_{a} · R^{a}_{bcd}  +  \gamma Λ^{-4} · R^{ab} · R^{d}_{a} · R_{bd}  +  \delta Λ^{-4} · φ1 · φ1 · R^{ab} · R_{ab} )  +  \epsilon Λ^{2} · φ1 · φ1  +  \zeta · ∇^{a}φ1 · ∇_{a}φ1  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (2.7224423587e+06) Λ^{-4} · R · R^{bcd}_{a} · R^{a}_{bcd}  +  (1.7262220677e+07) Λ^{-4} · R^{ab} · R^{d}_{a} · R_{bd}  +  (-1.9245704926e+05) Λ^{-4} · φ1 · φ1 · R^{ab} · R_{ab} )  +  (4.5183786765e-10) Λ^{2} · φ1 · φ1  +  (3.9518336198e-09) · ∇^{a}φ1 · ∇_{a}φ1  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · R · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · R^{ab} · R^{d}_{a} · R_{bd} ) ] +
√(-g) [ M_p² ( \delta · Λ^{-4} · φ1 · φ1 · R^{ab} · R_{ab} ) ] +
√(-g) [ \epsilon · Λ^{2} · φ1 · φ1 ] +
√(-g) [ \zeta · ∇^{a}φ1 · ∇_{a}φ1 ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 2.7224423587e+06 · Λ^{-4} · R · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( 1.7262220677e+07 · Λ^{-4} · R^{ab} · R^{d}_{a} · R_{bd} ) ] +
√(-g) [ M_p² ( -1.9245704926e+05 · Λ^{-4} · φ1 · φ1 · R^{ab} · R_{ab} ) ] +
√(-g) [ 4.5183786765e-10 · Λ^{2} · φ1 · φ1 ] +
√(-g) [ 3.9518336198e-09 · ∇^{a}φ1 · ∇_{a}φ1 ] +
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
    "candidate": "R · R^{bcd}_{a} · R^{a}_{bcd}",
    "mass_dim": 6,
    "lambda_power": -4,
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
    "candidate": "φ1 · φ1 · R^{ab} · R_{ab}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\epsilon",
    "coeff_token": "COEFF_4",
    "candidate": "φ1 · φ1",
    "mass_dim": 2,
    "lambda_power": 2,
    "sector": "scalar"
  },
  {
    "coeff_symbol": "\\zeta",
    "coeff_token": "COEFF_5",
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
  "max_relative_effect_to_EH": 8.945659095627868e-05,
  "dominant_correction_term": "R^{ab} · R^{d}_{a} · R_{bd}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 3,
  "tiny_correction_terms": 0,
  "correction_term_count": 3,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "R · R^{bcd}_{a} · R^{a}_{bcd}",
      "coeff_symbol": "\\beta",
      "coefficient": "2722442.358749045",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 1.4108289833776558e-05,
      "effect_class": "weak"
    },
    {
      "candidate": "R^{ab} · R^{d}_{a} · R_{bd}",
      "coeff_symbol": "\\gamma",
      "coefficient": "17262220.67720791",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 8.945659095627868e-05,
      "effect_class": "weak"
    },
    {
      "candidate": "φ1 · φ1 · R^{ab} · R_{ab}",
      "coeff_symbol": "\\delta",
      "coefficient": "-192457.04926276926",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 1.1625021445364398e-06,
      "effect_class": "weak"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0009/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0009/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0009/agent_solver_result/agent_solve/top_06_lagrangian_20_solution.csv`

## 24. wave_0028_lag_13  chi2=1942.431207

- scalar_config: `phi2_only`
- proposal_group: `eh_phi2_only`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": null, "phi2": "quadratic"}`
- agent_parameter_sample_index: `769`
- H0_km_s_Mpc: `65.17068673`
- Omega_m0: `0.25729363`
- lambda_H_Lambda_over_H0: `4599.59692787`
- effective_correction_status: `weak`
- max_relative_effect_to_EH: `3.35052308e-05`
- dominant_correction_term: `φ2 · R^{bcd}_{a} · R^{a}_{bcd}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-1} · φ2 · R  +  \gamma Λ^{-3} · φ2 · R^{ab} · R_{ab}  +  \delta Λ^{-3} · φ2 · R^{bcd}_{a} · R^{a}_{bcd}  +  \epsilon Λ^{-4} · φ2 · φ2 · R^{bcd}_{a} · R^{a}_{bcd}  +  \zeta Λ^{-4} · ∇^{a}φ2 · ∇^{b}φ2 · R_{ab} )  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-20.5493649073) Λ^{-1} · φ2 · R  +  (-3.9785637717e+09) Λ^{-3} · φ2 · R^{ab} · R_{ab}  +  (-4.6995406653e+09) Λ^{-3} · φ2 · R^{bcd}_{a} · R^{a}_{bcd}  +  (1.0000000000e+12) Λ^{-4} · φ2 · φ2 · R^{bcd}_{a} · R^{a}_{bcd}  +  (-1.0000000000e+12) Λ^{-4} · ∇^{a}φ2 · ∇^{b}φ2 · R_{ab} )  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-1} · φ2 · R ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-3} · φ2 · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( \delta · Λ^{-3} · φ2 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( \epsilon · Λ^{-4} · φ2 · φ2 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( \zeta · Λ^{-4} · ∇^{a}φ2 · ∇^{b}φ2 · R_{ab} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -20.5493649073 · Λ^{-1} · φ2 · R ) ] +
√(-g) [ M_p² ( -3.9785637717e+09 · Λ^{-3} · φ2 · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( -4.6995406653e+09 · Λ^{-3} · φ2 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( 1.0000000000e+12 · Λ^{-4} · φ2 · φ2 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( -1.0000000000e+12 · Λ^{-4} · ∇^{a}φ2 · ∇^{b}φ2 · R_{ab} ) ] +
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
    "candidate": "φ2 · φ2 · R^{bcd}_{a} · R^{a}_{bcd}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\zeta",
    "coeff_token": "COEFF_5",
    "candidate": "∇^{a}φ2 · ∇^{b}φ2 · R_{ab}",
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
  "effective_correction_status": "weak",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 3.350523075451009e-05,
  "dominant_correction_term": "φ2 · R^{bcd}_{a} · R^{a}_{bcd}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 3,
  "tiny_correction_terms": 2,
  "correction_term_count": 5,
  "tiny_correction_fraction": 0.4,
  "term_effects": [
    {
      "candidate": "φ2 · R",
      "coeff_symbol": "\\beta",
      "coefficient": "-20.5493649072858",
      "lambda_power": -1,
      "sector": "non-minimal",
      "relative_effect_to_EH": 3.09952508915963e-06,
      "effect_class": "weak"
    },
    {
      "candidate": "φ2 · R^{ab} · R_{ab}",
      "coeff_symbol": "\\gamma",
      "coefficient": "-3978563771.712457",
      "lambda_power": -3,
      "sector": "non-minimal",
      "relative_effect_to_EH": 2.8365048147800336e-05,
      "effect_class": "weak"
    },
    {
      "candidate": "φ2 · R^{bcd}_{a} · R^{a}_{bcd}",
      "coeff_symbol": "\\delta",
      "coefficient": "-4699540665.264032",
      "lambda_power": -3,
      "sector": "non-minimal",
      "relative_effect_to_EH": 3.350523075451009e-05,
      "effect_class": "weak"
    },
    {
      "candidate": "φ2 · φ2 · R^{bcd}_{a} · R^{a}_{bcd}",
      "coeff_symbol": "\\epsilon",
      "coefficient": "1000000000000.0",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 5.376800931172343e-10,
      "effect_class": "tiny"
    },
    {
      "candidate": "∇^{a}φ2 · ∇^{b}φ2 · R_{ab}",
      "coeff_symbol": "\\zeta",
      "coefficient": "-1000000000000.0",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 5.376800931172343e-10,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0028/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0028/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0028/agent_solver_result/agent_solve/top_02_lagrangian_13_solution.csv`

## 25. wave_0037_lag_21  chi2=1946.87085

- scalar_config: `phi2_only`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": null, "phi2": "quadratic"}`
- agent_parameter_sample_index: `61`
- H0_km_s_Mpc: `62.81191588`
- Omega_m0: `0.27373218`
- lambda_H_Lambda_over_H0: `5593.97952004`
- effective_correction_status: `active`
- max_relative_effect_to_EH: `0.01402443`
- dominant_correction_term: `R^{bcd}_{a} · R^{a}_{bcd}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-2} · R^{ab} · R_{ab}  +  \gamma Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd}  +  \delta Λ^{-4} · R^{b}_{a} · R^{cd} · R^{a}_{cbd}  +  \epsilon Λ^{-4} · ∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}  +  \zeta Λ^{-3} · φ2 · R^{ab} · R_{ab}  +  \eta Λ^{-3} · φ2 · R^{bcd}_{a} · R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (3.0736512397e+04) Λ^{-2} · R^{ab} · R_{ab}  +  (2.1943050629e+05) Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd}  +  (2.5851380473e+05) Λ^{-4} · R^{b}_{a} · R^{cd} · R^{a}_{cbd}  +  (3.1669376063e+08) Λ^{-4} · ∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}  +  (663.6990564528) Λ^{-3} · φ2 · R^{ab} · R_{ab}  +  (1.0179124450e+07) Λ^{-3} · φ2 · R^{bcd}_{a} · R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-2} · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( \delta · Λ^{-4} · R^{b}_{a} · R^{cd} · R^{a}_{cbd} ) ] +
√(-g) [ M_p² ( \epsilon · Λ^{-4} · ∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( \zeta · Λ^{-3} · φ2 · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( \eta · Λ^{-3} · φ2 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 3.0736512397e+04 · Λ^{-2} · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( 2.1943050629e+05 · Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( 2.5851380473e+05 · Λ^{-4} · R^{b}_{a} · R^{cd} · R^{a}_{cbd} ) ] +
√(-g) [ M_p² ( 3.1669376063e+08 · Λ^{-4} · ∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( 663.6990564528 · Λ^{-3} · φ2 · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( 1.0179124450e+07 · Λ^{-3} · φ2 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
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
    "candidate": "R^{bcd}_{a} · R^{a}_{bcd}",
    "mass_dim": 4,
    "lambda_power": -2,
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
    "coeff_symbol": "\\epsilon",
    "coeff_token": "COEFF_4",
    "candidate": "∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\zeta",
    "coeff_token": "COEFF_5",
    "candidate": "φ2 · R^{ab} · R_{ab}",
    "mass_dim": 5,
    "lambda_power": -3,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\eta",
    "coeff_token": "COEFF_6",
    "candidate": "φ2 · R^{bcd}_{a} · R^{a}_{bcd}",
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
  "max_relative_effect_to_EH": 0.01402443121428704,
  "dominant_correction_term": "R^{bcd}_{a} · R^{a}_{bcd}",
  "active_correction_terms": 1,
  "moderate_correction_terms": 1,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 4,
  "correction_term_count": 6,
  "tiny_correction_fraction": 0.6666666666666666,
  "term_effects": [
    {
      "candidate": "R^{ab} · R_{ab}",
      "coeff_symbol": "\\beta",
      "coefficient": "30736.51239670984",
      "lambda_power": -2,
      "sector": "gravity",
      "relative_effect_to_EH": 0.001964458411775169,
      "effect_class": "moderate"
    },
    {
      "candidate": "R^{bcd}_{a} · R^{a}_{bcd}",
      "coeff_symbol": "\\gamma",
      "coefficient": "219430.50628657074",
      "lambda_power": -2,
      "sector": "gravity",
      "relative_effect_to_EH": 0.01402443121428704,
      "effect_class": "active"
    },
    {
      "candidate": "R^{b}_{a} · R^{cd} · R^{a}_{cbd}",
      "coeff_symbol": "\\delta",
      "coefficient": "258513.80473388886",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 5.279955314090324e-10,
      "effect_class": "tiny"
    },
    {
      "candidate": "∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}",
      "coeff_symbol": "\\epsilon",
      "coefficient": "316693760.62659305",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 6.468238344489568e-07,
      "effect_class": "tiny"
    },
    {
      "candidate": "φ2 · R^{ab} · R_{ab}",
      "coeff_symbol": "\\zeta",
      "coefficient": "663.6990564527729",
      "lambda_power": -3,
      "sector": "non-minimal",
      "relative_effect_to_EH": 1.78273296471491e-12,
      "effect_class": "tiny"
    },
    {
      "candidate": "φ2 · R^{bcd}_{a} · R^{a}_{bcd}",
      "coeff_symbol": "\\eta",
      "coefficient": "10179124.449575776",
      "lambda_power": -3,
      "sector": "non-minimal",
      "relative_effect_to_EH": 2.734170032602046e-08,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0037/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0037/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0037/agent_solver_result/agent_solve/top_04_lagrangian_21_solution.csv`

## 26. wave_0024_lag_24  chi2=1946.870851

- scalar_config: `phi2_only`
- proposal_group: `eh_phi2_only`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": null, "phi2": "axion"}`
- agent_parameter_sample_index: `891`
- H0_km_s_Mpc: `64.40439901`
- Omega_m0: `0.29299992`
- lambda_H_Lambda_over_H0: `2980.37463924`
- effective_correction_status: `weak`
- max_relative_effect_to_EH: `4.21325155e-06`
- dominant_correction_term: `R · R^{bcd}_{a} · R^{a}_{bcd}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · R · R^{bcd}_{a} · R^{a}_{bcd}  +  \gamma Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf}  +  \delta Λ^{-3} · φ2 · R^{ab} · R_{ab}  +  \epsilon Λ^{-3} · φ2 · R^{bcd}_{a} · R^{a}_{bcd} )  +  \zeta Λ^{2} · φ2 · φ2  +  \eta · φ2 · φ2 · φ2 · φ2  +  \theta · ∇^{a}φ2 · ∇_{a}φ2  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-1.6621523601e+08) Λ^{-4} · R · R^{bcd}_{a} · R^{a}_{bcd}  +  (-1.0622659768) Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf}  +  (468.088594312) Λ^{-3} · φ2 · R^{ab} · R_{ab}  +  (2.6479368389e+05) Λ^{-3} · φ2 · R^{bcd}_{a} · R^{a}_{bcd} )  +  (507.346408991) Λ^{2} · φ2 · φ2  +  (6.1499579462e+07) · φ2 · φ2 · φ2 · φ2  +  (-223.8487118389) · ∇^{a}φ2 · ∇_{a}φ2  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · R · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf} ) ] +
√(-g) [ M_p² ( \delta · Λ^{-3} · φ2 · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( \epsilon · Λ^{-3} · φ2 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ \zeta · Λ^{2} · φ2 · φ2 ] +
√(-g) [ \eta · φ2 · φ2 · φ2 · φ2 ] +
√(-g) [ \theta · ∇^{a}φ2 · ∇_{a}φ2 ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -1.6621523601e+08 · Λ^{-4} · R · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( -1.0622659768 · Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf} ) ] +
√(-g) [ M_p² ( 468.088594312 · Λ^{-3} · φ2 · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( 2.6479368389e+05 · Λ^{-3} · φ2 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ 507.346408991 · Λ^{2} · φ2 · φ2 ] +
√(-g) [ 6.1499579462e+07 · φ2 · φ2 · φ2 · φ2 ] +
√(-g) [ -223.8487118389 · ∇^{a}φ2 · ∇_{a}φ2 ] +
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
    "candidate": "R · R^{bcd}_{a} · R^{a}_{bcd}",
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
    "candidate": "φ2 · R^{ab} · R_{ab}",
    "mass_dim": 5,
    "lambda_power": -3,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\epsilon",
    "coeff_token": "COEFF_4",
    "candidate": "φ2 · R^{bcd}_{a} · R^{a}_{bcd}",
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
    "candidate": "φ2 · φ2 · φ2 · φ2",
    "mass_dim": 4,
    "lambda_power": 0,
    "sector": "scalar"
  },
  {
    "coeff_symbol": "\\theta",
    "coeff_token": "COEFF_7",
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
  "max_relative_effect_to_EH": 4.213251551508782e-06,
  "dominant_correction_term": "R · R^{bcd}_{a} · R^{a}_{bcd}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 1,
  "tiny_correction_terms": 3,
  "correction_term_count": 4,
  "tiny_correction_fraction": 0.75,
  "term_effects": [
    {
      "candidate": "R · R^{bcd}_{a} · R^{a}_{bcd}",
      "coeff_symbol": "\\beta",
      "coefficient": "-166215236.01237375",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 4.213251551508782e-06,
      "effect_class": "weak"
    },
    {
      "candidate": "R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf}",
      "coeff_symbol": "\\gamma",
      "coefficient": "-1.0622659768117118",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 2.692649532190752e-14,
      "effect_class": "tiny"
    },
    {
      "candidate": "φ2 · R^{ab} · R_{ab}",
      "coeff_symbol": "\\delta",
      "coefficient": "468.0885943120206",
      "lambda_power": -3,
      "sector": "non-minimal",
      "relative_effect_to_EH": 2.790530283948811e-11,
      "effect_class": "tiny"
    },
    {
      "candidate": "φ2 · R^{bcd}_{a} · R^{a}_{bcd}",
      "coeff_symbol": "\\epsilon",
      "coefficient": "264793.68388694804",
      "lambda_power": -3,
      "sector": "non-minimal",
      "relative_effect_to_EH": 1.5785789332699436e-08,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0024/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0024/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0024/agent_solver_result/agent_solve/top_04_lagrangian_24_solution.csv`

## 27. wave_0003_lag_20  chi2=1946.870851

- scalar_config: `phi2_only`
- proposal_group: `eh_phi2_only`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": null, "phi2": "quadratic"}`
- agent_parameter_sample_index: `653`
- H0_km_s_Mpc: `66.03849963`
- Omega_m0: `0.41096787`
- lambda_H_Lambda_over_H0: `1738.74806474`
- effective_correction_status: `weak`
- max_relative_effect_to_EH: `2.69142518e-05`
- dominant_correction_term: `φ2 · R^{bcd}_{a} · R^{a}_{bcd}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-2} · R · R  +  \gamma Λ^{-4} · R^{ab} · R^{d}_{a} · R_{bd}  +  \delta Λ^{-3} · φ2 · R^{ab} · R_{ab}  +  \epsilon Λ^{-3} · φ2 · R^{bcd}_{a} · R^{a}_{bcd} )  +  \zeta Λ^{2} · φ2 · φ2  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (16.6358914263) Λ^{-2} · R · R  +  (2.7093434514e+06) Λ^{-4} · R^{ab} · R^{d}_{a} · R_{bd}  +  (7104.2215470948) Λ^{-3} · φ2 · R^{ab} · R_{ab}  +  (7.0802839862e+04) Λ^{-3} · φ2 · R^{bcd}_{a} · R^{a}_{bcd} )  +  (-1.5993792565e-05) Λ^{2} · φ2 · φ2  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-2} · R · R ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · R^{ab} · R^{d}_{a} · R_{bd} ) ] +
√(-g) [ M_p² ( \delta · Λ^{-3} · φ2 · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( \epsilon · Λ^{-3} · φ2 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ \zeta · Λ^{2} · φ2 · φ2 ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 16.6358914263 · Λ^{-2} · R · R ) ] +
√(-g) [ M_p² ( 2.7093434514e+06 · Λ^{-4} · R^{ab} · R^{d}_{a} · R_{bd} ) ] +
√(-g) [ M_p² ( 7104.2215470948 · Λ^{-3} · φ2 · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( 7.0802839862e+04 · Λ^{-3} · φ2 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ -1.5993792565e-05 · Λ^{2} · φ2 · φ2 ] +
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
    "candidate": "φ2 · R^{ab} · R_{ab}",
    "mass_dim": 5,
    "lambda_power": -3,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\epsilon",
    "coeff_token": "COEFF_4",
    "candidate": "φ2 · R^{bcd}_{a} · R^{a}_{bcd}",
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
  "max_relative_effect_to_EH": 2.6914251786223083e-05,
  "dominant_correction_term": "φ2 · R^{bcd}_{a} · R^{a}_{bcd}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 3,
  "tiny_correction_terms": 1,
  "correction_term_count": 4,
  "tiny_correction_fraction": 0.25,
  "term_effects": [
    {
      "candidate": "R · R",
      "coeff_symbol": "\\beta",
      "coefficient": "16.63589142630145",
      "lambda_power": -2,
      "sector": "gravity",
      "relative_effect_to_EH": 1.1005321994872345e-05,
      "effect_class": "weak"
    },
    {
      "candidate": "R^{ab} · R^{d}_{a} · R_{bd}",
      "coeff_symbol": "\\gamma",
      "coefficient": "2709343.451437014",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 5.928535425156708e-07,
      "effect_class": "tiny"
    },
    {
      "candidate": "φ2 · R^{ab} · R_{ab}",
      "coeff_symbol": "\\delta",
      "coefficient": "7104.221547094791",
      "lambda_power": -3,
      "sector": "non-minimal",
      "relative_effect_to_EH": 2.700524552926321e-06,
      "effect_class": "weak"
    },
    {
      "candidate": "φ2 · R^{bcd}_{a} · R^{a}_{bcd}",
      "coeff_symbol": "\\epsilon",
      "coefficient": "70802.83986177006",
      "lambda_power": -3,
      "sector": "non-minimal",
      "relative_effect_to_EH": 2.6914251786223083e-05,
      "effect_class": "weak"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0003/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0003/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0003/agent_solver_result/agent_solve/top_06_lagrangian_20_solution.csv`

## 28. wave_0022_lag_22  chi2=1946.870857

- scalar_config: `phi2_only`
- proposal_group: `non_eh`
- theory_track: `non_eh`
- potential_types: `{"phi1": null, "phi2": "axion"}`
- agent_parameter_sample_index: `311`
- H0_km_s_Mpc: `61.60953137`
- Omega_m0: `0.27299725`
- lambda_H_Lambda_over_H0: `4979.53953209`
- effective_correction_status: `unclear`
- max_relative_effect_to_EH: ``
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha Λ^{-2} · R · R  +  \beta Λ^{-3} · φ2 · R^{ab} · R_{ab}  +  \gamma Λ^{-3} · φ2 · R^{bcd}_{a} · R^{a}_{bcd}  +  \delta Λ^{-3} · ∇^{a}φ2 · ∇_{a}R  +  \epsilon Λ^{-3} · ∇^{a}∇_{a}φ2 · R )  +  \zeta Λ^{1} · ∇^{a}∇_{a}φ2  +  \eta Λ^{-2} · φ2 · φ2 · φ2 · φ2 · φ2 · φ2  +  \theta Λ^{-2} · φ2 · φ2 · ∇^{a}φ2 · ∇_{a}φ2  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (573.9304296195) Λ^{-2} · R · R  +  (-74.0883761797) Λ^{-3} · φ2 · R^{ab} · R_{ab}  +  (6.6634651875e+06) Λ^{-3} · φ2 · R^{bcd}_{a} · R^{a}_{bcd}  +  (1.9866718090e+06) Λ^{-3} · ∇^{a}φ2 · ∇_{a}R  +  (-28.0913675302) Λ^{-3} · ∇^{a}∇_{a}φ2 · R )  +  (1.1982273446e+05) Λ^{1} · ∇^{a}∇_{a}φ2  +  (-4.9181462895e+04) Λ^{-2} · φ2 · φ2 · φ2 · φ2 · φ2 · φ2  +  (3.8149576517e+09) Λ^{-2} · φ2 · φ2 · ∇^{a}φ2 · ∇_{a}φ2  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · Λ^{-2} · R · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-3} · φ2 · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-3} · φ2 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( \delta · Λ^{-3} · ∇^{a}φ2 · ∇_{a}R ) ] +
√(-g) [ M_p² ( \epsilon · Λ^{-3} · ∇^{a}∇_{a}φ2 · R ) ] +
√(-g) [ \zeta · Λ^{1} · ∇^{a}∇_{a}φ2 ] +
√(-g) [ \eta · Λ^{-2} · φ2 · φ2 · φ2 · φ2 · φ2 · φ2 ] +
√(-g) [ \theta · Λ^{-2} · φ2 · φ2 · ∇^{a}φ2 · ∇_{a}φ2 ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 573.9304296195 · Λ^{-2} · R · R ) ] +
√(-g) [ M_p² ( -74.0883761797 · Λ^{-3} · φ2 · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( 6.6634651875e+06 · Λ^{-3} · φ2 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( 1.9866718090e+06 · Λ^{-3} · ∇^{a}φ2 · ∇_{a}R ) ] +
√(-g) [ M_p² ( -28.0913675302 · Λ^{-3} · ∇^{a}∇_{a}φ2 · R ) ] +
√(-g) [ 1.1982273446e+05 · Λ^{1} · ∇^{a}∇_{a}φ2 ] +
√(-g) [ -4.9181462895e+04 · Λ^{-2} · φ2 · φ2 · φ2 · φ2 · φ2 · φ2 ] +
√(-g) [ 3.8149576517e+09 · Λ^{-2} · φ2 · φ2 · ∇^{a}φ2 · ∇_{a}φ2 ] +
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
    "candidate": "∇^{a}φ2 · ∇_{a}R",
    "mass_dim": 5,
    "lambda_power": -3,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\epsilon",
    "coeff_token": "COEFF_4",
    "candidate": "∇^{a}∇_{a}φ2 · R",
    "mass_dim": 5,
    "lambda_power": -3,
    "sector": "non-minimal"
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
    "candidate": "φ2 · φ2 · φ2 · φ2 · φ2 · φ2",
    "mass_dim": 6,
    "lambda_power": -2,
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0022/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0022/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0022/agent_solver_result/agent_solve/top_07_lagrangian_22_solution.csv`

## 29. wave_0001_lag_15  chi2=9434.002797

- scalar_config: `phi2_only`
- proposal_group: `eh_phi2_only`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": null, "phi2": "axion"}`
- agent_parameter_sample_index: `463`
- H0_km_s_Mpc: `57.799893`
- Omega_m0: `0.27673253`
- lambda_H_Lambda_over_H0: `1409.5207391`
- effective_correction_status: `weak`
- max_relative_effect_to_EH: `2.76159775e-05`
- dominant_correction_term: `R^{bcd}_{a} · R^{a}_{bcd}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd}  +  \gamma Λ^{-4} · ∇^{a}R · ∇_{a}R  +  \delta Λ^{-1} · φ2 · R )  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (27.4330038644) Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd}  +  (-9.1330655417e+06) Λ^{-4} · ∇^{a}R · ∇_{a}R  +  (-0.0300964279) Λ^{-1} · φ2 · R )  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · ∇^{a}R · ∇_{a}R ) ] +
√(-g) [ M_p² ( \delta · Λ^{-1} · φ2 · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 27.4330038644 · Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( -9.1330655417e+06 · Λ^{-4} · ∇^{a}R · ∇_{a}R ) ] +
√(-g) [ M_p² ( -0.0300964279 · Λ^{-1} · φ2 · R ) ] +
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
    "candidate": "∇^{a}R · ∇_{a}R",
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
  "max_relative_effect_to_EH": 2.7615977472954973e-05,
  "dominant_correction_term": "R^{bcd}_{a} · R^{a}_{bcd}",
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
      "coefficient": "27.433003864381273",
      "lambda_power": -2,
      "sector": "gravity",
      "relative_effect_to_EH": 2.7615977472954973e-05,
      "effect_class": "weak"
    },
    {
      "candidate": "∇^{a}R · ∇_{a}R",
      "coeff_symbol": "\\gamma",
      "coefficient": "-9133065.54169867",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 4.6276519607717715e-06,
      "effect_class": "weak"
    },
    {
      "candidate": "φ2 · R",
      "coeff_symbol": "\\delta",
      "coefficient": "-0.03009642786289648",
      "lambda_power": -1,
      "sector": "non-minimal",
      "relative_effect_to_EH": 5.0520963549625526e-06,
      "effect_class": "weak"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0001/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0001/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0001/agent_solver_result/agent_solve/top_05_lagrangian_15_solution.csv`

## 30. wave_0002_lag_4  chi2=9434.002848

- scalar_config: `phi2_only`
- proposal_group: `eh_phi2_only`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": null, "phi2": "axion"}`
- agent_parameter_sample_index: `944`
- H0_km_s_Mpc: `60.61283612`
- Omega_m0: `0.27194278`
- lambda_H_Lambda_over_H0: `1880.42424165`
- effective_correction_status: `weak`
- max_relative_effect_to_EH: `3.87703711e-06`
- dominant_correction_term: `φ2 · R`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-1} · φ2 · R )  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (0.03346693) Λ^{-1} · φ2 · R )  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
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
√(-g) [ M_p² ( 0.03346693 · Λ^{-1} · φ2 · R ) ] +
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
  "max_relative_effect_to_EH": 3.877037107960587e-06,
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
      "coefficient": "0.03346692996030852",
      "lambda_power": -1,
      "sector": "non-minimal",
      "relative_effect_to_EH": 3.877037107960587e-06,
      "effect_class": "weak"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0002/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0002/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0002/agent_solver_result/agent_solve/top_06_lagrangian_4_solution.csv`

## 31. wave_0001_lag_13  chi2=9434.003106

- scalar_config: `phi2_only`
- proposal_group: `non_eh`
- theory_track: `non_eh`
- potential_types: `{"phi1": null, "phi2": "quadratic"}`
- agent_parameter_sample_index: `783`
- H0_km_s_Mpc: `71.28905041`
- Omega_m0: `0.35862747`
- lambda_H_Lambda_over_H0: `1266.45029969`
- effective_correction_status: `unclear`
- max_relative_effect_to_EH: ``
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha Λ^{-1} · φ2 · R  +  \beta Λ^{-3} · φ2 · R · R )  +  \gamma Λ^{-1} · φ2 · φ2 · ∇^{a}∇_{a}φ2  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (-0.0099834701) Λ^{-1} · φ2 · R  +  (1.5965425712e+04) Λ^{-3} · φ2 · R · R )  +  (-1.0652926095e-06) Λ^{-1} · φ2 · φ2 · ∇^{a}∇_{a}φ2  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · Λ^{-1} · φ2 · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-3} · φ2 · R · R ) ] +
√(-g) [ \gamma · Λ^{-1} · φ2 · φ2 · ∇^{a}∇_{a}φ2 ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( -0.0099834701 · Λ^{-1} · φ2 · R ) ] +
√(-g) [ M_p² ( 1.5965425712e+04 · Λ^{-3} · φ2 · R · R ) ] +
√(-g) [ -1.0652926095e-06 · Λ^{-1} · φ2 · φ2 · ∇^{a}∇_{a}φ2 ] +
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
    "candidate": "φ2 · R · R",
    "mass_dim": 5,
    "lambda_power": -3,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\gamma",
    "coeff_token": "COEFF_2",
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0001/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0001/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0001/agent_solver_result/agent_solve/top_06_lagrangian_13_solution.csv`

## 32. wave_0002_lag_6  chi2=9434.003127

- scalar_config: `phi2_only`
- proposal_group: `eh_phi2_only`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": null, "phi2": "quadratic"}`
- agent_parameter_sample_index: `155`
- H0_km_s_Mpc: `66.94120025`
- Omega_m0: `0.39595706`
- lambda_H_Lambda_over_H0: `549.03037242`
- effective_correction_status: `moderate`
- max_relative_effect_to_EH: `0.00109638`
- dominant_correction_term: `φ2 · R`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-1} · φ2 · R )  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-0.1327790556) Λ^{-1} · φ2 · R )  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
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
√(-g) [ M_p² ( -0.1327790556 · Λ^{-1} · φ2 · R ) ] +
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
  "effective_correction_status": "moderate",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 0.0010963849919862765,
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
      "coefficient": "-0.13277905559377867",
      "lambda_power": -1,
      "sector": "non-minimal",
      "relative_effect_to_EH": 0.0010963849919862765,
      "effect_class": "moderate"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0002/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0002/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0002/agent_solver_result/agent_solve/top_07_lagrangian_6_solution.csv`

## 33. wave_0012_lag_18  chi2=9434.004088

- scalar_config: `phi2_only`
- proposal_group: `eh_phi2_only`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": null, "phi2": "quadratic"}`
- agent_parameter_sample_index: `394`
- H0_km_s_Mpc: `66.75612037`
- Omega_m0: `0.21940602`
- lambda_H_Lambda_over_H0: `1972.50467792`
- effective_correction_status: `weak`
- max_relative_effect_to_EH: `7.07721224e-05`
- dominant_correction_term: `∇^{a}R · ∇_{a}R`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh}  +  \gamma Λ^{-4} · ∇^{a}R · ∇_{a}R  +  \delta Λ^{-1} · φ2 · R  +  \epsilon Λ^{-3} · φ2 · R^{bcd}_{a} · R^{a}_{bcd} )  +  \zeta Λ^{2} · φ2 · φ2  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (6.5891354244e+07) Λ^{-4} · R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh}  +  (5.3567871664e+08) Λ^{-4} · ∇^{a}R · ∇_{a}R  +  (0.0480607604) Λ^{-1} · φ2 · R  +  (-9.1825415285e+04) Λ^{-3} · φ2 · R^{bcd}_{a} · R^{a}_{bcd} )  +  (-5.9146499621e-10) Λ^{2} · φ2 · φ2  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh} ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · ∇^{a}R · ∇_{a}R ) ] +
√(-g) [ M_p² ( \delta · Λ^{-1} · φ2 · R ) ] +
√(-g) [ M_p² ( \epsilon · Λ^{-3} · φ2 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ \zeta · Λ^{2} · φ2 · φ2 ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 6.5891354244e+07 · Λ^{-4} · R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh} ) ] +
√(-g) [ M_p² ( 5.3567871664e+08 · Λ^{-4} · ∇^{a}R · ∇_{a}R ) ] +
√(-g) [ M_p² ( 0.0480607604 · Λ^{-1} · φ2 · R ) ] +
√(-g) [ M_p² ( -9.1825415285e+04 · Λ^{-3} · φ2 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ -5.9146499621e-10 · Λ^{2} · φ2 · φ2 ] +
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
    "candidate": "R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\gamma",
    "coeff_token": "COEFF_2",
    "candidate": "∇^{a}R · ∇_{a}R",
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
    "candidate": "φ2 · R^{bcd}_{a} · R^{a}_{bcd}",
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
  "max_relative_effect_to_EH": 7.07721223789024e-05,
  "dominant_correction_term": "∇^{a}R · ∇_{a}R",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 4,
  "tiny_correction_terms": 0,
  "correction_term_count": 4,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh}",
      "coeff_symbol": "\\beta",
      "coefficient": "65891354.24391687",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 8.705350504637738e-06,
      "effect_class": "weak"
    },
    {
      "candidate": "∇^{a}R · ∇_{a}R",
      "coeff_symbol": "\\gamma",
      "coefficient": "535678716.6441784",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 7.07721223789024e-05,
      "effect_class": "weak"
    },
    {
      "candidate": "φ2 · R",
      "coeff_symbol": "\\delta",
      "coefficient": "0.04806076035568384",
      "lambda_power": -1,
      "sector": "non-minimal",
      "relative_effect_to_EH": 4.479612164122776e-06,
      "effect_class": "weak"
    },
    {
      "candidate": "φ2 · R^{bcd}_{a} · R^{a}_{bcd}",
      "coeff_symbol": "\\epsilon",
      "coefficient": "-91825.41528510893",
      "lambda_power": -3,
      "sector": "non-minimal",
      "relative_effect_to_EH": 2.199766557876966e-06,
      "effect_class": "weak"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0012/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0012/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0012/agent_solver_result/agent_solve/top_06_lagrangian_18_solution.csv`

## 34. wave_0011_lag_18  chi2=9434.005109

- scalar_config: `phi2_only`
- proposal_group: `eh_phi2_only`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": null, "phi2": "axion"}`
- agent_parameter_sample_index: `692`
- H0_km_s_Mpc: `63.50485228`
- Omega_m0: `0.32828054`
- lambda_H_Lambda_over_H0: `1376.83275658`
- effective_correction_status: `weak`
- max_relative_effect_to_EH: `2.29696657e-05`
- dominant_correction_term: `R_{ab} · R^{adef} · R^{b}_{def}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def}  +  \gamma Λ^{-1} · φ2 · R )  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (4.1271422542e+07) Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def}  +  (-0.0373530416) Λ^{-1} · φ2 · R )  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def} ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-1} · φ2 · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 4.1271422542e+07 · Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def} ) ] +
√(-g) [ M_p² ( -0.0373530416 · Λ^{-1} · φ2 · R ) ] +
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
    "candidate": "R_{ab} · R^{adef} · R^{b}_{def}",
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
  "max_relative_effect_to_EH": 2.296966570531028e-05,
  "dominant_correction_term": "R_{ab} · R^{adef} · R^{b}_{def}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 2,
  "tiny_correction_terms": 0,
  "correction_term_count": 2,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "R_{ab} · R^{adef} · R^{b}_{def}",
      "coeff_symbol": "\\beta",
      "coefficient": "41271422.5416711",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 2.296966570531028e-05,
      "effect_class": "weak"
    },
    {
      "candidate": "φ2 · R",
      "coeff_symbol": "\\gamma",
      "coefficient": "-0.0373530415591954",
      "lambda_power": -1,
      "sector": "non-minimal",
      "relative_effect_to_EH": 5.745772513032384e-06,
      "effect_class": "weak"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0011/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0011/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0011/agent_solver_result/agent_solve/top_07_lagrangian_18_solution.csv`

## 35. wave_0022_lag_19  chi2=9434.006433

- scalar_config: `phi2_only`
- proposal_group: `non_eh`
- theory_track: `non_eh`
- potential_types: `{"phi1": null, "phi2": "axion"}`
- agent_parameter_sample_index: `466`
- H0_km_s_Mpc: `67.23832304`
- Omega_m0: `0.3062713`
- lambda_H_Lambda_over_H0: `1876.88485318`
- effective_correction_status: `unclear`
- max_relative_effect_to_EH: ``
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha Λ^{-2} · R · R  +  \beta Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd}  +  \gamma Λ^{-4} · R^{ab} · R^{d}_{a} · R_{bd}  +  \delta Λ^{-4} · R^{b}_{a} · R^{cd} · R^{a}_{cbd}  +  \epsilon Λ^{-4} · φ2 · φ2 · φ2 · φ2 · R  +  \zeta Λ^{-4} · φ2 · φ2 · R^{ab} · R_{ab} )  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (4359.538032865) Λ^{-2} · R · R  +  (-8494.8740803665) Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd}  +  (-3.7231332661e+10) Λ^{-4} · R^{ab} · R^{d}_{a} · R_{bd}  +  (1.6869224919e+10) Λ^{-4} · R^{b}_{a} · R^{cd} · R^{a}_{cbd}  +  (1.0000000000e+12) Λ^{-4} · φ2 · φ2 · φ2 · φ2 · R  +  (-1.0000000000e+12) Λ^{-4} · φ2 · φ2 · R^{ab} · R_{ab} )  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · Λ^{-2} · R · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · R^{ab} · R^{d}_{a} · R_{bd} ) ] +
√(-g) [ M_p² ( \delta · Λ^{-4} · R^{b}_{a} · R^{cd} · R^{a}_{cbd} ) ] +
√(-g) [ M_p² ( \epsilon · Λ^{-4} · φ2 · φ2 · φ2 · φ2 · R ) ] +
√(-g) [ M_p² ( \zeta · Λ^{-4} · φ2 · φ2 · R^{ab} · R_{ab} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 4359.538032865 · Λ^{-2} · R · R ) ] +
√(-g) [ M_p² ( -8494.8740803665 · Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( -3.7231332661e+10 · Λ^{-4} · R^{ab} · R^{d}_{a} · R_{bd} ) ] +
√(-g) [ M_p² ( 1.6869224919e+10 · Λ^{-4} · R^{b}_{a} · R^{cd} · R^{a}_{cbd} ) ] +
√(-g) [ M_p² ( 1.0000000000e+12 · Λ^{-4} · φ2 · φ2 · φ2 · φ2 · R ) ] +
√(-g) [ M_p² ( -1.0000000000e+12 · Λ^{-4} · φ2 · φ2 · R^{ab} · R_{ab} ) ] +
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
    "candidate": "R^{bcd}_{a} · R^{a}_{bcd}",
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
    "candidate": "R^{b}_{a} · R^{cd} · R^{a}_{cbd}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\epsilon",
    "coeff_token": "COEFF_4",
    "candidate": "φ2 · φ2 · φ2 · φ2 · R",
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0022/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0022/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0022/agent_solver_result/agent_solve/top_08_lagrangian_19_solution.csv`

## 36. wave_0028_lag_15  chi2=9434.006437

- scalar_config: `phi2_only`
- proposal_group: `non_eh`
- theory_track: `non_eh`
- potential_types: `{"phi1": null, "phi2": "quadratic"}`
- agent_parameter_sample_index: `201`
- H0_km_s_Mpc: `72.69866481`
- Omega_m0: `0.33103378`
- lambda_H_Lambda_over_H0: `3462.69740675`
- effective_correction_status: `unclear`
- max_relative_effect_to_EH: ``
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha Λ^{-1} · φ2 · R  +  \beta Λ^{-2} · φ2 · φ2 · R  +  \gamma Λ^{-3} · φ2 · φ2 · φ2 · R  +  \delta Λ^{-4} · φ2 · φ2 · ∇^{a}∇_{a}R  +  \epsilon Λ^{-4} · ∇^{a}φ2 · ∇_{a}φ2 · R )  +  \zeta Λ^{-1} · φ2 · φ2 · ∇^{a}∇_{a}φ2  +  \eta Λ^{-2} · φ2 · φ2 · φ2 · ∇^{a}∇_{a}φ2  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (30.7931247508) Λ^{-1} · φ2 · R  +  (1254.3977311894) Λ^{-2} · φ2 · φ2 · R  +  (9.5797104139) Λ^{-3} · φ2 · φ2 · φ2 · R  +  (637.6684701895) Λ^{-4} · φ2 · φ2 · ∇^{a}∇_{a}R  +  (8597.3055411101) Λ^{-4} · ∇^{a}φ2 · ∇_{a}φ2 · R )  +  (9.3261480538e+05) Λ^{-1} · φ2 · φ2 · ∇^{a}∇_{a}φ2  +  (3.0326817343e+05) Λ^{-2} · φ2 · φ2 · φ2 · ∇^{a}∇_{a}φ2  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · Λ^{-1} · φ2 · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-2} · φ2 · φ2 · R ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-3} · φ2 · φ2 · φ2 · R ) ] +
√(-g) [ M_p² ( \delta · Λ^{-4} · φ2 · φ2 · ∇^{a}∇_{a}R ) ] +
√(-g) [ M_p² ( \epsilon · Λ^{-4} · ∇^{a}φ2 · ∇_{a}φ2 · R ) ] +
√(-g) [ \zeta · Λ^{-1} · φ2 · φ2 · ∇^{a}∇_{a}φ2 ] +
√(-g) [ \eta · Λ^{-2} · φ2 · φ2 · φ2 · ∇^{a}∇_{a}φ2 ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 30.7931247508 · Λ^{-1} · φ2 · R ) ] +
√(-g) [ M_p² ( 1254.3977311894 · Λ^{-2} · φ2 · φ2 · R ) ] +
√(-g) [ M_p² ( 9.5797104139 · Λ^{-3} · φ2 · φ2 · φ2 · R ) ] +
√(-g) [ M_p² ( 637.6684701895 · Λ^{-4} · φ2 · φ2 · ∇^{a}∇_{a}R ) ] +
√(-g) [ M_p² ( 8597.3055411101 · Λ^{-4} · ∇^{a}φ2 · ∇_{a}φ2 · R ) ] +
√(-g) [ 9.3261480538e+05 · Λ^{-1} · φ2 · φ2 · ∇^{a}∇_{a}φ2 ] +
√(-g) [ 3.0326817343e+05 · Λ^{-2} · φ2 · φ2 · φ2 · ∇^{a}∇_{a}φ2 ] +
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
    "candidate": "φ2 · φ2 · R",
    "mass_dim": 4,
    "lambda_power": -2,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\gamma",
    "coeff_token": "COEFF_2",
    "candidate": "φ2 · φ2 · φ2 · R",
    "mass_dim": 5,
    "lambda_power": -3,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\delta",
    "coeff_token": "COEFF_3",
    "candidate": "φ2 · φ2 · ∇^{a}∇_{a}R",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\epsilon",
    "coeff_token": "COEFF_4",
    "candidate": "∇^{a}φ2 · ∇_{a}φ2 · R",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\zeta",
    "coeff_token": "COEFF_5",
    "candidate": "φ2 · φ2 · ∇^{a}∇_{a}φ2",
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0028/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0028/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0028/agent_solver_result/agent_solve/top_05_lagrangian_15_solution.csv`

## 37. wave_0026_lag_6  chi2=9434.006557

- scalar_config: `both`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "quadratic", "phi2": "axion"}`
- agent_parameter_sample_index: `515`
- H0_km_s_Mpc: `60.70189054`
- Omega_m0: `0.27013443`
- lambda_H_Lambda_over_H0: `5993.65426881`
- effective_correction_status: `moderate`
- max_relative_effect_to_EH: `0.00116638`
- dominant_correction_term: `φ2 · R`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-1} · φ2 · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (3529.5287247258) Λ^{-1} · φ2 · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
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
√(-g) [ M_p² ( 3529.5287247258 · Λ^{-1} · φ2 · R ) ] +
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
  "max_relative_effect_to_EH": 0.0011663824802000775,
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
      "coefficient": "3529.5287247257743",
      "lambda_power": -1,
      "sector": "non-minimal",
      "relative_effect_to_EH": 0.0011663824802000775,
      "effect_class": "moderate"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0026/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0026/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0026/agent_solver_result/agent_solve/top_08_lagrangian_6_solution.csv`

## 38. wave_0027_lag_3  chi2=9434.006855

- scalar_config: `phi2_only`
- proposal_group: `non_eh`
- theory_track: `non_eh`
- potential_types: `{"phi1": null, "phi2": "quadratic"}`
- agent_parameter_sample_index: `871`
- H0_km_s_Mpc: `74.16752293`
- Omega_m0: `0.27709766`
- lambda_H_Lambda_over_H0: `6899.63726839`
- effective_correction_status: `unclear`
- max_relative_effect_to_EH: ``
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha Λ^{-2} · φ2 · φ2 · R )  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (1.2239889301e+06) Λ^{-2} · φ2 · φ2 · R )  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · Λ^{-2} · φ2 · φ2 · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 1.2239889301e+06 · Λ^{-2} · φ2 · φ2 · R ) ] +
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0027/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0027/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0027/agent_solver_result/agent_solve/top_07_lagrangian_3_solution.csv`

## 39. wave_0024_lag_2  chi2=9434.007215

- scalar_config: `phi2_only`
- proposal_group: `non_eh`
- theory_track: `non_eh`
- potential_types: `{"phi1": null, "phi2": "axion"}`
- agent_parameter_sample_index: `21`
- H0_km_s_Mpc: `72.5312822`
- Omega_m0: `0.25889844`
- lambda_H_Lambda_over_H0: `9276.59145921`
- effective_correction_status: `unclear`
- max_relative_effect_to_EH: ``
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha Λ^{-3} · φ2 · φ2 · φ2 · R )  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (1.1496782352e+08) Λ^{-3} · φ2 · φ2 · φ2 · R )  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · Λ^{-3} · φ2 · φ2 · φ2 · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 1.1496782352e+08 · Λ^{-3} · φ2 · φ2 · φ2 · R ) ] +
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0024/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0024/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0024/agent_solver_result/agent_solve/top_06_lagrangian_2_solution.csv`

## 40. wave_0003_lag_14  chi2=9434.007303

- scalar_config: `both`
- proposal_group: `non_eh`
- theory_track: `non_eh`
- potential_types: `{"phi1": "axion", "phi2": "quadratic"}`
- agent_parameter_sample_index: `449`
- H0_km_s_Mpc: `58.72848735`
- Omega_m0: `0.36915139`
- lambda_H_Lambda_over_H0: `1277.67697693`
- effective_correction_status: `unclear`
- max_relative_effect_to_EH: ``
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha Λ^{-2} · φ2 · φ2 · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (-0.8145337851) Λ^{-2} · φ2 · φ2 · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · Λ^{-2} · φ2 · φ2 · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( -0.8145337851 · Λ^{-2} · φ2 · φ2 · R ) ] +
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0003/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0003/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_912_triad_v1_wave_0003/agent_solver_result/agent_solve/top_08_lagrangian_14_solution.csv`
