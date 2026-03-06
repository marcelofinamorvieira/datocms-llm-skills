# Repo Layout

The root [README](../README.md#repo-layout) shows the short shape of the repo.
This page explains why the folders are split this way.

## Canonical Tree

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
docs/
evals/
  results/
  reports/
  scripts/
```

## Why It Is Split This Way

- `skills/` contains the shipped skill folders. Their names match each skill's canonical `name:` value.
- `skills/datocms-setup/` is the only shipped setup entrypoint. Its `SKILL.md` stays small and routes into local recipes through references and a manifest.
- `skills/datocms-setup/recipes/frontend-foundation/` contains project primitives such as data access, draft mode, previews, cache tags, and type generation.
- `skills/datocms-setup/recipes/frontend-features/` contains rendering and discovery add-ons layered on top of that foundation.
- `skills/datocms-setup/recipes/migrations/` contains repeatable schema and environment workflows.
- `skills/datocms-setup/recipes/onboarding/` contains one-shot content import flows.
- `skills/datocms-setup/recipes/platform/` contains project-level integrations such as webhooks, build triggers, and CMA type generation.
- `docs/` is for longer reference material that would make the root README too heavy.
- `evals/` keeps fixtures, checked-in results, reports, and tooling together so the trigger-quality loop is easy to inspect.
