_Internal recipe for `datocms-setup`. Use this file only after the parent skill selects the `web-previews` recipe and queues any prerequisites from `../../../references/recipe-manifest.json`._


# DatoCMS Web Previews Setup

You are an expert at setting up the DatoCMS Web Previews plugin integration. This recipe generates a preview-links endpoint that returns draft/published URLs for records, enabling editors to preview content directly from the DatoCMS UI.

See `../../../patterns/OUTPUT_STATUS.md` for output status definitions.

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

2. **Prerequisite: Draft mode** — Check if the draft mode enable endpoint exists:
   - Next.js: `src/app/api/draft-mode/enable/route.ts` or `app/api/draft-mode/enable/route.ts`
   - Nuxt: `server/api/draft-mode/enable.ts`
   - SvelteKit: `src/routes/api/draft-mode/enable/+server.ts`
   - Astro: `src/pages/api/draft-mode/enable/index.ts` or `src/pages/api/draft-mode/enable.ts`

   **If draft mode does not exist, STOP immediately and tell the user:**
   > "Draft mode must be set up before configuring Web Previews. Use the `draft-mode` recipe first."

3. **Existing preview-links endpoint** — Check if a preview-links endpoint already exists:
   - Next.js: `src/app/api/preview-links/route.ts` or `app/api/preview-links/route.ts`
   - Nuxt: `server/api/preview-links.ts`
   - SvelteKit: `src/routes/api/preview-links/+server.ts`
   - Astro: `src/pages/api/preview-links/index.ts` or `src/pages/api/preview-links.ts`

4. **Existing utilities** — Check for CORS helper and error handling utilities (likely created by draft mode setup)

5. **Installed deps** — Check `package.json` for: `@datocms/rest-client-utils`

6. **File structure** — Determine whether the project uses a `src/` directory

### Stop conditions

- If draft mode does not exist, stop and record `draft-mode` as a prerequisite and continue after it is applied.
- If a preview-links endpoint already exists, inspect it first and update it in place by default. Only ask about full replacement if the current implementation is materially incompatible or the user requested a rewrite.

---

## Step 2: Ask Questions

Ask one question:

> "What are your content models and their frontend URL patterns? For example:
> - `blog_post` → `/blog/[slug]`
> - `page` → `/[slug]`
> - `home_page` → `/`
>
> You can skip this and I'll scaffold TODO placeholders for you to fill in later. That result is `scaffolded`, not `production-ready`."

Use the user's answer to populate the `recordToWebsiteRoute` switch statement. If the user skips, use TODO placeholders like:
```typescript
// TODO: Add your content models and URL patterns here
// Example: case 'blog_post': return `/blog/${record.slug}`;
```

If placeholders are used, record the exact missing model-to-route mappings and include them in the final handoff.

---

## Step 3: Load References

Read the relevant reference files. Load only what is needed.

**Always load:**
- `../../../references/shared/datocms-frontend-integrations/web-previews-concepts.md`

**Load per framework — focus on the `## Web Previews (Optional)` section:**

| Framework | Reference file |
|---|---|
| Next.js | `../../../references/shared/datocms-frontend-integrations/nextjs.md` |
| Nuxt | `../../../references/shared/datocms-frontend-integrations/nuxt.md` |
| SvelteKit | `../../../references/shared/datocms-frontend-integrations/sveltekit.md` |
| Astro | `../../../references/shared/datocms-frontend-integrations/astro.md` |

---

## Step 4: Generate Code

Create all files following the patterns in the loaded references. Generate:

### Files to generate

1. **Preview-links endpoint** — Handles POST requests from the DatoCMS Web Previews plugin:
   - CORS headers and OPTIONS preflight handling
   - `SECRET_API_TOKEN` validation
   - `recordToWebsiteRoute` function that maps DatoCMS records to frontend URLs
   - Status branching: returns both draft and published links with appropriate labels
   - Uses the draft mode enable endpoint URL for draft links

