# Skill Catalog

## Core Skills

| Skill | Repo path | Scope |
|---|---|---|
| `datocms-plugin-builder` | `skills/datocms-plugin-builder` | Build or extend DatoCMS plugins |
| `datocms-cma` | `skills/datocms-cma` | Content management scripts, records, schema, environments, and webhooks |
| `datocms-cli` | `skills/datocms-cli` | CLI workflows, migrations, environments, and imports |
| `datocms-cda` | `skills/datocms-cda` | Content delivery queries, GraphQL reads, media, SEO, and typed queries |
| `datocms-frontend-integrations` | `skills/datocms-frontend-integrations` | Framework integration patterns for draft mode, previews, live updates, rendering, and search |

## Setup Groups

### Frontend Foundation

| Skill | Repo path | Companion skills |
|---|---|---|
| `datocms-setup-draft-mode` | `setup/frontend-foundation/datocms-setup-draft-mode` | `datocms-frontend-integrations` |
| `datocms-setup-web-previews` | `setup/frontend-foundation/datocms-setup-web-previews` | `datocms-frontend-integrations` |
| `datocms-setup-content-link` | `setup/frontend-foundation/datocms-setup-content-link` | `datocms-frontend-integrations` |
| `datocms-setup-realtime` | `setup/frontend-foundation/datocms-setup-realtime` | `datocms-frontend-integrations` |
| `datocms-setup-cache-tags` | `setup/frontend-foundation/datocms-setup-cache-tags` | `datocms-frontend-integrations`, `datocms-cda` |
| `datocms-setup-cda-client` | `setup/frontend-foundation/datocms-setup-cda-client` | `datocms-frontend-integrations`, `datocms-cda` |
| `datocms-setup-graphql-types` | `setup/frontend-foundation/datocms-setup-graphql-types` | `datocms-cda` |

### Frontend Features

| Skill | Repo path | Companion skills |
|---|---|---|
| `datocms-setup-responsive-images` | `setup/frontend-features/datocms-setup-responsive-images` | `datocms-cda`, `datocms-frontend-integrations` |
| `datocms-setup-structured-text` | `setup/frontend-features/datocms-setup-structured-text` | `datocms-cda`, `datocms-frontend-integrations` |
| `datocms-setup-video-player` | `setup/frontend-features/datocms-setup-video-player` | `datocms-cda`, `datocms-frontend-integrations` |
| `datocms-setup-site-search` | `setup/frontend-features/datocms-setup-site-search` | `datocms-frontend-integrations`, `datocms-cma` |
| `datocms-setup-seo` | `setup/frontend-features/datocms-setup-seo` | `datocms-cda`, `datocms-frontend-integrations` |
| `datocms-setup-robots-sitemaps` | `setup/frontend-features/datocms-setup-robots-sitemaps` | `datocms-cda`, `datocms-frontend-integrations` |

### Migrations

| Skill | Repo path | Companion skills |
|---|---|---|
| `datocms-setup-migrations` | `setup/migrations/datocms-setup-migrations` | `datocms-cli` |
| `datocms-setup-migration-release-workflow` | `setup/migrations/datocms-setup-migration-release-workflow` | `datocms-cli` |
| `datocms-setup-blueprint-sync` | `setup/migrations/datocms-setup-blueprint-sync` | `datocms-cli` |
| `datocms-setup-sandbox-iteration` | `setup/migrations/datocms-setup-sandbox-iteration` | `datocms-cli` |
| `datocms-setup-cli-profiles` | `setup/migrations/datocms-setup-cli-profiles` | `datocms-cli` |
| `datocms-setup-migration-autogenerate` | `setup/migrations/datocms-setup-migration-autogenerate` | `datocms-cli` |

### Onboarding

| Skill | Repo path | Companion skills |
|---|---|---|
| `datocms-setup-contentful-import` | `setup/onboarding/datocms-setup-contentful-import` | `datocms-cli` |
| `datocms-setup-wordpress-import` | `setup/onboarding/datocms-setup-wordpress-import` | `datocms-cli` |

### Platform

| Skill | Repo path | Companion skills |
|---|---|---|
| `datocms-setup-cma-types` | `setup/platform/datocms-setup-cma-types` | `datocms-cli`, `datocms-cma` |
| `datocms-setup-webhooks` | `setup/platform/datocms-setup-webhooks` | `datocms-cma`, `datocms-frontend-integrations` |
| `datocms-setup-build-triggers` | `setup/platform/datocms-setup-build-triggers` | `datocms-cma` |

## Setup Prerequisites

- Run `datocms-setup-draft-mode` before `datocms-setup-web-previews`, `datocms-setup-content-link`, `datocms-setup-realtime`, or `datocms-setup-cache-tags`.
- Run `datocms-setup-migrations` before `datocms-setup-migration-release-workflow`, `datocms-setup-blueprint-sync`, `datocms-setup-sandbox-iteration`, or `datocms-setup-migration-autogenerate`.
