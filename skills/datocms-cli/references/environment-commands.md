# Environment Commands

Managing DatoCMS environments (sandboxes) and making direct CMA calls from the
CLI.

---

## Simple Environment Commands

- **`environments:list`** — list all primary and sandbox environments: `npx datocms environments:list`
- **`environments:primary`** — get the ID of the primary environment: `npx datocms environments:primary`
- **`environments:rename`** — rename an environment: `npx datocms environments:rename <ENVIRONMENT_ID> <NEW_ENVIRONMENT_ID>`
- **`environments:destroy`** — destroy a sandbox environment: `npx datocms environments:destroy <ENVIRONMENT_ID>`

**Warning:** `environments:destroy` permanently deletes the environment and all its data.

---

## environments:fork

Create a new sandbox environment by forking an existing one:

```bash
npx datocms environments:fork <SOURCE_ENVIRONMENT_ID> <NEW_ENVIRONMENT_ID>
```

Run `npx datocms environments:fork --help` for all flags (including `--fast`
and `--force`).

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

Use `cma:call` for one-off CMA operations directly from the terminal.

The command surface is dynamic and follows the installed CLI / `@datocms/cma-client`
version, so always check `npx datocms cma:call --help` before assuming a
resource/method pair exists. DatoCMS announced this dynamic surface on
December 4, 2025.

### Command shape

```bash
npx datocms cma:call <RESOURCE> <METHOD> [...pathArgs]
```

### Examples

```bash
# List all models
npx datocms cma:call item_types list

# Find a specific record
npx datocms cma:call items find 12345

# Create a record
npx datocms cma:call items create --data '{"item_type": {"type": "item_type", "id": "blog_post"}, "title": "Hello"}'

# List records with filtering
npx datocms cma:call items list --params '{"filter": {"type": "blog_post"}}'

# Target a specific environment and profile
npx datocms cma:call items list --environment=staging --profile=staging
```

### Guidance

- Use `--data` for create/update request bodies and `--params` for query parameters
- Add `--environment` when targeting a sandbox
- Use `--profile` or `--api-token` when the command must run against a non-default credential context
- Switch to `datocms-cma` when the task needs loops, branching, retries, or reusable typed code
