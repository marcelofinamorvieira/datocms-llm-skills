# Setup Router

Use this file to choose the right internal recipe bundle without loading the
entire setup tree.

## Targeted Mode

If the user clearly asks for one of these outcomes, load only that recipe plus
its prerequisites from `recipe-manifest.json`:

| Group | Recipe ids | Typical user intents |
|---|---|---|
| `frontend-foundation` | `cda-client`, `draft-mode`, `web-previews`, `content-link`, `realtime`, `cache-tags`, `graphql-types` | query baseline, previews, visual editing, live preview, cache invalidation, typed queries |
| `frontend-features` | `responsive-images`, `structured-text`, `video-player`, `site-search`, `seo`, `robots-sitemaps` | media rendering, rich text, search, metadata, sitemap wiring |
| `migrations` | `migrations`, `migration-release-workflow`, `blueprint-sync`, `sandbox-iteration`, `cli-profiles`, `migration-autogenerate` | schema workflow, promotion, shared history, sandbox reset, profiles, diff-based generation |
| `onboarding` | `contentful-import`, `wordpress-import` | one-shot import helpers |
| `platform` | `cma-types`, `webhooks`, `build-triggers` | schema types, webhook sync, build trigger management |

## Discovery Mode

Use discovery mode only when the user asks for broad setup such as “set up
DatoCMS for this project” or mixes several unrelated setup goals.

Ask one compact grouped clarification pass that covers:

1. Which setup lane they want first: frontend foundation, frontend features, migrations, onboarding, or platform.
2. Whether they need published-only reads or preview/editor workflows.
3. Whether imports, schema workflows, or platform automation are in scope right now.

Then select the smallest recipe bundle that satisfies the answer set.

## Prerequisite Rules

- Queue `draft-mode` before `web-previews`, `content-link`, `realtime`, or `cache-tags` when that foundation is missing.
- Queue `migrations` before `migration-release-workflow`, `blueprint-sync`, `sandbox-iteration`, or `migration-autogenerate` when that baseline is missing.
- Dedupe shared foundations across the bundle and apply them once.

## Bundle Rules

- Prefer one run with queued prerequisites over telling the user to run another setup skill.
- Keep follow-up suggestions inside `datocms-setup` and refer to recipe ids only.
- Load recipe-local assets and scripts only for the selected recipes.
