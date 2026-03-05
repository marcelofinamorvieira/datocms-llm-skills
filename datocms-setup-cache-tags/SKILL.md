---
name: datocms-setup-cache-tags
description: >-
  Set up DatoCMS cache tag invalidation for granular content purging. Next.js
  uses framework-centric revalidateTag() with a database for tag storage; Nuxt,
  SvelteKit, and Astro use CDN-first cache tags forwarded via response headers.
  Supports Next.js (App Router), Nuxt, SvelteKit, and Astro. Requires the
  executeQuery wrapper to be already configured.
disable-model-invocation: true
---

# DatoCMS Cache Tags Setup

You are an expert at setting up DatoCMS cache tag invalidation. This skill generates the files needed for granular cache invalidation — only pages affected by a content change are purged, instead of revalidating all DatoCMS content on every change.

**Two approaches exist:**
- **Next.js (framework-centric):** Uses `rawExecuteQuery` with `queryId` to get cache tags, stores them in a database (Turso, Vercel Postgres, etc.), and calls `revalidateTag()` on webhook events.
- **Nuxt / SvelteKit / Astro (CDN-first):** Uses `rawExecuteQuery` to get cache tags, forwards them as CDN response headers, and a webhook handler calls the CDN's purge API.

**CDN header names:**

| CDN | Response header |
|---|---|
| Netlify / Cloudflare | `Cache-Tag` |
| Fastly | `Surrogate-Key` |
| Bunny | `CDN-Tag` |

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

2. **Prerequisite: executeQuery wrapper** — Search for an existing `executeQuery` function that wraps `@datocms/cda-client`. This wrapper is the foundation for cache tags.

   **If executeQuery does not exist, STOP immediately and tell the user:**
   > "The `executeQuery` wrapper must exist before setting up cache tags. Run `datocms-setup-draft-mode` first (Claude Code alias: `/setup-draft-mode`) — it creates the wrapper you need as a foundation."

3. **Existing cache tag setup** — Check for signs that cache tags are already configured:
   - Next.js: Check if `executeQuery` already uses `rawExecuteQuery` with `queryId`, or if a `cache-tags-db` module exists
   - Nuxt: Check if a `useQueryWithCacheTags` composable or `fetchWithCacheTags` server util exists
   - SvelteKit: Check if a `performQueryWithCacheTags` function exists
   - Astro: Check if an `executeQueryWithCacheTags` function exists
   - Any framework: Check if a webhook handler for cache invalidation exists

   If cache tags appear to be already configured, inform the user and ask if they want to replace the existing implementation.

4. **Astro SSR requirement** — If the framework is Astro, check `astro.config.mjs` (or `.ts`) for `output: 'server'` or `output: 'hybrid'`. Cache tags require SSR to set response headers. If the output mode is `'static'` or not set, warn the user that they need SSR mode for cache tags.

5. **Installed deps** — Check `package.json` for: `@datocms/cda-client`

6. **File structure** — Determine whether the project uses a `src/` directory

### Stop conditions

- If the `executeQuery` wrapper does not exist, stop and tell the user to run `datocms-setup-draft-mode` first (Claude Code alias: `/setup-draft-mode`).
- If cache tags are already configured, inform the user and ask if they want to replace them.

---

## Step 2: Ask Questions

### Next.js

Ask which database the user wants for storing cache tag mappings:

- **Turso** (SQLite edge database) — installs `@libsql/client`
- **Vercel Postgres** — installs `@vercel/postgres`
- **Other / I'll figure it out later** — generates the code with a placeholder database interface that the user can implement

### Nuxt / SvelteKit / Astro

Ask which CDN the user is deploying to:

- **Netlify / Cloudflare** — uses `Cache-Tag` header
- **Fastly** — uses `Surrogate-Key` header
- **Bunny** — uses `CDN-Tag` header
- **Other / I'll figure it out later** — generates the code with a generic `Cache-Tag` header and a placeholder purge function

This determines:
- The cache tag response header name (`Cache-Tag`, `Surrogate-Key`, or `CDN-Tag`)
- The webhook handler's purge API call pattern

