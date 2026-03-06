# Trigger Eval Analysis

Generated at: 2026-03-06T15:59:03.390948+00:00
Threshold: `0.5`

Overall: 12/18 reported-pass (66.7%), precision 100.0%, recall 40.0%, F1 57.1%.

## Overall By Query Mode

| Query Mode | Total | Reported Pass | Precision | Recall | F1 | Unstable |
|---|---:|---:|---:|---:|---:|---:|
| implicit | 15 | 12/15 (80.0%) | 100.0% | 57.1% | 72.7% | 0 |
| overlap | 3 | 0/3 (0.0%) | 0.0% | 0.0% | 0.0% | 0 |

| Skill | Reported Pass | Precision | Recall | F1 | FN | FP | Unstable |
|---|---:|---:|---:|---:|---:|---:|---:|
| datocms-frontend-integrations | 12/18 (66.7%) | 100.0% | 40.0% | 57.1% | 6 | 0 | 0 |

## Skill Mode Breakdown

### datocms-frontend-integrations

| Query Mode | Total | Reported Pass | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| implicit | 15 | 12/15 (80.0%) | 100.0% | 57.1% | 72.7% |
| overlap | 3 | 0/3 (0.0%) | 0.0% | 0.0% | 0.0% |

## Highest-Impact False Negatives

- `datocms-frontend-integrations` [overlap] rate=0.000: I need to set up draft mode for my Next.js App Router site with DatoCMS. I want enable/disable route handlers, a dual-token executeQuery wrapper, and the cookie-based draft dete...
- `datocms-frontend-integrations` [overlap] rate=0.000: I'm building a Nuxt 3 site with DatoCMS and I need to set up the Web Previews plugin integration. Editors should be able to click 'Open preview' in the CMS and see the draft pag...
- `datocms-frontend-integrations` rate=0.000: Can you help me set up Content Link for my SvelteKit site? I want editors in draft mode to be able to click on content elements and jump directly to the corresponding record in ...
- `datocms-frontend-integrations` rate=0.000: I need real-time content updates on my Astro site when in draft mode. When an editor changes content in DatoCMS, the preview page should update immediately without a page refres...
- `datocms-frontend-integrations` rate=0.000: Setting up my Astro site with DatoCMS. I need the executeQuery helper to fetch content, and I want to handle both published and draft content based on whether draft mode is acti...
- `datocms-frontend-integrations` [overlap] rate=0.000: How do I set up cache tag invalidation for my Next.js site with DatoCMS? I want granular revalidation so when a blog post changes, only that page gets revalidated, not the entir...
