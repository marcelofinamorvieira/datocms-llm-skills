# Trigger Eval Comparison

Baseline: `evals/results/adHocRuns/2026-03-06-frontmatter-refresh/analysis.json`
Candidate: `evals/results/adHocRuns/2026-03-06-frontmatter-rerun-current/analysis.json`

Overall reported pass: 119/125 (95.2%) -> 122/125 (97.6%) (+2.4%)
Overall recall / precision / F1: 92.9%/98.5%/95.6% -> 95.7%/100.0%/97.8%

## Overall By Query Mode

| Query Mode | Total Δ | Pass Δ | Recall Δ | Precision Δ | F1 Δ |
|---|---:|---:|---:|---:|---:|
| implicit | +0 | +3.3% | +5.3% | +2.7% | +4.0% |
| explicit | +0 | 0.0% | 0.0% | 0.0% | 0.0% |
| overlap | +0 | 0.0% | 0.0% | 0.0% | 0.0% |

| Skill | Pass Δ | Recall Δ | Precision Δ | F1 Δ | FN Δ | FP Δ |
|---|---:|---:|---:|---:|---:|---:|
| datocms-cda | 0.0% | 0.0% | 0.0% | 0.0% | +0 | +0 |
| datocms-cli | 0.0% | 0.0% | 0.0% | 0.0% | +0 | +0 |
| datocms-cma | 0.0% | 0.0% | 0.0% | 0.0% | +0 | +0 |
| datocms-frontend-integrations | +11.1% | +20.0% | 0.0% | +15.7% | -2 | +0 |
| datocms-plugin-builder | 0.0% | 0.0% | 0.0% | 0.0% | +0 | +0 |
| datocms-setup | +2.9% | 0.0% | +4.0% | +2.0% | +0 | -1 |

## Query-Level Improvements

- `datocms-frontend-integrations` rate 0.000 -> 1.000: Can you help me set up Content Link for my SvelteKit site? I want editors in draft mode to be able to click on content elements and jump directly to the corr...
- `datocms-frontend-integrations` rate 0.000 -> 1.000: I need real-time content updates on my Astro site when in draft mode. When an editor changes content in DatoCMS, the preview page should update immediately w...
- `datocms-setup` rate 1.000 -> 0.000: How do I fork my DatoCMS environment, make schema changes via the CMA, and then promote it to primary? I want to do this in a CI pipeline.
