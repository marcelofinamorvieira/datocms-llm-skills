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

Run `npx datocms wordpress:import --help` for all flags. Key flags include `--autoconfirm` (skip prompts), `--concurrency` (default: 15), and `--ignore-errors`.

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

Run `npx datocms contentful:import --help` for all flags. Key flags include `--autoconfirm` (skip prompts), `--concurrency` (default: 15), and `--ignore-errors`.

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
