# Importing Content

WordPress and Contentful import commands.

---

## WordPress Import

### Installation

```bash
npm install --save-dev @datocms/cli-plugin-wordpress
```

### Command

```bash
npx datocms wordpress:import [flags]
```

### Flags

| Flag | Type | Required | Description |
|---|---|---|---|
| `--wp-url=<url>` | string | No* | A URL within a WordPress REST API-enabled site (e.g., `https://www.example.com`) |
| `--wp-json-api-url=<url>` | string | No* | The WordPress JSON API endpoint (e.g., `https://www.example.com/wp-json`). Exclusive with `--wp-url` |
| `--wp-username=<user>` | string | Yes | WordPress username |
| `--wp-password=<pass>` | string | Yes | WordPress password |
| `--autoconfirm` | boolean | No | Skip confirmation prompts (forces destroy of existing `wp_*` models) |
| `--ignore-errors` | boolean | No | Try to continue despite errors during import |
| `--concurrency=<n>` | integer | No | Maximum concurrent operations (default: 15) |

*One of `--wp-url` or `--wp-json-api-url` is needed to specify the WordPress site.

### Import Steps

The import runs in this order:

1. Destroy existing WordPress schema (`wp_*` models) from DatoCMS
2. Import WordPress metadata (concurrently):
   - Categories
   - Tags
   - Authors
   - Assets
3. Import WordPress content (concurrently):
   - Pages
   - Articles

### Example

```bash
npx datocms wordpress:import \
  --wp-url=https://myblog.wordpress.com \
  --wp-username=admin \
  --wp-password=secret \
  --autoconfirm
```

---

## Contentful Import

### Installation

```bash
npm install --save-dev @datocms/cli-plugin-contentful
```

### Command

```bash
npx datocms contentful:import [flags]
```

### Flags

| Flag | Type | Required | Description |
|---|---|---|---|
| `--contentful-token=<token>` | string | No | Contentful read-only API token |
| `--contentful-space-id=<id>` | string | No | Contentful space ID |
| `--contentful-environment=<env>` | string | No | Contentful environment to import from |
| `--autoconfirm` | boolean | No | Skip confirmation prompts (forces destroy of existing Contentful schema) |
| `--ignore-errors` | boolean | No | Try to continue despite errors during import |
| `--skip-content` | boolean | No | Import only the schema (models), skip records and assets |
| `--only-content-type=<types>` | string | No | Import only specific content types (comma-separated Contentful IDs, e.g., `blogPost,author`) |
| `--concurrency=<n>` | integer | No | Maximum concurrent operations (default: 15) |
| `--log-level=<level>` | enum | No | Logging level (`NONE`, `BASIC`, `BODY`, `BODY_AND_HEADERS`) |

### Import Steps

The import runs in this order:

1. Download Contentful schema
2. Destroy existing Contentful schema from DatoCMS
3. Copy Contentful schema:
   - Set locales
   - Import models
   - Import fields
4. Import content (skipped if `--skip-content`):
   - Import assets
   - Import records
5. Add validations to fields

### Examples

```bash
# Full import from Contentful
npx datocms contentful:import \
  --contentful-token=your_token \
  --contentful-space-id=your_space \
  --autoconfirm

# Schema-only import (no content)
npx datocms contentful:import \
  --contentful-token=your_token \
  --contentful-space-id=your_space \
  --skip-content \
  --autoconfirm

# Import specific content types only
npx datocms contentful:import \
  --contentful-token=your_token \
  --contentful-space-id=your_space \
  --only-content-type=blogPost,landingPage,author
```