---

## Step 3: Load References

Use the `Read` tool to load reference files. Load only what is needed.

**Always load:**
- `../datocms-cda-skill/references/draft-caching-environments.md` — for cache tags concepts, webhook payload format, and CDN header table

**Load per framework — focus on the `## Cache Tags (Optional)` section:**

| Framework | Reference file |
|---|---|
| Next.js | `../datocms-frontend-integrations-skill/references/nextjs.md` |
| Nuxt | `../datocms-frontend-integrations-skill/references/nuxt.md` |
| SvelteKit | `../datocms-frontend-integrations-skill/references/sveltekit.md` |
| Astro | `../datocms-frontend-integrations-skill/references/astro.md` |

---

## Step 4: Generate Code

Generate framework-specific cache tag invalidation files following the patterns in the loaded references.

### Next.js (App Router)

1. **Replace `executeQuery`** at `src/lib/datocms/executeQuery.ts` (or `lib/datocms/executeQuery.ts` if no `src/`) — Replace the Core version with one that:
   - Uses `rawExecuteQuery` instead of `executeQuery` from `@datocms/cda-client`
   - Accepts an optional `queryId` option
   - When `queryId` is provided: sets `returnCacheTags: true`, reads the `x-cache-tags` response header, stores the mapping in the DB via `cacheTagsDb.storeTags()`, and tags the `fetch` with `[queryId]`
   - When `queryId` is omitted: falls back to the simple `cacheTag = 'datocms'` single-tag approach (backward compatible)
   - Wrapped in React `cache()` for deduplication
   - Uses `requestInitOptions: { cache: 'force-cache', next: { tags } }` for Next.js caching

2. **Create `cache-tags-db.ts`** in the same directory as `executeQuery` — Database abstraction with:
   - A `CacheTagsDb` interface: `storeTags(queryId, tags)` and `findQueryIdsForTags(tags)`
   - A `query_cache_tags(query_id TEXT, tag TEXT)` join table schema
   - Implementation for the chosen database (Turso with `@libsql/client`, Vercel Postgres with `@vercel/postgres`, or a placeholder interface)
   - Auto-creates the table on first use

3. **Create webhook handler** at `src/app/api/revalidate/route.ts` (or `app/api/revalidate/route.ts` if no `src/`):
   - Validates `Authorization: Bearer <CACHE_INVALIDATION_WEBHOOK_SECRET>`
   - Reads tags from `body?.entity?.attributes?.tags` (this is the DatoCMS webhook payload path)
   - Always calls `revalidateTag(cacheTag)` for the global `'datocms'` tag (for queries without `queryId`)
   - Looks up affected `queryId`s via `cacheTagsDb.findQueryIdsForTags(tags)`
   - Calls `revalidateTag(queryId)` for each affected query

### Nuxt

1. **Create `fetchWithCacheTags` server utility** at `server/middleware/cache-tags.ts` (or `server/utils/cache-tags.ts`) — A wrapper around `rawExecuteQuery` that:
   - Accepts the query and optional variables
   - Calls `rawExecuteQuery` with `returnCacheTags: true`
   - Reads the `x-cache-tags` response header
   - Returns `{ data, cacheTags }`
   - Uses `useRuntimeConfig().public.datocmsPublishedContentCdaToken` for the token

   Optionally also create a composable at `composables/useQueryWithCacheTags.ts` that wraps the server util for use in pages.

2. **Create usage pattern** — Show how to use `fetchWithCacheTags` in a server route or page, setting the CDN header via `setResponseHeader(event, 'Cache-Tag', cacheTags)` (or `Surrogate-Key` / `CDN-Tag` depending on CDN choice). For pages, show using `useRequestEvent()` to access the event.

3. **Create webhook handler** at `server/api/invalidate-cache.ts`:
   - Validates `Authorization: Bearer <cacheInvalidationWebhookSecret>` from `useRuntimeConfig()`
   - Reads tags from `body?.entity?.attributes?.tags`
   - Calls the CDN's purge API with those tags (with commented examples for Fastly, Netlify, Cloudflare, Bunny)

