# MOCK / SYNTHETIC EXPERIMENTS ONLY

The user explicitly requested that mock data and results stay separate from all
real-observation work. This applies to every descendant directory.

- A mock fit is evaluated against a synthetic data vector, never real observations.
- Do not copy mock data into the project's `data/` directories.
- Do not write mock runs, proposals, memory, reports, or Solver results into the
  main project's corresponding directories. Use the experiment's isolated source
  workspace and an `MOCK_` run name. Never seed mock proposals with real winners.
- Do not ingest these artifacts into real-data benchmarks or real-data agent memory.
- Preserve `MOCK / SYNTHETIC` in captions, headings, filenames and exported table
  metadata. Plots must display a visible MOCK label, even if detached from this folder.
- Raw schema-sensitive files (pickles, parameter arrays, numeric LCDM caches) remain
  in marked directories with sidecar manifests; never silently remove those markers.
- Refit LCDM on this same mock before computing its delta AIC or delta BIC.
- Keep the one fixed noise seed. Do not regenerate until a preferred result appears.
- One mock searched over 250 parent theories is ONE mock realization, not 250 mocks.
- Treat exact matching to the real comparator as pending until its original settings
  and code provenance are checked. Do not invent a matching run configuration.
- This is a Gaussian fixed-covariance likelihood-level pilot for an appendix. It
  does not measure a global p-value for the original 8000-theory experiment.
- The mock exception permits the actual EOM -> Builder -> Solver pipeline to use
  synthetic data; all grammar, numerical, physical, and sampling rules still apply.
