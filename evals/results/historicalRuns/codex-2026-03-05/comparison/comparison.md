# Trigger Eval Comparison

Baseline: `evals/results/historicalRuns/codex-2026-03-05/baseline/analysis.json`
Candidate: `evals/results/historicalRuns/codex-2026-03-05/candidate/analysis.json`

Overall reported pass: 90/91 (98.9%) -> 91/91 (100.0%) (+1.1%)
Overall recall / precision / F1: 97.8%/100.0%/98.9% -> 100.0%/100.0%/100.0%

## Overall By Query Mode

| Query Mode | Total Δ | Pass Δ | Recall Δ | Precision Δ | F1 Δ |
|---|---:|---:|---:|---:|---:|
| implicit | +0 | +1.1% | +2.2% | 0.0% | +1.1% |

| Skill | Pass Δ | Recall Δ | Precision Δ | F1 Δ | FN Δ | FP Δ |
|---|---:|---:|---:|---:|---:|---:|
| datocms-cda | 0.0% | 0.0% | 0.0% | 0.0% | +0 | +0 |
| datocms-cli | 0.0% | 0.0% | 0.0% | 0.0% | +0 | +0 |
| datocms-cma | 0.0% | 0.0% | 0.0% | 0.0% | +0 | +0 |
| datocms-frontend-integrations | +5.6% | +10.0% | 0.0% | +5.3% | -1 | +0 |
| datocms-plugin-builder | 0.0% | 0.0% | 0.0% | 0.0% | +0 | +0 |

## Query-Level Improvements

- `datocms-frontend-integrations` rate 0.000 -> 1.000: How do I set up cache tag invalidation for my Next.js site with DatoCMS? I want granular revalidation so when a blog post changes, only that page gets revali...
