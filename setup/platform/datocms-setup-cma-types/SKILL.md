---
name: datocms-setup-cma-types
description: >-
  Set up DatoCMS CMA schema type generation with @datocms/cli, a
  generate-cma-types script, framework-appropriate output paths, and env
  placeholders. Use when users explicitly want type-safe CMA record operations
  without configuring GraphQL query type generation.
disable-model-invocation: true
---

# DatoCMS CMA Type Generation Setup

You are an expert at setting up standalone CMA schema type generation. This
skill configures only the `schema:generate` workflow and does not overlap with
GraphQL query type-generation setup.

**Shared bundle requirement:** This skill reuses references from `datocms-cli`
and `datocms-cma`. Ensure those companion skills are installed alongside this
one so the referenced files are available.

Follow these steps in order. Do not skip steps.

---

## Step 1: Detect Context (silent)

Silently examine the project:

1. **Framework** — Read `package.json` and check for:
   - `next` -> Next.js
   - `nuxt` -> Nuxt
   - `@sveltejs/kit` -> SvelteKit
   - `astro` -> Astro
2. **Node project** — Confirm `package.json` exists
3. **CLI installation** — Check `package.json` for `@datocms/cli`
4. **dotenv support** — Check `package.json` for `dotenv-cli`
5. **Existing script** — Check `package.json` for `generate-cma-types`
6. **Existing output** — Check for `src/lib/datocms/cma-types.ts` or
   `lib/datocms/cma-types.ts`
7. **Environment files** — Check `.env.example`, `.env`, and `.env.local` for a
   CMA-capable token
8. **File structure** — Determine whether the project uses `src/`

### Stop conditions

- If the framework cannot be determined, ask the user.
- If the repo already has a materially different schema-type generation setup,
  inspect and patch it in place by default instead of replacing it.

---

## Step 2: Ask Questions

Ask zero questions by default.

Only ask if the project already has a conflicting CMA type-generation flow and
patching it safely is unclear.

---

## Step 3: Load References

Read only these references:

- `../../../skills/datocms-cli/references/cli-setup.md`
- `../../../skills/datocms-cma/references/type-generation.md`

---

## Step 4: Generate Code

Generate only the standalone CMA type-generation setup.

### Required project changes

1. **Install missing packages**:
   - `@datocms/cli`
   - `dotenv-cli`
2. **Patch `.env.example`** with the framework-appropriate CMA token placeholder
3. **Patch `package.json`** with `generate-cma-types`
4. **Choose the output path**:
   - Next.js / Astro / SvelteKit with `src/`: `src/lib/datocms/cma-types.ts`
   - Next.js / Astro / SvelteKit without `src/`: `lib/datocms/cma-types.ts`
   - Nuxt: `lib/datocms/cma-types.ts`
5. **Run the initial generation only if a CMA-capable token already exists**

### Mandatory rules

- Configure only CMA schema types
- Do not configure gql.tada
- Do not configure GraphQL Code Generator
- Preserve an existing working script name if the repo already uses one, but
  ensure `generate-cma-types` exists
- Use the framework-specific env var naming from the reference

---

## Step 5: Next Steps

After generating the files, tell the user:

1. Re-run `generate-cma-types` after schema changes
2. Use the generated unions such as `AnyModel` and `AnyBlock` with `raw*()`
   CMA methods
3. Use `datocms-setup-graphql-types` separately if they also want typed CDA
   queries

---

## Verification Checklist

Before presenting the result, verify:

1. `package.json` contains `generate-cma-types`
2. `.env.example` contains the correct framework-specific CMA token placeholder
3. The output path matches the detected framework and `src/` layout
4. `@datocms/cli` and `dotenv-cli` are installed or added
5. No GraphQL query type-generation setup was added by this skill
