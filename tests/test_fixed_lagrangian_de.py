import unittest

from ai_theory_lab.fixed_lagrangian_de import (
    ParameterSpec,
    _replicate_seed,
    _sample_from_unit,
    task_index_to_selection,
)


class FixedLagrangianDifferentialEvolutionTests(unittest.TestCase):
    def test_parameter_transforms(self):
        linear = ParameterSpec("x", "linear", 2.0, 6.0)
        logarithmic = ParameterSpec("y", "log10", 1.0e-2, 1.0e2)
        signed = ParameterSpec("z", "signed_log10", 1.0e-3, 1.0e1)
        self.assertAlmostEqual(linear.from_unit(0.25), 3.0)
        self.assertAlmostEqual(logarithmic.from_unit(0.5), 1.0)
        self.assertLess(signed.from_unit(0.25), 0.0)
        self.assertGreater(signed.from_unit(0.75), 0.0)

    def test_complete_sample_overwrites_only_active_parameters(self):
        specs = [ParameterSpec("Omega_m0", "linear", 0.2, 0.4)]
        sample = _sample_from_unit([0.5], specs, {"Omega_m0": 0.25, "H0_km_s_Mpc": 66.0})
        self.assertAlmostEqual(sample["Omega_m0"], 0.3)
        self.assertEqual(sample["H0_km_s_Mpc"], 66.0)

    def test_array_task_mapping_covers_seven_by_twenty(self):
        proposals = ["G263", "O769", "F456", "Gm986", "Q88", "D820", "K301"]
        self.assertEqual(task_index_to_selection(1, proposals), ("G263", 1))
        self.assertEqual(task_index_to_selection(7, proposals), ("K301", 1))
        self.assertEqual(task_index_to_selection(8, proposals), ("G263", 2))
        self.assertEqual(task_index_to_selection(140, proposals), ("K301", 20))
        with self.assertRaises(ValueError):
            task_index_to_selection(141, proposals)

    def test_seed_is_reproducible_and_agent_specific(self):
        self.assertEqual(_replicate_seed("K301", 1), _replicate_seed("K301", 1))
        self.assertNotEqual(_replicate_seed("K301", 1), _replicate_seed("K301", 2))
        self.assertNotEqual(_replicate_seed("K301", 1), _replicate_seed("G263", 1))


if __name__ == "__main__":
    unittest.main()
