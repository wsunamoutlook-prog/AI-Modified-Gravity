# Accepted Lagrangians And Parameters

Each entry is the best chi-square representative of one accepted theory family.
The full accepted-attempt list is preserved in `accepted_summary.json`.
Each displayed entry uses the actual `agent_lagrangians.pkl` object that entered EOM -> Builder -> Solver.

## 1. wave_0011_lag_8  chi2=1638.042839

- scalar_config: `phi1_only`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: `410`
- H0_km_s_Mpc: `65.42949628`
- Omega_m0: `0.27342163`
- lambda_H_Lambda_over_H0: `2329.56446586`
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0011/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0011/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0011/agent_solver_result/agent_solve/top_01_lagrangian_8_solution.csv`

## 2. wave_0004_lag_8  chi2=1639.029936

- scalar_config: `phi1_only`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: `476`
- H0_km_s_Mpc: `70.46081395`
- Omega_m0: `0.29304078`
- lambda_H_Lambda_over_H0: `1010.3900358`
- effective_correction_status: `moderate`
- max_relative_effect_to_EH: `2.93455739e-04`
- dominant_correction_term: `φ1 · ∇^{a}∇_{a}R`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-3} · φ1 · ∇^{a}∇_{a}R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (9.4150749241e+04) Λ^{-3} · φ1 · ∇^{a}∇_{a}R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-3} · φ1 · ∇^{a}∇_{a}R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 9.4150749241e+04 · Λ^{-3} · φ1 · ∇^{a}∇_{a}R ) ] +
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
]
```

### Effective Correction Diagnostics

```json
{
  "effective_correction_status": "moderate",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 0.00029345573912236203,
  "dominant_correction_term": "φ1 · ∇^{a}∇_{a}R",
  "active_correction_terms": 0,
  "moderate_correction_terms": 1,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 0,
  "correction_term_count": 1,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "φ1 · ∇^{a}∇_{a}R",
      "coeff_symbol": "\\beta",
      "coefficient": "94150.74924085995",
      "lambda_power": -3,
      "sector": "non-minimal",
      "relative_effect_to_EH": 0.00029345573912236203,
      "effect_class": "moderate"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0004/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0004/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0004/agent_solver_result/agent_solve/top_01_lagrangian_8_solution.csv`

## 3. wave_0005_lag_7  chi2=1640.959345

- scalar_config: `phi1_only`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: `584`
- H0_km_s_Mpc: `72.61043866`
- Omega_m0: `0.28260554`
- lambda_H_Lambda_over_H0: `1.64136710e+04`
- effective_correction_status: `weak`
- max_relative_effect_to_EH: `8.15425035e-06`
- dominant_correction_term: `∇^{a}φ1 · ∇^{b}φ1 · R_{ab}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-2} · R · R  +  \gamma Λ^{-4} · ∇^{a}φ1 · ∇^{b}φ1 · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-387.9684203977) Λ^{-2} · R · R  +  (3.3578381026e+10) Λ^{-4} · ∇^{a}φ1 · ∇^{b}φ1 · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-2} · R · R ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · ∇^{a}φ1 · ∇^{b}φ1 · R_{ab} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -387.9684203977 · Λ^{-2} · R · R ) ] +
√(-g) [ M_p² ( 3.3578381026e+10 · Λ^{-4} · ∇^{a}φ1 · ∇^{b}φ1 · R_{ab} ) ] +
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
]
```

### Effective Correction Diagnostics

```json
{
  "effective_correction_status": "weak",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 8.154250352690893e-06,
  "dominant_correction_term": "∇^{a}φ1 · ∇^{b}φ1 · R_{ab}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 2,
  "tiny_correction_terms": 0,
  "correction_term_count": 2,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "R · R",
      "coeff_symbol": "\\beta",
      "coefficient": "-387.968420397726",
      "lambda_power": -2,
      "sector": "gravity",
      "relative_effect_to_EH": 2.880148794483972e-06,
      "effect_class": "weak"
    },
    {
      "candidate": "∇^{a}φ1 · ∇^{b}φ1 · R_{ab}",
      "coeff_symbol": "\\gamma",
      "coefficient": "33578381025.837135",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 8.154250352690893e-06,
      "effect_class": "weak"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0005/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0005/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0005/agent_solver_result/agent_solve/top_02_lagrangian_7_solution.csv`

## 4. wave_0002_lag_4  chi2=1643.892678

