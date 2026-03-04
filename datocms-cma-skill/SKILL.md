---
name: datocms-cma
description: >-
  Interact with the DatoCMS Content Management API (CMA) using the official
  TypeScript/JavaScript REST clients. Use when users want to create, read,
  update, or delete records (items), manage uploads and assets, define or
  modify models and fields (schema), work with environments (fork, promote),
  configure webhooks and build triggers, manage roles and API tokens,
  schedule publication or unpublication, handle localized content,
  build modular content with blocks and structured text, paginate and
  filter records, write migration and seeding scripts, or generate
  TypeScript types from your DatoCMS schema for type-safe record
  operations. Covers the most commonly used CMA resources — records,
  uploads, schema, environments, webhooks, access control, scheduling,
  and workflows.
---

# DatoCMS Content Management API Skill

You are an expert at writing code that interacts with the DatoCMS Content Management API (CMA). Follow these steps in order. Do not skip steps.

---

## Step 1: Detect Context

Silently examine the project to determine the runtime and which CMA client package is available.

1. Read `package.json` and check for these packages (in priority order):
   - `@datocms/cma-client` — Universal/isomorphic package. **Recommended for most cases.** Works in any environment with native `fetch`. Only provide a `fetchFn` if your runtime lacks native Fetch API.
   - `@datocms/cma-client-node` — Node.js-optimized. Adds upload helpers (`createFromLocalFile`, `createFromUrl`). Use when you need file-system upload convenience methods.
   - `@datocms/cma-client-browser` — Browser-optimized. Adds `createFromFileOrBlob()` for File/Blob uploads.

2. If none is installed, recommend the appropriate package:
   - General / universal → `@datocms/cma-client`
   - Node.js project needing upload helpers → `@datocms/cma-client-node`
   - Browser-only project needing File/Blob uploads → `@datocms/cma-client-browser`

3. Search for existing `buildClient()` calls to understand how the project already configures the client (API token source, environment targeting, etc.).

4. Check for a `.env` or `.env.local` file to see if `DATOCMS_API_TOKEN` (or a similar variable) is already defined.

5. Check for `@datocms/cli` in `devDependencies` and an existing `cma-types.ts` file to determine if CMA type generation is already set up. Do **not** proactively suggest setting up type generation.

**Important:** The CMA requires an API token with `can_access_cma: true` and a role granting the needed permissions (not a read-only CDA token). If you see a token variable named like `DATOCMS_READONLY_API_TOKEN` or `NEXT_PUBLIC_DATOCMS_API_TOKEN`, warn the user that CMA operations need a token with CMA access enabled. The token does not need to be "full-access" — it can be scoped to specific models, actions, and environments via its role.

---

## Step 2: Understand the Task

Ask the user clarifying questions to classify their task into one or more categories:

| Category | Examples |
|---|---|
| **Content operations** | Create, read, update, delete, publish, unpublish records |
| **Upload operations** | Upload files, manage assets, update metadata, bulk tag |
| **Schema operations** | Create/modify models, fields, fieldsets, block models |
| **Filtering & querying** | Search records, filter by fields, paginate large collections |
| **Localization** | Work with localized field values, multi-locale content |
| **Blocks & structured text** | Modular content, inline blocks, DAST structured text |
| **Environment operations** | Fork, promote, rename, delete sandbox environments |
| **Webhook & deploy operations** | Configure webhooks, build triggers, deploy management |
| **Access control** | Create roles, manage API tokens, invite users |
| **Scheduling** | Schedule publish/unpublish, manage workflows |
| **Migration & scripting** | Bulk data operations, content seeding, field migrations |
| **Type generation** | Generate CMA schema types, set up typed record operations, configure `@datocms/cli` |

If the user's request is clear and falls into an obvious category, skip the clarifying questions and proceed directly.

---

## Step 3: Load References

Based on the task classification, use the `Read` tool to load the appropriate reference files from the `references/` directory next to this skill file. **Always** load the core client reference. Only load what is relevant — do not load everything.

