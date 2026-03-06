# Trigger Eval Analysis

Generated at: 2026-03-06T15:59:03.395683+00:00
Threshold: `0.5`

Overall: 122/125 reported-pass (97.6%), precision 100.0%, recall 95.7%, F1 97.8%.

## Overall By Query Mode

| Query Mode | Total | Reported Pass | Precision | Recall | F1 | Unstable |
|---|---:|---:|---:|---:|---:|---:|
| implicit | 92 | 92/92 (100.0%) | 100.0% | 100.0% | 100.0% | 0 |
| explicit | 24 | 24/24 (100.0%) | 100.0% | 100.0% | 100.0% | 0 |
| overlap | 9 | 6/9 (66.7%) | 100.0% | 62.5% | 76.9% | 0 |

| Skill | Reported Pass | Precision | Recall | F1 | FN | FP | Unstable |
|---|---:|---:|---:|---:|---:|---:|---:|
| datocms-cda | 19/19 (100.0%) | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 |
| datocms-cli | 18/18 (100.0%) | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 |
| datocms-cma | 18/18 (100.0%) | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 |
| datocms-frontend-integrations | 15/18 (83.3%) | 100.0% | 70.0% | 82.4% | 3 | 0 | 0 |
| datocms-plugin-builder | 18/18 (100.0%) | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 |
| datocms-setup | 34/34 (100.0%) | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 |

## Skill Mode Breakdown

### datocms-cda

| Query Mode | Total | Reported Pass | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| implicit | 14 | 14/14 (100.0%) | 100.0% | 100.0% | 100.0% |
| overlap | 5 | 5/5 (100.0%) | 100.0% | 100.0% | 100.0% |

### datocms-cma

| Query Mode | Total | Reported Pass | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| implicit | 17 | 17/17 (100.0%) | 100.0% | 100.0% | 100.0% |
| overlap | 1 | 1/1 (100.0%) | 100.0% | 100.0% | 100.0% |

### datocms-frontend-integrations

| Query Mode | Total | Reported Pass | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| implicit | 15 | 15/15 (100.0%) | 100.0% | 100.0% | 100.0% |
| overlap | 3 | 0/3 (0.0%) | 0.0% | 0.0% | 0.0% |

### datocms-setup

| Query Mode | Total | Reported Pass | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| implicit | 10 | 10/10 (100.0%) | 0.0% | 0.0% | 0.0% |
| explicit | 24 | 24/24 (100.0%) | 100.0% | 100.0% | 100.0% |

## Highest-Impact False Negatives

- `datocms-frontend-integrations` [overlap] rate=0.000: I need to set up draft mode for my Next.js App Router site with DatoCMS. I want enable/disable route handlers, a dual-token executeQuery wrapper, and the cookie-based draft dete...
- `datocms-frontend-integrations` [overlap] rate=0.000: I'm building a Nuxt 3 site with DatoCMS and I need to set up the Web Previews plugin integration. Editors should be able to click 'Open preview' in the CMS and see the draft pag...
- `datocms-frontend-integrations` [overlap] rate=0.000: How do I set up cache tag invalidation for my Next.js site with DatoCMS? I want granular revalidation so when a blog post changes, only that page gets revalidated, not the entir...
