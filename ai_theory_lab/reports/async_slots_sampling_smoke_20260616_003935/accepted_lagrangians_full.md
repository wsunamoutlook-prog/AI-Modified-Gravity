# Accepted Lagrangians Full

Complete dimension-balanced Lagrangians, best-fit coefficient substitutions, metadata, and Solver paths.
Only the best chi-square representative from each accepted theory family is shown for human inspection.
The full accepted-attempt list is preserved in `accepted_summary.json`.

## 1. task_000002_slot_02_lag_1  chi2=4275.344491

- scalar_config: `both`
- proposal_group: `open_search`
- theory_track: `eh_anchored`
- potential_types: `{"phi1": "quadratic", "phi2": "axion"}`
- agent_parameter_sample_index: `3`
- H0_km_s_Mpc: `59.33164627`
- Omega_m0: `0.30621669`
- lambda_H_Lambda_over_H0: `966.44022647`
- effective_correction_status: `active`
- max_relative_effect_to_EH: `17.99321991`
- dominant_correction_term: `φ1 · ∇^{a}φ1 · ∇_{a}R`

### Raw Dimension-Balanced Lagrangian

```text
√(-g) [ M_p² ( \alpha · R  +  \beta Λ^{-4} · φ1 · ∇^{a}φ1 · ∇_{a}R  +  \gamma Λ^{-4} · φ1 · ∇^{a}∇_{a}φ1 · R  +  \delta Λ^{-4} · ∇^{a}φ1 · ∇^{b}φ1 · R_{ab} )  +  \epsilon Λ^{-2} · φ2 · φ2 · ∇^{a}φ2 · ∇_{a}φ2  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Best-Fit Lagrangian

```text
√(-g) [ M_p² ( (0.5) · R  +  (-2.9936720944e+16) Λ^{-4} · φ1 · ∇^{a}φ1 · ∇_{a}R  +  (3.1282401975e+13) Λ^{-4} · φ1 · ∇^{a}∇_{a}φ1 · R  +  (4.7853409727e+14) Λ^{-4} · ∇^{a}φ1 · ∇^{b}φ1 · R_{ab} )  +  (-9.5489345489e-04) Λ^{-2} · φ2 · φ2 · ∇^{a}φ2 · ∇_{a}φ2  +  -½ g^{μν} ∇_μφ1 ∇_νφ1  +  -½ m_1² φ1²  +  -½ g^{μν} ∇_μφ2 ∇_νφ2  +  -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms

```text
√(-g) [ M_p² ( \alpha · R ) ] +
√(-g) [ M_p² ( \beta · Λ^{-4} · φ1 · ∇^{a}φ1 · ∇_{a}R ) ] +
√(-g) [ M_p² ( \gamma · Λ^{-4} · φ1 · ∇^{a}∇_{a}φ1 · R ) ] +
√(-g) [ M_p² ( \delta · Λ^{-4} · ∇^{a}φ1 · ∇^{b}φ1 · R_{ab} ) ] +
√(-g) [ \epsilon · Λ^{-2} · φ2 · φ2 · ∇^{a}φ2 · ∇_{a}φ2 ] +
√(-g) [ -½ g^{μν} ∇_μφ1 ∇_νφ1 ] +
√(-g) [ -½ m_1² φ1² ] +
√(-g) [ -½ g^{μν} ∇_μφ2 ∇_νφ2 ] +
√(-g) [ -m_2² f_2² (1 - cos(φ2/f_2)) ]
```

### Expanded Terms With Best-Fit Coefficients

```text
√(-g) [ M_p² ( 0.5 · R ) ] +
√(-g) [ M_p² ( -2.9936720944e+16 · Λ^{-4} · φ1 · ∇^{a}φ1 · ∇_{a}R ) ] +
√(-g) [ M_p² ( 3.1282401975e+13 · Λ^{-4} · φ1 · ∇^{a}∇_{a}φ1 · R ) ] +
√(-g) [ M_p² ( 4.7853409727e+14 · Λ^{-4} · ∇^{a}φ1 · ∇^{b}φ1 · R_{ab} ) ] +
√(-g) [ -9.5489345489e-04 · Λ^{-2} · φ2 · φ2 · ∇^{a}φ2 · ∇_{a}φ2 ] +
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
    "candidate": "φ1 · ∇^{a}φ1 · ∇_{a}R",
    "mass_dim": 6,
    "lambda_power": -4,
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
    "candidate": "∇^{a}φ1 · ∇^{b}φ1 · R_{ab}",
    "mass_dim": 6,
    "lambda_power": -4,
    "sector": "non-minimal"
  },
  {
    "coeff_symbol": "\\epsilon",
    "coeff_token": "COEFF_4",
    "candidate": "φ2 · φ2 · ∇^{a}φ2 · ∇_{a}φ2",
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
  "effective_correction_status": "active",
  "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
  "max_relative_effect_to_EH": 17.99321991159788,
  "dominant_correction_term": "φ1 · ∇^{a}φ1 · ∇_{a}R",
  "active_correction_terms": 3,
  "moderate_correction_terms": 0,
  "weak_correction_terms": 0,
  "tiny_correction_terms": 0,
  "correction_term_count": 3,
  "tiny_correction_fraction": 0.0,
  "term_effects": [
    {
      "candidate": "φ1 · ∇^{a}φ1 · ∇_{a}R",
      "coeff_symbol": "\\beta",
      "coefficient": "-2.9936720943851636e+16",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 17.99321991159788,
      "effect_class": "active"
    },
    {
      "candidate": "φ1 · ∇^{a}∇_{a}φ1 · R",
      "coeff_symbol": "\\gamma",
      "coefficient": "31282401974547.13",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 0.018802030427672208,
      "effect_class": "active"
    },
    {
      "candidate": "∇^{a}φ1 · ∇^{b}φ1 · R_{ab}",
      "coeff_symbol": "\\delta",
      "coefficient": "478534097265130.1",
      "lambda_power": -4,
      "sector": "non-minimal",
      "relative_effect_to_EH": 0.28761898350319637,
      "effect_class": "active"
    }
  ]
}
```

### Output Paths

- proposal: ``
- solver output: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/async_slots_sampling_smoke_20260616_003935_task_000002_slot_02/agent_solver_result/agent_solve`
- accepted_samples_summary.csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/async_slots_sampling_smoke_20260616_003935_task_000002_slot_02/agent_solver_result/agent_solve/accepted_samples_summary.csv`
- solution csv: `/Users/sunwenrong/Desktop/AI Modified Gravity/Project/Modify GR/ai_theory_lab/runs/async_slots_sampling_smoke_20260616_003935_task_000002_slot_02/agent_solver_result/agent_solve/top_01_lagrangian_1_solution.csv`
