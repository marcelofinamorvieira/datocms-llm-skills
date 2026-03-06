---
name: datocms-setup-cli-profiles
description: >-
  Set up reusable named DatoCMS CLI profiles and token placeholders while
  preserving the current default-profile conventions. Use when users
  explicitly want local, staging, or production-style CLI profile setup
  without a blueprint-sync workflow.
disable-model-invocation: true
---

# DatoCMS CLI Profiles Setup

You are an expert at setting up named DatoCMS CLI profiles in existing
projects. This skill stays lean: it only patches CLI config, env placeholders,
and one safe listing script when needed.

**Shared bundle requirement:** This skill reuses references from `datocms-cli`.
Ensure that companion skill is installed alongside this one so the referenced
files are available.

Follow these steps in order. Do not skip steps.

---

## Step 1: Detect Context (silent)

Silently examine the project:

1. **Node project** — Check for `package.json`
2. **CLI installation** — Check `package.json` for `@datocms/cli`
3. **Existing CLI config** — Check for `datocms.config.json`
4. **Existing profiles** — Inspect `datocms.config.json` for a `default`
   profile and any named profiles
5. **Migrations convention** — Check whether the repo already has a clear
   migrations convention through existing CLI config, a `migrations/`
   directory, or package scripts
6. **Environment files** — Check `.env.example`, `.env`, and `.env.local`
7. **Existing scripts** — Check `package.json` for `datocms:environments:list`
   or another safe equivalent that already runs `npx datocms environments:list`

### Stop conditions

- If `package.json` is missing, stop and explain that this setup targets Node
  projects only.
- If the repo already has a materially different profile scheme, patch it in
  place by default instead of normalizing names or removing profiles.

---

## Step 2: Ask Questions

Ask one question:

> "Which CLI profile ids should I create or update?"

Do not ask for environment-variable names separately. Derive those from the
requested profile ids.

---

## Step 3: Load References

Read only these references:

- `../../../skills/datocms-cli/references/cli-setup.md`
- `../../../skills/datocms-cli/references/environment-commands.md`

---

## Step 4: Generate Code

Generate only these project changes:

1. **Create or patch `datocms.config.json`**
2. **Patch `.env.example`** with one token placeholder per named profile:

   ```env
   DATOCMS_STAGING_PROFILE_API_TOKEN=your_token_here
   DATOCMS_PRODUCTION_PROFILE_API_TOKEN=your_token_here
   ```

3. **Patch `package.json`** with `datocms:environments:list` only when no safe
   equivalent already exists

### Required behavior

- Preserve the current `default` profile if one exists
- Clone the current default profile's non-token config into the requested named
  profiles when possible
- If no config exists yet, create `default` plus the requested named profiles
  with `logLevel: "NONE"`
- Only include a `migrations` block for new profiles when the repo already has
  one clear migrations convention

### Mandatory rules

- Do not remove or rename existing profiles unless the user explicitly asks
- Do not generate one package script per profile
- Do not force a fixed local, staging, production naming convention
- Do not create multi-project rollout helpers in this setup
- Do not write tokens into config files

---

## Step 5: Install Dependencies

Install `@datocms/cli` only if it is missing. Do not add any other packages for
this setup.

---

## Step 6: Next Steps

After generating the files, tell the user:

1. Fill in the per-profile tokens locally
2. Test each new profile with `npx datocms environments:list --profile=<id>`
3. Use `datocms-setup-blueprint-sync` separately when they want shared
   multi-project rollout from one migration history

---

## Verification Checklist

Before presenting the result, verify:

1. `datocms.config.json` exists and preserves current working profile config
2. Requested profile ids exist in config after the patch
3. `.env.example` contains the per-profile token placeholders
4. `datocms:environments:list` is added only when no safe equivalent exists
5. No one-script-per-profile expansion was added
