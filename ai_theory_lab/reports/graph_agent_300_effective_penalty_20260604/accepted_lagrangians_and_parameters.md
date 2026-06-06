# Accepted Lagrangians And Parameters

Each entry is the best chi-square representative of one accepted theory family.
The full accepted-attempt list is preserved in `accepted_summary.json`.
Each displayed entry uses the actual `agent_lagrangians.pkl` object that entered EOM -> Builder -> Solver.

## 1. loop_177  chi2=1638.344047

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "axion", "phi2": null}`
- agent_parameter_sample_index: `649`
- H0_km_s_Mpc: `61.51773911`
- Omega_m0: `0.30326949`
- lambda_H_Lambda_over_H0: `5194.69617704`
- effective_correction_status: `eh_dominated`
- max_relative_effect_to_EH: `7.06611896e-19`
- dominant_correction_term: `φ1 · R^{bcd}_{a} · R^{a}_{bcd}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \beta · R  +  \gamma Λ^{-4} · R^{b}_{a} · R^{cd} · R^{a}_{cbd}  +  \alpha Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd}  +  \delta Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (4.4969921512e-06) Λ^{-4} · R^{b}_{a} · R^{cd} · R^{a}_{cbd}  +  (-2.9084094822e-08) Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd}  +  (-9.1545723056e-09) Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( \beta · R ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · R^{b}_{a} · R^{cd} · R^{a}_{cbd} ) ] +
√(-g) [ M_p² ( \delta · Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( -2.9084094822e-08 · Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 4.4969921512e-06 · Λ^{-4} · R^{b}_{a} · R^{cd} · R^{a}_{cbd} ) ] +
√(-g) [ M_p² ( -9.1545723056e-09 · Λ^{-4} · φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Term Metadata

```json
[
  {
    "coeff_symbol": "\\alpha",
    "coeff_token": "COEFF_0",
    "candidate": "φ1 · R^{bcd}_{a} · R^{a}_{bcd}",
    "mass_dim": 5,
    "lambda_power": -3,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\beta",
    "coeff_token": "COEFF_1",
    "candidate": "R",
    "mass_dim": 2,
    "lambda_power": 0,
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
    "coeff_symbol": "\\delta",
    "coeff_token": "COEFF_3",
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
  "max_relative_effect_to_EH": 7.066118960164622e-19,
  "dominant_correction_term": "φ1 · R^{bcd}_{a} · R^{a}_{bcd}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 3,
  "correction_term_count": 3,
  "tiny_correction_fraction": 1.0,
  "term_effects": [
    {
      "candidate": "φ1 · R^{bcd}_{a} · R^{a}_{bcd}",
      "coeff_symbol": "\\alpha",
      "coefficient": "-2.9084094821907384e-08",
      "lambda_power": -3,
      "sector": "non-minimal",
      "relative_effect_to_EH": 7.066118960164622e-19,
      "effect_class": "tiny"
    },
    {
      "candidate": "R^{b}_{a} · R^{cd} · R^{a}_{cbd}",
      "coeff_symbol": "\\gamma",
      "coefficient": "4.49699215116836e-06",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 1.2351267205245923e-20,
      "effect_class": "tiny"
    },
    {
      "candidate": "φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd}",
      "coeff_symbol": "\\delta",
      "coefficient": "-9.154572305564202e-09",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 7.290866615770126e-23,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260604_214338_fb477553/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260604_214338_fb477553/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260604_214338_fb477553/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 2. loop_97  chi2=1639.029216

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: `10`
- H0_km_s_Mpc: `59.43761936`
- Omega_m0: `0.30204125`
- lambda_H_Lambda_over_H0: `7358.50635915`
- effective_correction_status: `eh_dominated`
- max_relative_effect_to_EH: `6.08573609e-21`
- dominant_correction_term: `∇^{a}∇_{a}φ1 · R`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-3} · ∇^{a}∇_{a}φ1 · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (5.1343559275e-10) Λ^{-3} · ∇^{a}∇_{a}φ1 · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-3} · ∇^{a}∇_{a}φ1 · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 5.1343559275e-10 · Λ^{-3} · ∇^{a}∇_{a}φ1 · R ) ] +
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
    "candidate": "∇^{a}∇_{a}φ1 · R",
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
  "max_relative_effect_to_EH": 6.085736091254625e-21,
  "dominant_correction_term": "∇^{a}∇_{a}φ1 · R",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 1,
  "correction_term_count": 1,
  "tiny_correction_fraction": 1.0,
  "term_effects": [
    {
      "candidate": "∇^{a}∇_{a}φ1 · R",
      "coeff_symbol": "\\beta",
      "coefficient": "5.134355927499868e-10",
      "lambda_power": -3,
      "sector": "non-minimal",
      "relative_effect_to_EH": 6.085736091254625e-21,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260604_205812_e6e5d494/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260604_205812_e6e5d494/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260604_205812_e6e5d494/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 3. loop_263  chi2=1642.105949

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: `329`
- H0_km_s_Mpc: `65.76542192`
- Omega_m0: `0.29678499`
- lambda_H_Lambda_over_H0: `7822.69077905`
- effective_correction_status: `eh_dominated`
- max_relative_effect_to_EH: `2.28864538e-17`
- dominant_correction_term: `φ1 · ∇^{a}∇_{a}R`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \beta Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf}  +  \gamma · R  +  \delta Λ^{-4} · ∇^{c}R^{ab} · ∇_{b}R_{ac}  +  \alpha Λ^{-3} · φ1 · ∇^{a}∇_{a}R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (9.3512524184e-07) Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf}  +  (0.5) · R  +  (4.0711149269e-05) Λ^{-4} · ∇^{c}R^{ab} · ∇_{b}R_{ac}  +  (3.7545045951e-06) Λ^{-3} · φ1 · ∇^{a}∇_{a}R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · Λ^{-3} · φ1 · ∇^{a}∇_{a}R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf} ) ] +
√(-g) [ M_p² ( \gamma · R ) ] +
√(-g) [ M_p² ( \delta · Λ^{-4} · ∇^{c}R^{ab} · ∇_{b}R_{ac} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 3.7545045951e-06 · Λ^{-3} · φ1 · ∇^{a}∇_{a}R ) ] +
√(-g) [ M_p² ( 9.3512524184e-07 · Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf} ) ] +
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 4.0711149269e-05 · Λ^{-4} · ∇^{c}R^{ab} · ∇_{b}R_{ac} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ]
```

### Term Metadata

```json
[
  {
    "coeff_symbol": "\\alpha",
    "coeff_token": "COEFF_0",
    "candidate": "φ1 · ∇^{a}∇_{a}R",
    "mass_dim": 5,
    "lambda_power": -3,
    "sector": "non-minimal"
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
    "candidate": "R",
    "mass_dim": 2,
    "lambda_power": 0,
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
  "max_relative_effect_to_EH": 2.2886453789362108e-17,
  "dominant_correction_term": "φ1 · ∇^{a}∇_{a}R",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 3,
  "correction_term_count": 3,
  "tiny_correction_fraction": 1.0,
  "term_effects": [
    {
      "candidate": "φ1 · ∇^{a}∇_{a}R",
      "coeff_symbol": "\\alpha",
      "coefficient": "3.7545045951490457e-06",
      "lambda_power": -3,
      "sector": "non-minimal",
      "relative_effect_to_EH": 2.2886453789362108e-17,
      "effect_class": "tiny"
    },
    {
      "candidate": "R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf}",
      "coeff_symbol": "\\beta",
      "coefficient": "9.351252418422497e-07",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 4.9943056993442415e-22,
      "effect_class": "tiny"
    },
    {
      "candidate": "∇^{c}R^{ab} · ∇_{b}R_{ac}",
      "coeff_symbol": "\\delta",
      "coefficient": "4.071114926903893e-05",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 2.1742961875422764e-20,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260604_223450_d7eb90a0/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260604_223450_d7eb90a0/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260604_223450_d7eb90a0/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 4. loop_280  chi2=1643.16001

- scalar_config: `both`
- potential_types: `{"phi1": "axion", "phi2": "quadratic"}`
- agent_parameter_sample_index: `522`
- H0_km_s_Mpc: `64.39954469`
- Omega_m0: `0.29568897`
- lambda_H_Lambda_over_H0: `2.37500434e+04`
- effective_correction_status: `eh_only`
- max_relative_effect_to_EH: `0`
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \beta · R )  +  \alpha Λ^{-2} · φ2 · φ2 · φ2 · φ2 · φ2 · φ2  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R )  +  (6.8524438888e-07) Λ^{-2} · φ2 · φ2 · φ2 · φ2 · φ2 · φ2  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1))  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Expanded Terms

```text
√(-g) [ \alpha · Λ^{-2} · φ2 · φ2 · φ2 · φ2 · φ2 · φ2 ] +
√(-g) [ M_p² ( \beta · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ 6.8524438888e-07 · Λ^{-2} · φ2 · φ2 · φ2 · φ2 · φ2 · φ2 ] +
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
    "candidate": "φ2 · φ2 · φ2 · φ2 · φ2 · φ2",
    "mass_dim": 6,
    "lambda_power": -2,
    "sector": "scalar"
  },
  {
    "coeff_symbol": "\\beta",
    "coeff_token": "COEFF_1",
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
- solver output: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260604_224633_c9e286eb/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260604_224633_c9e286eb/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260604_224633_c9e286eb/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 5. loop_108  chi2=1643.910898

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "axion", "phi2": null}`
- agent_parameter_sample_index: `870`
- H0_km_s_Mpc: `66.57673912`
- Omega_m0: `0.31293915`
- lambda_H_Lambda_over_H0: `8875.56807626`
- effective_correction_status: `eh_dominated`
- max_relative_effect_to_EH: `2.93830381e-19`
- dominant_correction_term: `∇^{a}φ1 · ∇^{b}φ1 · R_{ab}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \gamma · R  +  \alpha Λ^{-4} · φ1 · ∇^{a}φ1 · ∇_{a}R  +  \beta Λ^{-4} · ∇^{a}φ1 · ∇^{b}φ1 · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-1.0825793650e-10) Λ^{-4} · φ1 · ∇^{a}φ1 · ∇_{a}R  +  (-5.7365067642e-05) Λ^{-4} · ∇^{a}φ1 · ∇^{b}φ1 · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · Λ^{-4} · φ1 · ∇^{a}φ1 · ∇_{a}R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · ∇^{a}φ1 · ∇^{b}φ1 · R_{ab} ) ] +
√(-g) [ M_p² ( \gamma · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( -1.0825793650e-10 · Λ^{-4} · φ1 · ∇^{a}φ1 · ∇_{a}R ) ] +
√(-g) [ M_p² ( -5.7365067642e-05 · Λ^{-4} · ∇^{a}φ1 · ∇^{b}φ1 · R_{ab} ) ] +
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
    "candidate": "φ1 · ∇^{a}φ1 · ∇_{a}R",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\beta",
    "coeff_token": "COEFF_1",
    "candidate": "∇^{a}φ1 · ∇^{b}φ1 · R_{ab}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\gamma",
    "coeff_token": "COEFF_2",
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
  "effective_correction_status": "eh_dominated",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 2.938303807213998e-19,
  "dominant_correction_term": "∇^{a}φ1 · ∇^{b}φ1 · R_{ab}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 2,
  "correction_term_count": 2,
  "tiny_correction_fraction": 1.0,
  "term_effects": [
    {
      "candidate": "φ1 · ∇^{a}φ1 · ∇_{a}R",
      "coeff_symbol": "\\alpha",
      "coefficient": "-1.0825793649590927e-10",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 5.545094254076237e-25,
      "effect_class": "tiny"
    },
    {
      "candidate": "∇^{a}φ1 · ∇^{b}φ1 · R_{ab}",
      "coeff_symbol": "\\beta",
      "coefficient": "-5.73650676421285e-05",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 2.938303807213998e-19,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260604_210505_ad09b981/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260604_210505_ad09b981/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260604_210505_ad09b981/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 6. loop_277  chi2=1645.445856

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "axion", "phi2": null}`
- agent_parameter_sample_index: `570`
- H0_km_s_Mpc: `66.16535845`
- Omega_m0: `0.32473702`
- lambda_H_Lambda_over_H0: `1.51493453e+04`
- effective_correction_status: `eh_dominated`
- max_relative_effect_to_EH: `4.10867003e-20`
- dominant_correction_term: `φ1 · R^{ab} · R_{ab}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \beta Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf}  +  \gamma · R  +  \alpha Λ^{-3} · φ1 · R^{ab} · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (5.3612698785e-08) Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf}  +  (0.5) · R  +  (3.9650450660e-08) Λ^{-3} · φ1 · R^{ab} · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · Λ^{-3} · φ1 · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf} ) ] +
√(-g) [ M_p² ( \gamma · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 3.9650450660e-08 · Λ^{-3} · φ1 · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( 5.3612698785e-08 · Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf} ) ] +
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
    "candidate": "φ1 · R^{ab} · R_{ab}",
    "mass_dim": 5,
    "lambda_power": -3,
    "sector": "non-minimal"
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
  "effective_correction_status": "eh_dominated",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 4.108670031388896e-20,
  "dominant_correction_term": "φ1 · R^{ab} · R_{ab}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 2,
  "correction_term_count": 2,
  "tiny_correction_fraction": 1.0,
  "term_effects": [
    {
      "candidate": "φ1 · R^{ab} · R_{ab}",
      "coeff_symbol": "\\alpha",
      "coefficient": "3.9650450659890896e-08",
      "lambda_power": -3,
      "sector": "non-minimal",
      "relative_effect_to_EH": 4.108670031388896e-20,
      "effect_class": "tiny"
    },
    {
      "candidate": "R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf}",
      "coeff_symbol": "\\beta",
      "coefficient": "5.361269878456949e-08",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 2.0357395076954045e-24,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260604_224408_c889581b/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260604_224408_c889581b/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260604_224408_c889581b/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 7. loop_132  chi2=1652.906911

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: `780`
- H0_km_s_Mpc: `70.34939326`
- Omega_m0: `0.3172009`
- lambda_H_Lambda_over_H0: `2.05866339e+04`
- effective_correction_status: `eh_dominated`
- max_relative_effect_to_EH: `2.97598371e-20`
- dominant_correction_term: `φ1 · R · R`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def}  +  \gamma · R  +  \delta Λ^{-4} · R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh}  +  \beta Λ^{-3} · φ1 · R · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (-4.6401798265e-10) Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def}  +  (0.5) · R  +  (-1.5741298759e-06) Λ^{-4} · R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh}  +  (-1.0029414318e-07) Λ^{-3} · φ1 · R · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def} ) ] +
√(-g) [ M_p² ( \beta · Λ^{-3} · φ1 · R · R ) ] +
√(-g) [ M_p² ( \gamma · R ) ] +
√(-g) [ M_p² ( \delta · Λ^{-4} · R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( -4.6401798265e-10 · Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def} ) ] +
√(-g) [ M_p² ( -1.0029414318e-07 · Λ^{-3} · φ1 · R · R ) ] +
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -1.5741298759e-06 · Λ^{-4} · R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ]
```

### Term Metadata

```json
[
  {
    "coeff_symbol": "\\alpha",
    "coeff_token": "COEFF_0",
    "candidate": "R_{ab} · R^{adef} · R^{b}_{def}",
    "mass_dim": 6,
    "lambda_power": -4,
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
    "coeff_symbol": "\\gamma",
    "coeff_token": "COEFF_2",
    "candidate": "R",
    "mass_dim": 2,
    "lambda_power": 0,
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
  "max_relative_effect_to_EH": 2.975983714869213e-20,
  "dominant_correction_term": "φ1 · R · R",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 3,
  "correction_term_count": 3,
  "tiny_correction_fraction": 1.0,
  "term_effects": [
    {
      "candidate": "R_{ab} · R^{adef} · R^{b}_{def}",
      "coeff_symbol": "\\alpha",
      "coefficient": "-4.6401798265436894e-10",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 5.166821269416179e-27,
      "effect_class": "tiny"
    },
    {
      "candidate": "φ1 · R · R",
      "coeff_symbol": "\\beta",
      "coefficient": "-1.0029414317546424e-07",
      "lambda_power": -3,
      "sector": "non-minimal",
      "relative_effect_to_EH": 2.975983714869213e-20,
      "effect_class": "tiny"
    },
    {
      "candidate": "R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh}",
      "coeff_symbol": "\\delta",
      "coefficient": "-1.5741298758924404e-06",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 1.752787182311141e-23,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260604_211920_498c52e8/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260604_211920_498c52e8/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260604_211920_498c52e8/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 8. loop_150  chi2=1653.193319

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: `639`
- H0_km_s_Mpc: `63.52873552`
- Omega_m0: `0.31565502`
- lambda_H_Lambda_over_H0: `1.66440871e+04`
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
- solver output: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260604_212849_73cfd00d/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260604_212849_73cfd00d/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260604_212849_73cfd00d/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 9. loop_59  chi2=1655.124543

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "axion", "phi2": null}`
- agent_parameter_sample_index: `531`
- H0_km_s_Mpc: `66.51223834`
- Omega_m0: `0.26095624`
- lambda_H_Lambda_over_H0: `5.40670096e+04`
- effective_correction_status: `eh_dominated`
- max_relative_effect_to_EH: `1.86259999e-27`
- dominant_correction_term: `φ1 · ∇^{a}∇_{a}φ1 · R`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \beta · R  +  \alpha Λ^{-4} · φ1 · ∇^{a}∇_{a}φ1 · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-3.5085674790e-09) Λ^{-4} · φ1 · ∇^{a}∇_{a}φ1 · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · Λ^{-4} · φ1 · ∇^{a}∇_{a}φ1 · R ) ] +
√(-g) [ M_p² ( \beta · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( -3.5085674790e-09 · Λ^{-4} · φ1 · ∇^{a}∇_{a}φ1 · R ) ] +
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
    "candidate": "φ1 · ∇^{a}∇_{a}φ1 · R",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\beta",
    "coeff_token": "COEFF_1",
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
  "effective_correction_status": "eh_dominated",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 1.8625999890440632e-27,
  "dominant_correction_term": "φ1 · ∇^{a}∇_{a}φ1 · R",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 1,
  "correction_term_count": 1,
  "tiny_correction_fraction": 1.0,
  "term_effects": [
    {
      "candidate": "φ1 · ∇^{a}∇_{a}φ1 · R",
      "coeff_symbol": "\\alpha",
      "coefficient": "-3.5085674789591123e-09",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 1.8625999890440632e-27,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260604_203953_d152ef32/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260604_203953_d152ef32/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260604_203953_d152ef32/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 10. loop_118  chi2=1666.311808

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "axion", "phi2": null}`
- agent_parameter_sample_index: `987`
- H0_km_s_Mpc: `71.74863086`
- Omega_m0: `0.27105274`
- lambda_H_Lambda_over_H0: `6757.89024998`
- effective_correction_status: `eh_dominated`
- max_relative_effect_to_EH: `9.06107625e-20`
- dominant_correction_term: `R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha Λ^{-4} · ∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}  +  \beta Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf}  +  \gamma · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (-5.0711388364e-06) Λ^{-4} · ∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}  +  (9.4491844624e-05) Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf}  +  (0.5) · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · Λ^{-4} · ∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf} ) ] +
√(-g) [ M_p² ( \gamma · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( -5.0711388364e-06 · Λ^{-4} · ∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( 9.4491844624e-05 · Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf} ) ] +
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
    "candidate": "∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}",
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
  "effective_correction_status": "eh_dominated",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 9.061076250701233e-20,
  "dominant_correction_term": "R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 2,
  "correction_term_count": 2,
  "tiny_correction_fraction": 1.0,
  "term_effects": [
    {
      "candidate": "∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}",
      "coeff_symbol": "\\alpha",
      "coefficient": "-5.071138836410729e-06",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 4.862850953698715e-21,
      "effect_class": "tiny"
    },
    {
      "candidate": "R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf}",
      "coeff_symbol": "\\beta",
      "coefficient": "9.449184462390338e-05",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 9.061076250701233e-20,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260604_211017_8c44f1f9/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260604_211017_8c44f1f9/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260604_211017_8c44f1f9/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 11. loop_180  chi2=1668.758591

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: `49`
- H0_km_s_Mpc: `57.68621948`
- Omega_m0: `0.34256795`
- lambda_H_Lambda_over_H0: `1.68117583e+04`
- effective_correction_status: `eh_dominated`
- max_relative_effect_to_EH: `2.19208348e-22`
- dominant_correction_term: `∇^{c}R^{ab} · ∇_{c}R_{ab}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha Λ^{-4} · ∇^{c}R^{ab} · ∇_{c}R_{ab}  +  \beta Λ^{-4} · R · R^{ab} · R_{ab}  +  \gamma Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{fdh}  +  \delta · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (8.7554736770e-06) Λ^{-4} · ∇^{c}R^{ab} · ∇_{c}R_{ab}  +  (-1.7354265753e-07) Λ^{-4} · R · R^{ab} · R_{ab}  +  (1.7420764638e-07) Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{fdh}  +  (0.5) · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · Λ^{-4} · ∇^{c}R^{ab} · ∇_{c}R_{ab} ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · R · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{fdh} ) ] +
√(-g) [ M_p² ( \delta · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 8.7554736770e-06 · Λ^{-4} · ∇^{c}R^{ab} · ∇_{c}R_{ab} ) ] +
√(-g) [ M_p² ( -1.7354265753e-07 · Λ^{-4} · R · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( 1.7420764638e-07 · Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{fdh} ) ] +
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
    "candidate": "∇^{c}R^{ab} · ∇_{c}R_{ab}",
    "mass_dim": 6,
    "lambda_power": -4,
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
    "candidate": "R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{fdh}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\delta",
    "coeff_token": "COEFF_3",
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
  "effective_correction_status": "eh_dominated",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 2.1920834827113346e-22,
  "dominant_correction_term": "∇^{c}R^{ab} · ∇_{c}R_{ab}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 3,
  "correction_term_count": 3,
  "tiny_correction_fraction": 1.0,
  "term_effects": [
    {
      "candidate": "∇^{c}R^{ab} · ∇_{c}R_{ab}",
      "coeff_symbol": "\\alpha",
      "coefficient": "8.755473676983667e-06",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 2.1920834827113346e-22,
      "effect_class": "tiny"
    },
    {
      "candidate": "R · R^{ab} · R_{ab}",
      "coeff_symbol": "\\beta",
      "coefficient": "-1.7354265753060696e-07",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 4.3449390307542e-24,
      "effect_class": "tiny"
    },
    {
      "candidate": "R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{fdh}",
      "coeff_symbol": "\\gamma",
      "coefficient": "1.742076463801044e-07",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 4.361588170788766e-24,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260604_214544_de4536fa/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260604_214544_de4536fa/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260604_214544_de4536fa/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 12. loop_297  chi2=1678.718943

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "axion", "phi2": null}`
- agent_parameter_sample_index: `614`
- H0_km_s_Mpc: `65.04577776`
- Omega_m0: `0.28315389`
- lambda_H_Lambda_over_H0: `2.05732088e+04`
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
- solver output: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260604_225633_a01defd4/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260604_225633_a01defd4/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260604_225633_a01defd4/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 13. loop_243  chi2=1679.835491

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "axion", "phi2": null}`
- agent_parameter_sample_index: `78`
- H0_km_s_Mpc: `71.13014924`
- Omega_m0: `0.32733098`
- lambda_H_Lambda_over_H0: `2316.0074619`
- effective_correction_status: `eh_dominated`
- max_relative_effect_to_EH: `2.61902652e-19`
- dominant_correction_term: `R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha Λ^{-4} · R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh}  +  \beta · R  +  \gamma Λ^{-4} · R · R · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (-3.7676427616e-06) Λ^{-4} · R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh}  +  (0.5) · R  +  (-1.2875331450e-06) Λ^{-4} · R · R · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · Λ^{-4} · R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh} ) ] +
√(-g) [ M_p² ( \beta · R ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · R · R · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( -3.7676427616e-06 · Λ^{-4} · R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh} ) ] +
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -1.2875331450e-06 · Λ^{-4} · R · R · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
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
    "candidate": "R",
    "mass_dim": 2,
    "lambda_power": 0,
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
  "max_relative_effect_to_EH": 2.6190265185065565e-19,
  "dominant_correction_term": "R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 2,
  "correction_term_count": 2,
  "tiny_correction_fraction": 1.0,
  "term_effects": [
    {
      "candidate": "R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh}",
      "coeff_symbol": "\\alpha",
      "coefficient": "-3.7676427616392466e-06",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 2.6190265185065565e-19,
      "effect_class": "tiny"
    },
    {
      "candidate": "R · R · R",
      "coeff_symbol": "\\gamma",
      "coefficient": "-1.2875331450097341e-06",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 8.95011460367197e-20,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260604_222215_9e492e2f/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260604_222215_9e492e2f/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260604_222215_9e492e2f/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 14. loop_143  chi2=1680.463807

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: `494`
- H0_km_s_Mpc: `66.25766145`
- Omega_m0: `0.27957952`
- lambda_H_Lambda_over_H0: `4.45785519e+04`
- effective_correction_status: `eh_dominated`
- max_relative_effect_to_EH: `5.62260231e-24`
- dominant_correction_term: `φ1 · R^{bcd}_{a} · R^{a}_{bcd}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \gamma · R  +  \beta Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd} )  +  \alpha Λ^{2} · φ1 · φ1  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-2.9571550311e-10) Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd} )  +  (-1.1238187818e-09) Λ^{2} · φ1 · φ1  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Expanded Terms

