import json
import unittest

from ai_theory_lab.fixed_lagrangian_resampling import (
    DEFAULT_MANIFEST,
    _representatives,
    _sample_sd,
    _seed_for_replicate,
)


class FixedLagrangianResamplingTests(unittest.TestCase):
    def test_manifest_has_seven_unique_non_sonnet_representatives(self):
        manifest = json.loads(DEFAULT_MANIFEST.read_text(encoding="utf-8"))
        reps = _representatives(manifest)
        self.assertEqual(len(reps), 7)
        self.assertEqual(len({rep["proposal"] for rep in reps}), 7)
        self.assertNotIn("Claude Sonnet 5", {rep["agent"] for rep in reps})
        self.assertTrue(all(rep["headline_k"] == 5 for rep in reps))

    def test_replicate_seed_is_reproducible_and_changes(self):
        self.assertEqual(_seed_for_replicate(1), _seed_for_replicate(1))
        self.assertNotEqual(_seed_for_replicate(1), _seed_for_replicate(2))
        with self.assertRaises(ValueError):
            _seed_for_replicate(0)

    def test_sample_sd_uses_sample_standard_deviation(self):
        self.assertEqual(_sample_sd([1.0]), 0.0)
        self.assertAlmostEqual(_sample_sd([1.0, 3.0]), 2.0**0.5)


if __name__ == "__main__":
    unittest.main()
