# cmp600 vs cmp2000 cheap partial summary

The cheap 2000-target runs are censored at the 72-hour Slurm limit.

The local archive used here contains full memory/proposal JSONL artifacts, but not the remote per-task Solver run directories for the cheap 2000-target campaign.  Therefore the appendix writes the recoverable representative coefficient vectors from local proposal/sample memory; replace these with the corresponding `accepted_samples_summary.csv` rows if the remote run directories are later pulled back.

## Metrics

### flagship-600
- DeepSeek V4 Pro: recorded 600/600, open best 1637.953, open <1650 210, non-EH best 1946.871, non-EH <2000 3.
- GPT-5.5: recorded 600/600, open best 1638.130, open <1650 80, non-EH best 1946.871, non-EH <2000 3.
- Claude Opus 4.8: recorded 600/600, open best 1637.995, open <1650 98, non-EH best 1946.871, non-EH <2000 3.
- Gemini 3.1 Pro: recorded 600/600, open best 1637.969, open <1650 74, non-EH best 2492.845, non-EH <2000 0.
- Qwen 3.7 Plus: recorded 600/600, open best 1638.035, open <1650 29, non-EH best 1946.871, non-EH <2000 9.

### cheap-2000 partial
- DeepSeek V4 Pro: recorded 1633/2000, open best 1637.962, open <1650 196, non-EH best 1693.860, non-EH <2000 27.
- GPT-5.4 Mini: recorded 1621/2000, open best 1637.955, open <1650 278, non-EH best 1942.427, non-EH <2000 12.
- Claude Sonnet 4.6: recorded 1655/2000, open best 1638.014, open <1650 288, non-EH best 1946.871, non-EH <2000 6.
- Gemini 2.5 Flash: recorded 1592/2000, open best 1638.034, open <1650 276, non-EH best 1942.422, non-EH <2000 5.
- Qwen 3.7 Plus: recorded 1541/2000, open best 1637.930, open <1650 191, non-EH best 1896.001, non-EH <2000 3.

## Interesting representatives
- GPT-5.4 Mini open_search: chi2=1637.955, scalar=both, ops=R; R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{fdh}
- GPT-5.4 Mini non_eh: chi2=1942.427, scalar=phi2_only, ops=R^{bcd}_{a} · R^{a}_{bcd}; ∇^{a}∇_{a}R · R^{c}_{c}; φ2 · φ2 · R; φ2 · φ2 · R^{ab} · R_{ab}; φ2 · φ2 · R^{bcd}_{a} · R^{a}_{bcd}; ∇^{a}φ2 · ∇_{a}φ2
- Claude Sonnet 4.6 open_search: chi2=1638.014, scalar=both, ops=R; φ2 · R · R; φ2 · φ2 · φ2 · φ2 · φ2
- Claude Sonnet 4.6 non_eh: chi2=1946.871, scalar=phi2_only, ops=R · R^{ab} · R_{ab}; R_{ab} · R^{adef} · R^{b}_{def}; φ2 · φ2 · R^{ab} · R_{ab}; φ2 · φ2 · R^{bcd}_{a} · R^{a}_{bcd}; φ2 · φ2; φ2 · ∇^{a}∇_{a}φ2; φ2 · φ2 · φ2 · φ2 · φ2; φ2 · φ2 · φ2 · φ2 · φ2 · φ2
- Gemini 2.5 Flash open_search: chi2=1638.034, scalar=phi1_only, ops=R; R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh}
- Gemini 2.5 Flash non_eh: chi2=1942.422, scalar=phi2_only, ops=R^{bcd}_{a} · R^{a}_{bcd}; φ2 · R; φ2 · R^{ab} · R_{ab}; φ2 · R^{bcd}_{a} · R^{a}_{bcd}
- Qwen 3.7 Plus open_search: chi2=1637.930, scalar=phi1_only, ops=R; φ1 · R^{bcd}_{a} · R^{a}_{bcd}; φ1 · φ1 · R^{bcd}_{a} · R^{a}_{bcd}
- Qwen 3.7 Plus non_eh: chi2=1896.001, scalar=phi2_only, ops=∇^{a}∇_{a}R; R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{fdh}; φ2 · φ2 · R; φ2 · R^{ab} · R_{ab}; φ2 · R^{bcd}_{a} · R^{a}_{bcd}; φ2 · ∇^{a}∇_{a}φ2 · R; φ2 · ∇^{a}∇_{a}φ2; φ2 · φ2 · ∇^{a}φ2 · ∇_{a}φ2
- DeepSeek V4 Pro open_search: chi2=1637.962, scalar=phi1_only, ops=R; R^{ab} · R_{ab}; φ1 · φ1 · R^{ab} · R_{ab}
- DeepSeek V4 Pro non_eh: chi2=1693.860, scalar=both, ops=φ2 · φ2 · R; φ1 · ∇^{a}∇_{a}φ1 · φ2; φ1 · ∇^{a}∇_{a}φ1 · φ2 · φ2

## Repeated families
- agents=claude,deepseek,gemini,openai,qwen, best=1637.930, scalar=phi1_only, ops=R; φ1 · φ1 · R · R
- agents=claude,deepseek,gemini,openai,qwen, best=1637.930, scalar=phi1_only, ops=R; φ1 · R^{bcd}_{a} · R^{a}_{bcd}
- agents=claude,deepseek,gemini,openai,qwen, best=1637.937, scalar=phi1_only, ops=R
- agents=claude,deepseek,gemini,openai,qwen, best=1637.950, scalar=both, ops=R
- agents=deepseek,openai, best=1946.871, scalar=phi2_only, ops=φ2 · R^{ab} · R_{ab}; φ2 · R^{bcd}_{a} · R^{a}_{bcd}