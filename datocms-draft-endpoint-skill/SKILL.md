---
name: datocms-draft-endpoint
description: >-
  Add authenticated draft mode endpoints and optional features to an existing
  DatoCMS project. Core: enable/disable API routes with dual-token architecture
  and draft content querying. Optional features (independently selectable):
  Web Previews plugin integration (preview links from the DatoCMS UI),
  Content Link (click-to-edit overlays for visual editing), and real-time
  content update subscriptions. Supports Next.js (App Router), Nuxt,
  SvelteKit, and Astro.
---

# DatoCMS Draft Mode Endpoint Skill

You are an expert at setting up authenticated draft mode endpoints for DatoCMS projects. This skill supports 4 features with a modular architecture:

- **Core Draft Mode** (always included) — Enable/disable endpoints, dual-token architecture, draft content querying
- **Web Previews** (optional) — Preview links endpoint for the DatoCMS Web Previews plugin
- **Content Link** (optional) — Click-to-edit overlays connecting website elements to DatoCMS fields
- **Real-Time Updates** (optional) — Live content streaming so editors see changes without page reload

Follow these steps in order. Do not skip steps.

---

## Step 1: Detect Context (silent)

Silently examine the project to determine setup and configuration.

1. **Framework** — Read `package.json` and check for:
   - `next` → Next.js (App Router)
   - `nuxt` → Nuxt
   - `@sveltejs/kit` → SvelteKit
   - `astro` → Astro

2. **Existing DatoCMS setup** — Check for:
   - `@datocms/cda-client` in dependencies
   - An existing `executeQuery` wrapper (search for imports of `executeQuery` from `@datocms/cda-client` or a local wrapper)
   - Environment variable files (`.env`, `.env.local`, `.env.example`) for existing DatoCMS tokens

3. **Existing draft mode** — Check if draft endpoints already exist:
   - Next.js: `src/app/api/draft-mode/` or `app/api/draft-mode/`
   - Nuxt: `server/api/draft-mode/`
   - SvelteKit: `src/routes/api/draft-mode/`
   - Astro: `src/pages/api/draft-mode/`

4. **File structure** — Determine whether the project uses a `src/` directory or not (check for `src/app`, `src/routes`, `src/pages`, etc.)

**Stop conditions:**
- If the framework cannot be determined, inform the user and ask them to specify which framework they are using.
- If `@datocms/cda-client` is not installed, tell the user to install it first: `npm install @datocms/cda-client`
- If draft endpoints already exist, inform the user and ask if they want to replace or update them.

---

## Step 2: Ask Questions

