# Accepted Lagrangians Full

Complete dimension-balanced Lagrangians, best-fit coefficient substitutions, metadata, and Solver paths.
Only the best chi-square representative from each accepted theory family is shown for human inspection.
The full accepted-attempt list is preserved in `accepted_summary.json`.

## 1. loop_75  chi2=1640.9734

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: `275`
- H0_km_s_Mpc: `63.54786351`
- Omega_m0: `0.3071309`
- lambda_H_Lambda_over_H0: `2824.2083226`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-3} · φ1 · R^{ab} · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-1.0784201280e-07) Λ^{-3} · φ1 · R^{ab} · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
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
√(-g) [ M_p² ( -1.0784201280e-07 · Λ^{-3} · φ1 · R^{ab} · R_{ab} ) ] +
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

### Output Paths

- proposal: ``
- solver output: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_212949_49e2ca04/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_212949_49e2ca04/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_212949_49e2ca04/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 2. loop_199  chi2=1649.567186

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: `355`
- H0_km_s_Mpc: `69.90522639`
- Omega_m0: `0.22825558`
- lambda_H_Lambda_over_H0: `1.22101163e+04`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha Λ^{-2} · R^{ab} · R_{ab}  +  \beta · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (6.4317441261e-08) Λ^{-2} · R^{ab} · R_{ab}  +  (0.5) · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · Λ^{-2} · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( \beta · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 6.4317441261e-08 · Λ^{-2} · R^{ab} · R_{ab} ) ] +
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
    "candidate": "R^{ab} · R_{ab}",
    "mass_dim": 4,
    "lambda_power": -2,
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

### Output Paths

- proposal: ``
- solver output: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_223019_268c403d/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_223019_268c403d/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_223019_268c403d/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 3. loop_237  chi2=1650.673035

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "axion", "phi2": null}`
- agent_parameter_sample_index: `850`
- H0_km_s_Mpc: `68.85520078`
- Omega_m0: `0.33248304`
- lambda_H_Lambda_over_H0: `8355.4063537`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha Λ^{-4} · R^{ab} · R^{d}_{a} · R_{bd}  +  \beta · R  +  \gamma Λ^{-4} · φ1 · φ1 · R · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (2.7087347023e-10) Λ^{-4} · R^{ab} · R^{d}_{a} · R_{bd}  +  (0.5) · R  +  (-6.2664112409e-10) Λ^{-4} · φ1 · φ1 · R · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · Λ^{-4} · R^{ab} · R^{d}_{a} · R_{bd} ) ] +
√(-g) [ M_p² ( \beta · R ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · φ1 · φ1 · R · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 2.7087347023e-10 · Λ^{-4} · R^{ab} · R^{d}_{a} · R_{bd} ) ] +
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -6.2664112409e-10 · Λ^{-4} · φ1 · φ1 · R · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
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
    "candidate": "R",
    "mass_dim": 2,
    "lambda_power": 0,
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
    "candidate": "-m_1² f_1² (1 - cos(φ1/f_1))",
    "mass_dim": 4,
    "lambda_power": 0,
    "fixed": true,
    "sector": "matter",
    "potential_type": "axion"
  }
]
```

### Output Paths

