# DatoCMS Skills

A collection of focused DatoCMS skills for content operations, schema work, frontend delivery, and repeatable setup flows. Each skill keeps its runtime surface small: one `SKILL.md`, scoped references, and optional host metadata under `agents/`.

## Repo Layout

```text
skills/                     # reusable domain skills; folder names match `name:`
setup/
  frontend-foundation/      # query, draft, preview, and shared data-layer setup
  frontend-features/        # rendering, search, and content presentation setup
  migrations/               # migration and environment workflow setup
  onboarding/               # one-shot import and onboarding flows
  platform/                 # webhooks, triggers, and type-generation setup
docs/                       # repo structure, catalog, and install guides
evals/                      # trigger eval fixtures, scripts, and reports
local/                      # optional ignored scratch space for local-only checkouts
```

## Skill Groups

- Core domain skills live in `skills/` and use canonical folder names that match each skill's `name:` value.
- Frontend setup is split between `frontend-foundation` and `frontend-features` so foundational wiring stays separate from presentation-level add-ons.
- `platform/` holds setup flows that manage project-level integrations instead of product features.
- Setup flows report either `scaffolded` or `production-ready` so contributors can distinguish a usable starter from a finished implementation.

## Docs

- [Repo layout](docs/repo-layout.md)
- [Skill catalog](docs/skill-catalog.md)
- [Install guide](docs/install.md)
- [Evaluation loop](evals/README.md)

## Validation

```bash
python3 evals/scripts/validate_skill_repo.py --repo-root .
```

Run the clean-tree variant before publishing changes:

```bash
python3 evals/scripts/validate_skill_repo.py --repo-root . --require-clean-git
```
