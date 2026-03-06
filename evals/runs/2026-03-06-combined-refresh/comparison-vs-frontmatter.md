# Trigger Eval Comparison

Baseline: `evals/runs/2026-03-06-frontmatter-refresh/analysis.json`
Candidate: `evals/runs/2026-03-06-combined-refresh/analysis.json`

Overall reported pass: 119/125 (95.2%) -> 118/125 (94.4%) (-0.8%)
Overall recall / precision / F1: 92.9%/98.5%/95.6% -> 90.0%/100.0%/94.7%

## Overall By Query Mode

| Query Mode | Total Δ | Pass Δ | Recall Δ | Precision Δ | F1 Δ |
|---|---:|---:|---:|---:|---:|
| implicit | +0 | +1.1% | 0.0% | +2.7% | +1.3% |
| explicit | +0 | 0.0% | 0.0% | 0.0% | 0.0% |
| overlap | +0 | -22.2% | -25.0% | 0.0% | -22.4% |

| Skill | Pass Δ | Recall Δ | Precision Δ | F1 Δ | FN Δ | FP Δ |
|---|---:|---:|---:|---:|---:|---:|
| datocms-cda | -10.5% | -22.2% | 0.0% | -12.5% | +2 | +0 |
| datocms-cli | 0.0% | 0.0% | 0.0% | 0.0% | +0 | +0 |
| datocms-cma | 0.0% | 0.0% | 0.0% | 0.0% | +0 | +0 |
| datocms-frontend-integrations | 0.0% | 0.0% | 0.0% | 0.0% | +0 | +0 |
| datocms-plugin-builder | 0.0% | 0.0% | 0.0% | 0.0% | +0 | +0 |
| datocms-setup | +2.9% | 0.0% | +4.0% | +2.0% | +0 | -1 |

## Query-Level Improvements

- `datocms-setup` rate 1.000 -> 0.000: How do I fork my DatoCMS environment, make schema changes via the CMA, and then promote it to primary? I want to do this in a CI pipeline.

## Query-Level Regressions

- `datocms-cda` [overlap] rate 1.000 -> 0.000: I need to render structured text from DatoCMS that contains inline records and block records. The structured text has embedded 'call to action' blocks and li...
- `datocms-cda` [overlap] rate 1.000 -> 0.000: my datocms images are loading slow. i heard there's some responsive image stuff with srcset and blur-up placeholders? im using react-datocms. can you help me...
