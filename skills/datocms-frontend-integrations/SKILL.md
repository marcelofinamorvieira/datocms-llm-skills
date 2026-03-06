---
name: datocms-frontend-integrations
description: >-
  DatoCMS front-end integrations for existing web projects (Next.js App Router,
  Nuxt, SvelteKit, Astro, plus React/Vue/Svelte component usage). Use when users
  ask to set up draft mode endpoints, Web Previews preview-links APIs, Content
  Link visual editing, real-time preview updates/subscriptions, or cache-tag
  invalidation/revalidation flows (Next.js revalidateTag or CDN purge by tags).
  Also use for framework component/hook wiring with react-datocms, vue-datocms,
  @datocms/svelte, and @datocms/astro: Image/SRCImage/datocms-image,
  StructuredText, VideoPlayer (React/Vue/Svelte), SEO/meta helpers
  (renderMetaTags/toHead/Seo), QuerySubscription/QueryListener realtime patterns,
  ContentLink components, Site Search (React/Vue or custom API usage), and
  robots/sitemap generation patterns for DatoCMS-powered sites.
---

# DatoCMS Front-End Integrations Skill

You are an expert at setting up DatoCMS front-end integrations and using `react-datocms`, `vue-datocms`, `@datocms/svelte`, and `@datocms/astro` components, hooks, and stores. This skill covers three domains:

- **Setup tasks** — Draft mode endpoints, Web Previews plugin, Content Link visual editing, real-time update subscriptions (Next.js, Nuxt, SvelteKit, Astro)
- **React components & hooks** — `<Image>`, `<SRCImage>`, `<StructuredText>`, `<VideoPlayer>`, SEO utilities, `useQuerySubscription`, `<ContentLink>`, `useSiteSearch` (React-based projects: Next.js, Remix, Astro w/ React, plain React)
- **Vue components & composables** — `<datocms-image>`, `<datocms-naked-image>`, `<datocms-structured-text>`, `<VideoPlayer>`, `toHead()`, `useQuerySubscription`, `<ContentLink>`, `useSiteSearch` (Vue-based projects: Nuxt, plain Vue)
- **Svelte components & stores** — `<Image>`, `<NakedImage>`, `<StructuredText>`, `<VideoPlayer>`, `<Head>`, `querySubscription`, `<ContentLink>` (Svelte/SvelteKit projects). Note: site search is not available in `@datocms/svelte`.
- **Astro components** — `<Image>`, `<StructuredText>`, `<Seo>`, `<QueryListener>`, `<ContentLink>` (Astro projects using `@datocms/astro`). Note: video player and site search are not available in `@datocms/astro`.
- **Search / crawl infrastructure** — low-level Site Search API usage outside React/Vue widgets, plus robots.txt and sitemap patterns that work correctly with DatoCMS Search Indexes

Follow these steps in order. Do not skip steps.

---

## Step 1: Detect Context (silent)

Silently examine the project to determine setup and configuration.

1. **Framework** — Read `package.json` and check for:
   - `next` → Next.js (App Router)
   - `nuxt` → Nuxt
   - `@sveltejs/kit` → SvelteKit
   - `astro` → Astro
   - If none match, check for `react` / `react-dom` → plain React or React-based framework

2. **React-based, Vue-based, Svelte, or Astro?** — Determine the UI library:
   - **React-based** (Next.js, Remix, Astro with React integration, plain React) → uses `react-datocms`
   - **Vue-based** (Nuxt, plain Vue) → uses `vue-datocms`
   - **SvelteKit** → uses `@datocms/svelte`
   - **Astro** (without React integration) → uses `@datocms/astro` (native Astro components). Note: if the Astro project uses React integration and has `react-datocms` installed, prefer `react-datocms` for components. If the project uses `@datocms/astro`, use its native components.

3. **Existing DatoCMS setup** — Check for:
   - `@datocms/cda-client` in dependencies
   - An existing `executeQuery` wrapper (search for imports of `executeQuery` from `@datocms/cda-client` or a local wrapper)
   - `react-datocms` in dependencies (React projects)
   - `vue-datocms` in dependencies (Vue projects)
   - `@datocms/svelte` in dependencies (Svelte/SvelteKit projects)
   - `@datocms/astro` in dependencies (Astro projects)
   - Environment variable files (`.env`, `.env.local`, `.env.example`) for existing DatoCMS tokens

