# Accepted Lagrangians And Parameters

Each entry is the best chi-square representative of one accepted theory family.
The full accepted-attempt list is preserved in `accepted_summary.json`.
Each displayed entry uses the actual `agent_lagrangians.pkl` object that entered EOM -> Builder -> Solver.

## 1. loop_01  chi2=1640.045401

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: `58`
- H0_km_s_Mpc: `66.66213977`
- Omega_m0: `0.27248512`
- lambda_H_Lambda_over_H0: `1.23757964e+04`
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
- solver output: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_143921_1e33c0b9/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_143921_1e33c0b9/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_143921_1e33c0b9/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 2. loop_07  chi2=1657.023856

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "axion", "phi2": null}`
- agent_parameter_sample_index: `485`
- H0_km_s_Mpc: `57.09327206`
- Omega_m0: `0.27260845`
- lambda_H_Lambda_over_H0: `4132.75186775`
- effective_correction_status: `eh_dominated`
- max_relative_effect_to_EH: `8.88510276e-23`
- dominant_correction_term: `φ1 · φ1 · R · R`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · φ1 · φ1 · R · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-2.2643275765e-09) Λ^{-4} · φ1 · φ1 · R · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · φ1 · φ1 · R · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -2.2643275765e-09 · Λ^{-4} · φ1 · φ1 · R · R ) ] +
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
  "max_relative_effect_to_EH": 8.885102756994853e-23,
  "dominant_correction_term": "φ1 · φ1 · R · R",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 1,
  "correction_term_count": 1,
  "tiny_correction_fraction": 1.0,
  "term_effects": [
    {
      "candidate": "φ1 · φ1 · R · R",
      "coeff_symbol": "\\beta",
      "coefficient": "-2.264327576463958e-09",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 8.885102756994853e-23,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_144246_2586f297/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_144246_2586f297/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_144246_2586f297/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 3. loop_08  chi2=1674.136138

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: `800`
- H0_km_s_Mpc: `60.38153379`
- Omega_m0: `0.29780189`
- lambda_H_Lambda_over_H0: `2.01089368e+04`
- effective_correction_status: `eh_dominated`
- max_relative_effect_to_EH: `4.61842208e-25`
- dominant_correction_term: `φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-2.2655825294e-09) Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
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
√(-g) [ M_p² ( -2.2655825294e-09 · Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
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
  "effective_correction_status": "eh_dominated",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 4.61842207500585e-25,
  "dominant_correction_term": "φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 1,
  "correction_term_count": 1,
  "tiny_correction_fraction": 1.0,
  "term_effects": [
    {
      "candidate": "φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd}",
      "coeff_symbol": "\\beta",
      "coefficient": "-2.265582529390176e-09",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 4.61842207500585e-25,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_144257_f11b1231/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_144257_f11b1231/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_144257_f11b1231/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 4. loop_05  chi2=1686.231827

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: `36`
- H0_km_s_Mpc: `71.69081916`
- Omega_m0: `0.20725463`
- lambda_H_Lambda_over_H0: `9233.17404355`
- effective_correction_status: `eh_dominated`
- max_relative_effect_to_EH: `9.05108578e-24`
- dominant_correction_term: `∇^{c}R^{ab} · ∇_{c}R_{ab}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · ∇^{c}R^{ab} · ∇_{c}R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (3.2890825478e-08) Λ^{-4} · ∇^{c}R^{ab} · ∇_{c}R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · ∇^{c}R^{ab} · ∇_{c}R_{ab} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 3.2890825478e-08 · Λ^{-4} · ∇^{c}R^{ab} · ∇_{c}R_{ab} ) ] +
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
  }
]
```

### Effective Correction Diagnostics

```json
{
  "effective_correction_status": "eh_dominated",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 9.051085782528072e-24,
  "dominant_correction_term": "∇^{c}R^{ab} · ∇_{c}R_{ab}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 1,
  "correction_term_count": 1,
  "tiny_correction_fraction": 1.0,
  "term_effects": [
    {
      "candidate": "∇^{c}R^{ab} · ∇_{c}R_{ab}",
      "coeff_symbol": "\\beta",
      "coefficient": "3.289082547847523e-08",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 9.051085782528072e-24,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_144221_03a93ae2/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_144221_03a93ae2/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_144221_03a93ae2/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 5. loop_04_expanded  chi2=1688.147231

- scalar_config: `both`
- potential_types: `{"phi1": "axion", "phi2": "axion"}`
- agent_parameter_sample_index: `449`
- H0_km_s_Mpc: `66.84312655`
- Omega_m0: `0.24015564`
- lambda_H_Lambda_over_H0: `1.15602638e+04`
- effective_correction_status: `eh_dominated`
- max_relative_effect_to_EH: `2.37640992e-22`
- dominant_correction_term: `∇^{c}R^{ab} · ∇_{c}R_{ab}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · ∇^{c}R^{ab} · ∇_{c}R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (2.1220828334e-06) Λ^{-4} · ∇^{c}R^{ab} · ∇_{c}R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
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
√(-g) [ M_p² ( 2.1220828334e-06 · Λ^{-4} · ∇^{c}R^{ab} · ∇_{c}R_{ab} ) ] +
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
  "effective_correction_status": "eh_dominated",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 2.3764099215282317e-22,
  "dominant_correction_term": "∇^{c}R^{ab} · ∇_{c}R_{ab}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 1,
  "correction_term_count": 1,
  "tiny_correction_fraction": 1.0,
  "term_effects": [
    {
      "candidate": "∇^{c}R^{ab} · ∇_{c}R_{ab}",
      "coeff_symbol": "\\beta",
      "coefficient": "2.1220828333979084e-06",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 2.3764099215282317e-22,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_144044_5df1f48b/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_144044_5df1f48b/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_144044_5df1f48b/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 6. loop_06  chi2=1701.282902

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: `260`
- H0_km_s_Mpc: `65.65881447`
- Omega_m0: `0.24777173`
- lambda_H_Lambda_over_H0: `3.73245641e+04`
- effective_correction_status: `eh_dominated`
- max_relative_effect_to_EH: `1.25666434e-22`
- dominant_correction_term: `φ1 · φ1 · R · R`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · φ1 · φ1 · R · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (3.8716666358e-05) Λ^{-4} · φ1 · φ1 · R · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · φ1 · φ1 · R · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 3.8716666358e-05 · Λ^{-4} · φ1 · φ1 · R · R ) ] +
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
  }
]
```

### Effective Correction Diagnostics

```json
{
  "effective_correction_status": "eh_dominated",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 1.2566643400632075e-22,
  "dominant_correction_term": "φ1 · φ1 · R · R",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 1,
  "correction_term_count": 1,
  "tiny_correction_fraction": 1.0,
  "term_effects": [
    {
      "candidate": "φ1 · φ1 · R · R",
      "coeff_symbol": "\\beta",
      "coefficient": "3.87166663582217e-05",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 1.2566643400632075e-22,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_144236_7001ce62/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_144236_7001ce62/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_144236_7001ce62/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 7. loop_09  chi2=1724.480145

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "axion", "phi2": null}`
- agent_parameter_sample_index: `119`
- H0_km_s_Mpc: `71.98920625`
- Omega_m0: `0.23516984`
- lambda_H_Lambda_over_H0: `2.01979124e+04`
- effective_correction_status: `eh_dominated`
- max_relative_effect_to_EH: `7.85333329e-27`
- dominant_correction_term: `φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-2.5015117826e-10) Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
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
√(-g) [ M_p² ( -2.5015117826e-10 · Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
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
  "effective_correction_status": "eh_dominated",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 7.853333291163505e-27,
  "dominant_correction_term": "φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 1,
  "correction_term_count": 1,
  "tiny_correction_fraction": 1.0,
  "term_effects": [
    {
      "candidate": "φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd}",
      "coeff_symbol": "\\beta",
      "coefficient": "-2.5015117826407204e-10",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 7.853333291163505e-27,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_144308_0ff96a50/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_144308_0ff96a50/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_144308_0ff96a50/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 8. loop_02  chi2=1727.274391

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "axion", "phi2": null}`
- agent_parameter_sample_index: `486`
- H0_km_s_Mpc: `63.0925891`
- Omega_m0: `0.24709086`
- lambda_H_Lambda_over_H0: `6741.69830162`
- effective_correction_status: `eh_dominated`
- max_relative_effect_to_EH: `5.52690901e-20`
- dominant_correction_term: `∇^{c}R^{ab} · ∇_{c}R_{ab}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · ∇^{c}R^{ab} · ∇_{c}R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-5.7085994719e-05) Λ^{-4} · ∇^{c}R^{ab} · ∇_{c}R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · ∇^{c}R^{ab} · ∇_{c}R_{ab} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -5.7085994719e-05 · Λ^{-4} · ∇^{c}R^{ab} · ∇_{c}R_{ab} ) ] +
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
  }
]
```

### Effective Correction Diagnostics

```json
{
  "effective_correction_status": "eh_dominated",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 5.526909009916111e-20,
  "dominant_correction_term": "∇^{c}R^{ab} · ∇_{c}R_{ab}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 1,
  "correction_term_count": 1,
  "tiny_correction_fraction": 1.0,
  "term_effects": [
    {
      "candidate": "∇^{c}R^{ab} · ∇_{c}R_{ab}",
      "coeff_symbol": "\\beta",
      "coefficient": "-5.708599471936607e-05",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 5.526909009916111e-20,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_143933_3ea2c236/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_143933_3ea2c236/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_143933_3ea2c236/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`
