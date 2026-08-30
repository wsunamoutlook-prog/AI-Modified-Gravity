"""Extended atomic methods spanning common optical and materials experiments."""

from __future__ import annotations

from typing import Any, Mapping

import numpy as np
from scipy import optimize, signal, special

from .model import AlgorithmResult, AlgorithmSpec, result
from .registry import algorithm
from .schemas import boolean, choice, integer, number, object_schema
from .validation import (
    SignalLabError,
    as_1d,
    as_2d,
    paired_1d,
    require_strictly_increasing,
    require_uniform_spacing,
)

E_CHARGE = 1.602176634e-19
HBAR = 1.054571817e-34
K_B_EV = 8.617333262145e-5
LORENZ_NUMBER = 2.44e-8


def _spec(
    name: str,
    domain: str,
    category: str,
    summary: str,
    inputs: tuple[str, ...],
    outputs: tuple[str, ...],
    schema: Mapping[str, Any] | None = None,
    *,
    tags: tuple[str, ...] = (),
    assumptions: tuple[str, ...] = (),
    caveats: tuple[str, ...] = (),
    references: tuple[str, ...] = (),
) -> AlgorithmSpec:
    return AlgorithmSpec(
        name=name,
        domain=domain,
        category=category,
        summary=summary,
        required_inputs=inputs,
        outputs=outputs,
        parameter_schema=schema or object_schema(),
        tags=tags,
        assumptions=assumptions,
        caveats=caveats,
        references=references,
    )