Ask the user these questions (skip any that the user's request already answers):

1. **Web Previews plugin integration**: "Do you want to add a preview-links endpoint for the DatoCMS Web Previews plugin? This lets editors preview draft/published versions of records directly from the DatoCMS UI."

2. **Content Link (visual editing)**: "Do you want to enable Content Link? This adds click-to-edit overlays on your draft site — editors can click any element to jump to the corresponding field in DatoCMS. Includes support for text fields (automatic via stega encoding), non-text fields (via `data-datocms-content-link-url` with `_editingUrl`), structured text with embedded blocks, and stega stripping utilities for SEO/comparisons."

3. **Real-time updates**: "Do you want draft content to update in real-time without page reload? This uses subscription-based updates so editors see changes instantly."
   - For Next.js and SvelteKit, this is a well-established pattern.
   - For Nuxt, mention that `vue-datocms` provides `useQuerySubscription` for this.
   - For Astro, mention that `@datocms/astro` provides a `QueryListener` component.

4. **Content models** (only ask if Web Previews was selected): "What are your main content models and their frontend URL patterns? For example: `blog_post` → `/blog/[slug]`, `page` → `/[slug]`. I need this to configure the `recordToWebsiteRoute` function that maps DatoCMS records to frontend URLs."

---

## Step 3: Load References

Use the `Read` tool to load the appropriate reference files from the `references/` directory next to this skill file.

**Always load:**
- `references/draft-mode-concepts.md` — Core concepts (token validation, cookies, open redirect prevention, etc.)

**Load per framework:**

| Framework | Reference file |
|-----------|----------------|
| Next.js (App Router) | `references/nextjs.md` |
| Nuxt | `references/nuxt.md` |
| SvelteKit | `references/sveltekit.md` |
| Astro | `references/astro.md` |

**Conditionally load based on Step 2 answers:**

| Feature selected | Load |
|---|---|
| Web Previews | `references/web-previews-concepts.md` |
| Content Link | `references/content-link-concepts.md` |
| Real-time updates | `references/realtime-concepts.md` |

---

## Step 4: Generate Code

Create all files following the patterns in the loaded references. The framework reference files are organized with section markers:

- **`## Core`** — Always follow. Generates enable/disable endpoints, utils, draft mode helper, and query function with `includeDrafts` + token switching.
- **`## Web Previews (Optional)`** — Only follow if the user selected Web Previews. Generates the preview-links endpoint and `recordToWebsiteRoute`.
- **`## Content Link (Optional)`** — Only follow if the user selected Content Link. Adds `contentLink` and `baseEditingUrl` to the query function, sets up the ContentLink component with client-side routing support, and includes structured text group/boundary patterns, non-text field handling with `_editingUrl`, and stega stripping examples.
- **`## Real-Time Updates (Optional)`** — Only follow if the user selected Real-time updates. Generates subscription setup code.

### Mandatory Rules (apply to all generated code)

#### Security
- All secrets (API tokens, JWT secrets) come from environment variables — never hardcode them
- Validate the `SECRET_API_TOKEN` query parameter on the enable endpoint (and preview-links endpoint if Web Previews is selected)
- No authentication required on the disable endpoint (it only removes the draft cookie)
- Use `isRelativeUrl()` to validate redirect URLs and prevent open redirect vulnerabilities

#### Cookie Attributes (for iframe support)
- `partitioned: true` — Required for CHIPS (third-party cookie partitioning)
- `sameSite: 'none'` — Required because DatoCMS loads the preview in an iframe
- `secure: true` — Required when `sameSite` is `'none'`

#### Framework-Specific Patterns
- Use the framework's native env access pattern (e.g., `process.env` for Next.js, `useRuntimeConfig()` for Nuxt, `$env/dynamic/private` for SvelteKit, `astro:env/server` for Astro)
- Use the framework's native redirect mechanism
- Use the framework's native JSON response helpers

#### Query Function Modification
- Modify the existing `executeQuery` wrapper (or create one) to:
  - Accept an `includeDrafts` option
  - Switch between published and draft CDA tokens based on `includeDrafts`
  - Always set `excludeInvalid: true`
  - If Content Link was selected: enable `contentLink: 'v1'` and pass `baseEditingUrl` when `includeDrafts` is true

#### TypeScript
- Follow TypeScript strictness rules: no `as unknown as`, no unnecessary `as` casts
- Let TypeScript infer types wherever possible
- Use `import type { ... }` for type-only imports

#### Dependencies
- Install required packages that are missing from the project

---

## Step 5: Guide DatoCMS Setup

After generating the code, tell the user to complete these setup steps. Only include steps for features that were selected.

### Always (Core)

1. **Create API tokens** in DatoCMS (Settings → API tokens):
   - A **Published Content CDA Token** — with access to published content only
   - A **Draft Content CDA Token** — with access to draft content (check "Include drafts" when creating)

2. **Generate a SECRET_API_TOKEN** — a random string used to authenticate requests from DatoCMS to your endpoints. You can generate one with: `openssl rand -hex 32`

3. **Set environment variables** — list all required env vars with descriptions (these are framework-specific, detailed in the reference)

### If Web Previews was selected

4. **Install the "Web Previews" plugin** in DatoCMS (Settings → Plugins → Add), and configure it:
   - Set the "Preview webhook URL" to: `{YOUR_SITE_URL}/api/preview-links?token={SECRET_API_TOKEN}`
   - (Next.js uses this exact path; other frameworks have slight variations — refer to the generated code)

5. **Fill in `recordToWebsiteRoute`** — the user must add their own content models to the switch statement, mapping each model's ID (or api_key for Astro) to the frontend URL pattern

6. **Add CSP header** — Add `Content-Security-Policy: frame-ancestors 'self' https://plugins-cdn.datocms.com` to allow the Web Previews plugin to embed your site in an iframe (needed for sidebar preview and Visual editing tab). Framework-specific CSP setup is in each framework reference file.

### If Content Link was selected

7. **Set `DATOCMS_BASE_EDITING_URL`** (or framework-specific equivalent) — This enables Content Link (click-to-edit overlays). The value is found in DatoCMS under Settings → Environment settings. It looks like: `https://{project-slug}.admin.datocms.com/environments/{environment-name}`

### If Real-Time Updates was selected

8. **Install the real-time subscription package** for the framework (listed in the framework reference's Real-Time Dependencies section)

---

## Step 6: Verify

Before presenting the final code, check the items relevant to what was generated:

### Always (Core)
1. **Token validation** — Enable endpoint checks `SECRET_API_TOKEN`
2. **Open redirect prevention** — Enable and disable endpoints validate redirect URLs with `isRelativeUrl()`
3. **Cookie attributes** — `partitioned: true`, `sameSite: 'none'`, `secure: true` on all cookie operations
4. **Query function** — Modified to support `includeDrafts` and token switching
5. **JWT signing** (non-Next.js frameworks) — Draft mode cookie uses JWT signed with a secret
6. **Environment variables** — All secrets come from env vars, none are hardcoded
7. **No auth on disable** — The disable endpoint does not require a token

### If Web Previews was selected
8. **CORS** — Preview-links endpoint includes CORS headers and handles OPTIONS requests
9. **Preview-links token validation** — Preview-links endpoint checks `SECRET_API_TOKEN`
10. **Error handling** — `handleUnexpectedError` catches `ApiError` from `@datocms/cma-client` and uses `serialize-error` for other errors
11. **CSP header** — `frame-ancestors 'self' https://plugins-cdn.datocms.com` is configured

### If Content Link was selected
12. **Content Link in query function** — `contentLink: 'v1'` and `baseEditingUrl` are set when `includeDrafts` is true
13. **ContentLink component** — Includes `enableClickToEdit()`, `onNavigateTo` for routing, and `setCurrentPath` for path sync

### If Real-Time Updates was selected
14. **Subscription setup** — Real-time subscription code passes the correct token, `includeDrafts`, and `excludeInvalid` options
15. **Dependencies** — All required subscription packages are listed for installation
