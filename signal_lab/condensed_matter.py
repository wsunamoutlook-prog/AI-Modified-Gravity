"""Atomic algorithms for condensed-matter transport, thermodynamics, and diffraction."""

from __future__ import annotations

from typing import Any, Mapping

import numpy as np
from scipy import optimize, signal

from .model import AlgorithmResult, AlgorithmSpec, result
from .registry import algorithm
from .schemas import choice, integer, number, object_schema
from .validation import SignalLabError, as_1d, paired_1d, require_strictly_increasing, require_uniform_spacing

NIST_HALL_REF = "NIST, The Hall Effect and van der Pauw Technique, https://www.nist.gov/pml/nanoscale-device-characterization-division/popular-links/hall-effect/hall-effect"
VDP_REF = "van der Pauw, Philips Res. Rep. 13, 1 (1958)"
LK_REF = "Lifshitz and Kosevich, Sov. Phys. JETP 2, 636 (1956); Shoenberg, Magnetic Oscillations in Metals"
RIETVELD_REF = "Rietveld, J. Appl. Cryst. 2, 65 (1969), doi:10.1107/S0021889869006558"
SHIRLEY_REF = "Shirley, Phys. Rev. B 5, 4709 (1972), doi:10.1103/PhysRevB.5.4709"

E_CHARGE = 1.602176634e-19
K_B_EV = 8.617333262145e-5
K_B = 1.380649e-23
HBAR = 1.054571817e-34
M_E = 9.1093837139e-31
R_GAS = 8.31446261815324


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
        name=name, domain="condensed_matter", category=category, summary=summary,
        required_inputs=inputs, outputs=outputs,
        parameter_schema=schema or object_schema(), tags=tags,
        assumptions=assumptions, caveats=caveats, references=references,
    )


