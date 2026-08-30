"""Atomic frequency-domain, time-frequency, noise, and lock-in methods."""

from __future__ import annotations

from typing import Any, Mapping

import numpy as np
from scipy import signal

from .model import AlgorithmResult, AlgorithmSpec, result
from .registry import algorithm
from .schemas import boolean, choice, integer, number, object_schema
from .validation import SignalLabError, as_1d, paired_1d, require_uniform_spacing

SCIPY_REF = "SciPy signal processing API, https://docs.scipy.org/doc/scipy/reference/signal.html"
NIST_ALLAN_REF = "NIST SP 1065, Handbook of Frequency Stability Analysis, https://tf.nist.gov/general/pdf/2220.pdf"
LOCKIN_REF = "Zurich Instruments MFIA User Manual, Principles of Lock-in Detection, https://docs.zhinst.com/pdf/ziMFIA_UserManual.pdf"


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
    references: tuple[str, ...] = (SCIPY_REF,),
) -> AlgorithmSpec:
    return AlgorithmSpec(
        name=name, domain="general", category=category, summary=summary,
        required_inputs=inputs, outputs=outputs,
        parameter_schema=schema or object_schema(), tags=tags,
        assumptions=assumptions, caveats=caveats, references=references,
    )


def _uniform_time(payload: Mapping[str, Any]) -> tuple[np.ndarray, np.ndarray, float]:
    time, y = paired_1d(payload, "time", "y")
    dt = require_uniform_spacing(time, "time")
    return time, y, 1.0 / dt


