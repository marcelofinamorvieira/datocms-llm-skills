---
name: datocms-setup
description: >-
  Command-style one-time DatoCMS setup wizard for frontend foundation,
  frontend features, migrations, onboarding imports, and platform automation.
  Use when users want to scaffold or configure DatoCMS project setup, route to
  the right setup recipe, and answer a short clarification pass when needed.
disable-model-invocation: true
---

# DatoCMS Setup

This is the single public setup entrypoint for DatoCMS project scaffolding.
Keep the public surface small, detect the repo context first, and load only the
internal recipe files needed for the user's requested outcome.

## Workflow

1. Silently inspect the repo before asking questions:
   - framework and package manager
   - file layout and `src/` usage
   - existing DatoCMS query wrappers, preview wiring, migrations, or platform scripts
   - env files and dependency state
2. Read `references/router.md`.
3. Read `references/recipe-manifest.json` and select the smallest recipe set that satisfies the request.
4. Use targeted mode when the request clearly names a setup outcome. Use discovery mode only when the request is broad or ambiguous.
5. Queue prerequisites from the manifest before dependent recipes. Never tell the user to invoke another setup skill separately.
6. Load only the selected `recipes/<group>/<recipe>/recipe.md` files and the local shared references they point to.
7. Patch existing project code in place by default instead of rewriting working implementations.

## Rules

- Do not load every recipe up front.
- Do not reference or depend on any external setup bundles.
- Treat recipe ids such as `draft-mode`, `web-previews`, and `migration-release-workflow` as internal orchestration labels.
- If several requested outcomes share a foundation, apply that foundation once and continue through the queued recipes.
- If the user asks for broad setup, ask one compact grouped clarification pass, then execute the minimal recipe bundle.
- Report `scaffolded` when a recipe still depends on placeholders, provider choices, or route mappings the repo could not resolve automatically.
- Report `production-ready` only when the selected recipe no longer depends on unresolved customer-specific values.
- End by summarizing which internal recipes were used and which optional follow-up recipes are available inside `datocms-setup`.