```text
√(-g) [ \alpha · Λ^{2} · φ1 · φ1 ] +
√(-g) [ M_p² ( \beta · Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( \gamma · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ -1.1238187818e-09 · Λ^{2} · φ1 · φ1 ] +
√(-g) [ M_p² ( -2.9571550311e-10 · Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
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
    "candidate": "φ1 · φ1",
    "mass_dim": 2,
    "lambda_power": 2,
    "sector": "scalar"
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
  "effective_correction_status": "eh_dominated",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 5.6226023117205095e-24,
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
      "coefficient": "-2.9571550311093814e-10",
      "lambda_power": -3,
      "sector": "non-minimal",
      "relative_effect_to_EH": 5.6226023117205095e-24,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260604_212511_86de306d/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260604_212511_86de306d/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260604_212511_86de306d/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 15. loop_200  chi2=1691.766732

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: `344`
- H0_km_s_Mpc: `59.11760212`
- Omega_m0: `0.200111`
- lambda_H_Lambda_over_H0: `3.01895901e+04`
- effective_correction_status: `eh_dominated`
- max_relative_effect_to_EH: `8.01774861e-26`
- dominant_correction_term: `R_{ab} · R^{adef} · R^{b}_{def}`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (3.3300542178e-08) Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 3.3300542178e-08 · Λ^{-4} · R_{ab} · R^{adef} · R^{b}_{def} ) ] +
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
  "max_relative_effect_to_EH": 8.017748606497641e-26,
  "dominant_correction_term": "R_{ab} · R^{adef} · R^{b}_{def}",
  "active_correction_terms": 0,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 1,
  "correction_term_count": 1,
  "tiny_correction_fraction": 1.0,
  "term_effects": [
    {
      "candidate": "R_{ab} · R^{adef} · R^{b}_{def}",
      "coeff_symbol": "\\beta",
      "coefficient": "3.330054217844082e-08",
      "lambda_power": -4,
      "sector": "gravity",
      "relative_effect_to_EH": 8.017748606497641e-26,
      "effect_class": "tiny"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260604_215623_73144500/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260604_215623_73144500/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260604_215623_73144500/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 16. loop_16  chi2=1756.864092

- scalar_config: `both`
- potential_types: `{"phi1": "quadratic", "phi2": "axion"}`
- agent_parameter_sample_index: `490`
- H0_km_s_Mpc: `64.62124256`
- Omega_m0: `0.35224905`
- lambda_H_Lambda_over_H0: `6313.8840642`
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
- solver output: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260604_202134_a45a6dae/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260604_202134_a45a6dae/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260604_202134_a45a6dae/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 17. loop_11_expanded  chi2=9434.007717

- scalar_config: `phi2_only`
- potential_types: `{"phi1": null, "phi2": "axion"}`
- agent_parameter_sample_index: `684`
- H0_km_s_Mpc: `58.81523479`
- Omega_m0: `0.24499998`
- lambda_H_Lambda_over_H0: `3.12222434e+04`
- effective_correction_status: `unclear`
- max_relative_effect_to_EH: ``
- dominant_correction_term: ``

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha Λ^{-4} · R^{ab} · R^{d}_{a} · R_{bd}  +  \delta Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf}  +  \beta Λ^{-4} · φ2 · φ2 · φ2 · φ2 · R  +  \gamma Λ^{-4} · φ2 · φ2 · R^{bcd}_{a} · R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (-4.2090267042e-05) Λ^{-4} · R^{ab} · R^{d}_{a} · R_{bd}  +  (3.9897793970e-06) Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf}  +  (-8.0256620546e-05) Λ^{-4} · φ2 · φ2 · φ2 · φ2 · R  +  (1.5020317537e-08) Λ^{-4} · φ2 · φ2 · R^{bcd}_{a} · R^{a}_{bcd} )  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · Λ^{-4} · R^{ab} · R^{d}_{a} · R_{bd} ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · φ2 · φ2 · φ2 · φ2 · R ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · φ2 · φ2 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( \delta · Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( -4.2090267042e-05 · Λ^{-4} · R^{ab} · R^{d}_{a} · R_{bd} ) ] +
√(-g) [ M_p² ( -8.0256620546e-05 · Λ^{-4} · φ2 · φ2 · φ2 · φ2 · R ) ] +
√(-g) [ M_p² ( 1.5020317537e-08 · Λ^{-4} · φ2 · φ2 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( 3.9897793970e-06 · Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Term Metadata

```json
[
  {
    "coeff_symbol": "\\alpha",
    "coeff_token": "COEFF_0",
    "candidate": "R^{ab} · R^{d}_{a} · R_{bd}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\beta",
    "coeff_token": "COEFF_1",
    "candidate": "φ2 · φ2 · φ2 · φ2 · R",
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
    "candidate": "R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "gravity"
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
- solver output: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260604_201831_ff34143e/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260604_201831_ff34143e/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260604_201831_ff34143e/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`
