# Trigger Eval Comparison

Baseline: `/Users/marcelofinamorvieira/datoCMS/skills/evals/results/adHocRuns/2026-03-20-codex-combined-refresh/analysis.json`
Candidate: `/Users/marcelofinamorvieira/datoCMS/skills/evals/results/adHocRuns/2026-03-20-claude-code-combined-refresh/analysis.json`

Overall reported pass: 180/192 (93.8%) -> 183/192 (95.3%) (+1.6%)
Overall recall / precision / F1: 93.2%/96.5%/94.8% -> 98.3%/94.3%/96.3%

## Overall By Query Mode

| Query Mode | Total Δ | Pass Δ | Recall Δ | Precision Δ | F1 Δ |
|---|---:|---:|---:|---:|---:|
| implicit | +0 | +1.9% | +6.4% | -2.1% | +2.2% |
| explicit | +0 | -1.6% | 0.0% | -1.7% | -0.9% |
| overlap | +0 | +8.7% | +14.3% | -5.0% | +6.2% |

| Skill | Pass Δ | Recall Δ | Precision Δ | F1 Δ | FN Δ | FP Δ |
|---|---:|---:|---:|---:|---:|---:|
| datocms-cda | -9.1% | 0.0% | -15.4% | -8.3% | +0 | +2 |
| datocms-cli | -3.7% | 0.0% | -5.6% | -2.9% | +0 | +1 |
| datocms-cma | 0.0% | 0.0% | 0.0% | 0.0% | +0 | +0 |
| datocms-frontend-integrations | +17.4% | +28.6% | 0.0% | +19.6% | -4 | +0 |
| datocms-plugin-builder | +7.1% | +11.1% | 0.0% | +5.9% | -1 | +0 |
| datocms-plugin-design-system | +7.1% | +12.5% | 0.0% | +6.7% | -1 | +0 |
| datocms-plugin-scaffold | 0.0% | 0.0% | 0.0% | 0.0% | +0 | +0 |
| datocms-setup | 0.0% | 0.0% | 0.0% | 0.0% | +0 | +0 |

## Query-Level Improvements

- `datocms-frontend-integrations` rate 0.000 -> 1.000: Can you help me set up Content Link for my SvelteKit site? I want editors in draft mode to be able to click on content elements and jump directly to the corr...
- `datocms-frontend-integrations` [overlap] rate 0.000 -> 1.000: How do I set up cache tag invalidation for my Next.js site with DatoCMS? I want granular revalidation so when a blog post changes, only that page gets revali...
- `datocms-frontend-integrations` rate 0.000 -> 1.000: I need real-time content updates on my Astro site when in draft mode. When an editor changes content in DatoCMS, the preview page should update immediately w...
- `datocms-frontend-integrations` rate 0.000 -> 1.000: Setting up my Astro site with DatoCMS. I need the executeQuery helper to fetch content, and I want to handle both published and draft content based on whethe...
- `datocms-plugin-builder` [overlap] rate 0.000 -> 1.000: Patch this existing DatoCMS plugin settings page and make the updated UI feel native to DatoCMS while keeping the behavior the same.
- `datocms-plugin-design-system` [overlap] rate 0.000 -> 1.000: Scaffold a new DatoCMS plugin with a config screen and make the initial UI feel native to DatoCMS.

## Query-Level Regressions

- `datocms-cda` rate 0.000 -> 1.000: Help me set up draft mode for my Nuxt 3 site with DatoCMS. I need the enable/disable endpoints and the executeQuery wrapper that switches between published a...
- `datocms-cda` [overlap] rate 0.000 -> 1.000: how do i set up cache tag invalidation for my DatoCMS next.js site? when content changes i want to revalidate only the affected pages, not the whole site
- `datocms-cli` [explicit] rate 0.000 -> 1.000: Use datocms-cli to write a DatoCMS CMA script that imports 300 products from CSV and uploads their images.
