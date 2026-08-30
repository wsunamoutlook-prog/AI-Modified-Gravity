from __future__ import annotations

import math
import unittest

import numpy as np

import signal_lab
from signal_lab.agent_api import execute, execute_pipeline, inspect, search, tool_manifest
from signal_lab.validation import SignalLabError


class SignalLabCatalogTests(unittest.TestCase):
    def test_catalog_is_large_unique_and_machine_readable(self) -> None:
        catalog = signal_lab.list_algorithms()
        names = [item["name"] for item in catalog]
        self.assertGreaterEqual(len(catalog), 110)
        self.assertEqual(len(names), len(set(names)))
        self.assertEqual(set(item["domain"] for item in catalog), {
            "general",
            "optics",
            "condensed_matter",
        })
        for item in catalog:
            self.assertIn("type", item["parameter_schema"])
            self.assertTrue(item["required_inputs"])
            self.assertTrue(item["outputs"])

    def test_search_inspect_and_manifest(self) -> None:
        matches = search("carrier-density", domain="condensed_matter")
        self.assertIn("transport.hall_linear", {item["name"] for item in matches})
        spec = inspect("spectrum.welch_psd")
        self.assertEqual(spec["parameter_schema"]["properties"]["segment_length"]["type"], "integer")
        self.assertEqual(tool_manifest()["algorithm_count"], len(signal_lab.list_algorithms()))

    def test_parameter_schema_rejects_unknown_keys(self) -> None:
        time = np.linspace(0.0, 1.0, 128, endpoint=False)
        with self.assertRaises(SignalLabError):
            execute("spectrum.welch_psd", {"time": time, "y": np.sin(time)}, {"nperseg": 64})


class GeneralSignalTests(unittest.TestCase):
    def test_fft_recovers_tone_amplitude_frequency_and_phase(self) -> None:
        sample_rate = 1024.0
        time = np.arange(2048) / sample_rate
        amplitude = 2.5
        phase = 0.37
        values = amplitude * np.cos(2.0 * np.pi * 64.0 * time + phase)
        output = execute(
            "spectrum.fft",
            {"time": time, "y": values},
            {"window": "none", "detrend": "constant"},
        ).values
        peak = int(np.argmax(output["amplitude"][1:]) + 1)
        self.assertAlmostEqual(float(output["frequency"][peak]), 64.0, places=10)
        self.assertAlmostEqual(float(output["amplitude"][peak]), amplitude, places=10)
        self.assertAlmostEqual(float(output["phase"][peak]), phase, places=10)

    def test_welch_psd_recovers_tone(self) -> None:
        sample_rate = 1000.0
        time = np.arange(4096) / sample_rate
        values = np.sin(2.0 * np.pi * 125.0 * time)
        output = execute(
            "spectrum.welch_psd",
            {"time": time, "y": values},
            {"segment_length": 1000, "overlap_fraction": 0.5},
        ).values
        peak = int(np.argmax(output["psd"][1:]) + 1)
        self.assertAlmostEqual(float(output["frequency"][peak]), 125.0, places=8)

    def test_lockin_recovers_amplitude_and_phase(self) -> None:
        sample_rate = 2000.0
        time = np.arange(8000) / sample_rate
        amplitude = 1.7
        phase = -0.42
        values = amplitude * np.cos(2.0 * np.pi * 83.0 * time + phase)
        output = execute(
            "lockin.demodulate",
            {"time": time, "signal": values},
            {
                "reference_frequency": 83.0,
                "lowpass_cutoff": 5.0,
                "filter_order": 4,
                "amplitude_convention": "peak",
            },
        ).values
        interior = slice(1000, -1000)
        self.assertAlmostEqual(float(np.median(output["amplitude"][interior])), amplitude, places=4)
        self.assertAlmostEqual(float(np.median(output["phase"][interior])), phase, places=4)

    def test_gaussian_peak_fit(self) -> None:
        x = np.linspace(-5.0, 5.0, 501)
        y = 0.2 + 3.0 * np.exp(-0.5 * ((x - 0.7) / 0.8) ** 2)
        output = execute("peaks.fit_single", {"x": x, "y": y}, {"model": "gaussian"}).values
        parameters = output["parameters"]
        self.assertAlmostEqual(float(parameters["amplitude"]), 3.0, places=7)
        self.assertAlmostEqual(float(parameters["center"]), 0.7, places=7)
        self.assertAlmostEqual(float(parameters["sigma"]), 0.8, places=7)

    def test_asls_separates_smooth_baseline(self) -> None:
        x = np.linspace(0.0, 100.0, 501)
        baseline = 0.01 * x + 1.0
        y = baseline + 8.0 * np.exp(-0.5 * ((x - 50.0) / 1.2) ** 2)
        output = execute(
            "baseline.asls",
            {"y": y},
            {"lambda": 1e7, "asymmetry": 0.001},
        ).values
        edge_error = np.mean(np.abs(output["baseline"][[0, 1, -2, -1]] - baseline[[0, 1, -2, -1]]))
        self.assertLess(edge_error, 0.15)
        self.assertGreater(float(np.max(output["corrected"])), 7.0)