- scalar_config: `phi1_only`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: `928`
- H0_km_s_Mpc: `69.90278298`
- Omega_m0: `0.27750908`
- lambda_H_Lambda_over_H0: `5.19710758e+04`
- effective_correction_status: `weak`
- max_relative_effect_to_EH: `1.02509173e-06`
- dominant_correction_term: `φ1 · φ1 · R^{ab} · R_{ab}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · φ1 · φ1 · R^{ab} · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (1.0000000000e+12) Λ^{-4} · φ1 · φ1 · R^{ab} · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · φ1 · φ1 · R^{ab} · R_{ab} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 1.0000000000e+12 · Λ^{-4} · φ1 · φ1 · R^{ab} · R_{ab} ) ] +
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
  "max_relative_effect_to_EH": 1.0250917336927913e-06,
  "dominant_correction_term": "φ1 · φ1 · R^{ab} · R_{ab}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 1,
  "tiny_correction_terms": 0,
  "correction_term_count": 1,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "φ1 · φ1 · R^{ab} · R_{ab}",
      "coeff_symbol": "\\beta",
      "coefficient": "1000000000000.0",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 1.0250917336927913e-06,
      "effect_class": "weak"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0002/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0002/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0002/agent_solver_result/agent_solve/top_01_lagrangian_4_solution.csv`

## 5. wave_0005_lag_6  chi2=1644.803417

