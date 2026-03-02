---
name: datocms-plugin-builder
description: >-
  Build DatoCMS plugins using datocms-plugin-sdk. Use when users want to
  create or modify a DatoCMS plugin, work with the connect() function,
  field extensions, sidebar panels, custom pages, dropdown actions,
  asset sources, lifecycle hooks, modals, config screens, inspectors,
  outlets, upload sidebars, record presentation, structured text
  customization, or any plugin SDK hooks.
---

# DatoCMS Plugin Builder

Interactive guide for building DatoCMS plugins using the `datocms-plugin-sdk` package.

## Interactive Build Flow

Follow these steps IN ORDER. Ask questions before generating any code. Do not skip steps.

### Step 1: Detect Project State

Silently examine the working directory to determine whether this is an existing plugin project or a new one:

1. Check `package.json` for `datocms-plugin-sdk` in dependencies
2. Check for `src/main.tsx` or `src/index.tsx` with a `connect()` call
3. Check for build config (`vite.config.ts` or `vite.config.js`)

**Augment mode** (existing plugin found):
- Read the existing `connect()` call to understand which hooks are already implemented
- Read existing component files to understand patterns in use
- Check `package.json` for existing dependencies
- You will ADD to or modify the existing code, not replace it

**Scaffold mode** (no existing plugin):
- You will create the full project structure from scratch

Tell the user which mode you detected and what you found.

### Step 1b: Scaffold the Project (Scaffold Mode Only)

If in scaffold mode, before asking detailed plugin questions:

1. **Ask for the plugin name** using `AskUserQuestion` (e.g., "What should we name this plugin?"). This will be used as the folder name.
2. **Create the project structure manually** using the patterns from `references/project-scaffold.md`. Create the plugin directory **inside the current working directory** (e.g., `./my-plugin-name/`). Create:
   - The plugin directory with the chosen name
   - `package.json` with DatoCMS plugin metadata and dependencies
   - `tsconfig.json`, `tsconfig.app.json`, and `tsconfig.node.json`
   - `vite.config.ts`
   - `index.html`
   - `src/main.tsx` (entry point with `connect()`)
   - `src/vite-env.d.ts` (Vite type declarations)
   - `src/utils/render.tsx` (React render utility)
   - `src/entrypoints/` directory for render hook components

   Read `references/project-scaffold.md` for the exact file contents and structure.

3. **Run `npm install`** inside the new plugin directory so dependencies are available for type checking and the dev server.
4. All subsequent file operations happen **inside the new plugin directory**.

### Step 2: Discovery Questions

Ask the user the relevant discovery questions using `AskUserQuestion`. Since `AskUserQuestion` supports a maximum of 4 questions per call, **combine purpose + features into a single question**, and batch the remaining questions together. If you still have more than 4 questions, use two sequential `AskUserQuestion` calls.

1. **Plugin purpose + features**: What should this plugin do, and which features does it need? After the user describes the purpose, **infer likely features** and confirm them (e.g., "settings"/"API key" → config screen, "custom field UI" → field extension, "validate before save" → lifecycle hook). Available features:
   - **Field extension** — **editor** (replaces the default field input) or **addon** (extra UI below the field input). If the UI needs to **control** the field value, use editor. If it **displays** info about the value, use addon. When unsure, addon is safer. **Restriction**: never use editor for Modular Content, Single Block, or Structured Text fields. Also decide **manual** (user installs per-field) vs **override** (plugin auto-applies based on conditions like field type or model) — see `field-extensions.md`.
   - **Sidebar panel** — collapsible panel in the record editing sidebar
   - **Custom page** — full page via navigation tab, settings area, or content sidebar
   - **Dropdown actions** — custom actions in context menus (5 scopes: field, record form, records, assets, schema)
   - **Asset source** — custom upload source in the Media Area (renders a picker, calls `ctx.select()`)
   - **Lifecycle hook** — runs at specific moments: `onBoot`, `onBeforeItemUpsert`, `onBeforeItemsPublish`, `onBeforeItemsUnpublish`, `onBeforeItemsDestroy`
   - **Config screen** — global settings page for plugin configuration
   - **Custom modal** — popup dialog opened from other plugin contexts
   - **Outlet** — banner/widget at the top of a record form (`itemFormOutlets`) or collection view (`itemCollectionOutlets`)
   - **Inspector** — split-screen: custom left panel + DatoCMS-managed right panel (record list, editor, or custom panel)
   - **Upload sidebar** — UI in the Media Area asset detail view (collapsible panel or full-width sidebar)
   - **Structured text customization** — custom inline marks or block-level styles for Structured Text fields
   - **Record presentation** — customize record display in lists/link fields, or pre-filter the record picker
