# DatoCMS Plugin SDK — Agent Skill

Everything your coding agent needs to build DatoCMS plugins from scratch (or improve existing ones).

This repo contains an interactive skill that teaches AI coding agents how to work with the [`datocms-plugin-sdk`](https://www.npmjs.com/package/datocms-plugin-sdk). It covers the full plugin surface — field extensions, sidebar panels, custom pages, dropdown actions, asset sources, lifecycle hooks, modals, config screens, inspectors, outlets, and more — across 16 detailed reference docs.

The skill walks your agent through a structured build flow: it detects whether you're starting fresh or augmenting an existing plugin, asks discovery questions, loads only the relevant reference docs, generates TypeScript + React code, and guides you through wiring everything up in DatoCMS.

## Install

First, clone the repo:

```bash
git clone https://github.com/marcelofinamorvieira/datocms-llm-skills.git
```

Then copy the skill into your agent's directory. You can install it **globally** (available in all your projects) or **per-project** (only available in the current project).

### Claude Code

```bash
# Global (all projects)
cp -r datocms-llm-skills/datocms-pluginsdk-skill ~/.claude/skills/datocms-plugin-builder

# Project only
cp -r datocms-llm-skills/datocms-pluginsdk-skill .claude/skills/datocms-plugin-builder
```

### Cursor

```bash
# Global (all projects)
cp -r datocms-llm-skills/datocms-pluginsdk-skill ~/.cursor/skills/datocms-plugin-builder

# Project only
cp -r datocms-llm-skills/datocms-pluginsdk-skill .cursor/skills/datocms-plugin-builder
```

### OpenAI Codex CLI

```bash
# Global (all projects)
cp -r datocms-llm-skills/datocms-pluginsdk-skill ~/.codex/skills/datocms-plugin-builder

# Project only
cp -r datocms-llm-skills/datocms-pluginsdk-skill .agents/skills/datocms-plugin-builder
```

### Windsurf

```bash
# Global (all projects)
cp -r datocms-llm-skills/datocms-pluginsdk-skill ~/.windsurf/skills/datocms-plugin-builder

# Project only
cp -r datocms-llm-skills/datocms-pluginsdk-skill .windsurf/skills/datocms-plugin-builder
```

### Amp

```bash
# Project only
cp -r datocms-llm-skills/datocms-pluginsdk-skill .amp/skills/datocms-plugin-builder
```

### Cline

```bash
# Project only
cp -r datocms-llm-skills/datocms-pluginsdk-skill .cline/skills/datocms-plugin-builder
```

### Roo Code

```bash
# Global (all projects)
cp -r datocms-llm-skills/datocms-pluginsdk-skill ~/.roo/skills/datocms-plugin-builder

# Project only
cp -r datocms-llm-skills/datocms-pluginsdk-skill .roo/skills/datocms-plugin-builder
```

### GitHub Copilot

```bash
# Project only
cp -r datocms-llm-skills/datocms-pluginsdk-skill .agents/skills/datocms-plugin-builder
```

### Gemini CLI

```bash
# Global (all projects)
cp -r datocms-llm-skills/datocms-pluginsdk-skill ~/.gemini/skills/datocms-plugin-builder

# Project only
cp -r datocms-llm-skills/datocms-pluginsdk-skill .gemini/skills/datocms-plugin-builder
```

### Aider

```bash
# Project only
cp -r datocms-llm-skills/datocms-pluginsdk-skill .aider/skills/datocms-plugin-builder
```

## What's inside

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

## Usage

Once installed, just ask your agent to build a DatoCMS plugin. The skill activates automatically when it detects plugin-related intent. Some examples:

- *"Create a DatoCMS plugin that adds a character counter below text fields"*
- *"Add a sidebar panel to this plugin that shows SEO suggestions"*
- *"Build a plugin with a custom page that shows analytics for all records"*
- *"Add a lifecycle hook that validates required fields before publish"*

The agent will walk you through discovery questions, generate the code, and guide you through testing it locally in DatoCMS.

## How it works

The skill follows a 7-step interactive flow:

1. **Detect** — figures out if you're starting fresh or working on an existing plugin
2. **Scaffold** — sets up the full project structure if needed (Vite, TypeScript, React)
3. **Discover** — asks what your plugin should do, then maps that to SDK features
4. **Load references** — pulls in only the relevant docs (not all 16 files every time)
5. **Generate** — writes the `connect()` call, component files, and dependencies
6. **Wire up** — walks you through installing the plugin in DatoCMS and testing it
7. **Polish** — error boundaries, loading states, edge cases, publishing prep

## Contributing

Found an issue in the reference docs? Want to improve a code pattern? PRs are welcome.
