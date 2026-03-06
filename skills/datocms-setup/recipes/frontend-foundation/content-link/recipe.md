_Internal recipe for `datocms-setup`. Use this file only after the parent skill selects the `content-link` recipe and queues any prerequisites from `../../../references/recipe-manifest.json`._


# DatoCMS Content Link Setup

You are an expert at setting up DatoCMS Content Link — click-to-edit overlays that let editors click any element on the draft site to jump directly to the corresponding field in DatoCMS.

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
   > "Draft mode must be set up before configuring Content Link. Use the `draft-mode` recipe first."

3. **Existing executeQuery wrapper** — Find the `executeQuery` function. It must exist (created by draft mode setup). Check if it already has `contentLink` and `baseEditingUrl` options.

4. **Root layout file** — Find the root layout:
   - Next.js: `src/app/layout.tsx` or `app/layout.tsx`
   - Nuxt: `app.vue` or `layouts/default.vue`
   - SvelteKit: `src/routes/+layout.svelte`
   - Astro: `src/layouts/Layout.astro` or similar

5. **Existing CSP config** — Check if `frame-ancestors` CSP header is already configured

6. **Installed deps** — Check `package.json` for: `@datocms/content-link`, `react-datocms`, `vue-datocms`, `@datocms/svelte`, `@datocms/astro`

### Stop conditions

- If draft mode does not exist, stop and record `draft-mode` as a prerequisite and continue after it is applied.
- If `executeQuery` already has `contentLink: 'v1'` and `baseEditingUrl`, inspect the existing Content Link setup first and update it in place by default. Only ask about full replacement if the current implementation is incompatible or the user explicitly wants a rewrite.

---

## Step 2: Ask Questions

Zero questions. Proceed directly.

---

## Step 3: Load References

Read the relevant reference files. Load only what is needed.

**Always load:**
- `../../../references/shared/datocms-frontend-integrations/content-link-concepts.md`

**Load per framework — focus on the `## Content Link (Optional)` section:**

| Framework | Reference file |
|---|---|
| Next.js | `../../../references/shared/datocms-frontend-integrations/nextjs.md` |
| Nuxt | `../../../references/shared/datocms-frontend-integrations/nuxt.md` |
| SvelteKit | `../../../references/shared/datocms-frontend-integrations/sveltekit.md` |
| Astro | `../../../references/shared/datocms-frontend-integrations/astro.md` |

**Load the framework-appropriate component reference:**

| Framework | Component reference |
|---|---|
| Next.js (React) | `../../../references/shared/datocms-frontend-integrations/react-content-link.md` |
| Nuxt (Vue) | `../../../references/shared/datocms-frontend-integrations/vue-content-link.md` |
| SvelteKit | `../../../references/shared/datocms-frontend-integrations/svelte-content-link.md` |
| Astro | `../../../references/shared/datocms-frontend-integrations/astro-content-link.md` |

---

## Step 4: Modify executeQuery

Modify the existing `executeQuery` wrapper to add Content Link support when in draft mode:

- Add `contentLink: 'v1'` to the query options when `includeDrafts` is true
- Add `baseEditingUrl` (from environment variable) to the query options when `includeDrafts` is true

**Environment variable for baseEditingUrl:**
- Next.js: `DATOCMS_BASE_EDITING_URL`
- Nuxt: `NUXT_PUBLIC_DATOCMS_BASE_EDITING_URL`
- SvelteKit: `PRIVATE_DATOCMS_BASE_EDITING_URL`
- Astro: `DATOCMS_BASE_EDITING_URL`

Read the existing `executeQuery` file first, then make targeted modifications. Do not rewrite the entire file.

---

## Step 5: Generate ContentLink Component

Generate the ContentLink component with framework-specific router integration:

### Next.js (React)
- Create a `ContentLink` client component that wraps `@datocms/content-link`
- Wire `onNavigateTo` to Next.js `router.push()`
- Wire `currentPath` to `usePathname()`
- Include `enableClickToEdit` and `stripStega` props

