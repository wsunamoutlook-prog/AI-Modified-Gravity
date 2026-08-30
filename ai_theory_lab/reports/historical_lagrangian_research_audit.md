# Historical Lagrangian Research Audit

## 1. Scope and interpretation

This audit searches the locally available historical outputs rather than only one
benchmark run. The inventory contains 143 `attempt_history.jsonl` files (138
distinct by content hash), 17,513 pulled accepted-sample summaries, the old
full-space Solver scans, and the later GPT/Claude/Gemini/Qwen/DeepSeek agent
runs. After structural deduplication, the agent histories contain about 2,052
distinct accepted operator/scalar families.

Model attribution is made only when the individual proposal JSON records
`proposal_mode=llm` together with a non-null provider and model. A theory found
inside a model-named run after `direct_candidate_policy` fallback is retained
as a historical physics result but is explicitly **not** credited to that LLM.

The shortlist below deliberately separates three notions of value:

1. **Statistical value:** low \(\chi^2_{\rm tot}\) and competitive stored AIC.
2. **Structural value:** a compact non-EH or degenerate curvature combination
   that admits a recognizable covariant or FLRW interpretation.
3. **Diagnostic value:** a theory that exposes a boundary term, a cancelled
   correction, or a scalar-only explanation of an apparently good fit.

Passing the project pipeline means:

\[
\text{grammar valid}\to\text{FLRW EOM filter}\to\text{Builder}
\to\text{background Solver}.
\]

It does **not** establish full covariant ghost freedom, scalar/tensor
perturbation stability, a healthy Newtonian limit, Solar-System bounds, or
gravitational-wave constraints. All quoted fits use the background
DES-SN + DESI DR2 BAO likelihood.

### AIC convention

Every AIC below is the value stored with that historical Solver result,

\[
{\rm AIC}_{\rm stored}=\chi^2_{\rm tot}+2k_{\rm stored}.
\]

The historical comparison reports used
\(\chi^2_{\Lambda{\rm CDM}}=1645.28\),
\({\rm AIC}_{\Lambda{\rm CDM}}=1653.28\), and \(k_{\Lambda{\rm CDM}}=4\).
The current code uses the better-motivated effective count
\(k_{\Lambda{\rm CDM}}=3\), which would give
\({\rm AIC}_{\Lambda{\rm CDM}}=1651.28\). One must not subtract the new
baseline AIC from an old candidate AIC without first recounting that candidate's
effective parameters under the same convention. Before publication, the
shortlisted models should therefore be replayed once with the current
post-reduction \(k\) counter.

## 2. Notation and FLRW identities

We use

\[
X_i\equiv \nabla_\mu\phi_i\nabla^\mu\phi_i,\qquad
V_i^{\rm quad}=\frac12m_i^2\phi_i^2,\qquad
V_i^{\rm ax}=m_i^2f_i^2\left[1-\cos(\phi_i/f_i)\right].
\]

For a spatially flat FLRW metric with lapse \(N=1\),

\[
\begin{aligned}
R &= 6(2H^2+\dot H),\\
R_{\mu\nu}R^{\mu\nu}
 &=12(3H^4+3H^2\dot H+\dot H^2),\\
R_{\mu\nu\rho\sigma}R^{\mu\nu\rho\sigma}
 &=12(2H^4+2H^2\dot H+\dot H^2),\\
\mathcal G
 &\equiv R^2-4R_{\mu\nu}R^{\mu\nu}
   +R_{\mu\nu\rho\sigma}R^{\mu\nu\rho\sigma}
 =24H^2(H^2+\dot H).
\end{aligned}
\]

Hence, on flat FLRW only,

\[
R_{\mu\nu}R^{\mu\nu}
-R_{\mu\nu\rho\sigma}R^{\mu\nu\rho\sigma}
=\frac12\mathcal G.
\]

This last equality is an FLRW identity, **not** a covariant identity. A
covariant Gauss--Bonnet coupling requires the complete combination
\(F(\phi)\mathcal G=F(\phi)(R^2-4R_{\mu\nu}^2+R_{\mu\nu\rho\sigma}^2)\).

For any homogeneous nonminimal coupling \(F(\phi)R\),

\[
\int dt\,a^3 F R
\doteq -6\int dt\,a^3\left(FH^2+H\dot F\right),
\]

where \(\doteq\) denotes equality up to a boundary term. With the mostly-plus
signature,

\[
\Box\phi=-\ddot\phi-3H\dot\phi,\qquad X_\phi=-\dot\phi^2.
\]

## 3. Shortlist at a glance

The \(\Delta{\rm AIC}_{\rm old}\) column uses the historical
\(\Lambda\)CDM AIC \(1653.28\) only as an internal diagnostic.

