"""Atomic preprocessing, calibration, filtering, and uncertainty methods."""

from __future__ import annotations

from typing import Any, Mapping

import numpy as np
from scipy import interpolate, ndimage, signal, sparse
from scipy.sparse.linalg import spsolve

from .model import AlgorithmResult, AlgorithmSpec, result
from .registry import algorithm
from .schemas import boolean, choice, integer, number, object_schema
from .validation import (
    SignalLabError,
    as_1d,
    odd_window,
    paired_1d,
    require_strictly_increasing,
    require_uniform_spacing,
)

SG_REF = "Savitzky and Golay, Anal. Chem. 36, 1627 (1964), doi:10.1021/ac60214a047"
ASLS_REF = "Eilers and Boelens, Baseline Correction with Asymmetric Least Squares Smoothing (2005)"
SCIPY_REF = "SciPy signal processing API, https://docs.scipy.org/doc/scipy/reference/signal.html"


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
        name=name,
        domain="general",
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
    "preprocess.sort_axis", "data_hygiene", "Sort paired samples by the independent axis.",
    ("x", "y"), ("x", "y", "order"), tags=("sort", "axis", "paired"),
))
def sort_axis(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    x, y = paired_1d(payload, finite=False)
    order = np.argsort(x, kind="stable")
    return result({"x": x[order], "y": y[order], "order": order})


@algorithm(_spec(
    "preprocess.drop_nonfinite", "data_hygiene", "Remove paired rows containing NaN or infinity.",
    ("x", "y"), ("x", "y", "kept_mask", "removed_count"), tags=("nan", "cleaning"),
))
def drop_nonfinite(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    x, y = paired_1d(payload, finite=False)
    mask = np.isfinite(x) & np.isfinite(y)
    return result(
        {"x": x[mask], "y": y[mask], "kept_mask": mask, "removed_count": int((~mask).sum())}
    )


@algorithm(_spec(
    "preprocess.crop_range", "data_hygiene", "Select samples inside an inclusive axis interval.",
    ("x", "y"), ("x", "y", "kept_mask"),
    object_schema({"xmin": number(), "xmax": number()}), tags=("crop", "range"),
))
def crop_range(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    x, y = paired_1d(payload)
    xmin = float(params.get("xmin", np.min(x)))
    xmax = float(params.get("xmax", np.max(x)))
    if xmax < xmin:
        raise SignalLabError("xmax must be >= xmin")
    mask = (x >= xmin) & (x <= xmax)
    if not np.any(mask):
        raise SignalLabError("crop interval contains no samples")
    return result({"x": x[mask], "y": y[mask], "kept_mask": mask})


@algorithm(_spec(
    "preprocess.average_repeats", "aggregation", "Average observations sharing the same axis value.",
    ("x", "y"), ("x", "mean", "std", "sem", "count"),
    tags=("repeat", "mean", "sem"), assumptions=("Repeated x values are exactly equal.",),
))
def average_repeats(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    x, y = paired_1d(payload)
    unique, inverse = np.unique(x, return_inverse=True)
    count = np.bincount(inverse)
    mean = np.bincount(inverse, weights=y) / count
    variance_sum = np.bincount(inverse, weights=(y - mean[inverse]) ** 2)
    std = np.sqrt(np.divide(variance_sum, count - 1, out=np.zeros_like(mean), where=count > 1))
    sem = std / np.sqrt(count)
    return result({"x": unique, "mean": mean, "std": std, "sem": sem, "count": count})


@algorithm(_spec(
    "preprocess.bin_average", "aggregation", "Average paired data in fixed-width or fixed-count bins.",
    ("x", "y"), ("x", "mean", "std", "sem", "count"),
    object_schema({"bins": integer(50, minimum=1), "mode": choice("count", ("count", "width")), "width": number(exclusive_minimum=0)}),
    tags=("binning", "average", "sem"),
))
def bin_average(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    x, y = paired_1d(payload)
    order = np.argsort(x)
    x, y = x[order], y[order]
    mode = params.get("mode", "count")
    if mode == "width":
        width = float(params.get("width", (x.max() - x.min()) / 50.0))
        if width <= 0:
            raise SignalLabError("width must be positive")
        edges = np.arange(x.min(), x.max() + width, width)
        if edges.size < 2:
            edges = np.array([x.min(), x.max() + width])
    else:
        bins = int(params.get("bins", 50))
        edges = np.linspace(x.min(), x.max(), bins + 1)
    index = np.clip(np.digitize(x, edges, right=False) - 1, 0, len(edges) - 2)
    rows = []
    for bin_index in range(len(edges) - 1):
        values = y[index == bin_index]
        coords = x[index == bin_index]
        if values.size:
            std = float(np.std(values, ddof=1)) if values.size > 1 else 0.0
            rows.append((float(np.mean(coords)), float(np.mean(values)), std, std / np.sqrt(values.size), values.size))
    if not rows:
        raise SignalLabError("no populated bins")
    columns = np.asarray(rows, dtype=float).T
    return result({"x": columns[0], "mean": columns[1], "std": columns[2], "sem": columns[3], "count": columns[4].astype(int)})


@algorithm(_spec(
    "preprocess.resample_uniform", "resampling", "Interpolate irregular paired data onto a uniform axis.",
    ("x", "y"), ("x", "y"),
    object_schema({"points": integer(minimum=2), "step": number(exclusive_minimum=0), "method": choice("linear", ("linear", "nearest", "cubic", "pchip"))}),
    tags=("interpolation", "uniform", "resample"), assumptions=("x is single-valued after sorting.",),
    caveats=("Interpolation does not create independent information.",),
))
def resample_uniform(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    x, y = paired_1d(payload)
    order = np.argsort(x)
    x, y = x[order], y[order]
    unique, indices = np.unique(x, return_index=True)
    x, y = unique, y[indices]
    require_strictly_increasing(x)
    if "step" in params:
        step = float(params["step"])
        target = np.arange(x[0], x[-1] + 0.5 * step, step)
    else:
        target = np.linspace(x[0], x[-1], int(params.get("points", x.size)))
    method = params.get("method", "linear")
    if method == "pchip":
        values = interpolate.PchipInterpolator(x, y)(target)
    else:
        values = interpolate.interp1d(x, y, kind=method, bounds_error=True)(target)
    return result({"x": target, "y": values}, metadata={"interpolation": method})


@algorithm(_spec(
    "calibration.subtract_reference", "calibration", "Subtract a background or reference trace point by point.",
    ("signal", "reference"), ("corrected",), tags=("background", "reference", "subtract"),
))
def subtract_reference(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    sample = np.asarray(payload["signal"], dtype=float)
    reference = np.asarray(payload["reference"], dtype=float)
    if sample.shape != reference.shape:
        raise SignalLabError("signal and reference must have identical shapes")
    return result({"corrected": sample - reference})


@algorithm(_spec(
    "calibration.ratio_reference", "calibration", "Divide a signal by a reference trace with explicit zero handling.",
    ("signal", "reference"), ("ratio", "valid_mask"),
    object_schema({"epsilon": number(0.0, minimum=0.0)}), tags=("reference", "ratio", "normalization"),
))
def ratio_reference(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    sample = np.asarray(payload["signal"], dtype=float)
    reference = np.asarray(payload["reference"], dtype=float)
    if sample.shape != reference.shape:
        raise SignalLabError("signal and reference must have identical shapes")
    epsilon = float(params.get("epsilon", 0.0))
    valid = np.abs(reference) > epsilon
    ratio = np.full(sample.shape, np.nan, dtype=float)
    np.divide(sample, reference, out=ratio, where=valid)
    warnings = [] if np.all(valid) else [f"masked {int((~valid).sum())} near-zero reference values"]
    return result({"ratio": ratio, "valid_mask": valid}, warnings=warnings)


@algorithm(_spec(
    "preprocess.normalize", "scaling", "Normalize an array by max, area, L2 norm, z-score, or min-max range.",
    ("y",), ("normalized", "offset", "scale"),
    object_schema({"mode": choice("max", ("max", "area", "l2", "zscore", "minmax")), "absolute": boolean(True)}),
    tags=("normalize", "scaling"),
))
def normalize(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    y = as_1d(payload["y"], "y")
    mode = params.get("mode", "max")
    absolute = bool(params.get("absolute", True))
    offset = 0.0
    if mode == "zscore":
        offset, scale = float(np.mean(y)), float(np.std(y, ddof=1))
    elif mode == "minmax":
        offset, scale = float(np.min(y)), float(np.max(y) - np.min(y))
    elif mode == "area":
        x = np.asarray(payload.get("x", np.arange(y.size)), dtype=float)
        if x.shape != y.shape:
            raise SignalLabError("optional x must match y for area normalization")
        scale = float(np.trapezoid(np.abs(y) if absolute else y, x))
    elif mode == "l2":
        scale = float(np.linalg.norm(y))
    else:
        scale = float(np.max(np.abs(y)) if absolute else np.max(y))
    if not np.isfinite(scale) or scale == 0:
        raise SignalLabError("normalization scale is zero or non-finite")
    return result({"normalized": (y - offset) / scale, "offset": offset, "scale": scale})


@algorithm(_spec(
    "baseline.polynomial", "baseline", "Fit and subtract a polynomial baseline.",
    ("x", "y"), ("corrected", "baseline", "coefficients"),
    object_schema({"degree": integer(2, minimum=0, maximum=12), "edge_fraction": number(1.0, exclusive_minimum=0.0, maximum=1.0)}),
    tags=("baseline", "polynomial", "detrend"), caveats=("A polynomial can absorb broad physical features; inspect the baseline.",),
))
def polynomial_baseline(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    x, y = paired_1d(payload)
    degree = int(params.get("degree", 2))
    fraction = float(params.get("edge_fraction", 1.0))
    mask = np.ones(x.size, dtype=bool)
    if fraction < 1.0:
        count = max(degree + 1, int(np.ceil(x.size * fraction / 2.0)))
        mask[:] = False
        mask[:count] = True
        mask[-count:] = True
    if mask.sum() <= degree:
        raise SignalLabError("not enough baseline points for requested degree")
    center, scale = float(np.mean(x)), float(np.ptp(x) / 2.0 or 1.0)
    coefficients = np.polynomial.polynomial.polyfit((x[mask] - center) / scale, y[mask], degree)
    baseline = np.polynomial.polynomial.polyval((x - center) / scale, coefficients)
    return result({"corrected": y - baseline, "baseline": baseline, "coefficients": coefficients}, metadata={"x_center": center, "x_scale": scale})


@algorithm(_spec(
    "baseline.asls", "baseline", "Asymmetric least-squares baseline for spectra with positive peaks.",
    ("y",), ("corrected", "baseline"),
    object_schema({"lambda": number(1e6, exclusive_minimum=0.0), "asymmetry": number(0.01, exclusive_minimum=0.0, maximum=1.0), "iterations": integer(20, minimum=1, maximum=200)}),
    tags=("baseline", "asls", "spectroscopy"), assumptions=("Signal peaks are mainly positive relative to a smooth baseline.",),
    caveats=("lambda and asymmetry are scale- and sampling-dependent.",), references=(ASLS_REF,),
))
def asls_baseline(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    y = as_1d(payload["y"], "y")
    if y.size < 4:
        raise SignalLabError("AsLS requires at least four samples")
    lam = float(params.get("lambda", 1e6))
    asymmetry = float(params.get("asymmetry", 0.01))
    iterations = int(params.get("iterations", 20))
    difference = sparse.diags([1.0, -2.0, 1.0], [0, 1, 2], shape=(y.size - 2, y.size), format="csc")
    penalty = lam * (difference.T @ difference)
    weights = np.ones(y.size)
    baseline = np.zeros_like(y)
    for _ in range(iterations):
        system = sparse.spdiags(weights, 0, y.size, y.size) + penalty
        baseline = spsolve(system, weights * y)
        weights = np.where(y > baseline, asymmetry, 1.0 - asymmetry)
    return result({"corrected": y - baseline, "baseline": baseline})


@algorithm(_spec(
    "outlier.hampel", "outlier", "Replace local median-absolute-deviation outliers with the local median.",
    ("y",), ("filtered", "outlier_mask"),
    object_schema({"window": integer(7, minimum=3), "sigma": number(3.0, exclusive_minimum=0.0)}),
    tags=("outlier", "hampel", "despike"), caveats=("May remove narrow real peaks if the window is too short.",),
))
def hampel_filter(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    y = as_1d(payload["y"], "y")
    window = odd_window(int(params.get("window", 7)), y.size)
    sigma = float(params.get("sigma", 3.0))
    median = ndimage.median_filter(y, size=window, mode="reflect")
    deviation = ndimage.median_filter(np.abs(y - median), size=window, mode="reflect")
    threshold = sigma * 1.4826 * deviation
    mask = np.abs(y - median) > np.maximum(threshold, np.finfo(float).eps)
    filtered = y.copy()
    filtered[mask] = median[mask]
    return result({"filtered": filtered, "outlier_mask": mask})


@algorithm(_spec(
    "filter.savgol", "filter", "Savitzky-Golay smoothing or derivative estimation.",
    ("y",), ("filtered",),
    object_schema({"window": integer(9, minimum=3), "polyorder": integer(3, minimum=0), "derivative": integer(0, minimum=0), "delta": number(1.0, exclusive_minimum=0.0)}),
    tags=("filter", "smoothing", "derivative", "savitzky-golay"), caveats=("Preserves polynomial features but can ring at abrupt transitions.",), references=(SG_REF, SCIPY_REF),
))
def savgol_filter(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    y = as_1d(payload["y"], "y")
    window = odd_window(int(params.get("window", 9)), y.size)
    polyorder = int(params.get("polyorder", 3))
    derivative = int(params.get("derivative", 0))
    if polyorder >= window:
        raise SignalLabError("polyorder must be smaller than window")
    if derivative > polyorder:
        raise SignalLabError("derivative must be <= polyorder")
    filtered = signal.savgol_filter(y, window, polyorder, deriv=derivative, delta=float(params.get("delta", 1.0)), mode="interp")
    return result({"filtered": filtered})


@algorithm(_spec(
    "filter.gaussian", "filter", "Gaussian convolution smoothing in sample units.",
    ("y",), ("filtered",), object_schema({"sigma": number(1.0, exclusive_minimum=0.0)}),
    tags=("filter", "gaussian", "smoothing"), caveats=("Broadens peaks by the filter point-spread function.",),
))
def gaussian_filter(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    y = as_1d(payload["y"], "y")
    return result({"filtered": ndimage.gaussian_filter1d(y, float(params.get("sigma", 1.0)), mode="reflect")})


@algorithm(_spec(
    "filter.butterworth", "filter", "Zero-phase Butterworth low-, high-, band-pass, or band-stop filter.",
    ("time", "y"), ("filtered",),
    object_schema({"kind": choice("lowpass", ("lowpass", "highpass", "bandpass", "bandstop")), "cutoff": {"type": "array"}, "order": integer(4, minimum=1, maximum=20)}),
    tags=("filter", "butterworth", "zero-phase"), assumptions=("time is uniformly sampled.",), caveats=("filtfilt is noncausal and unsuitable for real-time latency claims.",), references=(SCIPY_REF,),
))
def butterworth_filter(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    time, y = paired_1d(payload, "time", "y")
    dt = require_uniform_spacing(time, "time")
    nyquist = 0.5 / dt
    cutoff = np.atleast_1d(params.get("cutoff", [0.1 * nyquist])).astype(float)
    if np.any(cutoff <= 0) or np.any(cutoff >= nyquist):
        raise SignalLabError(f"cutoff must lie strictly between 0 and Nyquist ({nyquist:g})")
    kind = params.get("kind", "lowpass")
    expected = 2 if kind in {"bandpass", "bandstop"} else 1
    if cutoff.size != expected:
        raise SignalLabError(f"{kind} requires {expected} cutoff value(s)")
    sos = signal.butter(int(params.get("order", 4)), cutoff / nyquist, btype=kind, output="sos")
    return result({"filtered": signal.sosfiltfilt(sos, y)}, metadata={"sample_rate": 1.0 / dt})


@algorithm(_spec(
    "filter.notch", "filter", "Zero-phase IIR notch filter for a known narrow interference frequency.",
    ("time", "y"), ("filtered",),
    object_schema({"frequency": number(exclusive_minimum=0.0), "quality_factor": number(30.0, exclusive_minimum=0.0)}, required=("frequency",)),
    tags=("filter", "notch", "line-noise"), assumptions=("time is uniformly sampled.",), caveats=("Inspect phase/amplitude distortion near the notch.",), references=(SCIPY_REF,),
))
def notch_filter(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    time, y = paired_1d(payload, "time", "y")
    dt = require_uniform_spacing(time, "time")
    fs = 1.0 / dt
    frequency = float(params["frequency"])
    if frequency >= fs / 2:
        raise SignalLabError("notch frequency must be below Nyquist")
    b, a = signal.iirnotch(frequency, float(params.get("quality_factor", 30.0)), fs=fs)
    return result({"filtered": signal.filtfilt(b, a, y)}, metadata={"sample_rate": fs})


@algorithm(_spec(
    "calculus.derivative", "calculus", "Estimate dy/dx using second-order finite differences.",
    ("x", "y"), ("derivative",),
    object_schema({"order": integer(1, minimum=1, maximum=4)}), tags=("derivative", "gradient"), caveats=("Differentiation amplifies high-frequency noise; smooth only with a justified bandwidth.",),
))
def numerical_derivative(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    x, y = paired_1d(payload)
    require_strictly_increasing(x)
    derivative = y.copy()
    for _ in range(int(params.get("order", 1))):
        derivative = np.gradient(derivative, x, edge_order=2)
    return result({"derivative": derivative})


@algorithm(_spec(
    "calculus.cumulative_integral", "calculus", "Cumulative trapezoidal integral with a defined zero origin.",
    ("x", "y"), ("integral",), tags=("integral", "cumulative"),
))
def cumulative_integral(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    x, y = paired_1d(payload)
    require_strictly_increasing(x)
    return result({"integral": np.concatenate(([0.0], np.cumsum(0.5 * (y[1:] + y[:-1]) * np.diff(x))))})


@algorithm(_spec(
    "alignment.cross_correlation_shift", "alignment", "Estimate and apply an integer-sample shift by normalized cross-correlation.",
    ("reference", "moving"), ("aligned", "shift_samples", "correlation"),
    tags=("alignment", "cross-correlation", "shift"), assumptions=("Traces share a sampling interval and differ mainly by translation.",),
))
def cross_correlation_shift(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    reference = as_1d(payload["reference"], "reference")
    moving = as_1d(payload["moving"], "moving")
    if reference.size != moving.size:
        raise SignalLabError("reference and moving must have equal length")
    a = reference - np.mean(reference)
    b = moving - np.mean(moving)
    correlation = signal.correlate(a, b, mode="full", method="fft")
    lags = signal.correlation_lags(a.size, b.size, mode="full")
    shift = int(lags[np.argmax(correlation)])
    aligned = ndimage.shift(moving, shift=shift, order=1, mode="constant", cval=np.nan, prefilter=False)
    norm = np.linalg.norm(a) * np.linalg.norm(b)
    peak = float(np.max(correlation) / norm) if norm else np.nan
    return result({"aligned": aligned, "shift_samples": shift, "correlation": peak})


@algorithm(_spec(
    "uncertainty.bootstrap_mean_ci", "uncertainty", "Nonparametric bootstrap confidence interval for a sample mean.",
    ("samples",), ("mean", "lower", "upper", "bootstrap_means"),
    object_schema({"confidence": number(0.95, exclusive_minimum=0.0, maximum=1.0), "resamples": integer(2000, minimum=100), "seed": integer(0, minimum=0)}),
    tags=("bootstrap", "confidence-interval", "uncertainty"), assumptions=("Samples are exchangeable; dependence requires block bootstrap.",),
))
def bootstrap_mean_ci(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    samples = as_1d(payload["samples"], "samples")
    confidence = float(params.get("confidence", 0.95))
    resamples = int(params.get("resamples", 2000))
    rng = np.random.default_rng(int(params.get("seed", 0)))
    bootstrap_means = np.empty(resamples)
    chunk = 256
    for start in range(0, resamples, chunk):
        stop = min(start + chunk, resamples)
        indices = rng.integers(0, samples.size, size=(stop - start, samples.size))
        bootstrap_means[start:stop] = np.mean(samples[indices], axis=1)
    alpha = (1.0 - confidence) / 2.0
    lower, upper = np.quantile(bootstrap_means, [alpha, 1.0 - alpha])
    return result({"mean": float(np.mean(samples)), "lower": float(lower), "upper": float(upper), "bootstrap_means": bootstrap_means})
