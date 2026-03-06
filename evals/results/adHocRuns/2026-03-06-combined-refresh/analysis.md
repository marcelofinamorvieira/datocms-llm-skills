# Trigger Eval Analysis

Generated at: 2026-03-06T15:59:03.391912+00:00
Threshold: `0.5`

Overall: 118/125 reported-pass (94.4%), precision 100.0%, recall 90.0%, F1 94.7%.

## Overall By Query Mode

| Query Mode | Total | Reported Pass | Precision | Recall | F1 | Unstable |
|---|---:|---:|---:|---:|---:|---:|
| implicit | 92 | 90/92 (97.8%) | 100.0% | 94.7% | 97.3% | 0 |
| explicit | 24 | 24/24 (100.0%) | 100.0% | 100.0% | 100.0% | 0 |
| overlap | 9 | 4/9 (44.4%) | 100.0% | 37.5% | 54.5% | 0 |

| Skill | Reported Pass | Precision | Recall | F1 | FN | FP | Unstable |
|---|---:|---:|---:|---:|---:|---:|---:|
| datocms-cda | 17/19 (89.5%) | 100.0% | 77.8% | 87.5% | 2 | 0 | 0 |
| datocms-cli | 18/18 (100.0%) | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 |
| datocms-cma | 18/18 (100.0%) | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 |
| datocms-frontend-integrations | 13/18 (72.2%) | 100.0% | 50.0% | 66.7% | 5 | 0 | 0 |
| datocms-plugin-builder | 18/18 (100.0%) | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 |
| datocms-setup | 34/34 (100.0%) | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 |

## Skill Mode Breakdown

### datocms-cda

| Query Mode | Total | Reported Pass | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| implicit | 14 | 14/14 (100.0%) | 100.0% | 100.0% | 100.0% |
| overlap | 5 | 3/5 (60.0%) | 100.0% | 50.0% | 66.7% |

### datocms-cma

| Query Mode | Total | Reported Pass | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| implicit | 17 | 17/17 (100.0%) | 100.0% | 100.0% | 100.0% |
| overlap | 1 | 1/1 (100.0%) | 100.0% | 100.0% | 100.0% |

### datocms-frontend-integrations

| Query Mode | Total | Reported Pass | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| implicit | 15 | 13/15 (86.7%) | 100.0% | 71.4% | 83.3% |
| overlap | 3 | 0/3 (0.0%) | 0.0% | 0.0% | 0.0% |

### datocms-setup

| Query Mode | Total | Reported Pass | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| implicit | 10 | 10/10 (100.0%) | 0.0% | 0.0% | 0.0% |
| explicit | 24 | 24/24 (100.0%) | 100.0% | 100.0% | 100.0% |

## Highest-Impact False Negatives

- `datocms-cda` [overlap] rate=0.000: my datocms images are loading slow. i heard there's some responsive image stuff with srcset and blur-up placeholders? im using react-datocms. can you help me set up the image co...
- `datocms-cda` [overlap] rate=0.000: I need to render structured text from DatoCMS that contains inline records and block records. The structured text has embedded 'call to action' blocks and links to other records...
- `datocms-frontend-integrations` [overlap] rate=0.000: I need to set up draft mode for my Next.js App Router site with DatoCMS. I want enable/disable route handlers, a dual-token executeQuery wrapper, and the cookie-based draft dete...
- `datocms-frontend-integrations` [overlap] rate=0.000: I'm building a Nuxt 3 site with DatoCMS and I need to set up the Web Previews plugin integration. Editors should be able to click 'Open preview' in the CMS and see the draft pag...
- `datocms-frontend-integrations` rate=0.000: Can you help me set up Content Link for my SvelteKit site? I want editors in draft mode to be able to click on content elements and jump directly to the corresponding record in ...
- `datocms-frontend-integrations` rate=0.000: I need real-time content updates on my Astro site when in draft mode. When an editor changes content in DatoCMS, the preview page should update immediately without a page refres...
- `datocms-frontend-integrations` [overlap] rate=0.000: How do I set up cache tag invalidation for my Next.js site with DatoCMS? I want granular revalidation so when a blog post changes, only that page gets revalidated, not the entir...