| ID | Source and sector | \(\chi^2\) | stored AIC | \(k\) | \(\Delta{\rm AIC}_{\rm old}\) | Why it matters |
|---|---|---:|---:|---:|---:|---|
| O1 | GPT-5.5 open search | 1637.953 | 1649.953 | 6 | -3.327 | Best exact-coefficient active \(R^2+\phi R^2\) candidate |
| O2 | Qwen 3.7 open search | 1637.930 | 1651.930 | 7 | -1.350 | Lowest historical agent \(\chi^2\); scalar-dependent Riemann-squared |
| O3 | DeepSeek V4 open search | 1637.962 | 1651.962 | 7 | -1.318 | Compact Ricci-squared deformation |
| N1 | DeepSeek V4 non-EH | 1693.860 | 1721.860 | 14 | +68.580 | Best non-EH fit; induced gravity plus kinetic mixing |
| N2 | sector-v3 non-EH | 1861.637 | 1893.637 | 16 | +240.357 | Strongest exact-coefficient higher-derivative non-EH branch |
| N3 | DeepSeek V4 non-EH | 1874.173 | 1896.173 | 11 | +242.893 | Curvature-cubic and scalar-curvature EFT |
| N4 | Qwen 3.7 non-EH | 1896.001 | 1918.001 | 11 | +264.721 | Rich non-EH branch with several removable boundary pieces |
| N5 | old \(L\#961\) non-EH | 1934.592 | 1952.592 | 9 | +299.312 | Clean \(\phi R+\phi^2\mathcal G/2\) form on FLRW |
| N6 | Claude-run deterministic fallback | 1930.880 | 1948.880 | 9 | +295.600 | Broad pure/high-curvature EFT stress test |
| N7 | Gemini-run deterministic fallback | 1939.014 | 1959.014 | 10 | +305.734 | Mixed Riemann/cubic/scalar-curvature branch |
| N8 | old \(L\#622\) non-EH | 1946.871 | 1964.871 | 9 | +311.591 | Linear scalar, FLRW-GB-equivalent branch |
| N9 | old \(L\#434\) non-EH | 1946.871 | 1964.871 | 9 | +311.591 | Quadratic scalar, FLRW-GB-equivalent branch |
| C1 | old \(L\#682\) control | 1641.353 | 1653.353 | 6 | +0.073 | All higher-curvature terms cancel; EH + scalar baseline |
| C2 | old \(L\#1038\) control | 1678.041 | 1690.041 | 6 | +36.761 | Surviving correction is a total derivative |
| C3 | old \(L\#944\) control | 1715.114 | 1737.114 | 11 | +83.834 | Effective scalar kinetic/potential theory, not modified gravity |

The best repeated modern DES-SN + DESI evaluation of \(L\#961\) found in the
old scans is \(\chi^2=1929.10\), AIC \(=1947.10\). The detailed entry below
uses the canonical v5.2 result because it has the fully recovered coefficient
row; repeated modern evaluations span approximately
\(\chi^2=1929.10\)--\(1946.86\). Older Hz-only and Hz+SN runs are not mixed
into this table.

### 中文阅读指南

- **O1：最值得先重跑的统计候选。** 它是 EH 引力加
  \(R^2+\phi_1R^2\) 修正；历史 AIC 优于同口径
  \(\Lambda\)CDM，而且最佳点的修正系数并非简单收敛到零。
- **O2/O3：低 \(\chi^2\) 的曲率平方候选。** 二者分别让标量场调制
  Riemann 平方和 Ricci 平方，但精确终点系数需要重新恢复；协变层面
  也必须检查额外自由度和稳定性。
- **N1：数值上最好的无裸 \(R\) 候选。** \(\phi_2^2R\) 生成有效
  Planck 质量，并伴随两个标量之间的动力学混合；它的研究重点不是
  再压低一点 \(\chi^2\)，而是检查有效牛顿常数、动能矩阵和局域极限。
- **N2/N3/N4/N6/N7：高导数 EFT 候选。** 它们证明某些复杂非 EH
  结构能通过背景管线，但目前更适合作为逐项消融的母模型，不能直接
  宣称为协变无鬼理论。
- **N5（\(L\#961\)）：结构上最干净。** 过滤后只剩
  \(\phi_2R+\phi_2^2(R_{\mu\nu}^2-R_{\mu\nu\rho\sigma}^2)\)；
  后一组合仅在平直 FLRW 上等于 \(\phi_2^2\mathcal G/2\)，并非完整
  协变 Gauss--Bonnet 耦合。
- **N8/N9：\(L\#961\) 的对照族。** 它们分别给出线性和二次标量乘
  同一个 FLRW-GB 等效组合，适合用于研究“背景简并是否能提升为协变
  简并”。
- **C1/C2/C3：诊断对照，不是新引力发现。** 它们分别展示修正被
  cancellation 条件消掉、修正退化为边界项、以及只剩标量动能/势能
  重整化的情况。

## 4. Statistically competitive open-search theories

### O1. Active \(R^2+\phi_1R^2\) correction

**Readable form.** Einstein gravity, a quadratic scalar, a constant \(R^2\)
correction, and a scalar-dependent \(R^2\) correction.

**Exact validated Lagrangian**

\[
\boxed{
\mathcal L_{\rm O1}=\sqrt{-g}\left[
M_{\rm P}^2\left(
\alpha R+\frac{\beta}{\Lambda^2}R^2
+\frac{\gamma}{\Lambda^3}\phi_1R^2
\right)
-\frac12X_1-\frac12m_1^2\phi_1^2
\right].
}
\]

\[
\chi^2=1637.953294,\quad
{\rm AIC}=1649.953294,\quad
{\rm BIC}=1683.035550,\quad k=6.
\]

\[
\alpha=0.5,\qquad
\beta=1.4027\times10^{13},\qquad
\gamma=-4.4330\times10^2,
\]

with \(H_0=65.45~{\rm km\,s^{-1}\,Mpc^{-1}}\),
\(\Omega_{m0}=0.2716\), and \(\Lambda/H_0=4615.4\).

**Why study it.** It is the best candidate for a direct statistical follow-up:
the exact Solver row is available, its stored AIC beats the historical
\(\Lambda\)CDM reference by 3.33, and the \(R^2\) coefficient is not merely
numerically zero. On FLRW, \(R^2=36(2H^2+\dot H)^2\). The next tests should be
a current-\(k\) replay, scalaron/auxiliary-field reformulation, and perturbative
stability. Passing the project FLRW cancellation filter alone is not a proof
that this covariant higher-curvature action is healthy.

Source:
`cmp1500_openai_gpt_5_5_expensive_v1`,
`task_000347_expanded_refine_slot_05_lag_1`.

### O2. Scalar-dependent Kretschmann correction

**Readable form.** Einstein gravity plus an axion whose value controls the
Kretschmann scalar \(K=R_{\mu\nu\rho\sigma}R^{\mu\nu\rho\sigma}\).

\[
\boxed{
\mathcal L_{\rm O2}=\sqrt{-g}\left[
M_{\rm P}^2\left(
\alpha R+\frac{\beta}{\Lambda^3}\phi_1K
+\frac{\gamma}{\Lambda^4}\phi_1^2K
\right)
-\frac12X_1-V_1^{\rm ax}
\right].
}
\]

\[
\chi^2=1637.930341,\quad
{\rm AIC}=1651.930341,\quad
{\rm BIC}=1690.526306,\quad k=7.
\]

The locally recovered coefficient vector nearest to the terminal optimum is

\[
\alpha=0.5,\qquad
\beta=-4.67\times10^{13},\qquad
\gamma=9.69\times10^{14}.
\]

These coefficients are **not** an exact terminal best-fit row; the structure
and fit metrics are exact, while the vector was recovered from the nearest
current-loop joint-prior sample. On flat FLRW,

\[
K=12(2H^4+2H^2\dot H+\dot H^2).
\]

**Why study it.** This is the lowest \(\chi^2\) found in the pulled historical
agent runs, but its AIC advantage is only 1.35 under the old convention and the
exact terminal coefficients need a replay. It is a useful test of whether a
scalar-dependent Kretschmann term can remain active without violating
perturbative stability.

Source:
`cmp2000_qwen3_7_plus_cheap_v1`,
`task_000847_expanded_slot_01_lag_1`.

### O3. Compact Ricci-squared deformation

**Readable form.** Einstein gravity plus an axion-dependent coefficient of
\(R_{\mu\nu}R^{\mu\nu}\).

\[
\boxed{
\mathcal L_{\rm O3}=\sqrt{-g}\left[
M_{\rm P}^2\left(
\alpha R+\frac{\beta}{\Lambda^2}R_{\mu\nu}R^{\mu\nu}
+\frac{\gamma}{\Lambda^4}\phi_1^2R_{\mu\nu}R^{\mu\nu}
\right)
-\frac12X_1-V_1^{\rm ax}
\right].
}
\]

\[
\chi^2=1637.961668,\quad
{\rm AIC}=1651.961668,\quad
{\rm BIC}=1690.557632,\quad k=7.
\]

Nearest recovered, rather than exact terminal, coefficients:

\[
\alpha=0.5,\qquad \beta=-9.134\times10^3,\qquad
\gamma=-7.01\times10^8.
\]

**Why study it.** Its stored AIC is competitive and the operator content is
more compact than most agent proposals. Unlike the FLRW-GB combinations below,
generic Ricci-squared gravity carries an additional spin-2 concern covariantly;
the next calculation must therefore be a perturbation/auxiliary-field analysis,
not only another background scan.

Source:
`cmp2000_deepseek_ali_v4_pro_cheap_v1`,
`task_001266_slot_03_lag_1`.

## 5. Non-EH theories with research value

### N1. Best non-EH fit: induced gravity with kinetic mixing

**Readable form.** There is no bare Einstein-Hilbert term. The effective Planck
mass is generated by \(\phi_2^2R\), while \(\phi_2\) also controls the kinetic
sector of \(\phi_1\).

\[
\boxed{
\begin{aligned}
\mathcal L_{\rm N1}=\sqrt{-g}\Bigg[
&M_{\rm P}^2\frac{\alpha}{\Lambda^2}\phi_2^2R
+\frac{\beta}{\Lambda}\phi_1\Box\phi_1\,\phi_2
+\frac{\gamma}{\Lambda^2}\phi_1\Box\phi_1\,\phi_2^2\\
&-\frac12X_1-V_1^{\rm ax}
-\frac12X_2-V_2^{\rm quad}
\Bigg].
\end{aligned}
}
\]

\[
\chi^2=1693.859901,\quad
{\rm AIC}=1721.859901,\quad
{\rm BIC}=1799.051831,\quad k=14.
\]

The exact terminal coefficient row was not present in the local pull. The
nearest recovered current-loop vector, whose own
\(\chi^2=1702.424\), is

\[
\alpha=-7.251\times10^3,\qquad
\beta=-57.47,\qquad
\gamma=3.64\times10^{11}.
\]

Writing

\[
F(\phi_2)=M_{\rm P}^2\alpha\phi_2^2/\Lambda^2,\qquad
G(\phi_2)=\beta\phi_2/\Lambda+\gamma\phi_2^2/\Lambda^2,
\]

the FLRW nonminimal term becomes

\[
\int dt\,a^3F R\doteq
-6\int dt\,a^3(FH^2+H\dot F),
\]

and integration by parts gives

\[
\int\sqrt{-g}\,G\phi_1\Box\phi_1
\doteq-\int\sqrt{-g}\left[
G X_1+\phi_1G_{,\phi_2}\nabla_\mu\phi_1\nabla^\mu\phi_2
\right].
\]

**Why study it.** This is by far the best non-EH background fit in the pulled
history. It has a clear scalar-tensor interpretation rather than a random pile
of invariants. Its central risk is equally clear: without a bare \(M_{\rm P}^2R\)
term, the sign and evolution of \(F(\phi_2)\) determine the effective Newton
constant. A serious follow-up must require \(F>0\), check zero crossings,
diagonalize the scalar kinetic matrix, and test local/perturbative gravity.

Source:
`cmp2000_deepseek_ali_v4_pro_cheap_v1`,
`task_000425_expanded_refine_slot_08_lag_1`.

### N2. Exact higher-derivative two-scalar branch

**Readable form.** A genuinely non-EH action combining a derivative of the
Ricci tensor, scalar-coupled curvature squares, and derivative self-interactions
of two axions.

\[
\boxed{
\begin{aligned}
\mathcal L_{\rm N2}=\sqrt{-g}\Bigg\{M_{\rm P}^2\Bigg[
&\frac{\alpha}{\Lambda^4}
\nabla_\rho R_{\mu\nu}\nabla^\rho R^{\mu\nu}
+\frac{\beta}{\Lambda^3}\phi_2R_{\mu\nu}R^{\mu\nu}\\
&+\frac{\gamma}{\Lambda^3}\phi_2
R_{\mu\nu\rho\sigma}R^{\mu\nu\rho\sigma}
\Bigg]
+\frac{\delta}{\Lambda}X_1\phi_2\\
&+\frac{\epsilon}{\Lambda^2}\phi_2^3\Box\phi_2
+\frac{\zeta}{\Lambda^2}\phi_2^2X_2
-\frac12X_1-V_1^{\rm ax}-\frac12X_2-V_2^{\rm ax}
\Bigg\}.
\end{aligned}
}
\]

\[
\chi^2=1861.637101,\quad
{\rm AIC}=1893.637101,\quad
{\rm BIC}=1981.856449,\quad k=16.
\]

\[
\begin{aligned}
\alpha&=8.5234\times10^{10},&
\beta&=-2.4083\times10^5,&
\gamma&=-6.4725\times10^5,\\
\delta&=-4.3198\times10^5,&
\epsilon&=-3.2071\times10^9,&
\zeta&=4.7083\times10^{-5}.
\end{aligned}
\]

**Why study it.** It is the best non-EH branch for which both the terminal fit
and all displayed coefficients are exact. It is not a compact final theory:
the \(\nabla R_{\mu\nu}\nabla R^{\mu\nu}\) operator is a serious covariant
higher-derivative warning, and only 16 of 1000 samples were accepted. Its value
is as evidence that a very restricted viable parameter island exists and as a
target for operator ablation: remove one sector at a time and test whether the
fit survives.

Source:
`graph_agent_batch_312_sector_v3`,
`wave_0001_complex_lag_12`.

### N3. Curvature-cubic scalar EFT

\[
\boxed{
\begin{aligned}
\mathcal L_{\rm N3}=\sqrt{-g}\Bigg\{M_{\rm P}^2\Bigg[
&\frac{\alpha}{\Lambda^4}R
R_{\mu\nu\rho\sigma}R^{\mu\nu\rho\sigma}
+\frac{\beta}{\Lambda^4}
\nabla^\rho R^{\mu\nu}\nabla_\nu R_{\mu\rho}\\
&+\frac{\gamma}{\Lambda^3}\phi_2^3R
+\frac{\delta}{\Lambda^3}\phi_2R_{\mu\nu}R^{\mu\nu}
+\frac{\epsilon}{\Lambda^3}\phi_2
R_{\mu\nu\rho\sigma}R^{\mu\nu\rho\sigma}
\Bigg]\\
&+\frac{\zeta}{\Lambda}\phi_2^2\Box\phi_2
+\frac{\eta}{\Lambda^2}\phi_2^2X_2
-\frac12X_2-V_2^{\rm quad}\Bigg\}.
\end{aligned}
}
\]

\[
\chi^2=1874.172629,\quad
{\rm AIC}=1896.172629,\quad
{\rm BIC}=1956.823431,\quad k=11.
\]

The local history contains the exact structure and metrics but not the exact
terminal coefficient row. This candidate is useful for ablation and
degeneracy searches, not yet for quoting a physical best-fit parameter point.
No Gauss--Bonnet claim is justified unless the reduced coefficient relations
are explicitly shown.

Source:
`cmp2000_deepseek_ali_v4_pro_cheap_v1`,
`task_001042_expanded_refine_slot_01_lag_1`.

### N4. Qwen non-EH branch and its boundary reductions

\[
\boxed{
\begin{aligned}
\mathcal L_{\rm N4}=\sqrt{-g}\Bigg\{M_{\rm P}^2\Bigg[
&\frac{\alpha}{\Lambda^2}\Box R
+\frac{\beta}{\Lambda^4}\mathcal R_{3a}
+\frac{\gamma}{\Lambda^2}\phi_2^2R\\
&+\frac{\delta}{\Lambda^3}\phi_2R_{\mu\nu}R^{\mu\nu}
+\frac{\epsilon}{\Lambda^3}\phi_2
R_{\mu\nu\rho\sigma}R^{\mu\nu\rho\sigma}
+\frac{\zeta}{\Lambda^4}\phi_2\Box\phi_2 R
\Bigg]\\
&+\eta\phi_2\Box\phi_2
+\frac{\theta}{\Lambda^2}\phi_2^2X_2
-\frac12X_2-V_2^{\rm quad}\Bigg\},
\end{aligned}
}
\]

where
\(\mathcal R_{3a}=R_{\mu\nu}{}^{\rho\sigma}
R_{\rho}{}^{\mu\alpha\beta}R_{\sigma\alpha\beta}{}^\nu\)
denotes the contraction used by the grammar.

\[
\chi^2=1896.000881,\quad
{\rm AIC}=1918.000881,\quad
{\rm BIC}=1978.651683,\quad k=11.
\]

\[
\begin{aligned}
\alpha&=4.1096\times10^5,&
\beta&=-3.5114\times10^{-6},&
\gamma&=-8.8450\times10^3,\\
\delta&=-3.0887\times10^{-2},&
\epsilon&=4.1229\times10^7,&
\zeta&=-6.3842\times10^3,\\
\eta&=5.2826\times10^{15},&
\theta&=1.4184\times10^{-10}.&
\end{aligned}
\]

**Reduction.** With constant \(\alpha\),
\(\int\sqrt{-g}\,\Box R\) is a boundary term. Also,

\[
\int\sqrt{-g}\,\eta\phi_2\Box\phi_2
\doteq-\int\sqrt{-g}\,\eta X_2,
\]

so this apparently huge \(\eta\) is a kinetic renormalization rather than a
new higher-curvature interaction. The physically active core is therefore
smaller than the raw eight-operator list: \(\phi_2^2R\), scalar-coupled
Ricci/Riemann squares, \(\phi_2\Box\phi_2R\), and the cubic curvature term.

Source:
`cmp2000_qwen3_7_plus_cheap_v1`,
`task_000809_expanded_refine_slot_03_lag_1`.

### N5. \(L\#961\): the cleanest FLRW-GB-equivalent structure

The raw grammar proposal contained nine nonminimal/curvature operators. The
FLRW EOM filter imposed

\[
\alpha=-\iota,\qquad
\beta=\gamma=\delta=\epsilon=\eta=\theta=0,
\]

leaving only \(\zeta\) and \(\iota\) free:

\[
\boxed{
\mathcal L_{961}^{\rm red}
=\sqrt{-g}\left[
M_{\rm P}^2\left(
\frac{\zeta}{\Lambda}\phi_2R
+\frac{\iota}{\Lambda^4}\phi_2^2
\left(R_{\mu\nu}R^{\mu\nu}
-R_{\mu\nu\rho\sigma}R^{\mu\nu\rho\sigma}\right)
\right)
-\frac12X_2-V_2^{\rm quad}
\right].
}
\]

Canonical v5.2 fit:

\[
\chi^2=1934.592396,\quad
{\rm AIC}=1952.592396,\quad
{\rm BIC}=2002.215779,\quad k=9,
\]

\[
\zeta=2.68593\times10^{-3},\qquad
\iota=-17.6097,\qquad
H_0=72.44,\qquad \Omega_{m0}=0.2901.
\]

On flat FLRW,

\[
\boxed{
\mathcal L_{961}^{\rm FLRW}
=\sqrt{-g}\left[
M_{\rm P}^2\left(
\frac{\zeta}{\Lambda}\phi_2R
+\frac{\iota}{2\Lambda^4}\phi_2^2\mathcal G
\right)
-\frac12X_2-V_2^{\rm quad}
\right].
}
\]

**Why study it.** This is the cleanest special structure in the whole archive.
It combines induced gravity with a quadratic scalar coupling to a
Gauss--Bonnet-equivalent FLRW invariant. It is also a good example of why the
raw operator count is misleading: seven displayed terms are removed by the
background degeneracy relations.

**Crucial caveat.** The covariant action contains
\(R_{\mu\nu}^2-R_{\mu\nu\rho\sigma}^2\), not the full
\(\mathcal G=R^2-4R_{\mu\nu}^2+R_{\mu\nu\rho\sigma}^2\).
The GB interpretation is therefore valid only after imposing flat FLRW.
A proper follow-up should construct the covariant completion
\(\phi_2^2\mathcal G\) and compare its background and perturbations with the
pipeline branch.

Source: old full-space \(L\#961\), canonical `solver_result/v5.2`.

### N6. High-curvature stress-test theory from a Claude-run fallback

\[
\boxed{
\begin{aligned}
\mathcal L_{\rm N6}=\sqrt{-g}\Bigg\{M_{\rm P}^2\Bigg[
&\frac{\alpha}{\Lambda^2}R^2
+\frac{\beta}{\Lambda^2}R_{\mu\nu}R^{\mu\nu}
+\frac{\gamma}{\Lambda^4}\mathcal R_{3c}
+\frac{\delta}{\Lambda^4}\mathcal R_{3a}\\
&+\frac{\epsilon}{\Lambda^4}R\Box R
+\frac{\zeta}{\Lambda^4}\phi_2^4R
+\frac{\eta}{\Lambda^4}\phi_2^2R_{\mu\nu}R^{\mu\nu}
+\frac{\theta}{\Lambda^4}\phi_2^2
R_{\mu\nu\rho\sigma}R^{\mu\nu\rho\sigma}
\Bigg]\\
&-\frac12X_2-V_2^{\rm quad}\Bigg\}.
\end{aligned}
}
\]

\[
\chi^2=1930.879552,\quad
{\rm AIC}=1948.879552,\quad
{\rm BIC}=1998.502935,\quad k=9.
\]

\[
\begin{aligned}
\alpha&=1.87\times10^{-9},&
\beta&=-1.09\times10^{12},&
\gamma&=1.90\times10^{-10},&
\delta&=-2.58\times10^{11},\\
\epsilon&=-1.62\times10^{15},&
\zeta&=-170.1,&
\eta&=4.54\times10^{-5},&
\theta&=6.11\times10^7.
\end{aligned}
\]

This is less attractive as a final model than N1 or \(L\#961\), but valuable
as an ablation target: its raw fit is better than most non-EH branches despite
having many nominal operators. A reduced-action analysis should first remove
integration-by-parts redundancies and then test which single curvature sector
actually controls the background.

Source:
`cmp1500_claude_opus_4_8_expensive_v1`,
`task_001247_expanded_refine_slot_07_lag_1`.
The proposal JSON records `proposal_mode=direct_candidate_policy` and no
LLM provider, so this structure must not be credited to Claude Opus itself.

### N7. Mixed-curvature branch from a Gemini-run fallback

\[
\boxed{
\begin{aligned}
\mathcal L_{\rm N7}=\sqrt{-g}\Bigg\{M_{\rm P}^2\Bigg[
&\frac{\alpha}{\Lambda^2}R_{\mu\nu\rho\sigma}^2
+\frac{\beta}{\Lambda^4}\mathcal R_{3b}
+\frac{\gamma}{\Lambda^3}\phi_2^3R\\
&+\frac{\delta}{\Lambda^3}\phi_2R_{\mu\nu}^2
+\frac{\epsilon}{\Lambda^4}\phi_2^2R_{\mu\nu}^2
+\frac{\zeta}{\Lambda^4}\phi_2^2R_{\mu\nu\rho\sigma}^2
\Bigg]\\
&+\eta\Lambda\Box\phi_2
+\frac{\theta}{\Lambda^2}\phi_2^2X_2
-\frac12X_2-V_2^{\rm quad}\Bigg\}.
\end{aligned}
}
\]

\[
\chi^2=1939.013956,\quad
{\rm AIC}=1959.013956,\quad
{\rm BIC}=2014.151048,\quad k=10.
\]

The \(\eta\Lambda\Box\phi_2\) term is a boundary term for constant \(\eta\).
The remaining theory is a mixed scalar-curvature EFT. Its coefficient ratios
do not by themselves demonstrate a Gauss--Bonnet combination.

Source:
`cmp1500_gemini_3_1_pro_expensive_v1`,
`task_001067_expanded_refine_slot_04_lag_1`.
The proposal JSON records `proposal_mode=direct_candidate_policy` and no
LLM provider, so this structure must not be credited to Gemini itself.

## 6. Clean FLRW-degenerate partners

### N8. \(L\#622\): linear scalar times the FLRW GB combination

The filter sets
\(\alpha=\beta=\zeta=0\) and \(\delta=-\epsilon\):

\[
\boxed{
\mathcal L_{622}^{\rm red}=\sqrt{-g}\left[
M_{\rm P}^2\frac{\epsilon}{\Lambda^3}\phi_2
\left(R_{\mu\nu\rho\sigma}^2-R_{\mu\nu}^2\right)
+\frac{\gamma}{\Lambda^2}\phi_2^2X_2
-\frac12X_2-V_2^{\rm quad}
\right].
}
\]

\[
\chi^2=1946.870857,\quad
{\rm AIC}=1964.870857,\quad
{\rm BIC}=2014.494241,\quad k=9,
\]

\[
\epsilon=-339.1804,\qquad \gamma=-146.9677.
\]

On flat FLRW,

\[
\mathcal L_{622}^{\rm FLRW}
=\sqrt{-g}\left[
-\frac{M_{\rm P}^2\epsilon}{2\Lambda^3}\phi_2\mathcal G
+\frac{\gamma}{\Lambda^2}\phi_2^2X_2
-\frac12X_2-V_2^{\rm quad}
\right].
\]

This is structurally clean but statistically sits on the common
\(\chi^2\simeq1946.87\) plateau.

Source: old full-space \(L\#622\), canonical `solver_result/v5.2`.

### N9. \(L\#434\): quadratic scalar times the FLRW GB combination

The filter sets \(\beta=-\gamma\) and \(\delta=0\):

\[
\boxed{
\mathcal L_{434}^{\rm red}=\sqrt{-g}\left[
M_{\rm P}^2\frac{\gamma}{\Lambda^4}\phi_2^2
\left(R_{\mu\nu}^2-R_{\mu\nu\rho\sigma}^2\right)
+\frac{\alpha}{\Lambda^2}\phi_2^2X_2
-\frac12X_2-V_2^{\rm quad}
\right].
}
\]

\[
\chi^2=1946.870851,\quad
{\rm AIC}=1964.870851,\quad
{\rm BIC}=2014.494234,\quad k=9,
\]

\[
\alpha=9.6969\times10^{-6},\qquad
\gamma=5.6818\times10^7.
\]

On flat FLRW,

\[
\mathcal L_{434}^{\rm FLRW}
=\sqrt{-g}\left[
\frac{M_{\rm P}^2\gamma}{2\Lambda^4}\phi_2^2\mathcal G
+\frac{\alpha}{\Lambda^2}\phi_2^2X_2
-\frac12X_2-V_2^{\rm quad}
\right].
\]

Together, \(L\#622\), \(L\#434\), and \(L\#961\) form a useful family:
linear and quadratic scalar couplings to the same FLRW curvature combination,
with \(L\#961\) additionally containing \(\phi_2R\).

Source: old full-space \(L\#434\), canonical `solver_result/v5.2`.

## 7. Diagnostic controls that should not be called new gravity

### C1. \(L\#682\): all corrections cancelled

The raw proposal contained derivative-curvature and cubic-curvature terms, but
the EOM relations set all of them to zero. The reduced theory is simply

\[
\boxed{
\mathcal L_{682}^{\rm red}
=\sqrt{-g}\left[
M_{\rm P}^2\gamma R-\frac12X_1-V_1^{\rm quad}
\right].
}
\]

\[
\chi^2=1641.352834,\qquad
{\rm AIC}=1653.352834,\qquad k=6.
\]

Its stored AIC is almost identical to the historical \(\Lambda\)CDM reference.
This is a useful baseline showing that a good raw fit need not indicate an
active higher-curvature correction.

### C2. \(L\#1038\): a total-derivative correction

After filtering, the only apparent curvature correction is

\[
\gamma=\eta:\qquad
\frac{\eta}{\Lambda^4}
\left(R\Box R+\nabla_\mu R\nabla^\mu R\right).
\]

But

\[
R\Box R+\nabla_\mu R\nabla^\mu R
=\nabla_\mu(R\nabla^\mu R),
\]

so the reduced action is EH + scalar up to a boundary term:

\[
\boxed{
\mathcal L_{1038}^{\rm red}
\doteq\sqrt{-g}\left[M_{\rm P}^2\theta R-\frac12X_1-V_1^{\rm quad}\right].
}
\]

\[
\chi^2=1678.040604,\qquad
{\rm AIC}=1690.040604,\qquad k=6.
\]

This is an important regression test for the report layer: operator presence
alone must not be interpreted as physical modified gravity.

### C3. \(L\#944\): scalar EFT after curvature cancellation

All higher-curvature coefficients vanish after the filter, leaving

\[
\boxed{
\mathcal L_{944}^{\rm red}
=\sqrt{-g}\left[
M_{\rm P}^2\delta R
+\beta\phi_1\Box\phi_1
+\epsilon\Lambda^2\phi_1^2
+\iota X_1-\frac12X_1-V_1^{\rm ax}
\right].
}
\]

\[
\chi^2=1715.113561,\qquad
{\rm AIC}=1737.113561,\qquad k=11.
\]

Since
\(\int\sqrt{-g}\,\phi_1\Box\phi_1
\doteq-\int\sqrt{-g}\,X_1\),
this is an effective scalar kinetic and potential renormalization, not a
higher-curvature discovery.

## 8. Recommended research order

### Tier A: worth immediate replay and physics analysis

1. **O1, \(R^2+\phi_1R^2\):** exact coefficients, competitive AIC, visibly
   active correction. Recompute current AIC, then analyze perturbations.
2. **N1, induced gravity + kinetic mixing:** best non-EH fit and a clear
   scalar-tensor interpretation. Check \(M_{\rm eff}^2=2F(\phi_2)>0\),
   kinetic eigenvalues, and the Newtonian limit.
3. **\(L\#961\):** cleanest special relation. Build the true covariant
   \(\phi_2^2\mathcal G\) completion and test whether the fit/degeneracy
   persists away from FLRW.

### Tier B: useful ablation or covariant-completion targets

4. **O2 and O3:** statistically competitive scalar-dependent curvature-square
   theories, but exact terminal coefficients should be regenerated.
5. **N2:** exact and unusually good for a non-EH high-derivative action; use
   systematic operator ablation rather than treating all six terms as final.
6. **N4:** first remove \(\Box R\) and \(\phi\Box\phi\) redundancies, then replay
   the reduced action.
7. **\(L\#622\) and \(L\#434\):** clean FLRW-GB-equivalent controls for the
   covariant-completion study.

### Tier C: controls, not discovery claims

8. **\(L\#682\):** EH + scalar after cancellation.
9. **\(L\#1038\):** explicit total-derivative control.
10. **\(L\#944\):** scalar kinetic/potential renormalization.

## 9. Minimal follow-up matrix

| Candidate | Re-run current \(k\)/AIC | Exact coefficients | Covariant perturbations | Newtonian/local limit | Operator ablation |
|---|---:|---:|---:|---:|---:|
| O1 | required | available | required | required | useful |
| O2 | required | must regenerate | required | required | useful |
| O3 | required | must regenerate | required | required | useful |
| N1 | required | must regenerate | required | essential | useful |
| N2 | required | available | essential | essential | essential |
| N4 | required | available | essential | essential | essential |
| \(L\#961\) | required | available | essential | essential | covariant completion |
| \(L\#622/434\) | required | available | essential | essential | covariant completion |

## 10. Bottom line

The archive does not support the statement that the globally best
background-fitting model is already compelling new gravity. The strongest
open-search fits cluster near \(\chi^2\simeq1637.93\), but several families
are EH/scalar baselines or contain corrections whose physical activity must be
checked after reduction. Conversely, the cleanest new-physics structure,
\(L\#961\), is not statistically competitive by AIC but is theoretically
interesting because the FLRW filter isolates a compact
\(\phi_2R+\phi_2^2\mathcal G/2\)-equivalent branch.

The most defensible research program is therefore two-track:

\[
\boxed{
\text{O1 for statistical competitiveness}
\qquad+\qquad
\text{N1 and }L\#961\text{ for new-physics structure}.
}
\]

The currently running/pending `frontier6_openonly_aic_v2/v3` Oscar jobs are
not part of this local audit because their complete theory and Solver artifacts
have not yet been pulled into the workspace. Their final structures should be
merged into this document only after completion, structural deduplication, and
recovery of the exact best-fit rows.
