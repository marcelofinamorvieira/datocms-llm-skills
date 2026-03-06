---
name: datocms-setup-contentful-import
description: >-
  Set up a one-shot DatoCMS CLI Contentful import workflow with the required
  plugin, env placeholders, and a reusable local helper. Use when users
  explicitly want provider-specific onboarding from Contentful into DatoCMS
  without adding long-lived orchestration.
disable-model-invocation: true
---

# DatoCMS Contentful Import Setup

You are an expert at setting up the minimum repeatable workflow for importing
Contentful content into DatoCMS through the CLI. This skill keeps the setup
provider-specific and lightweight: one plugin, one helper, one package script.

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
3. **CLI installation** — Check `package.json` for `@datocms/cli`
4. **Contentful plugin** — Check `package.json` for
   `@datocms/cli-plugin-contentful`
5. **Environment files** — Check `.env.example`, `.env`, and `.env.local`
6. **Existing helper** — Check for `scripts/datocms-import-contentful.mjs`
7. **Existing scripts** — Check `package.json` for `datocms:import:contentful`

### Stop conditions

- If `package.json` is missing, stop and explain that this setup targets Node
  projects only.
- If an existing Contentful import helper follows a materially different flow,
  patch it in place by default and only ask if a rewrite would replace working
  behavior.

---

## Step 2: Ask Questions

Ask zero questions by default.

Only ask if an existing Contentful import helper materially conflicts with the
lean onboarding flow.

---

## Step 3: Load References

Read only these references:

- `../../../skills/datocms-cli/references/cli-setup.md`
- `../../../skills/datocms-cli/references/importing-content.md`

Also inspect this bundled asset only when generating files:

- `assets/datocms-import-contentful.mjs`

---

## Step 4: Generate Code

Generate only these project changes:

1. **Install missing packages**:
   - `@datocms/cli`
   - `@datocms/cli-plugin-contentful`
2. **Patch `.env.example`** so it includes:

   ```env
   DATOCMS_API_TOKEN=your_cma_token_here
   CONTENTFUL_SPACE_ID=your_space_id_here
   CONTENTFUL_TOKEN=your_contentful_token_here
   CONTENTFUL_ENVIRONMENT=master
   ```

3. **Create or patch `scripts/datocms-import-contentful.mjs`** from
   `assets/datocms-import-contentful.mjs`
4. **Patch `package.json`** with `datocms:import:contentful`

### Mandatory rules

- The helper must validate `CONTENTFUL_SPACE_ID` and `CONTENTFUL_TOKEN`
- The helper may use `CONTENTFUL_ENVIRONMENT` when present, but it must stay
  optional
- The helper must forward extra CLI flags to `contentful:import`
- The helper must not pass `--autoconfirm` by default
- Do not add CI files or multi-step orchestration around the import
- Do not add provider-mapping or transformation layers in this setup

---

## Step 5: Next Steps

After generating the files, tell the user:

1. Fill in the Contentful credentials and DatoCMS CMA token locally
2. Run the helper once without `--autoconfirm` to review the import behavior
3. Add flags like `--skip-content`, `--only-content-type`, or `--autoconfirm`
   only when they intentionally want those modes

---

## Verification Checklist

Before presenting the result, verify:

1. `@datocms/cli` and `@datocms/cli-plugin-contentful` are installed or added
2. `.env.example` contains the Contentful placeholders
3. `scripts/datocms-import-contentful.mjs` exists
4. `package.json` contains `datocms:import:contentful`
5. The helper does not inject `--autoconfirm` by default
