---
name: datocms-setup-graphql-types
description: >-
  Set up TypeScript type generation for DatoCMS GraphQL queries using gql.tada
  or GraphQL Code Generator. Optionally generates CMA schema types. Supports
  Next.js (App Router), Nuxt, SvelteKit, and Astro. Detects the framework
  automatically, generates config files, installs dependencies, and runs the
  initial schema generation.
disable-model-invocation: true
---

# DatoCMS GraphQL Type Generation Setup

You are an expert at setting up TypeScript type generation for DatoCMS projects. This skill configures either **gql.tada** or **GraphQL Code Generator** for fully typed CDA queries, and optionally generates CMA schema types for typed record operations.

Follow these steps in order. Do not skip steps.

---

## Step 1: Detect Context (silent)

Silently examine the project:

1. **Framework** — Read `package.json` and check for:
   - `next` → Next.js (App Router)
   - `nuxt` → Nuxt
   - `@sveltejs/kit` → SvelteKit
   - `astro` → Astro
   - If none match, stop and ask the user which framework they are using.

2. **Existing type generation setup** — Check if type generation is already configured:
   - gql.tada: Check if `gql.tada` is in `package.json` dependencies
   - gql.tada: Check if `tsconfig.json` has `gql.tada/ts-plugin` or `@0no-co/graphqlsp` in `compilerOptions.plugins`
   - gql.tada: Check if a `graphql.ts` init file exists (e.g., `src/lib/datocms/graphql.ts` or `lib/datocms/graphql.ts`)
   - GraphQL Code Generator: Check if `@graphql-codegen/cli` is in `package.json` devDependencies
   - GraphQL Code Generator: Check if `graphql.config.ts` exists at the project root
   - Check if `schema.graphql` already exists at the project root

3. **Existing scripts** — Check `package.json` scripts for `generate-schema`, `generate-ts-types`, `generate-cma-types`

4. **Installed deps** — Check `package.json` for: `gql.tada`, `@graphql-codegen/cli`, `graphql`, `dotenv-cli`, `@datocms/cli`

5. **Env files** — Check `.env`, `.env.local`, `.env.example` for existing DatoCMS tokens (especially the published CDA token needed for schema introspection)

6. **File structure** — Determine whether the project uses a `src/` directory

### Stop conditions

- If the framework cannot be determined, ask the user.
- If type generation is already configured (gql.tada or graphql-codegen detected), inform the user and ask: "Type generation is already configured with [detected approach]. Do you want me to replace it with a fresh setup?"

---

## Step 2: Ask Questions

### Question 1: Which approach?

Ask the user which type generation approach they want:

- **gql.tada** (Recommended) — Automatic type inference via TypeScript plugin. Used in all DatoCMS starters. Best for new projects and simpler setups. Queries are written as `graphql()` tagged templates in `.ts` files.
- **GraphQL Code Generator** — Manual codegen CLI command. Best for existing codegen pipelines and `.graphql` file workflows. Used in DatoCMS fully-fledged demos.

### Question 2: CMA types?

Ask the user if they also want CMA schema types:

- **Yes** — Generate typed CMA record operations using `@datocms/cli schema:generate`. This produces a `cma-types.ts` file with TypeScript types for all models/blocks, used with `@datocms/cma-client`'s `raw*()` methods.
- **No** — Skip CMA type generation (most common — only needed if using the CMA client for record CRUD).

---

## Step 3: Load References

Use the `Read` tool to load reference files. Load only what is needed.

**Always load:**
- `../datocms-cda-skill/references/type-generation.md`

**If CMA types requested:**
- Also load `../datocms-cma-skill/references/type-generation.md`

---

## Step 4: Generate Code

Generate files following the patterns in the loaded references. The specific files depend on the chosen approach and framework.

### For gql.tada

