"""Atomic algorithms for optical spectroscopy, polarization, and imaging."""

from __future__ import annotations

from typing import Any, Mapping

import numpy as np
from scipy import optimize, signal

from .model import AlgorithmResult, AlgorithmSpec, result
from .registry import algorithm
from .schemas import boolean, choice, integer, number, object_schema
from .validation import SignalLabError, as_1d, as_2d, paired_1d, require_strictly_increasing, require_uniform_spacing

PHASOR_REF = "Digman et al., Biophys. J. 94, L14 (2008), doi:10.1529/biophysj.107.120154"
RL_REF = "Richardson-Lucy implementation discussion, A&A 540, A80 (2012), https://www.aanda.org/articles/aa/full_html/2012/03/aa18681-11/aa18681-11.html"
NIST_POL_REF = "NIST Technical Note 1622, Spectrophotometry and polarimetry, https://www.govinfo.gov/content/pkg/GOVPUB-C13-283cba0d329737c161c3a4d73a039cff/pdf/GOVPUB-C13-283cba0d329737c161c3a4d73a039cff.pdf"
KK_REF = "Kuzmenko, Rev. Sci. Instrum. 76, 083108 (2005), arXiv:cond-mat/0503565"


def _spec(
    name: str,
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
        name=name, domain="optics", category=category, summary=summary,
        required_inputs=inputs, outputs=outputs,
        parameter_schema=schema or object_schema(), tags=tags,
        assumptions=assumptions, caveats=caveats, references=references,
    )


