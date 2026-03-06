# Trigger Eval Analysis

Generated at: 2026-03-06T15:59:03.391201+00:00
Threshold: `0.5`

Overall: 90/91 reported-pass (98.9%), precision 100.0%, recall 97.8%, F1 98.9%.

| Skill | Reported Pass | Precision | Recall | F1 | FN | FP | Unstable |
|---|---:|---:|---:|---:|---:|---:|---:|
| datocms-cda | 19/19 (100.0%) | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 |
| datocms-cli | 18/18 (100.0%) | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 |
| datocms-cma | 18/18 (100.0%) | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 |
| datocms-frontend-integrations | 17/18 (94.4%) | 100.0% | 90.0% | 94.7% | 1 | 0 | 0 |
| datocms-plugin-builder | 18/18 (100.0%) | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 |

## Highest-Impact False Negatives

- `datocms-frontend-integrations` rate=0.000: How do I set up cache tag invalidation for my Next.js site with DatoCMS? I want granular revalidation so when a blog post changes, only that page gets revalidated, not the entir...