4. **Add runtime config** to `nuxt.config.ts` — Add `cacheInvalidationWebhookSecret` (and CDN-specific vars like `fastlyServiceId`, `fastlyKey`) to `runtimeConfig`:
   ```ts
   runtimeConfig: {
     cacheInvalidationWebhookSecret: '',
     // CDN-specific (uncomment for your CDN):
     // fastlyServiceId: '',
     // fastlyKey: '',
   }
   ```

### SvelteKit

1. **Create `performQueryWithCacheTags` function** at `src/lib/datocms/queries.ts` (or similar) — A wrapper around `rawExecuteQuery` that:
   - Accepts a `RequestEvent`, the query, and optional variables
   - Checks draft mode to select the correct token
   - Calls `rawExecuteQuery` with `returnCacheTags: true`
   - Reads the `x-cache-tags` response header
   - Returns `{ data, cacheTags }`
   - Uses `$env/dynamic/private` for tokens

2. **Create usage pattern** — Show how to use `performQueryWithCacheTags` in a `+page.server.ts` load function, calling `event.setHeaders({ 'Cache-Tag': cacheTags })` (or `Surrogate-Key` / `CDN-Tag` depending on CDN choice)

3. **Create webhook handler** at `src/routes/api/invalidate-cache/+server.ts`:
   - Exports `POST` as a `RequestHandler`
   - Validates `Authorization: Bearer <PRIVATE_CACHE_INVALIDATION_WEBHOOK_SECRET>` from `$env/dynamic/private`
   - Reads tags from `body?.entity?.attributes?.tags`
   - Calls the CDN's purge API with those tags (with commented examples)

### Astro

1. **Create `executeQueryWithCacheTags` function** at `src/lib/datocms/executeQuery.ts` (alongside the existing `executeQuery`) — A wrapper around `rawExecuteQuery` that:
   - Accepts the query and optional `{ variables, includeDrafts }` options
   - Calls `rawExecuteQuery` with `returnCacheTags: true`
   - Reads the `x-cache-tags` response header
   - Returns `{ data, cacheTags }`
   - Imports tokens from `astro:env/server`

2. **Create usage pattern** — Show how to use `executeQueryWithCacheTags` in an `.astro` page (SSR mode), setting response headers via `Astro.response.headers.set('Cache-Tag', cacheTags)` (or `Surrogate-Key` / `CDN-Tag` depending on CDN choice)

3. **Create webhook handler** at `src/pages/api/invalidate-cache.ts`:
   - Exports `POST` as an `APIRoute`
   - Validates `Authorization: Bearer <CACHE_INVALIDATION_WEBHOOK_SECRET>` imported from `astro:env/server`
   - Reads tags from `body?.entity?.attributes?.tags`
   - Calls the CDN's purge API with those tags (with commented examples)

4. **Add env schema entries** in `astro.config.mjs` (or `.ts`) under `env.schema`:
   ```js
   CACHE_INVALIDATION_WEBHOOK_SECRET: envField.string({
     context: 'server',
     access: 'secret',
   }),
   // CDN-specific (uncomment for your CDN):
   // FASTLY_SERVICE_ID: envField.string({ context: 'server', access: 'secret' }),
   // FASTLY_KEY: envField.string({ context: 'server', access: 'secret' }),
   ```

### Mandatory rules for all generated code

#### Security
- All secrets come from environment variables — never hardcode them
- Validate the webhook secret on the invalidation endpoint
- Webhook handlers should return 401 for invalid secrets

#### TypeScript
- No `as unknown as` — this is a forbidden anti-pattern
- No unnecessary `as SomeType` casts
- Let TypeScript infer types wherever possible
- Use `import type { ... }` for type-only imports