@algorithm(_spec(
    "optics.dark_flat_correct", "calibration", "Apply dark subtraction and flat/reference-field correction to 1D or 2D detector data.",
    ("sample", "dark", "flat"), ("corrected", "valid_mask"),
    object_schema({"epsilon": number(0.0, minimum=0.0), "normalize_flat": boolean(True)}),
    tags=("dark", "flat-field", "detector", "image"), assumptions=("sample, dark, and flat were acquired with compatible gain/exposure settings.",), caveats=("Bad/saturated pixels and temporal drift require separate masks or calibration frames.",),
))
def dark_flat_correct(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    sample = np.asarray(payload["sample"], dtype=float)
    dark = np.asarray(payload["dark"], dtype=float)
    flat = np.asarray(payload["flat"], dtype=float)
    if not (sample.shape == dark.shape == flat.shape):
        raise SignalLabError("sample, dark, and flat must have identical shapes")
    denominator = flat - dark
    if bool(params.get("normalize_flat", True)):
        finite_positive = denominator[np.isfinite(denominator) & (denominator > 0)]
        if finite_positive.size == 0:
            raise SignalLabError("flat-dark contains no positive finite values")
        denominator = denominator / np.median(finite_positive)
    valid = np.isfinite(sample) & np.isfinite(dark) & np.isfinite(denominator) & (np.abs(denominator) > float(params.get("epsilon", 0.0)))
    corrected = np.full(sample.shape, np.nan)
    np.divide(sample - dark, denominator, out=corrected, where=valid)
    warnings = [] if np.all(valid) else [f"masked {int((~valid).sum())} invalid or near-zero flat-field pixels"]
    return result({"corrected": corrected, "valid_mask": valid}, warnings=warnings)


@algorithm(_spec(
    "optics.transmittance_to_absorbance", "spectroscopy", "Convert fractional transmittance T to decadic absorbance A=-log10(T).",
    ("transmittance",), ("absorbance", "valid_mask"),
    tags=("absorbance", "transmittance", "ftir", "uv-vis"), assumptions=("Transmittance is a fraction, not percent.",), caveats=("T<=0 is invalid; stray light biases high absorbance.",),
))
def transmittance_to_absorbance(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    transmittance = np.asarray(payload["transmittance"], dtype=float)
    valid = np.isfinite(transmittance) & (transmittance > 0)
    absorbance = np.full(transmittance.shape, np.nan)
    absorbance[valid] = -np.log10(transmittance[valid])
    return result({"absorbance": absorbance, "valid_mask": valid}, warnings=[] if np.all(valid) else ["nonpositive transmittance values were masked"])


@algorithm(_spec(
    "optics.absorbance_to_absorption_coefficient", "spectroscopy", "Convert decadic absorbance to absorption coefficient alpha=ln(10) A / thickness.",
    ("absorbance",), ("absorption_coefficient",),
    object_schema({"thickness": number(exclusive_minimum=0.0)}, required=("thickness",)),
    tags=("absorption", "beer-lambert", "uv-vis"), assumptions=("Thickness units define inverse units of alpha; scattering and reflection are negligible or corrected.",),
))
def absorbance_to_alpha(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    absorbance = np.asarray(payload["absorbance"], dtype=float)
    return result({"absorption_coefficient": np.log(10.0) * absorbance / float(params["thickness"])})


@algorithm(_spec(
    "optics.beer_lambert_concentration", "spectroscopy", "Infer concentration from A=epsilon*c*path_length.",
    ("absorbance",), ("concentration",),
    object_schema({"molar_absorptivity": number(exclusive_minimum=0.0), "path_length": number(exclusive_minimum=0.0)}, required=("molar_absorptivity", "path_length")),
    tags=("beer-lambert", "concentration", "absorbance"), assumptions=("The sample obeys Beer-Lambert linearity at the selected wavelength.",), caveats=("Association, scattering, saturation, and matrix effects can invalidate linearity.",),
))
def beer_lambert_concentration(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    absorbance = np.asarray(payload["absorbance"], dtype=float)
    denominator = float(params["molar_absorptivity"]) * float(params["path_length"])
    return result({"concentration": absorbance / denominator})


@algorithm(_spec(
    "optics.energy_wavelength_convert", "units", "Convert between vacuum wavelength, photon energy, wavenumber, and frequency.",
    ("value",), ("wavelength_m", "energy_ev", "frequency_hz", "wavenumber_cm1"),
    object_schema({"input_kind": choice("wavelength_nm", ("wavelength_nm", "energy_ev", "frequency_hz", "wavenumber_cm1"))}),
    tags=("units", "photon", "wavelength", "energy"), assumptions=("Vacuum wavelength and frequency are intended.",),
))
def photon_units(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    value = np.asarray(payload["value"], dtype=float)
    kind = params.get("input_kind", "wavelength_nm")
    c = 299_792_458.0
    h_ev_s = 4.135667696e-15
    if kind == "energy_ev":
        frequency = value / h_ev_s
    elif kind == "frequency_hz":
        frequency = value
    elif kind == "wavenumber_cm1":
        frequency = value * 100.0 * c
    else:
        frequency = c / (value * 1e-9)
    wavelength = c / frequency
    return result({"wavelength_m": wavelength, "energy_ev": h_ev_s * frequency, "frequency_hz": frequency, "wavenumber_cm1": 1.0 / (100.0 * wavelength)})


@algorithm(_spec(
    "optics.raman_shift", "spectroscopy", "Compute Raman shift from excitation and scattered wavelengths.",
    ("scattered_wavelength_nm",), ("raman_shift_cm1",),
    object_schema({"excitation_wavelength_nm": number(exclusive_minimum=0.0)}, required=("excitation_wavelength_nm",)),
    tags=("raman", "wavenumber", "spectroscopy"), assumptions=("Wavelengths are vacuum nanometers.",),
))
def raman_shift(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    scattered = np.asarray(payload["scattered_wavelength_nm"], dtype=float)
    excitation = float(params["excitation_wavelength_nm"])
    return result({"raman_shift_cm1": 1e7 * (1.0 / excitation - 1.0 / scattered)})


@algorithm(_spec(
    "optics.rta_balance", "spectroscopy", "Compute absorptance A=1-R-T from fractional reflectance and transmittance.",
    ("reflectance", "transmittance"), ("absorptance", "closure_error_mask"),
    object_schema({"tolerance": number(0.02, minimum=0.0)}), tags=("reflectance", "transmittance", "absorptance", "energy-balance"), assumptions=("R and T are hemispherically compatible fractions with matched geometry.",), caveats=("Negative A or R+T>1 can indicate calibration, scattering, or geometry mismatch.",),
))
def rta_balance(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    reflectance = np.asarray(payload["reflectance"], dtype=float)
    transmittance = np.asarray(payload["transmittance"], dtype=float)
    if reflectance.shape != transmittance.shape:
        raise SignalLabError("reflectance and transmittance must have identical shapes")
    absorptance = 1.0 - reflectance - transmittance
    tolerance = float(params.get("tolerance", 0.02))
    mask = (absorptance < -tolerance) | (reflectance < -tolerance) | (transmittance < -tolerance)
    return result({"absorptance": absorptance, "closure_error_mask": mask}, warnings=[] if not np.any(mask) else [f"energy-balance check failed at {int(mask.sum())} samples"])


@algorithm(_spec(
    "optics.tauc_transform", "bandgap", "Construct Tauc coordinates (alpha*E)^power versus photon energy.",
    ("energy_ev", "absorption_coefficient"), ("energy_ev", "tauc_y", "valid_mask"),
    object_schema({"transition": choice("direct_allowed", ("direct_allowed", "indirect_allowed", "direct_forbidden", "indirect_forbidden"))}),
    tags=("tauc", "bandgap", "absorption"), assumptions=("A Tauc relation and a physically appropriate transition type apply in the selected region.",), caveats=("The linear region must be selected and justified; disorder/excitons can invalidate simple extrapolation.",),
))
def tauc_transform(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    energy = as_1d(payload["energy_ev"], "energy_ev")
    alpha = as_1d(payload["absorption_coefficient"], "absorption_coefficient")
    if energy.size != alpha.size:
        raise SignalLabError("energy_ev and absorption_coefficient must have equal length")
    powers = {"direct_allowed": 2.0, "indirect_allowed": 0.5, "direct_forbidden": 2.0 / 3.0, "indirect_forbidden": 1.0 / 3.0}
    power = powers[params.get("transition", "direct_allowed")]
    valid = np.isfinite(energy) & np.isfinite(alpha) & (energy > 0) & (alpha >= 0)
    transformed = np.full(energy.shape, np.nan)
    transformed[valid] = (alpha[valid] * energy[valid]) ** power
    return result({"energy_ev": energy, "tauc_y": transformed, "valid_mask": valid}, metadata={"power": power})


@algorithm(_spec(
    "optics.tauc_linear_gap", "bandgap", "Fit a selected linear Tauc interval and extrapolate its energy-axis intercept.",
    ("energy_ev", "tauc_y"), ("bandgap_ev", "slope", "intercept", "fit", "r_squared"),
    object_schema({"emin": number(), "emax": number()}, required=("emin", "emax")),
    tags=("tauc", "bandgap", "linear-fit"), assumptions=("emin..emax is the justified linear absorption-edge region.",),
))
def tauc_linear_gap(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    energy, y = paired_1d(payload, "energy_ev", "tauc_y", finite=False)
    mask = np.isfinite(energy) & np.isfinite(y) & (energy >= float(params["emin"])) & (energy <= float(params["emax"]))
    if mask.sum() < 3:
        raise SignalLabError("selected Tauc interval needs at least three finite points")
    slope, intercept = np.polyfit(energy[mask], y[mask], 1)
    if slope == 0:
        raise SignalLabError("Tauc fit slope is zero")
    fit = slope * energy[mask] + intercept
    total = y[mask] - np.mean(y[mask])
    r2 = 1.0 - float(np.sum((y[mask] - fit) ** 2) / np.sum(total**2)) if np.sum(total**2) else np.nan
    return result({"bandgap_ev": float(-intercept / slope), "slope": float(slope), "intercept": float(intercept), "fit": fit, "r_squared": r2}, metadata={"kept_mask": mask})


@algorithm(_spec(
    "optics.kk_hilbert_pair", "dispersion", "Approximate a Kramers-Kronig conjugate by a discrete Hilbert transform.",
    ("frequency", "component"), ("frequency", "conjugate"),
    object_schema({"direction": choice("imag_to_real", ("imag_to_real", "real_to_imag")), "subtract_endpoint_line": boolean(True)}),
    tags=("kramers-kronig", "hilbert", "causality"), assumptions=("frequency is uniform and the response is causal with adequate spectral coverage.",), caveats=("Finite bandwidth and extrapolation dominate edge errors; use constrained variational KK analysis for publication-grade optical constants.",), references=(KK_REF,),
))
def kk_hilbert_pair(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    frequency, component = paired_1d(payload, "frequency", "component")
    require_uniform_spacing(frequency, "frequency")
    values = component.copy()
    if bool(params.get("subtract_endpoint_line", True)):
        values = values - np.interp(frequency, [frequency[0], frequency[-1]], [component[0], component[-1]])
    hilbert = np.imag(signal.hilbert(values))
    conjugate = -hilbert if params.get("direction", "imag_to_real") == "imag_to_real" else hilbert
    return result({"frequency": frequency, "conjugate": conjugate}, warnings=["finite-band Hilbert transform: exclude and inspect edge regions"])


@algorithm(_spec(
    "optics.stokes_from_analyzers", "polarization", "Recover Stokes parameters from linear analyzer intensities and optional circular channels.",
    ("i0", "i45", "i90", "i135"), ("s0", "s1", "s2", "s3"),
    object_schema({"circular_convention": choice("right_minus_left", ("right_minus_left", "left_minus_right"))}),
    tags=("stokes", "polarization", "polarimetry"), assumptions=("Analyzer channels share radiometric calibration; circular channels use payload keys ircp and ilcp.",), caveats=("Instrument Mueller-matrix calibration is required for accurate polarimetry.",), references=(NIST_POL_REF,),
))
def stokes_from_analyzers(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    channels = [np.asarray(payload[key], dtype=float) for key in ("i0", "i45", "i90", "i135")]
    if len({item.shape for item in channels}) != 1:
        raise SignalLabError("linear analyzer intensities must have identical shapes")
    i0, i45, i90, i135 = channels
    s0, s1, s2 = i0 + i90, i0 - i90, i45 - i135
    warnings: list[str] = []
    if "ircp" in payload and "ilcp" in payload:
        ircp, ilcp = np.asarray(payload["ircp"], dtype=float), np.asarray(payload["ilcp"], dtype=float)
        if ircp.shape != s0.shape or ilcp.shape != s0.shape:
            raise SignalLabError("ircp and ilcp must match the linear analyzer shapes")
        s3 = ircp - ilcp if params.get("circular_convention", "right_minus_left") == "right_minus_left" else ilcp - ircp
    else:
        s3 = np.full(s0.shape, np.nan)
        warnings.append("circular analyzer channels absent; s3 is undefined")
    return result({"s0": s0, "s1": s1, "s2": s2, "s3": s3}, warnings=warnings)


@algorithm(_spec(
    "optics.polarization_metrics", "polarization", "Compute degree of polarization, linear polarization angle, and ellipticity from Stokes parameters.",
    ("s0", "s1", "s2", "s3"), ("degree_polarization", "degree_linear", "azimuth", "ellipticity_angle", "valid_mask"),
    object_schema({"degrees": boolean(True)}), tags=("stokes", "dop", "dolp", "azimuth", "ellipticity"), references=(NIST_POL_REF,),
))
def polarization_metrics(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    arrays = [np.asarray(payload[key], dtype=float) for key in ("s0", "s1", "s2", "s3")]
    if len({item.shape for item in arrays}) != 1:
        raise SignalLabError("all Stokes arrays must have identical shapes")
    s0, s1, s2, s3 = arrays
    valid = np.isfinite(s0) & (s0 > 0)
    dop = np.full(s0.shape, np.nan)
    dolp = np.full(s0.shape, np.nan)
    dop[valid] = np.sqrt(s1[valid] ** 2 + s2[valid] ** 2 + s3[valid] ** 2) / s0[valid]
    dolp[valid] = np.sqrt(s1[valid] ** 2 + s2[valid] ** 2) / s0[valid]
    azimuth = 0.5 * np.arctan2(s2, s1)
    ellipticity = 0.5 * np.arctan2(s3, np.sqrt(s1**2 + s2**2))
    if bool(params.get("degrees", True)):
        azimuth, ellipticity = np.degrees(azimuth), np.degrees(ellipticity)
    return result({"degree_polarization": dop, "degree_linear": dolp, "azimuth": azimuth, "ellipticity_angle": ellipticity, "valid_mask": valid})


@algorithm(_spec(
    "optics.malus_fit", "polarization", "Fit analyzer intensity to offset + amplitude*cos^2(angle-angle0).",
    ("angle", "intensity"), ("fit", "offset", "amplitude", "axis_angle", "visibility", "covariance"),
    object_schema({"angle_unit": choice("degree", ("degree", "radian"))}),
    tags=("malus", "polarization", "analyzer"), assumptions=("A dominant linearly polarized component follows Malus law.",), references=(NIST_POL_REF,),
))
def malus_fit(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    angle, intensity = paired_1d(payload, "angle", "intensity")
    radians = np.radians(angle) if params.get("angle_unit", "degree") == "degree" else angle
    def model(theta: np.ndarray, offset: float, amplitude: float, theta0: float) -> np.ndarray:
        return offset + amplitude * np.cos(theta - theta0) ** 2
    initial = [float(np.min(intensity)), float(np.ptp(intensity)), float(radians[np.argmax(intensity)])]
    fitted, covariance = optimize.curve_fit(model, radians, intensity, p0=initial, maxfev=20000)
    prediction = model(radians, *fitted)
    maximum, minimum = fitted[0] + fitted[1], fitted[0]
    visibility = float((maximum - minimum) / (maximum + minimum)) if maximum + minimum else np.nan
    axis = float(np.degrees(fitted[2]) % 180.0) if params.get("angle_unit", "degree") == "degree" else float(fitted[2] % np.pi)
    return result({"fit": prediction, "offset": float(fitted[0]), "amplitude": float(fitted[1]), "axis_angle": axis, "visibility": visibility, "covariance": covariance})


@algorithm(_spec(
    "optics.fringe_visibility", "interferometry", "Compute Michelson fringe visibility (Imax-Imin)/(Imax+Imin).",
    ("intensity",), ("visibility", "minimum", "maximum"),
    object_schema({"low_percentile": number(1.0, minimum=0.0, maximum=50.0), "high_percentile": number(99.0, minimum=50.0, maximum=100.0)}),
    tags=("interference", "visibility", "contrast"), caveats=("Percentile estimates suppress isolated noise but must be reported.",),
))
def fringe_visibility(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    intensity = as_1d(payload["intensity"], "intensity")
    minimum, maximum = np.percentile(intensity, [float(params.get("low_percentile", 1.0)), float(params.get("high_percentile", 99.0))])
    if maximum + minimum == 0:
        raise SignalLabError("Imax + Imin is zero")
    return result({"visibility": float((maximum - minimum) / (maximum + minimum)), "minimum": float(minimum), "maximum": float(maximum)})


@algorithm(_spec(
    "optics.fluorescence_phasor", "lifetime", "Compute first-harmonic fluorescence lifetime phasor from a decay histogram.",
    ("time", "counts"), ("g", "s", "phase_lifetime", "modulation_lifetime", "modulation"),
    object_schema({"angular_frequency": number(exclusive_minimum=0.0)}, required=("angular_frequency",)),
    tags=("flim", "phasor", "lifetime"), assumptions=("Background and instrument-response effects are corrected or negligible.",), caveats=("A single-exponential lifetime interpretation is invalid for mixtures even though the phasor remains useful.",), references=(PHASOR_REF,),
))
def fluorescence_phasor(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    time, counts = paired_1d(payload, "time", "counts")
    omega = float(params["angular_frequency"])
    total = float(np.trapezoid(counts, time))
    if total <= 0:
        raise SignalLabError("integrated fluorescence counts must be positive")
    g = float(np.trapezoid(counts * np.cos(omega * time), time) / total)
    s = float(np.trapezoid(counts * np.sin(omega * time), time) / total)
    modulation = float(np.hypot(g, s))
    phase_lifetime = float(s / (omega * g)) if g != 0 else np.inf
    modulation_lifetime = float(np.sqrt(max(0.0, modulation ** -2 - 1.0)) / omega) if modulation > 0 else np.inf
    return result({"g": g, "s": s, "phase_lifetime": phase_lifetime, "modulation_lifetime": modulation_lifetime, "modulation": modulation})


@algorithm(_spec(
    "optics.richardson_lucy", "imaging", "Positivity-preserving Richardson-Lucy deconvolution with a known PSF.",
    ("image", "psf"), ("deconvolved",),
    object_schema({"iterations": integer(30, minimum=1, maximum=1000), "clip": boolean(True), "epsilon": number(1e-12, exclusive_minimum=0.0)}),
    tags=("deconvolution", "psf", "image", "poisson"), assumptions=("The PSF is known, shift invariant, and the data are approximately Poisson limited.",), caveats=("Iterations amplify noise; select stopping/regularization independently of desired visual sharpness.",), references=(RL_REF,),
))
def richardson_lucy(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    image = as_2d(payload["image"], "image")
    psf = as_2d(payload["psf"], "psf")
    if np.any(image < 0) or np.any(psf < 0):
        raise SignalLabError("Richardson-Lucy requires nonnegative image and PSF")
    psf_sum = float(np.sum(psf))
    if psf_sum <= 0:
        raise SignalLabError("PSF sum must be positive")
    kernel = psf / psf_sum
    mirror = kernel[::-1, ::-1]
    estimate = np.full(image.shape, max(float(np.mean(image)), float(params.get("epsilon", 1e-12))))
    epsilon = float(params.get("epsilon", 1e-12))
    for _ in range(int(params.get("iterations", 30))):
        blurred = signal.fftconvolve(estimate, kernel, mode="same")
        ratio = image / np.maximum(blurred, epsilon)
        estimate *= signal.fftconvolve(ratio, mirror, mode="same")
        if bool(params.get("clip", True)):
            estimate = np.clip(estimate, 0.0, None)
    return result({"deconvolved": estimate})


@algorithm(_spec(
    "optics.wiener_deconvolution", "imaging", "Frequency-domain Wiener deconvolution with scalar noise-to-signal regularization.",
    ("image", "psf"), ("deconvolved",),
    object_schema({"regularization": number(1e-3, exclusive_minimum=0.0)}),
    tags=("deconvolution", "wiener", "psf", "image"), assumptions=("PSF is shift invariant and regularization approximates the noise-to-signal spectrum ratio.",), caveats=("A scalar regularizer is a simplification; inspect ringing and residuals.",),
))
def wiener_deconvolution(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    image = as_2d(payload["image"], "image")
    psf = as_2d(payload["psf"], "psf")
    padded = np.zeros_like(image)
    if psf.shape[0] > image.shape[0] or psf.shape[1] > image.shape[1]:
        raise SignalLabError("PSF must not exceed image dimensions")
    padded[: psf.shape[0], : psf.shape[1]] = psf / np.sum(psf)
    padded = np.fft.ifftshift(padded)
    transfer = np.fft.fft2(padded)
    regularization = float(params.get("regularization", 1e-3))
    restored = np.fft.ifft2(np.fft.fft2(image) * np.conj(transfer) / (np.abs(transfer) ** 2 + regularization)).real
    return result({"deconvolved": restored})


@algorithm(_spec(
    "optics.spot_moments", "imaging", "Intensity-weighted centroid, covariance, RMS widths, and orientation of a 2D spot.",
    ("image",), ("centroid_x", "centroid_y", "sigma_major", "sigma_minor", "angle", "covariance"),
    object_schema({"pixel_size_x": number(1.0, exclusive_minimum=0.0), "pixel_size_y": number(1.0, exclusive_minimum=0.0), "background": number(0.0)}),
    tags=("beam", "centroid", "spot", "moments"), assumptions=("After background subtraction, image intensity is proportional to signal and nonnegative.",), caveats=("Moment widths are sensitive to background, clipping, and hot pixels.",),
))
def spot_moments(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    image = as_2d(payload["image"], "image") - float(params.get("background", 0.0))
    weights = np.clip(image, 0.0, None)
    total = float(np.sum(weights))
    if total <= 0:
        raise SignalLabError("background-subtracted image has no positive intensity")
    yy, xx = np.indices(image.shape)
    xx = xx * float(params.get("pixel_size_x", 1.0))
    yy = yy * float(params.get("pixel_size_y", 1.0))
    cx, cy = float(np.sum(weights * xx) / total), float(np.sum(weights * yy) / total)
    dx, dy = xx - cx, yy - cy
    covariance = np.array([[np.sum(weights * dx * dx), np.sum(weights * dx * dy)], [np.sum(weights * dx * dy), np.sum(weights * dy * dy)]], dtype=float) / total
    eigenvalues, eigenvectors = np.linalg.eigh(covariance)
    order = np.argsort(eigenvalues)[::-1]
    eigenvalues, eigenvectors = eigenvalues[order], eigenvectors[:, order]
    angle = float(np.arctan2(eigenvectors[1, 0], eigenvectors[0, 0]))
    return result({"centroid_x": cx, "centroid_y": cy, "sigma_major": float(np.sqrt(max(0.0, eigenvalues[0]))), "sigma_minor": float(np.sqrt(max(0.0, eigenvalues[1]))), "angle": angle, "covariance": covariance})


@algorithm(_spec(
    "optics.radial_profile", "imaging", "Azimuthally average a 2D image around a specified or intensity-weighted center.",
    ("image",), ("radius", "mean", "std", "count"),
    object_schema({"center_x": number(), "center_y": number(), "bin_width": number(1.0, exclusive_minimum=0.0)}),
    tags=("radial", "azimuthal-average", "image", "scattering"), caveats=("Azimuthal averaging hides anisotropy; inspect the 2D pattern first.",),
))
def radial_profile(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    image = as_2d(payload["image"], "image")
    yy, xx = np.indices(image.shape)
    finite = np.isfinite(image)
    if "center_x" in params and "center_y" in params:
        cx, cy = float(params["center_x"]), float(params["center_y"])
    else:
        weights = np.clip(np.where(finite, image, 0.0), 0.0, None)
        if np.sum(weights) == 0:
            cx, cy = (image.shape[1] - 1) / 2.0, (image.shape[0] - 1) / 2.0
        else:
            cx, cy = float(np.sum(weights * xx) / np.sum(weights)), float(np.sum(weights * yy) / np.sum(weights))
    width = float(params.get("bin_width", 1.0))
    bins = np.floor(np.hypot(xx - cx, yy - cy) / width).astype(int)
    maximum = int(np.max(bins))
    count = np.bincount(bins[finite], minlength=maximum + 1)
    sums = np.bincount(bins[finite], weights=image[finite], minlength=maximum + 1)
    mean = np.divide(sums, count, out=np.full(maximum + 1, np.nan), where=count > 0)
    variance = np.bincount(bins[finite], weights=(image[finite] - mean[bins[finite]]) ** 2, minlength=maximum + 1)
    std = np.sqrt(np.divide(variance, count, out=np.full(maximum + 1, np.nan), where=count > 0))
    return result({"radius": (np.arange(maximum + 1) + 0.5) * width, "mean": mean, "std": std, "count": count}, metadata={"center_x": cx, "center_y": cy})


@algorithm(_spec(
    "optics.edge_mtf", "imaging", "Estimate line-spread function and normalized MTF from a uniformly sampled edge-spread function.",
    ("position", "edge_spread"), ("frequency", "mtf", "line_spread"),
    object_schema({"window": choice("hann", ("hann", "hamming", "blackman", "none"))}),
    tags=("mtf", "edge", "resolution", "imaging"), assumptions=("The edge-spread function has already been projected perpendicular to a sufficiently sharp edge.",), caveats=("Sampling, edge angle, differentiation noise, and edge quality affect the MTF.",),
))
def edge_mtf(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    position, esf = paired_1d(payload, "position", "edge_spread")
    step = require_uniform_spacing(position, "position")
    line_spread = np.gradient(esf, position, edge_order=2)
    line_spread -= np.mean([line_spread[0], line_spread[-1]])
    window_name = params.get("window", "hann")
    window = np.ones(line_spread.size) if window_name == "none" else signal.get_window(window_name, line_spread.size)
    transfer = np.abs(np.fft.rfft(line_spread * window))
    if transfer[0] == 0:
        raise SignalLabError("zero-frequency MTF normalization is zero")
    return result({"frequency": np.fft.rfftfreq(line_spread.size, d=step), "mtf": transfer / transfer[0], "line_spread": line_spread})


@algorithm(_spec(
    "optics.pump_probe_fractional_change", "ultrafast", "Compute DeltaT/T or DeltaR/R from pumped and unpumped traces.",
    ("pumped", "unpumped"), ("fractional_change", "valid_mask"),
    object_schema({"epsilon": number(0.0, minimum=0.0)}), tags=("pump-probe", "delta-t-over-t", "delta-r-over-r"), caveats=("Correct timing drift, pump scatter, chirp, and long-lived offsets before interpretation.",),
))
def pump_probe_fractional_change(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    pumped = np.asarray(payload["pumped"], dtype=float)
    unpumped = np.asarray(payload["unpumped"], dtype=float)
    if pumped.shape != unpumped.shape:
        raise SignalLabError("pumped and unpumped must have identical shapes")
    valid = np.isfinite(pumped) & np.isfinite(unpumped) & (np.abs(unpumped) > float(params.get("epsilon", 0.0)))
    change = np.full(pumped.shape, np.nan)
    np.divide(pumped - unpumped, unpumped, out=change, where=valid)
    return result({"fractional_change": change, "valid_mask": valid})
