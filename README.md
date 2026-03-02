# DatoCMS Plugin SDK — Agent Skills

Everything your coding agent needs to build DatoCMS plugins from scratch (or improve existing ones).

This repo contains a comprehensive, interactive skill that teaches AI coding agents how to work with the [`datocms-plugin-sdk`](https://www.npmjs.com/package/datocms-plugin-sdk). It covers the full plugin surface: field extensions, sidebar panels, custom pages, dropdown actions, asset sources, lifecycle hooks, modals, config screens, inspectors, outlets, and more.

The skill walks the agent through a structured build flow — it detects whether you're starting fresh or augmenting an existing plugin, asks the right discovery questions, loads only the relevant reference docs, generates proper TypeScript + React code, and guides you through wiring everything up in DatoCMS.

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

## Installation

Clone the repo (or download it) somewhere on your machine, then point your agent at it. Each agent has a slightly different way to do this — pick yours below.

### Clone

```bash
git clone https://github.com/datocms/datocms-plugin-sdk-agent-skill.git ~/.datocms-skill
```

(Use any path you like — the commands below assume `~/.datocms-skill`.)

### Claude Code

```bash
claude --add-dir ~/.datocms-skill
```

Or, to make it permanent for a specific project, add to your project's `.claude/settings.json`:

```json
{
  "additionalDirectories": ["~/.datocms-skill"]
}
```

Claude Code will auto-discover the `SKILL.md` from the added directory and make the skill available in your session.

### OpenAI Codex CLI

Add the skill path as a read reference in your project's `AGENTS.md`:

```markdown
@~/.datocms-skill/datocms-pluginsdk-skill/SKILL.md
```

Or symlink it into your project's skills directory:

```bash
mkdir -p .agents/skills && ln -s ~/.datocms-skill/datocms-pluginsdk-skill .agents/skills/datocms-plugin-builder
```

### Gemini CLI

Import the skill from your project's `GEMINI.md`:

```markdown
@~/.datocms-skill/datocms-pluginsdk-skill/SKILL.md
```

### Cursor

Symlink the skill into your project's rules directory:

```bash
mkdir -p .cursor/rules && ln -s ~/.datocms-skill/datocms-pluginsdk-skill/SKILL.md .cursor/rules/datocms-plugin-builder.md
```

### Windsurf

Symlink the skill into your project's rules directory:

```bash
mkdir -p .windsurf/rules && ln -s ~/.datocms-skill/datocms-pluginsdk-skill/SKILL.md .windsurf/rules/datocms-plugin-builder.md
```

### Amp

Symlink or copy the skill file so Amp discovers it:

```bash
ln -s ~/.datocms-skill/datocms-pluginsdk-skill/SKILL.md ./AGENTS.md
```

Or reference it in an existing `AGENTS.md` with an import.

### GitHub Copilot

Copy or symlink the skill into your project's instructions:

```bash
mkdir -p .github/instructions && ln -s ~/.datocms-skill/datocms-pluginsdk-skill/SKILL.md .github/instructions/datocms-plugin-builder.instructions.md
```

### Cline

Symlink the skill into your project's rules directory:

```bash
mkdir -p .clinerules && ln -s ~/.datocms-skill/datocms-pluginsdk-skill/SKILL.md .clinerules/datocms-plugin-builder.md
```

### Roo Code

Symlink the skill into your project's rules directory:

```bash
mkdir -p .roo/rules && ln -s ~/.datocms-skill/datocms-pluginsdk-skill/SKILL.md .roo/rules/datocms-plugin-builder.md
```

### Aider

Point Aider at the skill via CLI flag or config:

```bash
aider --read ~/.datocms-skill/datocms-pluginsdk-skill/SKILL.md
```

Or add to your `.aider.conf.yml`:

```yaml
read: ~/.datocms-skill/datocms-pluginsdk-skill/SKILL.md
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
