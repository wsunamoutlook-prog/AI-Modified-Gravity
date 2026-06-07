# Accepted Lagrangians Full

Complete dimension-balanced Lagrangians, best-fit coefficient substitutions, metadata, and Solver paths.
Only the best chi-square representative from each accepted theory family is shown for human inspection.
The full accepted-attempt list is preserved in `accepted_summary.json`.

## 1. loop_23  chi2=1638.598412

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: `896`
- H0_km_s_Mpc: `57.1694547`
- Omega_m0: `0.30379696`
- lambda_H_Lambda_over_H0: `8742.78792958`
- effective_correction_status: `eh_dominated`
- max_relative_effect_to_EH: `4.06575643e-13`
- dominant_correction_term: `∇^{a}∇_{a}R`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-2} · ∇^{a}∇_{a}R  +  \gamma Λ^{-4} · R^{b}_{a} · R^{cd} · R^{a}_{cbd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-1.5538577212e-05) Λ^{-2} · ∇^{a}∇_{a}R  +  (-9.9716666086e-06) Λ^{-4} · R^{b}_{a} · R^{cd} · R^{a}_{cbd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-2} · ∇^{a}∇_{a}R ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · R^{b}_{a} · R^{cd} · R^{a}_{cbd} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -1.5538577212e-05 · Λ^{-2} · ∇^{a}∇_{a}R ) ] +
√(-g) [ M_p² ( -9.9716666086e-06 · Λ^{-4} · R^{b}_{a} · R^{cd} · R^{a}_{cbd} ) ] +
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
    "candidate": "∇^{a}∇_{a}R",
    "mass_dim": 4,
    "lambda_power": -2,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\gamma",
    "coeff_token": "COEFF_2",
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
  "max_relative_effect_to_EH": 4.065756432979204e-13,
  "dominant_correction_term": "∇^{a}∇_{a}R",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 2,
  "correction_term_count": 2,
  "tiny_correction_fraction": 1.0,
  "term_effects": [
    {
      "candidate": "∇^{a}∇_{a}R",
      "coeff_symbol": "\\beta",
      "coefficient": "-1.5538577212309392e-05",
      "lambda_power": -2,
      "sector": "gravity",
      "relative_effect_to_EH": 4.065756432979204e-13,
      "effect_class": "tiny"
    },
    {
      "candidate": "R^{b}_{a} · R^{cd} · R^{a}_{cbd}",
      "coeff_symbol": "\\gamma",
      "coefficient": "-9.971666608553604e-06",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 3.413484770672544e-21,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_145110_8e857bfa/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_145110_8e857bfa/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_145110_8e857bfa/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 2. loop_96  chi2=1639.952934

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "axion", "phi2": null}`
- agent_parameter_sample_index: `963`
- H0_km_s_Mpc: `58.53487373`
- Omega_m0: `0.29532473`
- lambda_H_Lambda_over_H0: `6312.18919192`
- effective_correction_status: `eh_dominated`
- max_relative_effect_to_EH: `2.17393878e-17`
- dominant_correction_term: `R^{bcd}_{a} · R^{a}_{bcd}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd}  +  \gamma Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{fdh} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (4.3308917447e-10) Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd}  +  (2.6124980890e-08) Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{fdh} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{fdh} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 4.3308917447e-10 · Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( 2.6124980890e-08 · Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{fdh} ) ] +
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
  "max_relative_effect_to_EH": 2.1739387775268482e-17,
  "dominant_correction_term": "R^{bcd}_{a} · R^{a}_{bcd}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 2,
  "correction_term_count": 2,
  "tiny_correction_fraction": 1.0,
  "term_effects": [
    {
      "candidate": "R^{bcd}_{a} · R^{a}_{bcd}",
      "coeff_symbol": "\\beta",
      "coefficient": "4.330891744702922e-10",
      "lambda_power": -2,
      "sector": "gravity",
      "relative_effect_to_EH": 2.1739387775268482e-17,
      "effect_class": "tiny"
    },
    {
      "candidate": "R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{fdh}",
      "coeff_symbol": "\\gamma",
      "coefficient": "2.6124980890441464e-08",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 3.2912884672813115e-23,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_151122_8a8f4876/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_151122_8a8f4876/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_151122_8a8f4876/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 3. loop_01  chi2=1640.045401

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
- solver output: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_144458_d68cefb1/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_144458_d68cefb1/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_144458_d68cefb1/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 4. loop_63  chi2=1641.015645

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "axion", "phi2": null}`
- agent_parameter_sample_index: `386`
- H0_km_s_Mpc: `64.90587936`
- Omega_m0: `0.30086024`
- lambda_H_Lambda_over_H0: `1.28644016e+04`
- effective_correction_status: `eh_dominated`
- max_relative_effect_to_EH: `7.22853881e-13`
- dominant_correction_term: `R^{bcd}_{a} · R^{a}_{bcd}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd}  +  \gamma Λ^{-2} · ∇^{a}∇_{a}R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-5.9813566851e-05) Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd}  +  (-1.2083554224e-10) Λ^{-2} · ∇^{a}∇_{a}R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
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
√(-g) [ M_p² ( -5.9813566851e-05 · Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( -1.2083554224e-10 · Λ^{-2} · ∇^{a}∇_{a}R ) ] +
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
  "effective_correction_status": "eh_dominated",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 7.228538812719648e-13,
  "dominant_correction_term": "R^{bcd}_{a} · R^{a}_{bcd}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 2,
  "correction_term_count": 2,
  "tiny_correction_fraction": 1.0,
  "term_effects": [
    {
      "candidate": "R^{bcd}_{a} · R^{a}_{bcd}",
      "coeff_symbol": "\\beta",
      "coefficient": "-5.981356685126718e-05",
      "lambda_power": -2,
      "sector": "gravity",
      "relative_effect_to_EH": 7.228538812719648e-13,
      "effect_class": "tiny"
    },
    {
      "candidate": "∇^{a}∇_{a}R",
      "coeff_symbol": "\\gamma",
      "coefficient": "-1.20835542235697e-10",
      "lambda_power": -2,
      "sector": "gravity",
      "relative_effect_to_EH": 1.4603115195900666e-18,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_150154_3d19a615/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_150154_3d19a615/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_150154_3d19a615/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 5. loop_80  chi2=1641.144276

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: `248`
- H0_km_s_Mpc: `66.720513`
- Omega_m0: `0.29774898`
- lambda_H_Lambda_over_H0: `3357.26551228`
- effective_correction_status: `eh_dominated`
- max_relative_effect_to_EH: `1.18743825e-16`
- dominant_correction_term: `R^{bcd}_{a} · R^{a}_{bcd}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd}  +  \gamma Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-6.6919458256e-10) Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd}  +  (2.0791458775e-05) Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -6.6919458256e-10 · Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( 2.0791458775e-05 · Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def} ) ] +
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
  }
]
```

### Effective Correction Diagnostics

```json
{
  "effective_correction_status": "eh_dominated",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 1.1874382484287354e-16,
  "dominant_correction_term": "R^{bcd}_{a} · R^{a}_{bcd}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 2,
  "correction_term_count": 2,
  "tiny_correction_fraction": 1.0,
  "term_effects": [
    {
      "candidate": "R^{bcd}_{a} · R^{a}_{bcd}",
      "coeff_symbol": "\\beta",
      "coefficient": "-6.691945825591573e-10",
      "lambda_power": -2,
      "sector": "gravity",
      "relative_effect_to_EH": 1.1874382484287354e-16,
      "effect_class": "tiny"
    },
    {
      "candidate": "R_{ab} · R^{adef} · R^{b}_{def}",
      "coeff_symbol": "\\gamma",
      "coefficient": "2.0791458774906775e-05",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 3.2731974221306283e-19,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_150638_9f97ad57/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_150638_9f97ad57/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_150638_9f97ad57/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 6. loop_30  chi2=1642.079229

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: `294`
- H0_km_s_Mpc: `59.37780202`
- Omega_m0: `0.30783336`
- lambda_H_Lambda_over_H0: `3.35112651e+04`
- effective_correction_status: `eh_dominated`
- max_relative_effect_to_EH: `9.96457318e-19`
- dominant_correction_term: `∇^{a}∇_{a}R`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-2} · ∇^{a}∇_{a}R  +  \gamma Λ^{-4} · ∇^{a}∇_{a}R · R^{c}_{c} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (5.5951322129e-10) Λ^{-2} · ∇^{a}∇_{a}R  +  (8.2258858023e-07) Λ^{-4} · ∇^{a}∇_{a}R · R^{c}_{c} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-2} · ∇^{a}∇_{a}R ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · ∇^{a}∇_{a}R · R^{c}_{c} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 5.5951322129e-10 · Λ^{-2} · ∇^{a}∇_{a}R ) ] +
√(-g) [ M_p² ( 8.2258858023e-07 · Λ^{-4} · ∇^{a}∇_{a}R · R^{c}_{c} ) ] +
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
    "candidate": "∇^{a}∇_{a}R",
    "mass_dim": 4,
    "lambda_power": -2,
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
  "max_relative_effect_to_EH": 9.964573182542347e-19,
  "dominant_correction_term": "∇^{a}∇_{a}R",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 2,
  "correction_term_count": 2,
  "tiny_correction_fraction": 1.0,
  "term_effects": [
    {
      "candidate": "∇^{a}∇_{a}R",
      "coeff_symbol": "\\beta",
      "coefficient": "5.595132212871505e-10",
      "lambda_power": -2,
      "sector": "gravity",
      "relative_effect_to_EH": 9.964573182542347e-19,
      "effect_class": "tiny"
    },
    {
      "candidate": "∇^{a}∇_{a}R · R^{c}_{c}",
      "coeff_symbol": "\\gamma",
      "coefficient": "8.225885802328274e-07",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 1.304515896953017e-24,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_145304_3b45c371/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_145304_3b45c371/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_145304_3b45c371/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 7. loop_81  chi2=1645.488927

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "axion", "phi2": null}`
- agent_parameter_sample_index: `104`
- H0_km_s_Mpc: `71.57539293`
- Omega_m0: `0.30495798`
- lambda_H_Lambda_over_H0: `2.33635882e+04`
- effective_correction_status: `eh_dominated`
- max_relative_effect_to_EH: `2.49237027e-16`
- dominant_correction_term: `R^{bcd}_{a} · R^{a}_{bcd}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd}  +  \gamma Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (6.8023919308e-08) Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd}  +  (4.6172527669e-07) Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 6.8023919308e-08 · Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( 4.6172527669e-07 · Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def} ) ] +
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
  "effective_correction_status": "eh_dominated",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 2.492370269743005e-16,
  "dominant_correction_term": "R^{bcd}_{a} · R^{a}_{bcd}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 2,
  "correction_term_count": 2,
  "tiny_correction_fraction": 1.0,
  "term_effects": [
    {
      "candidate": "R^{bcd}_{a} · R^{a}_{bcd}",
      "coeff_symbol": "\\beta",
      "coefficient": "6.802391930763376e-08",
      "lambda_power": -2,
      "sector": "gravity",
      "relative_effect_to_EH": 2.492370269743005e-16,
      "effect_class": "tiny"
    },
    {
      "candidate": "R_{ab} · R^{adef} · R^{b}_{def}",
      "coeff_symbol": "\\gamma",
      "coefficient": "4.6172527669467815e-07",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 3.0992419157043188e-24,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_150655_629b206e/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_150655_629b206e/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_150655_629b206e/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 8. loop_13  chi2=1649.162372

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "axion", "phi2": null}`
- agent_parameter_sample_index: `986`
- H0_km_s_Mpc: `63.26019701`
- Omega_m0: `0.32641743`
- lambda_H_Lambda_over_H0: `4413.51745838`
- effective_correction_status: `eh_dominated`
- max_relative_effect_to_EH: `6.48979887e-16`
- dominant_correction_term: `φ1 · R^{bcd}_{a} · R^{a}_{bcd}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (6.8321783104e-06) Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
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
√(-g) [ M_p² ( 6.8321783104e-06 · Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
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
  "max_relative_effect_to_EH": 6.489798865984903e-16,
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
      "coefficient": "6.832178310402819e-06",
      "lambda_power": -3,
      "sector": "non-minimal",
      "relative_effect_to_EH": 6.489798865984903e-16,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_144931_d3a1012a/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_144931_d3a1012a/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_144931_d3a1012a/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 9. loop_55  chi2=1651.159287

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "axion", "phi2": null}`
- agent_parameter_sample_index: `895`
- H0_km_s_Mpc: `57.61627208`
- Omega_m0: `0.29512684`
- lambda_H_Lambda_over_H0: `1.01553926e+04`
- effective_correction_status: `eh_dominated`
- max_relative_effect_to_EH: `1.90861177e-16`
- dominant_correction_term: `∇^{a}∇_{a}R`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-2} · ∇^{a}∇_{a}R  +  \gamma Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (9.8419472745e-09) Λ^{-2} · ∇^{a}∇_{a}R  +  (2.6023383035e-05) Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-2} · ∇^{a}∇_{a}R ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 9.8419472745e-09 · Λ^{-2} · ∇^{a}∇_{a}R ) ] +
√(-g) [ M_p² ( 2.6023383035e-05 · Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def} ) ] +
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
    "candidate": "∇^{a}∇_{a}R",
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
  "max_relative_effect_to_EH": 1.9086117663447293e-16,
  "dominant_correction_term": "∇^{a}∇_{a}R",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 2,
  "correction_term_count": 2,
  "tiny_correction_fraction": 1.0,
  "term_effects": [
    {
      "candidate": "∇^{a}∇_{a}R",
      "coeff_symbol": "\\beta",
      "coefficient": "9.841947274501575e-09",
      "lambda_power": -2,
      "sector": "gravity",
      "relative_effect_to_EH": 1.9086117663447293e-16,
      "effect_class": "tiny"
    },
    {
      "candidate": "R_{ab} · R^{adef} · R^{b}_{def}",
      "coeff_symbol": "\\gamma",
      "coefficient": "2.602338303502759e-05",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 4.893356804641042e-21,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_150000_8cd7cabb/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_150000_8cd7cabb/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_150000_8cd7cabb/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 10. loop_07  chi2=1657.023856

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
- solver output: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_144824_2e612024/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_144824_2e612024/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_144824_2e612024/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 11. loop_74  chi2=1667.751076

- scalar_config: `both`
- potential_types: `{"phi1": "quadratic", "phi2": "axion"}`
- agent_parameter_sample_index: `737`
- H0_km_s_Mpc: `72.66626976`
- Omega_m0: `0.2742044`
- lambda_H_Lambda_over_H0: `8240.62453741`
- effective_correction_status: `eh_dominated`
- max_relative_effect_to_EH: `1.61064624e-13`
- dominant_correction_term: `R^{bcd}_{a} · R^{a}_{bcd}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd}  +  \gamma Λ^{-2} · ∇^{a}∇_{a}R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-5.4687796048e-06) Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd}  +  (-1.5165478244e-09) Λ^{-2} · ∇^{a}∇_{a}R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-2} · ∇^{a}∇_{a}R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -5.4687796048e-06 · Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( -1.5165478244e-09 · Λ^{-2} · ∇^{a}∇_{a}R ) ] +
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
  "max_relative_effect_to_EH": 1.610646239205202e-13,
  "dominant_correction_term": "R^{bcd}_{a} · R^{a}_{bcd}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 2,
  "correction_term_count": 2,
  "tiny_correction_fraction": 1.0,
  "term_effects": [
    {
      "candidate": "R^{bcd}_{a} · R^{a}_{bcd}",
      "coeff_symbol": "\\beta",
      "coefficient": "-5.468779604834786e-06",
      "lambda_power": -2,
      "sector": "gravity",
      "relative_effect_to_EH": 1.610646239205202e-13,
      "effect_class": "tiny"
    },
    {
      "candidate": "∇^{a}∇_{a}R",
      "coeff_symbol": "\\gamma",
      "coefficient": "-1.5165478244317147e-09",
      "lambda_power": -2,
      "sector": "gravity",
      "relative_effect_to_EH": 4.466484712304593e-17,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_150446_152e2be9/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_150446_152e2be9/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_150446_152e2be9/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 12. loop_08  chi2=1674.136138

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
- solver output: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_144837_8d65b0ee/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_144837_8d65b0ee/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_144837_8d65b0ee/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 13. loop_04_expanded  chi2=1688.147231

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
- solver output: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_144622_81806b62/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_144622_81806b62/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_144622_81806b62/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 14. loop_06  chi2=1701.282902

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
- solver output: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_144811_533c58c9/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_144811_533c58c9/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260606_144811_533c58c9/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`
