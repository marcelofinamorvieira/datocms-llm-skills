# Creating Migrations

Scaffolding new migration scripts with `migrations:new`.

---

## Command

```bash
npx datocms migrations:new <NAME> [flags]
```

Creates a new migration script in the migrations directory.

### Arguments

| Argument | Required | Description |
|---|---|---|
| `NAME` | Yes | The name to give to the script |

### Flags

| Flag | Type | Description |
|---|---|---|
| `--ts` | boolean | Force creation of a TypeScript migration file (exclusive with `--js`) |
| `--js` | boolean | Force creation of a JavaScript migration file (exclusive with `--ts`) |
| `--template=<path>` | string | Start from a custom template file (exclusive with `--autogenerate`) |
| `--autogenerate=<envs>` | string | Auto-generate by diffing two environments (exclusive with `--template`) |
| `--schema=<filter>` | string | Include schema type definitions for models/blocks (TypeScript only). Use `"all"` or comma-separated API keys |

---

## File Naming Convention

Generated files follow the pattern:

```
{unix_timestamp}_{camelCaseName}.ts|js
```

Examples:
- `npx datocms migrations:new "add blog model"` → `1709312400_addBlogModel.ts`
- `npx datocms migrations:new "seed content" --js` → `1709312400_seedContent.js`

---

## Default Templates

### TypeScript (default for TS projects)

```ts
import { Client } from '@datocms/cli/lib/cma-client-node';

export default async function(client: Client): Promise<void> {
  // DatoCMS migration script

  // For more examples, head to our Content Management API docs:
  // https://www.datocms.com/docs/content-management-api

  const articleModel = await client.itemTypes.create({
    name: 'Article',
    api_key: 'article',
  });

  const titleField = await client.fields.create(articleModel, {
    label: 'Title',
    api_key: 'title',
    field_type: 'string',
    validators: {
      required: {},
    },
  });

  const article = await client.items.create({
    item_type: articleModel,
    title: 'My first article!',
  });
}
```

### JavaScript

```js
'use strict';

/** @param client { import("@datocms/cli/lib/cma-client-node").Client } */
module.exports = async (client) => {
  // DatoCMS migration script

  // For more examples, head to our Content Management API docs:
  // https://www.datocms.com/docs/content-management-api

  const articleModel = await client.itemTypes.create({
    name: 'Article',
    api_key: 'article',
  });

  const titleField = await client.fields.create(articleModel, {
    label: 'Title',
    api_key: 'title',
    field_type: 'string',
    validators: {
      required: {},
    },
  });

  const article = await client.items.create({
    item_type: articleModel,
    title: 'My first article!',
  });
}
```

---

## Format Detection

The CLI determines the file format in this order:

1. If `--template` is provided → use the template file's extension
2. If `--js` flag is set → JavaScript
3. If `--ts` flag is set or a `tsconfig.json` is found → TypeScript
4. Otherwise → JavaScript

---

## Autogenerate Mode

Auto-generates a migration script by diffing the schemas of two environments:

```bash
# Diff sandbox "staging" against primary environment
npx datocms migrations:new "sync staging changes" --autogenerate=staging

# Diff environment "foo" against environment "bar"
npx datocms migrations:new "sync foo to bar" --autogenerate=foo:bar
```

- `--autogenerate=foo` — Finds changes in sandbox `foo` compared to the primary environment
- `--autogenerate=foo:bar` — Finds changes in environment `foo` compared to environment `bar`

This is useful for capturing manual schema changes made in a sandbox and converting them into a reproducible migration script.

---

## Schema Types Flag

For TypeScript migrations, include schema type definitions for autocomplete and type checking:

```bash
# Include types for all models and blocks
npx datocms migrations:new "update schema" --ts --schema=all

# Include types for specific models only
npx datocms migrations:new "update blog" --ts --schema=blog_post,author
```

When `--schema` is used, the generated migration file includes:
- An additional `ItemTypeDefinition` import
- Schema type definitions inserted before the migration function

This flag only works with TypeScript migrations.
