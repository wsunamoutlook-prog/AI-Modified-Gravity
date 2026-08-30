# Signal Lab

Signal Lab is a domain-aware collection of small, composable data-processing
algorithms for optical and condensed-matter experiments.  It is deliberately
independent of the modified-gravity discovery pipeline: importing this package
does not change any theory-search settings or generated artifacts.

The package currently exposes 113 atomic algorithms in three domains:

- `general`: data hygiene, calibration, filtering, baseline removal, peak
  analysis, spectral estimation, correlation, lock-in demodulation,
  uncertainty, image registration, analytic-signal analysis, and generic
  fitting;
- `optics`: transmission/absorbance, Beer--Lambert analysis, Tauc analysis,
  Kramers--Kronig transforms, polarimetry, interferometry, fluorescence
  lifetime phasors, THz-TDS transfer functions, ellipsometry, relative quantum
  yield, image correction/deconvolution, spot/MTF analysis, and pump--probe
  normalization;
- `condensed_matter`: transport, Hall and van der Pauw analysis, transitions,
  magnetism, activated/VRH fits, calorimetry and thermal transport,
  superconducting and weak-localization fits, dielectric/impedance analysis,
  diffraction and pair-distribution transforms, XAS/photoemission processing,
  and quantum oscillations.

The catalog is broad rather than instrument-vendor specific.  Instrument file
parsers, detector calibrations, and physical models that depend on a particular
laboratory geometry should be separate adapters feeding these atomic methods.

## Agent API

Every algorithm has a stable dotted identifier and a machine-readable contract
containing required inputs, outputs, parameter schema, assumptions, caveats,
tags, and references.

```python
from signal_lab.agent_api import search, inspect, execute

matches = search("power spectral density", domain="general")
contract = inspect("spectrum.welch_psd")
result = execute(
    "spectrum.welch_psd",
    {"time": time_s, "y": voltage_v},
    {"segment_length": 2048, "window": "hann", "detrend": "constant"},
)

frequency_hz = result.values["frequency"]
psd_v2_per_hz = result.values["psd"]
```

Use `result.metadata` for provenance and `result.warnings` for method-specific
limitations.  Signal Lab never invents units; the calling agent must retain and
report them.

The same catalog is available from the command line:

```bash
python -m signal_lab list --domain optics --names-only
python -m signal_lab describe optics.tauc_linear_gap
python -m signal_lab manifest
```

An algorithm can consume an NPZ payload and produce a compressed NPZ plus a
JSON metadata sidecar:

```bash
python -m signal_lab run spectrum.welch_psd \
  --input trace.npz \
  --params '{"segment_length": 2048}' \
  --output welch_result.npz
```

## Composable Pipelines

Pipeline steps map algorithm input/output names to explicit keys in shared
state.  This makes each transformation inspectable and reproducible.

```python
from signal_lab.agent_api import execute_pipeline

processed = execute_pipeline(
    {"raw_x": wavelength_nm, "raw_y": intensity},
    [
        {
            "algorithm": "preprocess.drop_nonfinite",
            "inputs": {"x": "raw_x", "y": "raw_y"},
            "outputs": {"x": "clean_x", "y": "clean_y"},
        },
        {
            "algorithm": "baseline.asls",
            "inputs": {"x": "clean_x", "y": "clean_y"},
            "params": {"lambda": 1e6, "asymmetry": 0.01},
            "outputs": {"corrected": "signal_corrected"},
        },
        {
            "algorithm": "peaks.find",
            "inputs": {"x": "clean_x", "y": "signal_corrected"},
            "params": {"prominence": 0.05},
        },
    ],
)
```

`processed.history` records every algorithm, parameter set, state-key mapping,
warning, and metadata block.

## Catalog

### General measurement processing

- Hygiene and calibration: `preprocess.sort_axis`,
  `preprocess.drop_nonfinite`, `preprocess.crop_range`,
  `preprocess.average_repeats`, `preprocess.bin_average`,
  `preprocess.resample_uniform`, `calibration.subtract_reference`,
  `calibration.ratio_reference`, and `preprocess.normalize`.
- Baselines, outliers, and filters: `baseline.polynomial`, `baseline.asls`,
  `outlier.hampel`, `filter.savgol`, `filter.gaussian`,
  `filter.butterworth`, and `filter.notch`.
- Calculus and registration: `calculus.derivative`,
  `calculus.cumulative_integral`, and
  `alignment.cross_correlation_shift`.
- Peaks and fits: `peaks.find`, `peaks.fit_single`, `peaks.integrate`,
  `peaks.fwhm`, `fit.exponential_decay`, `fit.power_law`, and
  `fit.robust_linear`.