- proposal: ``
- solver output: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_225237_a67ea8db/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_225237_a67ea8db/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_225237_a67ea8db/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 4. loop_133  chi2=1658.592046

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "axion", "phi2": null}`
- agent_parameter_sample_index: `612`
- H0_km_s_Mpc: `62.34552289`
- Omega_m0: `0.29422905`
- lambda_H_Lambda_over_H0: `6.56318205e+04`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · φ1 · ∇^{a}φ1 · ∇_{a}R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-2.5870466148e-10) Λ^{-4} · φ1 · ∇^{a}φ1 · ∇_{a}R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
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
√(-g) [ M_p² ( -2.5870466148e-10 · Λ^{-4} · φ1 · ∇^{a}φ1 · ∇_{a}R ) ] +
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

### Output Paths

- proposal: ``
- solver output: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_215622_e499b91a/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_215622_e499b91a/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_215622_e499b91a/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 5. loop_66  chi2=1659.11236

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: `572`
- H0_km_s_Mpc: `66.13951613`
- Omega_m0: `0.26748636`
- lambda_H_Lambda_over_H0: `2403.02719243`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \beta · R )  +  \alpha Λ^{1} · ∇^{a}∇_{a}φ1  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R )  +  (-1.7930795665e-07) Λ^{1} · ∇^{a}∇_{a}φ1  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Expanded Terms

```text
√(-g) [ \alpha · Λ^{1} · ∇^{a}∇_{a}φ1 ] +
√(-g) [ M_p² ( \beta · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ -1.7930795665e-07 · Λ^{1} · ∇^{a}∇_{a}φ1 ] +
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
    "candidate": "∇^{a}∇_{a}φ1",
    "mass_dim": 3,
    "lambda_power": 1,
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
    "candidate": "-½ m_1² φ1²",
    "mass_dim": 4,
    "lambda_power": 0,
    "fixed": true,
    "sector": "matter",
    "potential_type": "quadratic"
  }
]
```

### Output Paths

- proposal: ``
- solver output: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_212553_08f452b1/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_212553_08f452b1/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_212553_08f452b1/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 6. loop_46  chi2=1664.552041

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: `416`
- H0_km_s_Mpc: `64.44494063`
- Omega_m0: `0.34288713`
- lambda_H_Lambda_over_H0: `4.85766749e+04`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \beta · R  +  \delta Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf}  +  \alpha Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd}  +  \gamma Λ^{-4} · ∇^{a}φ1 · ∇_{a}φ1 · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (4.5892805050e-09) Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf}  +  (-3.7248281177e-09) Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd}  +  (2.1842237098e-05) Λ^{-4} · ∇^{a}φ1 · ∇_{a}φ1 · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( \beta · R ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · ∇^{a}φ1 · ∇_{a}φ1 · R ) ] +
√(-g) [ M_p² ( \delta · Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( -3.7248281177e-09 · Λ^{-3} · φ1 · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 2.1842237098e-05 · Λ^{-4} · ∇^{a}φ1 · ∇_{a}φ1 · R ) ] +
√(-g) [ M_p² ( 4.5892805050e-09 · Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ]
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
    "candidate": "∇^{a}φ1 · ∇_{a}φ1 · R",
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

### Output Paths

- proposal: ``
- solver output: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_211707_147ecec1/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_211707_147ecec1/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_211707_147ecec1/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 7. loop_40  chi2=1674.305113

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "axion", "phi2": null}`
- agent_parameter_sample_index: `462`
- H0_km_s_Mpc: `65.30950168`
- Omega_m0: `0.31937832`
- lambda_H_Lambda_over_H0: `2.78165278e+04`

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

### Output Paths

- proposal: ``
- solver output: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_211359_4d065520/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_211359_4d065520/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_211359_4d065520/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 8. loop_241  chi2=1677.775825

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: `371`
- H0_km_s_Mpc: `65.86429924`
- Omega_m0: `0.29572126`
- lambda_H_Lambda_over_H0: `5.56439609e+04`

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

### Output Paths

