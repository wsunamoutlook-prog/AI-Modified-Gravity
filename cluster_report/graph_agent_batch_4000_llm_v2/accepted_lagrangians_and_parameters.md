# Accepted Lagrangians And Parameters

Each entry is the best chi-square representative of one accepted theory family.
The full accepted-attempt list is preserved in `accepted_summary.json`.
Each displayed entry uses the actual `agent_lagrangians.pkl` object that entered EOM -> Builder -> Solver.

## 1. wave_0003_lag_1  chi2=1640.486961

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: ``
- H0_km_s_Mpc: ``
- Omega_m0: ``
- lambda_H_Lambda_over_H0: ``
- effective_correction_status: `unclear`
- max_relative_effect_to_EH: ``
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · ∇^{a}φ1 · ∇_{a}φ1 · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · ∇^{a}φ1 · ∇_{a}φ1 · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
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
√(-g) [ M_p² ( R ) ] +
√(-g) [ M_p² ( Λ^{-4} · ∇^{a}φ1 · ∇_{a}φ1 · R ) ] +
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
  "effective_correction_status": "unclear",
  "effective_correction_reason": "missing lambda_H_Lambda_over_H0",
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_4000_llm_v2_wave_0003/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: ``
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_4000_llm_v2_wave_0003/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 2. wave_0028_lag_3  chi2=1643.599994

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "axion", "phi2": null}`
- agent_parameter_sample_index: ``
- H0_km_s_Mpc: ``
- Omega_m0: ``
- lambda_H_Lambda_over_H0: ``
- effective_correction_status: `unclear`
- max_relative_effect_to_EH: ``
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-2} · R^{ab} · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-2} · R^{ab} · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-2} · R^{ab} · R_{ab} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( R ) ] +
√(-g) [ M_p² ( Λ^{-2} · R^{ab} · R_{ab} ) ] +
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
  }
]
```

### Effective Correction Diagnostics

```json
{
  "effective_correction_status": "unclear",
  "effective_correction_reason": "missing lambda_H_Lambda_over_H0",
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_4000_llm_v2_wave_0028/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: ``
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_4000_llm_v2_wave_0028/agent_solver_result/agent_solve/top_01_lagrangian_3_solution.csv`

## 3. wave_0009_lag_3  chi2=1644.742241

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: ``
- H0_km_s_Mpc: ``
- Omega_m0: ``
- lambda_H_Lambda_over_H0: ``
- effective_correction_status: `unclear`
- max_relative_effect_to_EH: ``
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-2} · R · R  +  \gamma Λ^{-3} · φ1 · R · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-2} · R · R  +  \gamma Λ^{-3} · φ1 · R · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-2} · R · R ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-3} · φ1 · R · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( R ) ] +
√(-g) [ M_p² ( Λ^{-2} · R · R ) ] +
√(-g) [ M_p² ( Λ^{-3} · φ1 · R · R ) ] +
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
  "effective_correction_status": "unclear",
  "effective_correction_reason": "missing lambda_H_Lambda_over_H0",
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_4000_llm_v2_wave_0009/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: ``
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_4000_llm_v2_wave_0009/agent_solver_result/agent_solve/top_01_lagrangian_3_solution.csv`

## 4. wave_0013_lag_3  chi2=1646.339806

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: ``
- H0_km_s_Mpc: ``
- Omega_m0: ``
- lambda_H_Lambda_over_H0: ``
- effective_correction_status: `unclear`
- max_relative_effect_to_EH: ``
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-2} · R · R  +  \gamma Λ^{-2} · R^{ab} · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-2} · R · R  +  \gamma Λ^{-2} · R^{ab} · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-2} · R · R ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-2} · R^{ab} · R_{ab} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( R ) ] +
√(-g) [ M_p² ( Λ^{-2} · R · R ) ] +
√(-g) [ M_p² ( Λ^{-2} · R^{ab} · R_{ab} ) ] +
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
  "effective_correction_status": "unclear",
  "effective_correction_reason": "missing lambda_H_Lambda_over_H0",
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_4000_llm_v2_wave_0013/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: ``
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_4000_llm_v2_wave_0013/agent_solver_result/agent_solve/top_01_lagrangian_3_solution.csv`

