# Client Types and Runtime Behaviors

Load this reference when the task uses `raw*()` methods, generated CMA types, advanced client behavior, platform limits, or site-level metadata.

## Quick Navigation

- [The Dual API Surface](#the-dual-api-surface)
- [Type System](#type-system)
- [Automatic Behaviors](#automatic-behaviors)
- [Technical Limits](#technical-limits)
- [Getting Site Information](#getting-site-information)

---

## The Dual API Surface

Every resource method exists in two forms:

- **Simplified**: `client.items.create(body)` uses friendly attribute-based objects and handles serialization automatically
- **Raw**: `client.items.rawCreate(body)` uses the JSON:API shape directly

Prefer the simplified API unless you specifically need raw JSON:API payloads or metadata such as relationship includes or `meta.total_count`.

```ts
const record = await client.items.create({
  item_type: { id: "model_123", type: "item_type" },
  title: "Hello World",
  slug: "hello-world",
});

console.log(record.id);
console.log(record.title);
```

---

## Type System

```ts
import type { ApiTypes } from "@datocms/cma-client-node";
```

The `ApiTypes` namespace contains the simplified API types. Common ones include:

- `ApiTypes.Item`
- `ApiTypes.ItemCreateSchema`
- `ApiTypes.ItemUpdateSchema`
- `ApiTypes.ItemType`
- `ApiTypes.Field`
- `ApiTypes.Upload`
- `ApiTypes.Webhook`
- `ApiTypes.Role`
- `ApiTypes.Environment`
- `ApiTypes.AccessToken`
- `ApiTypes.Workflow`

The `RawApiTypes` namespace contains the JSON:API equivalents for `raw*()` methods.

Many methods accept an optional generic `D extends ItemTypeDefinition` for per-model type safety. Use this when the project intentionally relies on generated CMA schema types.

**Legacy aliases:** `SimpleSchemaTypes = ApiTypes`, `SchemaTypes = RawApiTypes`. Prefer `ApiTypes` and `RawApiTypes` in new code.

See `references/type-generation.md` for generating the schema types file itself.

---

## Automatic Behaviors

### Rate Limit Retry

When `autoRetry` is `true` (the default), the client automatically retries 429 responses with linear incremental backoff. Do not add your own rate-limit retry loop unless you have a very specific reason.

### Transient Error Retry

Transient server errors (5xx with `transient: true`) are also retried automatically when `autoRetry` is enabled.

### Async Job Polling

Some operations return an async job under the hood. The client automatically polls `client.jobResults.find()` until the job completes and then returns the final result.

Common async-job operations include:

- `client.environments.fork()`
- `client.environments.destroy()`
- `client.itemTypes.update()`
- `client.itemTypes.destroy()`
- `client.fields.create()`
- `client.fields.update()`
- `client.fields.destroy()`
- `client.items.duplicate()`
- `client.items.bulkPublish()`
- `client.items.bulkUnpublish()`
- `client.items.bulkDestroy()`
- `client.items.bulkMoveToStage()`

---

## Technical Limits

| Limit | Value |
|---|---|
| Max record size | 300 KB including nested blocks, excluding assets and linked records |
| Max blocks per record | 600 |
| Max nested block depth | 5 levels |
| Max upload size | 1 GB per asset |
| Rate limit | 60 requests per 3 seconds |
| Bulk operation batch | 200 items per request |

Exceeding these typically triggers `TECHNICAL_LIMIT_REACHED` or `TOO_MANY_OPERATIONS`.

---

## Getting Site Information

Use the site resource when you need locales, timezone, or other project-level settings before mutating data:

```ts
const site = await client.site.find();

console.log(site.locales);
console.log(site.name);
```