2. **DatoCMS API access**: Does the plugin need to fetch or update DatoCMS records, assets, or models via the Content Management API? If yes, the plugin needs the `@datocms/cma-client-browser` dependency and the `"currentUserAccessToken"` permission in `package.json`.
3. **Target scope**: Should this apply to all models or specific ones?
4. **External dependencies**: Any external APIs or npm packages needed?

In **augment mode**, also ask: What should be ADDED to the existing plugin?

Adapt the questions based on what makes sense — skip irrelevant ones (e.g., don't ask about target models for an asset source). Infer features from the user's purpose description and present your best guess for confirmation rather than making the user pick from a raw list.

### Step 3: Load References

Based on the user's answers, use the `Read` tool to load the appropriate reference files from the `references/` directory next to this skill file. **Always** read the core architecture reference. Only load what's relevant — don't load everything.

**Always load:**
- `references/sdk-architecture.md`

**Load per feature:**
- Field extension → `references/field-extensions.md`
- Sidebar panel → `references/sidebar-panels.md`
- Custom page → `references/custom-pages.md`
- Dropdown actions → `references/dropdown-actions.md`
- Asset source → `references/asset-sources.md`
- Lifecycle hook → `references/lifecycle-hooks.md`
- Config screen → `references/config-screen.md`
- Custom modal → `references/modals.md`
- Outlet (form or collection) → `references/outlets.md`
- Inspector → `references/inspectors.md`
- Upload sidebar or upload sidebar panel → `references/upload-sidebars.md`
- Structured text customization → `references/structured-text.md`
- Record presentation → `references/record-presentation.md`

**Load if needed:**
- Reading `ctx.formValues` outside field extensions (sidebar panels, outlets, dropdown execute hooks), or programmatically reading/modifying Structured Text or Modular Content values from any context → `references/form-values.md`
- Scaffold mode → `references/project-scaffold.md` (already loaded if Step 1b ran)

### Step 4: Explore Project (Augment Mode Only)

If in augment mode:

1. Read the existing `connect()` call — understand all currently implemented hooks
2. Read existing component files for code patterns and conventions
3. Check `package.json` dependencies — know what's already available
4. Identify where new code should go (new files vs. modifying existing ones)
5. Follow the existing code style (naming, file organization, component patterns)

Build on existing patterns — don't rewrite working code.

### Step 5: Generate Code

**Scaffold mode:**
- The project structure was created in Step 1b
- Modify the `connect()` call in `src/main.tsx` to add the hooks the user needs
- Create component files in `src/entrypoints/` for each render hook
- Add any extra dependencies to `package.json` if needed

**Augment mode:**
- Add new hooks to the existing `connect()` call
- Create new component files for new render hooks
- Add new dependencies to `package.json` if needed
- Keep existing code intact

**Always ensure (every plugin):**
- Every rendered component is wrapped in `<Canvas ctx={ctx}>` (use `noAutoResizer` for pages, full-width sidebars, and inspectors)
- `'datocms-react-ui/styles.css'` is imported once in the entry file
- The `render()` utility is used in all render hooks
- Proper TypeScript types are imported using `import type { ... }` from `datocms-plugin-sdk` (the `import type` syntax is required because `isolatedModules` is enabled)
- Declaration hooks return the correct data structures, and IDs in declaration hooks match the IDs checked in render hooks
- **Always use a `switch` statement** in render hooks that dispatch by ID (`renderFieldExtension`, `renderPage`, `renderItemFormSidebarPanel`, `renderItemFormSidebar`, `renderModal`, `renderAssetSource`, `renderItemFormOutlet`, `renderItemCollectionOutlet`, `renderUploadSidebarPanel`, `renderUploadSidebar`, `renderInspector`, `renderInspectorPanel`) — even if there's only one case right now
- When using `useEffect` with `ctx` properties as dependencies, use `useDeepCompareEffect` from `use-deep-compare-effect` instead — the `ctx` object is recreated on every iframe message
- Guard `ctx.item` — it is `null` for new records (not yet saved). Always check before accessing record data.
- When generating code that uses optional packages (`lodash-es`, `use-deep-compare-effect`, `react-final-form`/`final-form`, `@datocms/cma-client-browser`, `datocms-structured-text-slate-utils`), always add them to `package.json` dependencies (and `@types/lodash-es` to devDependencies when using `lodash-es`)

**Ensure when applicable:**
- In **editor** field extensions, always check `ctx.disabled` and prevent all user input when `true` — this is a correctness requirement, not optional polish
- In field extensions, always use `get(ctx.formValues, ctx.fieldPath)` from `lodash-es` to read the current field value — do NOT use `ctx.formValues[ctx.fieldPath]` directly
- **Never** create Editor field extensions for Modular Content (`rich_text`), Single Block (`single_block`), or Structured Text (`structured_text`) fields — use Addon extensions instead
- Use `initialHeight: 0` for addons, outlets, and sidebar panels that may conditionally render nothing
- When using `ctx.navigateTo()` for plugin pages, always build environment-aware paths: `const envPrefix = ctx.isEnvironmentPrimary ? '' : \`/environments/${ctx.environment}\``
- Parameters passed to `ctx.openModal()` and values passed to `ctx.resolve()` must be JSON-serializable
- For plugins with configuration, create a `normalizeParameters()` function and a type guard (e.g., `isValidConfig()`) to handle empty or legacy parameter formats. See `references/config-screen.md`.
- For asset sources, URLs passed to `ctx.select({ resource: { url } })` **must be CORS-enabled**. If the source API doesn't support CORS, use the base64 resource format instead.
- In `renderManualFieldExtensionConfigScreen`, do **not** use form management libraries — use `ctx.setParameters()` directly

### Step 6: Wire Up & Verify

Guide the user through getting the plugin running:

1. **Install dependencies**: `npm install` (skip if no new dependencies were added since the last install — e.g., scaffold mode where Step 5 didn't add extra packages)
2. **Start dev server**: Tell the user to run `npm run dev` (starts at `http://localhost:5173/`). If it's already running, skip this step.
3. **Install in DatoCMS**:
   - Go to Settings > Plugins > Add new > Create a private plugin
   - Set entry point URL to `http://localhost:5173/`
4. **Plugin-type-specific testing**:
   - Field extension: Go to a record form, check the field has the new editor/addon
   - Sidebar panel: Go to a record form, check the sidebar for the new panel
   - Custom page: Check the navigation bar or settings area for the new tab/page
   - Dropdown action: Check the relevant dropdown menu
   - Asset source: Go to Media Area, click Upload, check for the new source
   - Config screen: Go to plugin settings page
   - Outlet: Go to a record form (or collection view) for the targeted model, check the top for the outlet
   - Inspector: Check the navigation bar for the new tab
   - Upload sidebar: Open an asset in the Media Area, check the sidebar
5. **Common issues**:
   - Blank iframe → Check browser console for errors
   - Plugin not loading → Verify the dev server URL matches the entry point
   - Missing styles → Ensure `'datocms-react-ui/styles.css'` is imported
   - `connect()` not running → Ensure `index.html` has `<div id="root"></div>` and correct script path
   - Field extension not showing → Check `fieldTypes` matches the field type, verify model targeting in `overrideFieldExtensions`
   - Page content cut off or not filling screen → Ensure `<Canvas ctx={ctx} noAutoResizer>` is used for pages, full-width sidebars, and inspectors
   - Plugin not loading in Safari → Safari does not support localhost iframes. Use Chrome or Firefox for local development.
   - Field extension state lost when field is hidden/shown → `ctx.toggleField()` completely **destroys** the field's plugin iframes when hiding and recreates them when showing. All React state is lost. If you need to preserve state across visibility changes, store it in plugin parameters or a ref outside the component tree.
   - `useEffect` running too often → The `ctx` object is recreated on every iframe message. Use `useDeepCompareEffect` instead of `useEffect` when depending on `ctx` properties.

### Step 7: Polish (if requested or needed)

Only apply these improvements if the user requests them or if clearly needed:

- **Error boundaries**: Wrap components in React error boundaries for graceful failure
- **Loading states**: Use `<Spinner />` for async operations
- **Config screen validation**: Validate settings before saving
- **Edge cases**:
  - Handle localized fields — see `references/field-extensions.md` for field extensions (uses `ctx.fieldPath`), and `references/form-values.md` for all other contexts (uses `readFieldValue` helper)
- **`onBoot` migration**: If plugin parameters evolve, use `onBoot` to migrate old formats
- **Lazy loading**: Use `React.lazy()` + `Suspense` for code splitting on larger plugins
- **Permission checks**: Always check `ctx.currentRole.meta.final_permissions.can_edit_schema` before `updatePluginParameters`
- **Publishing**: If the user wants to publish to npm/marketplace, ensure `package.json` meets requirements: name starts with `datocms-plugin-`, keywords include `datocms-plugin`, `homepage` is filled in, `datoCmsPlugin.permissions` array is present, and all asset paths in `dist/index.html` are relative. See `references/project-scaffold.md` for details.
