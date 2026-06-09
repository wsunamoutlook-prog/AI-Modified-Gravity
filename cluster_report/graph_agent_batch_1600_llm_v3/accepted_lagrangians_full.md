# Accepted Lagrangians Full

Complete dimension-balanced Lagrangians, best-fit coefficient substitutions, metadata, and Solver paths.
Only the best chi-square representative from each accepted theory family is shown for human inspection.
The full accepted-attempt list is preserved in `accepted_summary.json`.

## 1. wave_0029_lag_2  chi2=1637.96608

- scalar_config: `both`
- potential_types: `{"phi1": "axion", "phi2": "axion"}`
- agent_parameter_sample_index: `366`
- H0_km_s_Mpc: `65.59877902`
- Omega_m0: `0.27269376`
- lambda_H_Lambda_over_H0: `3916.60348032`
- effective_correction_status: `moderate`
- max_relative_effect_to_EH: `4.47141253e-04`
- dominant_correction_term: `∇^{c}R^{ab} · ∇_{c}R_{ab}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · ∇^{c}R^{ab} · ∇_{c}R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (5.2608166472e+10) Λ^{-4} · ∇^{c}R^{ab} · ∇_{c}R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · ∇^{c}R^{ab} · ∇_{c}R_{ab} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 5.2608166472e+10 · Λ^{-4} · ∇^{c}R^{ab} · ∇_{c}R_{ab} ) ] +
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
    "candidate": "∇^{c}R^{ab} · ∇_{c}R_{ab}",
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
  "effective_correction_status": "moderate",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 0.00044714125299953253,
  "dominant_correction_term": "∇^{c}R^{ab} · ∇_{c}R_{ab}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 1,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 0,
  "correction_term_count": 1,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "∇^{c}R^{ab} · ∇_{c}R_{ab}",
      "coeff_symbol": "\\beta",
      "coefficient": "52608166472.03281",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 0.00044714125299953253,
      "effect_class": "moderate"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0029/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0029/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0029/agent_solver_result/agent_solve/top_01_lagrangian_2_solution.csv`

## 2. wave_0033_lag_1  chi2=1638.020982

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "axion", "phi2": null}`
- agent_parameter_sample_index: `186`
- H0_km_s_Mpc: `68.40156332`
- Omega_m0: `0.27457736`
- lambda_H_Lambda_over_H0: `8151.2822964`
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0033/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0033/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0033/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 3. wave_0041_lag_2  chi2=1638.034487

- scalar_config: `both`
- potential_types: `{"phi1": "quadratic", "phi2": "axion"}`
- agent_parameter_sample_index: `603`
- H0_km_s_Mpc: `71.17485845`
- Omega_m0: `0.26529768`
- lambda_H_Lambda_over_H0: `5048.99016037`
- effective_correction_status: `weak`
- max_relative_effect_to_EH: `3.52445294e-06`
- dominant_correction_term: `∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · ∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (1.1451959865e+09) Λ^{-4} · ∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · ∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 1.1451959865e+09 · Λ^{-4} · ∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd} ) ] +
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
    "candidate": "∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}",
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
  "max_relative_effect_to_EH": 3.5244529367040723e-06,
  "dominant_correction_term": "∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 1,
  "tiny_correction_terms": 0,
  "correction_term_count": 1,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}",
      "coeff_symbol": "\\beta",
      "coefficient": "1145195986.5008905",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 3.5244529367040723e-06,
      "effect_class": "weak"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0041/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0041/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0041/agent_solver_result/agent_solve/top_01_lagrangian_2_solution.csv`

## 4. wave_0035_lag_5  chi2=1638.038172

- scalar_config: `both`
- potential_types: `{"phi1": "axion", "phi2": "quadratic"}`
- agent_parameter_sample_index: `572`
- H0_km_s_Mpc: `57.77583563`
- Omega_m0: `0.28158661`
- lambda_H_Lambda_over_H0: `5865.96143323`
- effective_correction_status: `weak`
- max_relative_effect_to_EH: `2.45452511e-06`
- dominant_correction_term: `∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · ∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (1.4530959678e+09) Λ^{-4} · ∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · ∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 1.4530959678e+09 · Λ^{-4} · ∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd} ) ] +
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
    "candidate": "∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}",
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
  "effective_correction_status": "weak",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 2.4545251141591005e-06,
  "dominant_correction_term": "∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 1,
  "tiny_correction_terms": 0,
  "correction_term_count": 1,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}",
      "coeff_symbol": "\\beta",
      "coefficient": "1453095967.774085",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 2.4545251141591005e-06,
      "effect_class": "weak"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0035/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0035/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0035/agent_solver_result/agent_solve/top_01_lagrangian_5_solution.csv`

## 5. wave_0031_lag_4  chi2=1638.040974

- scalar_config: `both`
- potential_types: `{"phi1": "quadratic", "phi2": "quadratic"}`
- agent_parameter_sample_index: `914`
- H0_km_s_Mpc: `69.93414808`
- Omega_m0: `0.30156543`
- lambda_H_Lambda_over_H0: `7831.59006636`
- effective_correction_status: `weak`
- max_relative_effect_to_EH: `1.26677913e-06`
- dominant_correction_term: `φ1 · φ1 · R · R`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · φ1 · φ1 · R · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-7.1517181038e+08) Λ^{-4} · φ1 · φ1 · R · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · φ1 · φ1 · R · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -7.1517181038e+08 · Λ^{-4} · φ1 · φ1 · R · R ) ] +
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
  "max_relative_effect_to_EH": 1.2667791266171632e-06,
  "dominant_correction_term": "φ1 · φ1 · R · R",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 1,
  "tiny_correction_terms": 0,
  "correction_term_count": 1,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "φ1 · φ1 · R · R",
      "coeff_symbol": "\\beta",
      "coefficient": "-715171810.377449",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 1.2667791266171632e-06,
      "effect_class": "weak"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0031/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0031/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0031/agent_solver_result/agent_solve/top_01_lagrangian_4_solution.csv`

## 6. wave_0107_lag_8  chi2=1638.055644

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: `581`
- H0_km_s_Mpc: `69.74528054`
- Omega_m0: `0.26623688`
- lambda_H_Lambda_over_H0: `6894.13756354`
- effective_correction_status: `weak`
- max_relative_effect_to_EH: `8.21884328e-05`
- dominant_correction_term: `φ1 · ∇^{a}∇^{b}φ1 · R_{ab}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-2} · R^{ab} · R_{ab}  +  \gamma Λ^{-4} · R^{ab} · R^{d}_{a} · R_{bd}  +  \delta Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def}  +  \epsilon Λ^{-4} · ∇^{c}R^{ab} · ∇_{c}R_{ab}  +  \zeta Λ^{-4} · φ1 · φ1 · R^{ab} · R_{ab}  +  \eta Λ^{-4} · φ1 · ∇^{a}∇^{b}φ1 · R_{ab}  +  \theta Λ^{-4} · ∇^{a}φ1 · ∇^{b}φ1 · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (0.9040919371) Λ^{-2} · R^{ab} · R_{ab}  +  (1.3740406486e+09) Λ^{-4} · R^{ab} · R^{d}_{a} · R_{bd}  +  (21.4042705621) Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def}  +  (-5.1612314145e+09) Λ^{-4} · ∇^{c}R^{ab} · ∇_{c}R_{ab}  +  (2.1437073464e+08) Λ^{-4} · φ1 · φ1 · R^{ab} · R_{ab}  +  (2.6424778379e+10) Λ^{-4} · φ1 · ∇^{a}∇^{b}φ1 · R_{ab}  +  (5.8721571215) Λ^{-4} · ∇^{a}φ1 · ∇^{b}φ1 · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-2} · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · R^{ab} · R^{d}_{a} · R_{bd} ) ] +
√(-g) [ M_p² ( \delta · Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def} ) ] +
√(-g) [ M_p² ( \epsilon · Λ^{-4} · ∇^{c}R^{ab} · ∇_{c}R_{ab} ) ] +
√(-g) [ M_p² ( \zeta · Λ^{-4} · φ1 · φ1 · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( \eta · Λ^{-4} · φ1 · ∇^{a}∇^{b}φ1 · R_{ab} ) ] +
√(-g) [ M_p² ( \theta · Λ^{-4} · ∇^{a}φ1 · ∇^{b}φ1 · R_{ab} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 0.9040919371 · Λ^{-2} · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( 1.3740406486e+09 · Λ^{-4} · R^{ab} · R^{d}_{a} · R_{bd} ) ] +
√(-g) [ M_p² ( 21.4042705621 · Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def} ) ] +
√(-g) [ M_p² ( -5.1612314145e+09 · Λ^{-4} · ∇^{c}R^{ab} · ∇_{c}R_{ab} ) ] +
√(-g) [ M_p² ( 2.1437073464e+08 · Λ^{-4} · φ1 · φ1 · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( 2.6424778379e+10 · Λ^{-4} · φ1 · ∇^{a}∇^{b}φ1 · R_{ab} ) ] +
√(-g) [ M_p² ( 5.8721571215 · Λ^{-4} · ∇^{a}φ1 · ∇^{b}φ1 · R_{ab} ) ] +
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
    "candidate": "R^{ab} · R^{d}_{a} · R_{bd}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\delta",
    "coeff_token": "COEFF_3",
    "candidate": "R_{ab} · R^{adef} · R^{b}_{def}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\epsilon",
    "coeff_token": "COEFF_4",
    "candidate": "∇^{c}R^{ab} · ∇_{c}R_{ab}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\zeta",
    "coeff_token": "COEFF_5",
    "candidate": "φ1 · φ1 · R^{ab} · R_{ab}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\eta",
    "coeff_token": "COEFF_6",
    "candidate": "φ1 · ∇^{a}∇^{b}φ1 · R_{ab}",
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
  }
]
```

