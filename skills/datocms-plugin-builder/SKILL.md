---
name: datocms-plugin-builder
description: >-
  Modify existing DatoCMS plugins built with datocms-plugin-sdk and connect().
  Use when users ask to patch or maintain an existing plugin project: config
  screen edits, hook additions, field extension tweaks, sidebar/page/outlet
  changes, validation updates, settings cleanup, dependency fixes, or other
  day-to-day plugin maintenance. Prefer `datocms-plugin-scaffold` when starting
  a new plugin from scratch.
---

# DatoCMS Plugin Builder

Default to augment mode. Move fast, inspect narrowly, and keep edits small.

## Step 1: Detect the smallest change surface

Silently inspect the project before asking questions.

1. Read `package.json` and confirm the plugin uses `datocms-plugin-sdk`.
2. Find the entry file that calls `connect()` (`src/main.tsx`, `src/index.tsx`, or equivalent).
3. Inspect the existing `connect()` call before changing any hook.
4. From the user request, identify the smallest touched surface:
   - config screen / plugin parameters
   - field extension or manual field extension config
   - sidebar panel, full sidebar, outlet, or custom page
   - dropdown action or lifecycle hook
   - modal, inspector, asset source, or upload sidebar
   - record presentation or structured text customization
   - dependency, build, or type fix around the plugin
5. Read only the direct path of the change:
   - the `connect()` entry file
   - the component or helper being edited
   - any imported file that must change too
6. Reuse the current file layout, naming, and UI patterns.

Do not start with broad discovery for obvious small edits like label renames,
option removal, config-field cleanup, single-hook wiring, or validation tweaks.

## Step 2: Patch unless the repo cannot answer

Ask zero questions by default.

Only ask when a wrong assumption would materially change behavior and the repo
cannot resolve it, such as:

- which DatoCMS surface to use
- which model or field scope to target
- whether a new permission or external dependency is allowed

If no plugin project exists, or the user wants a brand-new plugin folder, switch
to `datocms-plugin-scaffold`.

## Step 3: Load only the needed references

Start from project code. Read reference files only when the current
implementation does not already show the required pattern or when adding a new
surface. For long references, read the Quick Navigation section first and then
open only the relevant section.

### Surface references

- Config screen / plugin parameters -> `references/config-screen.md`
- Field extension / per-field config -> `references/field-extensions.md`
- Sidebar panel / full sidebar -> `references/sidebar-panels.md`
- Custom page -> `references/custom-pages.md`
- Dropdown actions -> `references/dropdown-actions.md`
- Lifecycle hooks -> `references/lifecycle-hooks.md`
- Modal -> `references/modals.md`
- Outlets -> `references/outlets.md`
- Inspector -> `references/inspectors.md`
- Asset source -> `references/asset-sources.md`
- Upload sidebar / panel -> `references/upload-sidebars.md`
- Structured text customization -> `references/structured-text.md`
- Record presentation -> `references/record-presentation.md`

### Load conditionally

- `references/connect-conventions.md` when wiring or adjusting hooks, render
  switches, modal flows, or frame-sizing behavior
- `references/form-values.md` only when reading `ctx.formValues` outside field
  extensions, or when touching Structured Text / modular content values
- `references/sdk-architecture.md` only for deeper SDK details not covered by
  `references/connect-conventions.md`

Do not load the whole reference set for a small patch.

## Step 4: Patch minimally

Prefer editing the existing declaration, render switch, component, or helper
over reorganizing the plugin.

- Add a new file only when it keeps the change smaller or matches the current
  structure.
- Keep dependency changes minimal and only add packages that the code actually
  uses.
- Preserve the existing UI style unless the user asked for a redesign.

Keep these guardrails:

- Inspect the existing `connect()` call before adding hooks.
- Keep exactly one top-level `connect()` call.
- Update declaration, render, and execute pairs together when a surface needs
  both sides.
- Wrap rendered UI in `<Canvas ctx={ctx}>`; use `noAutoResizer` for pages,
  inspectors, and full-width sidebars.
- Use `switch` for ID-dispatched render hooks.
- Use `import type { ... }` for SDK types.
- Guard `ctx.item` before reading record data.
- Use `get(ctx.formValues, ctx.fieldPath)` in field extensions; use the
  localized-value patterns from `references/form-values.md` elsewhere.
- Use `useDeepCompareEffect` instead of `useEffect` when depending on `ctx`
  object properties.
- Keep `ctx.openModal()` parameters and `ctx.resolve()` values JSON-serializable.
- Normalize stored plugin parameters before saving when config data may already
  exist in older shapes.
- Use `ctx.setParameters()` directly in
  `renderManualFieldExtensionConfigScreen`.
- Do not create editor field extensions for modular content, single block, or
  structured text fields; use addon extensions instead.

## Step 5: Verify with the smallest useful check

Run the lightest existing verification that meaningfully covers the change:

- `npm run build` by default for code changes
- the most relevant test or typecheck command if the project already has one
- `npm install` before verifying if dependencies changed

If the repo has no suitable script, run the closest existing build, typecheck,
or lint command instead.

Report:

1. what you changed
2. what you ran
3. the one manual DatoCMS check that still matters

## Cross-skill routing

- New plugin from scratch -> `datocms-plugin-scaffold`
- Standalone CMA scripts or schema work outside the plugin iframe -> `datocms-cma`
- Front-end preview, Content Link, or cache-tag work outside the plugin -> `datocms-frontend-integrations`
