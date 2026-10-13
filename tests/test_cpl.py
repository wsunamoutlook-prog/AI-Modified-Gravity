"""Likelihood checks at fixed parameters; no optimizer or LLM search."""
import unittest
import numpy as np
from ai_theory_lab.fit_cpl import Fit, hubble


class CPLTests(unittest.TestCase):
    def test_lcdm_limit(self):
        z = np.linspace(0, 3, 100)
        np.testing.assert_allclose(hubble(z, (.306, -1, 0)), np.sqrt(.306 * (1+z)**3 + .694))

    def test_observed_likelihood_quadrature_and_profiled_scale(self):
        fit = Fit()
        self.assertEqual(fit.n, 1833)
        theta = (.31416, -.84344, -.53571)
        chi2 = fit.exact(theta)["chi2"]
        self.assertLess(abs(chi2 - fit.exact(theta, order=16)["chi2"]), 1e-7)
        self.assertLess(abs(chi2 - fit.grid(theta, 24000)["chi2"]), .001)
        self.assertLess(abs(chi2 - fit.exact(theta, H0=58)["chi2"]), 1e-7)
        self.assertLess(chi2, fit.exact((.306, -1, 0))["chi2"])

if __name__ == "__main__":
    unittest.main()