2. **recordInfo helper** (if applicable per framework reference) — Helper to fetch record details using the CMA client when needed for URL generation

3. **CSP header configuration** — Add `frame-ancestors 'self' https://plugins-cdn.datocms.com` to the framework's response headers config

### Mandatory rules for all generated code

#### Security
- Validate `SECRET_API_TOKEN` on the preview-links endpoint
- CORS headers must be present on all responses (including error responses)
- Handle OPTIONS preflight requests

#### Error handling
- Reuse `handleUnexpectedError` from the draft mode utilities so error responses stay consistent across endpoints
- Return proper error status codes

#### TypeScript
Follow the TypeScript rules in `../../../patterns/MANDATORY_RULES.md`.

#### Env var conventions
Follow the env conventions in `../../../patterns/MANDATORY_RULES.md`.

Recipe-specific env var names:
- Next.js: `SECRET_API_TOKEN`
- Nuxt: `NUXT_SECRET_API_TOKEN`
- SvelteKit: `PRIVATE_SECRET_API_TOKEN`
- Astro: `SECRET_API_TOKEN`

#### File conflicts
Follow the file conflict rules in `../../../patterns/MANDATORY_RULES.md`.
- Reuse utilities created by draft mode setup (CORS, error handling, `isRelativeUrl`)

#### Output status
- Report `scaffolded` if `recordToWebsiteRoute` still contains TODO placeholder cases or if any required model-to-route mapping is missing
- Report `production-ready` only when every required mapping is implemented with real customer routes and no routing TODOs remain

---

## Step 5: Install Dependencies

Install missing packages:

| Package | When |
|---|---|
| `@datocms/rest-client-utils` | Next.js only (if not already installed) |
| `@datocms/cma-client` | Always (if not already installed) — needed for `RawApiTypes` / `ApiTypes` used by record-routing helpers |

`serialize-error` should already be installed from draft mode setup.

Use the project's package manager (see `../../../patterns/MANDATORY_RULES.md`).

---

## Step 6: Next Steps

After generating all files, tell the user:

1. **Configure the Web Previews plugin in DatoCMS:**
   - Go to Settings → Plugins → Web Previews
   - Set the webhook URL to your preview-links endpoint:
     - Next.js: `https://your-site.com/api/preview-links`
     - Nuxt: `https://your-site.com/api/preview-links`
     - SvelteKit: `https://your-site.com/api/preview-links`
     - Astro: `https://your-site.com/api/preview-links`
   - Add the `SECRET_API_TOKEN` as a query parameter: `?token=YOUR_SECRET_TOKEN`

2. **If the result is `scaffolded`**: list the exact missing model-to-route mappings and tell the user to replace the TODO cases in `recordToWebsiteRoute` before treating the setup as production-ready.

3. **If the result is `production-ready`**: explicitly say the preview routing has all required mappings and can be treated as ready for customer use.

4. **Suggested next steps:**
   - Use `datocms-setup` for `content-link` to enable click-to-edit visual editing overlays
   - Use `datocms-setup` for `realtime` to enable real-time content updates in draft mode

---

## Verification Checklist

Before presenting the final code, verify the correct output state.

### Base scaffold checks

1. Preview-links endpoint validates `SECRET_API_TOKEN`
2. CORS headers are included on all responses (including errors and OPTIONS)
3. `handleUnexpectedError` from the draft mode setup is reused for consistent serialized error responses
4. Status branching returns both draft and published links
5. Draft links use the enable endpoint URL with correct parameters
6. CSP header `frame-ancestors 'self' https://plugins-cdn.datocms.com` is configured
7. All generated TypeScript follows the mandatory rules (no `as unknown as`, inferred types, `import type`)

### Production-ready checks

1. Report `scaffolded` and list the missing mappings if `recordToWebsiteRoute` still contains TODO placeholder cases
2. Report `production-ready` only when `recordToWebsiteRoute` contains real customer mappings for every required model and no routing TODOs remain