@algorithm(_spec(
    "transport.field_even_odd", "transport", "Interpolate positive and negative field sweeps onto |B| and separate even/odd components.",
    ("field", "signal"), ("field_abs", "even", "odd", "positive_branch", "negative_branch"),
    object_schema({"points": integer(minimum=3), "max_abs_field": number(exclusive_minimum=0.0)}),
    tags=("symmetrize", "antisymmetrize", "magnetic-field", "hall"), assumptions=("Both field polarities cover an overlapping range and hysteresis is negligible or separately treated.",), caveats=("Interpolation across hysteretic branches can erase real path dependence; split sweep direction first when needed.",),
))
def field_even_odd(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    field, values = paired_1d(payload, "field", "signal")
    positive = field >= 0
    negative = field <= 0
    if positive.sum() < 2 or negative.sum() < 2:
        raise SignalLabError("both positive and negative field branches need at least two samples")
    bp, yp = field[positive], values[positive]
    bn, yn = -field[negative], values[negative]
    op, on = np.argsort(bp), np.argsort(bn)
    bp, yp, bn, yn = bp[op], yp[op], bn[on], yn[on]
    bp, ip = np.unique(bp, return_index=True)
    bn, inn = np.unique(bn, return_index=True)
    yp, yn = yp[ip], yn[inn]
    upper = min(float(bp[-1]), float(bn[-1]), float(params.get("max_abs_field", np.inf)))
    if upper <= max(float(bp[0]), float(bn[0])):
        raise SignalLabError("positive and negative branches have no overlapping |B| range")
    points = int(params.get("points", min(bp.size, bn.size)))
    grid = np.linspace(max(float(bp[0]), float(bn[0])), upper, points)
    pos = np.interp(grid, bp, yp)
    neg = np.interp(grid, bn, yn)
    return result({"field_abs": grid, "even": 0.5 * (pos + neg), "odd": 0.5 * (pos - neg), "positive_branch": pos, "negative_branch": neg})


@algorithm(_spec(
    "transport.resistivity_geometry", "transport", "Convert four-probe resistance to bulk resistivity rho=R*area/length.",
    ("resistance",), ("resistivity",),
    object_schema({"length": number(exclusive_minimum=0.0), "cross_section_area": number(exclusive_minimum=0.0)}, required=("length", "cross_section_area")),
    tags=("resistivity", "four-probe", "geometry"), assumptions=("Current density is uniform and voltage-probe spacing equals length.",), caveats=("Contact placement, anisotropy, current jetting, and geometric uncertainty may dominate.",),
))
def resistivity_geometry(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    resistance = np.asarray(payload["resistance"], dtype=float)
    return result({"resistivity": resistance * float(params["cross_section_area"]) / float(params["length"])})


@algorithm(_spec(
    "transport.van_der_pauw", "transport", "Solve the van der Pauw equation for sheet resistance and optional bulk resistivity.",
    ("resistance_a", "resistance_b"), ("sheet_resistance", "resistivity"),
    object_schema({"thickness": number(exclusive_minimum=0.0)}),
    tags=("van-der-pauw", "sheet-resistance", "resistivity"), assumptions=("Thin, uniform, simply connected sample with small ohmic contacts on its perimeter.",), caveats=("Large contacts, holes, anisotropy, and inhomogeneity violate the method assumptions.",), references=(NIST_HALL_REF, VDP_REF),
))
def van_der_pauw(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    ra = float(np.asarray(payload["resistance_a"], dtype=float))
    rb = float(np.asarray(payload["resistance_b"], dtype=float))
    if ra <= 0 or rb <= 0:
        raise SignalLabError("van der Pauw resistances must be positive")
    equation = lambda rs: np.exp(-np.pi * ra / rs) + np.exp(-np.pi * rb / rs) - 1.0
    lower = min(ra, rb) * 1e-9
    upper = max(ra, rb) * 1e9
    sheet = float(optimize.brentq(equation, lower, upper))
    resistivity = sheet * float(params["thickness"]) if "thickness" in params else np.nan
    return result({"sheet_resistance": sheet, "resistivity": resistivity})


@algorithm(_spec(
    "transport.hall_linear", "transport", "Fit odd Hall resistance versus field and infer sheet/bulk carrier density.",
    ("field", "hall_resistance"), ("hall_slope", "intercept", "fit", "r_squared", "sheet_density_m2", "bulk_density_m3", "carrier_sign"),
    object_schema({"thickness": number(exclusive_minimum=0.0), "min_abs_field": number(0.0, minimum=0.0), "max_abs_field": number(exclusive_minimum=0.0)}),
    tags=("hall", "carrier-density", "linear-fit"), assumptions=("A single dominant carrier type gives a linear Hall response in the selected field range.",), caveats=("Multiband conduction, anomalous Hall effect, contact mixing, and nonlinear response require a more complete model.",), references=(NIST_HALL_REF,),
))
def hall_linear(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    field, resistance = paired_1d(payload, "field", "hall_resistance")
    mask = np.abs(field) >= float(params.get("min_abs_field", 0.0))
    if "max_abs_field" in params:
        mask &= np.abs(field) <= float(params["max_abs_field"])
    if mask.sum() < 3:
        raise SignalLabError("Hall fit range needs at least three points")
    slope, intercept = np.polyfit(field[mask], resistance[mask], 1)
    prediction = slope * field[mask] + intercept
    total = resistance[mask] - np.mean(resistance[mask])
    r2 = 1.0 - float(np.sum((resistance[mask] - prediction) ** 2) / np.sum(total**2)) if np.sum(total**2) else np.nan
    sheet_density = 1.0 / (E_CHARGE * abs(slope)) if slope != 0 else np.inf
    bulk_density = sheet_density / float(params["thickness"]) if "thickness" in params else np.nan
    return result({"hall_slope": float(slope), "intercept": float(intercept), "fit": prediction, "r_squared": r2, "sheet_density_m2": sheet_density, "bulk_density_m3": bulk_density, "carrier_sign": -1 if slope < 0 else 1}, metadata={"kept_mask": mask})


@algorithm(_spec(
    "transport.hall_mobility", "transport", "Compute Hall mobility mu=|dRxy/dB|/R_sheet.",
    ("hall_slope", "sheet_resistance"), ("mobility_m2_per_vs", "mobility_cm2_per_vs"),
    tags=("hall", "mobility", "sheet-resistance"), assumptions=("Single-carrier Hall coefficient and sheet resistance describe the same conducting channel.",), references=(NIST_HALL_REF,),
))
def hall_mobility(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    slope = np.asarray(payload["hall_slope"], dtype=float)
    sheet = np.asarray(payload["sheet_resistance"], dtype=float)
    if np.any(sheet <= 0):
        raise SignalLabError("sheet_resistance must be positive")
    mobility = np.abs(slope) / sheet
    return result({"mobility_m2_per_vs": mobility, "mobility_cm2_per_vs": 1e4 * mobility})


@algorithm(_spec(
    "transport.conductivity_tensor", "transport", "Invert an isotropic 2D resistivity tensor into sigma_xx and sigma_xy.",
    ("rho_xx", "rho_xy"), ("sigma_xx", "sigma_xy"),
    object_schema({"hall_sign": choice("inverse_matrix", ("inverse_matrix", "same_sign"))}),
    tags=("conductivity", "resistivity", "tensor", "hall"), caveats=("Sign conventions for rho_xy and sigma_xy vary; metadata records the selected convention.",),
))
def conductivity_tensor(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    rho_xx = np.asarray(payload["rho_xx"], dtype=float)
    rho_xy = np.asarray(payload["rho_xy"], dtype=float)
    if rho_xx.shape != rho_xy.shape:
        raise SignalLabError("rho_xx and rho_xy must have identical shapes")
    denominator = rho_xx**2 + rho_xy**2
    if np.any(denominator == 0):
        raise SignalLabError("resistivity tensor is singular")
    sign = -1.0 if params.get("hall_sign", "inverse_matrix") == "inverse_matrix" else 1.0
    return result({"sigma_xx": rho_xx / denominator, "sigma_xy": sign * rho_xy / denominator}, metadata={"hall_sign": params.get("hall_sign", "inverse_matrix")})


@algorithm(_spec(
    "transport.magnetoresistance", "transport", "Compute percent magnetoresistance relative to a supplied or near-zero-field resistance.",
    ("field", "resistance"), ("magnetoresistance_percent", "reference_resistance"),
    object_schema({"reference_resistance": number(exclusive_minimum=0.0)}),
    tags=("magnetoresistance", "field", "transport"), caveats=("Sweep hysteresis and zero-field drift should be checked before normalization.",),
))
def magnetoresistance(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    field, resistance = paired_1d(payload, "field", "resistance")
    reference = float(params.get("reference_resistance", resistance[np.argmin(np.abs(field))]))
    if reference == 0:
        raise SignalLabError("reference resistance is zero")
    return result({"magnetoresistance_percent": 100.0 * (resistance - reference) / reference, "reference_resistance": reference})


@algorithm(_spec(
    "transport.iv_linear_resistance", "transport", "Fit a linear I-V interval and return differential resistance and conductance.",
    ("current", "voltage"), ("resistance", "conductance", "offset_voltage", "fit", "r_squared"),
    object_schema({"min_current": number(), "max_current": number()}),
    tags=("iv", "resistance", "linear-fit"), assumptions=("The selected I-V interval is ohmic.",),
))
def iv_linear_resistance(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    current, voltage = paired_1d(payload, "current", "voltage")
    mask = np.ones(current.size, dtype=bool)
    if "min_current" in params:
        mask &= current >= float(params["min_current"])
    if "max_current" in params:
        mask &= current <= float(params["max_current"])
    if mask.sum() < 3:
        raise SignalLabError("I-V fit interval needs at least three points")
    resistance, offset = np.polyfit(current[mask], voltage[mask], 1)
    prediction = resistance * current[mask] + offset
    total = voltage[mask] - np.mean(voltage[mask])
    r2 = 1.0 - float(np.sum((voltage[mask] - prediction) ** 2) / np.sum(total**2)) if np.sum(total**2) else np.nan
    return result({"resistance": float(resistance), "conductance": float(1.0 / resistance) if resistance else np.inf, "offset_voltage": float(offset), "fit": prediction, "r_squared": r2}, metadata={"kept_mask": mask})


@algorithm(_spec(
    "transport.differential_conductance", "transport", "Estimate dI/dV from an I-V curve with optional Savitzky-Golay differentiation.",
    ("voltage", "current"), ("voltage", "differential_conductance"),
    object_schema({"method": choice("gradient", ("gradient", "savgol")), "window": integer(9, minimum=3), "polyorder": integer(3, minimum=1)}),
    tags=("didv", "sts", "iv", "derivative"), caveats=("Numerical differentiation amplifies noise; report smoothing parameters.",),
))
def differential_conductance(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    voltage, current = paired_1d(payload, "voltage", "current")
    order = np.argsort(voltage)
    voltage, current = voltage[order], current[order]
    require_strictly_increasing(voltage, "voltage")
    if params.get("method", "gradient") == "savgol":
        window = int(params.get("window", 9))
        if window % 2 == 0 or window < 3 or window > voltage.size:
            raise SignalLabError("window must be odd, >=3, and <= data length")
        step = require_uniform_spacing(voltage, "voltage")
        derivative = signal.savgol_filter(current, window, int(params.get("polyorder", 3)), deriv=1, delta=step, mode="interp")
    else:
        derivative = np.gradient(current, voltage, edge_order=2)
    return result({"voltage": voltage, "differential_conductance": derivative})


@algorithm(_spec(
    "transition.resistive_tc", "phase_transition", "Estimate a resistive transition temperature at a fraction of the normal-state resistance.",
    ("temperature", "resistance"), ("tc", "normal_resistance", "criterion_resistance"),
    object_schema({"fraction": number(0.5, exclusive_minimum=0.0, maximum=1.0), "normal_high_fraction": number(0.1, exclusive_minimum=0.0, maximum=0.5)}),
    tags=("superconductivity", "tc", "transition", "resistance"), assumptions=("Resistance decreases through the transition as temperature decreases.",), caveats=("Report the criterion (onset, midpoint, zero) and normal-state definition.",),
))
def resistive_tc(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    temperature, resistance = paired_1d(payload, "temperature", "resistance")
    order = np.argsort(temperature)
    temperature, resistance = temperature[order], resistance[order]
    count = max(2, int(np.ceil(temperature.size * float(params.get("normal_high_fraction", 0.1)))))
    normal = float(np.median(resistance[-count:]))
    criterion = float(params.get("fraction", 0.5)) * normal
    difference = resistance - criterion
    crossings = np.flatnonzero(difference[:-1] * difference[1:] <= 0)
    if not crossings.size:
        raise SignalLabError("resistance does not cross the selected transition criterion")
    index = int(crossings[-1])
    r0, r1 = float(resistance[index]), float(resistance[index + 1])
    t0, t1 = float(temperature[index]), float(temperature[index + 1])
    if r1 == r0:
        tc = 0.5 * (t0 + t1)
    else:
        tc = t0 + (criterion - r0) * (t1 - t0) / (r1 - r0)
    return result({"tc": tc, "normal_resistance": normal, "criterion_resistance": criterion})


@algorithm(_spec(
    "transition.critical_current", "phase_transition", "Find positive and negative critical currents from an absolute voltage criterion.",
    ("current", "voltage"), ("critical_current_positive", "critical_current_negative", "criterion_voltage"),
    object_schema({"voltage_criterion": number(exclusive_minimum=0.0)}, required=("voltage_criterion",)),
    tags=("critical-current", "superconductivity", "iv"), caveats=("Criterion and electric-field conversion must match the measurement standard and sample geometry.",),
))
def critical_current(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    current, voltage = paired_1d(payload, "current", "voltage")
    criterion = float(params["voltage_criterion"])
    positive = np.flatnonzero((current >= 0) & (np.abs(voltage) >= criterion))
    negative = np.flatnonzero((current <= 0) & (np.abs(voltage) >= criterion))
    icp = float(current[positive[np.argmin(current[positive])]]) if positive.size else np.nan
    icn = float(current[negative[np.argmax(current[negative])]]) if negative.size else np.nan
    warnings = [] if positive.size and negative.size else ["voltage criterion was not crossed on both current polarities"]
    return result({"critical_current_positive": icp, "critical_current_negative": icn, "criterion_voltage": criterion}, warnings=warnings)


@algorithm(_spec(
    "magnetism.hysteresis_metrics", "magnetism", "Estimate coercive fields, remanence, loop area, and saturation from an ordered M(B) loop.",
    ("field", "magnetization"), ("coercive_fields", "remanence", "loop_area", "saturation_estimate"),
    object_schema({"saturation_field_fraction": number(0.8, exclusive_minimum=0.0, maximum=1.0)}),
    tags=("hysteresis", "coercivity", "remanence", "magnetization"), assumptions=("Samples follow the acquisition order around a closed loop.",), caveats=("Background slope and incomplete saturation bias all reported metrics.",),
))
def hysteresis_metrics(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    field, magnetization = paired_1d(payload, "field", "magnetization")
    coercive: list[float] = []
    for index in np.flatnonzero(magnetization[:-1] * magnetization[1:] <= 0):
        if magnetization[index + 1] != magnetization[index]:
            coercive.append(float(field[index] + (0.0 - magnetization[index]) * (field[index + 1] - field[index]) / (magnetization[index + 1] - magnetization[index])))
    remanence: list[float] = []
    for index in np.flatnonzero(field[:-1] * field[1:] <= 0):
        if field[index + 1] != field[index]:
            remanence.append(float(magnetization[index] + (0.0 - field[index]) * (magnetization[index + 1] - magnetization[index]) / (field[index + 1] - field[index])))
    threshold = float(params.get("saturation_field_fraction", 0.8)) * np.max(np.abs(field))
    saturation = float(np.mean(np.abs(magnetization[np.abs(field) >= threshold])))
    return result({"coercive_fields": np.asarray(coercive), "remanence": np.asarray(remanence), "loop_area": float(abs(np.trapezoid(magnetization, field))), "saturation_estimate": saturation})


@algorithm(_spec(
    "thermal.arrhenius", "thermal_activation", "Fit Arrhenius transport and return activation energy in eV.",
    ("temperature", "observable"), ("activation_energy_ev", "prefactor", "fit", "r_squared"),
    object_schema({"mode": choice("resistance", ("resistance", "conductivity")), "tmin": number(exclusive_minimum=0.0), "tmax": number(exclusive_minimum=0.0)}),
    tags=("arrhenius", "activation-energy", "temperature"), assumptions=("One thermally activated process dominates and observable is positive.",), caveats=("Select and report the linear 1/T interval; multiple channels cause curvature.",),
))
def arrhenius_fit(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    temperature, observable = paired_1d(payload, "temperature", "observable")
    mask = (temperature > 0) & (observable > 0)
    if "tmin" in params:
        mask &= temperature >= float(params["tmin"])
    if "tmax" in params:
        mask &= temperature <= float(params["tmax"])
    if mask.sum() < 3:
        raise SignalLabError("Arrhenius fit needs at least three positive samples")
    inverse = 1.0 / temperature[mask]
    slope, intercept = np.polyfit(inverse, np.log(observable[mask]), 1)
    mode = params.get("mode", "resistance")
    activation = slope * K_B_EV if mode == "resistance" else -slope * K_B_EV
    prediction = np.exp(intercept + slope * inverse)
    total = np.log(observable[mask]) - np.mean(np.log(observable[mask]))
    r2 = 1.0 - float(np.sum((np.log(observable[mask]) - np.log(prediction)) ** 2) / np.sum(total**2)) if np.sum(total**2) else np.nan
    return result({"activation_energy_ev": float(activation), "prefactor": float(np.exp(intercept)), "fit": prediction, "r_squared": r2}, metadata={"kept_mask": mask, "mode": mode})


@algorithm(_spec(
    "thermal.variable_range_hopping", "thermal_activation", "Fit R=R0*exp[(T0/T)^p] for a specified hopping exponent.",
    ("temperature", "resistance"), ("t0", "r0", "fit", "r_squared"),
    object_schema({"exponent": number(0.25, exclusive_minimum=0.0), "tmin": number(exclusive_minimum=0.0), "tmax": number(exclusive_minimum=0.0)}),
    tags=("vrh", "hopping", "transport", "temperature"), assumptions=("The selected hopping exponent and one conduction channel apply in the fit interval.",), caveats=("Compare competing exponents and inspect residuals; linearity alone is not decisive.",),
))
def variable_range_hopping(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    temperature, resistance = paired_1d(payload, "temperature", "resistance")
    mask = (temperature > 0) & (resistance > 0)
    if "tmin" in params:
        mask &= temperature >= float(params["tmin"])
    if "tmax" in params:
        mask &= temperature <= float(params["tmax"])
    if mask.sum() < 3:
        raise SignalLabError("VRH fit needs at least three positive samples")
    exponent = float(params.get("exponent", 0.25))
    axis = temperature[mask] ** (-exponent)
    slope, intercept = np.polyfit(axis, np.log(resistance[mask]), 1)
    t0 = slope ** (1.0 / exponent) if slope > 0 else np.nan
    prediction = np.exp(intercept + slope * axis)
    total = np.log(resistance[mask]) - np.mean(np.log(resistance[mask]))
    r2 = 1.0 - float(np.sum((np.log(resistance[mask]) - np.log(prediction)) ** 2) / np.sum(total**2)) if np.sum(total**2) else np.nan
    return result({"t0": float(t0), "r0": float(np.exp(intercept)), "fit": prediction, "r_squared": r2}, metadata={"kept_mask": mask, "exponent": exponent})


@algorithm(_spec(
    "magnetism.curie_weiss", "magnetism", "Fit susceptibility to chi0 + C/(T-theta_CW).",
    ("temperature", "susceptibility"), ("chi0", "curie_constant", "theta_cw", "fit", "covariance"),
    tags=("curie-weiss", "susceptibility", "magnetism"), assumptions=("The selected temperature interval is in the paramagnetic Curie-Weiss regime.",), caveats=("Temperature-independent backgrounds and short-range correlations can bias theta_CW.",),
))
def curie_weiss(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    temperature, susceptibility = paired_1d(payload, "temperature", "susceptibility")
    def model(t: np.ndarray, chi0: float, c: float, theta: float) -> np.ndarray:
        return chi0 + c / (t - theta)
    initial = [float(np.min(susceptibility)), float(np.ptp(susceptibility) * np.ptp(temperature)), float(np.min(temperature) - 1.0)]
    upper_theta = float(np.min(temperature) - np.finfo(float).eps)
    fitted, covariance = optimize.curve_fit(model, temperature, susceptibility, p0=initial, bounds=([-np.inf, 0.0, -np.inf], [np.inf, np.inf, upper_theta]), maxfev=30000)
    return result({"chi0": float(fitted[0]), "curie_constant": float(fitted[1]), "theta_cw": float(fitted[2]), "fit": model(temperature, *fitted), "covariance": covariance})


@algorithm(_spec(
    "thermodynamics.debye_low_t", "thermodynamics", "Fit C/T=gamma+beta*T^2 and infer Debye temperature.",
    ("temperature", "heat_capacity"), ("gamma", "beta", "debye_temperature", "fit", "r_squared"),
    object_schema({"atoms_per_formula_unit": number(1.0, exclusive_minimum=0.0), "tmax": number(exclusive_minimum=0.0)}),
    tags=("heat-capacity", "debye", "sommerfeld", "low-temperature"), assumptions=("Heat capacity is molar in J mol^-1 K^-1 and low-T form C=gamma*T+beta*T^3 applies.",),
))
def debye_low_t(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    temperature, heat_capacity = paired_1d(payload, "temperature", "heat_capacity")
    mask = temperature > 0
    if "tmax" in params:
        mask &= temperature <= float(params["tmax"])
    if mask.sum() < 3:
        raise SignalLabError("Debye fit needs at least three positive-temperature samples")
    x = temperature[mask] ** 2
    y = heat_capacity[mask] / temperature[mask]
    beta, gamma = np.polyfit(x, y, 1)
    if beta <= 0:
        raise SignalLabError("fitted beta is nonpositive; Debye temperature is undefined")
    atoms = float(params.get("atoms_per_formula_unit", 1.0))
    theta = (12.0 * np.pi**4 * atoms * R_GAS / (5.0 * beta)) ** (1.0 / 3.0)
    prediction = gamma + beta * x
    total = y - np.mean(y)
    r2 = 1.0 - float(np.sum((y - prediction) ** 2) / np.sum(total**2)) if np.sum(total**2) else np.nan
    return result({"gamma": float(gamma), "beta": float(beta), "debye_temperature": float(theta), "fit": prediction, "r_squared": r2}, metadata={"kept_mask": mask})


@algorithm(_spec(
    "thermal.seebeck", "thermoelectric", "Fit thermovoltage versus temperature difference to obtain the Seebeck coefficient.",
    ("delta_temperature", "thermovoltage"), ("seebeck_coefficient", "offset_voltage", "fit", "r_squared"),
    tags=("seebeck", "thermoelectric", "linear-fit"), assumptions=("Contact/reference thermopower is corrected or intentionally included.",), caveats=("Temperature gradients, offsets, and lead contributions are common systematic errors.",),
))
def seebeck(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    dt, voltage = paired_1d(payload, "delta_temperature", "thermovoltage")
    slope, intercept = np.polyfit(dt, voltage, 1)
    prediction = slope * dt + intercept
    total = voltage - np.mean(voltage)
    r2 = 1.0 - float(np.sum((voltage - prediction) ** 2) / np.sum(total**2)) if np.sum(total**2) else np.nan
    return result({"seebeck_coefficient": float(-slope), "offset_voltage": float(intercept), "fit": prediction, "r_squared": r2})


@algorithm(_spec(
    "thermal.conductivity", "thermoelectric", "Compute thermal conductivity k=P*L/(A*DeltaT).",
    ("heat_flow", "delta_temperature"), ("thermal_conductivity",),
    object_schema({"length": number(exclusive_minimum=0.0), "cross_section_area": number(exclusive_minimum=0.0)}, required=("length", "cross_section_area")),
    tags=("thermal-conductivity", "steady-state", "geometry"), assumptions=("Steady one-dimensional heat flow and negligible parasitic losses.",),
))
def thermal_conductivity(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    heat_flow = np.asarray(payload["heat_flow"], dtype=float)
    delta_temperature = np.asarray(payload["delta_temperature"], dtype=float)
    if heat_flow.shape != delta_temperature.shape:
        raise SignalLabError("heat_flow and delta_temperature must have identical shapes")
    if np.any(delta_temperature == 0):
        raise SignalLabError("delta_temperature contains zero")
    return result({"thermal_conductivity": heat_flow * float(params["length"]) / (float(params["cross_section_area"]) * delta_temperature)})


@algorithm(_spec(
    "diffraction.bragg_d_spacing", "diffraction", "Convert diffraction peak 2theta to d-spacing with Bragg's law.",
    ("two_theta_degree",), ("d_spacing",),
    object_schema({"wavelength": number(exclusive_minimum=0.0), "order": integer(1, minimum=1)}, required=("wavelength",)),
    tags=("xrd", "bragg", "d-spacing"), assumptions=("two_theta is in degrees and wavelength/d-spacing use the same length unit.",),
))
def bragg_d_spacing(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    two_theta = np.asarray(payload["two_theta_degree"], dtype=float)
    theta = np.radians(two_theta / 2.0)
    if np.any(np.sin(theta) <= 0):
        raise SignalLabError("Bragg angle must be positive")
    return result({"d_spacing": int(params.get("order", 1)) * float(params["wavelength"]) / (2.0 * np.sin(theta))})


@algorithm(_spec(
    "diffraction.scherrer_size", "diffraction", "Estimate coherent domain size with the Scherrer equation.",
    ("two_theta_degree", "fwhm_degree"), ("domain_size", "corrected_fwhm_radian"),
    object_schema({"wavelength": number(exclusive_minimum=0.0), "shape_factor": number(0.9, exclusive_minimum=0.0), "instrument_fwhm_degree": number(0.0, minimum=0.0)}, required=("wavelength",)),
    tags=("xrd", "scherrer", "crystallite-size", "linewidth"), assumptions=("Peak broadening is dominated by finite coherent domain size after instrumental correction.",), caveats=("Microstrain, defects, anisotropy, and line-shape choice also broaden peaks; this is not particle size.",), references=(RIETVELD_REF,),
))
def scherrer_size(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    two_theta = np.asarray(payload["two_theta_degree"], dtype=float)
    measured = np.radians(np.asarray(payload["fwhm_degree"], dtype=float))
    instrumental = np.radians(float(params.get("instrument_fwhm_degree", 0.0)))
    corrected_squared = measured**2 - instrumental**2
    if np.any(corrected_squared <= 0):
        raise SignalLabError("instrument-corrected FWHM is nonpositive")
    corrected = np.sqrt(corrected_squared)
    theta = np.radians(two_theta / 2.0)
    size = float(params.get("shape_factor", 0.9)) * float(params["wavelength"]) / (corrected * np.cos(theta))
    return result({"domain_size": size, "corrected_fwhm_radian": corrected})


@algorithm(_spec(
    "photoemission.shirley_baseline", "photoemission", "Iterative Shirley inelastic background between spectrum endpoints.",
    ("binding_energy", "intensity"), ("baseline", "corrected", "converged", "iterations"),
    object_schema({"endpoint_points": integer(5, minimum=1), "max_iterations": integer(200, minimum=1), "tolerance": number(1e-8, exclusive_minimum=0.0)}),
    tags=("xps", "shirley", "background", "photoemission"), assumptions=("Binding energy is increasing and endpoints represent background levels.",), caveats=("Shirley background is empirical and fit-window dependent; Tougaard-type models may be more physical.",), references=(SHIRLEY_REF,),
))
def shirley_baseline(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    energy, intensity = paired_1d(payload, "binding_energy", "intensity")
    order = np.argsort(energy)
    energy, intensity = energy[order], intensity[order]
    require_strictly_increasing(energy, "binding_energy")
    points = min(int(params.get("endpoint_points", 5)), max(1, energy.size // 3))
    left, right = float(np.mean(intensity[:points])), float(np.mean(intensity[-points:]))
    baseline = np.linspace(left, right, energy.size)
    converged = False
    max_iterations = int(params.get("max_iterations", 200))
    tolerance = float(params.get("tolerance", 1e-8))
    for iteration in range(1, max_iterations + 1):
        residual = intensity - baseline
        segment = 0.5 * (residual[:-1] + residual[1:]) * np.diff(energy)
        integral_to_right = np.concatenate((np.cumsum(segment[::-1])[::-1], [0.0]))
        total = integral_to_right[0]
        if abs(total) < np.finfo(float).eps:
            raise SignalLabError("Shirley residual integral is zero")
        updated = right + (left - right) * integral_to_right / total
        if np.max(np.abs(updated - baseline)) <= tolerance * max(1.0, np.max(np.abs(baseline))):
            baseline = updated
            converged = True
            break
        baseline = updated
    inverse = np.argsort(order)
    warnings = [] if converged else ["Shirley baseline did not converge within max_iterations"]
    return result({"baseline": baseline[inverse], "corrected": (intensity - baseline)[inverse], "converged": converged, "iterations": iteration}, warnings=warnings)


@algorithm(_spec(
    "quantum_oscillation.prepare_inverse_field", "quantum_oscillation", "Select a same-sign field window, subtract polynomial background, and resample oscillations uniformly in 1/B.",
    ("field", "signal"), ("inverse_field", "oscillation", "background", "field_sorted"),
    object_schema({"min_abs_field": number(exclusive_minimum=0.0), "max_abs_field": number(exclusive_minimum=0.0), "background_degree": integer(3, minimum=0, maximum=12), "points": integer(minimum=16)}, required=("min_abs_field",)),
    tags=("sdh", "dHvA", "inverse-field", "background"), assumptions=("Use one field polarity and a monotonic field segment.",), caveats=("Background order and field window can shift FFT amplitudes and apparent frequencies.",), references=(LK_REF,),
))
def prepare_inverse_field(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    field, values = paired_1d(payload, "field", "signal")
    lower = float(params["min_abs_field"])
    upper = float(params.get("max_abs_field", np.inf))
    positive_count = np.sum((field >= lower) & (field <= upper))
    negative_count = np.sum((-field >= lower) & (-field <= upper))
    sign = 1.0 if positive_count >= negative_count else -1.0
    selected_field = sign * field
    mask = (selected_field >= lower) & (selected_field <= upper)
    if mask.sum() < 16:
        raise SignalLabError("selected field window needs at least 16 samples")
    selected_field, selected_values = selected_field[mask], values[mask]
    order = np.argsort(selected_field)
    selected_field, selected_values = selected_field[order], selected_values[order]
    degree = int(params.get("background_degree", 3))
    coefficients = np.polyfit(selected_field, selected_values, degree)
    background = np.polyval(coefficients, selected_field)
    oscillation = selected_values - background
    inverse = 1.0 / selected_field
    order_inverse = np.argsort(inverse)
    inverse, oscillation = inverse[order_inverse], oscillation[order_inverse]
    grid = np.linspace(inverse[0], inverse[-1], int(params.get("points", inverse.size)))
    return result({"inverse_field": grid, "oscillation": np.interp(grid, inverse, oscillation), "background": background, "field_sorted": selected_field}, metadata={"field_sign": sign, "background_coefficients": coefficients})


@algorithm(_spec(
    "quantum_oscillation.fft", "quantum_oscillation", "FFT an oscillatory trace uniformly sampled in inverse field.",
    ("inverse_field", "oscillation"), ("frequency_t", "amplitude", "phase"),
    object_schema({"window": choice("hann", ("hann", "hamming", "blackman", "none")), "zero_padding_factor": integer(4, minimum=1, maximum=64)}),
    tags=("sdh", "dHvA", "fft", "onsager-frequency"), assumptions=("inverse_field is uniformly sampled in T^-1.",), caveats=("Peak width reflects finite 1/B window and window function, not only intrinsic frequency spread.",), references=(LK_REF,),
))
def quantum_oscillation_fft(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    inverse, oscillation = paired_1d(payload, "inverse_field", "oscillation")
    step = require_uniform_spacing(inverse, "inverse_field")
    window_name = params.get("window", "hann")
    window = np.ones(oscillation.size) if window_name == "none" else signal.get_window(window_name, oscillation.size)
    nfft = int(2 ** np.ceil(np.log2(oscillation.size * int(params.get("zero_padding_factor", 4)))))
    transformed = np.fft.rfft((oscillation - np.mean(oscillation)) * window, n=nfft)
    return result({"frequency_t": np.fft.rfftfreq(nfft, d=step), "amplitude": 2.0 * np.abs(transformed) / np.sum(window), "phase": np.angle(transformed)}, metadata={"window": window_name, "nfft": nfft})


@algorithm(_spec(
    "quantum_oscillation.landau_fan", "quantum_oscillation", "Fit Landau index versus inverse field to obtain oscillation frequency and intercept.",
    ("field_extrema", "landau_index"), ("frequency_t", "intercept", "fit", "r_squared"),
    tags=("landau-fan", "berry-phase", "quantum-oscillation"), assumptions=("Extrema are assigned a consistent Landau-index convention.",), caveats=("Berry-phase inference also depends on dimensional phase shifts, Zeeman splitting, and index convention.",), references=(LK_REF,),
))
def landau_fan(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    field, index = paired_1d(payload, "field_extrema", "landau_index")
    if np.any(field == 0):
        raise SignalLabError("field_extrema contains zero")
    inverse = 1.0 / np.abs(field)
    frequency, intercept = np.polyfit(inverse, index, 1)
    prediction = frequency * inverse + intercept
    total = index - np.mean(index)
    r2 = 1.0 - float(np.sum((index - prediction) ** 2) / np.sum(total**2)) if np.sum(total**2) else np.nan
    return result({"frequency_t": float(frequency), "intercept": float(intercept), "fit": prediction, "r_squared": r2})


@algorithm(_spec(
    "quantum_oscillation.lk_mass", "quantum_oscillation", "Fit Lifshitz-Kosevich thermal damping X/sinh(X) to obtain cyclotron mass.",
    ("temperature", "amplitude"), ("mass_me", "scale", "fit", "covariance"),
    object_schema({"effective_field_t": number(exclusive_minimum=0.0)}, required=("effective_field_t",)),
    tags=("lifshitz-kosevich", "effective-mass", "quantum-oscillation"), assumptions=("Amplitude is extracted consistently at one orbit and represented by an effective field.",), caveats=("Field-window averaging, spin zeros, beatings, and temperature-dependent scattering can bias mass.",), references=(LK_REF,),
))
def lk_mass(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    temperature, amplitude = paired_1d(payload, "temperature", "amplitude")
    field = float(params["effective_field_t"])
    def model(t: np.ndarray, scale: float, mass_me: float) -> np.ndarray:
        x = 2.0 * np.pi**2 * K_B * (mass_me * M_E) * t / (HBAR * E_CHARGE * field)
        return scale * np.divide(x, np.sinh(x), out=np.ones_like(x), where=x != 0)
    fitted, covariance = optimize.curve_fit(model, temperature, amplitude, p0=[float(np.max(amplitude)), 1.0], bounds=([0.0, 1e-4], [np.inf, 1000.0]), maxfev=20000)
    return result({"mass_me": float(fitted[1]), "scale": float(fitted[0]), "fit": model(temperature, *fitted), "covariance": covariance})


@algorithm(_spec(
    "quantum_oscillation.dingle", "quantum_oscillation", "Fit field damping after LK thermal correction to obtain Dingle temperature and quantum lifetime.",
    ("field", "amplitude"), ("dingle_temperature_k", "quantum_lifetime_s", "fit", "r_squared"),
    object_schema({"temperature_k": number(minimum=0.0), "mass_me": number(exclusive_minimum=0.0)}, required=("temperature_k", "mass_me")),
    tags=("dingle", "quantum-lifetime", "quantum-oscillation"), assumptions=("One orbit dominates and other field-dependent prefactors are corrected or negligible.",), caveats=("Background removal, field-window FFT amplitudes, and unresolved beats can strongly bias Dingle plots.",), references=(LK_REF,),
))
def dingle(payload: Mapping[str, Any], params: Mapping[str, Any]) -> AlgorithmResult:
    field, amplitude = paired_1d(payload, "field", "amplitude")
    mask = (field > 0) & (amplitude > 0)
    if mask.sum() < 3:
        raise SignalLabError("Dingle fit needs at least three positive field/amplitude samples")
    mass = float(params["mass_me"]) * M_E
    temperature = float(params["temperature_k"])
    x = 2.0 * np.pi**2 * K_B * mass * temperature / (HBAR * E_CHARGE * field[mask])
    rt = np.divide(x, np.sinh(x), out=np.ones_like(x), where=x != 0)
    inverse = 1.0 / field[mask]
    corrected_log = np.log(amplitude[mask] / rt)
    slope, intercept = np.polyfit(inverse, corrected_log, 1)
    dingle_temperature = -slope * HBAR * E_CHARGE / (2.0 * np.pi**2 * K_B * mass)
    lifetime = HBAR / (2.0 * np.pi * K_B * dingle_temperature) if dingle_temperature > 0 else np.nan
    prediction = intercept + slope * inverse
    total = corrected_log - np.mean(corrected_log)
    r2 = 1.0 - float(np.sum((corrected_log - prediction) ** 2) / np.sum(total**2)) if np.sum(total**2) else np.nan
    return result({"dingle_temperature_k": float(dingle_temperature), "quantum_lifetime_s": float(lifetime), "fit": prediction, "r_squared": r2}, metadata={"kept_mask": mask})
