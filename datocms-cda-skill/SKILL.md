---
name: datocms-cda
description: >-
  Query the DatoCMS Content Delivery API (CDA) — a read-only GraphQL API — using
  the official @datocms/cda-client TypeScript/JavaScript library. Use when users
  want to fetch records, filter and paginate collections, query localized content
  with fallbacks, work with modular content blocks, render structured text (DAST),
  display responsive images with imgix transformations and placeholders, handle
  SEO meta tags and favicons, query Mux videos, use draft/preview mode, target
  sandbox environments, integrate cache tags for CDN invalidation, enable Content
  Link for visual editing, or perform any client-side or server-side DatoCMS
  content reading operation.
---

# DatoCMS Content Delivery API Skill

You are an expert at querying the DatoCMS Content Delivery API (CDA) using `@datocms/cda-client`. The CDA is a **read-only GraphQL API** — it has no mutations. All content changes go through the CMA (Content Management API). Follow these steps in order. Do not skip steps.

---

## Step 1: Detect Context

Silently examine the project to determine setup and configuration.

1. Read `package.json` and check for `@datocms/cda-client`.
   - If not installed, recommend: `npm install @datocms/cda-client`

2. Search for existing `executeQuery` or `rawExecuteQuery` imports to understand how the project already uses the CDA client.

3. Check `.env`, `.env.local`, or similar files for a DatoCMS API token. Look for variable names like:
   - `DATOCMS_CDA_TOKEN`
   - `DATOCMS_READONLY_TOKEN`
   - `DATOCMS_API_TOKEN`
   - `NEXT_PUBLIC_DATOCMS_CDA_TOKEN`

4. Check the framework context (Next.js, Astro, Remix, Nuxt, SvelteKit, etc.) to determine whether queries run on the server or client. CDA queries work in both environments, but tokens should not be exposed to the browser unless the project intentionally uses a public read-only token.

**Important:** The CDA needs a **read-only API token** (or a full-access CMA token, which also works). If you see a token named `DATOCMS_API_TOKEN` used for CMA operations, the user may need a separate read-only token for the CDA, or they can reuse the CMA token if appropriate.

---

## Step 2: Understand the Task

Classify the user's task into one or more categories:

| Category | Examples |
|---|---|
| **Basic querying** | Fetch records by slug/ID, query single-instance models, list collections |
| **Filtering** | Filter by field values, AND/OR logic, meta field filters, deep filtering |
| **Pagination & ordering** | Paginate large collections, sort results, tree/hierarchical queries |
| **Localization** | Query localized fields, fallback locales, all-locale values |
| **Modular content** | Query block fields with GraphQL fragments, nested blocks |
| **Structured text** | Query DAST value/blocks/links, render with framework components |
| **Images & media** | Responsive images, imgix transforms, placeholders, focal points, video |
| **SEO & meta** | `_seoMetaTags`, favicons, `globalSeo`, Open Graph tags |
| **Draft/preview & caching** | Draft mode, strict mode, cache tags, CDN invalidation, Content Link |

If the user's request is clear, skip clarifying questions and proceed directly.

---

## Step 3: Load References

Based on the task classification, use the `Read` tool to load the appropriate reference files from the `references/` directory next to this skill file. **Always** load the core client reference. Only load what is relevant — do not load everything.

**Always load:**
- `references/client-and-config.md` — Client setup, options, error handling, limits, scalars

**Load per category:**

| Task category | Reference file |
|---|---|
| Basic querying (records, collections, meta) | `references/querying-basics.md` |
| Filtering (field filters, AND/OR, deep filtering, uploads) | `references/filtering.md` |
| Pagination & ordering (first/skip, auto-pagination, trees) | `references/pagination-and-ordering.md` |
| Localization | `references/localization.md` |
| Modular content (blocks, fragments) | `references/modular-content.md` |
| Structured text (DAST, rendering) | `references/structured-text.md` |
| Images & media (responsiveImage, video) | `references/images-and-videos.md` |
| SEO & meta tags | `references/seo-and-meta.md` |
| Draft/preview, caching, environments, Content Link | `references/draft-caching-environments.md` |

**Load cross-cutting references when needed:**
- If filtering localized fields → also load `references/localization.md`
- If querying modular content inside structured text → also load `references/modular-content.md`
- If querying images inside blocks → also load `references/images-and-videos.md`
- If paginating a large filtered collection → also load `references/pagination-and-ordering.md`
- If the query involves complex nesting → also load `references/pagination-and-ordering.md` for complexity costs

---

## Step 4: Generate Code

Write the code following these mandatory rules:

### Client Usage
- **Always use `executeQuery`** from `@datocms/cda-client` (not raw `fetch`)
- Use **`executeQueryWithAutoPagination`** when fetching more than 500 records
- Use **`rawExecuteQuery`** only when you need response headers (e.g., cache tags)
- Store the API token in an environment variable — never hardcode it

### GraphQL Queries
- Write queries as **template literal strings** (unless the project uses `TypedDocumentNode` / `gql.tada`)
- Use **GraphQL variables** for all dynamic values — never use string interpolation in queries
- Request **only the fields you need** — do not over-fetch
- Use DatoCMS custom scalars in variable declarations (e.g., `$first: IntType`, `$id: ItemId`)

### Structured Text
- Always query **all relevant sub-fields** (`value`, `blocks`, `links`, `inlineBlocks`) when the structured text field uses them — omitting any causes silent data loss

### Error Handling
- Catch `ApiError` from `@datocms/cda-client` at appropriate boundaries
- Do **not** add custom retry logic — `autoRetry` handles rate limits automatically

### TypeScript
- Follow the TypeScript strictness rules: no `as unknown as`, no unnecessary `as` casts
- Let TypeScript infer types wherever possible
- Use `import type { ... }` for type-only imports

---

## Step 5: Verify

Before presenting the final code:

1. **Token** — Ensure the token comes from an environment variable and has read permissions
2. **Error handling** — Ensure `ApiError` is caught at appropriate boundaries
3. **Pagination** — If the collection could exceed 500 records, use `executeQueryWithAutoPagination`
4. **Draft mode** — If `includeDrafts` is used, ensure it is intentional (not accidentally showing unpublished content in production)
5. **`excludeInvalid`** — Recommend for stable schemas. If the schema is changing (migrations, new required fields), use `filter: { _isValid: { eq: true } }` instead to avoid re-validation errors
6. **Type safety** — No type assertions (`as`) used to silence errors
7. **Imports** — All imports come from `@datocms/cda-client`
8. **Variables** — All dynamic values use GraphQL variables, not string interpolation
9. **Structured text completeness** — If querying structured text, all relevant sub-fields (`value`, `blocks`, `links`, `inlineBlocks`) are included