class OpticsTests(unittest.TestCase):
    def test_absorbance_and_absorption_coefficient(self) -> None:
        absorbance = execute(
            "optics.transmittance_to_absorbance",
            {"transmittance": np.array([1.0, 0.1])},
        ).values["absorbance"]
        self.assertTrue(np.allclose(absorbance, [0.0, 1.0]))
        alpha = execute(
            "optics.absorbance_to_absorption_coefficient",
            {"absorbance": np.array([1.0])},
            {"thickness": 0.01},
        ).values["absorption_coefficient"]
        self.assertAlmostEqual(float(alpha[0]), 100.0 * math.log(10.0), places=10)

    def test_tauc_gap_from_linear_edge(self) -> None:
        energy = np.linspace(1.2, 2.8, 300)
        gap = 1.73
        tauc = 4.2 * (energy - gap)
        output = execute(
            "optics.tauc_linear_gap",
            {"energy_ev": energy, "tauc_y": tauc},
            {"emin": 1.8, "emax": 2.6},
        ).values
        self.assertAlmostEqual(float(output["bandgap_ev"]), gap, places=12)
        self.assertAlmostEqual(float(output["r_squared"]), 1.0, places=12)

    def test_stokes_reconstruction(self) -> None:
        output = execute(
            "optics.stokes_from_analyzers",
            {
                "i0": np.array([8.0]),
                "i45": np.array([7.0]),
                "i90": np.array([2.0]),
                "i135": np.array([3.0]),
                "ircp": np.array([6.0]),
                "ilcp": np.array([4.0]),
            },
        ).values
        self.assertTrue(np.allclose([output["s0"][0], output["s1"][0], output["s2"][0], output["s3"][0]], [10.0, 6.0, 4.0, 2.0]))

    def test_spot_moments_recovers_gaussian_center_and_width(self) -> None:
        yy, xx = np.indices((101, 121))
        image = np.exp(-0.5 * (((xx - 62.0) / 7.0) ** 2 + ((yy - 44.0) / 3.0) ** 2))
        output = execute("optics.spot_moments", {"image": image}).values
        self.assertAlmostEqual(float(output["centroid_x"]), 62.0, places=5)
        self.assertAlmostEqual(float(output["centroid_y"]), 44.0, places=5)
        self.assertAlmostEqual(float(output["sigma_major"]), 7.0, places=4)
        self.assertAlmostEqual(float(output["sigma_minor"]), 3.0, places=4)

    def test_thz_transfer_function_recovers_complex_ratio(self) -> None:
        time = np.arange(1024, dtype=float) * 1e-13
        reference = np.exp(-0.5 * ((time - 4e-11) / 2e-12) ** 2)
        sample = 0.4 * reference
        output = execute(
            "optics.thz_transfer_function",
            {"time": time, "sample": sample, "reference": reference},
            {"window": "none", "epsilon": 1e-8},
        ).values
        self.assertTrue(np.allclose(output["amplitude"][output["valid_mask"]], 0.4, atol=1e-10))

    def test_ellipsometry_ratio(self) -> None:
        output = execute(
            "optics.ellipsometry_rho",
            {"psi": np.array([45.0]), "delta": np.array([90.0])},
        ).values
        self.assertAlmostEqual(float(output["rho_real"][0]), 0.0, places=12)
        self.assertAlmostEqual(float(output["rho_imag"][0]), 1.0, places=12)


