# Historical Trigger Eval Snapshots

This folder stores preserved snapshots that are no longer the canonical current result set.

Current accepted results now live in `evals/results/`.
Exploratory reruns now live in `evals/results/adHocRuns/`.

## 1) Existing Assistant Snapshot

Date analyzed: **March 5, 2026**  
Historical snapshot folder: `evals/results/historicalRuns/claude-code-2026-03-05/`

Analysis outputs:
- `evals/results/historicalRuns/claude-code-2026-03-05/analysis.md`
- `evals/results/historicalRuns/claude-code-2026-03-05/analysis.json`

Aggregate:
- Total: `91`
- Passed: `51` (`56.0%`)
- Precision: `100.0%`
- Recall: `13.0%`
- F1: `23.1%`
- Coverage manifest at the time: `evals/results/historicalRuns/claude-code-2026-03-05/manifest.json`
- Explicitly excluded from that published snapshot: `datocms-setup`

## 2) Local Classifier Snapshot

Date run: **March 5, 2026**

Baseline (before description updates):
- Raw files: `evals/results/historicalRuns/codex-2026-03-05/baseline/*.json`
- Analysis: `evals/results/historicalRuns/codex-2026-03-05/baseline/analysis.md`
- Aggregate: `90/91` (`98.9%`), precision `100.0%`, recall `97.8%`, F1 `98.9%`

Candidate (after description updates):
- Raw files: `evals/results/historicalRuns/codex-2026-03-05/candidate/*.json`
- Analysis: `evals/results/historicalRuns/codex-2026-03-05/candidate/analysis.md`
- Aggregate: `91/91` (`100.0%`), precision `100.0%`, recall `100.0%`, F1 `100.0%`

Comparison:
- `evals/results/historicalRuns/codex-2026-03-05/comparison/comparison.md`
- `evals/results/historicalRuns/codex-2026-03-05/comparison/comparison.json`
- Delta: `+1.1%` overall pass (`90/91` -> `91/91`)

## 3) Archived Published Root Snapshot

Date archived: **March 20, 2026**  
Historical snapshot folder: `evals/results/historicalRuns/published-root-2026-03-20-pre-claude-code-refresh/`

Analysis outputs:
- `evals/results/historicalRuns/published-root-2026-03-20-pre-claude-code-refresh/analysis.md`
- `evals/results/historicalRuns/published-root-2026-03-20-pre-claude-code-refresh/analysis.json`

Aggregate:
- Total: `125`
- Passed: `122` (`97.6%`)
- Precision: `100.0%`
- Recall: `95.7%`
- F1: `97.8%`
- Coverage manifest at the time: `evals/results/historicalRuns/published-root-2026-03-20-pre-claude-code-refresh/manifest.json`

## Notes on comparability

These historical snapshots were produced by different harnesses. Treat cross-snapshot comparisons as directional, not strictly apples-to-apples.