#### Env var naming conventions
- Next.js: `process.env.*` (e.g., `CACHE_INVALIDATION_WEBHOOK_SECRET`, `TURSO_DATABASE_URL`, `TURSO_AUTH_TOKEN`)
- Nuxt: `useRuntimeConfig()` with `NUXT_*` env vars (e.g., `NUXT_CACHE_INVALIDATION_WEBHOOK_SECRET`, `NUXT_FASTLY_SERVICE_ID`)
- SvelteKit: `$env/dynamic/private` with `PRIVATE_*` env vars (e.g., `PRIVATE_CACHE_INVALIDATION_WEBHOOK_SECRET`, `PRIVATE_FASTLY_SERVICE_ID`)
- Astro: `astro:env/server` (e.g., `CACHE_INVALIDATION_WEBHOOK_SECRET`, `FASTLY_SERVICE_ID`)

#### File conflicts
- Read existing files before modifying them
- Make targeted additions, not full rewrites
- Skip if already configured

---

## Step 5: Install Dependencies

Install missing packages:

| Package | When |
|---|---|
| `@libsql/client` | Next.js with Turso (if not already installed) |
| `@vercel/postgres` | Next.js with Vercel Postgres (if not already installed) |

For Nuxt, SvelteKit, and Astro: no additional dependencies — `rawExecuteQuery` is provided by `@datocms/cda-client` which should already be installed.

Use the project's package manager (check for `pnpm-lock.yaml`, `yarn.lock`, `bun.lockb`, or default to `npm`).

---

## Step 6: Environment Variables