4. **Existing draft mode** — Check if draft endpoints already exist:
   - Next.js: `src/app/api/draft-mode/` or `app/api/draft-mode/`
   - Nuxt: `server/api/draft-mode/`
   - SvelteKit: `src/routes/api/draft-mode/`
   - Astro: `src/pages/api/draft-mode/`

5. **File structure** — Determine whether the project uses a `src/` directory or not

**Stop conditions:**
- If the framework cannot be determined, ask the user to specify which framework they are using.
- If the task requires CDA queries and `@datocms/cda-client` is not installed, tell the user to install it: `npm install @datocms/cda-client`
- If the task requires react-datocms components and `react-datocms` is not installed, tell the user to install it: `npm install react-datocms`
- If the task requires vue-datocms components and `vue-datocms` is not installed, tell the user to install it: `npm install vue-datocms`
- If the task requires @datocms/svelte components and `@datocms/svelte` is not installed, tell the user to install it: `npm install @datocms/svelte`
- If the task requires @datocms/astro components and `@datocms/astro` is not installed, tell the user to install it: `npm install @datocms/astro`
- If draft endpoints already exist and the user wants draft mode setup, inform them and ask if they want to replace or update.

---

## Step 2: Classify the Task

Classify the user's request into one or more categories:

| Category | When to select |
|---|---|
| **Draft Mode Setup** | User wants to set up draft mode endpoints (enable/disable, token architecture, draft content querying) |
| **Web Previews Setup** | User wants to add the Web Previews plugin integration (preview links from DatoCMS UI) |
| **Responsive Images** | User wants to display DatoCMS images (React / Vue / Svelte / Astro) |
| **Structured Text Rendering** | User wants to render DatoCMS Structured Text fields (React / Vue / Svelte / Astro) |
| **Video Player** | User wants to integrate DatoCMS/Mux video (React / Vue / Svelte — not available in @datocms/astro) |
| **SEO & Meta Tags** | User wants to render `_seoMetaTags` and favicons with SEO utilities (React / Vue / Svelte / Astro) |
| **Real-Time Updates** | User wants live content updates via subscriptions (React / Vue / Svelte / Astro) |
| **Visual Editing / Content Link** | User wants click-to-edit overlays for editors (React / Vue / Svelte / Astro) |
| **Site Search** | User wants to build a search UI with DatoCMS Site Search (React / Vue via widgets, or other stacks via the low-level Search API) |
| **Robots & Sitemaps** | User wants `robots.txt`, sitemap routes, sitemap indexes, or DatoCMS crawler-specific allow/disallow rules |
| **Cache Tags** | User wants granular per-record cache invalidation using DatoCMS cache tags |

Multiple categories can apply (e.g., "set up draft mode with content link and real-time updates", or "display images and render structured text with visual editing overlays").

If the user's request is clear, skip clarifying questions and proceed directly. Only ask clarifying questions when the intent is genuinely ambiguous.

### Draft Mode Setup Sub-Flow