1. **Add `generate-schema` script** to `package.json` — Uses `dotenv-cli` to load the published CDA token and runs `gql.tada generate schema`:

   | Framework | Env var in script |
   |---|---|
   | Next.js | `$DATOCMS_PUBLISHED_CONTENT_CDA_TOKEN` |
   | Astro | `$DATOCMS_PUBLISHED_CONTENT_CDA_TOKEN` |
   | SvelteKit | `$PRIVATE_DATOCMS_PUBLISHED_CONTENT_CDA_TOKEN` |
   | Nuxt | `$NUXT_PUBLIC_DATOCMS_PUBLISHED_CONTENT_CDA_TOKEN` |

   The script format:
   ```json
   "generate-schema": "dotenv -c -- bash -c 'gql.tada generate schema https://graphql.datocms.com --header \"X-Exclude-Invalid: true\" --header \"Authorization: $ENV_VAR_NAME\"'"
   ```

2. **Add TypeScript plugin** to `tsconfig.json` `compilerOptions.plugins` array (create `plugins` if it doesn't exist):

   | Framework | Plugin name | Output path |
   |---|---|---|
   | Next.js | `gql.tada/ts-plugin` | `./src/lib/datocms/graphql-env.d.ts` |
   | Astro | `gql.tada/ts-plugin` | `./src/lib/datocms/graphql-env.d.ts` |
   | SvelteKit | `@0no-co/graphqlsp` | `./src/lib/datocms/graphql-env.d.ts` |
   | Nuxt | `gql.tada/ts-plugin` | `./lib/datocms/graphql-env.d.ts` |

   The plugin config:
   ```json
   {
     "name": "<plugin-name>",
     "schema": "./schema.graphql",
     "tadaOutputLocation": "<output-path>"
   }
   ```

3. **Create `graphql.ts` init file** at the directory matching the output path (e.g., `src/lib/datocms/graphql.ts` or `lib/datocms/graphql.ts` for Nuxt):

   ```ts
   import { initGraphQLTada } from 'gql.tada';
   import type { introspection } from './graphql-env.js';

   export const graphql = initGraphQLTada<{
     introspection: introspection;
     scalars: {
       BooleanType: boolean;
       CustomData: Record<string, string>;
       Date: string;
       DateTime: string;
       FloatType: number;
       IntType: number;
       ItemId: string;
       JsonField: unknown;
       MetaTagAttributes: Record<string, string>;
       UploadId: string;
     };
   }>();

   export { readFragment } from 'gql.tada';

   export type { FragmentOf, ResultOf, VariablesOf } from 'gql.tada';
   ```

4. **Run `generate-schema`** — Execute the script to produce `schema.graphql` at the project root. This is needed for the TypeScript plugin to provide autocomplete immediately.

### For GraphQL Code Generator

1. **Create `graphql.config.ts`** at the project root:

   ```ts
   import 'dotenv/config';
   import type { IGraphQLConfig } from 'graphql-config';

   const config: IGraphQLConfig = {
     schema: [
       {
         'https://graphql.datocms.com': {
           headers: {
             Authorization: `Bearer ${process.env.DATOCMS_READONLY_API_TOKEN}`,
             'X-Exclude-Invalid': 'true',
           },
         },
       },
     ],
     documents: ['./app/**/*.graphql', './components/**/*.graphql'],
     extensions: {
       codegen: {
         generates: {
           'graphql/types/': {
             preset: 'client',
             presetConfig: {
               fragmentMasking: { unmaskFunctionName: 'getFragmentData' },
             },
             config: {
               strictScalars: true,
               scalars: {
                 BooleanType: 'boolean',
                 CustomData: 'Record<string, unknown>',
                 Date: 'string',
                 DateTime: 'string',
                 FloatType: 'number',
                 IntType: 'number',
                 ItemId: 'string',
                 JsonField: 'unknown',
                 MetaTagAttributes: 'Record<string, string>',
                 UploadId: 'string',
               },
             },
           },
         },
       },
     },
   };

   export default config;
   ```

   Adjust the `documents` glob to match the project's file structure (e.g., `./src/**/*.graphql` if using a `src/` directory, or `./pages/**/*.graphql` for Nuxt).

   For Nuxt/SvelteKit, update the env var name in the `Authorization` header to match the framework convention — however, since `graphql.config.ts` uses `process.env` directly (not framework env access), the env var in `.env` can use a plain name like `DATOCMS_READONLY_API_TOKEN` that `dotenv` loads.

2. **Add `generate-ts-types` script** to `package.json`:

   ```json
   "generate-ts-types": "graphql-codegen --config graphql.config.ts"
   ```

3. **Run `generate-ts-types`** — Execute the script to produce the generated types in `graphql/types/`. This requires at least one `.graphql` file to exist. If none exist yet, inform the user that they need to create `.graphql` files first before running the codegen, and skip running the script.

### For CMA types (if requested)

1. **Add `generate-cma-types` script** to `package.json`:

   | Framework | Script |
   |---|---|
   | Next.js | `"dotenv -c -- bash -c 'npx @datocms/cli schema:generate src/lib/datocms/cma-types.ts --api-token=$DATOCMS_CMA_TOKEN'"` |
   | Astro | `"dotenv -c -- bash -c 'npx @datocms/cli schema:generate src/lib/datocms/cma-types.ts --api-token=$DATOCMS_CMA_TOKEN'"` |
   | SvelteKit | `"dotenv -c -- bash -c 'npx @datocms/cli schema:generate src/lib/datocms/cma-types.ts --api-token=$PRIVATE_DATOCMS_CMA_TOKEN'"` |
   | Nuxt | `"dotenv -c -- bash -c 'DATOCMS_API_TOKEN=$NUXT_DATOCMS_CMA_TOKEN npx @datocms/cli schema:generate lib/datocms/cma-types.ts'"` |

2. **Run `generate-cma-types`** — Execute the script to produce `cma-types.ts`. This requires the CMA token to be set in the env file. If the token is not configured yet, inform the user and skip running the script.

### Mandatory rules for all generated code

#### TypeScript
- No `as unknown as` — this is a forbidden anti-pattern
- No unnecessary `as SomeType` casts
- Let TypeScript infer types wherever possible
- Use `import type { ... }` for type-only imports

#### File conflicts
- Read existing files before modifying them
- Make targeted additions, not full rewrites (especially for `tsconfig.json` and `package.json`)
- Skip if a piece is already configured

---

## Step 5: Install Dependencies

Install missing packages using the project's package manager (check for `pnpm-lock.yaml`, `yarn.lock`, `bun.lockb`, or default to `npm`).

### For gql.tada

| Package | Type | Notes |
|---|---|---|
| `gql.tada` | dependency | Core library |
| `dotenv-cli` | devDependency | Loads env vars for schema generation script |
| `@0no-co/graphqlsp` | devDependency | **SvelteKit only** — the LSP plugin used instead of `gql.tada/ts-plugin` |

### For GraphQL Code Generator

| Package | Type | Notes |
|---|---|---|
| `@graphql-codegen/typed-document-node` | dependency | — |
| `@graphql-codegen/typescript` | dependency | — |
| `@graphql-codegen/typescript-operations` | dependency | — |
| `@graphql-typed-document-node/core` | dependency | — |
| `graphql` | dependency | — |
| `@graphql-codegen/cli` | devDependency | — |
| `graphql-config` | devDependency | — |

### For CMA types (if requested)

| Package | Type | Notes |
|---|---|---|
| `@datocms/cli` | devDependency | Provides the `schema:generate` command |
| `dotenv-cli` | devDependency | Loads env vars for the generate script (may already be installed from gql.tada) |

---

## Step 6: Environment Variables

Add placeholder values to `.env.example` (create if it doesn't exist) and `.env.local` (or `.env` depending on framework convention). Only add variables that don't already exist. Preserve any existing values.

### For gql.tada / schema introspection

The published CDA token is needed for schema generation. This is the same token used by `executeQuery` for published content — it may already exist if `/setup-draft-mode` was run.

#### Next.js / Astro
```
DATOCMS_PUBLISHED_CONTENT_CDA_TOKEN=your_published_token_here
```

#### SvelteKit
```
PRIVATE_DATOCMS_PUBLISHED_CONTENT_CDA_TOKEN=your_published_token_here
```

#### Nuxt
```
NUXT_PUBLIC_DATOCMS_PUBLISHED_CONTENT_CDA_TOKEN=your_published_token_here
```

### For GraphQL Code Generator

Uses `dotenv` directly (not framework env access), so a plain env var name works:

```
DATOCMS_READONLY_API_TOKEN=your_published_token_here
```

### For CMA types (if requested)

A CMA-capable API token is required (`can_access_cma: true`). A read-only CDA token will not work.

#### Next.js / Astro
```
DATOCMS_CMA_TOKEN=your_cma_api_token_here
```

#### SvelteKit
```
PRIVATE_DATOCMS_CMA_TOKEN=your_cma_api_token_here
```

#### Nuxt
```
NUXT_DATOCMS_CMA_TOKEN=your_cma_api_token_here
```

---

## Step 7: Next Steps

After generating all files, tell the user:

1. **Fill in tokens** (if not already set) — Get tokens from DatoCMS Settings → API Tokens:
   - **Published Content CDA Token** (for gql.tada schema generation) — read-only token scoped to published content
   - **CMA Token** (only if CMA types were requested) — a token with CMA access (`can_access_cma: true`)
   - **Read-only API Token** (for GraphQL Code Generator) — can be the same as the published CDA token

2. **How to write typed queries:**

   **gql.tada:**
   ```ts
   import { graphql } from '~/lib/datocms/graphql';

   const query = graphql(`
     query HomePage {
       homePage {
         title
       }
     }
   `);

   // executeQuery returns fully typed results
   const data = await executeQuery(query);
   // data.homePage?.title is typed as string
   ```

   **GraphQL Code Generator:**
   - Create `.graphql` files next to your components
   - Run `npm run generate-ts-types` after adding/changing queries
   - Import the typed document from `graphql/types/gql`

3. **Re-run after model changes:**
   - gql.tada: `npm run generate-schema` (regenerates `schema.graphql`)
   - GraphQL Code Generator: `npm run generate-ts-types` (regenerates typed documents)
   - CMA types: `npm run generate-cma-types` (regenerates `cma-types.ts`)

4. **IDE integration:**
   - gql.tada: The TypeScript plugin provides autocomplete and error checking for GraphQL queries directly in your editor. Make sure your editor uses the workspace TypeScript version (not a global one).
   - GraphQL Code Generator: Consider installing the GraphQL VS Code extension for `.graphql` file syntax highlighting.

---

## Verification Checklist

Before presenting the final code, verify:

1. **gql.tada:** `tsconfig.json` has the correct plugin (`gql.tada/ts-plugin` or `@0no-co/graphqlsp` for SvelteKit) with `schema` and `tadaOutputLocation`
2. **gql.tada:** The `graphql.ts` init file has all DatoCMS scalar mappings (`BooleanType`, `CustomData`, `Date`, `DateTime`, `FloatType`, `IntType`, `ItemId`, `JsonField`, `MetaTagAttributes`, `UploadId`)
3. **gql.tada:** The `generate-schema` script uses the correct framework-specific env var name
4. **gql.tada:** SvelteKit uses `@0no-co/graphqlsp` (not `gql.tada/ts-plugin`) and installs it as a dev dependency
5. **gql.tada:** Nuxt uses `lib/datocms/` paths (no `src/` prefix)
6. **GraphQL Code Generator:** `graphql.config.ts` has `strictScalars: true` and all DatoCMS scalar mappings
7. **GraphQL Code Generator:** The `documents` glob matches the project's file structure
8. **CMA types:** The generate script uses the correct framework-specific env var and output path
9. **CMA types:** Nuxt script remaps the env var inline (`DATOCMS_API_TOKEN=$NUXT_DATOCMS_CMA_TOKEN`)
10. All generated TypeScript follows the mandatory rules (no `as unknown as`, inferred types, `import type`)
11. Environment variables use the correct framework-specific prefixes
12. Existing files (`tsconfig.json`, `package.json`) are modified with targeted additions, not full rewrites