## 5. wave_0034_lag_4  chi2=1649.908553

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "axion", "phi2": null}`
- agent_parameter_sample_index: ``
- H0_km_s_Mpc: ``
- Omega_m0: ``
- lambda_H_Lambda_over_H0: ``
- effective_correction_status: `unclear`
- max_relative_effect_to_EH: ``
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd}  +  \gamma Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{fdh} )  +  \delta Λ^{1} · ∇^{a}∇_{a}φ1  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd}  +  \gamma Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{fdh} )  +  \delta Λ^{1} · ∇^{a}∇_{a}φ1  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{fdh} ) ] +
√(-g) [ \delta · Λ^{1} · ∇^{a}∇_{a}φ1 ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( R ) ] +
√(-g) [ M_p² ( Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{fdh} ) ] +
√(-g) [ Λ^{1} · ∇^{a}∇_{a}φ1 ] +
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
    "candidate": "R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{fdh}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\delta",
    "coeff_token": "COEFF_3",
    "candidate": "∇^{a}∇_{a}φ1",
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
  "effective_correction_status": "unclear",
  "effective_correction_reason": "missing lambda_H_Lambda_over_H0",
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_4000_llm_v2_wave_0034/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: ``
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_4000_llm_v2_wave_0034/agent_solver_result/agent_solve/top_01_lagrangian_4_solution.csv`

