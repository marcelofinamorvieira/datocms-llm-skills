---
name: datocms-cma
description: >-
  Interact with the DatoCMS Content Management API (CMA) using
  @datocms/cma-client, @datocms/cma-client-node, or @datocms/cma-client-browser.
  Use when users need programmatic CMA scripts: create/update/delete/publish
  records, bulk import/export (including CSV pipelines), paginate through large
  record sets, upload assets from URL/local files and set metadata, update
  structured text or block payloads, create/modify schema (models/fields/blocks),
  fork/promote environments, configure webhooks and build triggers, manage roles
  and API tokens, schedule publish/unpublish workflows, and generate CMA schema
  types for type-safe record operations.
---

# DatoCMS Content Management API Skill

You are an expert at writing code that interacts with the DatoCMS Content Management API (CMA). Use this workflow as a default. Reorder or skip steps when the task is purely diagnostic, advisory, or the user only needs an explanation.

---

## Step 1: Detect Context

If the project context is already established in this conversation (client
package, token variable, environment targeting), skip broad detection below.
Re-inspect only when a question cannot be answered from prior context.

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

Classify the user's task into one or more categories. Ask follow-up questions only when the request is ambiguous or the risk of a wrong assumption is high.

- **Content operations** — Create, read, update, delete, publish, or unpublish records
- **Upload operations** — Upload files, manage assets, update metadata, bulk tag
- **Schema operations** — Create or modify models, fields, fieldsets, block models
- **Filtering & querying** — Search records, filter by fields, paginate large collections
- **Localization** — Work with localized field values and multi-locale content
- **Blocks & modular content** — Modular content fields, single-block fields, nested block payloads
- **Structured text & block tooling** — DAST payloads, embedded blocks, block traversal, debugging helpers
- **Environment operations** — Fork, promote, rename, delete sandbox environments
- **Webhook & deploy operations** — Configure webhooks, build triggers, deploy management
- **Access control** — Create roles, manage API tokens, invite users
- **Scheduling** — Schedule publish/unpublish, manage workflows
- **Migration & scripting** — Bulk data operations, content seeding, field migrations
- **Type generation** — Generate CMA schema types or wire typed record operations

If the user's request is clear and falls into an obvious category, skip the clarifying questions and proceed directly.

---

## Step 3: Load References

Based on the task classification, read the appropriate reference files from the `references/` directory next to this skill file. Prefer section-level reads inside long references by using each file's Quick Navigation section first. Only load what is relevant.

**Always load:**
- `references/client-setup-and-errors.md` — Package choice, client setup, token/environment config, error handling

**Load per category:**

- `Content operations` → `references/records.md`
- `Upload operations` → `references/uploads.md`
- `Schema operations` → `references/schema.md`
- `Filtering & querying` → `references/filtering-and-pagination.md`
- `Localization` → `references/localization.md`
- `Blocks & modular content` → `references/block-records-and-modular-content.md`
- `Structured text & block tooling` → `references/structured-text-and-block-tools.md`
- `Environment operations` → `references/environments.md`
- `Webhook & deploy operations` → `references/webhooks-and-triggers.md`
- `Access control` → `references/access-control.md`
- `Scheduling` → `references/scheduling.md`
- `Migration & scripting` → `references/migration-patterns.md`
- `Type generation` → `references/type-generation.md`

**Load cross-cutting references when needed:**
- If the task involves localized fields in any context → also load `references/localization.md`
- If the task uses `raw*()` methods, generated CMA types, advanced client behavior, or platform limits → also load `references/client-types-and-behaviors.md`
- If the task involves modular content or single-block fields → also load `references/block-records-and-modular-content.md`
- If the task involves DAST structured text, `SchemaRepository`, `inspectItem()`, or block traversal utilities → also load `references/structured-text-and-block-tools.md`
- If the task involves listing many records → also load `references/filtering-and-pagination.md`
- If the task is a migration script → also load `references/migration-patterns.md` plus whatever domain refs are needed

---

## Step 4: Generate the Solution

When the response includes code, follow these default rules:

### Client Setup
- Default to `buildClient()` from the detected package (Step 1)
- Store the API token in an environment variable, never hardcode it
- Set the `environment` option when working with sandbox environments

### API Surface
- Default to the simplified API (e.g., `client.items.create()`) because it handles serialization/deserialization automatically
- Switch to `raw*()` methods only when the task explicitly needs raw JSON:API payloads, relationship metadata, or generated CMA schema types are intentionally part of the solution

### Pagination
- Prefer `*.listPagedIterator()` (for example `client.items.listPagedIterator()`) when iterating over collections
- Avoid manual offset/limit pagination loops unless a resource genuinely lacks an iterator
- Use `for await...of` to consume async iterators

### Blocks
- Prefer `buildBlockRecord()` when creating block records for the simplified API
- Import it from the same package as `buildClient`

### Error Handling
- Catch `ApiError` for API failures — it provides `.errors` getter and `.findError()` method
- Catch `TimeoutError` for request timeouts in long-running or request-heavy flows
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
4. **Pagination** — If the solution iterates a collection that could exceed a single page, prefer `listPagedIterator()`
5. **Type safety** — Ensure no type assertions (`as`) are used to silence errors
6. **Imports** — Ensure all imports come from the correct package (the one detected in Step 1)
7. **Generated types** — If the solution intentionally uses generated CMA types (`cma-types.ts`), ensure `raw*()` method generics and `RawApiTypes.Item<>` usage are deliberate and typed end to end

If the generated code is a script (migration, seeding, etc.), wrap it in an async function with proper error handling and progress reporting.

---

## Cross-Skill Routing

This skill covers **content management via the REST CMA** (mutations, schema, uploads, webhooks, scripts). If the task involves any of the following, activate the companion skill:

| Condition | Route to |
|---|---|
| CLI commands, migration scaffolding, `datocms schema:generate`, or environment operations via `npx datocms` | **datocms-cli** |
| Querying content with GraphQL for frontend display | **datocms-cda** |
| Setting up draft mode, Web Previews, Content Link, real-time subscriptions, or framework integration | **datocms-frontend-integrations** |
| Building a DatoCMS plugin | **datocms-plugin-builder** |