class CondensedMatterTests(unittest.TestCase):
    def test_field_even_odd_decomposition(self) -> None:
        field = np.linspace(-5.0, 5.0, 101)
        values = field**2 + 3.0 * field
        output = execute("transport.field_even_odd", {"field": field, "signal": values}, {"points": 51}).values
        b = output["field_abs"]
        self.assertTrue(np.allclose(output["even"], b**2, atol=1e-12))
        self.assertTrue(np.allclose(output["odd"], 3.0 * b, atol=1e-12))

    def test_van_der_pauw_equal_resistances(self) -> None:
        output = execute(
            "transport.van_der_pauw",
            {"resistance_a": 100.0, "resistance_b": 100.0},
            {"thickness": 2e-6},
        ).values
        expected = math.pi * 100.0 / math.log(2.0)
        self.assertAlmostEqual(float(output["sheet_resistance"]), expected, places=8)
        self.assertAlmostEqual(float(output["resistivity"]), expected * 2e-6, places=14)

    def test_hall_density(self) -> None:
        field = np.linspace(-9.0, 9.0, 101)
        slope = -12.5
        output = execute(
            "transport.hall_linear",
            {"field": field, "hall_resistance": slope * field + 0.03},
            {"thickness": 8e-9},
        ).values
        expected_sheet = 1.0 / (1.602176634e-19 * abs(slope))
        self.assertAlmostEqual(float(output["hall_slope"]), slope, places=10)
        self.assertAlmostEqual(float(output["sheet_density_m2"]), expected_sheet, delta=expected_sheet * 1e-12)
        self.assertEqual(output["carrier_sign"], -1)

    def test_arrhenius_activation_energy(self) -> None:
        temperature = np.linspace(100.0, 350.0, 100)
        activation = 0.082
        prefactor = 3.5
        observable = prefactor * np.exp(activation / (8.617333262145e-5 * temperature))
        output = execute(
            "thermal.arrhenius",
            {"temperature": temperature, "observable": observable},
            {"mode": "resistance"},
        ).values
        self.assertAlmostEqual(float(output["activation_energy_ev"]), activation, places=12)
        self.assertAlmostEqual(float(output["prefactor"]), prefactor, places=10)

    def test_debye_fit(self) -> None:
        temperature = np.linspace(0.5, 8.0, 100)
        gamma = 0.012
        beta = 2.4e-4
        heat_capacity = gamma * temperature + beta * temperature**3
        output = execute(
            "thermodynamics.debye_low_t",
            {"temperature": temperature, "heat_capacity": heat_capacity},
            {"atoms_per_formula_unit": 2.0, "tmax": 8.0},
        ).values
        expected_theta = (12.0 * math.pi**4 * 2.0 * 8.31446261815324 / (5.0 * beta)) ** (1.0 / 3.0)
        self.assertAlmostEqual(float(output["gamma"]), gamma, places=12)
        self.assertAlmostEqual(float(output["beta"]), beta, places=12)
        self.assertAlmostEqual(float(output["debye_temperature"]), expected_theta, places=9)

    def test_quantum_oscillation_frequency(self) -> None:
        inverse_field = np.linspace(0.05, 0.25, 1024)
        oscillation = np.cos(2.0 * np.pi * 235.0 * inverse_field + 0.2)
        output = execute(
            "quantum_oscillation.fft",
            {"inverse_field": inverse_field, "oscillation": oscillation},
            {"window": "hann", "zero_padding_factor": 8},
        ).values
        peak = int(np.argmax(output["amplitude"][1:]) + 1)
        self.assertAlmostEqual(float(output["frequency_t"][peak]), 235.0, delta=0.8)

    def test_lifshitz_kosevich_mass(self) -> None:
        temperature = np.linspace(0.4, 18.0, 80)
        field = 12.0
        mass_me = 0.42
        alpha = 2.0 * math.pi**2 * 1.380649e-23 * (mass_me * 9.1093837139e-31) / (1.054571817e-34 * 1.602176634e-19 * field)
        x = alpha * temperature
        amplitude = 2.3 * x / np.sinh(x)
        output = execute(
            "quantum_oscillation.lk_mass",
            {"temperature": temperature, "amplitude": amplitude},
            {"effective_field_t": field},
        ).values
        self.assertAlmostEqual(float(output["mass_me"]), mass_me, places=7)
        self.assertAlmostEqual(float(output["scale"]), 2.3, places=7)

    def test_resistive_transition_interpolates_descending_resistance(self) -> None:
        temperature = np.linspace(2.0, 12.0, 101)
        resistance = 10.0 / (1.0 + np.exp(-(temperature - 7.0) / 0.08))
        output = execute(
            "transition.resistive_tc",
            {"temperature": temperature, "resistance": resistance},
            {"fraction": 0.5, "normal_high_fraction": 0.1},
        ).values
        self.assertAlmostEqual(float(output["tc"]), 7.0, delta=0.03)

    def test_two_carrier_fit_recovers_synthetic_transport(self) -> None:
        field = np.linspace(-5.0, 5.0, 121)
        ne, nh, mue, muh = 2.5e25, 7.0e24, 0.12, 0.045
        electron = 1.0 + (mue * field) ** 2
        hole = 1.0 + (muh * field) ** 2
        sigma_xx = 1.602176634e-19 * (ne * mue / electron + nh * muh / hole)
        sigma_xy = 1.602176634e-19 * field * (-ne * mue**2 / electron + nh * muh**2 / hole)
        denominator = sigma_xx**2 + sigma_xy**2
        output = execute(
            "transport.two_carrier_fit",
            {
                "field": field,
                "rho_xx": sigma_xx / denominator,
                "rho_xy": -sigma_xy / denominator,
            },
            {
                "initial_electron_density_m3": ne * 1.1,
                "initial_hole_density_m3": nh * 0.9,
                "initial_electron_mobility_m2_per_vs": mue * 0.9,
                "initial_hole_mobility_m2_per_vs": muh * 1.1,
            },
        ).values
        self.assertAlmostEqual(float(output["electron_density_m3"]) / ne, 1.0, places=5)
        self.assertAlmostEqual(float(output["hole_density_m3"]) / nh, 1.0, places=5)
        self.assertAlmostEqual(float(output["electron_mobility_m2_per_vs"]) / mue, 1.0, places=5)
        self.assertAlmostEqual(float(output["hole_mobility_m2_per_vs"]) / muh, 1.0, places=5)

    def test_hln_fit_recovers_phase_coherence(self) -> None:
        field = np.r_[np.linspace(-0.4, -0.005, 100), np.linspace(0.005, 0.4, 100)]
        alpha, length = -0.62, 1.8e-7
        e, hbar = 1.602176634e-19, 1.054571817e-34
        bphi = hbar / (4.0 * e * length**2)
        ratio = bphi / np.abs(field)
        from scipy import special
        conductivity = alpha * e**2 / (2.0 * np.pi**2 * hbar) * (
            special.digamma(0.5 + ratio) - np.log(ratio)
        )
        output = execute(
            "quantum_transport.hln_fit",
            {"field": field, "delta_conductivity": conductivity},
            {"initial_alpha": -0.5, "initial_phase_coherence_length_m": 1.5e-7},
        ).values
        self.assertAlmostEqual(float(output["alpha"]), alpha, places=5)
        self.assertAlmostEqual(float(output["phase_coherence_length_m"]) / length, 1.0, places=5)

    def test_gl_upper_critical_field(self) -> None:
        temperature = np.linspace(1.0, 8.0, 80)
        hc20, tc = 13.5, 9.2
        reduced = temperature / tc
        field = hc20 * (1.0 - reduced**2) / (1.0 + reduced**2)
        output = execute(
            "superconductivity.hc2_gl",
            {"temperature": temperature, "critical_field": field},
        ).values
        self.assertAlmostEqual(float(output["hc2_zero"]), hc20, places=7)
        self.assertAlmostEqual(float(output["tc"]), tc, places=7)

    def test_randles_fit_and_dielectric_conversion(self) -> None:
        frequency = np.logspace(1.0, 6.0, 150)
        rs, rct, capacitance = 8.0, 120.0, 2.5e-6
        impedance = rs + rct / (1.0 + 1j * 2.0 * np.pi * frequency * rct * capacitance)
        fitted = execute(
            "impedance.randles_fit",
            {"frequency_hz": frequency, "z_real": impedance.real, "z_imag": impedance.imag},
        ).values
        self.assertAlmostEqual(float(fitted["series_resistance"]), rs, delta=2e-6)
        self.assertAlmostEqual(float(fitted["charge_transfer_resistance"]), rct, delta=2e-6)
        self.assertAlmostEqual(float(fitted["double_layer_capacitance_f"]), capacitance, delta=2e-12)

        empty_cell = 1e-12
        epsilon = 12.0 - 0.7j
        capacitor_impedance = 1.0 / (1j * 2.0 * np.pi * frequency * empty_cell * epsilon)
        dielectric = execute(
            "dielectric.permittivity_from_impedance",
            {
                "frequency_hz": frequency,
                "z_real": capacitor_impedance.real,
                "z_imag": capacitor_impedance.imag,
            },
            {"empty_cell_capacitance_f": empty_cell},
        ).values
        self.assertTrue(np.allclose(dielectric["epsilon_real"], 12.0))
        self.assertTrue(np.allclose(dielectric["epsilon_loss"], 0.7))

    def test_diffraction_and_entropy_atoms(self) -> None:
        lattice = execute(
            "diffraction.lattice_parameter_cubic",
            {"d_spacing": np.array([2.0]), "h": np.array([1]), "k": np.array([1]), "l": np.array([0])},
        ).values["lattice_parameter"]
        self.assertAlmostEqual(float(lattice[0]), 2.0 * math.sqrt(2.0), places=12)

        temperature = np.linspace(1.0, 10.0, 100)
        entropy = execute(
            "thermodynamics.entropy",
            {"temperature": temperature, "heat_capacity": 3.0 * temperature},
        ).values["entropy_change"]
        self.assertAlmostEqual(float(entropy[-1]), 27.0, places=12)


