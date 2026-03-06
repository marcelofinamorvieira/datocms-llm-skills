_Internal recipe for `datocms-setup`. Use this file only after the parent skill selects the `cda-client` recipe and queues any prerequisites from `../../../references/recipe-manifest.json`._


# DatoCMS CDA Client Setup

You are an expert at setting up the thinnest useful DatoCMS Content Delivery
API baseline for frontend frameworks. This recipe only installs
`@datocms/cda-client`, wires one published-content token placeholder, and
creates or patches the framework's shared query utility.

Follow these steps in order. Do not skip steps.

---

## Step 1: Detect Context (silent)

Silently examine the project:

1. **Framework** — Read `package.json` and check for:
   - `next` -> Next.js (App Router)
   - `nuxt` -> Nuxt
   - `@sveltejs/kit` -> SvelteKit
   - `astro` -> Astro
2. **File structure** — Determine whether the project uses `src/`
3. **Existing query utility** — Check for a shared DatoCMS query wrapper:
   - Next.js / Astro: `src/lib/datocms/executeQuery.ts`,
     `lib/datocms/executeQuery.ts`
   - SvelteKit: `src/lib/datocms/queries.ts`
   - Nuxt: `composables/useQuery.ts`
4. **Existing draft mode** — Check whether draft mode is already set up so the
   shared query utility can be patched toward the published-only baseline
   without fighting later preview upgrades
5. **Installed deps** — Check `package.json` for `@datocms/cda-client`
6. **Env files** — Check `.env`, `.env.local`, and `.env.example` for the
   published CDA token
7. **Typed-query context** — Check for existing gql.tada or GraphQL Code
   Generator usage so the query utility can preserve the repo's current typed
   document style without configuring it here

### Stop conditions

- If the framework cannot be determined, ask the user which supported
  framework they are using.
- If the repo already has a materially different shared query utility, inspect
  and patch it in place by default instead of replacing it wholesale.

---

## Step 2: Ask Questions

Ask zero questions by default.

Only ask if framework detection fails or the existing shared query utility is
materially different enough that patching it safely is unclear.

---

## Step 3: Load References

Read only these references:

- `../../../references/shared/datocms-cda/client-and-config.md`

Load the matching framework reference and focus on the core query-utility
shape:

| Framework | Reference file |
|---|---|
| Next.js | `../../../references/shared/datocms-frontend-integrations/nextjs.md` |
| Nuxt | `../../../references/shared/datocms-frontend-integrations/nuxt.md` |
| SvelteKit | `../../../references/shared/datocms-frontend-integrations/sveltekit.md` |
| Astro | `../../../references/shared/datocms-frontend-integrations/astro.md` |

---

## Step 4: Generate Code

Generate only these project changes:

1. **Install `@datocms/cda-client`** if it is missing
2. **Patch `.env.example`** with the framework-appropriate published-token
   placeholder only
3. **Create or patch the shared query utility** for the detected framework:
   - Next.js / Astro: `src/lib/datocms/executeQuery.ts` or
     `lib/datocms/executeQuery.ts`
   - SvelteKit: `src/lib/datocms/queries.ts`
   - Nuxt: `composables/useQuery.ts`

### Required behavior

The generated query utility must:

1. Use `@datocms/cda-client`
2. Inject the published CDA token from environment variables
3. Set `excludeInvalid: true`
4. Accept query variables
5. Preserve typed-document support when the repo already uses it

### Mandatory rules

- Keep this setup published-content only
- Do not add `includeDrafts` logic unless preserving an existing working
  implementation requires it
- Do not add `rawExecuteQuery`
- Do not add cache-tag or revalidation behavior
- Do not add gql.tada or GraphQL Code Generator config
- Do not add routes, cookies, JWT helpers, webhook handlers, or realtime code
- Make targeted additions instead of full rewrites
- Preserve working existing behavior where possible and patch toward the thin
  baseline

### Framework defaults

- **Next.js / Astro / SvelteKit:** keep the wrapper server-first and use a
  private published CDA token
- **Nuxt:** keep the public published-token convention and `composables`
  pattern so the baseline stays compatible with the existing Nuxt integration
  flow

---

## Step 5: Install Dependencies

Install only this package when missing:

- `@datocms/cda-client`

Use the detected package manager.

---

## Step 6: Environment Variables

Patch `.env.example` with only the framework-appropriate published-content CDA
token placeholder:

### Next.js
```env
DATOCMS_PUBLISHED_CONTENT_CDA_TOKEN=your_published_token_here
```

### Nuxt
```env
NUXT_PUBLIC_DATOCMS_PUBLISHED_CONTENT_CDA_TOKEN=your_published_token_here
```

### SvelteKit
```env
PRIVATE_DATOCMS_PUBLISHED_CONTENT_CDA_TOKEN=your_published_token_here
```

### Astro
```env
DATOCMS_PUBLISHED_CONTENT_CDA_TOKEN=your_published_token_here
```

Only add variables that do not already exist. Preserve any existing values.

---

## Step 7: Next Steps

After generating the files, tell the user:

1. Fill in the published CDA token locally
2. Use `datocms-setup` for `draft-mode` separately if they later want preview reads
3. Use `datocms-setup` for `graphql-types` separately if they want typed query
   generation
4. Keep cache tags, Content Link, and realtime as separate follow-up setups

---

## Verification Checklist

Before presenting the result, verify:

1. `@datocms/cda-client` is installed or added
2. `.env.example` contains only the published CDA token placeholder for the
   detected framework
3. The generated or patched query utility matches the detected framework and
   file layout
4. No preview or draft-token logic was added unless preserving an existing
   implementation required it
5. No `rawExecuteQuery`, cache-tag logic, typegen config, or route handlers
   were added
