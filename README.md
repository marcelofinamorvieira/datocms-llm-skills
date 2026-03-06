# DatoCMS Skills

Focused DatoCMS skills for content delivery, content management, CLI workflows,
frontend integrations, plugin work, and project setup. This README is the main
guide for the repo.

## Public Skills

- `datocms-cda`: read content with the DatoCMS CDA and GraphQL.
- `datocms-cma`: write records, manage schema, environments, and automation.
- `datocms-cli`: handle CLI workflows such as migrations, environments, and imports.
- `datocms-frontend-integrations`: patch or extend existing frontend integrations.
- `datocms-plugin-builder`: build or modify DatoCMS plugins.
- `datocms-setup`: one-time setup orchestrator for frontend, migrations, onboarding imports, and platform automation.

## Setup Skill Behavior

`datocms-setup` is meant to be called explicitly.

Its host metadata sets `allow_implicit_invocation: false`, so it does not
auto-trigger from a generic request like "install visual editing in my
project". Use `$datocms-setup` when you want the setup wizard to inspect the
repo, choose the right internal recipe, and queue prerequisites automatically.

Examples:

```text
$datocms-setup install visual editing in this project
$datocms-setup set up draft mode and web previews
$datocms-setup add migrations and a release workflow
```

Inside `datocms-setup`, setup work is organized into five internal lanes:

- `frontend-foundation`: `cda-client`, `draft-mode`, `web-previews`, `content-link`, `realtime`, `cache-tags`, `graphql-types`
- `frontend-features`: `responsive-images`, `structured-text`, `video-player`, `site-search`, `seo`, `robots-sitemaps`
- `migrations`: `migrations`, `migration-release-workflow`, `blueprint-sync`, `sandbox-iteration`, `cli-profiles`, `migration-autogenerate`
- `onboarding`: `contentful-import`, `wordpress-import`
- `platform`: `cma-types`, `webhooks`, `build-triggers`

Setup work should be reported as `scaffolded` when placeholders or unresolved
project-specific values remain, and `production-ready` only when those gaps are
gone.

## Install

Each public skill can be installed on its own, but the full public set gives
the smoothest cross-skill routing.

Recommended local development install:

```bash
ln -s /absolute/path/to/repo/skills/datocms-cda <skills-root>/datocms-cda
ln -s /absolute/path/to/repo/skills/datocms-cli <skills-root>/datocms-cli
ln -s /absolute/path/to/repo/skills/datocms-cma <skills-root>/datocms-cma
ln -s /absolute/path/to/repo/skills/datocms-frontend-integrations <skills-root>/datocms-frontend-integrations
ln -s /absolute/path/to/repo/skills/datocms-plugin-builder <skills-root>/datocms-plugin-builder
ln -s /absolute/path/to/repo/skills/datocms-setup <skills-root>/datocms-setup
```

If you only need one area, symlink or copy just that skill folder.
`datocms-setup` already contains its internal recipes, shared references, and
recipe-local scripts/assets, so there is no second setup bundle to install.

## Repo Layout

```text
skills/
  datocms-cda/
  datocms-cli/
  datocms-cma/
  datocms-frontend-integrations/
  datocms-plugin-builder/
  datocms-setup/
    agents/
    references/
    recipes/
docs/   # lightweight pointers; keep the root README canonical
evals/  # trigger fixtures, validation scripts, and reports
local/  # optional ignored scratch space
```

## Validate

```bash
python3 evals/scripts/validate_skill_repo.py --repo-root .
python3 evals/scripts/validate_skill_repo.py --repo-root . --require-clean-git
```

For the evaluation workflow details, see [evals/README.md](evals/README.md).
