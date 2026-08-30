# Signal Lab Agent Guide

Signal Lab supplies atomic numerical methods.  The agent is responsible for
choosing a physically appropriate sequence, retaining provenance, and avoiding
overinterpretation.

## Required Call Pattern

```text
identify observable and units
-> search the catalog
-> inspect the algorithm contract
-> validate assumptions against acquisition metadata
-> execute one atomic step
-> inspect warnings and diagnostics
-> record the step in a pipeline history
-> perform sensitivity/uncertainty checks
```

Use `signal_lab.agent_api.search`, `inspect`, `execute`, and
`execute_pipeline`.  Do not call private implementation functions.

## Rules

- Never modify or discard the raw dataset.
- Never apply hidden smoothing, baseline subtraction, interpolation,
  normalization, clipping, or phase unwrapping.
- Make units explicit in state-key names or external metadata.  Signal Lab
  arrays are unit-neutral.
- Do not use uniformly sampled methods on irregular data without an explicit
  resampling step and a stated interpolation method.
- Do not infer a physical mechanism from a generic fit alone.  Report the
  fitted model and its assumptions.
- Keep preprocessing hyperparameters in the result history and test whether
  conclusions survive reasonable alternatives.
- Use calibration/reference correction before derived quantities.
- Preserve signs and coordinate conventions for Hall, Seebeck, polarization,
  Fourier phase, and lock-in results.
- Propagate or bootstrap uncertainty when reporting final quantities.  A fit
  without a justified error model is exploratory.
- Flag edge cases such as extrapolated baselines, truncated peaks, saturation,
  nonstationary noise, unresolved peaks, and insufficient field/temperature
  range.
- Never describe a catalog method as instrument calibration unless its
  calibration constants and geometry were supplied by the experiment.

## Selection Hints

- Uneven time samples: prefer `spectrum.lomb_scargle`; do not silently FFT.
- Stationary PSD: prefer `spectrum.welch_psd`; use `spectrum.fft` for coherent
  line amplitudes and phase.
- Slow modulated measurement: use `lockin.demodulate` and report low-pass time
  constant/equivalent bandwidth.
- Spectroscopic baseline: test `baseline.asls` against a polynomial or a
  domain-specific model; do not baseline-correct before archiving raw spectra.
- Overlapping spectral lines: fit explicit line shapes and report covariance;
  `peaks.find` is only a candidate detector.
- Optical gap: Tauc analysis requires a justified transition exponent and a
  defensible linear interval.
- Kramers--Kronig: finite spectral support needs extrapolation assumptions;
  the atomic Hilbert-pair method is a numerical building block, not a complete
  optical-constants inversion.
- Van der Pauw/Hall: verify geometry, contact quality, thickness, field
  antisymmetrization, and sign convention.
- Quantum oscillations: subtract a smooth background, transform onto uniform
  `1/B`, window explicitly, and report the field window.
- Diffraction size: Scherrer estimates coherent-domain size, not necessarily
  particle size, and requires instrumental broadening correction.
- THz-TDS: align sample/reference time zero and inspect etalon echoes before
  using `optics.thz_transfer_function`; a transfer function is not yet a
  refractive-index inversion.
- Ellipsometry: `optics.ellipsometry_rho` only constructs the measured complex
  ratio.  Select and validate a multilayer dielectric model separately.
- Two-carrier and HLN fits: try multiple initial values and field windows;
  report parameter covariance or bootstrap spread because solutions can be
  nonunique.
- XAS/PDF: normalization and Fourier transforms assume experiment-specific
  background, self-scattering, absorption, and termination corrections have
  been justified.
- Impedance: compare multiple equivalent circuits and reject parameters that
  are not identifiable over the measured frequency window.

## Adding An Algorithm

1. Implement a pure function returning `AlgorithmResult`.
2. Register it with an `AlgorithmSpec` and a stable dotted name.
3. Declare all required inputs and outputs.
4. Add a constrained parameter schema, assumptions, caveats, tags, and a
   primary or official reference.
5. Add deterministic synthetic-data tests with known ground truth.
6. Keep file parsing and plotting outside the numerical atom.