### Effective Correction Diagnostics

```json
{
  "effective_correction_status": "weak",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 8.21884328221914e-05,
  "dominant_correction_term": "φ1 · ∇^{a}∇^{b}φ1 · R_{ab}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 3,
  "tiny_correction_terms": 4,
  "correction_term_count": 7,
  "tiny_correction_fraction": 0.5714285714285714,
  "term_effects": [
    {
      "candidate": "R^{ab} · R_{ab}",
      "coeff_symbol": "\\beta",
      "coefficient": "0.9040919370890026",
      "lambda_power": -2,
      "sector": "gravity",
      "relative_effect_to_EH": 3.804369593440269e-08,
      "effect_class": "tiny"
    },
    {
      "candidate": "R^{ab} · R^{d}_{a} · R_{bd}",
      "coeff_symbol": "\\gamma",
      "coefficient": "1374040648.6061563",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 1.2164935110031607e-06,
      "effect_class": "weak"
    },
    {
      "candidate": "R_{ab} · R^{adef} · R^{b}_{def}",
      "coeff_symbol": "\\delta",
      "coefficient": "21.40427056206571",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 1.895006255668079e-14,
      "effect_class": "tiny"
    },
    {
      "candidate": "∇^{c}R^{ab} · ∇_{c}R_{ab}",
      "coeff_symbol": "\\epsilon",
      "coefficient": "-5161231414.487185",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 4.569445984642752e-06,
      "effect_class": "weak"
    },
    {
      "candidate": "φ1 · φ1 · R^{ab} · R_{ab}",
      "coeff_symbol": "\\zeta",
      "coefficient": "214370734.64418468",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 6.667527905239641e-07,
      "effect_class": "tiny"
    },
    {
      "candidate": "φ1 · ∇^{a}∇^{b}φ1 · R_{ab}",
      "coeff_symbol": "\\eta",
      "coefficient": "26424778379.257713",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 8.21884328221914e-05,
      "effect_class": "weak"
    },
    {
      "candidate": "∇^{a}φ1 · ∇^{b}φ1 · R_{ab}",
      "coeff_symbol": "\\theta",
      "coefficient": "5.872157121491908",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 1.8264046879573024e-14,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0107/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0107/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0107/agent_solver_result/agent_solve/top_01_lagrangian_8_solution.csv`

## 7. wave_0101_lag_4  chi2=1638.057556

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: `419`
- H0_km_s_Mpc: `70.11116696`
- Omega_m0: `0.26533274`
- lambda_H_Lambda_over_H0: `7404.91292658`
- effective_correction_status: `weak`
- max_relative_effect_to_EH: `3.39008875e-06`
- dominant_correction_term: `R^{ab} · R^{d}_{a} · R_{bd}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · R^{ab} · R^{d}_{a} · R_{bd}  +  \gamma Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-5.0963693726e+09) Λ^{-4} · R^{ab} · R^{d}_{a} · R_{bd}  +  (-1.9774456164e+05) Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · R^{ab} · R^{d}_{a} · R_{bd} ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -5.0963693726e+09 · Λ^{-4} · R^{ab} · R^{d}_{a} · R_{bd} ) ] +
√(-g) [ M_p² ( -1.9774456164e+05 · Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
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
    "coeff_symbol": "\\gamma",
    "coeff_token": "COEFF_2",
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
  "max_relative_effect_to_EH": 3.3900887546579447e-06,
  "dominant_correction_term": "R^{ab} · R^{d}_{a} · R_{bd}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 2,
  "tiny_correction_terms": 0,
  "correction_term_count": 2,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "R^{ab} · R^{d}_{a} · R_{bd}",
      "coeff_symbol": "\\beta",
      "coefficient": "-5096369372.599835",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 3.3900887546579447e-06,
      "effect_class": "weak"
    },
    {
      "candidate": "φ1 · R^{bcd}_{a} · R^{a}_{bcd}",
      "coeff_symbol": "\\gamma",
      "coefficient": "-197744.56164436773",
      "lambda_power": -3,
      "sector": "non-minimal",
      "relative_effect_to_EH": 1.8238034511968135e-06,
      "effect_class": "weak"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0101/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0101/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0101/agent_solver_result/agent_solve/top_01_lagrangian_4_solution.csv`

## 8. wave_0077_lag_4  chi2=1638.062671

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: `929`
- H0_km_s_Mpc: `61.8549824`
- Omega_m0: `0.26441108`
- lambda_H_Lambda_over_H0: `7050.4718318`
- effective_correction_status: `weak`
- max_relative_effect_to_EH: `2.79834577e-05`
- dominant_correction_term: `φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-9.8804653710e+09) Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
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
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -9.8804653710e+09 · Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
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
  "effective_correction_status": "weak",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 2.7983457689014932e-05,
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
      "coefficient": "-9880465371.03515",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 2.7983457689014932e-05,
      "effect_class": "weak"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0077/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0077/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0077/agent_solver_result/agent_solve/top_01_lagrangian_4_solution.csv`

## 9. wave_0064_lag_4  chi2=1638.07453

- scalar_config: `both`
- potential_types: `{"phi1": "axion", "phi2": "axion"}`
- agent_parameter_sample_index: `821`
- H0_km_s_Mpc: `64.55059446`
- Omega_m0: `0.28217703`
- lambda_H_Lambda_over_H0: `7036.27572716`
- effective_correction_status: `eh_dominated`
- max_relative_effect_to_EH: `2.76804023e-14`
- dominant_correction_term: `R^{ab} · R^{d}_{a} · R_{bd}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · R^{ab} · R^{d}_{a} · R_{bd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (33.9245269178) Λ^{-4} · R^{ab} · R^{d}_{a} · R_{bd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · R^{ab} · R^{d}_{a} · R_{bd} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 33.9245269178 · Λ^{-4} · R^{ab} · R^{d}_{a} · R_{bd} ) ] +
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
  "max_relative_effect_to_EH": 2.7680402271484207e-14,
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
      "coefficient": "33.92452691783945",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 2.7680402271484207e-14,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0064/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0064/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0064/agent_solver_result/agent_solve/top_01_lagrangian_4_solution.csv`

## 10. wave_0052_lag_2  chi2=1638.074679

- scalar_config: `both`
- potential_types: `{"phi1": "quadratic", "phi2": "quadratic"}`
- agent_parameter_sample_index: `502`
- H0_km_s_Mpc: `61.68152339`
- Omega_m0: `0.265842`
- lambda_H_Lambda_over_H0: `6740.41921276`
- effective_correction_status: `weak`
- max_relative_effect_to_EH: `3.80717824e-05`
- dominant_correction_term: `∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · ∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-3.9293511846e+10) Λ^{-4} · ∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · ∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -3.9293511846e+10 · Λ^{-4} · ∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd} ) ] +
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
    "candidate": "∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}",
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
  "effective_correction_status": "weak",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 3.807178242259334e-05,
  "dominant_correction_term": "∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 1,
  "tiny_correction_terms": 0,
  "correction_term_count": 1,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}",
      "coeff_symbol": "\\beta",
      "coefficient": "-39293511846.4998",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 3.807178242259334e-05,
      "effect_class": "weak"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0052/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0052/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0052/agent_solver_result/agent_solve/top_01_lagrangian_2_solution.csv`

## 11. wave_0056_lag_8  chi2=1638.074751