## 6. wave_0031_lag_3  chi2=1651.746943

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: ``
- H0_km_s_Mpc: ``
- Omega_m0: ``
- lambda_H_Lambda_over_H0: ``
- effective_correction_status: `unclear`
- max_relative_effect_to_EH: ``
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · ∇^{a}R · ∇_{a}R )  +  \gamma Λ^{1} · ∇^{a}∇_{a}φ1  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · ∇^{a}R · ∇_{a}R )  +  \gamma Λ^{1} · ∇^{a}∇_{a}φ1  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · ∇^{a}R · ∇_{a}R ) ] +
√(-g) [ \gamma · Λ^{1} · ∇^{a}∇_{a}φ1 ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( R ) ] +
√(-g) [ M_p² ( Λ^{-4} · ∇^{a}R · ∇_{a}R ) ] +
√(-g) [ Λ^{1} · ∇^{a}∇_{a}φ1 ] +
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
    "candidate": "∇^{a}∇_{a}φ1",
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
  }
]
```

### Effective Correction Diagnostics

```json
{
  "effective_correction_status": "unclear",
  "effective_correction_reason": "missing lambda_H_Lambda_over_H0",
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_4000_llm_v2_wave_0031/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: ``
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_4000_llm_v2_wave_0031/agent_solver_result/agent_solve/top_01_lagrangian_3_solution.csv`

## 7. wave_0069_lag_1  chi2=1654.676501

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: ``
- H0_km_s_Mpc: ``
- Omega_m0: ``
- lambda_H_Lambda_over_H0: ``
- effective_correction_status: `unclear`
- max_relative_effect_to_EH: ``
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{fdh} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{fdh} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{fdh} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( R ) ] +
√(-g) [ M_p² ( Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{fdh} ) ] +
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
    "candidate": "R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{fdh}",
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
  "effective_correction_status": "unclear",
  "effective_correction_reason": "missing lambda_H_Lambda_over_H0",
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_4000_llm_v2_wave_0069/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: ``
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_4000_llm_v2_wave_0069/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 8. wave_0012_lag_4  chi2=1655.604545

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "axion", "phi2": null}`
- agent_parameter_sample_index: ``
- H0_km_s_Mpc: ``
- Omega_m0: ``
- lambda_H_Lambda_over_H0: ``
- effective_correction_status: `unclear`
- max_relative_effect_to_EH: ``
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd}  +  \gamma Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd}  +  \delta Λ^{-4} · φ1 · φ1 · ∇^{a}∇_{a}R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd}  +  \gamma Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd}  +  \delta Λ^{-4} · φ1 · φ1 · ∇^{a}∇_{a}R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( \delta · Λ^{-4} · φ1 · φ1 · ∇^{a}∇_{a}R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( R ) ] +
√(-g) [ M_p² ( Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( Λ^{-4} · φ1 · φ1 · ∇^{a}∇_{a}R ) ] +
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
    "candidate": "φ1 · φ1 · ∇^{a}∇_{a}R",
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
  "effective_correction_status": "unclear",
  "effective_correction_reason": "missing lambda_H_Lambda_over_H0",
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_4000_llm_v2_wave_0012/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: ``
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_4000_llm_v2_wave_0012/agent_solver_result/agent_solve/top_01_lagrangian_4_solution.csv`

## 9. wave_0053_lag_1  chi2=1664.49201

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "axion", "phi2": null}`
- agent_parameter_sample_index: ``
- H0_km_s_Mpc: ``
- Omega_m0: ``
- lambda_H_Lambda_over_H0: ``
- effective_correction_status: `unclear`
- max_relative_effect_to_EH: ``
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( R ) ] +
√(-g) [ M_p² ( Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf} ) ] +
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
  "effective_correction_status": "unclear",
  "effective_correction_reason": "missing lambda_H_Lambda_over_H0",
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_4000_llm_v2_wave_0053/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: ``
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_4000_llm_v2_wave_0053/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 10. wave_0010_lag_4  chi2=1670.029873

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "axion", "phi2": null}`
- agent_parameter_sample_index: ``
- H0_km_s_Mpc: ``
- Omega_m0: ``
- lambda_H_Lambda_over_H0: ``
- effective_correction_status: `unclear`
- max_relative_effect_to_EH: ``
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · φ1 · φ1 · R · R  +  \gamma Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · φ1 · φ1 · R · R  +  \gamma Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · φ1 · φ1 · R · R ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( R ) ] +
√(-g) [ M_p² ( Λ^{-4} · φ1 · φ1 · R · R ) ] +
√(-g) [ M_p² ( Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
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
    "candidate": "φ1 · φ1 · R · R",
    "mass_dim": 6,
    "lambda_power": -4,
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
  "effective_correction_status": "unclear",
  "effective_correction_reason": "missing lambda_H_Lambda_over_H0",
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_4000_llm_v2_wave_0010/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: ``
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_4000_llm_v2_wave_0010/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 11. wave_0044_lag_1  chi2=1671.846552

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "axion", "phi2": null}`
- agent_parameter_sample_index: ``
- H0_km_s_Mpc: ``
- Omega_m0: ``
- lambda_H_Lambda_over_H0: ``
- effective_correction_status: `unclear`
- max_relative_effect_to_EH: ``
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
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
√(-g) [ M_p² ( R ) ] +
√(-g) [ M_p² ( Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
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
  "effective_correction_status": "unclear",
  "effective_correction_reason": "missing lambda_H_Lambda_over_H0",
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_4000_llm_v2_wave_0044/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: ``
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_4000_llm_v2_wave_0044/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 12. wave_0003_lag_5  chi2=1681.728595

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: ``
- H0_km_s_Mpc: ``
- Omega_m0: ``
- lambda_H_Lambda_over_H0: ``
- effective_correction_status: `unclear`
- max_relative_effect_to_EH: ``
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-2} · R^{ab} · R_{ab}  +  \gamma Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd}  +  \delta Λ^{-3} · ∇^{a}φ1 · ∇_{a}R  +  \epsilon Λ^{-4} · φ1 · ∇^{a}∇_{a}φ1 · R )  +  \zeta Λ^{1} · ∇^{a}∇_{a}φ1  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-2} · R^{ab} · R_{ab}  +  \gamma Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd}  +  \delta Λ^{-3} · ∇^{a}φ1 · ∇_{a}R  +  \epsilon Λ^{-4} · φ1 · ∇^{a}∇_{a}φ1 · R )  +  \zeta Λ^{1} · ∇^{a}∇_{a}φ1  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-2} · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( \delta · Λ^{-3} · ∇^{a}φ1 · ∇_{a}R ) ] +
√(-g) [ M_p² ( \epsilon · Λ^{-4} · φ1 · ∇^{a}∇_{a}φ1 · R ) ] +
√(-g) [ \zeta · Λ^{1} · ∇^{a}∇_{a}φ1 ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( R ) ] +
√(-g) [ M_p² ( Λ^{-2} · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( Λ^{-3} · ∇^{a}φ1 · ∇_{a}R ) ] +
√(-g) [ M_p² ( Λ^{-4} · φ1 · ∇^{a}∇_{a}φ1 · R ) ] +
√(-g) [ Λ^{1} · ∇^{a}∇_{a}φ1 ] +
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
    "candidate": "∇^{a}φ1 · ∇_{a}R",
    "mass_dim": 5,
    "lambda_power": -3,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\epsilon",
    "coeff_token": "COEFF_4",
    "candidate": "φ1 · ∇^{a}∇_{a}φ1 · R",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\zeta",
    "coeff_token": "COEFF_5",
    "candidate": "∇^{a}∇_{a}φ1",
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
  }
]
```

### Effective Correction Diagnostics

```json
{
  "effective_correction_status": "unclear",
  "effective_correction_reason": "missing lambda_H_Lambda_over_H0",
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_4000_llm_v2_wave_0003/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: ``
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_4000_llm_v2_wave_0003/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 13. wave_0011_lag_6  chi2=1685.921976

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "axion", "phi2": null}`
- agent_parameter_sample_index: ``
- H0_km_s_Mpc: ``
- Omega_m0: ``
- lambda_H_Lambda_over_H0: ``
- effective_correction_status: `unclear`
- max_relative_effect_to_EH: ``
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · R · R · R  +  \gamma Λ^{-3} · ∇^{a}∇_{a}φ1 · R  +  \delta Λ^{-3} · ∇^{a}∇^{b}φ1 · R_{ab}  +  \epsilon Λ^{-4} · φ1 · ∇^{a}∇_{a}φ1 · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · R · R · R  +  \gamma Λ^{-3} · ∇^{a}∇_{a}φ1 · R  +  \delta Λ^{-3} · ∇^{a}∇^{b}φ1 · R_{ab}  +  \epsilon Λ^{-4} · φ1 · ∇^{a}∇_{a}φ1 · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · R · R · R ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-3} · ∇^{a}∇_{a}φ1 · R ) ] +
√(-g) [ M_p² ( \delta · Λ^{-3} · ∇^{a}∇^{b}φ1 · R_{ab} ) ] +
√(-g) [ M_p² ( \epsilon · Λ^{-4} · φ1 · ∇^{a}∇_{a}φ1 · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( R ) ] +
√(-g) [ M_p² ( Λ^{-4} · R · R · R ) ] +
√(-g) [ M_p² ( Λ^{-3} · ∇^{a}∇_{a}φ1 · R ) ] +
√(-g) [ M_p² ( Λ^{-3} · ∇^{a}∇^{b}φ1 · R_{ab} ) ] +
√(-g) [ M_p² ( Λ^{-4} · φ1 · ∇^{a}∇_{a}φ1 · R ) ] +
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
    "candidate": "∇^{a}∇_{a}φ1 · R",
    "mass_dim": 5,
    "lambda_power": -3,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\delta",
    "coeff_token": "COEFF_3",
    "candidate": "∇^{a}∇^{b}φ1 · R_{ab}",
    "mass_dim": 5,
    "lambda_power": -3,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\epsilon",
    "coeff_token": "COEFF_4",
    "candidate": "φ1 · ∇^{a}∇_{a}φ1 · R",
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
  "effective_correction_status": "unclear",
  "effective_correction_reason": "missing lambda_H_Lambda_over_H0",
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_4000_llm_v2_wave_0011/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: ``
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_4000_llm_v2_wave_0011/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 14. wave_0040_lag_2  chi2=1691.807219

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: ``
- H0_km_s_Mpc: ``
- Omega_m0: ``
- lambda_H_Lambda_over_H0: ``
- effective_correction_status: `unclear`
- max_relative_effect_to_EH: ``
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-2} · R · R  +  \gamma Λ^{-4} · ∇^{a}R · ∇_{a}R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-2} · R · R  +  \gamma Λ^{-4} · ∇^{a}R · ∇_{a}R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-2} · R · R ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · ∇^{a}R · ∇_{a}R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( R ) ] +
√(-g) [ M_p² ( Λ^{-2} · R · R ) ] +
√(-g) [ M_p² ( Λ^{-4} · ∇^{a}R · ∇_{a}R ) ] +
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
    "candidate": "∇^{a}R · ∇_{a}R",
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
  "effective_correction_status": "unclear",
  "effective_correction_reason": "missing lambda_H_Lambda_over_H0",
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_4000_llm_v2_wave_0040/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: ``
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_4000_llm_v2_wave_0040/agent_solver_result/agent_solve/top_01_lagrangian_4_solution.csv`

