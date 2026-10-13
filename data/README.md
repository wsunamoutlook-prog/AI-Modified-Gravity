# Likelihood inputs

These are the observed-data inputs used by `solver_v5_2/likelihood.py`.
They are retained in the release so the background likelihood can be evaluated
without fetching files from an experiment archive.

| File | Role |
| --- | --- |
| `SN data/DES-Dovekie_HD.csv` | DES supernova distance-modulus table, including heliocentric and Hubble-diagram redshifts. The likelihood uses 1820 entries. |
| `SN data/STAT+SYS.npz` | Compressed upper-triangle SN precision matrix used by the supplied Dovekie likelihood. Despite the internal `cov` key, it is not a covariance to invert again. |
| `SN data/DES-Dovekie-SN_Likelihood.py` | Supplied SN likelihood reference implementation. |
| `BAO data/desi_gaussian_bao_ALL_GCcomb_mean.txt` | The 13 DESI DR2 BAO distance-ratio measurements. |
| `BAO data/desi_gaussian_bao_ALL_GCcomb_cov.txt` | Full covariance for those BAO measurements, in the same order. |

The SN magnitude offset and BAO scale are profiled independently. The likelihood
adds the two chi-squares and assumes no SN–BAO cross-covariance. It contains no
CMB constraint. `MUERR` is not added to the supplied SN uncertainty matrix again.
Please cite the DES and DESI data papers cited in the manuscript when using
these inputs.

Treat these files as read-only. Synthetic observations must be written to a
separate `MOCK_*` directory with their generation metadata and a separately
refitted reference. They must never replace the files here.
