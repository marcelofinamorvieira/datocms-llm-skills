# Environment Commands

Managing DatoCMS environments (sandboxes) and making raw API calls from the CLI.

---

## Simple Environment Commands

- **`environments:list`** — List all primary and sandbox environments: `npx datocms environments:list`
- **`environments:primary`** — Get the ID of the primary environment: `npx datocms environments:primary`
- **`environments:rename`** — Rename an environment: `npx datocms environments:rename <ENVIRONMENT_ID> <NEW_ENVIRONMENT_ID>`
- **`environments:destroy`** — Destroy a sandbox environment: `npx datocms environments:destroy <ENVIRONMENT_ID>`

**Warning:** `environments:destroy` permanently deletes the environment and all its data.

---

## environments:fork

Create a new sandbox environment by forking an existing one:

```bash
npx datocms environments:fork <SOURCE_ENVIRONMENT_ID> <NEW_ENVIRONMENT_ID>
```

Run `npx datocms environments:fork --help` for all flags (includes `--fast` and `--force` options).

### Examples

```bash
# Fork primary into a sandbox named "staging"
npx datocms environments:fork main staging

# Fast fork for large environments
npx datocms environments:fork main staging --fast

# Force fast fork even if editors are active
npx datocms environments:fork main staging --fast --force
```

---

## environments:promote

Promote a sandbox environment to primary:

```bash
npx datocms environments:promote <ENVIRONMENT_ID>
```

### Example

```bash
npx datocms environments:promote staging
```

**Warning:** This replaces the current primary environment. The old primary becomes a sandbox.

---

## cma:call

Make raw Content Management API calls from the command line:

```bash
npx datocms cma:call <RESOURCE> <METHOD> [flags]
```

Run `npx datocms cma:call --help` for all arguments and flags.

### Examples

```bash
# List all models
npx datocms cma:call item_types list

# Find a specific record
npx datocms cma:call items find --params='{"item_id": "12345"}'

# Create a record
npx datocms cma:call items create --data='{"item_type": {"type": "item_type", "id": "blog_post"}, "title": "Hello"}'

# List records with filtering
npx datocms cma:call items list --params='{"filter": {"type": "blog_post"}}'

# Target a specific environment
npx datocms cma:call items list --environment=staging
```