## 15. wave_0083_lag_3  chi2=1713.438612

- scalar_config: `both`
- potential_types: `{"phi1": "axion", "phi2": "quadratic"}`
- agent_parameter_sample_index: ``
- H0_km_s_Mpc: ``
- Omega_m0: ``
- lambda_H_Lambda_over_H0: ``
- effective_correction_status: `unclear`
- max_relative_effect_to_EH: ``
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R )  +  \beta Λ^{1} · ∇^{a}∇_{a}φ1  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( \alpha · R )  +  \beta Λ^{1} · ∇^{a}∇_{a}φ1  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ \beta · Λ^{1} · ∇^{a}∇_{a}φ1 ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( R ) ] +
√(-g) [ Λ^{1} · ∇^{a}∇_{a}φ1 ] +
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
    "candidate": "∇^{a}∇_{a}φ1",
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
  "effective_correction_reason": "missing lambda_H_Lambda_over_H0",
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_4000_llm_v2_wave_0083/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: ``
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_4000_llm_v2_wave_0083/agent_solver_result/agent_solve/top_01_lagrangian_3_solution.csv`

## 16. wave_0024_lag_1  chi2=1714.208637

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: ``
- H0_km_s_Mpc: ``
- Omega_m0: ``
- lambda_H_Lambda_over_H0: ``
- effective_correction_status: `unclear`
- max_relative_effect_to_EH: ``
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( R ) ] +
√(-g) [ M_p² ( Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
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
  "effective_correction_status": "unclear",
  "effective_correction_reason": "missing lambda_H_Lambda_over_H0",
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_4000_llm_v2_wave_0024/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: ``
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_4000_llm_v2_wave_0024/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 17. wave_0051_lag_6  chi2=1729.649158

- scalar_config: `both`
- potential_types: `{"phi1": "quadratic", "phi2": "quadratic"}`
- agent_parameter_sample_index: ``
- H0_km_s_Mpc: ``
- Omega_m0: ``
- lambda_H_Lambda_over_H0: ``
- effective_correction_status: `unclear`
- max_relative_effect_to_EH: ``
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · ∇^{a}R · ∇_{a}R  +  \gamma Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd}  +  \delta Λ^{-3} · ∇^{a}∇^{b}φ1 · R_{ab}  +  \epsilon Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd}  +  \zeta Λ^{-4} · φ1 · φ2 · R^{ab} · R_{ab}  +  \eta Λ^{-4} · ∇^{a}φ2 · ∇_{a}φ2 · R  +  \theta Λ^{-4} · ∇^{a}φ1 · ∇^{b}φ1 · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · ∇^{a}R · ∇_{a}R  +  \gamma Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd}  +  \delta Λ^{-3} · ∇^{a}∇^{b}φ1 · R_{ab}  +  \epsilon Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd}  +  \zeta Λ^{-4} · φ1 · φ2 · R^{ab} · R_{ab}  +  \eta Λ^{-4} · ∇^{a}φ2 · ∇_{a}φ2 · R  +  \theta Λ^{-4} · ∇^{a}φ1 · ∇^{b}φ1 · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · ∇^{a}R · ∇_{a}R ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( \delta · Λ^{-3} · ∇^{a}∇^{b}φ1 · R_{ab} ) ] +
√(-g) [ M_p² ( \epsilon · Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( \zeta · Λ^{-4} · φ1 · φ2 · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( \eta · Λ^{-4} · ∇^{a}φ2 · ∇_{a}φ2 · R ) ] +
√(-g) [ M_p² ( \theta · Λ^{-4} · ∇^{a}φ1 · ∇^{b}φ1 · R_{ab} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( R ) ] +
√(-g) [ M_p² ( Λ^{-4} · ∇^{a}R · ∇_{a}R ) ] +
√(-g) [ M_p² ( Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( Λ^{-3} · ∇^{a}∇^{b}φ1 · R_{ab} ) ] +
√(-g) [ M_p² ( Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( Λ^{-4} · φ1 · φ2 · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( Λ^{-4} · ∇^{a}φ2 · ∇_{a}φ2 · R ) ] +
√(-g) [ M_p² ( Λ^{-4} · ∇^{a}φ1 · ∇^{b}φ1 · R_{ab} ) ] +
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
    "candidate": "∇^{a}R · ∇_{a}R",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\gamma",
    "coeff_token": "COEFF_2",
    "candidate": "φ1 · R^{bcd}_{a} · R^{a}_{bcd}",
    "mass_dim": 5,
    "lambda_power": -3,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\delta",
    "coeff_token": "COEFF_3",
    "candidate": "∇^{a}∇^{b}φ1 · R_{ab}",
    "mass_dim": 5,
    "lambda_power": -3,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\epsilon",
    "coeff_token": "COEFF_4",
    "candidate": "φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\zeta",
    "coeff_token": "COEFF_5",
    "candidate": "φ1 · φ2 · R^{ab} · R_{ab}",
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
  "effective_correction_reason": "missing lambda_H_Lambda_over_H0",
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_4000_llm_v2_wave_0051/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: ``
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_4000_llm_v2_wave_0051/agent_solver_result/agent_solve/top_01_lagrangian_6_solution.csv`
