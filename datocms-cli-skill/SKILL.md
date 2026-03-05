---
name: datocms-cli
description: >-
  Work with the DatoCMS CLI tool (@datocms/cli) for command-line migrations,
  environment operations, and deployment workflows. Use when users ask for
  datocms CLI commands or scripts such as migrations:new, migrations:run,
  migrations:status, migration scaffolding for models/fields/blocks, CLI setup
  with datocms.config.json and profiles, environment commands
  (list/fork/promote/rename/destroy), maintenance-mode toggling, CI/CD migration
  pipelines, and imports from WordPress or Contentful (including assets/content).
---

# DatoCMS CLI Skill

You are an expert at using the DatoCMS CLI (`@datocms/cli`). Follow these steps in order. Do not skip steps.

---

## Step 1: Detect Context

Silently examine the project to determine CLI readiness.

1. Read `package.json` and check for `@datocms/cli` in `devDependencies` (or `dependencies`).
   - If not installed, recommend: `npm install --save-dev @datocms/cli`

2. Look for a `datocms.config.json` file in the project root. This file stores CLI profiles with settings like migration directory, log level, and template paths.

3. Check for a `.env` or `.env.local` file containing `DATOCMS_API_TOKEN`. The CLI resolves tokens in this order:
   - `--api-token` flag on the command
   - Environment variable: `DATOCMS_API_TOKEN` (default profile) or `DATOCMS_<PROFILE_ID>_PROFILE_API_TOKEN` (named profile)

4. Check for a `migrations/` directory to see if migration scripting is already set up.

5. Detect TypeScript: look for `tsconfig.json` or a `migrations.tsconfig` setting in `datocms.config.json`. TypeScript projects default to `.ts` migration files.

**Important:** The CLI requires an API token with CMA access (`can_access_cma: true`). A read-only CDA token will not work. If you see a token named like `DATOCMS_READONLY_API_TOKEN` or `NEXT_PUBLIC_DATOCMS_API_TOKEN`, warn the user.

---

## Step 2: Understand the Task

Classify the user's task into one or more categories:

| Category | Examples |
|---|---|
| **CLI setup** | Install CLI, configure profiles, set API tokens, `datocms.config.json` |
| **Creating migrations** | Scaffold new migration scripts, autogenerate from environment diffs, custom templates |
| **Running migrations** | Execute pending migrations, dry-run, fork-and-run, in-place execution |
| **Environment management** | Fork, promote, rename, destroy, list environments via CLI commands |
| **Deployment workflow** | Maintenance mode, safe deployment sequences, CI/CD integration |
| **Importing content** | WordPress import, Contentful import |

If the user's request is clear and falls into an obvious category, skip clarifying questions and proceed directly.

---

## Step 3: Load References

Based on the task classification, use the `Read` tool to load the appropriate reference files from the `references/` directory next to this skill file. Only load what is relevant.

**Always load:**
- `references/cli-setup.md` — Installation, configuration, profiles, global flags, token resolution

**Load per category:**

| Task category | Reference file |
|---|---|
| Creating migrations | `references/creating-migrations.md` |
| Running migrations | `references/running-migrations.md` |
| Environment management | `references/environment-commands.md` |
| Deployment workflow | `references/deployment-workflow.md` |
| Importing content | `references/importing-content.md` |

**Load cross-cutting references when needed:**
- If creating + running migrations together → load both `creating-migrations.md` and `running-migrations.md`
- If deployment involves environment commands → also load `environment-commands.md`

---

## Step 4: Generate Code

Write commands and scripts following these mandatory rules:

### Command Prefix
- Always use `npx datocms` as the command prefix (ensures the locally installed version is used)
- Example: `npx datocms migrations:new "add blog model" --ts`

### Migration File Templates
- When generating migration file content, use the **exact function signatures** from the reference files
- TypeScript: `export default async function(client: Client): Promise<void>`
- JavaScript: `module.exports = async (client) => {}`
- Import for TypeScript migrations: `import { Client } from '@datocms/cli/lib/cma-client-node'`