When the task is classified as **Draft Mode Setup**, ask these additional questions (skip any the user's request already answers):

1. **Web Previews**: "Do you want to add a preview-links endpoint for the DatoCMS Web Previews plugin? This lets editors preview draft/published versions of records directly from the DatoCMS UI."

2. **Content Link (visual editing)**: "Do you want to enable Content Link? This adds click-to-edit overlays on your draft site — editors can click any element to jump to the corresponding field in DatoCMS."

3. **Real-time updates**: "Do you want draft content to update in real-time without page reload?"
   - For Nuxt, mention that `vue-datocms` provides `useQuerySubscription`.
   - For Astro with `@datocms/astro`, mention that it provides a `<QueryListener />` component that triggers page reloads on content changes (not live data updates).
   - For Astro with React integration, mention that `react-datocms` provides `useQuerySubscription` for live data updates.

4. **Content models** (only if Web Previews was selected): "What are your main content models and their frontend URL patterns? For example: `blog_post` → `/blog/[slug]`, `page` → `/[slug]`."

5. **Cache tags**: "Do you want granular cache invalidation using DatoCMS cache tags? Instead of revalidating all content on every change, this invalidates only the pages affected by the specific records that changed." Mention the prerequisites: Next.js needs a small database for tag mappings; other frameworks need a CDN with tag-based purging (Netlify, Cloudflare, Fastly, Bunny).

---

## Step 3: Load References

Read the reference files from the `references/` directory next to this skill file. Only load what is relevant — do not load everything.

### Draft Mode Setup References

**Always load for draft mode setup:**
- `references/draft-mode-concepts.md`

**Load per framework (for draft mode setup):**

| Framework | Reference file |
|---|---|
| Next.js (App Router) | `references/nextjs.md` |
| Nuxt | `references/nuxt.md` |
| SvelteKit | `references/sveltekit.md` |
| Astro | `references/astro.md` |

**Conditionally load based on draft mode sub-flow answers:**

| Feature selected | Load |
|---|---|
| Web Previews | `references/web-previews-concepts.md` |
| Content Link (SvelteKit / Astro without React) | `references/content-link-concepts.md` |
| Real-time updates (SvelteKit / Astro without React) | `references/realtime-concepts.md` |

### React Component/Hook References

Load based on the task categories identified in Step 2. These only apply to **React-based** projects.

| Category | Reference file |
|---|---|
| Responsive Images | `references/react-image.md` |
| Structured Text Rendering | `references/react-structured-text.md` |
| Video Player | `references/react-video-player.md` |
| SEO & Meta Tags | `references/react-seo.md` |
| Real-Time Updates (React project) | `references/react-realtime.md` |
| Visual Editing / Content Link (React project) | `references/react-content-link.md` |
| Site Search | `references/react-site-search.md` |

### Vue Component/Composable References

Load based on the task categories identified in Step 2. These only apply to **Vue-based** projects (Nuxt, plain Vue).

| Category | Reference file |
|---|---|
| Responsive Images | `references/vue-image.md` |
| Structured Text Rendering | `references/vue-structured-text.md` |
| Video Player | `references/vue-video-player.md` |
| SEO & Meta Tags | `references/vue-seo.md` |
| Real-Time Updates (Vue project) | `references/vue-realtime.md` |
| Visual Editing / Content Link (Vue project) | `references/vue-content-link.md` |
| Site Search | `references/vue-site-search.md` |

### Svelte Component/Store References

Load based on the task categories identified in Step 2. These only apply to **Svelte/SvelteKit** projects.

| Category | Reference file |
|---|---|
| Responsive Images | `references/svelte-image.md` |
| Structured Text Rendering | `references/svelte-structured-text.md` |
| Video Player | `references/svelte-video-player.md` |
| SEO & Meta Tags | `references/svelte-seo.md` |
| Real-Time Updates (Svelte project) | `references/svelte-realtime.md` |
| Visual Editing / Content Link (Svelte project) | `references/svelte-content-link.md` |

**Note:** There is no `svelte-site-search.md` — use
`references/site-search-api.md` for Svelte/SvelteKit site-search work.

### Astro Component References

Load based on the task categories identified in Step 2. These only apply to **Astro** projects using `@datocms/astro`.

| Category | Reference file |
|---|---|
| Responsive Images | `references/astro-image.md` |
| Structured Text Rendering | `references/astro-structured-text.md` |
| SEO & Meta Tags | `references/astro-seo.md` |
| Real-Time Updates (Astro project) | `references/astro-realtime.md` |
| Visual Editing / Content Link (Astro project) | `references/astro-content-link.md` |

**Note:** There is no `astro-video-player.md` or `astro-site-search.md` —
video player and Site Search widgets are not available in `@datocms/astro`. If
users need video in Astro, they should use the `@mux/mux-player` web component
directly or use React's `<VideoPlayer>` via Astro's React integration.

### Generic Search / Crawl References

Load these when the user's stack does not map cleanly to the React/Vue widget
references or when the task is specifically about crawler behavior:

| Category | Reference file |
|---|---|
| Site Search API (generic) | `references/site-search-api.md` |
| Robots & Sitemaps | `references/robots-and-sitemaps.md` |

**Note on React vs Vue vs Svelte vs Astro vs non-JS-framework for Content Link and Real-Time:**
- For React-based projects, load `react-content-link.md` and/or `react-realtime.md`
- For Vue-based projects, load `vue-content-link.md` and/or `vue-realtime.md`
- For Svelte/SvelteKit projects, load `svelte-content-link.md` and/or `svelte-realtime.md`
- For Astro projects using `@datocms/astro`, load `astro-content-link.md` and/or `astro-realtime.md`
- For non-React/non-Vue/non-Svelte/non-Astro projects, load `content-link-concepts.md` and/or `realtime-concepts.md` + the framework reference
- If both draft mode setup AND the component are needed (e.g., "set up draft mode with Content Link in Next.js"), load both the framework reference and the React/Vue/Svelte/Astro reference

---

## Step 4: Generate Code

Create all files following the patterns in the loaded references. Apply these rules to all generated code:

### Mandatory Rules

#### Security (Draft Mode Setup only)
- All secrets (API tokens, JWT secrets) come from environment variables — never hardcode them
- Validate the `SECRET_API_TOKEN` query parameter on the enable endpoint (and preview-links endpoint if Web Previews is selected)
- No authentication required on the disable endpoint (it only removes the draft cookie)
- Use `isRelativeUrl()` to validate redirect URLs and prevent open redirect vulnerabilities

#### Cookie Attributes (Draft Mode Setup only)
- `partitioned: true` — Required for CHIPS (third-party cookie partitioning)
- `sameSite: 'none'` — Required because DatoCMS loads the preview in an iframe
- `secure: true` — Required when `sameSite` is `'none'`

#### Framework-Specific Patterns (Draft Mode Setup only)
- Use the framework's native env access pattern (`process.env` for Next.js, `useRuntimeConfig()` for Nuxt, `$env/dynamic/private` for SvelteKit, `astro:env/server` for Astro)
- Use the framework's native redirect and response mechanisms

#### Query Function Modification (Draft Mode Setup only)
- Modify the existing `executeQuery` wrapper (or create one) to:
  - Accept an `includeDrafts` option
  - Switch between published and draft CDA tokens based on `includeDrafts`
  - Always set `excludeInvalid: true`
  - If Content Link was selected: enable `contentLink: 'v1'` and pass `baseEditingUrl` when `includeDrafts` is true

#### TypeScript (all generated code)
- No `as unknown as` — this is a forbidden anti-pattern
- No unnecessary `as SomeType` casts
- Let TypeScript infer types wherever possible
- Use `import type { ... }` for type-only imports

#### Astro Subpath Imports (Astro projects only)
- `@datocms/astro` uses subpath imports: `@datocms/astro/Image`, `@datocms/astro/StructuredText`, `@datocms/astro/Seo`, `@datocms/astro/QueryListener`, `@datocms/astro/ContentLink`
- Never import from `@datocms/astro` directly — always use the subpath

#### Dependencies (all generated code)
- Install required packages that are missing from the project
- For React `<VideoPlayer>`: ensure `@mux/mux-player-react` is installed
- For Vue `<VideoPlayer>`: ensure `@mux/mux-player` is installed (note: the web component, not the React package)
- For Svelte `<VideoPlayer>`: ensure `@mux/mux-player` is installed (same web component as Vue, not the React package)
- For `useSiteSearch` (React or Vue): ensure `@datocms/cma-client-browser` is installed

#### Output status (scaffold-capable tasks)
- Report `scaffolded` if Web Previews route mappings, Cache Tags provider details, or Site Search index IDs are still missing
- Report `production-ready` only when those customer-specific values are present and no related TODO placeholder logic remains

---

## Step 5: Verify

Before presenting the final code, check the items relevant to what was generated.

### Draft Mode Setup Checks

#### Always (Core)
1. **Token validation** — Enable endpoint checks `SECRET_API_TOKEN`
2. **Open redirect prevention** — Enable and disable endpoints validate redirect URLs with `isRelativeUrl()`
3. **Cookie attributes** — `partitioned: true`, `sameSite: 'none'`, `secure: true` on all cookie operations
4. **Query function** — Modified to support `includeDrafts` and token switching
5. **JWT signing** (non-Next.js frameworks) — Draft mode cookie uses JWT signed with a secret
6. **Environment variables** — All secrets from env vars, none hardcoded
7. **No auth on disable** — Disable endpoint does not require a token

#### If Web Previews was selected
8. **CORS** — Preview-links endpoint includes CORS headers and handles OPTIONS requests
9. **Preview-links token validation** — Preview-links endpoint checks `SECRET_API_TOKEN`
10. **Error handling** — `handleUnexpectedError` is reused so unexpected API errors are serialized consistently
11. **CSP header** — `frame-ancestors 'self' https://plugins-cdn.datocms.com` is configured

#### If Content Link was selected
12. **Content Link in query function** — `contentLink: 'v1'` and `baseEditingUrl` set when `includeDrafts` is true
13. **ContentLink component** — Includes `enableClickToEdit()`, `onNavigateTo` for routing, `setCurrentPath` for path sync

#### If Real-Time Updates was selected
14. **Subscription setup** — Passes correct token, `includeDrafts`, and `excludeInvalid` options
15. **Dependencies** — All required subscription packages listed for installation

#### If Cache Tags was selected
16. **Query function** — Next.js: `rawExecuteQuery` with `queryId` indirection and DB persistence. Other frameworks: `rawExecuteQuery` with `returnCacheTags: true`, forwarding tags as CDN headers.
17. **Webhook handler** — Verifies auth, reads `entity.attributes.tags`, triggers invalidation (Next.js: `revalidateTag()`; others: CDN purge API)
18. **Environment variables** — Webhook secret + framework-specific vars (Next.js: DB connection; others: CDN API credentials)

### React Component/Hook Checks

#### Responsive Images (React)
16. **GraphQL query** — Uses `responsiveImage` with `{ auto: format }` in imgixParams
17. **Component choice** — `<SRCImage>` for RSC/zero-JS, `<Image>` for crossfade/transparency
18. **No redundant fields** — Not requesting both `bgColor` and `base64`; `srcSet` omitted when possible

#### Structured Text (React)
19. **GraphQL fragment** — Includes `id` and `__typename` on all `links`, `blocks`, `inlineBlocks`
20. **Custom renderers** — Switch on `record.__typename` with default null case
21. **Content Link boundaries** — If Content Link is active, group/boundary attributes are present

#### Video Player (React)
22. **Peer dependency** — `@mux/mux-player-react` is installed
23. **GraphQL query** — Includes at minimum `muxPlaybackId`

#### SEO & Meta Tags (React)
24. **Tag concatenation** — Uses `[...page.seo, ...site.favicon]` pattern
25. **Framework-appropriate utility** — `toNextMetadata()` for Next.js, `toRemixMeta()` for Remix, `renderMetaTags()` for others

#### Real-Time Updates (React)
26. **Fetcher definition** — `fetcher` (if custom) defined as `const` outside component scope
27. **Draft mode integration** — Passes `includeDrafts`, `excludeInvalid`, `contentLink`, `baseEditingUrl` when in draft context

#### Content Link (React)
28. **Stega encoding enabled** — `contentLink: 'v1'` and `baseEditingUrl` in API calls
29. **Component mounted** — `<ContentLink />` in root layout/provider
30. **Framework navigation** — `onNavigateTo` and `currentPath` wired to router

#### Site Search (React)
31. **CMA client** — `@datocms/cma-client-browser` installed and `buildClient()` used
32. **Search index ID** — A real index ID is configured before calling the result `production-ready`; if it is missing, mark the result `scaffolded` and list the missing ID

### Vue Component/Composable Checks

#### Responsive Images (Vue)
33. **GraphQL query** — Uses `responsiveImage` with `{ auto: format }` in imgixParams
34. **Component choice** — `<datocms-naked-image>` for minimal JS, `<datocms-image>` for crossfade/transparency
35. **Kebab-case props** — Uses `picture-class`, `img-class`, `fade-in-duration`, etc. (not camelCase)

#### Structured Text (Vue)
36. **GraphQL fragment** — Includes `id` and `__typename` on all `links`, `blocks`, `inlineBlocks`
37. **Custom renderers** — Use Vue `h()` function, switch on `record.__typename` with default null case
38. **Content Link boundaries** — If Content Link is active, group/boundary attributes are present

#### Video Player (Vue)
39. **Peer dependency** — `@mux/mux-player` is installed (NOT `@mux/mux-player-react`)
40. **GraphQL query** — Includes at minimum `muxPlaybackId`

#### SEO & Meta Tags (Vue)
41. **`toHead()` usage** — Uses `toHead()` (NOT `renderMetaTags()` or `toNextMetadata()`)
42. **Tag concatenation** — Uses `[...page.seo, ...site.favicon]` pattern
43. **Integration** — Paired with `@unhead/vue` (`useHead`) for Composition API or `metaInfo()` for Options API

#### Real-Time Updates (Vue)
44. **Ref values** — `data`, `error`, `status` are Vue `Ref` values (access with `.value` in script)
45. **Fetcher definition** — `fetcher` (if custom) defined as `const` outside reactive scope
46. **Draft mode integration** — Passes `includeDrafts`, `excludeInvalid`, `contentLink`, `baseEditingUrl` when in draft context

#### Content Link (Vue)
47. **Stega encoding enabled** — `contentLink: 'v1'` and `baseEditingUrl` in API calls
48. **Component mounted** — `<ContentLink>` in root layout/App component
49. **Framework navigation** — `on-navigate-to` and `current-path` wired to Vue Router or Nuxt Router (kebab-case props)

#### Site Search (Vue)
50. **CMA client** — `@datocms/cma-client-browser` installed and `buildClient()` used
51. **Reactive state** — Uses `v-model` for query input and direct assignment (`state.page = ...`) instead of setter functions
52. **Highlight rendering** — Uses `HighlightPiece` data pattern with `v-for` template loops (not a callback)

For React or Vue site search, a missing `searchIndexId` means the result is `scaffolded`; list the missing index ID explicitly instead of calling the setup production-ready.

#### Generic Site Search
53. **Low-level search helper** — Uses `client.searchResults.rawList()` with an
    explicit `filter.search_index_id`
54. **Public token only** — Uses a search-only token with
    `can_perform_site_search`, never a CMA-capable token in the browser
55. **Pagination** — Maps `limit` and `offset` into stable `page` /
    `totalPages` UI data

### Svelte Component/Store Checks

#### Responsive Images (Svelte)
56. **GraphQL query** — Uses `responsiveImage` with `{ auto: format }` in imgixParams
57. **Component choice** — `<NakedImage />` for minimal JS, `<Image />` for crossfade/transparency
58. **camelCase props** — Uses `pictureClass`, `imgClass`, `fadeInDuration`, etc. (not kebab-case)

#### Structured Text (Svelte)
59. **GraphQL fragment** — Includes `id` and `__typename` on all `links`, `blocks`, `inlineBlocks`
60. **Predicate-component tuples** — Uses `components={[[isBlock, Block], ...]}` with separate `.svelte` files (NOT render props or `h()` functions)
61. **Content Link boundaries** — If Content Link is active, `data-datocms-content-link-boundary` on block/inline block/inline item `.svelte` components (NOT on item link components)

#### Video Player (Svelte)
62. **Peer dependency** — `@mux/mux-player` is installed (NOT `@mux/mux-player-react`)
63. **GraphQL query** — Includes at minimum `muxPlaybackId`

#### SEO & Meta Tags (Svelte)
64. **`<Head />` component** — Uses `<Head data={...} />` (NOT `renderMetaTags()`, `toHead()`, or `toNextMetadata()`)
65. **Tag concatenation** — Uses `[...page.seo, ...site.favicon]` pattern

#### Real-Time Updates (Svelte)
66. **Svelte store** — Uses `querySubscription()` returning a Svelte store, accessed with `$subscription` syntax (NOT `useQuerySubscription` hook/composable)
67. **Reactive destructuring** — Uses `$: ({ data, error, status } = $subscription)` pattern
68. **Draft mode integration** — Passes `includeDrafts`, `excludeInvalid`, `contentLink`, `baseEditingUrl` when in draft context

#### Content Link (Svelte)
69. **Stega encoding enabled** — `contentLink: 'v1'` and `baseEditingUrl` in API calls
70. **Component mounted** — `<ContentLink />` in root `+layout.svelte`
71. **SvelteKit navigation** — `onNavigateTo` with `goto` from `$app/navigation` and `currentPath` with `$page.url.pathname` from `$app/stores` (camelCase props)

### Astro Component Checks

#### Responsive Images (Astro)
72. **GraphQL query** — Uses `responsiveImage` with `{ auto: format }` in imgixParams
73. **Single component** — Uses `<Image />` only (no SRCImage/NakedImage split)
74. **Subpath import** — Imports from `@datocms/astro/Image` (not from `@datocms/astro`)
75. **No redundant fields** — Not requesting both `bgColor` and `base64`; `srcSet` omitted when possible

#### Structured Text (Astro)
76. **GraphQL fragment** — Includes `id` and `__typename` on all `links`, `blocks`, `inlineBlocks`
77. **`__typename`-keyed objects** — Uses `blockComponents={{ CtaRecord: Cta }}` with separate `.astro` files (NOT render props, `h()` functions, or predicate-component tuples)
78. **Astro props** — Block components use `Astro.props` to receive `{ block }`, inline records receive `{ record }`, link-to-records receive `{ node, record, attrs }`
79. **Content Link boundaries** — If Content Link is active, `data-datocms-content-link-boundary` on block, inline block, and inline record `.astro` components (NOT on link-to-record components)
80. **Subpath import** — Imports from `@datocms/astro/StructuredText`

#### SEO & Meta Tags (Astro)
81. **`<Seo />` component** — Uses `<Seo data={...} />` (NOT `renderMetaTags()`, `toHead()`, `<Head />`, or `toNextMetadata()`)
82. **Tag concatenation** — Uses `[...page.seo, ...site.favicon]` pattern
83. **Subpath import** — Imports from `@datocms/astro/Seo`

#### Real-Time Updates (Astro)
84. **Page reload approach** — Uses `<QueryListener />` for page reload (NOT live data subscription like React/Vue/Svelte)
85. **Matching options** — `<QueryListener />` options match the `executeQuery` options (token, includeDrafts, excludeInvalid, contentLink, baseEditingUrl)
86. **Conditional rendering** — Only rendered in draft mode context (not in production)
87. **Subpath import** — Imports from `@datocms/astro/QueryListener`

#### Content Link (Astro)
88. **Stega encoding enabled** — `contentLink: 'v1'` and `baseEditingUrl` in API calls
89. **Component mounted** — `<ContentLink />` in layout
90. **No navigation props** — Does NOT use `onNavigateTo` or `currentPath` (auto-detects via `astro:page-load` events)
91. **Only 2 props** — `enableClickToEdit` and `stripStega` (no `root`, `onNavigateTo`, or `currentPath`)
92. **Subpath import** — Imports from `@datocms/astro/ContentLink`

### Robots & Sitemaps Checks

93. **Ordered crawler rules** — `Allow` entries for Dato crawler sections appear
    before any catch-all `Disallow: /`
94. **Same-domain URLs** — Sitemap output only contains URLs under the configured
    public site URL
95. **Explicit sitemap sources** — Every public section has a concrete path
    builder and `lastmod` source
96. **Suffix-specific groups** — `DatoCmsSearchBot<suffix>` groups are emitted
    only when multiple search indexes or explicit suffixes exist

---

## Cross-Skill Routing

This skill covers **framework integration** (draft mode, Web Previews, Content Link, real-time updates, cache tags) and **component usage** (images, structured text, video, SEO, search). If the task involves any of the following, activate the companion skill:

| Condition | Route to |
|---|---|
| Writing or optimizing GraphQL queries for the CDA | **datocms-cda** |
| Programmatic content management, schema changes, migration scripts, or webhook creation via REST | **datocms-cma** |
| Building a DatoCMS plugin | **datocms-plugin-builder** |