- scalar_config: `phi1_only`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: `396`
- H0_km_s_Mpc: `74.93778947`
- Omega_m0: `0.31688055`
- lambda_H_Lambda_over_H0: `3842.99431148`
- effective_correction_status: `eh_only`
- max_relative_effect_to_EH: `0`
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R )  +  \beta · φ1 · ∇^{a}∇_{a}φ1  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R )  +  (2.0305536290e-07) · φ1 · ∇^{a}∇_{a}φ1  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ \beta · φ1 · ∇^{a}∇_{a}φ1 ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ 2.0305536290e-07 · φ1 · ∇^{a}∇_{a}φ1 ] +
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0005/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0005/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0005/agent_solver_result/agent_solve/top_04_lagrangian_6_solution.csv`

## 6. wave_0003_lag_6  chi2=1645.440639

- scalar_config: `phi1_only`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: `377`
- H0_km_s_Mpc: `68.4523603`
- Omega_m0: `0.28351`
- lambda_H_Lambda_over_H0: `6.90404485e+04`
- effective_correction_status: `eh_dominated`
- max_relative_effect_to_EH: `8.80269349e-08`
- dominant_correction_term: `∇^{c}R^{ab} · ∇_{b}R_{ac}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · ∇^{c}R^{ab} · ∇_{b}R_{ac} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (1.0000000000e+12) Λ^{-4} · ∇^{c}R^{ab} · ∇_{b}R_{ac} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · ∇^{c}R^{ab} · ∇_{b}R_{ac} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 1.0000000000e+12 · Λ^{-4} · ∇^{c}R^{ab} · ∇_{b}R_{ac} ) ] +
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
  "max_relative_effect_to_EH": 8.802693489254469e-08,
  "dominant_correction_term": "∇^{c}R^{ab} · ∇_{b}R_{ac}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 1,
  "correction_term_count": 1,
  "tiny_correction_fraction": 1.0,
  "term_effects": [
    {
      "candidate": "∇^{c}R^{ab} · ∇_{b}R_{ac}",
      "coeff_symbol": "\\beta",
      "coefficient": "1000000000000.0",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 8.802693489254469e-08,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0003/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0003/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0003/agent_solver_result/agent_solve/top_01_lagrangian_6_solution.csv`

## 7. wave_0013_lag_6  chi2=1647.038092

- scalar_config: `phi1_only`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: `886`
- H0_km_s_Mpc: `61.25898555`
- Omega_m0: `0.32281457`
- lambda_H_Lambda_over_H0: `5.09372246e+04`
- effective_correction_status: `moderate`
- max_relative_effect_to_EH: `1.87734934e-04`
- dominant_correction_term: `R^{ab} · R_{ab}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-2} · R^{ab} · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (2.4354860974e+05) Λ^{-2} · R^{ab} · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
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
√(-g) [ M_p² ( 2.4354860974e+05 · Λ^{-2} · R^{ab} · R_{ab} ) ] +
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
  "max_relative_effect_to_EH": 0.0001877349338779395,
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
      "coefficient": "243548.60973612312",
      "lambda_power": -2,
      "sector": "gravity",
      "relative_effect_to_EH": 0.0001877349338779395,
      "effect_class": "moderate"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0013/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0013/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0013/agent_solver_result/agent_solve/top_02_lagrangian_6_solution.csv`

## 8. wave_0013_lag_12  chi2=1647.387644

- scalar_config: `phi1_only`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "axion", "phi2": null}`
- agent_parameter_sample_index: `397`
- H0_km_s_Mpc: `73.8935027`
- Omega_m0: `0.23531759`
- lambda_H_Lambda_over_H0: `1.05750557e+04`
- effective_correction_status: `moderate`
- max_relative_effect_to_EH: `0.00103869`
- dominant_correction_term: `∇^{a}∇_{a}φ1 · R`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-3} · ∇^{a}∇_{a}φ1 · R  +  \gamma Λ^{-4} · φ1 · ∇^{a}∇_{a}φ1 · R  +  \delta Λ^{-4} · ∇^{a}φ1 · ∇_{a}φ1 · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-4.1815686208e+08) Λ^{-3} · ∇^{a}∇_{a}φ1 · R  +  (-1.0000000000e+12) Λ^{-4} · φ1 · ∇^{a}∇_{a}φ1 · R  +  (1.0000000000e+12) Λ^{-4} · ∇^{a}φ1 · ∇_{a}φ1 · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-3} · ∇^{a}∇_{a}φ1 · R ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · φ1 · ∇^{a}∇_{a}φ1 · R ) ] +
√(-g) [ M_p² ( \delta · Λ^{-4} · ∇^{a}φ1 · ∇_{a}φ1 · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -4.1815686208e+08 · Λ^{-3} · ∇^{a}∇_{a}φ1 · R ) ] +
√(-g) [ M_p² ( -1.0000000000e+12 · Λ^{-4} · φ1 · ∇^{a}∇_{a}φ1 · R ) ] +
√(-g) [ M_p² ( 1.0000000000e+12 · Λ^{-4} · ∇^{a}φ1 · ∇_{a}φ1 · R ) ] +
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
    "candidate": "∇^{a}∇_{a}φ1 · R",
    "mass_dim": 5,
    "lambda_power": -3,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\gamma",
    "coeff_token": "COEFF_2",
    "candidate": "φ1 · ∇^{a}∇_{a}φ1 · R",
    "mass_dim": 6,
    "lambda_power": -4,
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
  "max_relative_effect_to_EH": 0.0010386884925980473,
  "dominant_correction_term": "∇^{a}∇_{a}φ1 · R",
  "active_correction_terms": 0,
  "moderate_correction_terms": 3,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 0,
  "correction_term_count": 3,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "∇^{a}∇_{a}φ1 · R",
      "coeff_symbol": "\\beta",
      "coefficient": "-418156862.0770818",
      "lambda_power": -3,
      "sector": "non-minimal",
      "relative_effect_to_EH": 0.0010386884925980473,
      "effect_class": "moderate"
    },
    {
      "candidate": "φ1 · ∇^{a}∇_{a}φ1 · R",
      "coeff_symbol": "\\gamma",
      "coefficient": "-1000000000000.0",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 0.00034500668895250916,
      "effect_class": "moderate"
    },
    {
      "candidate": "∇^{a}φ1 · ∇_{a}φ1 · R",
      "coeff_symbol": "\\delta",
      "coefficient": "1000000000000.0",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 0.00034500668895250916,
      "effect_class": "moderate"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0013/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0013/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0013/agent_solver_result/agent_solve/top_03_lagrangian_12_solution.csv`

## 9. wave_0008_lag_8  chi2=1651.956163

- scalar_config: `phi1_only`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "axion", "phi2": null}`
- agent_parameter_sample_index: `178`
- H0_km_s_Mpc: `58.64378807`
- Omega_m0: `0.32376822`
- lambda_H_Lambda_over_H0: `1.93837159e+04`
- effective_correction_status: `eh_only`
- max_relative_effect_to_EH: `0`
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R )  +  \beta · ∇^{a}φ1 · ∇_{a}φ1  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R )  +  (-1.1919302624e-08) · ∇^{a}φ1 · ∇_{a}φ1  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ \beta · ∇^{a}φ1 · ∇_{a}φ1 ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ -1.1919302624e-08 · ∇^{a}φ1 · ∇_{a}φ1 ] +
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0008/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0008/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0008/agent_solver_result/agent_solve/top_01_lagrangian_8_solution.csv`

## 10. wave_0012_lag_4  chi2=1656.395923

- scalar_config: `phi1_only`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "axion", "phi2": null}`
- agent_parameter_sample_index: `90`
- H0_km_s_Mpc: `71.69623591`
- Omega_m0: `0.26050662`
- lambda_H_Lambda_over_H0: `7758.51261887`
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0012/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0012/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0012/agent_solver_result/agent_solve/top_01_lagrangian_4_solution.csv`

## 11. wave_0010_lag_5  chi2=1659.252065

- scalar_config: `phi1_only`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: `360`
- H0_km_s_Mpc: `66.14233061`
- Omega_m0: `0.25768118`
- lambda_H_Lambda_over_H0: `2023.71455179`
- effective_correction_status: `active`
- max_relative_effect_to_EH: `0.02641054`
- dominant_correction_term: `φ1 · R^{bcd}_{a} · R^{a}_{bcd}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-9.2185552587e+07) Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
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
√(-g) [ M_p² ( -9.2185552587e+07 · Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
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
  "effective_correction_status": "active",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 0.026410544901929636,
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
      "coefficient": "-92185552.58693016",
      "lambda_power": -3,
      "sector": "non-minimal",
      "relative_effect_to_EH": 0.026410544901929636,
      "effect_class": "active"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0010/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0010/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0010/agent_solver_result/agent_solve/top_02_lagrangian_5_solution.csv`

## 12. wave_0001_lag_15  chi2=9431.932834

- scalar_config: `phi2_only`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": null, "phi2": "axion"}`
- agent_parameter_sample_index: `84`
- H0_km_s_Mpc: `69.58704347`
- Omega_m0: `0.3814248`
- lambda_H_Lambda_over_H0: `6.65471870e+04`
- effective_correction_status: `weak`
- max_relative_effect_to_EH: `2.55992205e-05`
- dominant_correction_term: `φ2 · R^{ab} · R_{ab}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-3} · φ2 · R^{ab} · R_{ab}  +  \gamma Λ^{-3} · ∇^{a}∇_{a}φ2 · R  +  \delta Λ^{-4} · φ2 · φ2 · φ2 · φ2 · R  +  \epsilon Λ^{-4} · φ2 · φ2 · R^{ab} · R_{ab}  +  \zeta Λ^{-4} · φ2 · φ2 · R^{bcd}_{a} · R^{a}_{bcd}  +  \eta Λ^{-4} · ∇^{a}φ2 · ∇_{a}φ2 · R )  +  \theta Λ^{1} · ∇^{a}∇_{a}φ2  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-1.0000000000e+12) Λ^{-3} · φ2 · R^{ab} · R_{ab}  +  (9.6491399999e+11) Λ^{-3} · ∇^{a}∇_{a}φ2 · R  +  (-1.0000000000e+12) Λ^{-4} · φ2 · φ2 · φ2 · φ2 · R  +  (1.0000000000e+12) Λ^{-4} · φ2 · φ2 · R^{ab} · R_{ab}  +  (1.0000000000e+12) Λ^{-4} · φ2 · φ2 · R^{bcd}_{a} · R^{a}_{bcd}  +  (-1.0000000000e+12) Λ^{-4} · ∇^{a}φ2 · ∇_{a}φ2 · R )  +  (9.6941005933e-10) Λ^{1} · ∇^{a}∇_{a}φ2  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-3} · φ2 · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-3} · ∇^{a}∇_{a}φ2 · R ) ] +
√(-g) [ M_p² ( \delta · Λ^{-4} · φ2 · φ2 · φ2 · φ2 · R ) ] +
√(-g) [ M_p² ( \epsilon · Λ^{-4} · φ2 · φ2 · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( \zeta · Λ^{-4} · φ2 · φ2 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( \eta · Λ^{-4} · ∇^{a}φ2 · ∇_{a}φ2 · R ) ] +
√(-g) [ \theta · Λ^{1} · ∇^{a}∇_{a}φ2 ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -1.0000000000e+12 · Λ^{-3} · φ2 · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( 9.6491399999e+11 · Λ^{-3} · ∇^{a}∇_{a}φ2 · R ) ] +
√(-g) [ M_p² ( -1.0000000000e+12 · Λ^{-4} · φ2 · φ2 · φ2 · φ2 · R ) ] +
√(-g) [ M_p² ( 1.0000000000e+12 · Λ^{-4} · φ2 · φ2 · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( 1.0000000000e+12 · Λ^{-4} · φ2 · φ2 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( -1.0000000000e+12 · Λ^{-4} · ∇^{a}φ2 · ∇_{a}φ2 · R ) ] +
√(-g) [ 9.6941005933e-10 · Λ^{1} · ∇^{a}∇_{a}φ2 ] +
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
    "coeff_symbol": "\\gamma",
    "coeff_token": "COEFF_2",
    "candidate": "∇^{a}∇_{a}φ2 · R",
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
    "candidate": "∇^{a}∇_{a}φ2",
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
  "max_relative_effect_to_EH": 2.559922047518842e-05,
  "dominant_correction_term": "φ2 · R^{ab} · R_{ab}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 2,
  "tiny_correction_terms": 4,
  "correction_term_count": 6,
  "tiny_correction_fraction": 0.6666666666666666,
  "term_effects": [
    {
      "candidate": "φ2 · R^{ab} · R_{ab}",
      "coeff_symbol": "\\beta",
      "coefficient": "-1000000000000.0",
      "lambda_power": -3,
      "sector": "non-minimal",
      "relative_effect_to_EH": 2.559922047518842e-05,
      "effect_class": "weak"
    },
    {
      "candidate": "∇^{a}∇_{a}φ2 · R",
      "coeff_symbol": "\\gamma",
      "coefficient": "964913999989.7181",
      "lambda_power": -3,
      "sector": "non-minimal",
      "relative_effect_to_EH": 2.4701046225332748e-05,
      "effect_class": "weak"
    },
    {
      "candidate": "φ2 · φ2 · φ2 · φ2 · R",
      "coeff_symbol": "\\delta",
      "coefficient": "-1000000000000.0",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 2.0646887564314058e-17,
      "effect_class": "tiny"
    },
    {
      "candidate": "φ2 · φ2 · R^{ab} · R_{ab}",
      "coeff_symbol": "\\epsilon",
      "coefficient": "1000000000000.0",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 1.4510517123750838e-12,
      "effect_class": "tiny"
    },
    {
      "candidate": "φ2 · φ2 · R^{bcd}_{a} · R^{a}_{bcd}",
      "coeff_symbol": "\\zeta",
      "coefficient": "1000000000000.0",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 1.4510517123750838e-12,
      "effect_class": "tiny"
    },
    {
      "candidate": "∇^{a}φ2 · ∇_{a}φ2 · R",
      "coeff_symbol": "\\eta",
      "coefficient": "-1000000000000.0",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 1.4510517123750838e-12,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0001/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0001/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0001/agent_solver_result/agent_solve/top_02_lagrangian_15_solution.csv`

## 13. wave_0013_lag_16  chi2=9434.003155

- scalar_config: `phi2_only`
- theory_track: `non_eh`
- potential_types: `{"phi1": null, "phi2": "quadratic"}`
- agent_parameter_sample_index: `34`
- H0_km_s_Mpc: `74.7039342`
- Omega_m0: `0.31052926`
- lambda_H_Lambda_over_H0: `1055.39966007`
- effective_correction_status: `unclear`
- max_relative_effect_to_EH: ``
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{fdh}  +  \beta Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf}  +  \gamma Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def}  +  \delta Λ^{-1} · φ2 · R  +  \epsilon Λ^{-3} · φ2 · R^{ab} · R_{ab}  +  \zeta Λ^{-4} · φ2 · φ2 · R^{ab} · R_{ab} )  +  \eta Λ^{1} · φ2 · φ2 · φ2  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (-6.5563394510e+06) Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{fdh}  +  (1.4081161346e+06) Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf}  +  (3.6921821924e+06) Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def}  +  (-0.0108045928) Λ^{-1} · φ2 · R  +  (1.3492656773e+05) Λ^{-3} · φ2 · R^{ab} · R_{ab}  +  (-7.5125722511e+08) Λ^{-4} · φ2 · φ2 · R^{ab} · R_{ab} )  +  (1.0712703246e-05) Λ^{1} · φ2 · φ2 · φ2  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{fdh} ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf} ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def} ) ] +
√(-g) [ M_p² ( \delta · Λ^{-1} · φ2 · R ) ] +
√(-g) [ M_p² ( \epsilon · Λ^{-3} · φ2 · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( \zeta · Λ^{-4} · φ2 · φ2 · R^{ab} · R_{ab} ) ] +
√(-g) [ \eta · Λ^{1} · φ2 · φ2 · φ2 ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( -6.5563394510e+06 · Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{fdh} ) ] +
√(-g) [ M_p² ( 1.4081161346e+06 · Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf} ) ] +
√(-g) [ M_p² ( 3.6921821924e+06 · Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def} ) ] +
√(-g) [ M_p² ( -0.0108045928 · Λ^{-1} · φ2 · R ) ] +
√(-g) [ M_p² ( 1.3492656773e+05 · Λ^{-3} · φ2 · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( -7.5125722511e+08 · Λ^{-4} · φ2 · φ2 · R^{ab} · R_{ab} ) ] +
√(-g) [ 1.0712703246e-05 · Λ^{1} · φ2 · φ2 · φ2 ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Term Metadata

```json
[
  {
    "coeff_symbol": "\\alpha",
    "coeff_token": "COEFF_0",
    "candidate": "R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{fdh}",
    "mass_dim": 6,
    "lambda_power": -4,
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
    "candidate": "φ2 · R^{ab} · R_{ab}",
    "mass_dim": 5,
    "lambda_power": -3,
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0013/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0013/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0013/agent_solver_result/agent_solve/top_07_lagrangian_16_solution.csv`

## 14. wave_0004_lag_11  chi2=9434.004829

- scalar_config: `phi2_only`
- theory_track: `non_eh`
- potential_types: `{"phi1": null, "phi2": "axion"}`
- agent_parameter_sample_index: `819`
- H0_km_s_Mpc: `72.32392869`
- Omega_m0: `0.32581616`
- lambda_H_Lambda_over_H0: `592.51253179`
- effective_correction_status: `unclear`
- max_relative_effect_to_EH: ``
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha Λ^{-2} · R · R  +  \beta Λ^{-1} · φ2 · R )  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (-13.2617324028) Λ^{-2} · R · R  +  (-0.0570482742) Λ^{-1} · φ2 · R )  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · Λ^{-2} · R · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-1} · φ2 · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( -13.2617324028 · Λ^{-2} · R · R ) ] +
√(-g) [ M_p² ( -0.0570482742 · Λ^{-1} · φ2 · R ) ] +
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0004/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0004/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0004/agent_solver_result/agent_solve/top_08_lagrangian_11_solution.csv`

## 15. wave_0002_lag_9  chi2=9434.006131

- scalar_config: `both`
- theory_track: `non_eh`
- potential_types: `{"phi1": "quadratic", "phi2": "axion"}`
- agent_parameter_sample_index: `34`
- H0_km_s_Mpc: `64.93892288`
- Omega_m0: `0.30201192`
- lambda_H_Lambda_over_H0: `5785.16951458`
- effective_correction_status: `unclear`
- max_relative_effect_to_EH: ``
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha Λ^{-1} · φ2 · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.1164196108) Λ^{-1} · φ2 · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
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
√(-g) [ M_p² ( 0.1164196108 · Λ^{-1} · φ2 · R ) ] +
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0002/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0002/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0002/agent_solver_result/agent_solve/top_06_lagrangian_9_solution.csv`