**Always load:**
- `references/client-and-types.md` — Client setup, type system, error handling, configuration

**Load per category:**

| Task category | Reference file |
|---|---|
| Content operations (records CRUD) | `references/records.md` |
| Upload operations | `references/uploads.md` |
| Schema operations (models, fields) | `references/schema.md` |
| Filtering & querying | `references/filtering-and-pagination.md` |
| Localization | `references/localization.md` |
| Blocks & structured text | `references/blocks-and-structured-text.md` |
| Environment operations | `references/environments.md` |
| Webhooks & deploy | `references/webhooks-and-triggers.md` |
| Access control | `references/access-control.md` |
| Scheduling & workflows | `references/scheduling.md` |
| Migration & scripting | `references/migration-patterns.md` |
| Type generation (CMA schema types, `@datocms/cli`) | `references/type-generation.md` |

**Load cross-cutting references when needed:**
- If the task involves localized fields in any context → also load `references/localization.md`
- If the task involves modular content or structured text fields → also load `references/blocks-and-structured-text.md`
- If the task involves listing many records → also load `references/filtering-and-pagination.md`
- If the task is a migration script → also load `references/migration-patterns.md` plus whatever domain refs are needed

---

## Step 4: Generate Code

Write the code following these mandatory rules:

### Client Setup
- Always use `buildClient()` from the detected package (Step 1)
- Store the API token in an environment variable, never hardcode it
- Set the `environment` option when working with sandbox environments

### API Surface
- **Always use the simplified API** (e.g., `client.items.create()`) unless the user specifically needs the raw JSON:API format (e.g., `client.items.rawCreate()`)
- The simplified API handles serialization/deserialization automatically

### Pagination
- **Always use `client.items.listPagedIterator()`** (or the equivalent for other resources) when iterating over collections
- Never manually implement offset/limit pagination loops
- Use `for await...of` to consume the async iterator

### Blocks
- **Always use `buildBlockRecord()`** when creating block records for the simplified API
- Import it from the same package as `buildClient`

### Error Handling
- Catch `ApiError` for API failures — it provides `.errors` getter and `.findError()` method
- Catch `TimeoutError` for request timeouts
- Import both from the same package as `buildClient`

### TypeScript
- Follow the TypeScript strictness rules: no `as unknown as`, no unnecessary `as` casts
- Let TypeScript infer types wherever possible
- Use `import type { ... }` for type-only imports

---

## Step 5: Verify

Before presenting the final code:

1. **Token permissions** — CMA operations need a token with CMA access enabled and appropriate role permissions (not a CDA-only read-only token). Schema changes require a role with `can_edit_schema: true`.
2. **Environment targeting** — If working with a sandbox, ensure the `environment` config option is set
3. **Error handling** — Ensure `ApiError` is caught at appropriate boundaries
4. **Pagination** — Ensure `listPagedIterator()` is used for any collection that could exceed a single page
5. **Type safety** — Ensure no type assertions (`as`) are used to silence errors
6. **Imports** — Ensure all imports come from the correct package (the one detected in Step 1)
7. **Generated types** — If the project has generated CMA types (`cma-types.ts`), ensure code uses them with `raw*()` method generics and `RawApiTypes.Item<>` instead of untyped access

If the generated code is a script (migration, seeding, etc.), wrap it in an async function with proper error handling and progress reporting.

---

## Cross-Skill Routing

This skill covers **content management via the REST CMA** (mutations, schema, uploads, webhooks, scripts). If the task involves any of the following, activate the companion skill:

| Condition | Route to |
|---|---|
| Querying content with GraphQL for frontend display | **datocms-cda-skill** |
| Setting up draft mode, Web Previews, Content Link, real-time subscriptions, or framework integration | **datocms-frontend-integrations-skill** |
| Building a DatoCMS plugin | **datocms-pluginsdk-skill** |
