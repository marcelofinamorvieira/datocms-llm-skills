# Repo Layout

The repository is organized around the way contributors find and maintain
skills, not around installation order. That said, the public skills are
designed to cooperate through explicit handoff rules, so installing the full
public set is the recommended runtime setup even though each skill remains
individually installable.

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
      frontend-foundation/
      frontend-features/
      migrations/
      onboarding/
      platform/
docs/
evals/
```

## Why It Is Split This Way

- `skills/` contains reusable domain skills. Folder names match the canonical `name:` field so the repo path is no longer a translation layer.
- `skills/datocms-setup/` is the only shipped setup entrypoint. Its `SKILL.md` stays small and routes to internal recipes through local references and a manifest.
- `skills/datocms-setup/recipes/frontend-foundation/` contains setup flows that establish project primitives such as data access, draft mode, previews, or type generation.
- `skills/datocms-setup/recipes/frontend-features/` contains setup flows that layer on rendering and discovery features after the foundation is in place.
- `skills/datocms-setup/recipes/migrations/` contains repeatable schema and environment workflows.
- `skills/datocms-setup/recipes/onboarding/` contains one-shot content import flows.
- `skills/datocms-setup/recipes/platform/` contains project-level integrations such as webhooks, build triggers, and CMA type generation.
- `docs/` keeps repo guidance out of the root README so contributors can update layout, catalog, and install guidance independently.
- `evals/` stays isolated from shipped skill content.

## Optional Local Scratch Space

`local/` is intentionally outside the tracked layout. Use it for temporary checkouts, experiments, or support material that should not participate in validation or publishing.