- proposal: ``
- solver output: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_225435_566a2a59/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_225435_566a2a59/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_225435_566a2a59/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 9. loop_146  chi2=1686.029546

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "axion", "phi2": null}`
- agent_parameter_sample_index: `752`
- H0_km_s_Mpc: `57.77954223`
- Omega_m0: `0.35348041`
- lambda_H_Lambda_over_H0: `2460.89374783`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha Λ^{-4} · R · R^{bcd}_{a} · R^{a}_{bcd}  +  \beta Λ^{-4} · ∇^{c}R^{ab} · ∇_{c}R_{ab}  +  \gamma · R  +  \delta Λ^{-3} · ∇^{a}∇^{b}φ1 · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (-7.6356122544e-08) Λ^{-4} · R · R^{bcd}_{a} · R^{a}_{bcd}  +  (-3.0688094993e-07) Λ^{-4} · ∇^{c}R^{ab} · ∇_{c}R_{ab}  +  (0.5) · R  +  (3.5214875411e-08) Λ^{-3} · ∇^{a}∇^{b}φ1 · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · Λ^{-4} · R · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · ∇^{c}R^{ab} · ∇_{c}R_{ab} ) ] +
√(-g) [ M_p² ( \gamma · R ) ] +
√(-g) [ M_p² ( \delta · Λ^{-3} · ∇^{a}∇^{b}φ1 · R_{ab} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( -7.6356122544e-08 · Λ^{-4} · R · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( -3.0688094993e-07 · Λ^{-4} · ∇^{c}R^{ab} · ∇_{c}R_{ab} ) ] +
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 3.5214875411e-08 · Λ^{-3} · ∇^{a}∇^{b}φ1 · R_{ab} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
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
    "candidate": "∇^{c}R^{ab} · ∇_{c}R_{ab}",
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
    "candidate": "∇^{a}∇^{b}φ1 · R_{ab}",
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

### Output Paths

- proposal: ``
- solver output: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_220237_230e1eb9/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_220237_230e1eb9/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_220237_230e1eb9/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 10. loop_172  chi2=1686.631821

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: `386`
- H0_km_s_Mpc: `65.87057632`
- Omega_m0: `0.21995712`
- lambda_H_Lambda_over_H0: `1.28788400e+04`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha Λ^{-2} · R^{ab} · R_{ab}  +  \beta · R  +  \delta Λ^{-4} · R^{b}_{a} · R^{cd} · R^{a}_{cbd}  +  \gamma Λ^{-4} · φ1 · ∇^{a}∇^{b}φ1 · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (1.1756363235e-10) Λ^{-2} · R^{ab} · R_{ab}  +  (0.5) · R  +  (2.9681008228e-05) Λ^{-4} · R^{b}_{a} · R^{cd} · R^{a}_{cbd}  +  (6.1782305527e-08) Λ^{-4} · φ1 · ∇^{a}∇^{b}φ1 · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · Λ^{-2} · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( \beta · R ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · φ1 · ∇^{a}∇^{b}φ1 · R_{ab} ) ] +
√(-g) [ M_p² ( \delta · Λ^{-4} · R^{b}_{a} · R^{cd} · R^{a}_{cbd} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 1.1756363235e-10 · Λ^{-2} · R^{ab} · R_{ab} ) ] +
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 6.1782305527e-08 · Λ^{-4} · φ1 · ∇^{a}∇^{b}φ1 · R_{ab} ) ] +
√(-g) [ M_p² ( 2.9681008228e-05 · Λ^{-4} · R^{b}_{a} · R^{cd} · R^{a}_{cbd} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ]
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
    "candidate": "R",
    "mass_dim": 2,
    "lambda_power": 0,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\gamma",
    "coeff_token": "COEFF_2",
    "candidate": "φ1 · ∇^{a}∇^{b}φ1 · R_{ab}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "non-minimal"
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
    "candidate": "-½ m_1² φ1²",
    "mass_dim": 4,
    "lambda_power": 0,
    "fixed": true,
    "sector": "matter",
    "potential_type": "quadratic"
  }
]
```

### Output Paths