- scalar_config: `both`
- potential_types: `{"phi1": "quadratic", "phi2": "axion"}`
- agent_parameter_sample_index: `191`
- H0_km_s_Mpc: `67.90537139`
- Omega_m0: `0.26541569`
- lambda_H_Lambda_over_H0: `6270.26008445`
- effective_correction_status: `moderate`
- max_relative_effect_to_EH: `3.02439637e-04`
- dominant_correction_term: `φ1 · φ1 · ∇^{a}∇_{a}R`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · R · R^{ab} · R_{ab}  +  \gamma Λ^{-4} · ∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}  +  \delta Λ^{-3} · φ2 · ∇^{a}∇_{a}R  +  \epsilon Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd}  +  \zeta Λ^{-4} · φ1 · φ1 · ∇^{a}∇_{a}R  +  \eta Λ^{-4} · φ1 · ∇^{a}∇^{b}φ2 · R_{ab}  +  \theta Λ^{-4} · ∇^{a}φ2 · ∇^{b}φ2 · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (4.7107764347e+06) Λ^{-4} · R · R^{ab} · R_{ab}  +  (-83.1080755712) Λ^{-4} · ∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}  +  (1216.1994239056) Λ^{-3} · φ2 · ∇^{a}∇_{a}R  +  (-1.1163168570e+09) Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd}  +  (6.6320751197e+10) Λ^{-4} · φ1 · φ1 · ∇^{a}∇_{a}R  +  (8.5486383479e+04) Λ^{-4} · φ1 · ∇^{a}∇^{b}φ2 · R_{ab}  +  (4.7222337836e+05) Λ^{-4} · ∇^{a}φ2 · ∇^{b}φ2 · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · R · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · ∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( \delta · Λ^{-3} · φ2 · ∇^{a}∇_{a}R ) ] +
√(-g) [ M_p² ( \epsilon · Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( \zeta · Λ^{-4} · φ1 · φ1 · ∇^{a}∇_{a}R ) ] +
√(-g) [ M_p² ( \eta · Λ^{-4} · φ1 · ∇^{a}∇^{b}φ2 · R_{ab} ) ] +
√(-g) [ M_p² ( \theta · Λ^{-4} · ∇^{a}φ2 · ∇^{b}φ2 · R_{ab} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 4.7107764347e+06 · Λ^{-4} · R · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( -83.1080755712 · Λ^{-4} · ∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( 1216.1994239056 · Λ^{-3} · φ2 · ∇^{a}∇_{a}R ) ] +
√(-g) [ M_p² ( -1.1163168570e+09 · Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( 6.6320751197e+10 · Λ^{-4} · φ1 · φ1 · ∇^{a}∇_{a}R ) ] +
√(-g) [ M_p² ( 8.5486383479e+04 · Λ^{-4} · φ1 · ∇^{a}∇^{b}φ2 · R_{ab} ) ] +
√(-g) [ M_p² ( 4.7222337836e+05 · Λ^{-4} · ∇^{a}φ2 · ∇^{b}φ2 · R_{ab} ) ] +
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
    "candidate": "R · R^{ab} · R_{ab}",
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
    "candidate": "φ2 · ∇^{a}∇_{a}R",
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
    "candidate": "φ1 · φ1 · ∇^{a}∇_{a}R",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\eta",
    "coeff_token": "COEFF_6",
    "candidate": "φ1 · ∇^{a}∇^{b}φ2 · R_{ab}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\theta",
    "coeff_token": "COEFF_7",
    "candidate": "∇^{a}φ2 · ∇^{b}φ2 · R_{ab}",
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
  "max_relative_effect_to_EH": 0.00030243963669353995,
  "dominant_correction_term": "φ1 · φ1 · ∇^{a}∇_{a}R",
  "active_correction_terms": 0,
  "moderate_correction_terms": 1,
  "weak_correction_terms": 1,
  "tiny_correction_terms": 5,
  "correction_term_count": 7,
  "tiny_correction_fraction": 0.7142857142857143,
  "term_effects": [
    {
      "candidate": "R · R^{ab} · R_{ab}",
      "coeff_symbol": "\\beta",
      "coefficient": "4710776.434688062",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 6.095092040992595e-09,
      "effect_class": "tiny"
    },
    {
      "candidate": "∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}",
      "coeff_symbol": "\\gamma",
      "coefficient": "-83.10807557119526",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 1.0753033538721651e-13,
      "effect_class": "tiny"
    },
    {
      "candidate": "φ2 · ∇^{a}∇_{a}R",
      "coeff_symbol": "\\delta",
      "coefficient": "1216.1994239056269",
      "lambda_power": -3,
      "sector": "non-minimal",
      "relative_effect_to_EH": 1.0227056817287747e-09,
      "effect_class": "tiny"
    },
    {
      "candidate": "φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd}",
      "coeff_symbol": "\\epsilon",
      "coefficient": "-1116316857.0316627",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 5.090691202734124e-06,
      "effect_class": "weak"
    },
    {
      "candidate": "φ1 · φ1 · ∇^{a}∇_{a}R",
      "coeff_symbol": "\\zeta",
      "coefficient": "66320751196.65504",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 0.00030243963669353995,
      "effect_class": "moderate"
    },
    {
      "candidate": "φ1 · ∇^{a}∇^{b}φ2 · R_{ab}",
      "coeff_symbol": "\\eta",
      "coefficient": "85486.38347882066",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 2.1523258062964608e-11,
      "effect_class": "tiny"
    },
    {
      "candidate": "∇^{a}φ2 · ∇^{b}φ2 · R_{ab}",
      "coeff_symbol": "\\theta",
      "coefficient": "472223.3783578808",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 6.564178005180961e-12,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0056/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0056/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0056/agent_solver_result/agent_solve/top_01_lagrangian_8_solution.csv`

## 12. wave_0095_lag_1  chi2=1638.075674

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: `412`
- H0_km_s_Mpc: `64.02088978`
- Omega_m0: `0.26541326`
- lambda_H_Lambda_over_H0: `7484.67805312`
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0095/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0095/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0095/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 13. wave_0095_lag_8  chi2=1638.07644

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: `461`
- H0_km_s_Mpc: `60.10767991`
- Omega_m0: `0.26684872`
- lambda_H_Lambda_over_H0: `7610.29791166`
- effective_correction_status: `weak`
- max_relative_effect_to_EH: `6.44598310e-06`
- dominant_correction_term: `∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · R · R · R  +  \gamma Λ^{-4} · R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh}  +  \delta Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{fdh}  +  \epsilon Λ^{-4} · ∇^{c}R^{ab} · ∇_{c}R_{ab}  +  \zeta Λ^{-4} · ∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (184.4771399407) Λ^{-4} · R · R · R  +  (299.8035342667) Λ^{-4} · R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh}  +  (231.4034643905) Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{fdh}  +  (7.2585553045e+04) Λ^{-4} · ∇^{c}R^{ab} · ∇_{c}R_{ab}  +  (1.0810998287e+10) Λ^{-4} · ∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · R · R · R ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh} ) ] +
√(-g) [ M_p² ( \delta · Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{fdh} ) ] +
√(-g) [ M_p² ( \epsilon · Λ^{-4} · ∇^{c}R^{ab} · ∇_{c}R_{ab} ) ] +
√(-g) [ M_p² ( \zeta · Λ^{-4} · ∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 184.4771399407 · Λ^{-4} · R · R · R ) ] +
√(-g) [ M_p² ( 299.8035342667 · Λ^{-4} · R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh} ) ] +
√(-g) [ M_p² ( 231.4034643905 · Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{fdh} ) ] +
√(-g) [ M_p² ( 7.2585553045e+04 · Λ^{-4} · ∇^{c}R^{ab} · ∇_{c}R_{ab} ) ] +
√(-g) [ M_p² ( 1.0810998287e+10 · Λ^{-4} · ∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd} ) ] +
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
    "candidate": "R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{fdh}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\epsilon",
    "coeff_token": "COEFF_4",
    "candidate": "∇^{c}R^{ab} · ∇_{c}R_{ab}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\zeta",
    "coeff_token": "COEFF_5",
    "candidate": "∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}",
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
  "max_relative_effect_to_EH": 6.44598309860126e-06,
  "dominant_correction_term": "∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 1,
  "tiny_correction_terms": 4,
  "correction_term_count": 5,
  "tiny_correction_fraction": 0.8,
  "term_effects": [
    {
      "candidate": "R · R · R",
      "coeff_symbol": "\\beta",
      "coefficient": "184.47713994070367",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 1.0999322121590744e-13,
      "effect_class": "tiny"
    },
    {
      "candidate": "R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh}",
      "coeff_symbol": "\\gamma",
      "coefficient": "299.8035342667014",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 1.787557877171542e-13,
      "effect_class": "tiny"
    },
    {
      "candidate": "R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{fdh}",
      "coeff_symbol": "\\delta",
      "coefficient": "231.40346439045393",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 1.3797271822952068e-13,
      "effect_class": "tiny"
    },
    {
      "candidate": "∇^{c}R^{ab} · ∇_{c}R_{ab}",
      "coeff_symbol": "\\epsilon",
      "coefficient": "72585.55304515113",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 4.327863493406585e-11,
      "effect_class": "tiny"
    },
    {
      "candidate": "∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}",
      "coeff_symbol": "\\zeta",
      "coefficient": "10810998286.90261",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 6.44598309860126e-06,
      "effect_class": "weak"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0095/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0095/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0095/agent_solver_result/agent_solve/top_02_lagrangian_8_solution.csv`

## 14. wave_0080_lag_2  chi2=1638.086149

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: `147`
- H0_km_s_Mpc: `62.89924331`
- Omega_m0: `0.26673784`
- lambda_H_Lambda_over_H0: `7373.11497259`
- effective_correction_status: `weak`
- max_relative_effect_to_EH: `9.05219806e-05`
- dominant_correction_term: `R^{ab} · R_{ab}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-2} · R^{ab} · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-2460.5152687) Λ^{-2} · R^{ab} · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
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
√(-g) [ M_p² ( -2460.5152687 · Λ^{-2} · R^{ab} · R_{ab} ) ] +
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
  "effective_correction_status": "weak",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 9.052198063303056e-05,
  "dominant_correction_term": "R^{ab} · R_{ab}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 1,
  "tiny_correction_terms": 0,
  "correction_term_count": 1,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "R^{ab} · R_{ab}",
      "coeff_symbol": "\\beta",
      "coefficient": "-2460.5152687000445",
      "lambda_power": -2,
      "sector": "gravity",
      "relative_effect_to_EH": 9.052198063303056e-05,
      "effect_class": "weak"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0080/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0080/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0080/agent_solver_result/agent_solve/top_01_lagrangian_2_solution.csv`

## 15. wave_0065_lag_2  chi2=1638.089396

- scalar_config: `both`
- potential_types: `{"phi1": "quadratic", "phi2": "axion"}`
- agent_parameter_sample_index: `551`
- H0_km_s_Mpc: `58.63334614`
- Omega_m0: `0.26374452`
- lambda_H_Lambda_over_H0: `7267.21291085`
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0065/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0065/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0065/agent_solver_result/agent_solve/top_01_lagrangian_2_solution.csv`

