# Environment Commands

Managing DatoCMS environments (sandboxes) and making raw API calls from the CLI.

---

## environments:list

List all primary and sandbox environments:

```bash
npx datocms environments:list
```

Displays a table with environment IDs and whether each is the primary environment.

---

## environments:primary

Get the ID of the primary environment:

```bash
npx datocms environments:primary
```

Returns only the primary environment ID — useful in scripts.

---

## environments:fork

Create a new sandbox environment by forking an existing one:

```bash
npx datocms environments:fork <SOURCE_ENVIRONMENT_ID> <NEW_ENVIRONMENT_ID>
```

### Flags

| Flag | Type | Description |
|---|---|---|
| `--fast` | boolean | Fast fork (prevents writes to source environment during fork) |
| `--force` | boolean | Force fast fork even with active editing sessions (requires `--fast`) |

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

## environments:rename

Rename an environment:

```bash
npx datocms environments:rename <ENVIRONMENT_ID> <NEW_ENVIRONMENT_ID>
```

### Example

```bash
npx datocms environments:rename staging production-v2
```

---

## environments:destroy

Destroy a sandbox environment:

```bash
npx datocms environments:destroy <ENVIRONMENT_ID>
```

### Example

```bash
npx datocms environments:destroy staging
```

**Warning:** This permanently deletes the environment and all its data.

---

## cma:call

Make raw Content Management API calls from the command line:

```bash
npx datocms cma:call <RESOURCE> <METHOD> [flags]
```

### Arguments

| Argument | Description |
|---|---|
| `RESOURCE` | The CMA resource (e.g., `items`, `item_types`, `fields`, `uploads`) |
| `METHOD` | The method to call (e.g., `list`, `find`, `create`, `update`, `destroy`) |

### Flags

| Flag | Type | Description |
|---|---|---|
| `--environment=<env>` | string | Target a specific environment |
| `--data=<json>` | string | JSON data for the request body |
| `--params=<json>` | string | JSON query parameters |

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
