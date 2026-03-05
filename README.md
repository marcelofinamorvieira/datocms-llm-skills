# DatoCMS Agent Skills

A collection of skills that teach AI coding agents how to work with DatoCMS. Each skill is a self-contained package of reference docs and an interactive guide that walks your agent through the right approach — loading only the docs it needs, asking the right questions, and generating correct code.

## Available Skills

### `datocms-pluginsdk-skill` — Plugin Builder

Everything your agent needs to build DatoCMS plugins from scratch (or improve existing ones) using the [`datocms-plugin-sdk`](https://www.npmjs.com/package/datocms-plugin-sdk). Covers the full plugin surface — field extensions, sidebar panels, custom pages, dropdown actions, asset sources, lifecycle hooks, modals, config screens, inspectors, outlets, and more — across 16 detailed reference docs.

The skill follows a 7-step interactive flow: detect project state, scaffold if needed, ask discovery questions, load relevant references, generate TypeScript + React code, wire everything up in DatoCMS, and polish.

**Example prompts:**
- *"Create a DatoCMS plugin that adds a character counter below text fields"*
- *"Add a sidebar panel to this plugin that shows SEO suggestions"*
- *"Build a plugin with a custom page that shows analytics for all records"*
- *"Add a lifecycle hook that validates required fields before publish"*

<details>
<summary>What's inside</summary>

```
datocms-pluginsdk-skill/
├── SKILL.md                    # Main interactive guide (the entry point)
└── references/                 # 16 deep-dive reference docs
    ├── sdk-architecture.md     # Core concepts: connect(), hooks, Canvas, ctx
    ├── project-scaffold.md     # Full starter templates (package.json, Vite, tsconfig, etc.)
    ├── field-extensions.md     # Editors, addons, manual vs. override, localization
    ├── sidebar-panels.md       # Collapsible panels and full-width sidebars
    ├── custom-pages.md         # Navigation tabs, settings pages, content sidebar items
    ├── config-screen.md        # Global plugin configuration with react-final-form
    ├── lifecycle-hooks.md      # onBoot, onBeforeItemUpsert, publish/unpublish/destroy guards
    ├── dropdown-actions.md     # Context menu actions across 5 scopes
    ├── modals.md               # Popup dialogs that return values
    ├── asset-sources.md        # Custom upload sources with CORS/base64 handling
    ├── outlets.md              # Banners at top of record forms or collection views
    ├── inspectors.md           # Split-screen panels
    ├── upload-sidebars.md      # Media area sidebar customization
    ├── structured-text.md      # Custom marks and block-level styles
    ├── record-presentation.md  # Custom record display in lists and link fields
    └── form-values.md          # Reading/writing form data, localization helpers
```
</details>

---

### `datocms-cma-skill` — Content Management API

Everything your agent needs to interact with the DatoCMS Content Management API using the official TypeScript/JavaScript REST clients ([`@datocms/cma-client-node`](https://www.npmjs.com/package/@datocms/cma-client-node), `@datocms/cma-client-browser`). Covers records CRUD, uploads, schema management, filtering, localization, blocks & structured text, environments, webhooks, access control, scheduling, migration patterns, and CMA type generation for type-safe record operations — across 13 reference docs.

The skill follows a 5-step flow: detect the client package and token setup, classify the task, load relevant references, generate code with proper pagination/error handling/types, and verify correctness.

**Example prompts:**
- *"Write a script to bulk-publish all draft records in the blog model"*
- *"Create a migration that adds a new field to every model"*
- *"Fetch all records with a specific tag and update their status"*
- *"Set up a webhook that triggers on record publish"*

<details>
<summary>What's inside</summary>

```
datocms-cma-skill/
├── SKILL.md                              # Main interactive guide (the entry point)
└── references/                           # 13 deep-dive reference docs
    ├── client-and-types.md               # Client setup, type system, error handling
    ├── records.md                        # Create, read, update, delete, publish records
    ├── uploads.md                        # File uploads, asset management, metadata
    ├── schema.md                         # Models, fields, fieldsets, block models
    ├── filtering-and-pagination.md       # Search, filter, paginate large collections
    ├── localization.md                   # Multi-locale content handling
    ├── blocks-and-structured-text.md     # Modular content, inline blocks, DAST
    ├── environments.md                   # Fork, promote, sandbox management
    ├── webhooks-and-triggers.md          # Webhooks and build trigger configuration
    ├── access-control.md                 # Roles, API tokens, user management
    ├── scheduling.md                     # Scheduled publish/unpublish, workflows
    ├── migration-patterns.md             # Bulk operations, content seeding, field migrations
    └── type-generation.md                # CMA schema type generation with @datocms/cli
```
</details>

---

### `datocms-cli-skill` — CLI Tool

Everything your agent needs to work with the DatoCMS CLI ([`@datocms/cli`](https://www.npmjs.com/package/@datocms/cli)). Covers migration scripting (creating and running), environment management from the command line, maintenance mode, deployment workflows, CLI profiles and configuration, and content importing from WordPress or Contentful — across 6 reference docs.

The skill follows a 5-step flow: detect CLI installation and config, classify the task, load relevant references, generate commands and migration scaffolds, and verify correctness.

**Example prompts:**
- *"Create a new migration to add a blog model with title and body fields"*
- *"Run pending migrations against a forked sandbox environment"*
- *"Set up a safe deployment workflow with maintenance mode and environment promotion"*
- *"Import my WordPress site into DatoCMS"*

<details>
<summary>What's inside</summary>

```
datocms-cli-skill/
├── SKILL.md                              # Main interactive guide (the entry point)
└── references/                           # 6 deep-dive reference docs
    ├── cli-setup.md                      # Installation, datocms.config.json, profiles, token resolution
    ├── creating-migrations.md            # migrations:new command, templates, autogenerate, schema types
    ├── running-migrations.md             # migrations:run command, fork-and-run, in-place, tracking
    ├── environment-commands.md           # environments:* commands, cma:call for raw API access
    ├── deployment-workflow.md            # Maintenance mode, safe deploy sequence, CI/CD integration
    └── importing-content.md             # WordPress and Contentful import plugins
```
</details>

---

### `datocms-cda-skill` — Content Delivery API

Everything your agent needs to query the DatoCMS Content Delivery API (CDA) — a read-only GraphQL API — using the official [`@datocms/cda-client`](https://www.npmjs.com/package/@datocms/cda-client) TypeScript/JavaScript library. Covers querying records, filtering, pagination, localization with fallbacks, modular content blocks, structured text (DAST) rendering, responsive images with imgix, SEO meta tags, video, draft/preview mode, cache tags, and environment targeting — across 11 reference docs. Also includes setup for type generation with gql.tada or GraphQL Code Generator for fully typed CDA queries.

The skill follows a 5-step flow: detect the client package and token setup, classify the task, load relevant references, generate code with proper GraphQL variables/pagination/error handling, and verify correctness.

**Example prompts:**
- *"Fetch all blog posts sorted by date and paginate them"*
- *"Query localized content with fallback locales for a multilingual site"*
- *"Render structured text fields with custom block components in Next.js"*
- *"Set up responsive images with blur-up placeholders and focal point cropping"*

<details>
<summary>What's inside</summary>

```
datocms-cda-skill/
├── SKILL.md                              # Main interactive guide (the entry point)
└── references/                           # 11 deep-dive reference docs
    ├── client-and-config.md              # Client setup, options, error handling, scalars
    ├── querying-basics.md                # Records, collections, meta fields, single-instance models
    ├── filtering.md                      # Field filters, AND/OR logic, deep filtering, uploads
    ├── pagination-and-ordering.md        # first/skip, auto-pagination, ordering, trees
    ├── localization.md                   # Localized fields, fallback locales, all-locale values
    ├── modular-content.md                # Block fields, GraphQL fragments, nested blocks
    ├── structured-text.md                # DAST value/blocks/links, rendering with components
    ├── images-and-videos.md              # responsiveImage, imgix transforms, placeholders, Mux video
    ├── seo-and-meta.md                   # _seoMetaTags, favicons, globalSeo, Open Graph
    ├── draft-caching-environments.md     # Draft mode, cache tags, CDN invalidation, Content Link
    └── type-generation.md                # gql.tada and GraphQL Code Generator setup for typed queries
```
</details>

---

### `datocms-frontend-integrations-skill` — Front-End Integrations

Everything your agent needs to set up DatoCMS front-end integrations in existing projects. Covers two domains: **(1) Draft mode setup** — authenticated endpoints with dual-token architecture, Web Previews plugin, Content Link visual editing, and real-time update subscriptions for Next.js (App Router), Nuxt, SvelteKit, and Astro. **(2) Component/hook/store usage** from `react-datocms`, `vue-datocms`, `@datocms/svelte`, and `@datocms/astro` — responsive images, structured text rendering, video player, SEO/meta tags, real-time subscriptions, Content Link, and site search — across 33 reference docs.

The skill follows a 5-step flow: detect the framework and existing setup, classify the task, load relevant references (only for selected categories), generate code with proper patterns for each framework, and verify correctness.

**Example prompts:**
- *"Set up draft mode for my Next.js project with Content Link and real-time updates"*
- *"Display responsive images from DatoCMS in my Astro site"*
- *"Render structured text with custom blocks in my SvelteKit app"*
- *"Add SEO meta tags to my Nuxt pages using vue-datocms"*
- *"Set up Content Link visual editing in my Astro project"*
- *"Build a site search page with useSiteSearch in React"*

<details>
<summary>What's inside</summary>

```
datocms-frontend-integrations-skill/
├── SKILL.md                              # Main interactive guide (the entry point)
└── references/                           # 33 reference docs
    ├── draft-mode-concepts.md            # Core concepts: tokens, cookies, open redirects, JWT
    ├── web-previews-concepts.md          # Web Previews plugin: endpoint contract, CORS, Visual tab
    ├── content-link-concepts.md          # Content Link: createController, data attributes, stega
    ├── realtime-concepts.md              # Real-time updates: SSE streaming, client libraries
    ├── nextjs.md                         # Next.js App Router draft mode patterns
    ├── nuxt.md                           # Nuxt draft mode patterns
    ├── sveltekit.md                      # SvelteKit draft mode patterns
    ├── astro.md                          # Astro draft mode patterns
    ├── react-image.md                    # <SRCImage>, <Image> — responsive images (React)
    ├── react-structured-text.md          # <StructuredText> — render props (React)
    ├── react-video-player.md             # <VideoPlayer> — Mux video (React)
    ├── react-seo.md                      # renderMetaTags, toNextMetadata, toRemixMeta (React)
    ├── react-realtime.md                 # useQuerySubscription — live updates (React)
    ├── react-content-link.md             # <ContentLink> — visual editing (React)
    ├── react-site-search.md              # useSiteSearch — search UI (React)
    ├── vue-image.md                      # <datocms-image>, <datocms-naked-image> (Vue)
    ├── vue-structured-text.md            # <datocms-structured-text> — h() renderers (Vue)
    ├── vue-video-player.md               # <VideoPlayer> — Mux video (Vue)
    ├── vue-seo.md                        # toHead() — SEO meta tags (Vue)
    ├── vue-realtime.md                   # useQuerySubscription — live updates (Vue)
    ├── vue-content-link.md               # <ContentLink> — visual editing (Vue)
    ├── vue-site-search.md                # useSiteSearch — search UI (Vue)
    ├── svelte-image.md                   # <Image>, <NakedImage> — responsive images (Svelte)
    ├── svelte-structured-text.md         # <StructuredText> — predicate-component tuples (Svelte)
    ├── svelte-video-player.md            # <VideoPlayer> — Mux video (Svelte)
    ├── svelte-seo.md                     # <Head> — SEO meta tags (Svelte)
    ├── svelte-realtime.md                # querySubscription — Svelte store for live updates
    ├── svelte-content-link.md            # <ContentLink> — visual editing (Svelte)
    ├── astro-image.md                    # <Image> — zero-JS responsive images (Astro)
    ├── astro-structured-text.md          # <StructuredText> — __typename-keyed objects (Astro)
    ├── astro-seo.md                      # <Seo> — SEO meta tags (Astro)
    ├── astro-realtime.md                 # <QueryListener> — page reload on changes (Astro)
    └── astro-content-link.md             # <ContentLink> — auto-navigation visual editing (Astro)
```
</details>

---

### Slash Command Skills

These are action-oriented slash command skills that detect your framework, ask minimal questions, and generate all files. They reference the same reference docs as `datocms-frontend-integrations-skill` (no duplication) and use `disable-model-invocation: true` so they don't activate automatically — you invoke them explicitly via slash commands.

**Prerequisites:** `/setup-web-previews`, `/setup-content-link`, `/setup-realtime`, and `/setup-cache-tags` all require draft mode to be set up first. Run `/setup-draft-mode` before using them.

#### `/setup-draft-mode` — `datocms-setup-draft-mode`

Sets up DatoCMS draft mode from scratch: enable/disable endpoints, utilities (CORS, error handling, `isRelativeUrl`), and an `executeQuery` wrapper with dual-token switching and `includeDrafts` support. Detects the framework automatically, installs dependencies, and configures environment variables.

#### `/setup-web-previews` — `datocms-setup-web-previews`

Adds a preview-links endpoint for the DatoCMS Web Previews plugin. Asks for your content models and URL patterns (or uses TODO placeholders), generates the endpoint with CORS handling, token validation, `recordToWebsiteRoute` switch, and status branching for draft/published links.

#### `/setup-content-link` — `datocms-setup-content-link`

Enables Content Link visual editing — click-to-edit overlays that let editors click any element to jump to the corresponding field in DatoCMS. Modifies the `executeQuery` wrapper to enable stega encoding, generates a framework-specific `ContentLink` component, and adds it to the root layout.

#### `/setup-realtime` — `datocms-setup-realtime`

Adds real-time content updates in draft mode. Generates framework-specific subscription components: factory functions for Next.js (`generateRealtimeComponent` + `generatePageComponent`), `useQuerySubscription` usage for Nuxt, `querySubscription` store usage for SvelteKit, and `<QueryListener />` (page reload) for Astro.

#### `/setup-cache-tags` — `datocms-setup-cache-tags`

Sets up DatoCMS cache tag invalidation for granular content purging — only pages affected by a content change are purged, instead of revalidating everything. Next.js uses a framework-centric approach with `revalidateTag()` and a database for tag storage; Nuxt, SvelteKit, and Astro use CDN-first cache tags forwarded via response headers (supporting Netlify, Cloudflare, Fastly, and Bunny). Requires `executeQuery` to be already configured.

#### `/setup-graphql-types` — `datocms-setup-graphql-types`

Sets up TypeScript type generation for DatoCMS GraphQL queries using gql.tada or GraphQL Code Generator. Optionally generates CMA schema types for typed record operations. Detects the framework automatically, generates config files, installs dependencies, and runs the initial schema generation.

---

## Install

Clone the repo:

```bash
git clone https://github.com/marcelofinamorvieira/datocms-llm-skills.git
```

Then copy the skill(s) you want into your agent's directory. You can install them **globally** (available in all your projects) or **per-project** (only available in the current project).

Replace `<skill-folder>` with the skill you want to install (e.g., `datocms-pluginsdk-skill`, `datocms-cma-skill`, `datocms-cda-skill`) and `<skill-name>` with whatever name you'd like to give it locally (e.g., `datocms-plugin-builder`, `datocms-cma`, `datocms-cda`).

### Claude Code

```bash
# Global (all projects)
cp -r datocms-llm-skills/<skill-folder> ~/.claude/skills/<skill-name>

# Project only
cp -r datocms-llm-skills/<skill-folder> .claude/skills/<skill-name>
```

### Cursor

```bash
# Global (all projects)
cp -r datocms-llm-skills/<skill-folder> ~/.cursor/skills/<skill-name>

# Project only
cp -r datocms-llm-skills/<skill-folder> .cursor/skills/<skill-name>
```

### OpenAI Codex CLI

```bash
# Global (all projects)
cp -r datocms-llm-skills/<skill-folder> ~/.codex/skills/<skill-name>

# Project only
cp -r datocms-llm-skills/<skill-folder> .agents/skills/<skill-name>
```

### Windsurf

```bash
# Global (all projects)
cp -r datocms-llm-skills/<skill-folder> ~/.windsurf/skills/<skill-name>

# Project only
cp -r datocms-llm-skills/<skill-folder> .windsurf/skills/<skill-name>
```

### Amp

```bash
# Project only
cp -r datocms-llm-skills/<skill-folder> .amp/skills/<skill-name>
```

### Cline

```bash
# Project only
cp -r datocms-llm-skills/<skill-folder> .cline/skills/<skill-name>
```

### Roo Code

```bash
# Global (all projects)
cp -r datocms-llm-skills/<skill-folder> ~/.roo/skills/<skill-name>

# Project only
cp -r datocms-llm-skills/<skill-folder> .roo/skills/<skill-name>
```

### GitHub Copilot

```bash
# Project only
cp -r datocms-llm-skills/<skill-folder> .agents/skills/<skill-name>
```

### Gemini CLI

```bash
# Global (all projects)
cp -r datocms-llm-skills/<skill-folder> ~/.gemini/skills/<skill-name>

# Project only
cp -r datocms-llm-skills/<skill-folder> .gemini/skills/<skill-name>
```

### Aider

```bash
# Project only
cp -r datocms-llm-skills/<skill-folder> .aider/skills/<skill-name>
```

## Usage

Once installed, just describe what you want to do with DatoCMS. The relevant skill activates automatically when your agent detects matching intent — no special commands needed.

## Contributing

Found an issue in the reference docs? Want to improve a code pattern or add a new skill? PRs are welcome.