## 16. wave_0056_lag_3  chi2=1638.090406

- scalar_config: `both`
- potential_types: `{"phi1": "quadratic", "phi2": "axion"}`
- agent_parameter_sample_index: `969`
- H0_km_s_Mpc: `61.894254`
- Omega_m0: `0.26151833`
- lambda_H_Lambda_over_H0: `5437.73090897`
- effective_correction_status: `weak`
- max_relative_effect_to_EH: `1.49778564e-06`
- dominant_correction_term: `φ1 · φ1 · R · R`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · φ1 · φ1 · R · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (1.8570700808e+08) Λ^{-4} · φ1 · φ1 · R · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · φ1 · φ1 · R · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 1.8570700808e+08 · Λ^{-4} · φ1 · φ1 · R · R ) ] +
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
  "max_relative_effect_to_EH": 1.4977856424011672e-06,
  "dominant_correction_term": "φ1 · φ1 · R · R",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 1,
  "tiny_correction_terms": 0,
  "correction_term_count": 1,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "φ1 · φ1 · R · R",
      "coeff_symbol": "\\beta",
      "coefficient": "185707008.07883695",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 1.4977856424011672e-06,
      "effect_class": "weak"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0056/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0056/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0056/agent_solver_result/agent_solve/top_02_lagrangian_3_solution.csv`

## 17. wave_0037_lag_3  chi2=1638.094744

- scalar_config: `both`
- potential_types: `{"phi1": "axion", "phi2": "axion"}`
- agent_parameter_sample_index: `96`
- H0_km_s_Mpc: `65.11523552`
- Omega_m0: `0.28258325`
- lambda_H_Lambda_over_H0: `5501.95291177`
- effective_correction_status: `moderate`
- max_relative_effect_to_EH: `1.01374271e-04`
- dominant_correction_term: `∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · ∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-4.6447808376e+10) Λ^{-4} · ∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · ∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -4.6447808376e+10 · Λ^{-4} · ∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd} ) ] +
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
    "candidate": "∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}",
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
  "effective_correction_status": "moderate",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 0.00010137427136967762,
  "dominant_correction_term": "∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 1,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 0,
  "correction_term_count": 1,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}",
      "coeff_symbol": "\\beta",
      "coefficient": "-46447808376.214294",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 0.00010137427136967762,
      "effect_class": "moderate"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0037/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0037/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0037/agent_solver_result/agent_solve/top_01_lagrangian_3_solution.csv`

## 18. wave_0046_lag_7  chi2=1638.105504

- scalar_config: `both`
- potential_types: `{"phi1": "axion", "phi2": "quadratic"}`
- agent_parameter_sample_index: `843`
- H0_km_s_Mpc: `70.38707448`
- Omega_m0: `0.280625`
- lambda_H_Lambda_over_H0: `5094.76640171`
- effective_correction_status: `weak`
- max_relative_effect_to_EH: `7.44685404e-05`
- dominant_correction_term: `φ2 · R · R`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · ∇^{a}R · ∇_{a}R  +  \gamma Λ^{-3} · φ2 · R · R  +  \delta Λ^{-4} · φ1 · ∇^{a}∇^{b}φ1 · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (1.9441737175e+09) Λ^{-4} · ∇^{a}R · ∇_{a}R  +  (4.1305509286e+07) Λ^{-3} · φ2 · R · R  +  (3.2908272030e+08) Λ^{-4} · φ1 · ∇^{a}∇^{b}φ1 · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · ∇^{a}R · ∇_{a}R ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-3} · φ2 · R · R ) ] +
√(-g) [ M_p² ( \delta · Λ^{-4} · φ1 · ∇^{a}∇^{b}φ1 · R_{ab} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 1.9441737175e+09 · Λ^{-4} · ∇^{a}R · ∇_{a}R ) ] +
√(-g) [ M_p² ( 4.1305509286e+07 · Λ^{-3} · φ2 · R · R ) ] +
√(-g) [ M_p² ( 3.2908272030e+08 · Λ^{-4} · φ1 · ∇^{a}∇^{b}φ1 · R_{ab} ) ] +
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
    "candidate": "∇^{a}R · ∇_{a}R",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "gravity"
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
    "candidate": "φ1 · ∇^{a}∇^{b}φ1 · R_{ab}",
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
  "max_relative_effect_to_EH": 7.44685404234942e-05,
  "dominant_correction_term": "φ2 · R · R",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 3,
  "tiny_correction_terms": 0,
  "correction_term_count": 3,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "∇^{a}R · ∇_{a}R",
      "coeff_symbol": "\\beta",
      "coefficient": "1944173717.4787118",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 5.771224371325034e-06,
      "effect_class": "weak"
    },
    {
      "candidate": "φ2 · R · R",
      "coeff_symbol": "\\gamma",
      "coefficient": "41305509.28638269",
      "lambda_power": -3,
      "sector": "non-minimal",
      "relative_effect_to_EH": 7.44685404234942e-05,
      "effect_class": "weak"
    },
    {
      "candidate": "φ1 · ∇^{a}∇^{b}φ1 · R_{ab}",
      "coeff_symbol": "\\delta",
      "coefficient": "329082720.2961052",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 3.596919362812689e-06,
      "effect_class": "weak"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0046/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0046/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0046/agent_solver_result/agent_solve/top_01_lagrangian_7_solution.csv`

## 19. wave_0037_lag_5  chi2=1638.114093

- scalar_config: `both`
- potential_types: `{"phi1": "axion", "phi2": "quadratic"}`
- agent_parameter_sample_index: `398`
- H0_km_s_Mpc: `66.53452663`
- Omega_m0: `0.2848288`
- lambda_H_Lambda_over_H0: `7382.58730617`
- effective_correction_status: `moderate`
- max_relative_effect_to_EH: `6.73279869e-04`
- dominant_correction_term: `∇^{c}R^{ab} · ∇_{b}R_{ac}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · ∇^{c}R^{ab} · ∇_{b}R_{ac} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-1.0000000000e+12) Λ^{-4} · ∇^{c}R^{ab} · ∇_{b}R_{ac} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · ∇^{c}R^{ab} · ∇_{b}R_{ac} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -1.0000000000e+12 · Λ^{-4} · ∇^{c}R^{ab} · ∇_{b}R_{ac} ) ] +
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
  "max_relative_effect_to_EH": 0.0006732798688454707,
  "dominant_correction_term": "∇^{c}R^{ab} · ∇_{b}R_{ac}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 1,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 0,
  "correction_term_count": 1,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "∇^{c}R^{ab} · ∇_{b}R_{ac}",
      "coeff_symbol": "\\beta",
      "coefficient": "-1000000000000.0",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 0.0006732798688454707,
      "effect_class": "moderate"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0037/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0037/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0037/agent_solver_result/agent_solve/top_02_lagrangian_5_solution.csv`

## 20. wave_0057_lag_6  chi2=1638.127402

