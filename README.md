# DatoCMS Skills

A collection of focused DatoCMS skills for content operations, schema work,
frontend delivery, and one-time project setup. Each public skill keeps its
runtime surface small: one `SKILL.md`, scoped references, and optional host
metadata under `agents/`.

## Installation Model

Each public skill can be installed on its own, but the public set is designed
to cooperate. The skills use explicit handoff boundaries between CDA, CMA, CLI,
front-end integration, plugin work, and setup orchestration, so installing the
full public set gives the smoothest cross-skill routing.

If you only need one area, installing a single skill is still supported.

## Repo Layout

```text
skills/                     # shipped skills; folder names match `name:`
  datocms-setup/
    recipes/                # internal setup recipes grouped by workflow lane
docs/                       # repo structure, catalog, and install guides
evals/                      # trigger eval fixtures, scripts, and reports
local/                      # optional ignored scratch space for local-only checkouts
```

## Skill Groups

- Core domain skills live in `skills/` and use canonical folder names that match each skill's `name:` value.
- `skills/datocms-setup/` is the only public setup skill. It routes to internal recipe groups for frontend foundation, frontend features, migrations, onboarding, and platform work.
- Internal setup recipes keep the old workflow taxonomy for maintainers while removing that entire setup surface from public metadata.
- Setup recipes report either `scaffolded` or `production-ready` so contributors can distinguish a usable starter from a finished implementation.

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
