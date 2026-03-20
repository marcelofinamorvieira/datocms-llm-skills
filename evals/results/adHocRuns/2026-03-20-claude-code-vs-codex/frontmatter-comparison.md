# Trigger Eval Comparison

Baseline: `/Users/marcelofinamorvieira/datoCMS/skills/evals/results/adHocRuns/2026-03-20-codex-frontmatter-refresh/analysis.json`
Candidate: `/Users/marcelofinamorvieira/datoCMS/skills/evals/results/adHocRuns/2026-03-20-claude-code-frontmatter-refresh/analysis.json`

Overall reported pass: 189/192 (98.4%) -> 183/192 (95.3%) (-3.1%)
Overall recall / precision / F1: 97.5%/100.0%/98.7% -> 98.3%/94.3%/96.3%

## Overall By Query Mode

| Query Mode | Total Δ | Pass Δ | Recall Δ | Precision Δ | F1 Δ |
|---|---:|---:|---:|---:|---:|
| implicit | +0 | -0.9% | 0.0% | -2.1% | -1.1% |
| explicit | +0 | -8.1% | 0.0% | -9.1% | -4.8% |
| overlap | +0 | 0.0% | +4.8% | -5.0% | +0.4% |

| Skill | Pass Δ | Recall Δ | Precision Δ | F1 Δ | FN Δ | FP Δ |
|---|---:|---:|---:|---:|---:|---:|
| datocms-cda | -9.1% | 0.0% | -15.4% | -8.3% | +0 | +2 |
| datocms-cli | -3.7% | 0.0% | -5.6% | -2.9% | +0 | +1 |
| datocms-cma | 0.0% | 0.0% | 0.0% | 0.0% | +0 | +0 |
| datocms-frontend-integrations | 0.0% | 0.0% | 0.0% | 0.0% | +0 | +0 |
| datocms-plugin-builder | +7.1% | +11.1% | 0.0% | +5.9% | -1 | +0 |
| datocms-plugin-design-system | +7.1% | +12.5% | 0.0% | +6.7% | -1 | +0 |
| datocms-plugin-scaffold | 0.0% | 0.0% | 0.0% | 0.0% | +0 | +0 |
| datocms-setup | -8.5% | -2.4% | -9.1% | -5.9% | +1 | +4 |

## Query-Level Improvements

- `datocms-plugin-builder` [overlap] rate 0.000 -> 1.000: Patch this existing DatoCMS plugin settings page and make the updated UI feel native to DatoCMS while keeping the behavior the same.
- `datocms-plugin-design-system` [overlap] rate 0.000 -> 1.000: Scaffold a new DatoCMS plugin with a config screen and make the initial UI feel native to DatoCMS.

## Query-Level Regressions

- `datocms-setup` [overlap] rate 1.000 -> 0.000: Use datocms-setup to wire granular DatoCMS cache invalidation for this Next.js app with revalidateTag() and persistent tag storage.
- `datocms-cda` rate 0.000 -> 1.000: Help me set up draft mode for my Nuxt 3 site with DatoCMS. I need the enable/disable endpoints and the executeQuery wrapper that switches between published a...
- `datocms-cda` [overlap] rate 0.000 -> 1.000: how do i set up cache tag invalidation for my DatoCMS next.js site? when content changes i want to revalidate only the affected pages, not the whole site
- `datocms-cli` [explicit] rate 0.000 -> 1.000: Use datocms-cli to write a DatoCMS CMA script that imports 300 products from CSV and uploads their images.
- `datocms-setup` [explicit] rate 0.000 -> 1.000: Use datocms-setup to build the React site-search UI against the existing public search endpoint and current indexes only.
- `datocms-setup` [explicit] rate 0.000 -> 1.000: Use datocms-setup to patch my existing preview-links route handler only and keep the rest of the setup untouched.
- `datocms-setup` [explicit] rate 0.000 -> 1.000: Use datocms-setup to patch one missing ContentLink boundary in the existing Structured Text renderer and leave the rest of the visual editing setup untouched.
- `datocms-setup` [explicit] rate 0.000 -> 1.000: Use datocms-setup to wire a ContentLink component into my existing Next.js page and patch the current renderer only.