- Spectral/time-domain analysis: `spectrum.fft`, `spectrum.periodogram`,
  `spectrum.welch_psd`, `spectrum.lomb_scargle`, `spectrum.cross_psd`,
  `spectrum.coherence`, `time_frequency.stft`,
  `correlation.autocorrelation`, `correlation.cross_correlation`,
  `stability.allan_deviation`, `noise.power_law_exponent`,
  `lockin.demodulate`, and `lockin.xy_to_polar`.
- Uncertainty: `uncertainty.bootstrap_mean_ci`.
- Correlated uncertainty, analytic signals, image registration, and band
  integration: `statistics.block_sem`, `analytic_signal.envelope_phase`,
  `alignment.phase_correlation_2d`, and `spectrum.band_power`.

### Optics

- Radiometry/spectroscopy: `optics.dark_flat_correct`,
  `optics.transmittance_to_absorbance`,
  `optics.absorbance_to_absorption_coefficient`,
  `optics.beer_lambert_concentration`, `optics.energy_wavelength_convert`,
  `optics.raman_shift`, and `optics.rta_balance`.
- Optical-property inference: `optics.tauc_transform`,
  `optics.tauc_linear_gap`, and `optics.kk_hilbert_pair`.
- Polarization/interference: `optics.stokes_from_analyzers`,
  `optics.polarization_metrics`, `optics.malus_fit`, and
  `optics.fringe_visibility`.
- Imaging: `optics.richardson_lucy`, `optics.wiener_deconvolution`,
  `optics.spot_moments`, `optics.radial_profile`, and `optics.edge_mtf`.
- Time-resolved optics: `optics.fluorescence_phasor` and
  `optics.pump_probe_fractional_change`.
- Calibration and advanced optical measurements:
  `optics.spectral_response_correct`, `optics.relative_quantum_yield`,
  `optics.fresnel_index_from_reflectance`, `optics.ellipsometry_rho`,
  `optics.thz_transfer_function`, `optics.cavity_metrics`, and
  `optics.lifetime_mean`.

### Condensed matter

- Electrical transport: `transport.field_even_odd`,
  `transport.resistivity_geometry`, `transport.van_der_pauw`,
  `transport.hall_linear`, `transport.hall_mobility`,
  `transport.conductivity_tensor`, `transport.magnetoresistance`,
  `transport.iv_linear_resistance`, and
  `transport.differential_conductance`.
- Phase/critical behavior: `transition.resistive_tc` and
  `transition.critical_current`.
- Magnetic and thermal fits: `magnetism.hysteresis_metrics`,
  `magnetism.curie_weiss`, `thermal.arrhenius`,
  `thermal.variable_range_hopping`, `thermodynamics.debye_low_t`,
  `thermal.seebeck`, and `thermal.conductivity`.
- Structure/photoemission: `diffraction.bragg_d_spacing`,
  `diffraction.scherrer_size`, and `photoemission.shirley_baseline`.
- Quantum oscillations: `quantum_oscillation.prepare_inverse_field`,
  `quantum_oscillation.fft`, `quantum_oscillation.landau_fan`,
  `quantum_oscillation.lk_mass`, and `quantum_oscillation.dingle`.
- Multichannel and quantum transport: `transport.two_carrier_fit` and
  `quantum_transport.hln_fit`.
- Superconductivity, spectroscopy, and structure:
  `superconductivity.hc2_gl`, `spectroscopy.fano_fit`,
  `photoemission.fermi_edge`, `xas.edge_normalize`,
  `diffraction.q_from_two_theta`, `diffraction.lattice_parameter_cubic`, and
  `scattering.pair_distribution`.
- Magnetic, thermal, dielectric, and impedance transforms:
  `magnetism.demagnetization_correction`, `thermodynamics.entropy`,
  `thermal.wiedemann_franz`, `impedance.polar_to_complex`,
  `impedance.randles_fit`, and `dielectric.permittivity_from_impedance`.

## Scientific Use

1. Preserve raw data; never overwrite it with processed arrays.
2. Perform detector/reference correction before smoothing or fitting.
3. Record units, geometry, calibration constants, uncertainty model, algorithm
   versions, and all parameters.
4. Inspect assumptions and caveats before execution.  For example, FFT and
   digital-filter routines require uniform sampling, while Lomb--Scargle does
   not.
5. Compare conclusions across reasonable processing parameters and retain the
   sensitivity analysis.
6. Treat inferred gaps, lifetimes, carrier densities, masses, and similar
   quantities as model-dependent results, not direct observables.
7. Keep preprocessing and physical-model fitting as separate pipeline steps.

See [AGENT.md](AGENT.md) for agent rules and [REFERENCES.md](REFERENCES.md) for
method provenance.
