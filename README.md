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

Everything your agent needs to interact with the DatoCMS Content Management API using the official TypeScript/JavaScript REST clients ([`@datocms/cma-client-node`](https://www.npmjs.com/package/@datocms/cma-client-node), `@datocms/cma-client-browser`). Covers records CRUD, uploads, schema management, filtering, localization, blocks & structured text, environments, webhooks, access control, scheduling, and migration patterns — across 12 reference docs.

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
└── references/                           # 12 deep-dive reference docs
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
    └── migration-patterns.md             # Bulk operations, content seeding, field migrations
```
</details>

---

## Install

Clone the repo:

```bash
git clone https://github.com/marcelofinamorvieira/datocms-llm-skills.git
```

Then copy the skill(s) you want into your agent's directory. You can install them **globally** (available in all your projects) or **per-project** (only available in the current project).

Replace `<skill-folder>` with the skill you want to install (e.g., `datocms-pluginsdk-skill`, `datocms-cma-skill`) and `<skill-name>` with whatever name you'd like to give it locally (e.g., `datocms-plugin-builder`, `datocms-cma`).

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