class PipelineTests(unittest.TestCase):
    def test_declarative_pipeline_maps_state_and_records_provenance(self) -> None:
        x = np.array([2.0, np.nan, 1.0, 3.0])
        y = np.array([20.0, 99.0, 10.0, 30.0])
        output = execute_pipeline(
            {"raw_x": x, "raw_y": y},
            [
                {
                    "algorithm": "preprocess.drop_nonfinite",
                    "inputs": {"x": "raw_x", "y": "raw_y"},
                    "outputs": {"x": "clean_x", "y": "clean_y"},
                },
                {
                    "algorithm": "preprocess.sort_axis",
                    "inputs": {"x": "clean_x", "y": "clean_y"},
                    "outputs": {"x": "sorted_x", "y": "sorted_y"},
                },
            ],
        )
        self.assertTrue(np.array_equal(output.state["sorted_x"], [1.0, 2.0, 3.0]))
        self.assertTrue(np.array_equal(output.state["sorted_y"], [10.0, 20.0, 30.0]))
        self.assertEqual([step["algorithm"] for step in output.history], [
            "preprocess.drop_nonfinite",
            "preprocess.sort_axis",
        ])
        self.assertEqual(output.history[0]["metadata"]["algorithm"], "preprocess.drop_nonfinite")


if __name__ == "__main__":
    unittest.main()