## 16. wave_0003_lag_16  chi2=9434.007647

- scalar_config: `phi2_only`
- theory_track: `non_eh`
- potential_types: `{"phi1": null, "phi2": "quadratic"}`
- agent_parameter_sample_index: `642`
- H0_km_s_Mpc: `61.04414733`
- Omega_m0: `0.37401788`
- lambda_H_Lambda_over_H0: `764.31858552`
- effective_correction_status: `unclear`
- max_relative_effect_to_EH: ``
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha Λ^{-2} · R^{ab} · R_{ab}  +  \beta Λ^{-4} · R^{b}_{a} · R^{cd} · R^{a}_{cbd}  +  \gamma Λ^{-2} · φ2 · φ2 · R  +  \delta Λ^{-3} · ∇^{a}∇_{a}φ2 · R  +  \epsilon Λ^{-4} · φ2 · ∇^{a}φ2 · ∇_{a}R )  +  \zeta Λ^{-1} · φ2 · ∇^{a}φ2 · ∇_{a}φ2  +  \eta Λ^{-2} · φ2 · φ2 · φ2 · ∇^{a}∇_{a}φ2  +  \theta Λ^{-2} · φ2 · φ2 · ∇^{a}φ2 · ∇_{a}φ2  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (-9.1518968646) Λ^{-2} · R^{ab} · R_{ab}  +  (-1.5771283790e+06) Λ^{-4} · R^{b}_{a} · R^{cd} · R^{a}_{cbd}  +  (-0.0323676893) Λ^{-2} · φ2 · φ2 · R  +  (-159.3945486495) Λ^{-3} · ∇^{a}∇_{a}φ2 · R  +  (-6.6157175747e+05) Λ^{-4} · φ2 · ∇^{a}φ2 · ∇_{a}R )  +  (9.8480873222e-07) Λ^{-1} · φ2 · ∇^{a}φ2 · ∇_{a}φ2  +  (2.0319138462e-05) Λ^{-2} · φ2 · φ2 · φ2 · ∇^{a}∇_{a}φ2  +  (-4.5225024574e-09) Λ^{-2} · φ2 · φ2 · ∇^{a}φ2 · ∇_{a}φ2  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · Λ^{-2} · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · R^{b}_{a} · R^{cd} · R^{a}_{cbd} ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-2} · φ2 · φ2 · R ) ] +
√(-g) [ M_p² ( \delta · Λ^{-3} · ∇^{a}∇_{a}φ2 · R ) ] +
√(-g) [ M_p² ( \epsilon · Λ^{-4} · φ2 · ∇^{a}φ2 · ∇_{a}R ) ] +
√(-g) [ \zeta · Λ^{-1} · φ2 · ∇^{a}φ2 · ∇_{a}φ2 ] +
√(-g) [ \eta · Λ^{-2} · φ2 · φ2 · φ2 · ∇^{a}∇_{a}φ2 ] +
√(-g) [ \theta · Λ^{-2} · φ2 · φ2 · ∇^{a}φ2 · ∇_{a}φ2 ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( -9.1518968646 · Λ^{-2} · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( -1.5771283790e+06 · Λ^{-4} · R^{b}_{a} · R^{cd} · R^{a}_{cbd} ) ] +
√(-g) [ M_p² ( -0.0323676893 · Λ^{-2} · φ2 · φ2 · R ) ] +
√(-g) [ M_p² ( -159.3945486495 · Λ^{-3} · ∇^{a}∇_{a}φ2 · R ) ] +
√(-g) [ M_p² ( -6.6157175747e+05 · Λ^{-4} · φ2 · ∇^{a}φ2 · ∇_{a}R ) ] +
√(-g) [ 9.8480873222e-07 · Λ^{-1} · φ2 · ∇^{a}φ2 · ∇_{a}φ2 ] +
√(-g) [ 2.0319138462e-05 · Λ^{-2} · φ2 · φ2 · φ2 · ∇^{a}∇_{a}φ2 ] +
√(-g) [ -4.5225024574e-09 · Λ^{-2} · φ2 · φ2 · ∇^{a}φ2 · ∇_{a}φ2 ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Term Metadata

```json
[
  {
    "coeff_symbol": "\\alpha",
    "coeff_token": "COEFF_0",
    "candidate": "R^{ab} · R_{ab}",
    "mass_dim": 4,
    "lambda_power": -2,
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
    "candidate": "φ2 · φ2 · R",
    "mass_dim": 4,
    "lambda_power": -2,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\delta",
    "coeff_token": "COEFF_3",
    "candidate": "∇^{a}∇_{a}φ2 · R",
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0003/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0003/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0003/agent_solver_result/agent_solve/top_07_lagrangian_16_solution.csv`

## 17. wave_0001_lag_8  chi2=9434.007984

- scalar_config: `phi2_only`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": null, "phi2": "axion"}`
- agent_parameter_sample_index: `245`
- H0_km_s_Mpc: `71.02996692`
- Omega_m0: `0.35071928`
- lambda_H_Lambda_over_H0: `5.72325671e+04`
- effective_correction_status: `eh_dominated`
- max_relative_effect_to_EH: `1.70311165e-12`
- dominant_correction_term: `φ2 · φ2 · φ2 · R`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-3} · φ2 · φ2 · φ2 · R )  +  \gamma Λ^{1} · ∇^{a}∇_{a}φ2  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (1.0000000000e+12) Λ^{-3} · φ2 · φ2 · φ2 · R )  +  (-4.0687197860e-07) Λ^{1} · ∇^{a}∇_{a}φ2  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-3} · φ2 · φ2 · φ2 · R ) ] +
√(-g) [ \gamma · Λ^{1} · ∇^{a}∇_{a}φ2 ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 1.0000000000e+12 · Λ^{-3} · φ2 · φ2 · φ2 · R ) ] +
√(-g) [ -4.0687197860e-07 · Λ^{1} · ∇^{a}∇_{a}φ2 ] +
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
    "coeff_symbol": "\\gamma",
    "coeff_token": "COEFF_2",
    "candidate": "∇^{a}∇_{a}φ2",
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
  "max_relative_effect_to_EH": 1.7031116472485135e-12,
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
      "coefficient": "1000000000000.0",
      "lambda_power": -3,
      "sector": "non-minimal",
      "relative_effect_to_EH": 1.7031116472485135e-12,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0001/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0001/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0001/agent_solver_result/agent_solve/top_03_lagrangian_8_solution.csv`

## 18. wave_0001_lag_6  chi2=9434.007984

- scalar_config: `phi2_only`
- theory_track: `non_eh`
- potential_types: `{"phi1": null, "phi2": "quadratic"}`
- agent_parameter_sample_index: `29`
- H0_km_s_Mpc: `65.65968754`
- Omega_m0: `0.25348756`
- lambda_H_Lambda_over_H0: `3888.66159854`
- effective_correction_status: `unclear`
- max_relative_effect_to_EH: ``
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha Λ^{-4} · φ2 · φ2 · φ2 · φ2 · R )  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (-1.0000000000e+12) Λ^{-4} · φ2 · φ2 · φ2 · φ2 · R )  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · Λ^{-4} · φ2 · φ2 · φ2 · φ2 · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( -1.0000000000e+12 · Λ^{-4} · φ2 · φ2 · φ2 · φ2 · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Term Metadata

```json
[
  {
    "coeff_symbol": "\\alpha",
    "coeff_token": "COEFF_0",
    "candidate": "φ2 · φ2 · φ2 · φ2 · R",
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0001/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0001/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0001/agent_solver_result/agent_solve/top_04_lagrangian_6_solution.csv`

## 19. wave_0005_lag_12  chi2=9434.007984

- scalar_config: `phi2_only`
- theory_track: `non_eh`
- potential_types: `{"phi1": null, "phi2": "axion"}`
- agent_parameter_sample_index: `747`
- H0_km_s_Mpc: `69.67271303`
- Omega_m0: `0.32836353`
- lambda_H_Lambda_over_H0: `3577.33812231`
- effective_correction_status: `unclear`
- max_relative_effect_to_EH: ``
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha Λ^{-4} · R · R^{bcd}_{a} · R^{a}_{bcd}  +  \beta Λ^{-4} · ∇^{a}R · ∇_{a}R  +  \gamma Λ^{-2} · φ2 · φ2 · R  +  \delta Λ^{-3} · φ2 · φ2 · φ2 · R  +  \epsilon Λ^{-4} · φ2 · φ2 · φ2 · φ2 · R )  +  \zeta Λ^{-2} · φ2 · φ2 · φ2 · φ2 · φ2 · φ2  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (8.3786591331e+10) Λ^{-4} · R · R^{bcd}_{a} · R^{a}_{bcd}  +  (-6.4301486164e+11) Λ^{-4} · ∇^{a}R · ∇_{a}R  +  (-2.1066317594e+08) Λ^{-2} · φ2 · φ2 · R  +  (-1.0000000000e+12) Λ^{-3} · φ2 · φ2 · φ2 · R  +  (-1.0000000000e+12) Λ^{-4} · φ2 · φ2 · φ2 · φ2 · R )  +  (-1.3769553295e-07) Λ^{-2} · φ2 · φ2 · φ2 · φ2 · φ2 · φ2  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · Λ^{-4} · R · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · ∇^{a}R · ∇_{a}R ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-2} · φ2 · φ2 · R ) ] +
√(-g) [ M_p² ( \delta · Λ^{-3} · φ2 · φ2 · φ2 · R ) ] +
√(-g) [ M_p² ( \epsilon · Λ^{-4} · φ2 · φ2 · φ2 · φ2 · R ) ] +
√(-g) [ \zeta · Λ^{-2} · φ2 · φ2 · φ2 · φ2 · φ2 · φ2 ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 8.3786591331e+10 · Λ^{-4} · R · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( -6.4301486164e+11 · Λ^{-4} · ∇^{a}R · ∇_{a}R ) ] +
√(-g) [ M_p² ( -2.1066317594e+08 · Λ^{-2} · φ2 · φ2 · R ) ] +
√(-g) [ M_p² ( -1.0000000000e+12 · Λ^{-3} · φ2 · φ2 · φ2 · R ) ] +
√(-g) [ M_p² ( -1.0000000000e+12 · Λ^{-4} · φ2 · φ2 · φ2 · φ2 · R ) ] +
√(-g) [ -1.3769553295e-07 · Λ^{-2} · φ2 · φ2 · φ2 · φ2 · φ2 · φ2 ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Term Metadata

```json
[
  {
    "coeff_symbol": "\\alpha",
    "coeff_token": "COEFF_0",
    "candidate": "R · R^{bcd}_{a} · R^{a}_{bcd}",
    "mass_dim": 6,
    "lambda_power": -4,
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
    "candidate": "φ2 · φ2 · R",
    "mass_dim": 4,
    "lambda_power": -2,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\delta",
    "coeff_token": "COEFF_3",
    "candidate": "φ2 · φ2 · φ2 · R",
    "mass_dim": 5,
    "lambda_power": -3,
    "sector": "non-minimal"
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0005/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0005/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0005/agent_solver_result/agent_solve/top_06_lagrangian_12_solution.csv`

## 20. wave_0001_lag_5  chi2=9434.007984

- scalar_config: `phi2_only`
- theory_track: `non_eh`
- potential_types: `{"phi1": null, "phi2": "axion"}`
- agent_parameter_sample_index: `184`
- H0_km_s_Mpc: `64.39532763`
- Omega_m0: `0.32051978`
- lambda_H_Lambda_over_H0: `984.82987866`
- effective_correction_status: `unclear`
- max_relative_effect_to_EH: ``
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha Λ^{-3} · φ2 · φ2 · φ2 · R )  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (3.3938156249e+10) Λ^{-3} · φ2 · φ2 · φ2 · R )  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · Λ^{-3} · φ2 · φ2 · φ2 · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 3.3938156249e+10 · Λ^{-3} · φ2 · φ2 · φ2 · R ) ] +
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0001/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0001/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_208_split_v4_wave_0001/agent_solver_result/agent_solve/top_05_lagrangian_5_solution.csv`
