# Trigger Eval Analysis

Generated at: 2026-03-20T14:38:29.311507+00:00
Threshold: `0.5`

Overall: 183/192 reported-pass (95.3%), precision 99.1%, recall 93.2%, F1 96.1%.

## Overall By Query Mode

| Query Mode | Total | Reported Pass | Precision | Recall | F1 | Unstable |
|---|---:|---:|---:|---:|---:|---:|
| implicit | 107 | 105/107 (98.1%) | 100.0% | 95.7% | 97.8% | 0 |
| explicit | 62 | 61/62 (98.4%) | 98.0% | 100.0% | 99.0% | 0 |
| overlap | 23 | 17/23 (73.9%) | 100.0% | 71.4% | 83.3% | 0 |

| Skill | Reported Pass | Precision | Recall | F1 | FN | FP | Unstable |
|---|---:|---:|---:|---:|---:|---:|---:|
| datocms-cda | 20/22 (90.9%) | 100.0% | 81.8% | 90.0% | 2 | 0 | 0 |
| datocms-cli | 24/27 (88.9%) | 93.8% | 88.2% | 90.9% | 2 | 1 | 0 |
| datocms-cma | 21/21 (100.0%) | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 |
| datocms-frontend-integrations | 21/23 (91.3%) | 100.0% | 85.7% | 92.3% | 2 | 0 | 0 |
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
| overlap | 5 | 3/5 (60.0%) | 100.0% | 50.0% | 66.7% |

### datocms-cli

| Query Mode | Total | Reported Pass | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| implicit | 22 | 20/22 (90.9%) | 100.0% | 84.6% | 91.7% |
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

- `datocms-cda` [overlap] rate=0.000: my datocms images are loading slow. i heard there's some responsive image stuff with srcset and blur-up placeholders? im using react-datocms. can you help me set up the image co...
- `datocms-cda` [overlap] rate=0.000: I need to render structured text from DatoCMS that contains inline records and block records. The structured text has embedded 'call to action' blocks and links to other records...
- `datocms-cli` rate=0.000: i need to write a migration that renames a field from 'author_name' to 'author' on my blog_post model, and also changes its field type from single-line string to a link field po...
- `datocms-cli` rate=0.000: can you help me write a migration script that creates a new block model for an 'image gallery' with images (gallery field) and caption (string), then adds it as an allowed block...
- `datocms-frontend-integrations` [overlap] rate=0.000: I need to set up draft mode for my Next.js App Router site with DatoCMS. I want enable/disable route handlers, a dual-token executeQuery wrapper, and the cookie-based draft dete...
- `datocms-frontend-integrations` [overlap] rate=0.000: I'm building a Nuxt 3 site with DatoCMS and I need to set up the Web Previews plugin integration. Editors should be able to click 'Open preview' in the CMS and see the draft pag...
- `datocms-plugin-builder` [overlap] rate=0.000: Patch this existing DatoCMS plugin settings page and make the updated UI feel native to DatoCMS while keeping the behavior the same.
- `datocms-plugin-design-system` [overlap] rate=0.000: Scaffold a new DatoCMS plugin with a config screen and make the initial UI feel native to DatoCMS.
