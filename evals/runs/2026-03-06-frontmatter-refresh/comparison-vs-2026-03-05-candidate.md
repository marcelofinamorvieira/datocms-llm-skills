# Trigger Eval Comparison

Baseline: `evals/reports/codex-2026-03-05/candidate/analysis.json`
Candidate: `evals/runs/2026-03-06-frontmatter-refresh/analysis.json`

Overall reported pass: 91/91 (100.0%) -> 119/125 (95.2%) (-4.8%)
Overall recall / precision / F1: 100.0%/100.0%/100.0% -> 92.9%/98.5%/95.6%

| Skill | Pass Δ | Recall Δ | Precision Δ | F1 Δ | FN Δ | FP Δ |
|---|---:|---:|---:|---:|---:|---:|
| datocms-cda | 0.0% | 0.0% | 0.0% | 0.0% | +0 | +0 |
| datocms-cli | 0.0% | 0.0% | 0.0% | 0.0% | +0 | +0 |
| datocms-cma | 0.0% | 0.0% | 0.0% | 0.0% | +0 | +0 |
| datocms-frontend-integrations | -27.8% | -50.0% | 0.0% | -33.3% | +5 | +0 |
| datocms-plugin-builder | 0.0% | 0.0% | 0.0% | 0.0% | +0 | +0 |

## Query-Level Regressions

- `datocms-frontend-integrations` rate 1.000 -> 0.000: Can you help me set up Content Link for my SvelteKit site? I want editors in draft mode to be able to click on content elements and jump directly to the corr...
- `datocms-frontend-integrations` [overlap] rate 1.000 -> 0.000: How do I set up cache tag invalidation for my Next.js site with DatoCMS? I want granular revalidation so when a blog post changes, only that page gets revali...
- `datocms-frontend-integrations` rate 1.000 -> 0.000: I need real-time content updates on my Astro site when in draft mode. When an editor changes content in DatoCMS, the preview page should update immediately w...
- `datocms-frontend-integrations` [overlap] rate 1.000 -> 0.000: I need to set up draft mode for my Next.js App Router site with DatoCMS. I want enable/disable route handlers, a dual-token executeQuery wrapper, and the coo...
- `datocms-frontend-integrations` [overlap] rate 1.000 -> 0.000: I'm building a Nuxt 3 site with DatoCMS and I need to set up the Web Previews plugin integration. Editors should be able to click 'Open preview' in the CMS a...