- scalar_config: `both`
- potential_types: `{"phi1": "axion", "phi2": "quadratic"}`
- agent_parameter_sample_index: `560`
- H0_km_s_Mpc: `63.00871798`
- Omega_m0: `0.28581944`
- lambda_H_Lambda_over_H0: `6702.16584275`
- effective_correction_status: `active`
- max_relative_effect_to_EH: `0.02237347`
- dominant_correction_term: `φ2 · R · R`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · R^{ab} · R^{d}_{a} · R_{bd}  +  \gamma Λ^{-3} · φ2 · R · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-1.0000000000e+12) Λ^{-4} · R^{ab} · R^{d}_{a} · R_{bd}  +  (-2.6117301824e+10) Λ^{-3} · φ2 · R · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · R^{ab} · R^{d}_{a} · R_{bd} ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-3} · φ2 · R · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -1.0000000000e+12 · Λ^{-4} · R^{ab} · R^{d}_{a} · R_{bd} ) ] +
√(-g) [ M_p² ( -2.6117301824e+10 · Λ^{-3} · φ2 · R · R ) ] +
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
    "candidate": "R^{ab} · R^{d}_{a} · R_{bd}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "gravity"
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
  "max_relative_effect_to_EH": 0.022373468077663636,
  "dominant_correction_term": "φ2 · R · R",
  "active_correction_terms": 1,
  "moderate_correction_terms": 1,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 0,
  "correction_term_count": 2,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "R^{ab} · R^{d}_{a} · R_{bd}",
      "coeff_symbol": "\\beta",
      "coefficient": "-1000000000000.0",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 0.000991218308746386,
      "effect_class": "moderate"
    },
    {
      "candidate": "φ2 · R · R",
      "coeff_symbol": "\\gamma",
      "coefficient": "-26117301824.421734",
      "lambda_power": -3,
      "sector": "non-minimal",
      "relative_effect_to_EH": 0.022373468077663636,
      "effect_class": "active"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0057/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0057/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0057/agent_solver_result/agent_solve/top_01_lagrangian_6_solution.csv`

## 21. wave_0074_lag_4  chi2=1638.131101

- scalar_config: `both`
- potential_types: `{"phi1": "quadratic", "phi2": "quadratic"}`
- agent_parameter_sample_index: `931`
- H0_km_s_Mpc: `71.89658974`
- Omega_m0: `0.26245081`
- lambda_H_Lambda_over_H0: `6948.92515484`
- effective_correction_status: `eh_dominated`
- max_relative_effect_to_EH: `3.18578948e-13`
- dominant_correction_term: `φ2 · R^{bcd}_{a} · R^{a}_{bcd}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-3} · φ2 · R^{bcd}_{a} · R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-0.5129070606) Λ^{-3} · φ2 · R^{bcd}_{a} · R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
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
√(-g) [ M_p² ( -0.5129070606 · Λ^{-3} · φ2 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
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
  "effective_correction_status": "eh_dominated",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 3.1857894842455777e-13,
  "dominant_correction_term": "φ2 · R^{bcd}_{a} · R^{a}_{bcd}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 1,
  "correction_term_count": 1,
  "tiny_correction_fraction": 1.0,
  "term_effects": [
    {
      "candidate": "φ2 · R^{bcd}_{a} · R^{a}_{bcd}",
      "coeff_symbol": "\\beta",
      "coefficient": "-0.5129070606030489",
      "lambda_power": -3,
      "sector": "non-minimal",
      "relative_effect_to_EH": 3.1857894842455777e-13,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0074/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0074/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0074/agent_solver_result/agent_solve/top_01_lagrangian_4_solution.csv`

## 22. wave_0075_lag_4  chi2=1638.143573

- scalar_config: `both`
- potential_types: `{"phi1": "quadratic", "phi2": "axion"}`
- agent_parameter_sample_index: `981`
- H0_km_s_Mpc: `73.03570412`
- Omega_m0: `0.26102484`
- lambda_H_Lambda_over_H0: `7700.26233694`
- effective_correction_status: `eh_dominated`
- max_relative_effect_to_EH: `4.85150572e-16`
- dominant_correction_term: `φ1 · φ2 · R^{bcd}_{a} · R^{a}_{bcd}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · φ1 · φ2 · R^{bcd}_{a} · R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (2.3730053432) Λ^{-4} · φ1 · φ2 · R^{bcd}_{a} · R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · φ1 · φ2 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 2.3730053432 · Λ^{-4} · φ1 · φ2 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
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
    "candidate": "φ1 · φ2 · R^{bcd}_{a} · R^{a}_{bcd}",
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
  "effective_correction_status": "eh_dominated",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 4.851505719968046e-16,
  "dominant_correction_term": "φ1 · φ2 · R^{bcd}_{a} · R^{a}_{bcd}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 1,
  "correction_term_count": 1,
  "tiny_correction_fraction": 1.0,
  "term_effects": [
    {
      "candidate": "φ1 · φ2 · R^{bcd}_{a} · R^{a}_{bcd}",
      "coeff_symbol": "\\beta",
      "coefficient": "2.373005343152775",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 4.851505719968046e-16,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0075/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0075/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0075/agent_solver_result/agent_solve/top_01_lagrangian_4_solution.csv`

## 23. wave_0080_lag_1  chi2=1638.166764

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: `750`
- H0_km_s_Mpc: `61.62479401`
- Omega_m0: `0.26048217`
- lambda_H_Lambda_over_H0: `7075.22716224`
- effective_correction_status: `moderate`
- max_relative_effect_to_EH: `7.98120458e-04`
- dominant_correction_term: `∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · ∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (1.0000000000e+12) Λ^{-4} · ∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · ∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 1.0000000000e+12 · Λ^{-4} · ∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd} ) ] +
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
    "candidate": "∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}",
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
  "max_relative_effect_to_EH": 0.000798120457670431,
  "dominant_correction_term": "∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 1,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 0,
  "correction_term_count": 1,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}",
      "coeff_symbol": "\\beta",
      "coefficient": "1000000000000.0",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 0.000798120457670431,
      "effect_class": "moderate"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0080/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0080/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0080/agent_solver_result/agent_solve/top_02_lagrangian_1_solution.csv`

## 24. wave_0085_lag_7  chi2=1638.195065

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "axion", "phi2": null}`
- agent_parameter_sample_index: `864`
- H0_km_s_Mpc: `58.91247763`
- Omega_m0: `0.28218475`
- lambda_H_Lambda_over_H0: `5999.06545337`
- effective_correction_status: `weak`
- max_relative_effect_to_EH: `1.80465898e-05`
- dominant_correction_term: `∇^{c}R^{ab} · ∇_{b}R_{ac}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · R · R · R  +  \gamma Λ^{-4} · ∇^{c}R^{ab} · ∇_{b}R_{ac}  +  \delta Λ^{-4} · ∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}  +  \epsilon Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd}  +  \zeta Λ^{-4} · φ1 · φ1 · R · R  +  \eta Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-9.7845611091e+09) Λ^{-4} · R · R · R  +  (-1.1686906026e+10) Λ^{-4} · ∇^{c}R^{ab} · ∇_{b}R_{ac}  +  (-2.2058931236e+09) Λ^{-4} · ∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}  +  (3.0018845012e+05) Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd}  +  (1.4604211738e+09) Λ^{-4} · φ1 · φ1 · R · R  +  (1.2823200680e+09) Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · R · R · R ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · ∇^{c}R^{ab} · ∇_{b}R_{ac} ) ] +
√(-g) [ M_p² ( \delta · Λ^{-4} · ∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( \epsilon · Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( \zeta · Λ^{-4} · φ1 · φ1 · R · R ) ] +
√(-g) [ M_p² ( \eta · Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -9.7845611091e+09 · Λ^{-4} · R · R · R ) ] +
√(-g) [ M_p² ( -1.1686906026e+10 · Λ^{-4} · ∇^{c}R^{ab} · ∇_{b}R_{ac} ) ] +
√(-g) [ M_p² ( -2.2058931236e+09 · Λ^{-4} · ∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( 3.0018845012e+05 · Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( 1.4604211738e+09 · Λ^{-4} · φ1 · φ1 · R · R ) ] +
√(-g) [ M_p² ( 1.2823200680e+09 · Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
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
    "candidate": "∇^{c}R^{ab} · ∇_{b}R_{ac}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\delta",
    "coeff_token": "COEFF_3",
    "candidate": "∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}",
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
    "candidate": "φ1 · φ1 · R · R",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\eta",
    "coeff_token": "COEFF_6",
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
  "max_relative_effect_to_EH": 1.8046589764633153e-05,
  "dominant_correction_term": "∇^{c}R^{ab} · ∇_{b}R_{ac}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 6,
  "tiny_correction_terms": 0,
  "correction_term_count": 6,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "R · R · R",
      "coeff_symbol": "\\beta",
      "coefficient": "-9784561109.11786",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 1.5109042545369345e-05,
      "effect_class": "weak"
    },
    {
      "candidate": "∇^{c}R^{ab} · ∇_{b}R_{ac}",
      "coeff_symbol": "\\gamma",
      "coefficient": "-11686906025.514637",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 1.8046589764633153e-05,
      "effect_class": "weak"
    },
    {
      "candidate": "∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}",
      "coeff_symbol": "\\delta",
      "coefficient": "-2205893123.5590334",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 3.4062777760499798e-06,
      "effect_class": "weak"
    },
    {
      "candidate": "φ1 · R^{bcd}_{a} · R^{a}_{bcd}",
      "coeff_symbol": "\\epsilon",
      "coefficient": "300188.4501164827",
      "lambda_power": -3,
      "sector": "non-minimal",
      "relative_effect_to_EH": 5.3312732317695736e-06,
      "effect_class": "weak"
    },
    {
      "candidate": "φ1 · φ1 · R · R",
      "coeff_symbol": "\\zeta",
      "coefficient": "1460421173.7706041",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 8.288754007576513e-06,
      "effect_class": "weak"
    },
    {
      "candidate": "φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd}",
      "coeff_symbol": "\\eta",
      "coefficient": "1282320068.0466676",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 7.277924884898395e-06,
      "effect_class": "weak"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0085/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0085/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0085/agent_solver_result/agent_solve/top_03_lagrangian_7_solution.csv`

## 25. wave_0089_lag_4  chi2=1638.23119

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "axion", "phi2": null}`
- agent_parameter_sample_index: `351`
- H0_km_s_Mpc: `60.72424504`
- Omega_m0: `0.28855312`
- lambda_H_Lambda_over_H0: `6275.87513285`
- effective_correction_status: `eh_dominated`
- max_relative_effect_to_EH: `4.68580852e-07`
- dominant_correction_term: `R · R · R`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · R · R · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (3.6345589595e+08) Λ^{-4} · R · R · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · R · R · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 3.6345589595e+08 · Λ^{-4} · R · R · R ) ] +
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
  "max_relative_effect_to_EH": 4.6858085182439223e-07,
  "dominant_correction_term": "R · R · R",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 1,
  "correction_term_count": 1,
  "tiny_correction_fraction": 1.0,
  "term_effects": [
    {
      "candidate": "R · R · R",
      "coeff_symbol": "\\beta",
      "coefficient": "363455895.9462435",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 4.6858085182439223e-07,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0089/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0089/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0089/agent_solver_result/agent_solve/top_02_lagrangian_4_solution.csv`

## 26. wave_0037_lag_6  chi2=1638.231315

- scalar_config: `both`
- potential_types: `{"phi1": "axion", "phi2": "quadratic"}`
- agent_parameter_sample_index: `90`
- H0_km_s_Mpc: `63.0700626`
- Omega_m0: `0.27085412`
- lambda_H_Lambda_over_H0: `7479.35304925`
- effective_correction_status: `moderate`
- max_relative_effect_to_EH: `6.39107421e-04`
- dominant_correction_term: `R_{ab} · R^{adef} · R^{b}_{def}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (1.0000000000e+12) Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 1.0000000000e+12 · Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def} ) ] +
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
  "max_relative_effect_to_EH": 0.0006391074211790134,
  "dominant_correction_term": "R_{ab} · R^{adef} · R^{b}_{def}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 1,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 0,
  "correction_term_count": 1,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "R_{ab} · R^{adef} · R^{b}_{def}",
      "coeff_symbol": "\\beta",
      "coefficient": "1000000000000.0",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 0.0006391074211790134,
      "effect_class": "moderate"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0037/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0037/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0037/agent_solver_result/agent_solve/top_03_lagrangian_6_solution.csv`

## 27. wave_0023_lag_2  chi2=1638.235207

- scalar_config: `both`
- potential_types: `{"phi1": "quadratic", "phi2": "axion"}`
- agent_parameter_sample_index: `196`
- H0_km_s_Mpc: `70.83327533`
- Omega_m0: `0.2853244`
- lambda_H_Lambda_over_H0: `5182.85951166`
- effective_correction_status: `moderate`
- max_relative_effect_to_EH: `2.65364802e-04`
- dominant_correction_term: `R_{ab} · R^{adef} · R^{b}_{def}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-9.5739480962e+10) Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -9.5739480962e+10 · Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def} ) ] +
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
  "max_relative_effect_to_EH": 0.0002653648016182838,
  "dominant_correction_term": "R_{ab} · R^{adef} · R^{b}_{def}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 1,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 0,
  "correction_term_count": 1,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "R_{ab} · R^{adef} · R^{b}_{def}",
      "coeff_symbol": "\\beta",
      "coefficient": "-95739480961.72742",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 0.0002653648016182838,
      "effect_class": "moderate"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0023/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0023/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0023/agent_solver_result/agent_solve/top_01_lagrangian_2_solution.csv`

## 28. wave_0047_lag_2  chi2=1638.250313

- scalar_config: `both`
- potential_types: `{"phi1": "axion", "phi2": "quadratic"}`
- agent_parameter_sample_index: `147`
- H0_km_s_Mpc: `72.69516961`
- Omega_m0: `0.28399316`
- lambda_H_Lambda_over_H0: `5460.8369649`
- effective_correction_status: `moderate`
- max_relative_effect_to_EH: `0.00544942`
- dominant_correction_term: `φ1 · R^{bcd}_{a} · R^{a}_{bcd}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (2.3325540268e+08) Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
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
√(-g) [ M_p² ( 2.3325540268e+08 · Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
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
  "effective_correction_status": "moderate",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 0.005449424585663238,
  "dominant_correction_term": "φ1 · R^{bcd}_{a} · R^{a}_{bcd}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 1,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 0,
  "correction_term_count": 1,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "φ1 · R^{bcd}_{a} · R^{a}_{bcd}",
      "coeff_symbol": "\\beta",
      "coefficient": "233255402.67719555",
      "lambda_power": -3,
      "sector": "non-minimal",
      "relative_effect_to_EH": 0.005449424585663238,
      "effect_class": "moderate"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0047/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0047/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0047/agent_solver_result/agent_solve/top_01_lagrangian_2_solution.csv`

## 29. wave_0038_lag_3  chi2=1638.254122

- scalar_config: `both`
- potential_types: `{"phi1": "quadratic", "phi2": "axion"}`
- agent_parameter_sample_index: `617`
- H0_km_s_Mpc: `68.8105493`
- Omega_m0: `0.29964468`
- lambda_H_Lambda_over_H0: `5916.34745197`
- effective_correction_status: `moderate`
- max_relative_effect_to_EH: `0.00163236`
- dominant_correction_term: `∇^{c}R^{ab} · ∇_{c}R_{ab}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · ∇^{c}R^{ab} · ∇_{c}R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (1.0000000000e+12) Λ^{-4} · ∇^{c}R^{ab} · ∇_{c}R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · ∇^{c}R^{ab} · ∇_{c}R_{ab} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 1.0000000000e+12 · Λ^{-4} · ∇^{c}R^{ab} · ∇_{c}R_{ab} ) ] +
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
    "candidate": "∇^{c}R^{ab} · ∇_{c}R_{ab}",
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
  "max_relative_effect_to_EH": 0.0016323576216882704,
  "dominant_correction_term": "∇^{c}R^{ab} · ∇_{c}R_{ab}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 1,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 0,
  "correction_term_count": 1,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "∇^{c}R^{ab} · ∇_{c}R_{ab}",
      "coeff_symbol": "\\beta",
      "coefficient": "1000000000000.0",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 0.0016323576216882704,
      "effect_class": "moderate"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0038/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0038/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0038/agent_solver_result/agent_solve/top_02_lagrangian_3_solution.csv`

## 30. wave_0039_lag_4  chi2=1638.298815

- scalar_config: `both`
- potential_types: `{"phi1": "axion", "phi2": "quadratic"}`
- agent_parameter_sample_index: `111`
- H0_km_s_Mpc: `70.82324451`
- Omega_m0: `0.2874434`
- lambda_H_Lambda_over_H0: `5848.38368771`
- effective_correction_status: `weak`
- max_relative_effect_to_EH: `1.08887534e-05`
- dominant_correction_term: `∇^{a}φ1 · ∇_{a}R`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · ∇^{a}R · ∇_{a}R  +  \gamma Λ^{-3} · ∇^{a}φ1 · ∇_{a}R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (1838.3053558494) Λ^{-4} · ∇^{a}R · ∇_{a}R  +  (-5.6049300116e+05) Λ^{-3} · ∇^{a}φ1 · ∇_{a}R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · ∇^{a}R · ∇_{a}R ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-3} · ∇^{a}φ1 · ∇_{a}R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 1838.3053558494 · Λ^{-4} · ∇^{a}R · ∇_{a}R ) ] +
√(-g) [ M_p² ( -5.6049300116e+05 · Λ^{-3} · ∇^{a}φ1 · ∇_{a}R ) ] +
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
    "candidate": "∇^{a}R · ∇_{a}R",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\gamma",
    "coeff_token": "COEFF_2",
    "candidate": "∇^{a}φ1 · ∇_{a}R",
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
  "effective_correction_status": "weak",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 1.0888753413233585e-05,
  "dominant_correction_term": "∇^{a}φ1 · ∇_{a}R",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 1,
  "tiny_correction_terms": 1,
  "correction_term_count": 2,
  "tiny_correction_fraction": 0.5,
  "term_effects": [
    {
      "candidate": "∇^{a}R · ∇_{a}R",
      "coeff_symbol": "\\beta",
      "coefficient": "1838.3053558494385",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 3.1427093652384514e-12,
      "effect_class": "tiny"
    },
    {
      "candidate": "∇^{a}φ1 · ∇_{a}R",
      "coeff_symbol": "\\gamma",
      "coefficient": "-560493.0011636482",
      "lambda_power": -3,
      "sector": "non-minimal",
      "relative_effect_to_EH": 1.0888753413233585e-05,
      "effect_class": "weak"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0039/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0039/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0039/agent_solver_result/agent_solve/top_01_lagrangian_4_solution.csv`

## 31. wave_0065_lag_3  chi2=1638.337204

- scalar_config: `both`
- potential_types: `{"phi1": "axion", "phi2": "quadratic"}`
- agent_parameter_sample_index: `754`
- H0_km_s_Mpc: `68.86137077`
- Omega_m0: `0.27084726`
- lambda_H_Lambda_over_H0: `6704.31722666`
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0065/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0065/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0065/agent_solver_result/agent_solve/top_02_lagrangian_3_solution.csv`

## 32. wave_0109_lag_5  chi2=1638.34081

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "axion", "phi2": null}`
- agent_parameter_sample_index: `690`
- H0_km_s_Mpc: `73.71372217`
- Omega_m0: `0.28552719`
- lambda_H_Lambda_over_H0: `7177.41834041`
- effective_correction_status: `active`
- max_relative_effect_to_EH: `0.01027259`
- dominant_correction_term: `φ1 · R^{ab} · R_{ab}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · R^{b}_{a} · R^{cd} · R^{a}_{cbd}  +  \gamma Λ^{-3} · φ1 · R^{ab} · R_{ab}  +  \delta Λ^{-4} · φ1 · φ1 · R^{ab} · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (1.0000000000e+12) Λ^{-4} · R^{b}_{a} · R^{cd} · R^{a}_{cbd}  +  (9.9386108307e+08) Λ^{-3} · φ1 · R^{ab} · R_{ab}  +  (-1.0000000000e+12) Λ^{-4} · φ1 · φ1 · R^{ab} · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · R^{b}_{a} · R^{cd} · R^{a}_{cbd} ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-3} · φ1 · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( \delta · Λ^{-4} · φ1 · φ1 · R^{ab} · R_{ab} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 1.0000000000e+12 · Λ^{-4} · R^{b}_{a} · R^{cd} · R^{a}_{cbd} ) ] +
√(-g) [ M_p² ( 9.9386108307e+08 · Λ^{-3} · φ1 · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( -1.0000000000e+12 · Λ^{-4} · φ1 · φ1 · R^{ab} · R_{ab} ) ] +
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
  "max_relative_effect_to_EH": 0.010272593221062195,
  "dominant_correction_term": "φ1 · R^{ab} · R_{ab}",
  "active_correction_terms": 1,
  "moderate_correction_terms": 2,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 0,
  "correction_term_count": 3,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "R^{b}_{a} · R^{cd} · R^{a}_{cbd}",
      "coeff_symbol": "\\beta",
      "coefficient": "1000000000000.0",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 0.0007536278777786473,
      "effect_class": "moderate"
    },
    {
      "candidate": "φ1 · R^{ab} · R_{ab}",
      "coeff_symbol": "\\gamma",
      "coefficient": "993861083.0728272",
      "lambda_power": -3,
      "sector": "non-minimal",
      "relative_effect_to_EH": 0.010272593221062195,
      "effect_class": "active"
    },
    {
      "candidate": "φ1 · φ1 · R^{ab} · R_{ab}",
      "coeff_symbol": "\\delta",
      "coefficient": "-1000000000000.0",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 0.002751790306042741,
      "effect_class": "moderate"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0109/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0109/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0109/agent_solver_result/agent_solve/top_04_lagrangian_5_solution.csv`

## 33. wave_0033_lag_4  chi2=1638.341954

- scalar_config: `both`
- potential_types: `{"phi1": "quadratic", "phi2": "quadratic"}`
- agent_parameter_sample_index: `878`
- H0_km_s_Mpc: `64.98969062`
- Omega_m0: `0.30261655`
- lambda_H_Lambda_over_H0: `5671.58913841`
- effective_correction_status: `moderate`
- max_relative_effect_to_EH: `2.01676845e-04`
- dominant_correction_term: `∇^{a}∇_{a}R · R^{c}_{c}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def}  +  \gamma Λ^{-4} · ∇^{a}∇_{a}R · R^{c}_{c}  +  \delta Λ^{-4} · ∇^{c}R^{ab} · ∇_{c}R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (7.4554771614e+10) Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def}  +  (-1.0433862051e+11) Λ^{-4} · ∇^{a}∇_{a}R · R^{c}_{c}  +  (-2.5576879191e+10) Λ^{-4} · ∇^{c}R^{ab} · ∇_{c}R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def} ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · ∇^{a}∇_{a}R · R^{c}_{c} ) ] +
√(-g) [ M_p² ( \delta · Λ^{-4} · ∇^{c}R^{ab} · ∇_{c}R_{ab} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 7.4554771614e+10 · Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def} ) ] +
√(-g) [ M_p² ( -1.0433862051e+11 · Λ^{-4} · ∇^{a}∇_{a}R · R^{c}_{c} ) ] +
√(-g) [ M_p² ( -2.5576879191e+10 · Λ^{-4} · ∇^{c}R^{ab} · ∇_{c}R_{ab} ) ] +
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
    "candidate": "R_{ab} · R^{adef} · R^{b}_{def}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\gamma",
    "coeff_token": "COEFF_2",
    "candidate": "∇^{a}∇_{a}R · R^{c}_{c}",
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
  "max_relative_effect_to_EH": 0.0002016768445088599,
  "dominant_correction_term": "∇^{a}∇_{a}R · R^{c}_{c}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 2,
  "weak_correction_terms": 1,
  "tiny_correction_terms": 0,
  "correction_term_count": 3,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "R_{ab} · R^{adef} · R^{b}_{def}",
      "coeff_symbol": "\\beta",
      "coefficient": "74554771614.00656",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 0.00014410743605007442,
      "effect_class": "moderate"
    },
    {
      "candidate": "∇^{a}∇_{a}R · R^{c}_{c}",
      "coeff_symbol": "\\gamma",
      "coefficient": "-104338620506.48701",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 0.0002016768445088599,
      "effect_class": "moderate"
    },
    {
      "candidate": "∇^{c}R^{ab} · ∇_{c}R_{ab}",
      "coeff_symbol": "\\delta",
      "coefficient": "-25576879191.46126",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 4.943772749417866e-05,
      "effect_class": "weak"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0033/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0033/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0033/agent_solver_result/agent_solve/top_02_lagrangian_4_solution.csv`

## 34. wave_0028_lag_6  chi2=1638.345998

- scalar_config: `both`
- potential_types: `{"phi1": "axion", "phi2": "axion"}`
- agent_parameter_sample_index: `998`
- H0_km_s_Mpc: `65.36809367`
- Omega_m0: `0.30344174`
- lambda_H_Lambda_over_H0: `4549.37260169`
- effective_correction_status: `moderate`
- max_relative_effect_to_EH: `0.00227831`
- dominant_correction_term: `φ1 · φ2 · R^{bcd}_{a} · R^{a}_{bcd}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · φ1 · φ2 · R · R  +  \gamma Λ^{-4} · φ1 · φ2 · R^{bcd}_{a} · R^{a}_{bcd}  +  \delta Λ^{-4} · φ1 · ∇^{a}∇_{a}φ1 · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (3.0053719577e+11) Λ^{-4} · φ1 · φ2 · R · R  +  (1.0000000000e+12) Λ^{-4} · φ1 · φ2 · R^{bcd}_{a} · R^{a}_{bcd}  +  (-2.5796033217e+10) Λ^{-4} · φ1 · ∇^{a}∇_{a}φ1 · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · φ1 · φ2 · R · R ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · φ1 · φ2 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( \delta · Λ^{-4} · φ1 · ∇^{a}∇_{a}φ1 · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 3.0053719577e+11 · Λ^{-4} · φ1 · φ2 · R · R ) ] +
√(-g) [ M_p² ( 1.0000000000e+12 · Λ^{-4} · φ1 · φ2 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( -2.5796033217e+10 · Λ^{-4} · φ1 · ∇^{a}∇_{a}φ1 · R ) ] +
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
    "coeff_symbol": "\\gamma",
    "coeff_token": "COEFF_2",
    "candidate": "φ1 · φ2 · R^{bcd}_{a} · R^{a}_{bcd}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\delta",
    "coeff_token": "COEFF_3",
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
  "max_relative_effect_to_EH": 0.002278310648366462,
  "dominant_correction_term": "φ1 · φ2 · R^{bcd}_{a} · R^{a}_{bcd}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 3,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 0,
  "correction_term_count": 3,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "φ1 · φ2 · R · R",
      "coeff_symbol": "\\beta",
      "coefficient": "300537195765.89124",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 0.000684717093343626,
      "effect_class": "moderate"
    },
    {
      "candidate": "φ1 · φ2 · R^{bcd}_{a} · R^{a}_{bcd}",
      "coeff_symbol": "\\gamma",
      "coefficient": "1000000000000.0",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 0.002278310648366462,
      "effect_class": "moderate"
    },
    {
      "candidate": "φ1 · ∇^{a}∇_{a}φ1 · R",
      "coeff_symbol": "\\delta",
      "coefficient": "-25796033216.628635",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 0.00039672683082759896,
      "effect_class": "moderate"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0028/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0028/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0028/agent_solver_result/agent_solve/top_02_lagrangian_6_solution.csv`

## 35. wave_0031_lag_2  chi2=1638.353284

- scalar_config: `both`
- potential_types: `{"phi1": "axion", "phi2": "axion"}`
- agent_parameter_sample_index: `493`
- H0_km_s_Mpc: `72.4340985`
- Omega_m0: `0.29048211`
- lambda_H_Lambda_over_H0: `6275.03772502`
- effective_correction_status: `weak`
- max_relative_effect_to_EH: `1.36158019e-06`
- dominant_correction_term: `φ1 · ∇^{a}φ2 · ∇_{a}R`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · φ1 · ∇^{a}φ2 · ∇_{a}R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-1.8631032786e+09) Λ^{-4} · φ1 · ∇^{a}φ2 · ∇_{a}R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · φ1 · ∇^{a}φ2 · ∇_{a}R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -1.8631032786e+09 · Λ^{-4} · φ1 · ∇^{a}φ2 · ∇_{a}R ) ] +
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
    "candidate": "φ1 · ∇^{a}φ2 · ∇_{a}R",
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
  "effective_correction_status": "weak",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 1.3615801908712085e-06,
  "dominant_correction_term": "φ1 · ∇^{a}φ2 · ∇_{a}R",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 1,
  "tiny_correction_terms": 0,
  "correction_term_count": 1,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "φ1 · ∇^{a}φ2 · ∇_{a}R",
      "coeff_symbol": "\\beta",
      "coefficient": "-1863103278.6392286",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 1.3615801908712085e-06,
      "effect_class": "weak"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0031/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0031/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0031/agent_solver_result/agent_solve/top_04_lagrangian_2_solution.csv`

## 36. wave_0066_lag_2  chi2=1638.392762

- scalar_config: `both`
- potential_types: `{"phi1": "axion", "phi2": "axion"}`
- agent_parameter_sample_index: `197`
- H0_km_s_Mpc: `62.53489855`
- Omega_m0: `0.29350495`
- lambda_H_Lambda_over_H0: `5551.82095739`
- effective_correction_status: `moderate`
- max_relative_effect_to_EH: `0.00247523`
- dominant_correction_term: `φ1 · φ1 · R · R`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · φ1 · φ1 · R · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-3.1981094509e+11) Λ^{-4} · φ1 · φ1 · R · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · φ1 · φ1 · R · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -3.1981094509e+11 · Λ^{-4} · φ1 · φ1 · R · R ) ] +
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
  "max_relative_effect_to_EH": 0.0024752309523120653,
  "dominant_correction_term": "φ1 · φ1 · R · R",
  "active_correction_terms": 0,
  "moderate_correction_terms": 1,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 0,
  "correction_term_count": 1,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "φ1 · φ1 · R · R",
      "coeff_symbol": "\\beta",
      "coefficient": "-319810945087.6883",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 0.0024752309523120653,
      "effect_class": "moderate"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0066/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0066/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0066/agent_solver_result/agent_solve/top_04_lagrangian_2_solution.csv`

## 37. wave_0091_lag_5  chi2=1638.406547

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "axion", "phi2": null}`
- agent_parameter_sample_index: `394`
- H0_km_s_Mpc: `71.45513294`
- Omega_m0: `0.2796228`
- lambda_H_Lambda_over_H0: `5845.3802237`
- effective_correction_status: `weak`
- max_relative_effect_to_EH: `1.59544913e-05`
- dominant_correction_term: `∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · ∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (9.3133093909e+09) Λ^{-4} · ∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · ∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 9.3133093909e+09 · Λ^{-4} · ∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd} ) ] +
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
    "candidate": "∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}",
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
  "max_relative_effect_to_EH": 1.5954491339573018e-05,
  "dominant_correction_term": "∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 1,
  "tiny_correction_terms": 0,
  "correction_term_count": 1,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}",
      "coeff_symbol": "\\beta",
      "coefficient": "9313309390.867094",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 1.5954491339573018e-05,
      "effect_class": "weak"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0091/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0091/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0091/agent_solver_result/agent_solve/top_03_lagrangian_5_solution.csv`

