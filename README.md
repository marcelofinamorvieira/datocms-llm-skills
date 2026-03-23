# DatoCMS Skills

Focused DatoCMS skills for content delivery, content management, CLI workflows,
frontend integrations, plugin implementation, plugin UI design, and project
setup. This README is the main guide for the repo.

## Public Skills

- `datocms-cda`: read content with the DatoCMS CDA and GraphQL, including media, SEO, and typed query workflows.
- `datocms-cma`: write records, manage schema, environments, uploads, webhooks, and automation.
- `datocms-cli`: handle CLI workflows such as setup/config, migrations, schema generation, direct CMA calls, environments, deployment, multi-project sync, and imports.
- `datocms-frontend-integrations`: patch or extend existing frontend integrations for draft mode, previews, visual editing, rendering, and search.
- `datocms-plugin-builder`: patch and maintain existing DatoCMS plugins.
- `datocms-plugin-design-system`: design or restyle DatoCMS plugins so they feel native to the DatoCMS UI.
- `datocms-plugin-scaffold`: scaffold new DatoCMS plugin projects.
- `datocms-setup`: one-time setup orchestrator for frontend foundation/features, migrations, onboarding imports, and platform automation.

## Setup Skill Behavior

`datocms-setup` is meant to be called explicitly.

Its host metadata sets `allow_implicit_invocation: false`, so it does not
auto-trigger from a generic request like "install visual editing in my
project". Use `$datocms-setup` when you want the setup wizard to inspect the
repo, choose the right internal recipe, and queue prerequisites automatically.

After you call `$datocms-setup`, write the prompt as the outcome you want in
plain language. You do not need to know the internal recipe ids, but using
terms like `content link`, `visual editing`, `click-to-edit`, or `draft mode`
helps the router land on the smallest matching setup bundle.

Examples:

```text
$datocms-setup install visual editing in this project
$datocms-setup set up draft mode and web previews
$datocms-setup add migrations and a release workflow
```

For Content Link specifically, prompts like these are a good fit:

```text
$datocms-setup install content link in this project
$datocms-setup add visual editing to this app
$datocms-setup set up click-to-edit overlays for draft pages
$datocms-setup enable content-link for this repo and wire any missing prerequisites
```

If draft mode is missing, `datocms-setup` should queue that prerequisite in the
same run instead of requiring a second explicit setup call.

Inside `datocms-setup`, setup work is organized into five internal lanes:

- `frontend-foundation`: `cda-client`, `draft-mode`, `web-previews`, `content-link`, `realtime`, `visual-editing`, `cache-tags`, `graphql-types`
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

### Claude Code Plugin (recommended)

This repo ships as a Claude Code plugin. Add the marketplace and install:

```bash
/plugin marketplace add marcelofinamorvieira/datocms-llm-skills
/plugin install datocms@datocms-skills
```

Skills are namespaced under the plugin name (e.g. `/datocms:datocms-cda`).

To test locally during development:

```bash
claude --plugin-dir /path/to/this/repo
```

### Codex

Inside a Codex session, ask the skill installer to pull all skills from this repo:

```
$skill-installer install all of these skills from https://github.com/marcelofinamorvieira/datocms-llm-skills:
- skills/datocms-cda
- skills/datocms-cli
- skills/datocms-cma
- skills/datocms-frontend-integrations
- skills/datocms-plugin-builder
- skills/datocms-plugin-design-system
- skills/datocms-plugin-scaffold
- skills/datocms-setup
```

Restart Codex after installing. Then verify all 8 skills were picked up by
running `ls ~/.codex/skills/ | grep datocms`. You should see all 8 folders
listed. If any are missing, re-run `$skill-installer` for the missing skill
individually.

## Repo Layout

```text
.claude-plugin/
  plugin.json         # Claude Code plugin manifest
  marketplace.json    # Claude Code marketplace registry
skills/
  datocms-cda/
  datocms-cli/
  datocms-cma/
  datocms-frontend-integrations/
  datocms-plugin-builder/
  datocms-plugin-design-system/
  datocms-plugin-scaffold/
  datocms-setup/
    agents/           # Codex agent interface config (openai.yaml)
    patterns/
    references/
    recipes/
docs/   # deeper guides and longer repo notes
evals/
  *.json    # eval fixtures and checked-in result snapshots
  *.md      # eval guides and manual review matrices
  results/  # analyzed outputs and historical snapshots
  scripts/  # validation and eval tooling
local/  # local-only scratch inputs
```

## Validate

```bash
python3 evals/scripts/validate_skill_repo.py --repo-root .
python3 evals/scripts/validate_skill_repo.py --repo-root . --require-clean-git
```

For the evaluation workflow details, see [evals/README.md](evals/README.md).
