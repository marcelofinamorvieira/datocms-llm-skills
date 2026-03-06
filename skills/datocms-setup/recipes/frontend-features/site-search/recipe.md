_Internal recipe for `datocms-setup`. Use this file only after the parent skill selects the `site-search` recipe and queues any prerequisites from `../../../references/recipe-manifest.json`._


# DatoCMS Site Search Setup

You are an expert at setting up DatoCMS Site Search. This recipe combines Dato
project provisioning with local frontend wiring so the project ends up with a
working search route, explicit search-index wiring, and a least-privilege token
story.

**Output states:**

- `scaffolded` — local search UI exists, but one or more required values are
  still placeholders or the Dato-side automation could not complete
- `production-ready` — a real search index is wired, the search route is
  mounted, and no search token / index id placeholders remain

Follow these steps in order. Do not skip steps.

---

## Step 1: Detect Context (silent)

Silently examine the project:

1. **Framework** — Read `package.json` and check for:
   - `next` -> Next.js (App Router)
   - `nuxt` -> Nuxt
   - `@sveltejs/kit` -> SvelteKit
   - `astro` -> Astro
   - otherwise infer whether the project is React-based, Vue-based, or another
     stack
2. **UI stack** — Detect whether `react-datocms`, `vue-datocms`,
   `@datocms/svelte`, or `@datocms/astro` are installed
3. **CMA client packages** — Check for `@datocms/cma-client`,
   `@datocms/cma-client-node`, and `@datocms/cma-client-browser`
4. **Existing search UI** — Search for `/search` routes, `useSiteSearch`,
   `searchResults.rawList`, and existing search components
5. **Existing Dato helpers** — Search for a shared `executeQuery` wrapper, Dato
   lib folder, and existing env helpers
6. **Environment files** — Check `.env.example`, `.env`, `.env.local`, and
   framework-specific env conventions for:
   - a CMA-capable token
   - a public search token
   - a search index id
   - a public site URL
7. **Public route structure** — Inspect the repo for distinct top-level public
   sections such as `/blog`, `/docs`, or `/help`

### Stop conditions

- If the framework cannot be determined, ask the user which stack they are
  using.
- If the repo already has a materially different search integration, patch it in
  place by default instead of replacing it wholesale.

---

## Step 2: Ask Questions

Ask zero questions by default.

Only ask if:

- the repo clearly exposes multiple public sections but it is ambiguous whether
  they should be separate search indexes, or
- an existing `/search` route has conflicting ownership and patching it safely
  is unclear

Otherwise, proceed directly.

---

## Step 3: Load References

Read only what is needed:

- `../../../references/shared/datocms-frontend-integrations/site-search-api.md`
- `../../../references/shared/datocms-cma/client-types-and-behaviors.md`
- `../../../references/shared/datocms-cma/access-control.md`

Then load the framework-appropriate search UI reference:

| Stack | Reference |
|---|---|
| React / Next.js | `../../../references/shared/datocms-frontend-integrations/react-site-search.md` |
| Vue / Nuxt | `../../../references/shared/datocms-frontend-integrations/vue-site-search.md` |
| SvelteKit / Astro / unsupported UI stack | `../../../references/shared/datocms-frontend-integrations/site-search-api.md` |

---

## Step 4: Generate Code

Generate the full setup, attempting Dato-side automation first when a
CMA-capable token is available.

### Dato-side automation

If a CMA-capable token exists, attempt this remote setup in order:

1. **Inspect existing search indexes**
2. **Inspect roles and access tokens**
3. **Create or update one least-privilege search role** with
   `can_perform_site_search: true`
4. **Create or update one access token** bound to that role
5. **Create or update exactly one search index by default**
   - Preserve multiple existing indexes if the Dato project already has them
   - Create multiple new indexes only if the repo already exposes clear,
     top-level public sections and their crawling boundaries can be generated
     without guessing
6. **Trigger indexing** after creating or materially updating an index

If remote automation is blocked by missing permissions such as
`can_manage_search_indexes` or `can_manage_access_tokens`, continue with local
scaffolding and mark the result `scaffolded`.

### Local project changes

Generate only the minimum local files needed for a working search experience:

1. **Install missing packages**
   - React / Next.js: `react-datocms`, `@datocms/cma-client-browser`
   - Vue / Nuxt: `vue-datocms`, `@datocms/cma-client-browser`
   - Other stacks: a suitable CMA client package for the runtime used by the
     generated helper
2. **Patch env placeholders**
   - public search token
   - public search index id
   - public site URL if the project does not already define it
3. **Create or patch a shared search helper**
   - React / Vue widget stacks may keep this helper thin
   - SvelteKit / Astro / unsupported stacks must use
     `client.searchResults.rawList()`
4. **Create or patch a `/search` route**
   - React and Vue stacks should render a real search UI using `useSiteSearch`
   - Other stacks should render a framework-native page backed by the generated
     helper
5. **Reuse existing Dato lib conventions** for file placement instead of
   inventing parallel structures

### Public env var conventions

Use the framework's public env prefix:

- Next.js: `NEXT_PUBLIC_DATOCMS_SITE_SEARCH_TOKEN`,
  `NEXT_PUBLIC_DATOCMS_SITE_SEARCH_INDEX_ID`, `NEXT_PUBLIC_SITE_URL`
- Nuxt: `NUXT_PUBLIC_DATOCMS_SITE_SEARCH_TOKEN`,
  `NUXT_PUBLIC_DATOCMS_SITE_SEARCH_INDEX_ID`, `NUXT_PUBLIC_SITE_URL`
- SvelteKit: `PUBLIC_DATOCMS_SITE_SEARCH_TOKEN`,
  `PUBLIC_DATOCMS_SITE_SEARCH_INDEX_ID`, `PUBLIC_SITE_URL`
- Astro: `PUBLIC_DATOCMS_SITE_SEARCH_TOKEN`,
  `PUBLIC_DATOCMS_SITE_SEARCH_INDEX_ID`, `PUBLIC_SITE_URL`

Only add variables that do not already exist. Preserve existing values.

### Mandatory rules

- Always pass an explicit `search_index_id`
- Never expose a CMA-capable token in browser code
- Default to one search index unless the repo clearly needs more
- Preserve an existing `/search` page and patch it in place where possible
- Keep search result highlighting in the presentation layer; do not store
  rendered HTML in helpers
- When remote automation fails, report the exact missing permission or credential
  instead of silently dropping the Dato-side step

### Output status

- Report `scaffolded` if any search token or search index id is still a
  placeholder, if the `/search` route is not fully mounted, or if Dato-side
  automation could not complete
- Report `production-ready` only when the mounted search route uses a real token
  and search index id and any attempted Dato-side automation completed without
  unresolved TODOs

---

## Step 5: Next Steps

After generating the files, tell the user:

1. Which Dato-side resources were created or reused
2. Which env vars still need real values, if any
3. How to trigger a fresh indexing pass if the content has not been crawled yet
4. Which sections were mapped into search indexes, if more than one was used

---

## Verification Checklist

Before presenting the result, verify:

1. Search UI exists at a mounted `/search` route
2. React / Vue stacks use `useSiteSearch`
3. SvelteKit / Astro / unsupported stacks use `client.searchResults.rawList()`
4. `search_index_id` is explicit in every search request
5. Browser code uses only the public search token, never a CMA token
6. Missing `can_manage_search_indexes` or `can_manage_access_tokens` is called
   out explicitly when remote automation fails
7. The result is marked `scaffolded` if any token, search index id, or section
   mapping remains unresolved
