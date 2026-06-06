# Accepted Lagrangians: Full Dimension-Balanced Forms, Initial Conditions, And Parameters

This report rewrites accepted models from `graph_agent_120_policy2_20260603` using the actual `agent_lagrangians.pkl` objects that entered EOM -> Builder -> Solver. The Lagrangian form includes `√(-g)`, `M_p²` prefactors, `Λ` powers used to balance mass dimension, fixed scalar matter terms, best-fit coefficient substitutions, fit metrics, initial conditions, and output files. It is sorted by `chi2`.

## Numerical Convention

- Independent variable: `x = ln(a) = -ln(1+z)`.
- Dimensionless Hubble: `h(x) = H(x) / H0`.
- Scalar 1: `varphi1(x) = phi1(x) / Mp`; `q1 = d varphi1 / dx`.
- Scalar 2: `varphi2(x) = phi2(x) / Lambda`; `q2 = d varphi2 / dx`.
- Gravity and non-minimal sectors use `M_p² * coefficient * Λ^(2-d) * O_d`.
- Pure scalar generated sectors use `coefficient * Λ^(4-d) * O_d` without the `M_p²` prefactor.
- Fixed matter kinetic/potential terms are already dimension four and use `Λ^0`.
- `lambda_H = Lambda / H0`; physical `Lambda [eV] = lambda_H * H0 [eV]`.

============================================================================================
## Rank 1: loop_19_expanded  chi2=1638.1031
============================================================================================

### Theory Metadata

- `scalar_config`: `phi1_only`
- `potential_types`: `{"phi1": "axion", "phi2": null}`
- `sample_budget`: `3000`
- `proposal_json`: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/proposals/graph_agent_120_policy2_20260603/loop_19_expanded.json`
- `agent_lagrangians.pkl`: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_000951_88c3668b/agent_lagrangians.pkl`

### Raw Lagrangian From `agent_lagrangians.pkl`

```text
√(-g) [ M_p² ( \alpha Λ^{-2} · R^{ab} · R_{ab}  +  \beta Λ^{-4} · R · R^{ab} · R_{ab}  +  \gamma · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Best-Fit Coefficient-Substituted Lagrangian

```text
√(-g) [ M_p² ( (4.8162545203e-06) Λ^{-2} · R^{ab} · R_{ab}  +  (-1.4950869018e-07) Λ^{-4} · R · R^{ab} · R_{ab}  +  (0.5) · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Term Contributions

Symbolic:

```text
L = √(-g) [ M_p² ( \alpha · Λ^{-2} · R^{ab} · R_{ab} ) ]
  + √(-g) [ M_p² ( \beta · Λ^{-4} · R · R^{ab} · R_{ab} ) ]
  + √(-g) [ M_p² ( \gamma · R ) ]
  + √(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ]
  + √(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

Best-fit coefficients substituted:

```text
L = √(-g) [ M_p² ( (4.8162545203e-06) · Λ^{-2} · R^{ab} · R_{ab} ) ]
  + √(-g) [ M_p² ( (-1.4950869018e-07) · Λ^{-4} · R · R^{ab} · R_{ab} ) ]
  + √(-g) [ M_p² ( (0.5) · R ) ]
  + √(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ]
  + √(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Term Metadata

1. coeff `\alpha` = `4.8162545203e-06`; sector `gravity`; mass_dim `4`; Λ power `-2`; inside `M_p²(...)`: `yes`; fixed: `no`; candidate `R^{ab} · R_{ab}`
2. coeff `\beta` = `-1.4950869018e-07`; sector `gravity`; mass_dim `6`; Λ power `-4`; inside `M_p²(...)`: `yes`; fixed: `no`; candidate `R · R^{ab} · R_{ab}`
3. coeff `\gamma` = `0.5`; sector `gravity`; mass_dim `2`; Λ power `0`; inside `M_p²(...)`: `yes`; fixed: `no`; candidate `R`
4. coeff `1` = `1`; sector `matter`; mass_dim `4`; Λ power `0`; inside `M_p²(...)`: `no`; fixed: `yes`; candidate `-½ g^{μν} ∇_μφ1 ∇_νφ1`
5. coeff `1` = `1`; sector `matter`; mass_dim `4`; Λ power `0`; inside `M_p²(...)`: `no`; fixed: `yes`; candidate `-m_1² f_1² (1 - cos(φ1/f_1))`

### Fit Metrics

- chi2: `1638.1031`
- chi2 per point: `0.89367328`
- chi2_SN: `1629.9116`
- chi2_BAO: `8.1915486`
- AIC: `1652.1031`
- BIC: `1690.6991`
- k_params: `7`
- max |E_N|: `2.28646381e-06`
- agent_parameter_sample_index: `333`

### Initial Conditions And Sampled Values

- H0 [km/s/Mpc]: `69.343816`
- eps_HM = H0/Mp: `6.07468632e-61`
- lambda_H = Lambda/H0: `10819.083`
- Lambda [eV]: `1.60034368e-29`
- Omega_m0: `0.28074429`
- rho_bar: `0.84223287`
- varphi1_0 = phi1_0/Mp: `2.0540885`
- q1_0 = dvarphi1/dx|0: `-0.57554505`
- mu1 = m1/H0: `0.9889175`
- fbar1 = f1/Mp: `3.1742529`
- varphi2_0 = phi2_0/Lambda: `0`
- q2_0 = dvarphi2/dx|0: `0`
- mu2 = m2/Lambda: `0`
- fbar2 = f2/Lambda: `1`

### Free Coupling Values

- alpha: `4.8162545203e-06`  (proposal/catalog symbol `\alpha`)
- beta: `-1.4950869018e-07`  (proposal/catalog symbol `\beta`)
- gamma: `0.5`  (proposal/catalog symbol `\gamma`)

### Files

- Solver output directory: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_000951_88c3668b/agent_solver_result/agent_solve`
- model_ranking.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_000951_88c3668b/agent_solver_result/agent_solve/model_ranking.csv`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_000951_88c3668b/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- all_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_000951_88c3668b/agent_solver_result/agent_solve/all_samples_summary.csv`
- reject_reasons_by_model.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_000951_88c3668b/agent_solver_result/agent_solve/reject_reasons_by_model.csv`
- best_solution.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_000951_88c3668b/agent_solver_result/agent_solve/best_solution.csv`
- scan_report.txt: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_000951_88c3668b/agent_solver_result/agent_solve/scan_report.txt`

============================================================================================
## Rank 2: loop_38  chi2=1644.2982
============================================================================================

### Theory Metadata

- `scalar_config`: `phi1_only`
- `potential_types`: `{"phi1": "quadratic", "phi2": null}`
- `sample_budget`: `1000`
- `proposal_json`: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/proposals/graph_agent_120_policy2_20260603/loop_38_initial.json`
- `agent_lagrangians.pkl`: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_001900_0263fc67/agent_lagrangians.pkl`

### Raw Lagrangian From `agent_lagrangians.pkl`

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · ∇^{a}∇_{a}R · R^{c}_{c}  +  \delta Λ^{-4} · ∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}  +  \gamma Λ^{-4} · ∇^{a}φ1 · ∇_{a}φ1 · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Best-Fit Coefficient-Substituted Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-1.6163829468e-08) Λ^{-4} · ∇^{a}∇_{a}R · R^{c}_{c}  +  (-5.4131315009e-06) Λ^{-4} · ∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}  +  (-2.0385020624e-07) Λ^{-4} · ∇^{a}φ1 · ∇_{a}φ1 · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Expanded Term Contributions