@algorithm(_spec(
    "spectrum.fft", "spectrum", "One-sided FFT amplitude and phase for uniformly sampled real data.",
    ("time", "y"), ("frequency", "amplitude", "phase", "complex_spectrum"),
    object_schema({"window": choice("hann", ("none", "hann", "hamming", "blackman")), "detrend": choice("constant", ("none", "constant", "linear"))}),
    tags=("fft", "frequency", "phase"), assumptions=("time is uniformly sampled.",),
    caveats=("Finite records leak power; report the window and frequency resolution.",),
))
def fft_spectrum(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    time, y, fs = _uniform_time(payload)
    detrend = params.get("detrend", "constant")
    values = signal.detrend(y, type=detrend) if detrend != "none" else y.copy()
    window_name = params.get("window", "hann")
    window = np.ones(values.size) if window_name == "none" else signal.get_window(window_name, values.size)
    transformed = np.fft.rfft(values * window)
    coherent_gain = np.sum(window)
    amplitude = 2.0 * np.abs(transformed) / coherent_gain
    if amplitude.size:
        amplitude[0] *= 0.5
        if values.size % 2 == 0:
            amplitude[-1] *= 0.5
    return result({"frequency": np.fft.rfftfreq(values.size, d=1.0 / fs), "amplitude": amplitude, "phase": np.angle(transformed), "complex_spectrum": transformed}, metadata={"sample_rate": fs, "window": window_name, "frequency_resolution": fs / values.size})


@algorithm(_spec(
    "spectrum.periodogram", "spectrum", "Classical periodogram power spectral density estimate.",
    ("time", "y"), ("frequency", "psd"),
    object_schema({"window": choice("boxcar", ("boxcar", "hann", "hamming", "blackman")), "detrend": choice("constant", ("none", "constant", "linear"))}),
    tags=("periodogram", "psd", "noise"), assumptions=("time is uniformly sampled.",), caveats=("The raw periodogram has high variance; Welch averaging is usually more stable.",),
))
def periodogram(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    _, y, fs = _uniform_time(payload)
    detrend: str | bool = False if params.get("detrend", "constant") == "none" else params.get("detrend", "constant")
    frequency, psd = signal.periodogram(y, fs=fs, window=params.get("window", "boxcar"), detrend=detrend, scaling="density")
    return result({"frequency": frequency, "psd": psd}, metadata={"sample_rate": fs, "units": "y^2/Hz"})


@algorithm(_spec(
    "spectrum.welch_psd", "spectrum", "Welch averaged power spectral density estimate.",
    ("time", "y"), ("frequency", "psd"),
    object_schema({"segment_length": integer(256, minimum=4), "overlap_fraction": number(0.5, minimum=0.0, maximum=0.95), "window": choice("hann", ("hann", "hamming", "blackman", "boxcar")), "detrend": choice("constant", ("none", "constant", "linear"))}),
    tags=("welch", "psd", "noise"), assumptions=("time is uniformly sampled and the process is approximately stationary within segments.",), caveats=("Segment length trades frequency resolution against estimator variance.",),
))
def welch_psd(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    _, y, fs = _uniform_time(payload)
    segment_length = min(int(params.get("segment_length", 256)), y.size)
    overlap = int(segment_length * float(params.get("overlap_fraction", 0.5)))
    detrend: str | bool = False if params.get("detrend", "constant") == "none" else params.get("detrend", "constant")
    frequency, psd = signal.welch(y, fs=fs, window=params.get("window", "hann"), nperseg=segment_length, noverlap=overlap, detrend=detrend, scaling="density")
    return result({"frequency": frequency, "psd": psd}, metadata={"sample_rate": fs, "segment_length": segment_length, "frequency_resolution": fs / segment_length, "units": "y^2/Hz"})


@algorithm(_spec(
    "spectrum.lomb_scargle", "spectrum", "Lomb-Scargle periodogram for unevenly sampled data.",
    ("time", "y"), ("frequency", "power"),
    object_schema({"min_frequency": number(exclusive_minimum=0.0), "max_frequency": number(exclusive_minimum=0.0), "points": integer(2000, minimum=16), "normalize": boolean(True)}),
    tags=("lomb-scargle", "irregular", "periodogram"), caveats=("The searched frequency grid and spectral window must be reported.",),
))
def lomb_scargle(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    time, y = paired_1d(payload, "time", "y")
    order = np.argsort(time)
    time, y = time[order], y[order]
    span = float(time[-1] - time[0])
    if span <= 0:
        raise SignalLabError("time must span a nonzero interval")
    median_dt = float(np.median(np.diff(np.unique(time))))
    min_frequency = float(params.get("min_frequency", 1.0 / span))
    max_frequency = float(params.get("max_frequency", 0.5 / median_dt))
    if max_frequency <= min_frequency:
        raise SignalLabError("max_frequency must exceed min_frequency")
    frequency = np.linspace(min_frequency, max_frequency, int(params.get("points", 2000)))
    power = signal.lombscargle(time - time.min(), y - np.mean(y), 2.0 * np.pi * frequency, precenter=False, normalize=bool(params.get("normalize", True)))
    return result({"frequency": frequency, "power": power})


@algorithm(_spec(
    "spectrum.cross_psd", "spectrum", "Welch cross power spectral density of two synchronous traces.",
    ("time", "x", "y"), ("frequency", "cross_psd"),
    object_schema({"segment_length": integer(256, minimum=4), "overlap_fraction": number(0.5, minimum=0.0, maximum=0.95)}),
    tags=("cross-spectrum", "csd", "phase"), assumptions=("x and y are synchronous and uniformly sampled.",),
))
def cross_psd(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    time = as_1d(payload["time"], "time")
    x = as_1d(payload["x"], "x")
    y = as_1d(payload["y"], "y")
    if not (time.size == x.size == y.size):
        raise SignalLabError("time, x, and y must have equal length")
    fs = 1.0 / require_uniform_spacing(time, "time")
    nperseg = min(int(params.get("segment_length", 256)), time.size)
    noverlap = int(nperseg * float(params.get("overlap_fraction", 0.5)))
    frequency, spectrum = signal.csd(x, y, fs=fs, nperseg=nperseg, noverlap=noverlap, scaling="density")
    return result({"frequency": frequency, "cross_psd": spectrum}, metadata={"sample_rate": fs})


@algorithm(_spec(
    "spectrum.coherence", "spectrum", "Magnitude-squared coherence between two synchronous traces.",
    ("time", "x", "y"), ("frequency", "coherence"),
    object_schema({"segment_length": integer(256, minimum=4), "overlap_fraction": number(0.5, minimum=0.0, maximum=0.95)}),
    tags=("coherence", "coupling", "transfer"), assumptions=("x and y are synchronous, uniformly sampled, and approximately stationary within segments.",), caveats=("High coherence indicates linear correlation, not causality.",),
))
def coherence(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    time = as_1d(payload["time"], "time")
    x = as_1d(payload["x"], "x")
    y = as_1d(payload["y"], "y")
    if not (time.size == x.size == y.size):
        raise SignalLabError("time, x, and y must have equal length")
    fs = 1.0 / require_uniform_spacing(time, "time")
    nperseg = min(int(params.get("segment_length", 256)), time.size)
    noverlap = int(nperseg * float(params.get("overlap_fraction", 0.5)))
    frequency, values = signal.coherence(x, y, fs=fs, nperseg=nperseg, noverlap=noverlap)
    return result({"frequency": frequency, "coherence": values}, metadata={"sample_rate": fs})


@algorithm(_spec(
    "time_frequency.stft", "time_frequency", "Short-time Fourier transform and spectrogram magnitude.",
    ("time", "y"), ("frequency", "segment_time", "stft", "magnitude"),
    object_schema({"segment_length": integer(256, minimum=4), "overlap_fraction": number(0.75, minimum=0.0, maximum=0.95), "window": choice("hann", ("hann", "hamming", "blackman", "boxcar"))}),
    tags=("stft", "spectrogram", "nonstationary"), assumptions=("time is uniformly sampled.",), caveats=("Time and frequency resolution obey a window-length tradeoff.",),
))
def stft(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    time, y, fs = _uniform_time(payload)
    nperseg = min(int(params.get("segment_length", 256)), y.size)
    noverlap = int(nperseg * float(params.get("overlap_fraction", 0.75)))
    frequency, relative_time, transformed = signal.stft(y, fs=fs, window=params.get("window", "hann"), nperseg=nperseg, noverlap=noverlap)
    return result({"frequency": frequency, "segment_time": relative_time + time[0], "stft": transformed, "magnitude": np.abs(transformed)}, metadata={"sample_rate": fs})


@algorithm(_spec(
    "correlation.autocorrelation", "correlation", "Biased or unbiased normalized autocorrelation.",
    ("time", "y"), ("lag", "correlation"),
    object_schema({"normalization": choice("coefficient", ("coefficient", "biased", "unbiased")), "nonnegative_lags": boolean(True)}),
    tags=("autocorrelation", "memory", "time-series"), assumptions=("time is uniformly sampled.",),
))
def autocorrelation(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    time, y, fs = _uniform_time(payload)
    centered = y - np.mean(y)
    values = signal.correlate(centered, centered, mode="full", method="fft")
    lags = signal.correlation_lags(y.size, y.size, mode="full")
    mode = params.get("normalization", "coefficient")
    if mode == "unbiased":
        values = values / (y.size - np.abs(lags))
    elif mode == "biased":
        values = values / y.size
    else:
        zero = values[lags == 0][0]
        values = values / zero if zero else values * np.nan
    if bool(params.get("nonnegative_lags", True)):
        mask = lags >= 0
        lags, values = lags[mask], values[mask]
    return result({"lag": lags / fs, "correlation": values})


@algorithm(_spec(
    "correlation.cross_correlation", "correlation", "Normalized cross-correlation and lag of maximum correlation.",
    ("time", "x", "y"), ("lag", "correlation", "peak_lag", "peak_correlation"),
    tags=("cross-correlation", "delay", "synchronous"), assumptions=("x and y are synchronous and uniformly sampled.",),
))
def cross_correlation(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    time = as_1d(payload["time"], "time")
    x = as_1d(payload["x"], "x")
    y = as_1d(payload["y"], "y")
    if not (time.size == x.size == y.size):
        raise SignalLabError("time, x, and y must have equal length")
    fs = 1.0 / require_uniform_spacing(time, "time")
    a, b = x - np.mean(x), y - np.mean(y)
    values = signal.correlate(a, b, mode="full", method="fft")
    norm = np.linalg.norm(a) * np.linalg.norm(b)
    values = values / norm if norm else values * np.nan
    lags = signal.correlation_lags(x.size, y.size, mode="full") / fs
    index = int(np.nanargmax(np.abs(values)))
    return result({"lag": lags, "correlation": values, "peak_lag": float(lags[index]), "peak_correlation": float(values[index])})


@algorithm(_spec(
    "stability.allan_deviation", "stability", "Overlapping Allan deviation for uniformly sampled fractional-frequency data.",
    ("time", "fractional_frequency"), ("tau", "allan_deviation", "terms"),
    object_schema({"max_cluster_fraction": number(0.25, exclusive_minimum=0.0, maximum=0.5)}),
    tags=("allan", "stability", "drift", "noise"), assumptions=("fractional_frequency is uniformly sampled with no gaps.",), caveats=("Different Allan-family estimators diagnose different noise and drift processes.",), references=(NIST_ALLAN_REF,),
))
def allan_deviation(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    time = as_1d(payload["time"], "time")
    values = as_1d(payload["fractional_frequency"], "fractional_frequency")
    if time.size != values.size:
        raise SignalLabError("time and fractional_frequency must have equal length")
    dt = require_uniform_spacing(time, "time")
    max_m = max(1, int(values.size * float(params.get("max_cluster_fraction", 0.25))))
    clusters = np.unique(np.logspace(0, np.log10(max_m), num=max(2, min(40, max_m)), dtype=int))
    taus, deviations, terms = [], [], []
    cumulative = np.concatenate(([0.0], np.cumsum(values)))
    for m in clusters:
        if 2 * m >= values.size:
            continue
        averages = (cumulative[m:] - cumulative[:-m]) / m
        differences = averages[m:] - averages[:-m]
        if differences.size:
            taus.append(m * dt)
            deviations.append(np.sqrt(0.5 * np.mean(differences**2)))
            terms.append(differences.size)
    return result({"tau": np.asarray(taus), "allan_deviation": np.asarray(deviations), "terms": np.asarray(terms, dtype=int)})


@algorithm(_spec(
    "lockin.demodulate", "lockin", "Digital dual-phase lock-in demodulation by complex mixing and low-pass filtering.",
    ("time", "signal"), ("x", "y", "amplitude", "phase"),
    object_schema({"reference_frequency": number(exclusive_minimum=0.0), "reference_phase": number(0.0), "lowpass_cutoff": number(exclusive_minimum=0.0), "filter_order": integer(4, minimum=1, maximum=12), "amplitude_convention": choice("peak", ("peak", "rms"))}, required=("reference_frequency", "lowpass_cutoff")),
    tags=("lock-in", "demodulation", "phase-sensitive"), assumptions=("time is uniformly sampled and the reference is phase coherent.",), caveats=("The low-pass bandwidth sets response time and equivalent noise bandwidth.",), references=(LOCKIN_REF,),
))
def lockin_demodulate(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    time = as_1d(payload["time"], "time")
    values = as_1d(payload["signal"], "signal")
    if time.size != values.size:
        raise SignalLabError("time and signal must have equal length")
    fs = 1.0 / require_uniform_spacing(time, "time")
    frequency = float(params["reference_frequency"])
    cutoff = float(params["lowpass_cutoff"])
    if frequency >= fs / 2 or cutoff >= fs / 2:
        raise SignalLabError("reference_frequency and lowpass_cutoff must be below Nyquist")
    reference = np.exp(-1j * (2.0 * np.pi * frequency * time + float(params.get("reference_phase", 0.0))))
    mixed = values * reference
    sos = signal.butter(int(params.get("filter_order", 4)), cutoff, btype="lowpass", fs=fs, output="sos")
    baseband = signal.sosfiltfilt(sos, mixed.real) + 1j * signal.sosfiltfilt(sos, mixed.imag)
    factor = 2.0 if params.get("amplitude_convention", "peak") == "peak" else np.sqrt(2.0)
    x_component = factor * baseband.real
    y_component = factor * baseband.imag
    return result({"x": x_component, "y": y_component, "amplitude": np.hypot(x_component, y_component), "phase": np.arctan2(y_component, x_component)}, metadata={"sample_rate": fs, "reference_frequency": frequency, "lowpass_cutoff": cutoff})


@algorithm(_spec(
    "lockin.xy_to_polar", "lockin", "Convert lock-in X/Y quadratures to amplitude and unwrapped phase.",
    ("x", "y"), ("amplitude", "phase"),
    object_schema({"unwrap_phase": boolean(True), "degrees": boolean(False)}), tags=("lock-in", "quadrature", "phase"),
))
def lockin_xy_to_polar(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    x = as_1d(payload["x"], "x")
    y = as_1d(payload["y"], "y")
    if x.size != y.size:
        raise SignalLabError("x and y must have equal length")
    phase = np.arctan2(y, x)
    if bool(params.get("unwrap_phase", True)):
        phase = np.unwrap(phase)
    if bool(params.get("degrees", False)):
        phase = np.degrees(phase)
    return result({"amplitude": np.hypot(x, y), "phase": phase})


@algorithm(_spec(
    "noise.power_law_exponent", "noise", "Fit PSD=A*f^exponent over a selected positive-frequency band.",
    ("frequency", "psd"), ("amplitude", "exponent", "fit", "r_squared", "kept_mask"),
    object_schema({"min_frequency": number(minimum=0.0), "max_frequency": number(exclusive_minimum=0.0)}),
    tags=("one-over-f", "noise", "psd", "power-law"), caveats=("A straight log-log segment is descriptive and does not by itself identify a microscopic noise source.",),
))
def noise_power_law(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    frequency = as_1d(payload["frequency"], "frequency")
    psd = as_1d(payload["psd"], "psd")
    if frequency.size != psd.size:
        raise SignalLabError("frequency and psd must have equal length")
    lower = float(params.get("min_frequency", 0.0))
    upper = float(params.get("max_frequency", np.inf))
    mask = (frequency > max(0.0, lower)) & (frequency <= upper) & (psd > 0)
    if mask.sum() < 3:
        raise SignalLabError("selected band needs at least three positive PSD samples")
    exponent, intercept = np.polyfit(np.log(frequency[mask]), np.log(psd[mask]), 1)
    fitted = np.exp(intercept) * frequency[mask] ** exponent
    residual = np.log(psd[mask]) - np.log(fitted)
    total = np.log(psd[mask]) - np.mean(np.log(psd[mask]))
    r2 = 1.0 - float(np.sum(residual**2) / np.sum(total**2)) if np.sum(total**2) else np.nan
    return result({"amplitude": float(np.exp(intercept)), "exponent": float(exponent), "fit": fitted, "r_squared": r2, "kept_mask": mask})
