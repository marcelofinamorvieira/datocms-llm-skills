# Client Types and Runtime Behaviors

Load this reference when the task uses `raw*()` methods, generated CMA types, advanced client behavior, platform limits, or site-level metadata.

## Quick Navigation

- [The Dual API Surface](#the-dual-api-surface)
  - [JSON:API Payload Structure](#jsonapi-payload-structure)
  - [Raw Method Examples](#raw-method-examples)
  - [When to Use Raw vs Simplified](#when-to-use-raw-vs-simplified)
- [Type System](#type-system)
  - [Common Type Properties](#common-type-properties)
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

### JSON:API Payload Structure

The raw API methods exchange payloads conforming to the JSON:API specification. Every raw request and response body follows this shape:

```ts
const rawPayload = {
  data: {
    type: "item",
    id: "record_123",
    attributes: {
      title: "Hello World",
      slug: "hello-world",
    },
    relationships: {
      item_type: {
        data: { type: "item_type", id: "model_123" },
      },
      creator: {
        data: { type: "account", id: "account_456" },
      },
    },
    meta: {
      created_at: "2025-01-15T10:00:00.000+00:00",
      updated_at: "2025-01-15T12:30:00.000+00:00",
      published_at: "2025-01-15T12:30:00.000+00:00",
      status: "published",
      current_version: "version_789",
      is_valid: true,
    },
  },
};
```

**Important:** The simplified API flattens this structure so you work with `record.title` directly instead of `record.data.attributes.title`. The raw API preserves the full JSON:API envelope.

### Raw Method Examples

**`rawCreate()` — full JSON:API body with type, attributes, and relationships:**

```ts
const rawResponse = await client.items.rawCreate({
  data: {
    type: "item",
    attributes: {
      title: "New Article",
      slug: "new-article",
      body: "Article content here.",
    },
    relationships: {
      item_type: {
        data: { type: "item_type", id: "model_123" },
      },
    },
  },
});

const recordId = rawResponse.data.id;
const recordTitle = rawResponse.data.attributes.title;
```

**`rawUpdate()` — partial update with JSON:API payload:**

```ts
const rawUpdated = await client.items.rawUpdate("record_123", {
  data: {
    type: "item",
    id: "record_123",
    attributes: {
      title: "Updated Title",
    },
    meta: {
      current_version: "version_789",
    },
  },
});
```

**`rawList()` — accessing `meta.total_count` and pagination metadata:**

```ts
const rawListResponse = await client.items.rawList({
  filter: { type: "model_123" },
  page: { limit: 0 },
});

const totalRecords = rawListResponse.meta.total_count;
```

**Important:** Setting `page.limit: 0` returns zero records but still includes `meta.total_count`, which is useful for counting without fetching data.

```ts
const rawPage = await client.items.rawList({
  filter: { type: "model_123" },
  page: { offset: 0, limit: 30 },
});

const records = rawPage.data;
const totalCount = rawPage.meta.total_count;
```

**`rawFind()` — with query params:**

```ts
const rawRecord = await client.items.rawFind("record_123", {
  nested: true,
  version: "published",
});

const rawRecordAttributes = rawRecord.data.attributes;
const rawRecordRelationships = rawRecord.data.relationships;
```

### When to Use Raw vs Simplified

| Scenario | Use |
|----------|-----|
| Standard CRUD operations | Simplified |
| Need `meta.total_count` without fetching records | Raw (`rawList` with `page.limit: 0`) |
| Working with generated CMA types on the raw path | Raw |
| Need relationship includes or response metadata | Raw |
| Migration/export needing full JSON:API payloads | Raw |
| Everything else | Simplified |

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

### Common Type Properties

**Important:** These properties reflect the simplified API surface. Raw API types (`RawApiTypes.*`) wrap these in JSON:API structure with `data.attributes` and `data.relationships`.

**Important:** Type properties may vary between `@datocms/cma-client` versions. When in doubt, check the installed package's type definitions.

#### `ApiTypes.Item`

| Property | Type | Description |
|----------|------|-------------|
| `id` | `string` | Record ID |
| `item_type` | `{ id: string; type: "item_type" }` | Reference to the model this record belongs to |
| `meta.status` | `"draft" \| "updated" \| "published"` | Publication status |
| `meta.created_at` | `string` | ISO 8601 creation timestamp |
| `meta.updated_at` | `string` | ISO 8601 last update timestamp |
| `meta.published_at` | `string \| null` | ISO 8601 last publish timestamp |
| `meta.first_published_at` | `string \| null` | ISO 8601 first publish timestamp |
| `meta.current_version` | `string` | Version identifier for optimistic locking |
| `meta.is_valid` | `boolean` | Whether the record passes all validations |
| `meta.stage` | `string \| null` | Current workflow stage (if workflows are enabled) |
| `creator` | `{ id: string; type: "account" \| "access_token" \| "sso_user" }` | Who created the record |
| `[fieldApiKey]` | varies | Dynamic field values keyed by field API key |

#### `ApiTypes.ItemCreateSchema`

| Property | Type | Description |
|----------|------|-------------|
| `item_type` | `{ id: string; type: "item_type" }` | **Required.** Reference to the target model |
| `id` | `string \| undefined` | Optional custom record ID |
| `meta.created_at` | `string \| undefined` | Optional override for creation timestamp |
| `meta.updated_at` | `string \| undefined` | Optional override for update timestamp |
| `meta.first_published_at` | `string \| undefined` | Optional override for first publish timestamp |
| `meta.status` | `string \| undefined` | Optional initial publication status |
| `meta.current_version` | `string \| undefined` | Optional version identifier |
| `creator` | `{ id: string; type: string } \| undefined` | Optional creator override |
| `[fieldApiKey]` | varies | Field values keyed by field API key |

#### `ApiTypes.ItemUpdateSchema`

| Property | Type | Description |
|----------|------|-------------|
| `[fieldApiKey]` | varies | Field values to update (partial update — omitted fields are left unchanged) |
| `meta.current_version` | `string \| undefined` | Pass this for optimistic locking to prevent conflicting writes |

**Important:** Only include the fields you want to change. Omitted fields retain their current values.

#### `ApiTypes.ItemType`

| Property | Type | Description |
|----------|------|-------------|
| `id` | `string` | Model ID |
| `name` | `string` | Human-readable model name |
| `api_key` | `string` | API identifier for the model |
| `singleton` | `boolean` | Whether the model allows only one record |
| `modular_block` | `boolean` | Whether this model is a modular block (not a standalone model) |
| `sortable` | `boolean` | Whether records can be manually sorted |
| `tree` | `boolean` | Whether records are organized in a tree hierarchy |
| `draft_mode_active` | `boolean` | Whether draft/published workflow is enabled |
| `all_locales_required` | `boolean` | Whether all project locales are required for localized fields |
| `collection_appearance` | `string` | Default UI appearance for the record collection |
| `ordering_direction` | `string \| null` | Default sort direction |
| `ordering_meta` | `string \| null` | Meta field used for default ordering |

#### `ApiTypes.Field`

| Property | Type | Description |
|----------|------|-------------|
| `id` | `string` | Field ID |
| `label` | `string` | Human-readable field label |
| `api_key` | `string` | API identifier used as the key in record payloads |
| `field_type` | `string` | Field type (e.g., `"string"`, `"text"`, `"boolean"`, `"link"`, `"links"`, `"structured_text"`) |
| `localized` | `boolean` | Whether the field stores per-locale values |
| `validators` | `object` | Validation rules for the field |
| `appearance` | `object` | Editor appearance configuration |
| `default_value` | `unknown` | Default value assigned to new records |
| `position` | `number` | Ordering position within the model |
| `hint` | `string \| null` | Helper text displayed in the editor |

#### `ApiTypes.Upload`

| Property | Type | Description |
|----------|------|-------------|
| `id` | `string` | Upload/asset ID |
| `url` | `string` | Public URL of the asset |
| `filename` | `string` | Original filename including extension |
| `basename` | `string` | Filename without extension |
| `size` | `number` | File size in bytes |
| `width` | `number \| null` | Image width in pixels (null for non-images) |
| `height` | `number \| null` | Image height in pixels (null for non-images) |
| `format` | `string` | File format/extension |
| `mime_type` | `string` | MIME type of the file |
| `is_image` | `boolean` | Whether the upload is an image |
| `md5` | `string` | MD5 hash of the file |
| `blurhash` | `string \| null` | BlurHash placeholder string (images only) |
| `tags` | `string[]` | User-assigned tags |
| `smart_tags` | `string[]` | Auto-detected tags |
| `default_field_metadata` | `object` | Per-locale default alt, title, focal point, and custom data |
| `author` | `string \| null` | Author metadata |
| `copyright` | `string \| null` | Copyright metadata |
| `notes` | `string \| null` | Internal notes |

#### `ApiTypes.Role`

| Property | Type | Description |
|----------|------|-------------|
| `id` | `string` | Role ID |
| `name` | `string` | Role name |
| `can_edit_schema` | `boolean` | Permission to modify models and fields |
| `can_edit_site` | `boolean` | Permission to edit site-level settings |
| `can_manage_users` | `boolean` | Permission to manage collaborators |
| `can_manage_webhooks` | `boolean` | Permission to manage webhooks |
| `environments_access` | `string` | Level of access to environments |
| `positive_item_type_permissions` | `object[]` | Granted per-model permissions |
| `negative_item_type_permissions` | `object[]` | Denied per-model permissions |

#### `ApiTypes.Environment`

| Property | Type | Description |
|----------|------|-------------|
| `id` | `string` | Environment ID (also serves as its name) |
| `meta.primary` | `boolean` | Whether this is the primary environment |
| `meta.status` | `string` | Environment status (e.g., `"ready"`, `"creating"`, `"destroying"`) |

#### `ApiTypes.Webhook`

| Property | Type | Description |
|----------|------|-------------|
| `id` | `string` | Webhook ID |
| `name` | `string` | Human-readable name |
| `url` | `string` | Target URL that receives the webhook POST |
| `headers` | `object` | Custom HTTP headers sent with the request |
| `events` | `string[]` | Event types that trigger the webhook |
| `enabled` | `boolean` | Whether the webhook is active |
| `custom_payload` | `string \| null` | Custom payload template (overrides default JSON:API payload) |
| `payload_api_version` | `string \| null` | API version used for the payload |
| `http_basic_user` | `string \| null` | HTTP Basic auth username |
| `http_basic_password` | `string \| null` | HTTP Basic auth password |
| `auto_retry` | `boolean` | Whether failed deliveries are retried automatically |

#### `ApiTypes.AccessToken`

| Property | Type | Description |
|----------|------|-------------|
| `id` | `string` | Access token ID |
| `name` | `string` | Human-readable token name |
| `token` | `string \| null` | The actual token string (only visible at creation time, null afterward) |
| `hardcoded_type` | `string \| null` | Hardcoded type identifier (if any) |
| `role` | `{ id: string; type: "role" } \| null` | Associated role |
| `can_access_cda` | `boolean` | Whether the token can access the Content Delivery API |
| `can_access_cda_preview` | `boolean` | Whether the token can access the CDA in preview mode |
| `can_access_cma` | `boolean` | Whether the token can access the Content Management API |

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
