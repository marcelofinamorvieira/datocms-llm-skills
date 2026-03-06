---
name: datocms-setup-draft-mode
description: >-
  Set up DatoCMS draft mode with enable/disable endpoints, dual-token
  executeQuery wrapper, and all required utilities. Supports Next.js (App
  Router), Nuxt, SvelteKit, and Astro. Detects the framework automatically,
  generates all files, installs dependencies, and configures environment
  variables.
disable-model-invocation: true
---

# DatoCMS Draft Mode Setup

You are an expert at setting up DatoCMS draft mode for frontend frameworks. This skill generates all files needed for draft mode: enable/disable endpoints, utilities, and an `executeQuery` wrapper with dual-token switching.

**Shared bundle requirement:** This skill reuses references from `datocms-frontend-integrations`. Ensure that companion skill is installed alongside this one so the referenced files are available.

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

2. **Existing draft mode** — Check if draft endpoints already exist:
   - Next.js: `src/app/api/draft-mode/enable/route.ts` or `app/api/draft-mode/enable/route.ts`
   - Nuxt: `server/api/draft-mode/enable.ts`
   - SvelteKit: `src/routes/api/draft-mode/enable/+server.ts`
   - Astro: `src/pages/api/draft-mode/enable/index.ts` or `src/pages/api/draft-mode/enable.ts`

3. **Existing executeQuery wrapper** — Search for an existing `executeQuery` function that wraps `@datocms/cda-client`

4. **Installed deps** — Check `package.json` for: `@datocms/cda-client`, `serialize-error`, `jose`

5. **Env files** — Check `.env`, `.env.local`, `.env.example` for existing DatoCMS tokens

6. **File structure** — Determine whether the project uses a `src/` directory

### Stop conditions

- If the framework cannot be determined, ask the user.
- If draft endpoints already exist, inspect the current implementation first and update it in place by default. Only ask about full replacement if the existing setup is materially different, clearly broken, or the user requested a clean rewrite.

---

## Step 2: Ask Questions

Only ask if inspecting an existing draft mode setup leaves a high-impact ambiguity. Otherwise, zero questions — proceed directly.

---

## Step 3: Load References

Read the relevant reference files. Load only what is needed.

**Always load:**
- `../../../skills/datocms-frontend-integrations/references/draft-mode-concepts.md`

**Load per framework — focus on the `## Core` section:**

| Framework | Reference file |
|---|---|
| Next.js | `../../../skills/datocms-frontend-integrations/references/nextjs.md` |
| Nuxt | `../../../skills/datocms-frontend-integrations/references/nuxt.md` |
| SvelteKit | `../../../skills/datocms-frontend-integrations/references/sveltekit.md` |
| Astro | `../../../skills/datocms-frontend-integrations/references/astro.md` |

---

## Step 4: Generate Code

Create all files following the patterns in the loaded references. Generate:

### Files to generate

1. **Enable endpoint** — Validates `SECRET_API_TOKEN`, sets draft mode cookie, redirects to the requested page
2. **Disable endpoint** — Removes draft mode cookie (no auth required), redirects back
3. **Utilities** — CORS headers helper, generic error handling using `serialize-error`, and `isRelativeUrl()` for redirect validation
4. **executeQuery wrapper** — Wraps `@datocms/cda-client` with:
   - `includeDrafts` option that switches between published and draft CDA tokens
   - `excludeInvalid: true` always set
   - Dual-token architecture (published token for production, draft token for preview)

### Mandatory rules for all generated code

#### Security
- All secrets come from environment variables — never hardcode them
- Validate the `SECRET_API_TOKEN` query parameter on the enable endpoint
- No authentication required on the disable endpoint
- Use `isRelativeUrl()` to validate redirect URLs and prevent open redirect vulnerabilities

#### Cookie Attributes
- `partitioned: true` — Required for CHIPS (third-party cookie partitioning)
- `sameSite: 'none'` — Required because DatoCMS loads the preview in an iframe
- `secure: true` — Required when `sameSite` is `'none'`

#### Framework-Specific Patterns
- Use the framework's native env access pattern:
  - Next.js: `process.env`
  - Nuxt: `useRuntimeConfig()`
  - SvelteKit: `$env/dynamic/private`
  - Astro: `astro:env/server`
- Use the framework's native redirect and response mechanisms
- Non-Next.js frameworks: use `jose` for JWT signing/verification of the draft mode cookie

#### TypeScript
- No `as unknown as` — this is a forbidden anti-pattern
- No unnecessary `as SomeType` casts
- Let TypeScript infer types wherever possible
- Use `import type { ... }` for type-only imports

