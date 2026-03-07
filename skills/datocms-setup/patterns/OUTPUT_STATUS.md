# Output Status Definitions

Use these labels consistently when reporting recipe results.

---

## `scaffolded`

The implementation is structurally complete but contains unresolved placeholders or project-specific values that the user must fill in. Examples:

- `YOUR_API_TOKEN` placeholder in env files
- `// TODO: add your model-to-route mappings` comments
- Generic search index IDs that need replacement

Always explicitly list every placeholder that remains.

---

## `production-ready`

The implementation is fully functional with no unresolved values. All tokens, routes, model mappings, and configuration are wired to real project values.

This status requires that:
- All environment variables reference real values or are populated
- All route mappings and model API keys match the actual DatoCMS project
- No placeholder comments remain in generated code
- The feature works end-to-end without manual edits
