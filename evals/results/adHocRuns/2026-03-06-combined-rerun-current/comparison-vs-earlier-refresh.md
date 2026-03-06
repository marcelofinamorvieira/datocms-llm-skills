# Trigger Eval Comparison

Baseline: `evals/results/adHocRuns/2026-03-06-combined-refresh/analysis.json`
Candidate: `evals/results/adHocRuns/2026-03-06-combined-rerun-current/analysis.json`

Overall reported pass: 118/125 (94.4%) -> 122/125 (97.6%) (+3.2%)
Overall recall / precision / F1: 90.0%/100.0%/94.7% -> 95.7%/100.0%/97.8%

## Overall By Query Mode

| Query Mode | Total Δ | Pass Δ | Recall Δ | Precision Δ | F1 Δ |
|---|---:|---:|---:|---:|---:|
| implicit | +0 | +2.2% | +5.3% | 0.0% | +2.7% |
| explicit | +0 | 0.0% | 0.0% | 0.0% | 0.0% |
| overlap | +0 | +22.2% | +25.0% | 0.0% | +22.4% |

| Skill | Pass Δ | Recall Δ | Precision Δ | F1 Δ | FN Δ | FP Δ |
|---|---:|---:|---:|---:|---:|---:|
| datocms-cda | +10.5% | +22.2% | 0.0% | +12.5% | -2 | +0 |
| datocms-cli | 0.0% | 0.0% | 0.0% | 0.0% | +0 | +0 |
| datocms-cma | 0.0% | 0.0% | 0.0% | 0.0% | +0 | +0 |
| datocms-frontend-integrations | +11.1% | +20.0% | 0.0% | +15.7% | -2 | +0 |
| datocms-plugin-builder | 0.0% | 0.0% | 0.0% | 0.0% | +0 | +0 |
| datocms-setup | 0.0% | 0.0% | 0.0% | 0.0% | +0 | +0 |

## Query-Level Improvements

- `datocms-cda` [overlap] rate 0.000 -> 1.000: I need to render structured text from DatoCMS that contains inline records and block records. The structured text has embedded 'call to action' blocks and li...
- `datocms-cda` [overlap] rate 0.000 -> 1.000: my datocms images are loading slow. i heard there's some responsive image stuff with srcset and blur-up placeholders? im using react-datocms. can you help me...
- `datocms-frontend-integrations` rate 0.000 -> 1.000: Can you help me set up Content Link for my SvelteKit site? I want editors in draft mode to be able to click on content elements and jump directly to the corr...
- `datocms-frontend-integrations` rate 0.000 -> 1.000: I need real-time content updates on my Astro site when in draft mode. When an editor changes content in DatoCMS, the preview page should update immediately w...
