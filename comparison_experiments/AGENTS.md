# Controlled comparisons on real observations

These experiments are separate from `mock_experiments/`. Never use mock
observations, reference fits, proposal memory, or results in these comparisons.
Every arm has its own run name and cold-start memory. Historical outputs may
be read by the comparison/report code only, never by a proposal policy.

Use an isolated source snapshot. Keep EOM, Builder, Solver, data, physical
cuts, parameter bounds, nominal AIC and sampling gates fixed. Record every
intentional proposal-policy change. Do not present a non-LLM arm as an API
model, or fixed-structure DE as a theory-search baseline. One run per arm is
a pilot, not a repeated-seed estimate of comparative performance.

The memory-off arm retains result logging and mechanical duplicate control;
it receives no past fit outcomes, learned structure prior or parameter prior.
New calculations require the selected arm and budget to be explicit. Do not
automatically submit all available arms.