@algorithm(_spec(
    "statistics.block_sem", "general", "uncertainty",
    "Estimate a standard error from nonoverlapping block means for correlated data.",
    ("y",), ("block_means", "mean", "standard_error", "block_count"),
    object_schema({"block_size": integer(minimum=1)}, required=("block_size",)),
    tags=("blocking", "correlated-noise", "standard-error"),
    assumptions=("Blocks are long enough that their means are approximately independent.",),
    caveats=("Inspect standard error versus block size; one block size cannot prove convergence.",),
))
def block_sem(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    values = as_1d(payload["y"], "y")
    block_size = int(params["block_size"])
    count = values.size // block_size
    if count < 2:
        raise SignalLabError("block_size must leave at least two complete blocks")
    trimmed = values[: count * block_size]
    means = trimmed.reshape(count, block_size).mean(axis=1)
    return result({
        "block_means": means,
        "mean": float(np.mean(means)),
        "standard_error": float(np.std(means, ddof=1) / np.sqrt(count)),
        "block_count": count,
    }, metadata={"discarded_samples": int(values.size - trimmed.size)})


@algorithm(_spec(
    "spectrum.band_power", "general", "spectrum",
    "Integrate a one-sided PSD over a selected frequency band and return RMS.",
    ("frequency", "psd"), ("band_power", "rms", "min_frequency", "max_frequency"),
    object_schema({"min_frequency": number(minimum=0.0), "max_frequency": number(exclusive_minimum=0.0)}, required=("min_frequency", "max_frequency")),
    tags=("psd", "band-power", "rms"),
    assumptions=("PSD is one-sided and uses density scaling in signal-unit squared per Hz.",),
))
def band_power(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    frequency, psd = paired_1d(payload, "frequency", "psd")
    require_strictly_increasing(frequency, "frequency")
    lower, upper = float(params["min_frequency"]), float(params["max_frequency"])
    if upper <= lower:
        raise SignalLabError("max_frequency must exceed min_frequency")
    mask = (frequency >= lower) & (frequency <= upper) & (psd >= 0)
    if mask.sum() < 2:
        raise SignalLabError("selected band needs at least two nonnegative PSD samples")
    power = float(np.trapezoid(psd[mask], frequency[mask]))
    return result({"band_power": power, "rms": float(np.sqrt(power)), "min_frequency": lower, "max_frequency": upper})


@algorithm(_spec(
    "analytic_signal.envelope_phase", "general", "time_frequency",
    "Hilbert analytic-signal envelope, unwrapped phase, and instantaneous frequency.",
    ("time", "y"), ("envelope", "phase", "instantaneous_frequency"),
    tags=("hilbert", "envelope", "instantaneous-frequency"),
    assumptions=("Time is uniform and the trace is a sufficiently narrow-band real signal.",),
    caveats=("Instantaneous frequency is unstable where the envelope approaches zero and near record edges.",),
))
def analytic_envelope(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    time, values = paired_1d(payload, "time", "y")
    require_uniform_spacing(time, "time")
    analytic = signal.hilbert(values)
    phase = np.unwrap(np.angle(analytic))
    frequency = np.gradient(phase, time, edge_order=2) / (2.0 * np.pi)
    return result({"envelope": np.abs(analytic), "phase": phase, "instantaneous_frequency": frequency})


@algorithm(_spec(
    "alignment.phase_correlation_2d", "general", "alignment",
    "Estimate integer-pixel translation between two images by phase correlation.",
    ("reference", "moving"), ("shift_y", "shift_x", "correlation_peak", "correlation"),
    tags=("registration", "image", "phase-correlation", "drift"),
    assumptions=("Images differ primarily by cyclic translation and share contrast-producing structure.",),
    caveats=("Reported shifts are integer-pixel and cyclic; masks, rotation, scaling, or edge changes need a richer registration model.",),
))
def phase_correlation_2d(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    reference = as_2d(payload["reference"], "reference")
    moving = as_2d(payload["moving"], "moving")
    if reference.shape != moving.shape:
        raise SignalLabError("reference and moving images must have identical shapes")
    cross = np.fft.fft2(reference) * np.conj(np.fft.fft2(moving))
    magnitude = np.abs(cross)
    normalized = np.divide(cross, magnitude, out=np.zeros_like(cross), where=magnitude > 0)
    correlation = np.fft.ifft2(normalized).real
    peak = np.unravel_index(int(np.argmax(correlation)), correlation.shape)
    shift = np.asarray(peak, dtype=float)
    for axis, size in enumerate(reference.shape):
        if shift[axis] > size // 2:
            shift[axis] -= size
    return result({
        "shift_y": float(shift[0]),
        "shift_x": float(shift[1]),
        "correlation_peak": float(correlation[peak]),
        "correlation": correlation,
    })


@algorithm(_spec(
    "optics.spectral_response_correct", "optics", "calibration",
    "Divide detector counts by a calibrated spectral responsivity curve.",
    ("counts", "responsivity"), ("corrected", "valid_mask"),
    object_schema({"epsilon": number(0.0, minimum=0.0)}),
    tags=("spectrometer", "responsivity", "calibration"),
    assumptions=("Counts and responsivity share the same wavelength grid and acquisition settings are linear.",),
    caveats=("Absolute units require responsivity units, exposure, gain, collection geometry, and throughput calibration.",),
))
def spectral_response_correct(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    counts = np.asarray(payload["counts"], dtype=float)
    response = np.asarray(payload["responsivity"], dtype=float)
    if counts.shape != response.shape:
        raise SignalLabError("counts and responsivity must have identical shapes")
    valid = np.isfinite(counts) & np.isfinite(response) & (np.abs(response) > float(params.get("epsilon", 0.0)))
    corrected = np.full(counts.shape, np.nan)
    np.divide(counts, response, out=corrected, where=valid)
    return result({"corrected": corrected, "valid_mask": valid})


@algorithm(_spec(
    "optics.relative_quantum_yield", "optics", "photoluminescence",
    "Estimate sample photoluminescence quantum yield relative to a calibrated reference.",
    ("integrated_sample", "integrated_reference"), ("quantum_yield",),
    object_schema({
        "reference_quantum_yield": number(exclusive_minimum=0.0, maximum=1.0),
        "sample_absorbance": number(exclusive_minimum=0.0),
        "reference_absorbance": number(exclusive_minimum=0.0),
        "sample_refractive_index": number(1.0, exclusive_minimum=0.0),
        "reference_refractive_index": number(1.0, exclusive_minimum=0.0),
    }, required=("reference_quantum_yield", "sample_absorbance", "reference_absorbance")),
    tags=("photoluminescence", "quantum-yield", "relative-method"),
    assumptions=("Sample and reference spectra are instrument-response corrected and measured in matched linear geometry.",),
    caveats=("Reabsorption, inner-filter effects, scattering, concentration, and spectral mismatch can dominate the uncertainty.",),
))
def relative_quantum_yield(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    sample = np.asarray(payload["integrated_sample"], dtype=float)
    reference = np.asarray(payload["integrated_reference"], dtype=float)
    if np.any(reference == 0):
        raise SignalLabError("integrated_reference contains zero")
    absorb_sample = 1.0 - 10.0 ** (-float(params["sample_absorbance"]))
    absorb_reference = 1.0 - 10.0 ** (-float(params["reference_absorbance"]))
    if absorb_sample <= 0:
        raise SignalLabError("sample absorbed fraction is zero")
    refractive_factor = (float(params.get("sample_refractive_index", 1.0)) / float(params.get("reference_refractive_index", 1.0))) ** 2
    quantum_yield = float(params["reference_quantum_yield"]) * sample / reference * absorb_reference / absorb_sample * refractive_factor
    return result({"quantum_yield": quantum_yield})


@algorithm(_spec(
    "optics.fresnel_index_from_reflectance", "optics", "optical_constants",
    "Infer a real refractive index from normal-incidence reflectance for a nonabsorbing interface.",
    ("reflectance",), ("refractive_index", "valid_mask"),
    object_schema({"ambient_index": number(1.0, exclusive_minimum=0.0)}),
    tags=("fresnel", "reflectance", "refractive-index"),
    assumptions=("Normal incidence, semi-infinite nonabsorbing sample, smooth interface, and known ambient index.",),
    caveats=("Absorption, thin-film interference, roughness, and multilayers invalidate this inversion.",),
))
def fresnel_index(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    reflectance = np.asarray(payload["reflectance"], dtype=float)
    valid = np.isfinite(reflectance) & (reflectance >= 0) & (reflectance < 1)
    refractive = np.full(reflectance.shape, np.nan)
    root = np.sqrt(reflectance[valid])
    refractive[valid] = float(params.get("ambient_index", 1.0)) * (1.0 + root) / (1.0 - root)
    return result({"refractive_index": refractive, "valid_mask": valid})


@algorithm(_spec(
    "optics.ellipsometry_rho", "optics", "ellipsometry",
    "Convert ellipsometric Psi and Delta to the complex reflection ratio rho=tan(Psi) exp(i Delta).",
    ("psi", "delta"), ("rho_real", "rho_imag", "rho_magnitude", "rho_phase"),
    object_schema({"angle_unit": choice("degree", ("degree", "radian"))}),
    tags=("ellipsometry", "psi", "delta", "reflection-ratio"),
    caveats=("Inferring thickness or dielectric functions from rho requires an explicit multilayer optical model.",),
))
def ellipsometry_rho(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    psi = np.asarray(payload["psi"], dtype=float)
    delta = np.asarray(payload["delta"], dtype=float)
    if psi.shape != delta.shape:
        raise SignalLabError("psi and delta must have identical shapes")
    if params.get("angle_unit", "degree") == "degree":
        psi, delta = np.radians(psi), np.radians(delta)
    rho = np.tan(psi) * np.exp(1j * delta)
    return result({"rho_real": rho.real, "rho_imag": rho.imag, "rho_magnitude": np.abs(rho), "rho_phase": np.angle(rho)})


@algorithm(_spec(
    "optics.thz_transfer_function", "optics", "terahertz",
    "Compute the complex THz-TDS sample/reference transfer function.",
    ("time", "sample", "reference"), ("frequency", "transfer", "amplitude", "phase", "valid_mask"),
    object_schema({"window": choice("tukey", ("tukey", "hann", "none")), "tukey_alpha": number(0.1, minimum=0.0, maximum=1.0), "epsilon": number(1e-12, exclusive_minimum=0.0)}),
    tags=("thz-tds", "transfer-function", "phase", "spectroscopy"),
    assumptions=("Sample and reference traces share timing, sampling, polarization, and acquisition response.",),
    caveats=("Time-zero drift, etalon echoes, windowing, and phase unwrapping must be handled before material inversion.",),
))
def thz_transfer(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    time = as_1d(payload["time"], "time")
    sample = as_1d(payload["sample"], "sample")
    reference = as_1d(payload["reference"], "reference")
    if not (time.size == sample.size == reference.size):
        raise SignalLabError("time, sample, and reference must have equal length")
    step = require_uniform_spacing(time, "time")
    window_name = params.get("window", "tukey")
    if window_name == "none":
        window = np.ones(time.size)
    elif window_name == "tukey":
        window = signal.windows.tukey(time.size, alpha=float(params.get("tukey_alpha", 0.1)))
    else:
        window = signal.windows.hann(time.size)
    sample_fft = np.fft.rfft(sample * window)
    reference_fft = np.fft.rfft(reference * window)
    valid = np.abs(reference_fft) > float(params.get("epsilon", 1e-12))
    transfer = np.full(sample_fft.shape, np.nan + 1j * np.nan)
    np.divide(sample_fft, reference_fft, out=transfer, where=valid)
    return result({
        "frequency": np.fft.rfftfreq(time.size, d=step),
        "transfer": transfer,
        "amplitude": np.abs(transfer),
        "phase": np.unwrap(np.angle(transfer)),
        "valid_mask": valid,
    }, metadata={"window": window_name})


@algorithm(_spec(
    "optics.cavity_metrics", "optics", "resonator",
    "Compute finesse and quality factor from free spectral range and linewidth.",
    ("free_spectral_range", "linewidth", "resonance_frequency"), ("finesse", "quality_factor"),
    tags=("cavity", "resonator", "finesse", "quality-factor"),
    assumptions=("FSR, linewidth, and resonance frequency use the same frequency unit and linewidth is FWHM.",),
    caveats=("Instrument resolution and unresolved mode splitting broaden measured linewidths.",),
))
def cavity_metrics(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    fsr = np.asarray(payload["free_spectral_range"], dtype=float)
    linewidth = np.asarray(payload["linewidth"], dtype=float)
    resonance = np.asarray(payload["resonance_frequency"], dtype=float)
    if not (fsr.shape == linewidth.shape == resonance.shape):
        raise SignalLabError("cavity inputs must have identical shapes")
    if np.any(linewidth <= 0):
        raise SignalLabError("linewidth must be positive")
    return result({"finesse": fsr / linewidth, "quality_factor": resonance / linewidth})


@algorithm(_spec(
    "optics.lifetime_mean", "optics", "lifetime",
    "Compute intensity-weighted mean arrival time after optional constant-background subtraction.",
    ("time", "counts"), ("mean_lifetime", "integrated_counts"),
    object_schema({"background": number(0.0), "time_zero": number(0.0)}),
    tags=("lifetime", "tcspc", "first-moment"),
    assumptions=("The instrument response and truncation are negligible or separately corrected.",),
    caveats=("The mean is not a unique exponential lifetime for mixtures and is biased by background and finite windows.",),
))
def lifetime_mean(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    time, counts = paired_1d(payload, "time", "counts")
    corrected = np.clip(counts - float(params.get("background", 0.0)), 0.0, None)
    total = float(np.trapezoid(corrected, time))
    if total <= 0:
        raise SignalLabError("background-subtracted integrated counts must be positive")
    shifted = time - float(params.get("time_zero", 0.0))
    mean = float(np.trapezoid(shifted * corrected, time) / total)
    return result({"mean_lifetime": mean, "integrated_counts": total})


@algorithm(_spec(
    "transport.two_carrier_fit", "condensed_matter", "transport",
    "Jointly fit rho_xx(B) and rho_xy(B) to a classical electron-hole two-carrier model.",
    ("field", "rho_xx", "rho_xy"), ("electron_density_m3", "hole_density_m3", "electron_mobility_m2_per_vs", "hole_mobility_m2_per_vs", "rho_xx_fit", "rho_xy_fit", "cost"),
    object_schema({
        "initial_electron_density_m3": number(exclusive_minimum=0.0),
        "initial_hole_density_m3": number(exclusive_minimum=0.0),
        "initial_electron_mobility_m2_per_vs": number(exclusive_minimum=0.0),
        "initial_hole_mobility_m2_per_vs": number(exclusive_minimum=0.0),
    }, required=("initial_electron_density_m3", "initial_hole_density_m3", "initial_electron_mobility_m2_per_vs", "initial_hole_mobility_m2_per_vs")),
    tags=("hall", "two-carrier", "multiband", "magnetoresistance"),
    assumptions=("One electron-like and one hole-like Drude channel with field-independent densities and mobilities dominate.",),
    caveats=("The fit is often nonunique; use multiple initializations, parameter bounds, uncertainty, and independent rho_xx/rho_xy calibration.",),
))
def two_carrier_fit(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    field = as_1d(payload["field"], "field")
    rho_xx = as_1d(payload["rho_xx"], "rho_xx")
    rho_xy = as_1d(payload["rho_xy"], "rho_xy")
    if not (field.size == rho_xx.size == rho_xy.size):
        raise SignalLabError("field, rho_xx, and rho_xy must have equal length")
    scale_xx = max(float(np.ptp(rho_xx)), float(np.median(np.abs(rho_xx))), np.finfo(float).eps)
    scale_xy = max(float(np.ptp(rho_xy)), float(np.median(np.abs(rho_xy))), np.finfo(float).eps)

    def model(log_values: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        ne, nh, mue, muh = np.exp(log_values)
        electron = 1.0 + (mue * field) ** 2
        hole = 1.0 + (muh * field) ** 2
        sigma_xx = E_CHARGE * (ne * mue / electron + nh * muh / hole)
        sigma_xy = E_CHARGE * field * (-ne * mue**2 / electron + nh * muh**2 / hole)
        denominator = sigma_xx**2 + sigma_xy**2
        return sigma_xx / denominator, -sigma_xy / denominator

    initial = np.log([
        float(params["initial_electron_density_m3"]),
        float(params["initial_hole_density_m3"]),
        float(params["initial_electron_mobility_m2_per_vs"]),
        float(params["initial_hole_mobility_m2_per_vs"]),
    ])

    def residual(log_values: np.ndarray) -> np.ndarray:
        predicted_xx, predicted_xy = model(log_values)
        return np.concatenate(((predicted_xx - rho_xx) / scale_xx, (predicted_xy - rho_xy) / scale_xy))

    # Finite log-space bounds avoid overflow while remaining much broader than
    # realistic solid-state carrier densities and mobilities.
    lower = np.log([1e6, 1e6, 1e-12, 1e-12])
    upper = np.log([1e34, 1e34, 1e5, 1e5])
    fitted = optimize.least_squares(
        residual,
        initial,
        bounds=(lower, upper),
        loss="soft_l1",
        max_nfev=30000,
    )
    ne, nh, mue, muh = np.exp(fitted.x)
    fit_xx, fit_xy = model(fitted.x)
    return result({
        "electron_density_m3": float(ne),
        "hole_density_m3": float(nh),
        "electron_mobility_m2_per_vs": float(mue),
        "hole_mobility_m2_per_vs": float(muh),
        "rho_xx_fit": fit_xx,
        "rho_xy_fit": fit_xy,
        "cost": float(fitted.cost),
    }, metadata={"success": bool(fitted.success), "message": fitted.message})


@algorithm(_spec(
    "quantum_transport.hln_fit", "condensed_matter", "quantum_transport",
    "Fit low-field magnetoconductance to the single-channel Hikami-Larkin-Nagaoka form.",
    ("field", "delta_conductivity"), ("alpha", "phase_coherence_length_m", "phase_field_t", "fit", "cost"),
    object_schema({"initial_alpha": number(-0.5), "initial_phase_coherence_length_m": number(1e-7, exclusive_minimum=0.0), "max_abs_field": number(exclusive_minimum=0.0)}),
    tags=("weak-antilocalization", "wal", "hln", "phase-coherence"),
    assumptions=("A two-dimensional diffusive single-channel HLN correction applies in the selected low-field interval.",),
    caveats=("Spin-orbit, magnetic scattering, multichannel transport, classical backgrounds, and sign conventions may require generalized models.",),
    references=("Hikami, Larkin, and Nagaoka, Prog. Theor. Phys. 63, 707 (1980)",),
))
def hln_fit(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    field, conductivity = paired_1d(payload, "field", "delta_conductivity")
    mask = np.isfinite(field) & np.isfinite(conductivity) & (np.abs(field) > 0)
    if "max_abs_field" in params:
        mask &= np.abs(field) <= float(params["max_abs_field"])
    if mask.sum() < 6:
        raise SignalLabError("HLN fit needs at least six nonzero-field samples")
    selected_field = np.abs(field[mask])
    prefactor = E_CHARGE**2 / (2.0 * np.pi**2 * HBAR)

    def model(alpha: float, length: float) -> np.ndarray:
        bphi = HBAR / (4.0 * E_CHARGE * length**2)
        ratio = bphi / selected_field
        return alpha * prefactor * (special.digamma(0.5 + ratio) - np.log(ratio))

    initial_alpha = float(params.get("initial_alpha", -0.5))
    initial_length = float(params.get("initial_phase_coherence_length_m", 1e-7))
    scale = max(float(np.ptp(conductivity[mask])), float(np.max(np.abs(conductivity[mask]))), np.finfo(float).eps)
    fitted = optimize.least_squares(
        lambda values: (model(values[0], np.exp(values[1])) - conductivity[mask]) / scale,
        [initial_alpha, np.log(initial_length)],
        bounds=([-100.0, np.log(1e-12)], [100.0, np.log(1e-2)]),
        loss="soft_l1",
        max_nfev=30000,
    )
    alpha, length = float(fitted.x[0]), float(np.exp(fitted.x[1]))
    bphi = HBAR / (4.0 * E_CHARGE * length**2)
    return result({"alpha": alpha, "phase_coherence_length_m": length, "phase_field_t": float(bphi), "fit": model(alpha, length), "cost": float(fitted.cost)}, metadata={"kept_mask": mask, "success": bool(fitted.success)})


@algorithm(_spec(
    "superconductivity.hc2_gl", "condensed_matter", "superconductivity",
    "Fit Hc2(T)=Hc2(0)[1-(T/Tc)^2]/[1+(T/Tc)^2].",
    ("temperature", "critical_field"), ("hc2_zero", "tc", "coherence_length_zero_m", "fit", "covariance"),
    tags=("superconductivity", "upper-critical-field", "ginsburg-landau", "coherence-length"),
    assumptions=("The phenomenological Ginzburg-Landau interpolation describes the measured Hc2 branch.",),
    caveats=("WHH, Pauli limiting, anisotropy, multiband effects, and criterion choice may require different models.",),
))
def hc2_gl(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    temperature, critical_field = paired_1d(payload, "temperature", "critical_field")

    def model(t: np.ndarray, hc20: float, tc: float) -> np.ndarray:
        reduced = t / tc
        return hc20 * (1.0 - reduced**2) / (1.0 + reduced**2)

    p0 = [max(float(np.max(critical_field)), np.finfo(float).eps), max(float(np.max(temperature)) * 1.05, np.finfo(float).eps)]
    fitted, covariance = optimize.curve_fit(model, temperature, critical_field, p0=p0, bounds=([0.0, np.max(temperature)], [np.inf, np.inf]), maxfev=30000)
    flux_quantum = np.pi * HBAR / E_CHARGE
    coherence = np.sqrt(flux_quantum / (2.0 * np.pi * fitted[0])) if fitted[0] > 0 else np.nan
    return result({"hc2_zero": float(fitted[0]), "tc": float(fitted[1]), "coherence_length_zero_m": float(coherence), "fit": model(temperature, *fitted), "covariance": covariance})


@algorithm(_spec(
    "photoemission.fermi_edge", "condensed_matter", "photoemission",
    "Fit a Fermi-Dirac edge with an effective temperature and affine intensity scale.",
    ("energy_ev", "intensity"), ("fermi_energy_ev", "effective_temperature_k", "amplitude", "offset", "fit", "covariance"),
    tags=("arpes", "xps", "fermi-edge", "energy-calibration"),
    assumptions=("One Fermi edge dominates and instrumental resolution is negligible or absorbed into an effective temperature.",),
    caveats=("Publication-grade temperature or resolution extraction requires convolution with the measured resolution function and a background model.",),
))
def fermi_edge(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    energy, intensity = paired_1d(payload, "energy_ev", "intensity")

    def model(e: np.ndarray, offset: float, amplitude: float, ef: float, temperature: float) -> np.ndarray:
        argument = np.clip((e - ef) / (K_B_EV * temperature), -700.0, 700.0)
        return offset + amplitude / (1.0 + np.exp(argument))

    midpoint = float(energy[np.argmin(np.abs(intensity - 0.5 * (np.max(intensity) + np.min(intensity))))])
    initial = [float(np.min(intensity)), float(np.ptp(intensity)), midpoint, 20.0]
    fitted, covariance = optimize.curve_fit(model, energy, intensity, p0=initial, bounds=([-np.inf, -np.inf, energy.min(), 1e-3], [np.inf, np.inf, energy.max(), 1e5]), maxfev=30000)
    return result({"fermi_energy_ev": float(fitted[2]), "effective_temperature_k": float(fitted[3]), "amplitude": float(fitted[1]), "offset": float(fitted[0]), "fit": model(energy, *fitted), "covariance": covariance})


@algorithm(_spec(
    "spectroscopy.fano_fit", "condensed_matter", "spectroscopy",
    "Fit a Fano resonance plus linear background.",
    ("x", "y"), ("center", "fwhm", "q", "amplitude", "offset", "slope", "fit", "covariance"),
    tags=("fano", "raman", "infrared", "resonance", "lineshape"),
    assumptions=("One isolated Fano resonance and an approximately linear background describe the selected interval.",),
    caveats=("Fano parameter signs and amplitudes depend on the chosen normalization and background.",),
))
def fano_fit(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    x, y = paired_1d(payload, "x", "y")
    require_strictly_increasing(x)

    def model(axis: np.ndarray, amplitude: float, center: float, width: float, q: float, offset: float, slope: float) -> np.ndarray:
        epsilon = 2.0 * (axis - center) / width
        return offset + slope * (axis - center) + amplitude * (q + epsilon) ** 2 / (1.0 + epsilon**2)

    p0 = [float(np.ptp(y)), float(x[np.argmax(y)]), max(float(np.ptp(x) / 10.0), np.finfo(float).eps), 1.0, float(np.min(y)), 0.0]
    fitted, covariance = optimize.curve_fit(model, x, y, p0=p0, bounds=([-np.inf, x.min(), np.finfo(float).eps, -100.0, -np.inf, -np.inf], [np.inf, x.max(), np.inf, 100.0, np.inf, np.inf]), maxfev=50000)
    return result({"center": float(fitted[1]), "fwhm": float(fitted[2]), "q": float(fitted[3]), "amplitude": float(fitted[0]), "offset": float(fitted[4]), "slope": float(fitted[5]), "fit": model(x, *fitted), "covariance": covariance})


@algorithm(_spec(
    "diffraction.q_from_two_theta", "condensed_matter", "diffraction",
    "Convert diffraction angle 2theta to momentum-transfer magnitude Q=4 pi sin(theta)/lambda.",
    ("two_theta_degree",), ("q",),
    object_schema({"wavelength": number(exclusive_minimum=0.0)}, required=("wavelength",)),
    tags=("xrd", "neutron", "scattering", "momentum-transfer"),
    assumptions=("Wavelength and output Q use reciprocal length units consistently.",),
))
def q_from_two_theta(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    angle = np.radians(np.asarray(payload["two_theta_degree"], dtype=float) / 2.0)
    return result({"q": 4.0 * np.pi * np.sin(angle) / float(params["wavelength"])})


@algorithm(_spec(
    "diffraction.lattice_parameter_cubic", "condensed_matter", "diffraction",
    "Infer a cubic lattice parameter from d spacing and Miller indices.",
    ("d_spacing", "h", "k", "l"), ("lattice_parameter",),
    tags=("xrd", "lattice-parameter", "miller-index", "cubic"),
    assumptions=("The reflection belongs to a cubic phase and d spacing is calibrated.",),
))
def cubic_lattice_parameter(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    d = np.asarray(payload["d_spacing"], dtype=float)
    h = np.asarray(payload["h"], dtype=float)
    k = np.asarray(payload["k"], dtype=float)
    l = np.asarray(payload["l"], dtype=float)
    if not (d.shape == h.shape == k.shape == l.shape):
        raise SignalLabError("d_spacing and Miller-index arrays must have identical shapes")
    norm = h**2 + k**2 + l**2
    if np.any(d <= 0) or np.any(norm <= 0):
        raise SignalLabError("d spacing and Miller-index norm must be positive")
    return result({"lattice_parameter": d * np.sqrt(norm)})


@algorithm(_spec(
    "scattering.pair_distribution", "condensed_matter", "scattering",
    "Sine-transform S(Q) into the reduced pair-distribution function G(r).",
    ("q", "structure_factor"), ("r", "g_reduced"),
    object_schema({"r_min": number(0.0, minimum=0.0), "r_max": number(exclusive_minimum=0.0), "r_points": integer(1000, minimum=16), "lorch_window": boolean(True)}, required=("r_max",)),
    tags=("pdf", "total-scattering", "structure-factor", "fourier-transform"),
    assumptions=("Q is calibrated and S(Q) is normalized with appropriate self-scattering/background corrections.",),
    caveats=("Finite Q range, termination ripples, composition weights, and normalization dominate quantitative PDF interpretation.",),
))
def pair_distribution(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    q, sq = paired_1d(payload, "q", "structure_factor")
    order = np.argsort(q)
    q, sq = q[order], sq[order]
    require_strictly_increasing(q, "q")
    if np.any(q < 0):
        raise SignalLabError("q must be nonnegative")
    r_min, r_max = float(params.get("r_min", 0.0)), float(params["r_max"])
    if r_max <= r_min:
        raise SignalLabError("r_max must exceed r_min")
    r = np.linspace(r_min, r_max, int(params.get("r_points", 1000)))
    fq = q * (sq - 1.0)
    if bool(params.get("lorch_window", True)) and q[-1] > 0:
        argument = np.pi * q / q[-1]
        window = np.divide(np.sin(argument), argument, out=np.ones_like(argument), where=argument != 0)
        fq = fq * window
    transformed = (2.0 / np.pi) * np.trapezoid(fq[:, None] * np.sin(q[:, None] * r[None, :]), q, axis=0)
    return result({"r": r, "g_reduced": transformed})


@algorithm(_spec(
    "magnetism.demagnetization_correction", "condensed_matter", "magnetism",
    "Compute SI internal field H_int=H_applied-NM and internal susceptibility.",
    ("applied_field_a_per_m", "magnetization_a_per_m"), ("internal_field_a_per_m", "internal_susceptibility"),
    object_schema({"demagnetization_factor": number(minimum=0.0, maximum=1.0)}, required=("demagnetization_factor",)),
    tags=("demagnetization", "internal-field", "susceptibility"),
    assumptions=("A uniform ellipsoidal-sample demagnetization factor in SI units is appropriate.",),
    caveats=("Nonellipsoidal shapes and spatially nonuniform magnetization require numerical magnetostatics.",),
))
def demagnetization_correction(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    applied = np.asarray(payload["applied_field_a_per_m"], dtype=float)
    magnetization = np.asarray(payload["magnetization_a_per_m"], dtype=float)
    if applied.shape != magnetization.shape:
        raise SignalLabError("applied field and magnetization must have identical shapes")
    internal = applied - float(params["demagnetization_factor"]) * magnetization
    susceptibility = np.divide(magnetization, internal, out=np.full(internal.shape, np.nan), where=internal != 0)
    return result({"internal_field_a_per_m": internal, "internal_susceptibility": susceptibility})


@algorithm(_spec(
    "thermodynamics.entropy", "condensed_matter", "thermodynamics",
    "Integrate C/T over temperature to obtain entropy change.",
    ("temperature", "heat_capacity"), ("temperature", "entropy_change"),
    object_schema({"initial_entropy": number(0.0)}),
    tags=("entropy", "heat-capacity", "phase-transition"),
    assumptions=("Heat capacity and temperature use consistent molar or extensive units and the low-temperature extrapolation is supplied separately.",),
    caveats=("Missing low-temperature data produce an unknown additive entropy contribution.",),
))
def entropy_from_heat_capacity(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    temperature, capacity = paired_1d(payload, "temperature", "heat_capacity")
    order = np.argsort(temperature)
    temperature, capacity = temperature[order], capacity[order]
    require_strictly_increasing(temperature, "temperature")
    if np.any(temperature <= 0):
        raise SignalLabError("temperature must be positive")
    integrand = capacity / temperature
    increments = 0.5 * (integrand[1:] + integrand[:-1]) * np.diff(temperature)
    entropy = float(params.get("initial_entropy", 0.0)) + np.concatenate(([0.0], np.cumsum(increments)))
    return result({"temperature": temperature, "entropy_change": entropy})


@algorithm(_spec(
    "thermal.wiedemann_franz", "condensed_matter", "thermoelectric",
    "Estimate electronic thermal conductivity kappa_e=L*T/rho.",
    ("temperature", "resistivity"), ("electronic_thermal_conductivity",),
    object_schema({"lorenz_number": number(LORENZ_NUMBER, exclusive_minimum=0.0)}),
    tags=("wiedemann-franz", "thermal-conductivity", "resistivity"),
    assumptions=("Resistivity is in ohm meter, temperature in kelvin, and the selected Lorenz number applies.",),
    caveats=("Inelastic scattering, non-Fermi-liquid behavior, superconductivity, and multiband effects can violate the Sommerfeld Lorenz number.",),
))
def wiedemann_franz(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    temperature = np.asarray(payload["temperature"], dtype=float)
    resistivity = np.asarray(payload["resistivity"], dtype=float)
    if temperature.shape != resistivity.shape:
        raise SignalLabError("temperature and resistivity must have identical shapes")
    if np.any(temperature < 0) or np.any(resistivity <= 0):
        raise SignalLabError("temperature must be nonnegative and resistivity positive")
    return result({"electronic_thermal_conductivity": float(params.get("lorenz_number", LORENZ_NUMBER)) * temperature / resistivity})


@algorithm(_spec(
    "xas.edge_normalize", "condensed_matter", "xray_spectroscopy",
    "Fit pre/post-edge polynomials and normalize an absorption edge.",
    ("energy_ev", "mu"), ("normalized", "pre_edge", "post_edge", "edge_step", "valid_mask"),
    object_schema({"pre_min": number(), "pre_max": number(), "post_min": number(), "post_max": number(), "pre_degree": integer(1, minimum=0, maximum=3), "post_degree": integer(2, minimum=0, maximum=5)}, required=("pre_min", "pre_max", "post_min", "post_max")),
    tags=("xas", "xanes", "exafs", "edge-normalization"),
    assumptions=("Selected pre/post-edge intervals are free of other edges and support the polynomial orders.",),
    caveats=("EXAFS extraction additionally requires E0 selection, background spline, k conversion, and self-absorption checks.",),
))
def xas_edge_normalize(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    energy, mu = paired_1d(payload, "energy_ev", "mu")
    order = np.argsort(energy)
    energy, mu = energy[order], mu[order]
    pre_mask = (energy >= float(params["pre_min"])) & (energy <= float(params["pre_max"]))
    post_mask = (energy >= float(params["post_min"])) & (energy <= float(params["post_max"]))
    pre_degree, post_degree = int(params.get("pre_degree", 1)), int(params.get("post_degree", 2))
    if pre_mask.sum() <= pre_degree or post_mask.sum() <= post_degree:
        raise SignalLabError("pre/post-edge intervals need more samples than polynomial degree")
    pre = np.polyval(np.polyfit(energy[pre_mask], mu[pre_mask], pre_degree), energy)
    post = np.polyval(np.polyfit(energy[post_mask], mu[post_mask], post_degree), energy)
    step = post - pre
    valid = np.isfinite(step) & (np.abs(step) > np.finfo(float).eps)
    normalized = np.full(mu.shape, np.nan)
    normalized[valid] = (mu[valid] - pre[valid]) / step[valid]
    inverse = np.argsort(order)
    return result({"normalized": normalized[inverse], "pre_edge": pre[inverse], "post_edge": post[inverse], "edge_step": step[inverse], "valid_mask": valid[inverse]})


@algorithm(_spec(
    "impedance.polar_to_complex", "condensed_matter", "impedance",
    "Convert impedance magnitude and phase into real and imaginary components.",
    ("magnitude", "phase"), ("z_real", "z_imag"),
    object_schema({"angle_unit": choice("degree", ("degree", "radian"))}),
    tags=("impedance", "eis", "nyquist", "phase"),
    caveats=("Confirm whether the instrument reports negative phase for capacitive impedance.",),
))
def impedance_polar_to_complex(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    magnitude = np.asarray(payload["magnitude"], dtype=float)
    phase = np.asarray(payload["phase"], dtype=float)
    if magnitude.shape != phase.shape:
        raise SignalLabError("magnitude and phase must have identical shapes")
    if params.get("angle_unit", "degree") == "degree":
        phase = np.radians(phase)
    return result({"z_real": magnitude * np.cos(phase), "z_imag": magnitude * np.sin(phase)})


@algorithm(_spec(
    "impedance.randles_fit", "condensed_matter", "impedance",
    "Fit a simple Randles circuit Rs + (Rct parallel Cdl) to complex impedance.",
    ("frequency_hz", "z_real", "z_imag"), ("series_resistance", "charge_transfer_resistance", "double_layer_capacitance_f", "z_real_fit", "z_imag_fit", "cost"),
    tags=("impedance", "eis", "randles", "equivalent-circuit"),
    assumptions=("A series resistance and one ideal parallel R-C time constant describe the spectrum.",),
    caveats=("Equivalent circuits are nonunique; diffusion, constant-phase elements, inductance, and distributed relaxation require richer models.",),
))
def randles_fit(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    frequency = as_1d(payload["frequency_hz"], "frequency_hz")
    z_real = as_1d(payload["z_real"], "z_real")
    z_imag = as_1d(payload["z_imag"], "z_imag")
    if not (frequency.size == z_real.size == z_imag.size) or np.any(frequency <= 0):
        raise SignalLabError("positive frequency, z_real, and z_imag must have equal length")
    rs0 = max(float(np.min(z_real)), np.finfo(float).eps)
    rct0 = max(float(np.max(z_real) - rs0), rs0 * 0.1)
    peak_index = int(np.argmax(np.abs(z_imag)))
    c0 = 1.0 / (2.0 * np.pi * frequency[peak_index] * rct0)

    def model(log_values: np.ndarray) -> np.ndarray:
        rs, rct, capacitance = np.exp(log_values)
        omega = 2.0 * np.pi * frequency
        impedance = rs + rct / (1.0 + 1j * omega * rct * capacitance)
        return impedance

    scale = max(float(np.max(np.abs(z_real + 1j * z_imag))), np.finfo(float).eps)
    fitted = optimize.least_squares(
        lambda values: np.concatenate(
            ((model(values).real - z_real) / scale, (model(values).imag - z_imag) / scale)
        ),
        np.log([rs0, rct0, c0]),
        bounds=(np.log([1e-15, 1e-15, 1e-18]), np.log([1e15, 1e15, 1e6])),
        loss="soft_l1",
        max_nfev=30000,
    )
    rs, rct, capacitance = np.exp(fitted.x)
    impedance = model(fitted.x)
    return result({"series_resistance": float(rs), "charge_transfer_resistance": float(rct), "double_layer_capacitance_f": float(capacitance), "z_real_fit": impedance.real, "z_imag_fit": impedance.imag, "cost": float(fitted.cost)}, metadata={"success": bool(fitted.success)})


@algorithm(_spec(
    "dielectric.permittivity_from_impedance", "condensed_matter", "dielectric",
    "Convert complex impedance into relative permittivity using an empty-cell capacitance.",
    ("frequency_hz", "z_real", "z_imag"), ("epsilon_real", "epsilon_loss", "loss_tangent"),
    object_schema({"empty_cell_capacitance_f": number(exclusive_minimum=0.0)}, required=("empty_cell_capacitance_f",)),
    tags=("dielectric", "permittivity", "impedance", "loss-tangent"),
    assumptions=("Parallel-plate empty-cell capacitance captures sample geometry and the exp(+i omega t) convention is used.",),
    caveats=("Electrode polarization, contact impedance, leakage, fringing, and convention changes can dominate low-frequency permittivity.",),
))
def permittivity_from_impedance(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    frequency = as_1d(payload["frequency_hz"], "frequency_hz")
    z_real = as_1d(payload["z_real"], "z_real")
    z_imag = as_1d(payload["z_imag"], "z_imag")
    if not (frequency.size == z_real.size == z_imag.size) or np.any(frequency <= 0):
        raise SignalLabError("positive frequency, z_real, and z_imag must have equal length")
    impedance = z_real + 1j * z_imag
    if np.any(impedance == 0):
        raise SignalLabError("impedance contains zero")
    epsilon = 1.0 / (1j * 2.0 * np.pi * frequency * float(params["empty_cell_capacitance_f"]) * impedance)
    epsilon_real = epsilon.real
    epsilon_loss = -epsilon.imag
    loss_tangent = np.divide(epsilon_loss, epsilon_real, out=np.full(epsilon_real.shape, np.nan), where=epsilon_real != 0)
    return result({"epsilon_real": epsilon_real, "epsilon_loss": epsilon_loss, "loss_tangent": loss_tangent})
