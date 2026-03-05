---
name: datocms-setup-web-previews
description: >-
  Set up the DatoCMS Web Previews plugin integration with a preview-links
  endpoint, CORS handling, token validation, and record-to-URL routing. Supports
  Next.js (App Router), Nuxt, SvelteKit, and Astro. Requires draft mode to be
  already configured.
disable-model-invocation: true
---

# DatoCMS Web Previews Setup

You are an expert at setting up the DatoCMS Web Previews plugin integration. This skill generates a preview-links endpoint that returns draft/published URLs for records, enabling editors to preview content directly from the DatoCMS UI.

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
   - Astro: `src/pages/api/draft-mode/enable.ts`

   **If draft mode does not exist, STOP immediately and tell the user:**
   > "Draft mode must be set up before configuring Web Previews. Run `datocms-setup-draft-mode` first (Claude Code alias: `/setup-draft-mode`)."

3. **Existing preview-links endpoint** — Check if a preview-links endpoint already exists:
   - Next.js: `src/app/api/preview-links/route.ts` or `app/api/preview-links/route.ts`
   - Nuxt: `server/api/preview-links.ts`
   - SvelteKit: `src/routes/api/preview-links/+server.ts`
   - Astro: `src/pages/api/preview-links.ts`

4. **Existing utilities** — Check for CORS helper and error handling utilities (likely created by draft mode setup)

5. **Installed deps** — Check `package.json` for: `@datocms/rest-client-utils`

6. **File structure** — Determine whether the project uses a `src/` directory

### Stop conditions

- If draft mode does not exist, stop and tell the user to run `datocms-setup-draft-mode` first (Claude Code alias: `/setup-draft-mode`).
- If a preview-links endpoint already exists, inform the user and ask: "A preview-links endpoint already exists. Do you want me to replace it?"

---

## Step 2: Ask Questions

Ask one question:

> "What are your content models and their frontend URL patterns? For example:
> - `blog_post` → `/blog/[slug]`
> - `page` → `/[slug]`
> - `home_page` → `/`
>
> You can skip this and I'll add TODO placeholders for you to fill in later."

Use the user's answer to populate the `recordToWebsiteRoute` switch statement. If the user skips, use TODO placeholders like:
```typescript
// TODO: Add your content models and URL patterns here
// Example: case 'blog_post': return `/blog/${record.slug}`;
```

---

## Step 3: Load References

Use the `Read` tool to load reference files. Load only what is needed.

**Always load:**
- `../datocms-frontend-integrations-skill/references/web-previews-concepts.md`

**Load per framework — focus on the `## Web Previews (Optional)` section:**

| Framework | Reference file |
|---|---|
| Next.js | `../datocms-frontend-integrations-skill/references/nextjs.md` |
| Nuxt | `../datocms-frontend-integrations-skill/references/nuxt.md` |
| SvelteKit | `../datocms-frontend-integrations-skill/references/sveltekit.md` |
| Astro | `../datocms-frontend-integrations-skill/references/astro.md` |

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
- Use `handleUnexpectedError` (from the utilities created by draft mode setup) that catches `ApiError` from `@datocms/cma-client` and uses `serialize-error` for other errors
- Return proper error status codes

#### TypeScript
- No `as unknown as` — this is a forbidden anti-pattern
- No unnecessary `as SomeType` casts
- Let TypeScript infer types wherever possible
- Use `import type { ... }` for type-only imports

#### Env var conventions
Follow the same conventions as draft mode:
- Next.js: `SECRET_API_TOKEN`
- Nuxt: `NUXT_SECRET_API_TOKEN`
- SvelteKit: `PRIVATE_SECRET_API_TOKEN`
- Astro: `SECRET_API_TOKEN`

#### File conflicts
- Read existing files before modifying them
- Reuse utilities created by draft mode setup (CORS, error handling, `isRelativeUrl`)
- Skip if already configured

---

## Step 5: Install Dependencies

Install missing packages:

| Package | When |
|---|---|
| `@datocms/rest-client-utils` | Next.js only (if not already installed) |

Other dependencies (`@datocms/cma-client`, `serialize-error`) should already be installed from draft mode setup.

Use the project's package manager (check for `pnpm-lock.yaml`, `yarn.lock`, `bun.lockb`, or default to `npm`).

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

2. **Fill in URL patterns** (if TODO placeholders were used): Update the `recordToWebsiteRoute` function with your actual content models and URL patterns.

3. **Suggested next steps:**
   - Run `datocms-setup-content-link` (Claude Code alias: `/setup-content-link`) to enable click-to-edit visual editing overlays
   - Run `datocms-setup-realtime` (Claude Code alias: `/setup-realtime`) to enable real-time content updates in draft mode

---

## Verification Checklist

Before presenting the final code, verify:

1. Preview-links endpoint validates `SECRET_API_TOKEN`
2. CORS headers are included on all responses (including errors and OPTIONS)
3. `handleUnexpectedError` catches `ApiError` and uses `serialize-error`
4. `recordToWebsiteRoute` has correct switch statement with user's models (or TODO placeholders)
5. Status branching returns both draft and published links
6. Draft links use the enable endpoint URL with correct parameters
7. CSP header `frame-ancestors 'self' https://plugins-cdn.datocms.com` is configured
8. All generated TypeScript follows the mandatory rules (no `as unknown as`, inferred types, `import type`)

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