- proposal: ``
- solver output: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_221528_2323eec3/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_221528_2323eec3/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_221528_2323eec3/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 11. loop_118  chi2=1714.522956

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "axion", "phi2": null}`
- agent_parameter_sample_index: `359`
- H0_km_s_Mpc: `62.87090154`
- Omega_m0: `0.2712262`
- lambda_H_Lambda_over_H0: `6.44639914e+04`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · ∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}  +  \gamma Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf}  +  \delta Λ^{-4} · R^{ab} · R^{d}_{a} · R_{bd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (6.6527449513e-05) Λ^{-4} · ∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}  +  (1.0114218597e-06) Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf}  +  (9.0604853764e-10) Λ^{-4} · R^{ab} · R^{d}_{a} · R_{bd} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · ∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf} ) ] +
√(-g) [ M_p² ( \delta · Λ^{-4} · R^{ab} · R^{d}_{a} · R_{bd} ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 6.6527449513e-05 · Λ^{-4} · ∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( 1.0114218597e-06 · Λ^{-4} · R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{hdf} ) ] +
√(-g) [ M_p² ( 9.0604853764e-10 · Λ^{-4} · R^{ab} · R^{d}_{a} · R_{bd} ) ] +
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

### Output Paths

- proposal: ``
- solver output: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_214841_119e1346/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_214841_119e1346/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_214841_119e1346/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 12. loop_39  chi2=1722.722042

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "quadratic", "phi2": null}`
- agent_parameter_sample_index: `691`
- H0_km_s_Mpc: `67.63957554`
- Omega_m0: `0.38214079`
- lambda_H_Lambda_over_H0: `2.83813009e+04`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd}  +  \beta Λ^{-4} · ∇^{a}∇_{a}R · R^{c}_{c}  +  \gamma · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (-1.4591916311e-07) Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd}  +  (-8.1085675888e-10) Λ^{-4} · ∇^{a}∇_{a}R · R^{c}_{c}  +  (0.5) · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · ∇^{a}∇_{a}R · R^{c}_{c} ) ] +
√(-g) [ M_p² ( \gamma · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( -1.4591916311e-07 · Λ^{-2} · R^{bcd}_{a} · R^{a}_{bcd} ) ] +
√(-g) [ M_p² ( -8.1085675888e-10 · Λ^{-4} · ∇^{a}∇_{a}R · R^{c}_{c} ) ] +
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
    "candidate": "R^{bcd}_{a} · R^{a}_{bcd}",
    "mass_dim": 4,
    "lambda_power": -2,
    "sector": "gravity"
  },
  {
    "coeff_symbol": "\\beta",
    "coeff_token": "COEFF_1",
    "candidate": "∇^{a}∇_{a}R · R^{c}_{c}",
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
    "candidate": "-½ m_1² φ1²",
    "mass_dim": 4,
    "lambda_power": 0,
    "fixed": true,
    "sector": "matter",
    "potential_type": "quadratic"
  }
]
```

### Output Paths

- proposal: ``
- solver output: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_211339_9e680216/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_211339_9e680216/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_211339_9e680216/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 13. loop_295_expanded  chi2=1743.313128

- scalar_config: `phi1_only`
- potential_types: `{"phi1": "axion", "phi2": null}`
- agent_parameter_sample_index: `231`
- H0_km_s_Mpc: `67.46312707`
- Omega_m0: `0.39227301`
- lambda_H_Lambda_over_H0: `5407.48918807`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · ∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}  +  \delta Λ^{-4} · ∇^{a}R · ∇_{a}R )  +  \gamma Λ^{2} · φ1 · φ1  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (8.0375835482e-09) Λ^{-4} · ∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}  +  (-2.2354397455e-09) Λ^{-4} · ∇^{a}R · ∇_{a}R )  +  (-4.3727094474e-09) Λ^{2} · φ1 · φ1  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · ∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd} ) ] +
√(-g) [ \gamma · Λ^{2} · φ1 · φ1 ] +
√(-g) [ M_p² ( \delta · Λ^{-4} · ∇^{a}R · ∇_{a}R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( 8.0375835482e-09 · Λ^{-4} · ∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd} ) ] +
√(-g) [ -4.3727094474e-09 · Λ^{2} · φ1 · φ1 ] +
√(-g) [ M_p² ( -2.2354397455e-09 · Λ^{-4} · ∇^{a}R · ∇_{a}R ) ] +
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
    "coeff_symbol": "\\gamma",
    "coeff_token": "COEFF_2",
    "candidate": "φ1 · φ1",
    "mass_dim": 2,
    "lambda_power": 2,
    "sector": "scalar"
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

### Output Paths

- proposal: ``
- solver output: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_233231_a44253d0/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_233231_a44253d0/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_233231_a44253d0/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 14. loop_16  chi2=1756.864092

- scalar_config: `both`
- potential_types: `{"phi1": "quadratic", "phi2": "axion"}`
- agent_parameter_sample_index: `490`
- H0_km_s_Mpc: `64.62124256`
- Omega_m0: `0.35224905`
- lambda_H_Lambda_over_H0: `6313.8840642`

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

### Output Paths

- proposal: ``
- solver output: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_205958_690b4a04/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_205958_690b4a04/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_205958_690b4a04/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 15. loop_212_expanded  chi2=9434.007716

- scalar_config: `phi2_only`
- potential_types: `{"phi1": null, "phi2": "axion"}`
- agent_parameter_sample_index: `255`
- H0_km_s_Mpc: `62.10884365`
- Omega_m0: `0.24528518`
- lambda_H_Lambda_over_H0: `2634.13519492`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha Λ^{-4} · φ2 · φ2 · φ2 · φ2 · R )  +  \beta Λ^{1} · φ2 · φ2 · φ2  +  \gamma Λ^{-2} · φ2 · φ2 · φ2 · φ2 · φ2 · φ2  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (-7.2546702524e-05) Λ^{-4} · φ2 · φ2 · φ2 · φ2 · R )  +  (1.0594039175e-08) Λ^{1} · φ2 · φ2 · φ2  +  (3.8820225682e-08) Λ^{-2} · φ2 · φ2 · φ2 · φ2 · φ2 · φ2  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · Λ^{-4} · φ2 · φ2 · φ2 · φ2 · R ) ] +
√(-g) [ \beta · Λ^{1} · φ2 · φ2 · φ2 ] +
√(-g) [ \gamma · Λ^{-2} · φ2 · φ2 · φ2 · φ2 · φ2 · φ2 ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( -7.2546702524e-05 · Λ^{-4} · φ2 · φ2 · φ2 · φ2 · R ) ] +
√(-g) [ 1.0594039175e-08 · Λ^{1} · φ2 · φ2 · φ2 ] +
√(-g) [ 3.8820225682e-08 · Λ^{-2} · φ2 · φ2 · φ2 · φ2 · φ2 · φ2 ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
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
    "coeff_symbol": "\\beta",
    "coeff_token": "COEFF_1",
    "candidate": "φ2 · φ2 · φ2",
    "mass_dim": 3,
    "lambda_power": 1,
    "sector": "scalar"
  },
  {
    "coeff_symbol": "\\gamma",
    "coeff_token": "COEFF_2",
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

### Output Paths

- proposal: ``
- solver output: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_223805_ba41c09e/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_223805_ba41c09e/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_223805_ba41c09e/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 16. loop_11_expanded  chi2=9434.007717

- scalar_config: `phi2_only`
- potential_types: `{"phi1": null, "phi2": "axion"}`
- agent_parameter_sample_index: `684`
- H0_km_s_Mpc: `58.81523479`
- Omega_m0: `0.24499998`
- lambda_H_Lambda_over_H0: `3.12222434e+04`

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

### Output Paths

- proposal: ``
- solver output: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_205703_785e04b7/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_205703_785e04b7/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_205703_785e04b7/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`

