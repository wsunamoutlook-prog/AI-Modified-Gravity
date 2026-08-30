# Signal Lab Method References

The implementation favors standard numerical definitions and primary or
official sources.  These references support method selection; they do not
replace instrument manuals or experiment-specific calibration papers.

## General signal processing

- SciPy Signal Processing API, including Butterworth/notch filters,
  periodograms, Welch PSD, cross spectra, coherence, STFT, peak finding,
  correlation, resampling, and Lomb--Scargle:
  <https://docs.scipy.org/doc/scipy/reference/signal.html>
- A. Savitzky and M. J. E. Golay, smoothing and differentiation by simplified
  least squares, *Analytical Chemistry* **36**, 1627 (1964),
  <https://doi.org/10.1021/ac60214a047>.
- P. H. C. Eilers and H. F. M. Boelens, asymmetric least-squares baseline
  correction (2005), the basis of `baseline.asls`.
- D. W. Allan, variance analysis of frequency stability, *Proceedings of the
  IEEE* **54**, 221 (1966); NIST Special Publication 1065:
  <https://tf.nist.gov/general/pdf/2220.pdf>.
- Zurich Instruments, lock-in amplifier principles and demodulator filters:
  <https://docs.zhinst.com/pdf/ziMFIA_UserManual.pdf>.

## Optical measurements

- T. T. Tauc, optical absorption edge analysis; users must select the
  transition exponent and fit interval appropriate to the material.
- D. E. Aspnes, optical-property inversion and Kramers--Kronig analysis; for a
  constrained variational formulation see
  <https://arxiv.org/abs/cond-mat/0503565>.
- NIST, Stokes-parameter and polarization measurement conventions:
  <https://www.govinfo.gov/content/pkg/GOVPUB-C13-283cba0d329737c161c3a4d73a039cff/pdf/GOVPUB-C13-283cba0d329737c161c3a4d73a039cff.pdf>.
- E. Gratton and co-workers, fluorescence-lifetime phasor analysis:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC2157251/>.
- W. H. Richardson (1972) and L. B. Lucy (1974), iterative image
  deconvolution; numerical discussion:
  <https://www.aanda.org/articles/aa/full_html/2012/03/aa18681-11/aa18681-11.html>.
- ISO 12233 slanted-edge MTF concepts.  `optics.edge_mtf` implements the
  one-dimensional edge/line-spread Fourier core, not the complete ISO camera
  conformance workflow.
- M. C. Beard, G. M. Turner, and C. A. Schmuttenmaer, terahertz time-domain
  spectroscopy analysis and complex transfer functions, *J. Phys. Chem. B*
  **106**, 7146 (2002), <https://doi.org/10.1021/jp020579i>.
- D. F. Eaton, reference-comparison photoluminescence quantum-yield methods,
  *Pure Appl. Chem.* **60**, 1107 (1988),
  <https://doi.org/10.1351/pac198860071107>.

## Condensed-matter measurements

- L. J. van der Pauw, four-terminal sheet-resistance method; practical Hall
  and van der Pauw guidance from NIST:
  <https://www.nist.gov/pml/nanoscale-device-characterization-division/popular-links/hall-effect/hall-effect>.
- H. M. Rietveld, profile refinement, *Journal of Applied Crystallography*
  **2**, 65 (1969), <https://doi.org/10.1107/S0021889869006558>.
- D. A. Shirley, photoemission background, *Physical Review B* **5**, 4709
  (1972), <https://doi.org/10.1103/PhysRevB.5.4709>.
- B. D. Cullity and S. R. Stock, *Elements of X-Ray Diffraction*, for Bragg and
  Scherrer analysis and instrumental-broadening caveats.
- D. Shoenberg, *Magnetic Oscillations in Metals*, for Onsager frequency,
  Lifshitz--Kosevich thermal damping, Dingle analysis, and Landau fans.
- S. Hikami, A. I. Larkin, and Y. Nagaoka, two-dimensional
  magnetoconductance, *Prog. Theor. Phys.* **63**, 707 (1980),
  <https://doi.org/10.1143/PTP.63.707>.
- B. E. Warren, *X-Ray Diffraction*, for reciprocal-space transforms and
  total-scattering pair-distribution concepts; quantitative PDF analysis also
  requires experiment-specific normalization and termination corrections.
- M. Newville, fundamentals of X-ray absorption fine structure data reduction,
  *Rev. Mineral. Geochem.* **78**, 33 (2014),
  <https://doi.org/10.2138/rmg.2014.78.2>.
- N. F. Mott and E. A. Davis, variable-range hopping; the exponent must be
  selected for the dimensionality and interaction regime under study.
- Standard Curie--Weiss, Debye low-temperature heat-capacity, Arrhenius, Hall,
  Seebeck, thermal-conductivity, and conductivity-tensor relations are exposed
  as explicit fit/transform atoms with their assumptions in the registry.
