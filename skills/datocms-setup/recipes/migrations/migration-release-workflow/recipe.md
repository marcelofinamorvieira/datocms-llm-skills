_Internal recipe for `datocms-setup`. Use this file only after the parent skill selects the `migration-release-workflow` recipe and queues any prerequisites from `../../../references/recipe-manifest.json`._


# DatoCMS Migration Release Workflow Setup

You are an expert at turning a working DatoCMS CLI migration setup into a
repeatable production release workflow. This recipe adds one local helper and,
only when requested, one GitHub Actions workflow.

Follow these steps in order. Do not skip steps.

---

## Step 1: Detect Context (silent)

Silently examine the project:

1. **Node project** — Check for `package.json`
2. **Package manager** — See `../../../patterns/MANDATORY_RULES.md`.
3. **CLI setup** — Check for `@datocms/cli`, `datocms.config.json`, and a
   `migrations/` directory or existing migration scripts
4. **Existing helper** — Check for `scripts/datocms-release.mjs`
5. **Existing workflow** — Check for `.github/workflows/datocms-release.yml`
6. **Existing scripts** — Check `package.json` for `datocms:release`

### Stop conditions

- If the project does not already have working CLI migration setup, stop and
  record `migrations` as a prerequisite and continue after it is applied.
- If a release helper already exists, patch it in place by default instead of
  replacing it wholesale.

---

## Step 2: Ask Questions

Ask one question:

> "Do you also want a GitHub Actions template for this release workflow?"

If the user says no, generate only the local helper script and package wrapper.

---

## Step 3: Load References

Read only these references:

- `../../../references/shared/datocms-cli/cli-setup.md`
- `../../../references/shared/datocms-cli/running-migrations.md`
- `../../../references/shared/datocms-cli/environment-commands.md`
- `../../../references/shared/datocms-cli/deployment-workflow.md`

Also inspect these bundled assets only when generating files:

- `scripts/datocms-release.mjs`
- `assets/datocms-release.github-actions.yml`

---

## Step 4: Generate Code

Generate only these project files:

1. **`scripts/datocms-release.mjs`** — Copy and adapt
   `scripts/datocms-release.mjs`
2. **`package.json` script** — Add `datocms:release`
3. **Optional GitHub Actions workflow** — If the user opted in, copy and adapt
   `assets/datocms-release.github-actions.yml` to
   `.github/workflows/datocms-release.yml`

### Required behavior

The local helper script must:

1. Run `maintenance:on`
2. Run `migrations:run --destination=<env>`
3. Run `environments:promote <env>`
4. Always run `maintenance:off`, even after failures

### Mandatory rules

- Use Node built-ins only in the helper script
- Preserve any existing CLI profile flags or source-environment defaults the
  repo already uses
- Keep the workflow GitHub-only in v1
- Do not add provider-specific CI beyond GitHub Actions
- Do not create additional helper scripts
- Do not replace a working existing release workflow unless the user explicitly
  asked for a rewrite

---

## Step 5: Install Dependencies

Do not add any new dependencies for this setup unless the project is missing a
required Node runtime package for its own existing scripts. The bundled helper
must work with Node built-ins only.

---

## Step 6: Next Steps

After generating the files, tell the user:

1. Verify the destination environment naming convention used by the helper
2. Run a dry-run or sandbox rehearsal before using the production release flow
3. Set the required DatoCMS token in their env file
4. Review the generated GitHub workflow secrets mapping if CI scaffolding was
   enabled

---

## Verification Checklist

Before presenting the result, verify:

1. `scripts/datocms-release.mjs` exists and keeps `maintenance:off` in the
   failure path
2. `package.json` contains `datocms:release`
3. The helper uses `npx datocms`
4. The workflow file is created only when the user opted in
5. No non-GitHub CI files were added
