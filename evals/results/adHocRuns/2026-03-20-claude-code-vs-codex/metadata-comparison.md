# Trigger Eval Comparison

Baseline: `/Users/marcelofinamorvieira/datoCMS/skills/evals/results/adHocRuns/2026-03-20-codex-metadata-refresh/analysis.json`
Candidate: `/Users/marcelofinamorvieira/datoCMS/skills/evals/results/adHocRuns/2026-03-20-claude-code-metadata-refresh/analysis.json`

Overall reported pass: 183/192 (95.3%) -> 184/192 (95.8%) (+0.5%)
Overall recall / precision / F1: 93.2%/99.1%/96.1% -> 99.2%/94.4%/96.7%

## Overall By Query Mode

| Query Mode | Total Δ | Pass Δ | Recall Δ | Precision Δ | F1 Δ |
|---|---:|---:|---:|---:|---:|
| implicit | +0 | +1.9% | +4.3% | 0.0% | +2.2% |
| explicit | +0 | -9.7% | 0.0% | -10.3% | -5.6% |
| overlap | +0 | +21.7% | +23.8% | 0.0% | +14.2% |

| Skill | Pass Δ | Recall Δ | Precision Δ | F1 Δ | FN Δ | FP Δ |
|---|---:|---:|---:|---:|---:|---:|
| datocms-cda | +9.1% | +18.2% | 0.0% | +10.0% | -2 | +0 |
| datocms-cli | +7.4% | +11.8% | +0.7% | +6.2% | -2 | +0 |
| datocms-cma | 0.0% | 0.0% | 0.0% | 0.0% | +0 | +0 |
| datocms-frontend-integrations | +8.7% | +14.3% | 0.0% | +7.7% | -2 | +0 |
| datocms-plugin-builder | 0.0% | +11.1% | -10.0% | +0.6% | -1 | +1 |
| datocms-plugin-design-system | 0.0% | 0.0% | 0.0% | 0.0% | +0 | +0 |
| datocms-plugin-scaffold | 0.0% | 0.0% | 0.0% | 0.0% | +0 | +0 |
| datocms-setup | -8.5% | 0.0% | -10.9% | -5.7% | +0 | +5 |

## Query-Level Improvements

- `datocms-cda` [overlap] rate 0.000 -> 1.000: I need to render structured text from DatoCMS that contains inline records and block records. The structured text has embedded 'call to action' blocks and li...
- `datocms-cda` [overlap] rate 0.000 -> 1.000: my datocms images are loading slow. i heard there's some responsive image stuff with srcset and blur-up placeholders? im using react-datocms. can you help me...
- `datocms-cli` rate 0.000 -> 1.000: can you help me write a migration script that creates a new block model for an 'image gallery' with images (gallery field) and caption (string), then adds it...
- `datocms-cli` rate 0.000 -> 1.000: i need to write a migration that renames a field from 'author_name' to 'author' on my blog_post model, and also changes its field type from single-line strin...
- `datocms-frontend-integrations` [overlap] rate 0.000 -> 1.000: I need to set up draft mode for my Next.js App Router site with DatoCMS. I want enable/disable route handlers, a dual-token executeQuery wrapper, and the coo...
- `datocms-frontend-integrations` [overlap] rate 0.000 -> 1.000: I'm building a Nuxt 3 site with DatoCMS and I need to set up the Web Previews plugin integration. Editors should be able to click 'Open preview' in the CMS a...
- `datocms-plugin-builder` [overlap] rate 0.000 -> 1.000: Patch this existing DatoCMS plugin settings page and make the updated UI feel native to DatoCMS while keeping the behavior the same.

## Query-Level Regressions

- `datocms-plugin-builder` [explicit] rate 0.000 -> 1.000: Use datocms-plugin-builder to scaffold a brand-new DatoCMS plugin project with a config screen and starter files.
- `datocms-setup` [explicit] rate 0.000 -> 1.000: Use datocms-setup to add one more itemFormDropdownActions entry to our existing DatoCMS plugin and leave the current UI alone.
- `datocms-setup` [explicit] rate 0.000 -> 1.000: Use datocms-setup to build the React site-search UI against the existing public search endpoint and current indexes only.
- `datocms-setup` [explicit] rate 0.000 -> 1.000: Use datocms-setup to patch my existing preview-links route handler only and keep the rest of the setup untouched.
- `datocms-setup` [explicit] rate 0.000 -> 1.000: Use datocms-setup to patch one missing ContentLink boundary in the existing Structured Text renderer and leave the rest of the visual editing setup untouched.
- `datocms-setup` [explicit] rate 0.000 -> 1.000: Use datocms-setup to wire a ContentLink component into my existing Next.js page and patch the current renderer only.
