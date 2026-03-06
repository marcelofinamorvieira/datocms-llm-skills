_Internal recipe for `datocms-setup`. Use this file only after the parent skill selects the `graphql-types` recipe and queues any prerequisites from `../../../references/recipe-manifest.json`._


# DatoCMS GraphQL Type Generation Setup

You are an expert at setting up TypeScript type generation for DatoCMS GraphQL
queries. This recipe configures only CDA query typing. It does not configure CMA
schema types.

Follow these steps in order. Do not skip steps.

---

## Step 1: Detect Context (silent)

Silently examine the project:

1. **Framework** — Read `package.json` and check for:
   - `next` -> Next.js
   - `nuxt` -> Nuxt
   - `@sveltejs/kit` -> SvelteKit
   - `astro` -> Astro
2. **Existing typegen** — Check for:
   - `gql.tada` in `package.json`
   - `@graphql-codegen/cli` in `package.json`
   - `graphql.config.ts`
   - `schema.graphql`
   - an existing `graphql.ts` init file
3. **Existing scripts** — Check `package.json` for `generate-schema` and
   `generate-ts-types`
4. **Env files** — Check `.env`, `.env.local`, and `.env.example` for the
   published CDA token
5. **File structure** — Determine whether the project uses `src/`

### Stop conditions

- If the framework cannot be determined, ask the user.
- If the project already has a materially different type-generation setup,
  inspect and patch it in place by default instead of replacing it.

---

## Step 2: Ask Questions

Ask one question:

> "Which GraphQL query type-generation approach do you want: gql.tada
> (recommended) or GraphQL Code Generator?"

Do not ask about CMA types here. If the user wants CMA schema types, route them
to `datocms-setup` for `cma-types`.

---

## Step 3: Load References

Read only this reference:

- `../../../references/shared/datocms-cda/type-generation.md`

---

## Step 4: Generate Code

Generate the files and scripts required by the selected approach using the
framework-specific paths and env conventions from the reference.

### For gql.tada

Create or patch:

1. `generate-schema` in `package.json`
2. `tsconfig.json` plugin configuration
3. The `graphql.ts` init file
4. `schema.graphql` by running the generation script if the published CDA token
   is already available

### For GraphQL Code Generator

Create or patch:

1. `graphql.config.ts`
2. `generate-ts-types` in `package.json`
3. Generated types output, but only if at least one `.graphql` document already
   exists

### Mandatory rules

- Make targeted additions instead of full rewrites
- Preserve working existing scripts and config where possible
- Do not add CMA schema generation here
- Do not add `generate-cma-types` here
- If the user later wants typed CMA record operations, point them to
  `datocms-setup` for `cma-types`

---

## Step 5: Install Dependencies

Install only the dependencies required by the selected approach:

### gql.tada

- `gql.tada`
- `dotenv-cli`
- `@0no-co/graphqlsp` for SvelteKit only

### GraphQL Code Generator

- `graphql`
- `dotenv-cli`
- `@graphql-codegen/cli`
- the supporting codegen packages required by the reference

Use the detected package manager.

---

## Step 6: Next Steps

After generating the files, tell the user:

1. Re-run the query type-generation script after adding or changing GraphQL
   queries
2. Keep the published CDA token available in env files for schema introspection
3. Use `datocms-setup` for `cma-types` separately if they also want CMA schema types

---

## Verification Checklist

Before presenting the result, verify:

1. The chosen approach is fully configured
2. The generated files match the detected framework and `src/` layout
3. Existing config and scripts were patched in place instead of rewritten
4. No CMA-specific scripts, env vars, or references were added
