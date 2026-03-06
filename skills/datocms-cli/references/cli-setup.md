# CLI Setup

Installation, configuration, profiles, and global flags for `@datocms/cli`.

---

## Installation

```bash
npm install --save-dev @datocms/cli
```

After installation, commands are available via `npx datocms <command>`.

---

## Configuration File

The CLI uses `datocms.config.json` in the project root. Structure:

```json
{
  "profiles": {
    "default": {
      "logLevel": "NONE",
      "migrations": {
        "directory": "migrations",
        "modelApiKey": "schema_migration",
        "template": "migrations/template.ts",
        "tsconfig": "tsconfig.migrations.json"
      }
    },
    "staging": {
      "logLevel": "BASIC",
      "migrations": {
        "directory": "migrations"
      }
    }
  }
}
```

### Profile Config Properties

| Property | Type | Description |
|---|---|---|
| `logLevel` | `"NONE" \| "BASIC" \| "BODY" \| "BODY_AND_HEADERS"` | API call logging verbosity |
| `logMode` | `"stdout" \| "file" \| "directory"` | Where logs are written |
| `baseUrl` | `string` | Custom API base URL (advanced) |
| `migrations.directory` | `string` | Path to migrations directory (relative to config file) |
| `migrations.modelApiKey` | `string` | API key of the model used to track migrations |
| `migrations.template` | `string` | Path to a custom migration template file |
| `migrations.tsconfig` | `string` | Path to tsconfig for running TS migrations |

---

## Profile Management

### Set a profile

```bash
# Interactive setup for default profile
npx datocms profile:set

# Set a named profile with specific options
npx datocms profile:set staging --log-level=BASIC --migrations-dir=migrations
```

Flags for `profile:set`:
- `--log-level` — Logging level (`NONE`, `BASIC`, `BODY`, `BODY_AND_HEADERS`)
- `--migrations-dir` — Migrations directory path
- `--migrations-model` — API key of migration tracking model
- `--migrations-template` — Path to custom migration template
- `--migrations-tsconfig` — Path to tsconfig for TS migrations
- `--base-url` — Custom API base URL

### Remove a profile

```bash
npx datocms profile:remove staging
```

---

## API Token Resolution

The CLI resolves the API token in this order (first match wins):

1. **`--api-token` flag** — Passed directly on the command line
2. **Environment variable** — Based on the active profile:
   - Default profile: `DATOCMS_API_TOKEN`
   - Named profile (e.g., `staging`): `DATOCMS_STAGING_PROFILE_API_TOKEN`

The token must have CMA access enabled (`can_access_cma: true`).

### Example `.env` setup

```env
# For default profile
DATOCMS_API_TOKEN=your_full_access_token

# For a "staging" profile
DATOCMS_STAGING_PROFILE_API_TOKEN=your_staging_token
```

---

## Global Flags

These flags are available on all CMA-based commands:

| Flag | Description |
|---|---|
| `--api-token=<token>` | Override the API token for this command |
| `--profile=<name>` | Use a specific profile from `datocms.config.json` |
| `--log-level=<level>` | Set logging level (`NONE`, `BASIC`, `BODY`, `BODY_AND_HEADERS`) |
| `--log-mode=<mode>` | Set log output destination (`stdout`, `file`, `directory`) |
| `--json` | Output results as JSON |

### Log Mode Details

- `stdout` — Prints API call logs to the console (colored output)
- `file` — Appends all logs to `./api-calls.log`
- `directory` — Writes each API call to a separate file in `./api-calls/`
