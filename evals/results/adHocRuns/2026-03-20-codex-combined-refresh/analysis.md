# Trigger Eval Analysis

Generated at: 2026-03-20T14:50:26.635804+00:00
Threshold: `0.5`

Overall: 180/192 reported-pass (93.8%), precision 96.5%, recall 93.2%, F1 94.8%.

## Overall By Query Mode

| Query Mode | Total | Reported Pass | Precision | Recall | F1 | Unstable |
|---|---:|---:|---:|---:|---:|---:|
| implicit | 107 | 104/107 (97.2%) | 100.0% | 93.6% | 96.7% | 0 |
| explicit | 62 | 58/62 (93.5%) | 92.6% | 100.0% | 96.2% | 0 |
| overlap | 23 | 18/23 (78.3%) | 100.0% | 76.2% | 86.5% | 0 |

| Skill | Reported Pass | Precision | Recall | F1 | FN | FP | Unstable |
|---|---:|---:|---:|---:|---:|---:|---:|
| datocms-cda | 22/22 (100.0%) | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 |
| datocms-cli | 27/27 (100.0%) | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 |
| datocms-cma | 21/21 (100.0%) | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 |
| datocms-frontend-integrations | 17/23 (73.9%) | 100.0% | 57.1% | 72.7% | 6 | 0 | 0 |
| datocms-plugin-builder | 13/14 (92.9%) | 100.0% | 88.9% | 94.1% | 1 | 0 | 0 |
| datocms-plugin-design-system | 13/14 (92.9%) | 100.0% | 87.5% | 93.3% | 1 | 0 | 0 |
| datocms-plugin-scaffold | 12/12 (100.0%) | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 |
| datocms-setup | 55/59 (93.2%) | 91.1% | 100.0% | 95.3% | 0 | 4 | 0 |

## Skill Mode Breakdown

### datocms-cda

| Query Mode | Total | Reported Pass | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| implicit | 14 | 14/14 (100.0%) | 100.0% | 100.0% | 100.0% |
| explicit | 3 | 3/3 (100.0%) | 100.0% | 100.0% | 100.0% |
| overlap | 5 | 5/5 (100.0%) | 100.0% | 100.0% | 100.0% |

### datocms-cli

| Query Mode | Total | Reported Pass | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| implicit | 22 | 22/22 (100.0%) | 100.0% | 100.0% | 100.0% |
| explicit | 3 | 3/3 (100.0%) | 100.0% | 100.0% | 100.0% |
| overlap | 2 | 2/2 (100.0%) | 100.0% | 100.0% | 100.0% |

### datocms-cma

| Query Mode | Total | Reported Pass | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| implicit | 17 | 17/17 (100.0%) | 100.0% | 100.0% | 100.0% |
| explicit | 3 | 3/3 (100.0%) | 100.0% | 100.0% | 100.0% |
| overlap | 1 | 1/1 (100.0%) | 100.0% | 100.0% | 100.0% |

### datocms-frontend-integrations

| Query Mode | Total | Reported Pass | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| implicit | 15 | 12/15 (80.0%) | 100.0% | 57.1% | 72.7% |
| explicit | 3 | 3/3 (100.0%) | 100.0% | 100.0% | 100.0% |
| overlap | 5 | 2/5 (40.0%) | 100.0% | 40.0% | 57.1% |

### datocms-plugin-builder

| Query Mode | Total | Reported Pass | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| implicit | 10 | 10/10 (100.0%) | 100.0% | 100.0% | 100.0% |
| explicit | 3 | 3/3 (100.0%) | 100.0% | 100.0% | 100.0% |
| overlap | 1 | 0/1 (0.0%) | 0.0% | 0.0% | 0.0% |

### datocms-plugin-design-system

| Query Mode | Total | Reported Pass | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| implicit | 8 | 8/8 (100.0%) | 100.0% | 100.0% | 100.0% |
| explicit | 3 | 3/3 (100.0%) | 100.0% | 100.0% | 100.0% |
| overlap | 3 | 2/3 (66.7%) | 100.0% | 50.0% | 66.7% |

### datocms-plugin-scaffold

| Query Mode | Total | Reported Pass | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| implicit | 8 | 8/8 (100.0%) | 100.0% | 100.0% | 100.0% |
| explicit | 3 | 3/3 (100.0%) | 100.0% | 100.0% | 100.0% |
| overlap | 1 | 1/1 (100.0%) | 100.0% | 100.0% | 100.0% |

### datocms-setup

| Query Mode | Total | Reported Pass | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| implicit | 13 | 13/13 (100.0%) | 0.0% | 0.0% | 0.0% |
| explicit | 41 | 37/41 (90.2%) | 90.0% | 100.0% | 94.7% |
| overlap | 5 | 5/5 (100.0%) | 100.0% | 100.0% | 100.0% |

## Highest-Impact False Negatives

- `datocms-frontend-integrations` [overlap] rate=0.000: I need to set up draft mode for my Next.js App Router site with DatoCMS. I want enable/disable route handlers, a dual-token executeQuery wrapper, and the cookie-based draft dete...
- `datocms-frontend-integrations` [overlap] rate=0.000: I'm building a Nuxt 3 site with DatoCMS and I need to set up the Web Previews plugin integration. Editors should be able to click 'Open preview' in the CMS and see the draft pag...
- `datocms-frontend-integrations` rate=0.000: Can you help me set up Content Link for my SvelteKit site? I want editors in draft mode to be able to click on content elements and jump directly to the corresponding record in ...
- `datocms-frontend-integrations` rate=0.000: I need real-time content updates on my Astro site when in draft mode. When an editor changes content in DatoCMS, the preview page should update immediately without a page refres...
- `datocms-frontend-integrations` rate=0.000: Setting up my Astro site with DatoCMS. I need the executeQuery helper to fetch content, and I want to handle both published and draft content based on whether draft mode is acti...
- `datocms-frontend-integrations` [overlap] rate=0.000: How do I set up cache tag invalidation for my Next.js site with DatoCMS? I want granular revalidation so when a blog post changes, only that page gets revalidated, not the entir...
- `datocms-plugin-builder` [overlap] rate=0.000: Patch this existing DatoCMS plugin settings page and make the updated UI feel native to DatoCMS while keeping the behavior the same.
- `datocms-plugin-design-system` [overlap] rate=0.000: Scaffold a new DatoCMS plugin with a config screen and make the initial UI feel native to DatoCMS.
