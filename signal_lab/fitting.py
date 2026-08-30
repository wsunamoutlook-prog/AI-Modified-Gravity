"""Atomic peak detection, line-shape fitting, and regression methods."""

from __future__ import annotations

from typing import Any, Mapping

import numpy as np
from scipy import optimize, signal, special

from .model import AlgorithmResult, AlgorithmSpec, result
from .registry import algorithm
from .schemas import boolean, choice, integer, number, object_schema
from .validation import SignalLabError, paired_1d, require_strictly_increasing

SCIPY_SIGNAL_REF = "SciPy signal API, https://docs.scipy.org/doc/scipy/reference/signal.html"


def _spec(
    name: str,
    summary: str,
    inputs: tuple[str, ...],
    outputs: tuple[str, ...],
    schema: Mapping[str, Any] | None = None,
    *,
    category: str = "fitting",
    tags: tuple[str, ...] = (),
    assumptions: tuple[str, ...] = (),
    caveats: tuple[str, ...] = (),
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
        references=(SCIPY_SIGNAL_REF,),
    )


@algorithm(_spec(
    "peaks.find", "Locate peaks and return standard geometric properties.",
    ("x", "y"), ("indices", "x_peaks", "y_peaks", "properties"),
    object_schema({
        "height": number(), "prominence": number(minimum=0.0), "distance": integer(minimum=1),
        "width": number(minimum=0.0), "polarity": choice("positive", ("positive", "negative")),
    }),
    tags=("peaks", "prominence", "spectroscopy"),
    caveats=("Detection thresholds must be reported and tested against noise and resolution.",),
))
def find_peaks(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    x, y = paired_1d(payload)
    target = -y if params.get("polarity", "positive") == "negative" else y
    kwargs = {key: params[key] for key in ("height", "prominence", "distance", "width") if key in params}
    indices, properties = signal.find_peaks(target, **kwargs)
    serial_properties = {key: np.asarray(value) for key, value in properties.items()}
    return result({"indices": indices, "x_peaks": x[indices], "y_peaks": y[indices], "properties": serial_properties})


def _gaussian(x: np.ndarray, amplitude: float, center: float, sigma: float, offset: float) -> np.ndarray:
    return offset + amplitude * np.exp(-0.5 * ((x - center) / sigma) ** 2)


def _lorentzian(x: np.ndarray, amplitude: float, center: float, hwhm: float, offset: float) -> np.ndarray:
    return offset + amplitude / (1.0 + ((x - center) / hwhm) ** 2)


def _voigt(x: np.ndarray, area: float, center: float, sigma: float, gamma: float, offset: float) -> np.ndarray:
    profile = special.voigt_profile(x - center, sigma, gamma)
    return offset + area * profile


def _pseudo_voigt(
    x: np.ndarray, amplitude: float, center: float, fwhm: float, eta: float, offset: float
) -> np.ndarray:
    gaussian = np.exp(-4.0 * np.log(2.0) * ((x - center) / fwhm) ** 2)
    lorentzian = 1.0 / (1.0 + 4.0 * ((x - center) / fwhm) ** 2)
    return offset + amplitude * (eta * lorentzian + (1.0 - eta) * gaussian)


@algorithm(_spec(
    "peaks.fit_single", "Fit one Gaussian, Lorentzian, Voigt, or pseudo-Voigt peak plus constant offset.",
    ("x", "y"), ("fit", "residual", "parameters", "standard_errors", "covariance", "reduced_chi2"),
    object_schema({"model": choice("gaussian", ("gaussian", "lorentzian", "voigt", "pseudo_voigt")), "absolute_sigma": boolean(False)}),
    tags=("peak-fit", "gaussian", "lorentzian", "voigt"),
    assumptions=("The selected interval contains one resolvable peak and a constant baseline.",),
    caveats=("Line-shape parameters are model dependent; inspect residuals and covariance.",),
))
def fit_single_peak(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    x, y = paired_1d(payload)
    require_strictly_increasing(x)
    if x.size < 6:
        raise SignalLabError("single-peak fitting requires at least six points")
    uncertainty = payload.get("sigma")
    sigma_y = None if uncertainty is None else np.asarray(uncertainty, dtype=float)
    if sigma_y is not None and sigma_y.shape != y.shape:
        raise SignalLabError("sigma must match y")
    offset = float(np.percentile(y, 10))
    amplitude = float(y.max() - offset)
    center = float(x[np.argmax(y)])
    width = max(float(np.ptp(x) / 10.0), np.finfo(float).eps)
    model_name = params.get("model", "gaussian")
    if model_name == "lorentzian":
        function, p0 = _lorentzian, [amplitude, center, width, offset]
        bounds = ([-np.inf, x.min(), np.finfo(float).eps, -np.inf], [np.inf, x.max(), np.inf, np.inf])
        names = ("amplitude", "center", "hwhm", "offset")
    elif model_name == "voigt":
        function, p0 = _voigt, [amplitude * width, center, width, width, offset]
        bounds = ([-np.inf, x.min(), np.finfo(float).eps, np.finfo(float).eps, -np.inf], [np.inf, x.max(), np.inf, np.inf, np.inf])
        names = ("area", "center", "sigma", "gamma", "offset")
    elif model_name == "pseudo_voigt":
        function, p0 = _pseudo_voigt, [amplitude, center, 2.0 * width, 0.5, offset]
        bounds = ([-np.inf, x.min(), np.finfo(float).eps, 0.0, -np.inf], [np.inf, x.max(), np.inf, 1.0, np.inf])
        names = ("amplitude", "center", "fwhm", "eta", "offset")
    else:
        function, p0 = _gaussian, [amplitude, center, width, offset]
        bounds = ([-np.inf, x.min(), np.finfo(float).eps, -np.inf], [np.inf, x.max(), np.inf, np.inf])
        names = ("amplitude", "center", "sigma", "offset")
    fitted, covariance = optimize.curve_fit(
        function, x, y, p0=p0, bounds=bounds, sigma=sigma_y,
        absolute_sigma=bool(params.get("absolute_sigma", False)), maxfev=20000,
    )
    prediction = function(x, *fitted)
    residual = y - prediction
    dof = max(1, y.size - fitted.size)
    chi2 = float(np.sum((residual / sigma_y) ** 2) / dof) if sigma_y is not None else float(np.sum(residual**2) / dof)
    errors = np.sqrt(np.clip(np.diag(covariance), 0.0, np.inf))
    return result({
        "fit": prediction, "residual": residual,
        "parameters": dict(zip(names, fitted)),
        "standard_errors": dict(zip(names, errors)),
        "covariance": covariance, "reduced_chi2": chi2,
    }, metadata={"model": model_name})


@algorithm(_spec(
    "peaks.integrate", "Integrate baseline-subtracted area in an axis interval.",
    ("x", "y"), ("area", "xmin", "xmax"),
    object_schema({"xmin": number(), "xmax": number(), "baseline": choice("none", ("none", "linear_edges"))}),
    tags=("peak-area", "integration"),
))
def integrate_peak(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    x, y = paired_1d(payload)
    require_strictly_increasing(x)
    xmin = float(params.get("xmin", x.min()))
    xmax = float(params.get("xmax", x.max()))
    mask = (x >= xmin) & (x <= xmax)
    if mask.sum() < 2:
        raise SignalLabError("integration interval must contain at least two samples")
    xp, yp = x[mask], y[mask]
    if params.get("baseline", "none") == "linear_edges":
        yp = yp - np.interp(xp, [xp[0], xp[-1]], [yp[0], yp[-1]])
    return result({"area": float(np.trapezoid(yp, xp)), "xmin": xmin, "xmax": xmax})


@algorithm(_spec(
    "peaks.fwhm", "Estimate peak center and full width at half maximum by interpolation.",
    ("x", "y"), ("center", "left", "right", "fwhm"),
    tags=("fwhm", "linewidth", "peak"), assumptions=("The trace contains one dominant peak and is baseline corrected.",),
))
def estimate_fwhm(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    x, y = paired_1d(payload)
    require_strictly_increasing(x)
    index = int(np.argmax(y))
    half = 0.5 * float(y[index])
    left_candidates = np.flatnonzero(y[:index] <= half)
    right_candidates = np.flatnonzero(y[index + 1 :] <= half)
    if not left_candidates.size or not right_candidates.size:
        raise SignalLabError("peak does not cross half maximum on both sides")
    li = int(left_candidates[-1])
    ri = int(index + 1 + right_candidates[0])
    left = float(np.interp(half, [y[li], y[li + 1]], [x[li], x[li + 1]]))
    right = float(np.interp(half, [y[ri], y[ri - 1]], [x[ri], x[ri - 1]]))
    return result({"center": float(x[index]), "left": left, "right": right, "fwhm": right - left})


def _decay(t: np.ndarray, amplitude: float, tau: float, offset: float) -> np.ndarray:
    return offset + amplitude * np.exp(-t / tau)


@algorithm(_spec(
    "fit.exponential_decay", "Fit y(t)=offset+amplitude*exp(-t/tau).",
    ("time", "y"), ("fit", "residual", "amplitude", "tau", "offset", "covariance"),
    tags=("decay", "lifetime", "relaxation"), assumptions=("One exponential dominates over the selected interval.",),
    caveats=("Instrument response convolution is not included; use only when its width is negligible.",),
))
def fit_exponential_decay(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    time, y = paired_1d(payload, "time", "y")
    require_strictly_increasing(time, "time")
    shifted = time - time[0]
    offset0 = float(np.median(y[-max(2, y.size // 10) :]))
    amplitude0 = float(y[0] - offset0)
    tau0 = max(float(np.ptp(time) / 3.0), np.finfo(float).eps)
    fitted, covariance = optimize.curve_fit(_decay, shifted, y, p0=[amplitude0, tau0, offset0], bounds=([-np.inf, np.finfo(float).eps, -np.inf], [np.inf, np.inf, np.inf]), maxfev=20000)
    prediction = _decay(shifted, *fitted)
    return result({"fit": prediction, "residual": y - prediction, "amplitude": float(fitted[0]), "tau": float(fitted[1]), "offset": float(fitted[2]), "covariance": covariance})


@algorithm(_spec(
    "fit.power_law", "Fit y=A*x^exponent in log space with positive samples.",
    ("x", "y"), ("amplitude", "exponent", "fit", "r_squared"),
    tags=("power-law", "scaling", "log-log"), assumptions=("x and y are positive and log-space residuals are appropriate.",),
))
def fit_power_law(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    x, y = paired_1d(payload)
    mask = (x > 0) & (y > 0)
    if mask.sum() < 3:
        raise SignalLabError("power-law fitting needs at least three positive samples")
    slope, intercept = np.polyfit(np.log(x[mask]), np.log(y[mask]), 1)
    prediction = np.exp(intercept) * x[mask] ** slope
    residual = np.log(y[mask]) - np.log(prediction)
    total = np.log(y[mask]) - np.mean(np.log(y[mask]))
    r2 = 1.0 - float(np.sum(residual**2) / np.sum(total**2)) if np.sum(total**2) else np.nan
    return result({"amplitude": float(np.exp(intercept)), "exponent": float(slope), "fit": prediction, "r_squared": r2}, metadata={"kept_mask": mask})


@algorithm(_spec(
    "fit.robust_linear", "Robust straight-line regression using a soft-L1 loss.",
    ("x", "y"), ("slope", "intercept", "fit", "residual", "r_squared"),
    object_schema({"loss_scale": number(1.0, exclusive_minimum=0.0)}),
    tags=("linear", "robust", "regression"), caveats=("Robust loss downweights outliers but does not identify their physical cause.",),
))
def robust_linear(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    x, y = paired_1d(payload)
    initial = np.polyfit(x, y, 1)
    fit = optimize.least_squares(lambda coefficients: coefficients[0] * x + coefficients[1] - y, initial, loss="soft_l1", f_scale=float(params.get("loss_scale", 1.0)))
    slope, intercept = fit.x
    prediction = slope * x + intercept
    residual = y - prediction
    total = y - np.mean(y)
    r2 = 1.0 - float(np.sum(residual**2) / np.sum(total**2)) if np.sum(total**2) else np.nan
    return result({"slope": float(slope), "intercept": float(intercept), "fit": prediction, "residual": residual, "r_squared": r2})