## 38. wave_0029_lag_7  chi2=1638.407757

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "axion", "phi2": null}`
- agent_parameter_sample_index: `800`
- H0_km_s_Mpc: `62.28329003`
- Omega_m0: `0.30199085`
- lambda_H_Lambda_over_H0: `4930.90333377`
- effective_correction_status: `active`
- max_relative_effect_to_EH: `0.04070628`
- dominant_correction_term: `R^{ab} · R_{ab}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-2} · R^{ab} · R_{ab}  +  \gamma Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def}  +  \delta Λ^{-4} · ∇^{c}R^{ab} · ∇_{b}R_{ac} )  +  \epsilon Λ^{1} · ∇^{a}∇_{a}φ1  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (4.9486229095e+05) Λ^{-2} · R^{ab} · R_{ab}  +  (-1.0000000000e+12) Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def}  +  (1.0000000000e+12) Λ^{-4} · ∇^{c}R^{ab} · ∇_{b}R_{ac} )  +  (1.0156876848) Λ^{1} · ∇^{a}∇_{a}φ1  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-2} · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def} ) ] +
√(-g) [ M_p² ( \delta · Λ^{-4} · ∇^{c}R^{ab} · ∇_{b}R_{ac} ) ] +
√(-g) [ \epsilon · Λ^{1} · ∇^{a}∇_{a}φ1 ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 4.9486229095e+05 · Λ^{-2} · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( -1.0000000000e+12 · Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def} ) ] +
√(-g) [ M_p² ( 1.0000000000e+12 · Λ^{-4} · ∇^{c}R^{ab} · ∇_{b}R_{ac} ) ] +
√(-g) [ 1.0156876848 · Λ^{1} · ∇^{a}∇_{a}φ1 ] +
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
    "candidate": "∇^{c}R^{ab} · ∇_{b}R_{ac}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\epsilon",
    "coeff_token": "COEFF_4",
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
  "effective_correction_status": "active",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 0.04070627664122924,
  "dominant_correction_term": "R^{ab} · R_{ab}",
  "active_correction_terms": 1,
  "moderate_correction_terms": 2,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 0,
  "correction_term_count": 3,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "R^{ab} · R_{ab}",
      "coeff_symbol": "\\beta",
      "coefficient": "494862.2909532226",
      "lambda_power": -2,
      "sector": "gravity",
      "relative_effect_to_EH": 0.04070627664122924,
      "effect_class": "active"
    },
    {
      "candidate": "R_{ab} · R^{adef} · R^{b}_{def}",
      "coeff_symbol": "\\gamma",
      "coefficient": "-1000000000000.0",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 0.003383171714138285,
      "effect_class": "moderate"
    },
    {
      "candidate": "∇^{c}R^{ab} · ∇_{b}R_{ac}",
      "coeff_symbol": "\\delta",
      "coefficient": "1000000000000.0",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 0.003383171714138285,
      "effect_class": "moderate"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0029/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0029/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0029/agent_solver_result/agent_solve/top_04_lagrangian_7_solution.csv`

## 39. wave_0102_lag_6  chi2=1638.512533

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "axion", "phi2": null}`
- agent_parameter_sample_index: `570`
- H0_km_s_Mpc: `65.81731386`
- Omega_m0: `0.30123359`
- lambda_H_Lambda_over_H0: `6328.67913303`
- effective_correction_status: `moderate`
- max_relative_effect_to_EH: `0.00454287`
- dominant_correction_term: `φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-1.0000000000e+12) Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
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
√(-g) [ M_p² ( -1.0000000000e+12 · Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
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
  "max_relative_effect_to_EH": 0.0045428735646223595,
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
      "coefficient": "-1000000000000.0",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 0.0045428735646223595,
      "effect_class": "moderate"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0102/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0102/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0102/agent_solver_result/agent_solve/top_03_lagrangian_6_solution.csv`

## 40. wave_0022_lag_1  chi2=1638.679512

- scalar_config: `both`
- potential_types: `{"phi1": "axion", "phi2": "axion"}`
- agent_parameter_sample_index: `865`
- H0_km_s_Mpc: `71.26680603`
- Omega_m0: `0.29416283`
- lambda_H_Lambda_over_H0: `1.92497582e+04`
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
- solver output: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0022/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0022/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/graph_agent_batch_1600_llm_v3_wave_0022/agent_solver_result/agent_solve/top_02_lagrangian_1_solution.csv`
