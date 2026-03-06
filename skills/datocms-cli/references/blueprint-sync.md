# Blueprint Sync

Keeping one shared DatoCMS migration history in sync across multiple projects by
using CLI profiles.

---

## Recommended Shape

Use one `datocms.config.json` with one profile per project and one shared
`migrations/` directory:

```json
{
  "profiles": {
    "blueprint": {
      "logLevel": "NONE",
      "migrations": {
        "directory": "./migrations",
        "modelApiKey": "schema_migration"
      }
    },
    "client_a": {
      "logLevel": "NONE",
      "migrations": {
        "directory": "./migrations",
        "modelApiKey": "schema_migration"
      }
    },
    "client_b": {
      "logLevel": "NONE",
      "migrations": {
        "directory": "./migrations",
        "modelApiKey": "schema_migration"
      }
    }
  }
}
```

This keeps one canonical migration sequence and avoids drift caused by
per-project migration folders.

---

## Token Naming

The default CLI token env var is:

```bash
DATOCMS_API_TOKEN
```

Named profiles use:

```bash
DATOCMS_<PROFILE_ID>_PROFILE_API_TOKEN
```

Examples:

```bash
DATOCMS_BLUEPRINT_PROFILE_API_TOKEN=...
DATOCMS_CLIENT_A_PROFILE_API_TOKEN=...
DATOCMS_CLIENT_B_PROFILE_API_TOKEN=...
```

The token must have CMA access enabled.

---

## Daily Workflow

### 1. Create migrations once

Author new migrations against the blueprint workflow:

```bash
npx datocms migrations:new "add event model" --ts
```

### 2. Dry-run on a destination profile

```bash
npx datocms migrations:run --profile=client_a --dry-run
```

### 3. Apply to each destination project

Use fork-and-run by default:

```bash
npx datocms migrations:run --profile=client_a --destination=client-a-sync
npx datocms migrations:run --profile=client_b --destination=client-b-sync
```

Promote only after verifying the forked environments:

```bash
npx datocms environments:promote client-a-sync --profile=client_a
npx datocms environments:promote client-b-sync --profile=client_b
```

---

## Automation Guidance

For repeated multi-project rollout, prefer a small local helper script instead
of expanding `package.json` with many profile-specific scripts.

Recommended behavior for that helper:

1. Accept one or more destination profile ids as arguments
2. Compute a unique destination environment id per profile
3. Run `migrations:run --profile=<id> --destination=<env>`
4. Support `--dry-run`
5. Print the created environment ids instead of auto-promoting

Do not auto-promote in the sync helper by default. Promotion is a separate
release decision per project.

---

## Safety Notes

- Preserve an existing shared `migrations.directory` if one already exists
- Do not replace working custom profile ids
- Do not create one migrations directory per project unless the repo already
  follows that pattern and the user explicitly wants to keep it
- If the repo already has materially different profile conventions, patch in
  place rather than normalizing everything