## 17. loop_239  chi2=9434.007723

- scalar_config: `phi2_only`
- potential_types: `{"phi1": null, "phi2": "quadratic"}`
- agent_parameter_sample_index: `10`
- H0_km_s_Mpc: `59.87455439`
- Omega_m0: `0.21536537`
- lambda_H_Lambda_over_H0: `9966.24300027`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \gamma Λ^{-4} · ∇^{a}R · ∇_{a}R  +  \beta Λ^{-3} · φ2 · R · R  +  \delta Λ^{-4} · φ2 · φ2 · φ2 · φ2 · R )  +  \alpha · φ2 · φ2 · φ2 · φ2  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (-5.8590901337e-09) Λ^{-4} · ∇^{a}R · ∇_{a}R  +  (1.7432310334e-07) Λ^{-3} · φ2 · R · R  +  (-9.0262827728e-05) Λ^{-4} · φ2 · φ2 · φ2 · φ2 · R )  +  (5.4711652607e-05) · φ2 · φ2 · φ2 · φ2  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -½ m_2² φ2² ]
```

### Expanded Terms

```text
√(-g) [ \alpha · φ2 · φ2 · φ2 · φ2 ] +
√(-g) [ M_p² ( \beta · Λ^{-3} · φ2 · R · R ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · ∇^{a}R · ∇_{a}R ) ] +
√(-g) [ M_p² ( \delta · Λ^{-4} · φ2 · φ2 · φ2 · φ2 · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ 5.4711652607e-05 · φ2 · φ2 · φ2 · φ2 ] +
√(-g) [ M_p² ( 1.7432310334e-07 · Λ^{-3} · φ2 · R · R ) ] +
√(-g) [ M_p² ( -5.8590901337e-09 · Λ^{-4} · ∇^{a}R · ∇_{a}R ) ] +
√(-g) [ M_p² ( -9.0262827728e-05 · Λ^{-4} · φ2 · φ2 · φ2 · φ2 · R ) ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -½ m_2² φ2² ]
```

### Term Metadata

```json
[
  {
    "coeff_symbol": "\\alpha",
    "coeff_token": "COEFF_0",
    "candidate": "φ2 · φ2 · φ2 · φ2",
    "mass_dim": 4,
    "lambda_power": 0,
    "sector": "scalar"
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
    "candidate": "∇^{a}R · ∇_{a}R",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "gravity"
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

### Output Paths

- proposal: ``
- solver output: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_225337_baaf4042/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_225337_baaf4042/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_225337_baaf4042/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`
