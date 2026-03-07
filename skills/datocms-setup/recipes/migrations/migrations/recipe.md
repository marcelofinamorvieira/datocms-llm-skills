_Internal recipe for `datocms-setup`. Use this file only after the parent skill selects the `migrations` recipe and queues any prerequisites from `../../../references/recipe-manifest.json`._


# DatoCMS Migrations Setup

You are an expert at setting up DatoCMS CLI migrations in existing projects.
This recipe creates the minimum project baseline for `migrations:new` and
`migrations:run` without adding custom templates, CI files, or multi-project
profile management.

Follow these steps in order. Do not skip steps.

---

## Step 1: Detect Context (silent)

Silently examine the project:

1. **Node project** — Check for `package.json`. If missing, stop and tell the
   user this skill expects a JavaScript or TypeScript project with a package
   manifest.
2. **Package manager** — See `../../../patterns/MANDATORY_RULES.md`.
3. **CLI installation** — Check `package.json` for `@datocms/cli`.
4. **CLI config** — Check for `datocms.config.json`.
5. **Migrations directory** — Check for `migrations/`.
6. **Environment files** — Check `.env.example`, `.env`, and `.env.local` for
   `DATOCMS_API_TOKEN`.
7. **TypeScript** — Check for `tsconfig.json`.
8. **Scripts** — Check `package.json` for `datocms:migrations:run`,
   `datocms:migrations:dry-run`, and `datocms:environments:list`.

### Stop conditions

- If `package.json` is missing, stop and explain that this setup targets Node
  projects only.
- If the repo already has a materially different multi-profile CLI setup, patch
  in place by default and only ask if adopting the single-project baseline
  would override working behavior.

---

## Step 2: Ask Questions

Ask zero questions by default.

Only ask if the existing `datocms.config.json` clearly uses multiple profiles,
custom migration directories, or other working conventions that would be
changed by the single-project baseline.

---

## Step 3: Load References

Read only these references:

- `../../../references/shared/datocms-cli/cli-setup.md`
- `../../../references/shared/datocms-cli/creating-migrations.md`
- `../../../references/shared/datocms-cli/running-migrations.md`

---

## Step 4: Generate Code

Make the minimum project changes needed for a working single-project CLI setup.

### Required project changes

1. **Install `@datocms/cli`** if it is missing
2. **Create or patch `datocms.config.json`** with one `default` profile:
   - `logLevel: "NONE"`
   - `migrations.directory: "./migrations"`
   - `migrations.modelApiKey: "schema_migration"`
3. **Create `migrations/`** if it does not exist
4. **Patch `.env.example`** so it contains:

   ```env
   DATOCMS_API_TOKEN=your_cma_token_here
   ```

5. **Patch `package.json` scripts** so it includes exactly these helpers:
   - `datocms:migrations:run`
   - `datocms:migrations:dry-run`
   - `datocms:environments:list`

### Mandatory rules

- Use `npx datocms` in generated scripts
- Preserve existing scripts and merge changes in place
- Do not create a custom migration template file
- Do not create a migrations-specific tsconfig file
- Do not add CI files
- Do not create multiple CLI profiles
- Do not overwrite working values in env files

---

## Step 5: Install Dependencies

Use the project's package manager (see `../../../patterns/MANDATORY_RULES.md`).

- `@datocms/cli`

No other package should be added in this setup.

---

## Step 6: Next Steps

After generating the files, tell the user:

1. Add a CMA-capable token to their local env file
2. Create the first migration with:

   ```bash
   npx datocms migrations:new "describe the change" --ts
   ```

3. Dry-run before applying:

   ```bash
   npm run datocms:migrations:dry-run
   ```

4. Use `datocms-setup` for `migration-release-workflow` if they want a repeatable
   production rollout flow
5. Use `datocms-setup` for `blueprint-sync` if they need one migration history
   shared across multiple DatoCMS projects

---

## Verification Checklist

Before presenting the result, verify:

1. `@datocms/cli` is installed or added
2. `datocms.config.json` exists with one `default` profile
3. `migrations/` exists
4. `.env.example` contains `DATOCMS_API_TOKEN`
5. `package.json` contains the three required helper scripts
6. No custom template, custom tsconfig, CI file, or multi-profile config was
   added by default
