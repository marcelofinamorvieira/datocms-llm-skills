---
name: datocms-setup-sandbox-iteration
description: >-
  Set up a repeatable DatoCMS CLI sandbox iteration workflow with a reusable
  helper that resets a sandbox and can rerun migrations in place. Use when
  users explicitly want a local migration-iteration loop after basic CLI
  migrations are already configured.
disable-model-invocation: true
---

# DatoCMS Sandbox Iteration Setup

You are an expert at setting up a lean local sandbox-reset workflow for DatoCMS
CLI migrations. This skill adds one helper script and one package wrapper for
the common destroy, refork, rerun loop used during migration development.

**Shared bundle requirement:** This skill reuses references from `datocms-cli`.
Ensure that companion skill is installed alongside this one so the referenced
files are available.

Follow these steps in order. Do not skip steps.

---

## Step 1: Detect Context (silent)

Silently examine the project:

1. **Node project** — Check for `package.json`
2. **Package manager** — Detect `pnpm-lock.yaml`, `yarn.lock`, `bun.lockb`, or
   default to `npm`
3. **CLI migrations baseline** — Check for `@datocms/cli`,
   `datocms.config.json`, and a `migrations/` directory or existing migration
   scripts
4. **Existing helper** — Check for `scripts/datocms-reset-sandbox.mjs`
5. **Existing scripts** — Check `package.json` for `datocms:sandbox:reset`

### Stop conditions

- If the project does not already have working CLI migration setup, stop and
  tell the user to run `datocms-setup-migrations` first.
- If an existing sandbox-reset helper follows a materially different workflow,
  patch it in place by default and only ask if a rewrite would replace working
  behavior.

---

## Step 2: Ask Questions

Ask zero questions by default.

Only ask if an existing sandbox-reset helper materially conflicts with the lean
reset-and-rerun flow.

---

## Step 3: Load References

Read only these references:

- `../../../skills/datocms-cli/references/cli-setup.md`
- `../../../skills/datocms-cli/references/running-migrations.md`
- `../../../skills/datocms-cli/references/environment-commands.md`
- `../../../skills/datocms-cli/references/deployment-workflow.md`

Also inspect this bundled asset only when generating files:

- `assets/datocms-reset-sandbox.mjs`

---

## Step 4: Generate Code

Generate only these project changes:

1. **Create or patch `scripts/datocms-reset-sandbox.mjs`** from
   `assets/datocms-reset-sandbox.mjs`
2. **Patch `package.json`** with `datocms:sandbox:reset`

### Required behavior

The helper script must:

1. Accept explicit runtime arguments for the sandbox environment id
2. Accept an optional source environment id and optional profile flag
3. Destroy the target sandbox if it already exists
4. Fork from the requested source environment, or resolve the primary
   environment when no source is provided
5. Optionally rerun migrations in place on the sandbox
6. Never promote an environment
7. Never toggle maintenance mode

### Mandatory rules

- Use Node built-ins only in the helper script
- Keep environment ids and profiles runtime-configurable instead of hardcoding
  repo-specific values
- Allow the helper to skip the migration rerun when explicitly requested
- Do not add CI files, promotion logic, or maintenance-mode logic
- Do not add more than one helper script for this setup

---

## Step 5: Install Dependencies

Do not add any dependencies for this setup beyond the existing CLI baseline.
The helper must work with Node built-ins only.

---

## Step 6: Next Steps

After generating the files, tell the user:

1. Use the helper against disposable sandbox environments only
2. Run it once with migrations enabled and once with `--skip-migrations` so
   they understand both modes
3. Keep production rollout separate by using
   `datocms-setup-migration-release-workflow`

---

## Verification Checklist

Before presenting the result, verify:

1. `scripts/datocms-reset-sandbox.mjs` exists
2. `package.json` contains `datocms:sandbox:reset`
3. The helper uses `npx datocms`
4. The helper never promotes an environment
5. The helper never toggles maintenance mode