Symbolic:

```text
L = √(-g) [ M_p² ( \alpha · R ) ]
  + √(-g) [ M_p² ( \beta · Λ^{-4} · ∇^{a}∇_{a}R · R^{c}_{c} ) ]
  + √(-g) [ M_p² ( \gamma · Λ^{-4} · ∇^{a}φ1 · ∇_{a}φ1 · R ) ]
  + √(-g) [ M_p² ( \delta · Λ^{-4} · ∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd} ) ]
  + √(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ]
  + √(-g) [ -½ m_1² φ1² ]
```

Best-fit coefficients substituted:

```text
L = √(-g) [ M_p² ( (0.5) · R ) ]
  + √(-g) [ M_p² ( (-1.6163829468e-08) · Λ^{-4} · ∇^{a}∇_{a}R · R^{c}_{c} ) ]
  + √(-g) [ M_p² ( (-2.0385020624e-07) · Λ^{-4} · ∇^{a}φ1 · ∇_{a}φ1 · R ) ]
  + √(-g) [ M_p² ( (-5.4131315009e-06) · Λ^{-4} · ∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd} ) ]
  + √(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ]
  + √(-g) [ -½ m_1² φ1² ]
```

### Term Metadata

1. coeff `\alpha` = `0.5`; sector `gravity`; mass_dim `2`; Λ power `0`; inside `M_p²(...)`: `yes`; fixed: `no`; candidate `R`
2. coeff `\beta` = `-1.6163829468e-08`; sector `gravity`; mass_dim `6`; Λ power `-4`; inside `M_p²(...)`: `yes`; fixed: `no`; candidate `∇^{a}∇_{a}R · R^{c}_{c}`
3. coeff `\gamma` = `-2.0385020624e-07`; sector `non-minimal`; mass_dim `6`; Λ power `-4`; inside `M_p²(...)`: `yes`; fixed: `no`; candidate `∇^{a}φ1 · ∇_{a}φ1 · R`
4. coeff `\delta` = `-5.4131315009e-06`; sector `gravity`; mass_dim `6`; Λ power `-4`; inside `M_p²(...)`: `yes`; fixed: `no`; candidate `∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}`
5. coeff `1` = `1`; sector `matter`; mass_dim `4`; Λ power `0`; inside `M_p²(...)`: `no`; fixed: `yes`; candidate `-½ g^{μν} ∇_μφ1 ∇_νφ1`
6. coeff `1` = `1`; sector `matter`; mass_dim `4`; Λ power `0`; inside `M_p²(...)`: `no`; fixed: `yes`; candidate `-½ m_1² φ1²`

### Fit Metrics

- chi2: `1644.2982`
- chi2 per point: `0.89705304`
- chi2_SN: `1629.849`
- chi2_BAO: `14.449201`
- AIC: `1656.2982`
- BIC: `1689.3805`
- k_params: `6`
- max |E_N|: `4.38609342e-07`
- agent_parameter_sample_index: `545`

### Initial Conditions And Sampled Values

- H0 [km/s/Mpc]: `74.081139`
- eps_HM = H0/Mp: `6.48968726e-61`
- lambda_H = Lambda/H0: `2414.7841`
- Lambda [eV]: `3.81593564e-30`
- Omega_m0: `0.28835916`
- rho_bar: `0.86507747`
- varphi1_0 = phi1_0/Mp: `1.7374884`
- q1_0 = dvarphi1/dx|0: `-0.6178675`
- mu1 = m1/H0: `1.1348696`
- fbar1 = f1/Mp: `0.21591809`
- varphi2_0 = phi2_0/Lambda: `0`
- q2_0 = dvarphi2/dx|0: `0`
- mu2 = m2/Lambda: `0`
- fbar2 = f2/Lambda: `1`

### Free Coupling Values

- alpha: `0.5`  (proposal/catalog symbol `\alpha`)
- beta: `-1.6163829468e-08`  (proposal/catalog symbol `\beta`)
- gamma: `-2.0385020624e-07`  (proposal/catalog symbol `\gamma`)
- delta: `-5.4131315009e-06`  (proposal/catalog symbol `\delta`)

### Files

- Solver output directory: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_001900_0263fc67/agent_solver_result/agent_solve`
- model_ranking.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_001900_0263fc67/agent_solver_result/agent_solve/model_ranking.csv`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_001900_0263fc67/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- all_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_001900_0263fc67/agent_solver_result/agent_solve/all_samples_summary.csv`
- reject_reasons_by_model.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_001900_0263fc67/agent_solver_result/agent_solve/reject_reasons_by_model.csv`
- best_solution.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_001900_0263fc67/agent_solver_result/agent_solve/best_solution.csv`
- scan_report.txt: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_001900_0263fc67/agent_solver_result/agent_solve/scan_report.txt`

============================================================================================
## Rank 3: loop_100  chi2=1647.8495
============================================================================================

