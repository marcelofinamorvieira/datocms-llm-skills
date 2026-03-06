# Trigger Eval Reports

This folder contains model-specific trigger-eval snapshots.

## 1) Claude Code Eval (existing run set)

Date analyzed: **March 5, 2026**  
Source raw files: `evals/results/*.json`  
Snapshot copy: `evals/reports/claude-code-2026-03-05/raw/*.json`  
Note: this snapshot is derived from the existing Claude run files already present in the repo.
Analysis outputs:
- `evals/reports/claude-code-2026-03-05/analysis.md`
- `evals/reports/claude-code-2026-03-05/analysis.json`

Aggregate:
- Total: `91`
- Passed: `51` (`56.0%`)
- Precision: `100.0%`
- Recall: `13.0%`
- F1: `23.1%`
- Coverage manifest: `evals/results/manifest.json`
- Explicitly excluded from this published snapshot: `datocms-setup`

Per skill:
- `datocms-cda`: `11/19` (`57.9%`), recall `11.1%`
- `datocms-cli`: `9/18` (`50.0%`), recall `0.0%`
- `datocms-cma`: `10/18` (`55.6%`), recall `11.1%`
- `datocms-frontend-integrations`: `10/18` (`55.6%`), recall `20.0%`
- `datocms-plugin-builder`: `11/18` (`61.1%`), recall `22.2%`

## 2) Codex Eval (baseline vs candidate)

Date run: **March 5, 2026**

The Codex eval used `evals/scripts/run_codex_trigger_eval.py` to classify each eval prompt directly from frontmatter descriptions.

Baseline (before description updates):
- Raw files: `evals/reports/codex-2026-03-05/baseline/*.json`
- Analysis: `evals/reports/codex-2026-03-05/baseline/analysis.md`
- Aggregate: `90/91` (`98.9%`), precision `100.0%`, recall `97.8%`, F1 `98.9%`

Candidate (after description updates):
- Raw files: `evals/reports/codex-2026-03-05/candidate/*.json`
- Analysis: `evals/reports/codex-2026-03-05/candidate/analysis.md`
- Aggregate: `91/91` (`100.0%`), precision `100.0%`, recall `100.0%`, F1 `100.0%`

Comparison:
- `evals/reports/codex-2026-03-05/comparison/comparison.md`
- `evals/reports/codex-2026-03-05/comparison/comparison.json`
- Delta: `+1.1%` overall pass (`90/91` -> `91/91`)
- Improved skill: `datocms-frontend-integrations` (`17/18` -> `18/18`)

## Notes on comparability

These are intentionally two separate eval tracks:
- Claude Code track uses the existing Claude-style result files under `evals/results`.
- Codex track uses the local codex-based classification harness.

Because model, prompting, and harness differ, treat cross-model numbers as directional, not strictly apples-to-apples.