#### Env var naming conventions
- Next.js: plain `DATOCMS_*` (e.g., `DATOCMS_PUBLISHED_CONTENT_CDA_TOKEN`, `DATOCMS_DRAFT_CONTENT_CDA_TOKEN`, `SECRET_API_TOKEN`, `DRAFT_MODE_SECRET`)
- Nuxt: `NUXT_DATOCMS_*` / `NUXT_PUBLIC_DATOCMS_*` (e.g., `NUXT_DATOCMS_DRAFT_CONTENT_CDA_TOKEN`, `NUXT_SECRET_API_TOKEN`)
- SvelteKit: `PRIVATE_DATOCMS_*` (e.g., `PRIVATE_DATOCMS_DRAFT_CONTENT_CDA_TOKEN`, `PRIVATE_SECRET_API_TOKEN`)
- Astro: plain `DATOCMS_*` with `astro:env/server` schema validation

#### File conflicts
- Read existing files before modifying them
- Make targeted additions, not full rewrites
- Skip if a piece is already configured
- Preserve working existing behavior where possible and patch toward the recommended pattern instead of replacing entire files by default

---

## Step 5: Install Dependencies

Install missing packages:

| Package | When |
|---|---|
| `@datocms/cda-client` | Always (if not already installed) |
| `serialize-error` | Always (if not already installed) |
| `jose` | Non-Next.js frameworks only (for JWT signing) |

Use the project's package manager (check for `pnpm-lock.yaml`, `yarn.lock`, `bun.lockb`, or default to `npm`).

---

## Step 6: Environment Variables

Add placeholder values to `.env.example` (create if it doesn't exist) and `.env.local` (or `.env` depending on framework convention):

### Next.js
```
DATOCMS_PUBLISHED_CONTENT_CDA_TOKEN=your_published_token_here
DATOCMS_DRAFT_CONTENT_CDA_TOKEN=your_draft_token_here
SECRET_API_TOKEN=your_secret_webhook_token_here
DRAFT_MODE_SECRET=run_openssl_rand_hex_32
```

### Nuxt
```
NUXT_DATOCMS_PUBLISHED_CONTENT_CDA_TOKEN=your_published_token_here
NUXT_DATOCMS_DRAFT_CONTENT_CDA_TOKEN=your_draft_token_here
NUXT_SECRET_API_TOKEN=your_secret_webhook_token_here
NUXT_DRAFT_MODE_SECRET=run_openssl_rand_hex_32
```

### SvelteKit
```
PRIVATE_DATOCMS_PUBLISHED_CONTENT_CDA_TOKEN=your_published_token_here
PRIVATE_DATOCMS_DRAFT_CONTENT_CDA_TOKEN=your_draft_token_here
PRIVATE_SECRET_API_TOKEN=your_secret_webhook_token_here
PRIVATE_DRAFT_MODE_SECRET=run_openssl_rand_hex_32
```

### Astro
```
DATOCMS_PUBLISHED_CONTENT_CDA_TOKEN=your_published_token_here
DATOCMS_DRAFT_CONTENT_CDA_TOKEN=your_draft_token_here
SECRET_API_TOKEN=your_secret_webhook_token_here
DRAFT_MODE_SECRET=run_openssl_rand_hex_32
```

Only add variables that don't already exist. Preserve any existing values.

---

## Step 7: Next Steps

After generating all files, tell the user:

1. **Fill in tokens** — Get tokens from DatoCMS Settings → API Tokens:
   - Published Content CDA Token (read-only, published content)
   - Draft Content CDA Token (read-only, draft + published content)
   - Secret API Token (shared secret for webhook validation — can be any random string)

2. **Generate the draft mode secret** — Run: `openssl rand -hex 32`

3. **Suggested next steps:**
   - Run `datocms-setup-web-previews` to add preview links for editors in DatoCMS
   - Run `datocms-setup-content-link` to enable click-to-edit visual editing overlays
   - Run `datocms-setup-realtime` to enable real-time content updates in draft mode

---

## Verification Checklist

Before presenting the final code, verify:

1. Enable endpoint validates `SECRET_API_TOKEN`
2. Enable and disable endpoints validate redirect URLs with `isRelativeUrl()`
3. Cookies have `partitioned: true`, `sameSite: 'none'`, `secure: true`
4. `executeQuery` supports `includeDrafts` with token switching
5. Non-Next.js frameworks use JWT for the draft mode cookie
6. All secrets come from environment variables
7. Disable endpoint does NOT require authentication
8. All generated TypeScript follows the mandatory rules (no `as unknown as`, inferred types, `import type`)