Add placeholder values to `.env.example` (create if it doesn't exist) and `.env.local` (or `.env` depending on framework convention). Only add variables that don't already exist. Preserve any existing values.

### Next.js
```
CACHE_INVALIDATION_WEBHOOK_SECRET=   # Shared secret to verify webhook requests
TURSO_DATABASE_URL=                  # Turso database URL (or replace with your DB)
TURSO_AUTH_TOKEN=                    # Turso auth token
```

### Nuxt
```
NUXT_CACHE_INVALIDATION_WEBHOOK_SECRET=   # Shared secret to verify webhook requests
# CDN-specific vars (uncomment for your CDN):
# NUXT_FASTLY_SERVICE_ID=                 # Fastly service ID
# NUXT_FASTLY_KEY=                        # Fastly API key
```

### SvelteKit
```
PRIVATE_CACHE_INVALIDATION_WEBHOOK_SECRET=   # Shared secret to verify webhook requests
# CDN-specific vars (uncomment for your CDN):
# PRIVATE_FASTLY_SERVICE_ID=                 # Fastly service ID
# PRIVATE_FASTLY_KEY=                        # Fastly API key
```

### Astro
```
CACHE_INVALIDATION_WEBHOOK_SECRET=   # Shared secret to verify webhook requests
# CDN-specific vars (uncomment for your CDN):
# FASTLY_SERVICE_ID=                 # Fastly service ID
# FASTLY_KEY=                        # Fastly API key
```

---

## Step 7: Next Steps

After generating all files, tell the user:

1. **Create the webhook in DatoCMS** — Go to Project Settings → Webhooks → Create a new webhook:
   - **Name:** "Cache Tags Invalidation" (or similar)
   - **Event type:** Select "Content Delivery API Cache Tags" → "Invalidate" event
   - **URL:** Point to their webhook endpoint:
     - Next.js: `https://your-site.com/api/revalidate`
     - Nuxt: `https://your-site.com/api/invalidate-cache`
     - SvelteKit: `https://your-site.com/api/invalidate-cache`
     - Astro: `https://your-site.com/api/invalidate-cache`
   - **Secret token:** Must match the `CACHE_INVALIDATION_WEBHOOK_SECRET` env var (with framework prefix if applicable)
   - **Payload:** The webhook sends `{ entity: { attributes: { tags: ["tag1", "tag2", ...] } } }`

2. **Usage example** — Show how to use the new function in a page:
   - Next.js: Use the modified `executeQuery` with a `queryId` option (e.g., `queryId: 'blog-post-${slug}'`). Mention adding `export const dynamic = 'force-static'` on pages using cache tags for optimal caching. The `queryId` should be stable and unique per query+variables combination.
   - Nuxt: Use `fetchWithCacheTags` in server routes and set the CDN header on the response via `setResponseHeader(event, 'Cache-Tag', cacheTags)`
   - SvelteKit: Use `performQueryWithCacheTags` in load functions and call `event.setHeaders({ 'Cache-Tag': cacheTags })`
   - Astro: Use `executeQueryWithCacheTags` in `.astro` pages and set `Astro.response.headers.set('Cache-Tag', cacheTags)`. Remind the user that SSR mode (`output: 'server'` or `output: 'hybrid'`) is required.

3. **Testing** — Suggest the user:
   - Deploy the site to their hosting platform
   - Make a content change in DatoCMS
   - Verify that only affected pages are purged (check CDN logs or response headers)

---

## Verification Checklist

Before presenting the final code, verify:

1. The `executeQuery` wrapper (or new variant) uses `rawExecuteQuery` with `returnCacheTags: true` to access cache tags via the `x-cache-tags` response header
2. Next.js: `queryId` is passed to `rawExecuteQuery` and cache tags are stored in a database via `cacheTagsDb.storeTags()`
3. Next.js: Webhook handler calls `revalidateTag()` for both the global `'datocms'` tag and affected `queryId`s
4. Next.js: Pages using cache tags export `dynamic = 'force-static'`
5. Nuxt / SvelteKit / Astro: Cache tags are forwarded as CDN response headers using the correct header name (`Cache-Tag`, `Surrogate-Key`, or `CDN-Tag`)
6. Nuxt / SvelteKit / Astro: Webhook handler calls the CDN's purge API with the invalidated tags
7. All webhook handlers validate the secret via `Authorization: Bearer <secret>` header
8. All webhook handlers read tags from `body?.entity?.attributes?.tags` (the DatoCMS webhook payload path)
9. Nuxt: `cacheInvalidationWebhookSecret` is added to `runtimeConfig` in `nuxt.config.ts`
10. Astro: `CACHE_INVALIDATION_WEBHOOK_SECRET` is added to `env.schema` in `astro.config.mjs` using `envField.string()`
11. Astro: User is warned if output mode is not `'server'` or `'hybrid'` (SSR required for setting response headers)
12. All generated TypeScript follows the mandatory rules (no `as unknown as`, inferred types, `import type`)
13. Environment variables use the correct framework-specific names (`CACHE_INVALIDATION_WEBHOOK_SECRET`, `NUXT_CACHE_INVALIDATION_WEBHOOK_SECRET`, `PRIVATE_CACHE_INVALIDATION_WEBHOOK_SECRET`)

---

## LLM Failure Observer and Self-Heal Routing

The runtime LLM using this skill is the failure observer. The skill file does not self-detect failures.

### Hard Failure Classes (detect continuously)

1. `knowledge_gap`
2. `inaccuracy_or_conflict`
3. `context_bloat_or_ambiguity`
4. `missing_dependency_or_file`
5. `invalid_output_contract`

### Trigger Rule

On the first hard failure:

1. Stop normal execution immediately.
2. Emit a `Skill Failure Packet v1`.
3. Invoke `$skill-self-heal`.
4. Resume this skill only after a `Skill Repair Report v1` is returned.

### Skill Failure Packet v1

```json
{
  "packet_version": "v1",
  "source_skill": "string",
  "timestamp": "ISO-8601 string",
  "hard_failure_type": "knowledge_gap|inaccuracy_or_conflict|context_bloat_or_ambiguity|missing_dependency_or_file|invalid_output_contract",
  "failing_step": "string",
  "user_request": "string",
  "attempted_actions": ["string"],
  "evidence": ["string"],
  "candidate_files": ["/absolute/path"],
  "confidence": 0.0,
  "stop_reason": "string"
}
```

### Skill Repair Report v1

```json
{
  "report_version": "v1",
  "source_packet_id": "string",
  "files_changed": ["/absolute/path"],
  "validation_results": [
    { "name": "string", "pass": true, "evidence": "string" }
  ],
  "rolled_back": false,
  "root_cause": "string",
  "fix_summary": "string",
  "followups": ["string"]
}
```

### Routing Requirements

1. Keep `candidate_files` limited to absolute paths inside this repository.
2. Include concrete evidence in `evidence` (errors, missing paths, contradictions).
3. Set `confidence` from `0.0` to `1.0`.
