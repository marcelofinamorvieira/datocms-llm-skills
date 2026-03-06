# Trigger Eval Analysis

Generated at: 2026-03-06T13:48:19.446929+00:00
Threshold: `0.5`

Overall: 51/91 reported-pass (56.0%), precision 100.0%, recall 13.0%, F1 23.1%.

| Skill | Reported Pass | Precision | Recall | F1 | FN | FP | Unstable |
|---|---:|---:|---:|---:|---:|---:|---:|
| datocms-cda | 11/19 (57.9%) | 100.0% | 11.1% | 20.0% | 8 | 0 | 3 |
| datocms-cli | 9/18 (50.0%) | 0.0% | 0.0% | 0.0% | 9 | 0 | 5 |
| datocms-cma | 10/18 (55.6%) | 100.0% | 11.1% | 20.0% | 8 | 0 | 5 |
| datocms-frontend-integrations | 10/18 (55.6%) | 100.0% | 20.0% | 33.3% | 8 | 0 | 4 |
| datocms-plugin-builder | 11/18 (61.1%) | 100.0% | 22.2% | 36.4% | 7 | 0 | 4 |

## Highest-Impact False Negatives

- `datocms-cda` rate=0.000: I need to pull all blog posts from my DatoCMS project and display them on my Next.js site. They have a title, slug, cover image, and a rich text body. Can you write the GraphQL ...
- `datocms-cda` rate=0.000: my datocms images are loading slow. i heard there's some responsive image stuff with srcset and blur-up placeholders? im using react-datocms. can you help me set up the image co...
- `datocms-cda` rate=0.000: We have a multilingual DatoCMS site (English, French, German). I need to query the CDA with locale fallbacks so that if a field isn't translated to French it falls back to Engli...
- `datocms-cda` rate=0.000: Can you help me set up the SEO meta tags from DatoCMS? I need to query the _seoMetaTags field and the site favicon, then render them in my Next.js app's head/metadata.
- `datocms-cda` rate=0.000: I want to paginate through a collection of 500+ articles from DatoCMS CDA. What's the right way to do cursor-based pagination with the GraphQL API? I need to show 12 per page wi...
- `datocms-cda` rate=0.000: how do I query datocms to get all records that match a full-text search? the user types in a search bar and i need to search across title and body fields
- `datocms-cli` rate=0.000: I want to import our WordPress blog content into DatoCMS. We have about 400 posts with featured images and categories. Can you walk me through using the datocms CLI import command?
- `datocms-cli` rate=0.000: I want to toggle maintenance mode on my DatoCMS project using the CLI before running a big migration, then turn it off when done. How does that work?
- `datocms-cli` rate=0.000: can you help me write a migration script that creates a new block model for an 'image gallery' with images (gallery field) and caption (string), then adds it as an allowed block...
- `datocms-cli` rate=0.000: We're moving from Contentful to DatoCMS. The CLI has an import command for Contentful, right? How do I export from Contentful and import everything including assets and content ...