### File Naming
- Migration files are automatically named: `{unix_timestamp}_{camelCaseName}.ts|.js`
- Do not manually create migration files — always use `npx datocms migrations:new`

### Migration Script Bodies
- For the CMA API calls inside migration scripts (creating models, fields, records, uploads), defer to the **datocms-cma-skill** reference patterns
- The `client` parameter in migrations is the same CMA client from `@datocms/cma-client-node`

### Environment Safety
- Always specify `--source` when running migrations to be explicit about the target
- Use `--dry-run` first to preview changes before applying
- Prefer fork-and-run (default) over `--in-place` for production environments

---

## Step 5: Verify

Before presenting the final commands or scripts:

1. **API token** — Confirm a CMA-enabled token is available (via env var or `--api-token` flag)
2. **Config file** — If using profiles, verify `datocms.config.json` exists and has the right profile
3. **Migrations directory** — Confirm the migrations directory exists or will be created by the command
4. **TypeScript config** — If generating TS migrations, ensure `tsconfig.json` exists or `--migrations-tsconfig` is set
5. **Environment targeting** — Verify the correct `--source` / `--destination` environment is specified
6. **Safety checks** — For destructive operations (promote, destroy), confirm the user intends to target the right environment

---

## Cross-Skill Routing

This skill covers **CLI commands, flags, configuration, workflows, and migration file scaffolding**. If the task involves any of the following, activate the companion skill:

| Condition | Route to |
|---|---|
| CMA API calls inside migration script bodies (records, schema, uploads) | **datocms-cma-skill** |
| Programmatic environment management via `client.environments.*` in code | **datocms-cma-skill** |
| Generating TypeScript types from schema (`schema:generate`) | **datocms-cma-skill** (see `type-generation.md`) |
| Querying content with GraphQL for frontend display | **datocms-cda-skill** |
| Setting up framework integration, draft mode, or real-time updates | **datocms-frontend-integrations-skill** |
| Building a DatoCMS plugin | **datocms-pluginsdk-skill** |

---

## LLM Failure Observer and Self-Heal Routing

The runtime LLM using this skill is the failure observer. The skill file does not self-detect failures.

### Hard Failure Classes (detect continuously)

1. `knowledge_gap`
2. `inaccuracy_or_conflict`
3. `context_bloat_or_ambiguity`
4. `missing_dependency_or_file`
5. `invalid_output_contract`

### Trigger Rule

On the first hard failure:

1. Stop normal execution immediately.
2. Emit a `Skill Failure Packet v1`.
3. Invoke `$skill-self-heal`.
4. Resume this skill only after a `Skill Repair Report v1` is returned.

### Skill Failure Packet v1

```json
{
  "packet_version": "v1",
  "source_skill": "string",
  "timestamp": "ISO-8601 string",
  "hard_failure_type": "knowledge_gap|inaccuracy_or_conflict|context_bloat_or_ambiguity|missing_dependency_or_file|invalid_output_contract",
  "failing_step": "string",
  "user_request": "string",
  "attempted_actions": ["string"],
  "evidence": ["string"],
  "candidate_files": ["/absolute/path"],
  "confidence": 0.0,
  "stop_reason": "string"
}
```

### Skill Repair Report v1

```json
{
  "report_version": "v1",
  "source_packet_id": "string",
  "files_changed": ["/absolute/path"],
  "validation_results": [
    { "name": "string", "pass": true, "evidence": "string" }
  ],
  "rolled_back": false,
  "root_cause": "string",
  "fix_summary": "string",
  "followups": ["string"]
}
```

### Routing Requirements

1. Keep `candidate_files` limited to absolute paths inside this repository.
2. Include concrete evidence in `evidence` (errors, missing paths, contradictions).
3. Set `confidence` from `0.0` to `1.0`.
