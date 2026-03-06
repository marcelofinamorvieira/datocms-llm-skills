# Skill Catalog

The root [README](../README.md#public-skills) is the short version. This page
keeps the fuller catalog and the internal setup matrix.

## Core Skills

| Skill | Repo path | Scope |
|---|---|---|
| `datocms-plugin-builder` | `skills/datocms-plugin-builder` | Build or extend DatoCMS plugins |
| `datocms-cma` | `skills/datocms-cma` | Content management scripts, records, schema, environments, and webhooks |
| `datocms-cli` | `skills/datocms-cli` | CLI workflows, migrations, environments, and imports |
| `datocms-cda` | `skills/datocms-cda` | Content delivery queries, GraphQL reads, media, SEO, and typed queries |
| `datocms-frontend-integrations` | `skills/datocms-frontend-integrations` | Framework integration patterns for draft mode, previews, live updates, rendering, and search |
| `datocms-setup` | `skills/datocms-setup` | One-time setup orchestrator that routes to internal recipes for frontend, migrations, onboarding, and platform work |

## Internal Setup Recipes

`datocms-setup` is the public setup entrypoint. It owns the following internal
recipe groups:

| Group | Internal recipe ids | Notes |
|---|---|---|
| `frontend-foundation` | `cda-client`, `draft-mode`, `web-previews`, `content-link`, `realtime`, `cache-tags`, `graphql-types` | Query baseline, previews, visual editing, live preview, cache invalidation, typed queries |
| `frontend-features` | `responsive-images`, `structured-text`, `video-player`, `site-search`, `seo`, `robots-sitemaps` | Rendering and discovery add-ons layered on top of the foundation |
| `migrations` | `migrations`, `migration-release-workflow`, `blueprint-sync`, `sandbox-iteration`, `cli-profiles`, `migration-autogenerate` | Schema workflow, release, and environment tooling |
| `onboarding` | `contentful-import`, `wordpress-import` | One-shot import helpers |
| `platform` | `cma-types`, `webhooks`, `build-triggers` | Project-level automation and schema tooling |

## Setup Routing Rules

- `draft-mode` is queued automatically before `web-previews`, `content-link`, `realtime`, or `cache-tags` when that foundation is missing.
- `migrations` is queued automatically before `migration-release-workflow`, `blueprint-sync`, `sandbox-iteration`, or `migration-autogenerate` when that baseline is missing.
- The setup skill keeps setup self-contained: shared references, scripts, and assets all live inside `skills/datocms-setup`.
