# CLI Setup

Configuration, profiles, token selection, and global flags for `@datocms/cli`.

---

Install the CLI in the project and run it locally:

```bash
npm install --save-dev @datocms/cli
npx datocms --help
```

Use local `npx datocms` commands by default so the repo controls the CLI
version. If the repo already has an established runner style (`pnpm exec`,
`bunx`, package scripts), keep that convention.

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

## Preferred Profile Authoring Flow

Use `profile:set` as the default way to create or update profiles.

### Set a profile

```bash
# Interactive setup for the default profile
npx datocms profile:set

# Set a named profile with specific options
npx datocms profile:set staging --log-level=BASIC --migrations-dir=migrations
```

Run `npx datocms profile:set --help` for all available flags.

### Remove a profile

```bash
npx datocms profile:remove staging
```

---

## Active Profile Selection

The CLI decides **which profile configuration to use** in this order:

1. `--profile=<id>` on the command
2. `DATOCMS_PROFILE=<id>` in the environment
3. `default` profile in `datocms.config.json`

Use `DATOCMS_PROFILE` when multiple commands in the same shell should share the
same non-default profile.

---

## API Token Resolution

Once the active profile is known, the CLI resolves the API token in this order:

1. **`--api-token` flag** — passed directly on the command line
2. **Environment variable for the active profile**
   - default profile: `DATOCMS_API_TOKEN`
   - named profile `staging`: `DATOCMS_STAGING_PROFILE_API_TOKEN`

The token must have CMA access enabled (`can_access_cma: true`).

### Example `.env` setup

```env
# For the default profile
DATOCMS_API_TOKEN=your_full_access_token

# For a named profile
DATOCMS_STAGING_PROFILE_API_TOKEN=your_staging_token
```

---

## Global Flags

Run `npx datocms <command> --help` to see available flags. CMA-based commands
support flags such as `--api-token`, `--profile`, `--log-level`, `--log-mode`,
and `--json`.

### Log Mode Details

- `stdout` — prints API call logs to the console
- `file` — appends logs to `./api-calls.log`
- `directory` — writes each API call to a separate file in `./api-calls/`
