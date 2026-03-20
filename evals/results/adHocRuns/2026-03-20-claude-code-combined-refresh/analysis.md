# Trigger Eval Analysis

Generated at: 2026-03-20T15:01:34.796228+00:00
Threshold: `0.5`

Overall: 183/192 reported-pass (95.3%), precision 94.3%, recall 98.3%, F1 96.3%.

## Overall By Query Mode

| Query Mode | Total | Reported Pass | Precision | Recall | F1 | Unstable |
|---|---:|---:|---:|---:|---:|---:|
| implicit | 107 | 106/107 (99.1%) | 97.9% | 100.0% | 98.9% | 0 |
| explicit | 62 | 57/62 (91.9%) | 90.9% | 100.0% | 95.2% | 0 |
| overlap | 23 | 20/23 (87.0%) | 95.0% | 90.5% | 92.7% | 0 |

| Skill | Reported Pass | Precision | Recall | F1 | FN | FP | Unstable |
|---|---:|---:|---:|---:|---:|---:|---:|
| datocms-cda | 20/22 (90.9%) | 84.6% | 100.0% | 91.7% | 0 | 2 | 0 |
| datocms-cli | 26/27 (96.3%) | 94.4% | 100.0% | 97.1% | 0 | 1 | 0 |
| datocms-cma | 21/21 (100.0%) | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 |
| datocms-frontend-integrations | 21/23 (91.3%) | 100.0% | 85.7% | 92.3% | 2 | 0 | 0 |
| datocms-plugin-builder | 14/14 (100.0%) | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 |
| datocms-plugin-design-system | 14/14 (100.0%) | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 |
| datocms-plugin-scaffold | 12/12 (100.0%) | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 |
| datocms-setup | 55/59 (93.2%) | 91.1% | 100.0% | 95.3% | 0 | 4 | 0 |

## Skill Mode Breakdown

### datocms-cda

| Query Mode | Total | Reported Pass | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| implicit | 14 | 13/14 (92.9%) | 83.3% | 100.0% | 90.9% |
| explicit | 3 | 3/3 (100.0%) | 100.0% | 100.0% | 100.0% |
| overlap | 5 | 4/5 (80.0%) | 80.0% | 100.0% | 88.9% |

### datocms-cli

| Query Mode | Total | Reported Pass | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| implicit | 22 | 22/22 (100.0%) | 100.0% | 100.0% | 100.0% |
| explicit | 3 | 2/3 (66.7%) | 66.7% | 100.0% | 80.0% |
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
| implicit | 15 | 15/15 (100.0%) | 100.0% | 100.0% | 100.0% |
| explicit | 3 | 3/3 (100.0%) | 100.0% | 100.0% | 100.0% |
| overlap | 5 | 3/5 (60.0%) | 100.0% | 60.0% | 75.0% |

### datocms-plugin-builder

| Query Mode | Total | Reported Pass | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| implicit | 10 | 10/10 (100.0%) | 100.0% | 100.0% | 100.0% |
| explicit | 3 | 3/3 (100.0%) | 100.0% | 100.0% | 100.0% |
| overlap | 1 | 1/1 (100.0%) | 100.0% | 100.0% | 100.0% |

### datocms-plugin-design-system

| Query Mode | Total | Reported Pass | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| implicit | 8 | 8/8 (100.0%) | 100.0% | 100.0% | 100.0% |
| explicit | 3 | 3/3 (100.0%) | 100.0% | 100.0% | 100.0% |
| overlap | 3 | 3/3 (100.0%) | 100.0% | 100.0% | 100.0% |

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