### Nuxt (Vue)
- Create a `ContentLink` component using `vue-datocms`
- Wire `on-navigate-to` to `navigateTo()` from Nuxt
- Wire `current-path` to `useRoute().path`
- Use kebab-case props

### SvelteKit
- Create a `ContentLink` component using `@datocms/svelte`
- Wire `onNavigateTo` to `goto` from `$app/navigation`
- Wire `currentPath` to `$page.url.pathname` from `$app/stores`
- Use camelCase props

### Astro
- Use `<ContentLink />` from `@datocms/astro/ContentLink`
- Only 2 props: `enableClickToEdit` and `stripStega`
- No `onNavigateTo` or `currentPath` — auto-detects via `astro:page-load` events

---

## Step 6: Add ContentLink to Root Layout

Modify the root layout to include the `<ContentLink />` component. It should only render when in draft mode.

Read the existing layout file first, then make targeted additions.

---

## Step 7: Add CSP Header

If not already configured, add the Content Security Policy header:
```
frame-ancestors 'self' https://plugins-cdn.datocms.com
```

This is required for DatoCMS to embed the site in an iframe for visual editing.

---

## Step 8: Install Dependencies

Install missing packages:

| Package | When |
|---|---|
| `@datocms/content-link` | Always (if not already installed) |

The framework-specific component library (`react-datocms`, `vue-datocms`, `@datocms/svelte`, `@datocms/astro`) should already be installed or will be installed here if missing.

Use the project's package manager (check for `pnpm-lock.yaml`, `yarn.lock`, `bun.lockb`, or default to `npm`).

---

## Step 9: Environment Variables

Add the base editing URL placeholder to env files:

- Next.js: `DATOCMS_BASE_EDITING_URL=https://your-project.admin.datocms.com`
- Nuxt: `NUXT_PUBLIC_DATOCMS_BASE_EDITING_URL=https://your-project.admin.datocms.com`
- SvelteKit: `PRIVATE_DATOCMS_BASE_EDITING_URL=https://your-project.admin.datocms.com`
- Astro: `DATOCMS_BASE_EDITING_URL=https://your-project.admin.datocms.com`

Only add if not already present.

---

## Step 10: Next Steps

After generating all files, tell the user:

1. **Find your editing URL** — Go to DatoCMS Settings → your environment. The base editing URL looks like `https://your-project.admin.datocms.com`.

2. **Keyboard shortcut** — Editors can hold Alt (Option on Mac) while hovering to see clickable Content Link overlays.

3. **CSS fix** — If you see extra spacing in text content due to stega encoding, add this CSS:
   ```css
   [data-datocms-cle] { letter-spacing: normal !important; }
   ```

4. **Suggested next steps:**
   - Use `datocms-setup` for `realtime` to enable real-time content updates in draft mode

---

## Mandatory Rules for All Generated Code

### TypeScript
- No `as unknown as` — this is a forbidden anti-pattern
- No unnecessary `as SomeType` casts
- Let TypeScript infer types wherever possible
- Use `import type { ... }` for type-only imports

### File conflicts
- Read existing files before modifying them
- Make targeted additions, not full rewrites
- Skip if already configured
- Preserve working existing behavior and patch toward the recommended pattern instead of replacing entire files by default

---

## Verification Checklist

Before presenting the final code, verify:

1. `executeQuery` has `contentLink: 'v1'` and `baseEditingUrl` when `includeDrafts` is true
2. ContentLink component is created with correct framework-specific router integration
3. `<ContentLink />` is added to root layout, conditional on draft mode
4. CSP header `frame-ancestors 'self' https://plugins-cdn.datocms.com` is configured
5. Astro ContentLink uses only 2 props (`enableClickToEdit`, `stripStega`) — no `onNavigateTo` or `currentPath`
6. `DATOCMS_BASE_EDITING_URL` env var is added (with framework-appropriate prefix)
7. All generated TypeScript follows the mandatory rules (no `as unknown as`, inferred types, `import type`)
