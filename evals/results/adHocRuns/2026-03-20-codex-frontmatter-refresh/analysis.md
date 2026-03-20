# Trigger Eval Analysis

Generated at: 2026-03-20T14:27:00.588127+00:00
Threshold: `0.5`

Overall: 189/192 reported-pass (98.4%), precision 100.0%, recall 97.5%, F1 98.7%.

## Overall By Query Mode

| Query Mode | Total | Reported Pass | Precision | Recall | F1 | Unstable |
|---|---:|---:|---:|---:|---:|---:|
| implicit | 107 | 107/107 (100.0%) | 100.0% | 100.0% | 100.0% | 0 |
| explicit | 62 | 62/62 (100.0%) | 100.0% | 100.0% | 100.0% | 0 |
| overlap | 23 | 20/23 (87.0%) | 100.0% | 85.7% | 92.3% | 0 |

| Skill | Reported Pass | Precision | Recall | F1 | FN | FP | Unstable |
|---|---:|---:|---:|---:|---:|---:|---:|
| datocms-cda | 22/22 (100.0%) | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 |
| datocms-cli | 27/27 (100.0%) | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 |
| datocms-cma | 21/21 (100.0%) | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 |
| datocms-frontend-integrations | 22/23 (95.7%) | 100.0% | 92.9% | 96.3% | 1 | 0 | 0 |
| datocms-plugin-builder | 13/14 (92.9%) | 100.0% | 88.9% | 94.1% | 1 | 0 | 0 |
| datocms-plugin-design-system | 13/14 (92.9%) | 100.0% | 87.5% | 93.3% | 1 | 0 | 0 |
| datocms-plugin-scaffold | 12/12 (100.0%) | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 |
| datocms-setup | 59/59 (100.0%) | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 |

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
| implicit | 15 | 15/15 (100.0%) | 100.0% | 100.0% | 100.0% |
| explicit | 3 | 3/3 (100.0%) | 100.0% | 100.0% | 100.0% |
| overlap | 5 | 4/5 (80.0%) | 100.0% | 80.0% | 88.9% |

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
| explicit | 41 | 41/41 (100.0%) | 100.0% | 100.0% | 100.0% |
| overlap | 5 | 5/5 (100.0%) | 100.0% | 100.0% | 100.0% |

## Highest-Impact False Negatives

- `datocms-frontend-integrations` [overlap] rate=0.000: I need to set up draft mode for my Next.js App Router site with DatoCMS. I want enable/disable route handlers, a dual-token executeQuery wrapper, and the cookie-based draft dete...
- `datocms-plugin-builder` [overlap] rate=0.000: Patch this existing DatoCMS plugin settings page and make the updated UI feel native to DatoCMS while keeping the behavior the same.
- `datocms-plugin-design-system` [overlap] rate=0.000: Scaffold a new DatoCMS plugin with a config screen and make the initial UI feel native to DatoCMS.
