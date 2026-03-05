---
name: datocms-setup-realtime
description: >-
  Set up DatoCMS real-time content updates for draft mode. Generates
  framework-specific subscription components and usage patterns for live content
  streaming via SSE. Supports Next.js (App Router), Nuxt, SvelteKit, and Astro.
  Requires draft mode to be already configured.
disable-model-invocation: true
---

# DatoCMS Real-Time Updates Setup

You are an expert at setting up DatoCMS real-time content updates. This skill generates the components and patterns needed for live content streaming in draft mode, so editors see content changes without page reload.

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
   > "Draft mode must be set up before configuring real-time updates. Run `datocms-setup-draft-mode` first (Claude Code alias: `/setup-draft-mode`)."

3. **Content Link setup** — Check if Content Link is configured (look for `contentLink: 'v1'` in the `executeQuery` wrapper). If Content Link is set up, the real-time subscription options should include `contentLink` and `baseEditingUrl` as well.

4. **Existing realtime utilities** — Check for existing subscription components or patterns

5. **Installed deps** — Check `package.json` for: `react-datocms`, `vue-datocms`, `@datocms/svelte`, `@datocms/astro`

### Stop conditions

- If draft mode does not exist, stop and tell the user to run `datocms-setup-draft-mode` first (Claude Code alias: `/setup-draft-mode`).
- If realtime components already exist, inform the user and ask if they want to replace them.

---

## Step 2: Ask Questions

Zero questions. Proceed directly.

---

## Step 3: Load References

Use the `Read` tool to load reference files. Load only what is needed.

**Always load:**
- `../datocms-frontend-integrations-skill/references/realtime-concepts.md`

**Load per framework — focus on the `## Real-Time Updates (Optional)` section:**

| Framework | Reference file |
|---|---|
| Next.js | `../datocms-frontend-integrations-skill/references/nextjs.md` |
| Nuxt | `../datocms-frontend-integrations-skill/references/nuxt.md` |
| SvelteKit | `../datocms-frontend-integrations-skill/references/sveltekit.md` |
| Astro | `../datocms-frontend-integrations-skill/references/astro.md` |

**Load the framework-appropriate component reference:**

| Framework | Component reference |
|---|---|
| Next.js (React) | `../datocms-frontend-integrations-skill/references/react-realtime.md` |
| Nuxt (Vue) | `../datocms-frontend-integrations-skill/references/vue-realtime.md` |
| SvelteKit | `../datocms-frontend-integrations-skill/references/svelte-realtime.md` |
| Astro | `../datocms-frontend-integrations-skill/references/astro-realtime.md` |

---

## Step 4: Generate Code

Generate framework-specific real-time update components and patterns:

### Next.js (React)

Generate two files in `src/lib/datocms/realtime/` (or `lib/datocms/realtime/` if no `src/`):

1. **`generateRealtimeComponent.tsx`** — A factory function that creates a real-time wrapper component for any page. Takes a `useQuerySubscription`-compatible config and returns a client component that:
   - Uses `useQuerySubscription` from `react-datocms`
   - Passes `includeDrafts`, `excludeInvalid`, and the draft CDA token
   - If Content Link is configured: passes `contentLink` and `baseEditingUrl`
   - Renders the page component with live data

2. **`generatePageComponent.tsx`** — A factory function that creates the server/client page split. Takes the static page component and the GraphQL query, returns a component that:
   - In draft mode: renders the real-time wrapper
   - In production: renders the static page component

### Nuxt (Vue)

Generate a usage pattern/example showing how to use `useQuerySubscription` composable from `vue-datocms`:
- Wrap existing page data fetching with the composable
- Pass `includeDrafts`, `excludeInvalid`, and the draft CDA token
- If Content Link is configured: pass `contentLink` and `baseEditingUrl`
- Access `data`, `error`, `status` as Vue `Ref` values

### SvelteKit

Generate a usage pattern/example showing how to use `querySubscription` store from `@datocms/svelte`:
- Create a Svelte store with `querySubscription()`
- Access with `$subscription` syntax
- Use `$: ({ data, error, status } = $subscription)` for reactive destructuring
- Pass `includeDrafts`, `excludeInvalid`, and the draft CDA token
- If Content Link is configured: pass `contentLink` and `baseEditingUrl`

### Astro

Generate a usage pattern/example showing how to use `<QueryListener />` from `@datocms/astro/QueryListener`:
- Import from `@datocms/astro/QueryListener` (subpath import)
- `<QueryListener />` triggers page reload on content changes (NOT live data like React/Vue/Svelte)
- Options must match the `executeQuery` options (token, includeDrafts, excludeInvalid)
- If Content Link is configured: pass `contentLink` and `baseEditingUrl`
- Only render in draft mode context

### Mandatory rules for all generated code

#### Subscription options
- Pass the draft CDA token (not the published token) for real-time subscriptions
- Always include `includeDrafts: true` and `excludeInvalid: true`
- If Content Link is configured, include `contentLink: 'v1'` and `baseEditingUrl`

#### TypeScript
- No `as unknown as` — this is a forbidden anti-pattern
- No unnecessary `as SomeType` casts
- Let TypeScript infer types wherever possible
- Use `import type { ... }` for type-only imports

#### Env var conventions
Follow the same conventions as draft mode for accessing the draft CDA token:
- Next.js: `process.env.DATOCMS_DRAFT_CONTENT_CDA_TOKEN`
- Nuxt: `useRuntimeConfig().datocms.draftContentCdaToken`
- SvelteKit: `PRIVATE_DATOCMS_DRAFT_CONTENT_CDA_TOKEN` from `$env/dynamic/private`
- Astro: from `astro:env/server`

#### File conflicts
- Read existing files before modifying them
- Make targeted additions, not full rewrites
- Skip if already configured

---

## Step 5: Install Dependencies

Install missing packages:

| Package | When |
|---|---|
| `react-datocms` | Next.js (if not already installed) |
| `vue-datocms` | Nuxt (if not already installed) |
| `@datocms/svelte` | SvelteKit (if not already installed) |
| `@datocms/astro` | Astro (if not already installed) |

Use the project's package manager (check for `pnpm-lock.yaml`, `yarn.lock`, `bun.lockb`, or default to `npm`).

---

## Step 6: Next Steps

After generating all files, tell the user:

1. **How to convert an existing page** — Provide a concrete, framework-specific example showing how to take an existing page that fetches data with `executeQuery` and make it real-time in draft mode. Show the before and after.

2. **SSE connection limit** — Note that DatoCMS allows up to 500 concurrent SSE connections per project. Each open browser tab in draft mode uses one connection.

3. **Testing** — Suggest the user:
   - Enter draft mode on their site
   - Open the DatoCMS editor in another tab
   - Edit content and verify it appears in real-time on the site

---

## Verification Checklist

Before presenting the final code, verify:

1. Real-time subscription passes the draft CDA token (not published)
2. Subscription includes `includeDrafts: true` and `excludeInvalid: true`
3. If Content Link is configured, subscription includes `contentLink` and `baseEditingUrl`
4. Next.js: `generateRealtimeComponent.tsx` and `generatePageComponent.tsx` are created
5. Nuxt: usage example uses `useQuerySubscription` composable correctly with Vue refs
6. SvelteKit: usage example uses `querySubscription` store with `$subscription` syntax
7. Astro: uses `<QueryListener />` from subpath import, triggers page reload (not live data)
8. Astro: `<QueryListener />` only renders in draft mode
9. All generated TypeScript follows the mandatory rules (no `as unknown as`, inferred types, `import type`)
