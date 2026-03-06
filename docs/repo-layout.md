# Repo Layout

The repository is organized around the way contributors find and maintain skills, not around installation order.

## Canonical Tree

```text
skills/
  datocms-cda/
  datocms-cli/
  datocms-cma/
  datocms-frontend-integrations/
  datocms-plugin-builder/
setup/
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
- `setup/frontend-foundation/` contains setup flows that establish project primitives such as data access, draft mode, previews, or type generation.
- `setup/frontend-features/` contains setup flows that layer on rendering and discovery features after the foundation is in place.
- `setup/migrations/` contains repeatable schema and environment workflows.
- `setup/onboarding/` contains one-shot content import flows.
- `setup/platform/` contains project-level integrations such as webhooks, build triggers, and CMA type generation.
- `docs/` keeps repo guidance out of the root README so contributors can update layout, catalog, and install guidance independently.
- `evals/` stays isolated from shipped skill content.

## Optional Local Scratch Space

`local/` is intentionally outside the tracked layout. Use it for temporary checkouts, experiments, or support material that should not participate in validation or publishing.
