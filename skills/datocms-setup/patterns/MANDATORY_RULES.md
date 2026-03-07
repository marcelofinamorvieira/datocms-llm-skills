# Mandatory Rules

These rules apply to every datocms-setup recipe. They are not repeated in individual recipe files.

---

## TypeScript Strictness

- **Never** use `as unknown as SomeType` — this is a forbidden anti-pattern
- Avoid `as SomeType` casts — use type guards or fix upstream types instead
- Prefer `import type { ... }` for type-only imports
- Let TypeScript infer types wherever possible — do not add redundant annotations

---

## File Conflict Handling

- Always read existing files before writing — never blindly overwrite
- Make targeted additions to existing files instead of full replacements
- Preserve existing imports, exports, and surrounding code
- If an existing setup is materially different, patch in place by default
- Only ask about full replacement when the current setup is clearly incompatible or the user explicitly asked for a rewrite

---

## Framework Environment Variable Conventions

| Framework | Public prefix | Server-only | File |
|---|---|---|---|
| Next.js | `NEXT_PUBLIC_` | no prefix | `.env.local` |
| Nuxt | `NUXT_PUBLIC_` (runtime) | `NUXT_` (runtime) | `.env` |
| SvelteKit | `PUBLIC_` | no prefix | `.env` |
| Astro | `PUBLIC_` | no prefix | `.env` |

- Add variables to `.env.example` (with placeholder values) and the actual env file
- Never commit real tokens — use placeholder values in examples

---

## Dependency Installation

Detect the project's package manager before installing:

1. `pnpm-lock.yaml` -> `pnpm add`
2. `yarn.lock` -> `yarn add`
3. `bun.lockb` -> `bun add`
4. Otherwise -> `npm install`

Always install DatoCMS packages as regular dependencies (not devDependencies) unless the package is CLI-only.

---

## Zero Questions Default

Ask zero questions by default. Proceed with sensible defaults and call out assumptions.

Only ask when a safe implementation is blocked by something the repo cannot answer, such as:
- Missing model-to-route mappings required for correctness
- Ambiguous existing setup where patching the wrong file would break things
- Missing external service credentials that have no reasonable default