### Theory Metadata

- `scalar_config`: `phi1_only`
- `potential_types`: `{"phi1": "axion", "phi2": null}`
- `sample_budget`: `1000`
- `proposal_json`: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/proposals/graph_agent_120_policy2_20260603/loop_100_initial.json`
- `agent_lagrangians.pkl`: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_004625_7202c551/agent_lagrangians.pkl`

### Raw Lagrangian From `agent_lagrangians.pkl`

```text
√(-g) [ M_p² ( \alpha · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Best-Fit Coefficient-Substituted Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Term Contributions

Symbolic:

```text
L = √(-g) [ M_p² ( \alpha · R ) ]
  + √(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ]
  + √(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

Best-fit coefficients substituted:

```text
L = √(-g) [ M_p² ( (0.5) · R ) ]
  + √(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ]
  + √(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Term Metadata

1. coeff `\alpha` = `0.5`; sector `gravity`; mass_dim `2`; Λ power `0`; inside `M_p²(...)`: `yes`; fixed: `no`; candidate `R`
2. coeff `1` = `1`; sector `matter`; mass_dim `4`; Λ power `0`; inside `M_p²(...)`: `no`; fixed: `yes`; candidate `-½ g^{μν} ∇_μφ1 ∇_νφ1`
3. coeff `1` = `1`; sector `matter`; mass_dim `4`; Λ power `0`; inside `M_p²(...)`: `no`; fixed: `yes`; candidate `-m_1² f_1² (1 - cos(φ1/f_1))`

### Fit Metrics

- chi2: `1647.8495`
- chi2 per point: `0.89899047`
- chi2_SN: `1636.62`
- chi2_BAO: `11.22949`
- AIC: `1661.8495`
- BIC: `1700.4455`
- k_params: `7`
- max |E_N|: `8.92639702e-07`
- agent_parameter_sample_index: `422`

### Initial Conditions And Sampled Values

- H0 [km/s/Mpc]: `75.660792`
- eps_HM = H0/Mp: `6.62806869e-61`
- lambda_H = Lambda/H0: `17576.1`
- Lambda [eV]: `2.83666788e-29`
- Omega_m0: `0.281405`
- rho_bar: `0.84421501`
- varphi1_0 = phi1_0/Mp: `4.113359`
- q1_0 = dvarphi1/dx|0: `-0.28804861`
- mu1 = m1/H0: `0.5208395`
- fbar1 = f1/Mp: `4.1641935`
- varphi2_0 = phi2_0/Lambda: `0`
- q2_0 = dvarphi2/dx|0: `0`
- mu2 = m2/Lambda: `0`
- fbar2 = f2/Lambda: `1`

### Free Coupling Values

- alpha: `0.5`  (proposal/catalog symbol `\alpha`)

### Files

- Solver output directory: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_004625_7202c551/agent_solver_result/agent_solve`
- model_ranking.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_004625_7202c551/agent_solver_result/agent_solve/model_ranking.csv`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_004625_7202c551/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- all_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_004625_7202c551/agent_solver_result/agent_solve/all_samples_summary.csv`
- reject_reasons_by_model.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_004625_7202c551/agent_solver_result/agent_solve/reject_reasons_by_model.csv`
- best_solution.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_004625_7202c551/agent_solver_result/agent_solve/best_solution.csv`
- scan_report.txt: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_004625_7202c551/agent_solver_result/agent_solve/scan_report.txt`

============================================================================================
## Rank 4: loop_25  chi2=1691.0358
============================================================================================

### Theory Metadata

- `scalar_config`: `phi1_only`
- `potential_types`: `{"phi1": "quadratic", "phi2": null}`
- `sample_budget`: `1000`
- `proposal_json`: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/proposals/graph_agent_120_policy2_20260603/loop_25_initial.json`
- `agent_lagrangians.pkl`: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_001227_3dff8812/agent_lagrangians.pkl`

### Raw Lagrangian From `agent_lagrangians.pkl`

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · R · R · R  +  \gamma Λ^{-4} · ∇^{c}R^{ab} · ∇_{c}R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Best-Fit Coefficient-Substituted Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (9.9410814077e-07) Λ^{-4} · R · R · R  +  (1.2033676646e-08) Λ^{-4} · ∇^{c}R^{ab} · ∇_{c}R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Expanded Term Contributions

Symbolic:

```text
L = √(-g) [ M_p² ( \alpha · R ) ]
  + √(-g) [ M_p² ( \beta · Λ^{-4} · R · R · R ) ]
  + √(-g) [ M_p² ( \gamma · Λ^{-4} · ∇^{c}R^{ab} · ∇_{c}R_{ab} ) ]
  + √(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ]
  + √(-g) [ -½ m_1² φ1² ]
```

Best-fit coefficients substituted:

```text
L = √(-g) [ M_p² ( (0.5) · R ) ]
  + √(-g) [ M_p² ( (9.9410814077e-07) · Λ^{-4} · R · R · R ) ]
  + √(-g) [ M_p² ( (1.2033676646e-08) · Λ^{-4} · ∇^{c}R^{ab} · ∇_{c}R_{ab} ) ]
  + √(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ]
  + √(-g) [ -½ m_1² φ1² ]
```

### Term Metadata

1. coeff `\alpha` = `0.5`; sector `gravity`; mass_dim `2`; Λ power `0`; inside `M_p²(...)`: `yes`; fixed: `no`; candidate `R`
2. coeff `\beta` = `9.9410814077e-07`; sector `gravity`; mass_dim `6`; Λ power `-4`; inside `M_p²(...)`: `yes`; fixed: `no`; candidate `R · R · R`
3. coeff `\gamma` = `1.2033676646e-08`; sector `gravity`; mass_dim `6`; Λ power `-4`; inside `M_p²(...)`: `yes`; fixed: `no`; candidate `∇^{c}R^{ab} · ∇_{c}R_{ab}`
4. coeff `1` = `1`; sector `matter`; mass_dim `4`; Λ power `0`; inside `M_p²(...)`: `no`; fixed: `yes`; candidate `-½ g^{μν} ∇_μφ1 ∇_νφ1`
5. coeff `1` = `1`; sector `matter`; mass_dim `4`; Λ power `0`; inside `M_p²(...)`: `no`; fixed: `yes`; candidate `-½ m_1² φ1²`

### Fit Metrics

- chi2: `1691.0358`
- chi2 per point: `0.92255088`
- chi2_SN: `1667.9687`
- chi2_BAO: `23.067053`
- AIC: `1703.0358`
- BIC: `1736.118`
- k_params: `6`
- max |E_N|: `5.15680238e-07`
- agent_parameter_sample_index: `392`

### Initial Conditions And Sampled Values

- H0 [km/s/Mpc]: `59.755546`
- eps_HM = H0/Mp: `5.23473064e-61`
- lambda_H = Lambda/H0: `18866.152`
- Lambda [eV]: `2.40478716e-29`
- Omega_m0: `0.26637662`
- rho_bar: `0.79912985`
- varphi1_0 = phi1_0/Mp: `0.77911761`
- q1_0 = dvarphi1/dx|0: `-1.1401427`
- mu1 = m1/H0: `2.2605021`
- fbar1 = f1/Mp: `8.2492843`
- varphi2_0 = phi2_0/Lambda: `0`
- q2_0 = dvarphi2/dx|0: `0`
- mu2 = m2/Lambda: `0`
- fbar2 = f2/Lambda: `1`

### Free Coupling Values

- alpha: `0.5`  (proposal/catalog symbol `\alpha`)
- beta: `9.9410814077e-07`  (proposal/catalog symbol `\beta`)
- gamma: `1.2033676646e-08`  (proposal/catalog symbol `\gamma`)

### Files

- Solver output directory: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_001227_3dff8812/agent_solver_result/agent_solve`
- model_ranking.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_001227_3dff8812/agent_solver_result/agent_solve/model_ranking.csv`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_001227_3dff8812/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- all_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_001227_3dff8812/agent_solver_result/agent_solve/all_samples_summary.csv`
- reject_reasons_by_model.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_001227_3dff8812/agent_solver_result/agent_solve/reject_reasons_by_model.csv`
- best_solution.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_001227_3dff8812/agent_solver_result/agent_solve/best_solution.csv`
- scan_report.txt: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_001227_3dff8812/agent_solver_result/agent_solve/scan_report.txt`

============================================================================================
## Rank 5: loop_18  chi2=1698.2706
============================================================================================

### Theory Metadata

- `scalar_config`: `phi1_only`
- `potential_types`: `{"phi1": "quadratic", "phi2": null}`
- `sample_budget`: `1000`
- `proposal_json`: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/proposals/graph_agent_120_policy2_20260603/loop_18_initial.json`
- `agent_lagrangians.pkl`: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_000903_55601610/agent_lagrangians.pkl`

### Raw Lagrangian From `agent_lagrangians.pkl`

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · ∇^{a}φ1 · ∇^{b}φ1 · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Best-Fit Coefficient-Substituted Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-2.1684456750e-07) Λ^{-4} · ∇^{a}φ1 · ∇^{b}φ1 · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Expanded Term Contributions

Symbolic:

```text
L = √(-g) [ M_p² ( \alpha · R ) ]
  + √(-g) [ M_p² ( \beta · Λ^{-4} · ∇^{a}φ1 · ∇^{b}φ1 · R_{ab} ) ]
  + √(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ]
  + √(-g) [ -½ m_1² φ1² ]
```

Best-fit coefficients substituted:

```text
L = √(-g) [ M_p² ( (0.5) · R ) ]
  + √(-g) [ M_p² ( (-2.1684456750e-07) · Λ^{-4} · ∇^{a}φ1 · ∇^{b}φ1 · R_{ab} ) ]
  + √(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ]
  + √(-g) [ -½ m_1² φ1² ]
```

### Term Metadata

1. coeff `\alpha` = `0.5`; sector `gravity`; mass_dim `2`; Λ power `0`; inside `M_p²(...)`: `yes`; fixed: `no`; candidate `R`
2. coeff `\beta` = `-2.1684456750e-07`; sector `non-minimal`; mass_dim `6`; Λ power `-4`; inside `M_p²(...)`: `yes`; fixed: `no`; candidate `∇^{a}φ1 · ∇^{b}φ1 · R_{ab}`
3. coeff `1` = `1`; sector `matter`; mass_dim `4`; Λ power `0`; inside `M_p²(...)`: `no`; fixed: `yes`; candidate `-½ g^{μν} ∇_μφ1 ∇_νφ1`
4. coeff `1` = `1`; sector `matter`; mass_dim `4`; Λ power `0`; inside `M_p²(...)`: `no`; fixed: `yes`; candidate `-½ m_1² φ1²`

### Fit Metrics

- chi2: `1698.2706`
- chi2 per point: `0.92649788`
- chi2_SN: `1660.2458`
- chi2_BAO: `38.024856`
- AIC: `1710.2706`
- BIC: `1743.3529`
- k_params: `6`
- max |E_N|: `8.40385404e-07`
- agent_parameter_sample_index: `37`

### Initial Conditions And Sampled Values

- H0 [km/s/Mpc]: `70.75961`
- eps_HM = H0/Mp: `6.19871332e-61`
- lambda_H = Lambda/H0: `12065.685`
- Lambda [eV]: `1.82117847e-29`
- Omega_m0: `0.23794509`
- rho_bar: `0.71383527`
- varphi1_0 = phi1_0/Mp: `2.3854774`
- q1_0 = dvarphi1/dx|0: `-0.42047872`
- mu1 = m1/H0: `0.87888121`
- fbar1 = f1/Mp: `3.2913268`
- varphi2_0 = phi2_0/Lambda: `0`
- q2_0 = dvarphi2/dx|0: `0`
- mu2 = m2/Lambda: `0`
- fbar2 = f2/Lambda: `1`

### Free Coupling Values

- alpha: `0.5`  (proposal/catalog symbol `\alpha`)
- beta: `-2.1684456750e-07`  (proposal/catalog symbol `\beta`)

### Files

- Solver output directory: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_000903_55601610/agent_solver_result/agent_solve`
- model_ranking.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_000903_55601610/agent_solver_result/agent_solve/model_ranking.csv`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_000903_55601610/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- all_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_000903_55601610/agent_solver_result/agent_solve/all_samples_summary.csv`
- reject_reasons_by_model.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_000903_55601610/agent_solver_result/agent_solve/reject_reasons_by_model.csv`
- best_solution.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_000903_55601610/agent_solver_result/agent_solve/best_solution.csv`
- scan_report.txt: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_000903_55601610/agent_solver_result/agent_solve/scan_report.txt`

============================================================================================
## Rank 6: loop_30  chi2=1698.5561
============================================================================================

### Theory Metadata

- `scalar_config`: `phi1_only`
- `potential_types`: `{"phi1": "axion", "phi2": null}`
- `sample_budget`: `1000`
- `proposal_json`: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/proposals/graph_agent_120_policy2_20260603/loop_30_initial.json`
- `agent_lagrangians.pkl`: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_001425_54bc9fc3/agent_lagrangians.pkl`

### Raw Lagrangian From `agent_lagrangians.pkl`

```text
√(-g) [ M_p² ( \beta · R  +  \alpha Λ^{-4} · ∇^{a}φ1 · ∇^{b}φ1 · R_{ab}  +  \gamma Λ^{-4} · φ1 · ∇^{a}∇^{b}φ1 · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Best-Fit Coefficient-Substituted Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (8.3067755613e-10) Λ^{-4} · ∇^{a}φ1 · ∇^{b}φ1 · R_{ab}  +  (-3.2244368092e-08) Λ^{-4} · φ1 · ∇^{a}∇^{b}φ1 · R_{ab} )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Term Contributions

Symbolic:

```text
L = √(-g) [ M_p² ( \alpha · Λ^{-4} · ∇^{a}φ1 · ∇^{b}φ1 · R_{ab} ) ]
  + √(-g) [ M_p² ( \beta · R ) ]
  + √(-g) [ M_p² ( \gamma · Λ^{-4} · φ1 · ∇^{a}∇^{b}φ1 · R_{ab} ) ]
  + √(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ]
  + √(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

Best-fit coefficients substituted:

```text
L = √(-g) [ M_p² ( (8.3067755613e-10) · Λ^{-4} · ∇^{a}φ1 · ∇^{b}φ1 · R_{ab} ) ]
  + √(-g) [ M_p² ( (0.5) · R ) ]
  + √(-g) [ M_p² ( (-3.2244368092e-08) · Λ^{-4} · φ1 · ∇^{a}∇^{b}φ1 · R_{ab} ) ]
  + √(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ]
  + √(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Term Metadata

1. coeff `\alpha` = `8.3067755613e-10`; sector `non-minimal`; mass_dim `6`; Λ power `-4`; inside `M_p²(...)`: `yes`; fixed: `no`; candidate `∇^{a}φ1 · ∇^{b}φ1 · R_{ab}`
2. coeff `\beta` = `0.5`; sector `gravity`; mass_dim `2`; Λ power `0`; inside `M_p²(...)`: `yes`; fixed: `no`; candidate `R`
3. coeff `\gamma` = `-3.2244368092e-08`; sector `non-minimal`; mass_dim `6`; Λ power `-4`; inside `M_p²(...)`: `yes`; fixed: `no`; candidate `φ1 · ∇^{a}∇^{b}φ1 · R_{ab}`
4. coeff `1` = `1`; sector `matter`; mass_dim `4`; Λ power `0`; inside `M_p²(...)`: `no`; fixed: `yes`; candidate `-½ g^{μν} ∇_μφ1 ∇_νφ1`
5. coeff `1` = `1`; sector `matter`; mass_dim `4`; Λ power `0`; inside `M_p²(...)`: `no`; fixed: `yes`; candidate `-m_1² f_1² (1 - cos(φ1/f_1))`

### Fit Metrics

- chi2: `1698.5561`
- chi2 per point: `0.92665363`
- chi2_SN: `1635.0724`
- chi2_BAO: `63.483708`
- AIC: `1712.5561`
- BIC: `1751.1521`
- k_params: `7`
- max |E_N|: `3.16959599e-07`
- agent_parameter_sample_index: `900`

### Initial Conditions And Sampled Values

- H0 [km/s/Mpc]: `59.368771`
- eps_HM = H0/Mp: `5.20084817e-61`
- lambda_H = Lambda/H0: `22559.16`
- Lambda [eV]: `2.85690680e-29`
- Omega_m0: `0.23266161`
- rho_bar: `0.69798483`
- varphi1_0 = phi1_0/Mp: `1.01769`
- q1_0 = dvarphi1/dx|0: `-0.9826556`
- mu1 = m1/H0: `1.877887`
- fbar1 = f1/Mp: `4.7566765`
- varphi2_0 = phi2_0/Lambda: `0`
- q2_0 = dvarphi2/dx|0: `0`
- mu2 = m2/Lambda: `0`
- fbar2 = f2/Lambda: `1`

### Free Coupling Values

- alpha: `8.3067755613e-10`  (proposal/catalog symbol `\alpha`)
- beta: `0.5`  (proposal/catalog symbol `\beta`)
- gamma: `-3.2244368092e-08`  (proposal/catalog symbol `\gamma`)

### Files

- Solver output directory: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_001425_54bc9fc3/agent_solver_result/agent_solve`
- model_ranking.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_001425_54bc9fc3/agent_solver_result/agent_solve/model_ranking.csv`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_001425_54bc9fc3/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- all_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_001425_54bc9fc3/agent_solver_result/agent_solve/all_samples_summary.csv`
- reject_reasons_by_model.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_001425_54bc9fc3/agent_solver_result/agent_solve/reject_reasons_by_model.csv`
- best_solution.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_001425_54bc9fc3/agent_solver_result/agent_solve/best_solution.csv`
- scan_report.txt: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_001425_54bc9fc3/agent_solver_result/agent_solve/scan_report.txt`

============================================================================================
## Rank 7: loop_41  chi2=1711.0254
============================================================================================

### Theory Metadata

- `scalar_config`: `phi1_only`
- `potential_types`: `{"phi1": "quadratic", "phi2": null}`
- `sample_budget`: `1000`
- `proposal_json`: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/proposals/graph_agent_120_policy2_20260603/loop_41_initial.json`
- `agent_lagrangians.pkl`: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_002051_934609e8/agent_lagrangians.pkl`

### Raw Lagrangian From `agent_lagrangians.pkl`

```text
√(-g) [ M_p² ( \beta · R )  +  \alpha Λ^{1} · ∇^{a}∇_{a}φ1  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Best-Fit Coefficient-Substituted Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R )  +  (1.8006036970e-09) Λ^{1} · ∇^{a}∇_{a}φ1  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1² ]
```

### Expanded Term Contributions

Symbolic:

```text
L = √(-g) [ \alpha · Λ^{1} · ∇^{a}∇_{a}φ1 ]
  + √(-g) [ M_p² ( \beta · R ) ]
  + √(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ]
  + √(-g) [ -½ m_1² φ1² ]
```

Best-fit coefficients substituted:

```text
L = √(-g) [ (1.8006036970e-09) · Λ^{1} · ∇^{a}∇_{a}φ1 ]
  + √(-g) [ M_p² ( (0.5) · R ) ]
  + √(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ]
  + √(-g) [ -½ m_1² φ1² ]
```

### Term Metadata

1. coeff `\alpha` = `1.8006036970e-09`; sector `scalar`; mass_dim `3`; Λ power `1`; inside `M_p²(...)`: `no`; fixed: `no`; candidate `∇^{a}∇_{a}φ1`
2. coeff `\beta` = `0.5`; sector `gravity`; mass_dim `2`; Λ power `0`; inside `M_p²(...)`: `yes`; fixed: `no`; candidate `R`
3. coeff `1` = `1`; sector `matter`; mass_dim `4`; Λ power `0`; inside `M_p²(...)`: `no`; fixed: `yes`; candidate `-½ g^{μν} ∇_μφ1 ∇_νφ1`
4. coeff `1` = `1`; sector `matter`; mass_dim `4`; Λ power `0`; inside `M_p²(...)`: `no`; fixed: `yes`; candidate `-½ m_1² φ1²`

### Fit Metrics

- chi2: `1711.0254`
- chi2 per point: `0.93345628`
- chi2_SN: `1684.988`
- chi2_BAO: `26.037402`
- AIC: `1723.0254`
- BIC: `1756.1076`
- k_params: `6`
- max |E_N|: `1.96258460e-06`
- agent_parameter_sample_index: `886`

### Initial Conditions And Sampled Values

- H0 [km/s/Mpc]: `63.559885`
- eps_HM = H0/Mp: `5.56799991e-61`
- lambda_H = Lambda/H0: `9072.8561`
- Lambda [eV]: `1.23010507e-29`
- Omega_m0: `0.31331011`
- rho_bar: `0.93993032`
- varphi1_0 = phi1_0/Mp: `1.1360697`
- q1_0 = dvarphi1/dx|0: `-0.92107697`
- mu1 = m1/H0: `1.5921557`
- fbar1 = f1/Mp: `2.7813218`
- varphi2_0 = phi2_0/Lambda: `0`
- q2_0 = dvarphi2/dx|0: `0`
- mu2 = m2/Lambda: `0`
- fbar2 = f2/Lambda: `1`

### Free Coupling Values

- alpha: `1.8006036970e-09`  (proposal/catalog symbol `\alpha`)
- beta: `0.5`  (proposal/catalog symbol `\beta`)

### Files

- Solver output directory: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_002051_934609e8/agent_solver_result/agent_solve`
- model_ranking.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_002051_934609e8/agent_solver_result/agent_solve/model_ranking.csv`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_002051_934609e8/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- all_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_002051_934609e8/agent_solver_result/agent_solve/all_samples_summary.csv`
- reject_reasons_by_model.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_002051_934609e8/agent_solver_result/agent_solve/reject_reasons_by_model.csv`
- best_solution.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_002051_934609e8/agent_solver_result/agent_solve/best_solution.csv`
- scan_report.txt: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_002051_934609e8/agent_solver_result/agent_solve/scan_report.txt`

============================================================================================
## Rank 8: loop_120  chi2=1778.0108
============================================================================================

### Theory Metadata

- `scalar_config`: `phi1_only`
- `potential_types`: `{"phi1": "axion", "phi2": null}`
- `sample_budget`: `1000`
- `proposal_json`: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/proposals/graph_agent_120_policy2_20260603/loop_120_initial.json`
- `agent_lagrangians.pkl`: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_114319_a5805251/agent_lagrangians.pkl`

### Raw Lagrangian From `agent_lagrangians.pkl`

```text
√(-g) [ M_p² ( \alpha Λ^{-4} · ∇^{a}R · ∇_{a}R  +  \gamma Λ^{-4} · R^{ab} · R^{d}_{a} · R_{bd}  +  \delta · R  +  \beta Λ^{-4} · φ1 · ∇^{a}φ1 · ∇_{a}R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Best-Fit Coefficient-Substituted Lagrangian

```text
√(-g) [ M_p² ( (2.6795022265e-08) Λ^{-4} · ∇^{a}R · ∇_{a}R  +  (-8.0101526798e-05) Λ^{-4} · R^{ab} · R^{d}_{a} · R_{bd}  +  (0.5) · R  +  (4.7231029782e-05) Λ^{-4} · φ1 · ∇^{a}φ1 · ∇_{a}R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Term Contributions

Symbolic:

```text
L = √(-g) [ M_p² ( \alpha · Λ^{-4} · ∇^{a}R · ∇_{a}R ) ]
  + √(-g) [ M_p² ( \beta · Λ^{-4} · φ1 · ∇^{a}φ1 · ∇_{a}R ) ]
  + √(-g) [ M_p² ( \gamma · Λ^{-4} · R^{ab} · R^{d}_{a} · R_{bd} ) ]
  + √(-g) [ M_p² ( \delta · R ) ]
  + √(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ]
  + √(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

Best-fit coefficients substituted:

```text
L = √(-g) [ M_p² ( (2.6795022265e-08) · Λ^{-4} · ∇^{a}R · ∇_{a}R ) ]
  + √(-g) [ M_p² ( (4.7231029782e-05) · Λ^{-4} · φ1 · ∇^{a}φ1 · ∇_{a}R ) ]
  + √(-g) [ M_p² ( (-8.0101526798e-05) · Λ^{-4} · R^{ab} · R^{d}_{a} · R_{bd} ) ]
  + √(-g) [ M_p² ( (0.5) · R ) ]
  + √(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ]
  + √(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Term Metadata

1. coeff `\alpha` = `2.6795022265e-08`; sector `gravity`; mass_dim `6`; Λ power `-4`; inside `M_p²(...)`: `yes`; fixed: `no`; candidate `∇^{a}R · ∇_{a}R`
2. coeff `\beta` = `4.7231029782e-05`; sector `non-minimal`; mass_dim `6`; Λ power `-4`; inside `M_p²(...)`: `yes`; fixed: `no`; candidate `φ1 · ∇^{a}φ1 · ∇_{a}R`
3. coeff `\gamma` = `-8.0101526798e-05`; sector `gravity`; mass_dim `6`; Λ power `-4`; inside `M_p²(...)`: `yes`; fixed: `no`; candidate `R^{ab} · R^{d}_{a} · R_{bd}`
4. coeff `\delta` = `0.5`; sector `gravity`; mass_dim `2`; Λ power `0`; inside `M_p²(...)`: `yes`; fixed: `no`; candidate `R`
5. coeff `1` = `1`; sector `matter`; mass_dim `4`; Λ power `0`; inside `M_p²(...)`: `no`; fixed: `yes`; candidate `-½ g^{μν} ∇_μφ1 ∇_νφ1`
6. coeff `1` = `1`; sector `matter`; mass_dim `4`; Λ power `0`; inside `M_p²(...)`: `no`; fixed: `yes`; candidate `-m_1² f_1² (1 - cos(φ1/f_1))`

### Fit Metrics

- chi2: `1778.0108`
- chi2 per point: `0.97000046`
- chi2_SN: `1655.4198`
- chi2_BAO: `122.59104`
- AIC: `1792.0108`
- BIC: `1830.6068`
- k_params: `7`
- max |E_N|: `2.25627720e-07`
- agent_parameter_sample_index: `930`

### Initial Conditions And Sampled Values

- H0 [km/s/Mpc]: `68.748711`
- eps_HM = H0/Mp: `6.02255362e-61`
- lambda_H = Lambda/H0: `13847.466`
- Lambda [eV]: `2.03071958e-29`
- Omega_m0: `0.22396561`
- rho_bar: `0.67189682`
- varphi1_0 = phi1_0/Mp: `2.4655983`
- q1_0 = dvarphi1/dx|0: `-0.50501124`
- mu1 = m1/H0: `0.85698159`
- fbar1 = f1/Mp: `5.9519361`
- varphi2_0 = phi2_0/Lambda: `0`
- q2_0 = dvarphi2/dx|0: `0`
- mu2 = m2/Lambda: `0`
- fbar2 = f2/Lambda: `1`

### Free Coupling Values

- alpha: `2.6795022265e-08`  (proposal/catalog symbol `\alpha`)
- beta: `4.7231029782e-05`  (proposal/catalog symbol `\beta`)
- gamma: `-8.0101526798e-05`  (proposal/catalog symbol `\gamma`)
- delta: `0.5`  (proposal/catalog symbol `\delta`)

### Files

- Solver output directory: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_114319_a5805251/agent_solver_result/agent_solve`
- model_ranking.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_114319_a5805251/agent_solver_result/agent_solve/model_ranking.csv`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_114319_a5805251/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- all_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_114319_a5805251/agent_solver_result/agent_solve/all_samples_summary.csv`
- reject_reasons_by_model.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_114319_a5805251/agent_solver_result/agent_solve/reject_reasons_by_model.csv`
- best_solution.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_114319_a5805251/agent_solver_result/agent_solve/best_solution.csv`
- scan_report.txt: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_114319_a5805251/agent_solver_result/agent_solve/scan_report.txt`

============================================================================================
## Rank 9: loop_102  chi2=1786.0023
============================================================================================

### Theory Metadata

- `scalar_config`: `phi1_only`
- `potential_types`: `{"phi1": "axion", "phi2": null}`
- `sample_budget`: `1000`
- `proposal_json`: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/proposals/graph_agent_120_policy2_20260603/loop_102_initial.json`
- `agent_lagrangians.pkl`: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_004733_139d04a0/agent_lagrangians.pkl`

### Raw Lagrangian From `agent_lagrangians.pkl`

```text
√(-g) [ M_p² ( \alpha · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Best-Fit Coefficient-Substituted Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Term Contributions

Symbolic:

```text
L = √(-g) [ M_p² ( \alpha · R ) ]
  + √(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ]
  + √(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

Best-fit coefficients substituted:

```text
L = √(-g) [ M_p² ( (0.5) · R ) ]
  + √(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ]
  + √(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Term Metadata

1. coeff `\alpha` = `0.5`; sector `gravity`; mass_dim `2`; Λ power `0`; inside `M_p²(...)`: `yes`; fixed: `no`; candidate `R`
2. coeff `1` = `1`; sector `matter`; mass_dim `4`; Λ power `0`; inside `M_p²(...)`: `no`; fixed: `yes`; candidate `-½ g^{μν} ∇_μφ1 ∇_νφ1`
3. coeff `1` = `1`; sector `matter`; mass_dim `4`; Λ power `0`; inside `M_p²(...)`: `no`; fixed: `yes`; candidate `-m_1² f_1² (1 - cos(φ1/f_1))`

### Fit Metrics

- chi2: `1786.0023`
- chi2 per point: `0.97436023`
- chi2_SN: `1779.1031`
- chi2_BAO: `6.899226`
- AIC: `1800.0023`
- BIC: `1838.5983`
- k_params: `7`
- max |E_N|: `2.73921516e-07`
- agent_parameter_sample_index: `994`

### Initial Conditions And Sampled Values

- H0 [km/s/Mpc]: `63.924678`
- eps_HM = H0/Mp: `5.59995671e-61`
- lambda_H = Lambda/H0: `5297.0008`
- Lambda [eV]: `7.22293440e-30`
- Omega_m0: `0.32761694`
- rho_bar: `0.98285082`
- varphi1_0 = phi1_0/Mp: `0.55782325`
- q1_0 = dvarphi1/dx|0: `-1.2799105`
- mu1 = m1/H0: `2.7957614`
- fbar1 = f1/Mp: `1.3189184`
- varphi2_0 = phi2_0/Lambda: `0`
- q2_0 = dvarphi2/dx|0: `0`
- mu2 = m2/Lambda: `0`
- fbar2 = f2/Lambda: `1`

### Free Coupling Values

- alpha: `0.5`  (proposal/catalog symbol `\alpha`)

### Files

- Solver output directory: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_004733_139d04a0/agent_solver_result/agent_solve`
- model_ranking.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_004733_139d04a0/agent_solver_result/agent_solve/model_ranking.csv`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_004733_139d04a0/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- all_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_004733_139d04a0/agent_solver_result/agent_solve/all_samples_summary.csv`
- reject_reasons_by_model.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_004733_139d04a0/agent_solver_result/agent_solve/reject_reasons_by_model.csv`
- best_solution.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_004733_139d04a0/agent_solver_result/agent_solve/best_solution.csv`
- scan_report.txt: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_004733_139d04a0/agent_solver_result/agent_solve/scan_report.txt`

============================================================================================
## Rank 10: loop_19  chi2=2482.3852
============================================================================================

### Theory Metadata

- `scalar_config`: `phi1_only`
- `potential_types`: `{"phi1": "axion", "phi2": null}`
- `sample_budget`: `1000`
- `proposal_json`: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/proposals/graph_agent_120_policy2_20260603/loop_19_initial.json`
- `agent_lagrangians.pkl`: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_000940_107d608e/agent_lagrangians.pkl`

### Raw Lagrangian From `agent_lagrangians.pkl`

```text
√(-g) [ M_p² ( \alpha Λ^{-2} · R^{ab} · R_{ab}  +  \beta Λ^{-4} · R · R^{ab} · R_{ab}  +  \gamma · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Best-Fit Coefficient-Substituted Lagrangian

```text
√(-g) [ M_p² ( (1.1001273062e-10) Λ^{-2} · R^{ab} · R_{ab}  +  (-3.1300183983e-05) Λ^{-4} · R · R^{ab} · R_{ab}  +  (0.5) · R )  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Expanded Term Contributions

Symbolic:

```text
L = √(-g) [ M_p² ( \alpha · Λ^{-2} · R^{ab} · R_{ab} ) ]
  + √(-g) [ M_p² ( \beta · Λ^{-4} · R · R^{ab} · R_{ab} ) ]
  + √(-g) [ M_p² ( \gamma · R ) ]
  + √(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ]
  + √(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

Best-fit coefficients substituted:

```text
L = √(-g) [ M_p² ( (1.1001273062e-10) · Λ^{-2} · R^{ab} · R_{ab} ) ]
  + √(-g) [ M_p² ( (-3.1300183983e-05) · Λ^{-4} · R · R^{ab} · R_{ab} ) ]
  + √(-g) [ M_p² ( (0.5) · R ) ]
  + √(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ]
  + √(-g) [ -m_1² f_1² (1 - cos(φ1/f_1)) ]
```

### Term Metadata

1. coeff `\alpha` = `1.1001273062e-10`; sector `gravity`; mass_dim `4`; Λ power `-2`; inside `M_p²(...)`: `yes`; fixed: `no`; candidate `R^{ab} · R_{ab}`
2. coeff `\beta` = `-3.1300183983e-05`; sector `gravity`; mass_dim `6`; Λ power `-4`; inside `M_p²(...)`: `yes`; fixed: `no`; candidate `R · R^{ab} · R_{ab}`
3. coeff `\gamma` = `0.5`; sector `gravity`; mass_dim `2`; Λ power `0`; inside `M_p²(...)`: `yes`; fixed: `no`; candidate `R`
4. coeff `1` = `1`; sector `matter`; mass_dim `4`; Λ power `0`; inside `M_p²(...)`: `no`; fixed: `yes`; candidate `-½ g^{μν} ∇_μφ1 ∇_νφ1`
5. coeff `1` = `1`; sector `matter`; mass_dim `4`; Λ power `0`; inside `M_p²(...)`: `no`; fixed: `yes`; candidate `-m_1² f_1² (1 - cos(φ1/f_1))`

### Fit Metrics

- chi2: `2482.3852`
- chi2 per point: `1.3542745`
- chi2_SN: `1641.4039`
- chi2_BAO: `840.9813`
- AIC: `2496.3852`
- BIC: `2534.9812`
- k_params: `7`
- max |E_N|: `2.84091627e-06`
- agent_parameter_sample_index: `90`

### Initial Conditions And Sampled Values

- H0 [km/s/Mpc]: `63.573133`
- eps_HM = H0/Mp: `5.56916045e-61`
- lambda_H = Lambda/H0: `18229.03`
- Lambda [eV]: `2.47202155e-29`
- Omega_m0: `0.26884721`
- rho_bar: `0.80654162`
- varphi1_0 = phi1_0/Mp: `3.7173942`
- q1_0 = dvarphi1/dx|0: `-0.035186717`
- mu1 = m1/H0: `0.600267`
- fbar1 = f1/Mp: `3.0312332`
- varphi2_0 = phi2_0/Lambda: `0`
- q2_0 = dvarphi2/dx|0: `0`
- mu2 = m2/Lambda: `0`
- fbar2 = f2/Lambda: `1`

### Free Coupling Values

- alpha: `1.1001273062e-10`  (proposal/catalog symbol `\alpha`)
- beta: `-3.1300183983e-05`  (proposal/catalog symbol `\beta`)
- gamma: `0.5`  (proposal/catalog symbol `\gamma`)

### Files

- Solver output directory: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_000940_107d608e/agent_solver_result/agent_solve`
- model_ranking.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_000940_107d608e/agent_solver_result/agent_solve/model_ranking.csv`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_000940_107d608e/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- all_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_000940_107d608e/agent_solver_result/agent_solve/all_samples_summary.csv`
- reject_reasons_by_model.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_000940_107d608e/agent_solver_result/agent_solve/reject_reasons_by_model.csv`
- best_solution.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_000940_107d608e/agent_solver_result/agent_solve/best_solution.csv`
- scan_report.txt: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/agent_20260603_000940_107d608e/agent_solver_result/agent_solve/scan_report.txt`
