from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

import numpy as np
from scipy.linalg import cho_factor, cho_solve

from ai_theory_lab.lcdm_mock import (
    BAO_COV, BAO_TABLE, SN_COV, SN_TABLE, DATASET_KIND,
    _validate_destination, bao_shape_from_grid, gaussian_noise, generate_mock,
    sha256_file, write_bao_mock_table, write_sn_mock_table,
)
from solver_v5_2.likelihood import (
    chi2_des_sn_from_grid, chi2_desi_bao_from_grid,
    load_des_sn, load_desi_dr2_bao, mu_model_from_h_grid,
)


class LCDMMockTests(unittest.TestCase):
    def test_precision_transform_has_inverse_covariance_and_correct_whitening(self):
        precision = np.array([[4.0, 1.2, -0.5], [1.2, 2.5, 0.8], [-0.5, 0.8, 3.0]])
        transform = gaussian_noise(precision, np.eye(3), precision=True)
        np.testing.assert_allclose(transform @ transform.T, np.linalg.inv(precision), atol=1e-15)
        z = np.array([0.4, -1.3, 2.1])
        noise = gaussian_noise(precision, z, precision=True)
        self.assertAlmostEqual(float(noise @ precision @ noise), float(z @ z), places=13)
        np.testing.assert_allclose(np.linalg.cholesky(precision).T @ noise, z, atol=1e-15)
        wrong_transform = np.linalg.solve(np.linalg.cholesky(precision), np.eye(3))
        self.assertGreater(np.max(np.abs(wrong_transform @ wrong_transform.T - np.linalg.inv(precision))), 0.01)

    def test_covariance_transform_preserves_correlations(self):
        covariance = np.array([[0.5, -0.12, 0.07], [-0.12, 0.3, 0.09], [0.07, 0.09, 0.4]])
        transform = gaussian_noise(covariance, np.eye(3), precision=False)
        np.testing.assert_allclose(transform @ transform.T, covariance, atol=1e-15)
        with self.assertRaises(ValueError):
            gaussian_noise(np.array([[1.0, 0.2], [0.8, 1.0]]), np.ones(2), precision=False)

    def test_bao_shape_matches_existing_likelihood_profile(self):
        z_grid = np.linspace(0, 2.5025, 3000)
        h_grid = np.sqrt(0.337 * (1 + z_grid) ** 3 + 1 - 0.337)
        covariance = np.diag([0.05, 0.04, 0.2, 0.15]) + 0.03 * np.ones((4, 4))
        bao = {"z": np.array([0.2, 0.5, 0.8, 1.7]),
               "quantity": np.array(["DV_over_rs", "DH_over_rs", "DM_over_rs", "DM_over_rs"]),
               "cho": cho_factor(covariance, lower=True)}
        shape = bao_shape_from_grid(bao, z_grid, h_grid)
        bao["value"] = 29.7 * shape + np.array([0.2, -0.08, 0.4, -0.3])
        expected_alpha = float(shape @ cho_solve(bao["cho"], bao["value"])) / float(shape @ cho_solve(bao["cho"], shape))
        residual = bao["value"] - expected_alpha * shape
        expected_chi2 = float(residual @ cho_solve(bao["cho"], residual))
        actual_chi2, actual_alpha = chi2_desi_bao_from_grid(bao, z_grid, h_grid)
        self.assertEqual(actual_alpha, expected_alpha)
        self.assertEqual(actual_chi2, expected_chi2)

    def _fixture(self, root: Path):
        sn_dir, bao_dir = root / "real_SN", root / "real_BAO"
        sn_dir.mkdir()
        bao_dir.mkdir()
        z_sn = np.array([0.1, 0.25, 0.6, 1.0])
        z_bao = np.linspace(0.2, 2.5, 13)
        quantity = np.array((["DV_over_rs", "DM_over_rs", "DH_over_rs"] * 5)[:13])
        grid = np.linspace(0.0, 2.5 * 1.001, 3000)
        h = np.sqrt(0.32 * (1.0 + grid) ** 3 + (1.0 - 0.32))
        mu = mu_model_from_h_grid(z_sn, z_sn + 0.001, grid, h, 70.0) + 0.17
        sn_lines = ["# real fixture metadata\n", "VARNAMES: CID zHD zHEL MU MUERR\n"]
        sn_lines += [f"SN: original_{i} {z:.17g} {z+0.001:.17g} {value:.17g} 0.1\n"
                     for i, (z, value) in enumerate(zip(z_sn, mu))]
        (sn_dir / SN_TABLE).write_text("".join(sn_lines))
        covariance = np.diag([0.01, 0.02, 0.03, 0.04]) + 0.002 * np.ones((4, 4))
        precision = np.linalg.inv(covariance)
        # This deliberately exercises DES's misleading `cov` packed-precision format.
        np.savez(sn_dir / SN_COV, nsn=np.array([4]), cov=precision[np.triu_indices(4)])
        shape = bao_shape_from_grid({"z": z_bao, "quantity": quantity}, grid, h)
        (bao_dir / BAO_TABLE).write_text("# real fixture metadata\n" + "".join(
            f"{z:.17g} {value:.17g} {q}\n" for z, value, q in zip(z_bao, 29.0 * shape, quantity)))
        np.savetxt(bao_dir / BAO_COV, np.diag(np.linspace(0.01, 0.05, 13)) + 0.001 * np.ones((13, 13)))
        return sn_dir, bao_dir

    def test_generation_roundtrip_labels_streams_profile_and_original_bytes(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            sn_dir, bao_dir = self._fixture(root)
            source_paths = [sn_dir / SN_TABLE, sn_dir / SN_COV, bao_dir / BAO_TABLE, bao_dir / BAO_COV]
            original_hashes = {path: sha256_file(path) for path in source_paths}
            output = root / "MOCK_fixture"
            manifest = generate_mock(sn_dir, bao_dir, output, seed=20260908)
            self.assertEqual(manifest["generation_status"], "VERIFIED")
            self.assertEqual(manifest["N_SN"], 4)
            self.assertEqual(manifest["N_BAO"], 13)
            self.assertAlmostEqual(manifest["generating_fit"]["Omega_m0"], 0.32, places=14)
            self.assertAlmostEqual(manifest["generating_fit"]["sn_offset_hat"], 0.17, places=12)
            self.assertAlmostEqual(manifest["generating_fit"]["bao_alpha_hat"], 29.0, places=12)
            for folder in [output, output / "SN", output / "BAO"]:
                metadata = json.loads((folder / "manifest.json").read_text())
                self.assertEqual(metadata["dataset_kind"], DATASET_KIND)
                self.assertIs(metadata["is_real_observation"], False)
                self.assertIn("NOT REAL OBSERVATIONS", (folder / "README_MOCK.md").read_text())
            self.assertTrue((output / "SN" / SN_TABLE).read_text().startswith("# MOCK / SYNTHETIC"))
            self.assertTrue((output / "BAO" / BAO_TABLE).read_text().startswith("# MOCK / SYNTHETIC"))
            self.assertEqual(sha256_file(output / "SN" / SN_COV), original_hashes[sn_dir / SN_COV])
            self.assertEqual(sha256_file(output / "BAO" / BAO_COV), original_hashes[bao_dir / BAO_COV])
            for source, digest in original_hashes.items():
                self.assertEqual(sha256_file(source), digest)
            expected_generated = {
                f"SN/{SN_TABLE}", f"SN/{SN_COV}", f"BAO/{BAO_TABLE}", f"BAO/{BAO_COV}",
                "MOCK_generation_arrays.npz", "MOCK_LCDM_reference.json",
            }
            self.assertEqual(set(manifest["generated_files_sha256"]), expected_generated)
            for relative_path, digest in manifest["generated_files_sha256"].items():
                self.assertEqual(sha256_file(output / relative_path), digest)
            generating_cache = output / "REAL_DATA_GENERATING_FIT_ONLY_cache"
            cache_marker = json.loads((generating_cache / "manifest.json").read_text())
            self.assertEqual(cache_marker["record_kind"], "REAL_DATA_GENERATING_FIT_ONLY")
            self.assertEqual(cache_marker["input_dataset_kind"], "REAL_OBSERVATION")
            self.assertIs(cache_marker["is_mock_search_result"], False)
            self.assertNotIn("dataset_kind", cache_marker)
            self.assertIn("REAL OBSERVATIONS", (generating_cache / "README_MOCK.md").read_text())
            mock_cache_marker = json.loads((output / "MOCK_LCDM_cache" / "manifest.json").read_text())
            self.assertEqual(mock_cache_marker["dataset_kind"], DATASET_KIND)
            arrays = np.load(output / "MOCK_generation_arrays.npz", allow_pickle=False)
            self.assertEqual(str(arrays["dataset_kind"]), DATASET_KIND)
            self.assertFalse(bool(arrays["is_real_observation"]))
            sn, bao = load_des_sn(output / "SN"), load_desi_dr2_bao(output / "BAO")
            np.testing.assert_array_equal(sn["mu"], arrays["sn_mock"])
            np.testing.assert_array_equal(bao["value"], arrays["bao_mock"])
            streams = np.random.SeedSequence(20260908).spawn(2)
            np.testing.assert_array_equal(arrays["sn_whitened_gaussian"], np.random.Generator(np.random.PCG64(streams[0])).standard_normal(4))
            np.testing.assert_array_equal(arrays["bao_whitened_gaussian"], np.random.Generator(np.random.PCG64(streams[1])).standard_normal(13))
            np.testing.assert_allclose(arrays["sn_mock"], arrays["sn_mean"] + arrays["sn_noise"], atol=0)
            self.assertAlmostEqual(float(arrays["sn_noise"] @ sn["invcov"] @ arrays["sn_noise"]), float(arrays["sn_whitened_gaussian"] @ arrays["sn_whitened_gaussian"]), places=12)
            # The saved nuisance means reproduce the fitted real LCDM shape exactly.
            noiseless = dict(sn, mu=arrays["sn_mean"])
            c2, offset = chi2_des_sn_from_grid(noiseless, arrays["z_grid"], arrays["h_grid"], 70.0)
            self.assertAlmostEqual(c2, 0.0, places=10)
            self.assertAlmostEqual(offset, 0.17, places=12)
            ref = json.loads((output / "MOCK_LCDM_reference.json").read_text())
            self.assertEqual(ref["record_kind"], "MOCK_LCDM_REFIT")
            self.assertGreater(ref["fit"]["chi2"], 0.0)
            self.assertTrue(list((output / "MOCK_LCDM_cache").glob("lcdm_reference_*.json")))
            with self.assertRaises(FileExistsError):
                generate_mock(sn_dir, bao_dir, output, seed=20260908)

    def test_destination_and_table_overwrite_guards(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            sn_dir, bao_dir = self._fixture(root)
            for output in (root / "unlabelled", sn_dir / "MOCK_inside_observations"):
                with self.assertRaises(ValueError):
                    _validate_destination(sn_dir, bao_dir, output)
            with self.assertRaises(FileExistsError):
                write_sn_mock_table(sn_dir / SN_TABLE, sn_dir / SN_TABLE, np.zeros(4))
            with self.assertRaises(FileExistsError):
                write_bao_mock_table(bao_dir / BAO_TABLE, bao_dir / BAO_TABLE, np.zeros(13))
            bad = root / "MOCK_bad_row_count.txt"
            with self.assertRaises(ValueError):
                write_sn_mock_table(sn_dir / SN_TABLE, bad, np.zeros(5))
            self.assertFalse(bad.exists())


if __name__ == "__main__":
    unittest.main()
