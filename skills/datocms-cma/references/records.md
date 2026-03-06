# Records (Items)

Records are the content entries in DatoCMS. They are instances of models (item types). This is the most-used resource in the CMA.

## Quick Navigation

- [Creating Records](#creating-records)
- [Retrieving Records](#retrieving-records)
- [Listing Records](#listing-records)
- [Updating Records](#updating-records)
- [Publishing and Unpublishing](#publishing-and-unpublishing)
- [Deleting Records](#deleting-records)
- [Duplicating Records](#duplicating-records)
- [Bulk Operations](#bulk-operations)
- [Finding References](#finding-references)
- [Record Versions](#record-versions)
- [Field Value Formats](#field-value-formats)
- [Complete Example: Create, Publish, Update, Delete](#complete-example-create-publish-update-delete)

---

## Creating Records

```ts
const record = await client.items.create({
  item_type: { id: "model_123", type: "item_type" },
  title: "My First Post",
  slug: "my-first-post",
});
```

The `item_type` relationship is **required** — it tells DatoCMS which model this record belongs to. You can use the model's numeric ID or its string ID. With the simplified API, always use the `id`.

### Finding the Model ID

```ts
// List all models and find by api_key
const models = await client.itemTypes.list();
const blogModel = models.find((m) => m.api_key === "blog_post");

// Or find directly if you know the ID
const model = await client.itemTypes.find("model_123");
```

### Creating a Record with All Meta Options

```ts
const record = await client.items.create({
  item_type: { id: modelId, type: "item_type" },
  // Field values — keys are field api_keys
  title: "Hello World",
  body: "Some content...",
  // Optional: provide a specific ID
  id: "custom-id-here",
  // Optional: set creator
  creator: { id: tokenId, type: "access_token" },
  // Optional: set meta (timestamps, status)
  meta: {
    status: "draft",
    created_at: "2024-01-01T00:00:00Z",
    first_published_at: null,
    current_version: "1",
  },
});
```

---

## Retrieving Records

### Find by ID

```ts
const record = await client.items.find("record-id");
```

### With Nested Blocks

When a record has modular content (`rich_text`), structured text (`structured_text`), or single block (`single_block`) fields, pass `nested: true` to inline the block records in the response:

```ts
const record = await client.items.find("record-id", {
  nested: true,
});
// Now record.content contains full block objects instead of just IDs
```

**Important:** Without `nested: true`, block fields contain arrays of block record IDs (strings). With `nested: true`, they contain full block objects with all their attributes. Always use `nested: true` when you need to read block content.

### With Version Info

```ts
const record = await client.items.find("record-id", {
  version: "current", // or "published" or "published-or-current"
});
```

---

## Listing Records

### Basic List (First Page)

```ts
const records = await client.items.list({
  filter: { type: "blog_post" }, // Filter by model api_key or ID
});
```

For auto-pagination, iterator options, counting, and filtering patterns, see `references/filtering-and-pagination.md`. Use that reference whenever a record query may span multiple pages.

---

## Updating Records

### Partial Update

```ts
await client.items.update("record-id", {
  title: "Updated Title",
});
```

Only the fields you specify are updated. Other fields remain unchanged.

### Optimistic Locking

To prevent overwriting concurrent changes, use `meta.current_version`:

```ts
const record = await client.items.find("record-id");

await client.items.update("record-id", {
  title: "Updated Title",
  meta: { current_version: record.meta.current_version },
});
```

If someone else updated the record between your `find` and `update`, the API returns a 409 (Conflict) error.

---

## Publishing and Unpublishing

### Publish a Record

```ts
await client.items.publish("record-id");
```

### Unpublish a Record

```ts
await client.items.unpublish("record-id");
```

### Selective Publication (Specific Locales)

```ts
await client.items.publish("record-id", {
  content_in_locales: ["en", "it"],
  non_localized_content: true,
});
```

This publishes only the specified locales' content and, optionally, non-localized fields.

### Recursive Publish/Unpublish (Tree Models)

For tree-structured models, use `recursive` to cascade to parent/child records:

```ts
// Publish a record and auto-publish its unpublished parents
await client.items.publish("record-id", undefined, { recursive: true });

// Unpublish a record and auto-unpublish its children
await client.items.unpublish("record-id", undefined, { recursive: true });
```

---

## Deleting Records

```ts
await client.items.destroy("record-id");
```

---

## Duplicating Records

```ts
const duplicated = await client.items.duplicate("record-id");
```

This is an async job — the client automatically waits for the job to complete and returns the new record.

---

## Bulk Operations

All bulk operations accept an `items` array of record references and are async jobs. **Maximum 200 items per request** — batch larger sets in groups of 200.

### Bulk Publish

```ts
await client.items.bulkPublish({
  items: [
    { id: "record-1", type: "item" },
    { id: "record-2", type: "item" },
  ],
});
```

### Bulk Unpublish

```ts
await client.items.bulkUnpublish({
  items: [
    { id: "record-1", type: "item" },
    { id: "record-2", type: "item" },
  ],
});
```

### Bulk Destroy

```ts
await client.items.bulkDestroy({
  items: [
    { id: "record-1", type: "item" },
    { id: "record-2", type: "item" },
  ],
});
```

### Bulk Move to Workflow Stage

```ts
await client.items.bulkMoveToStage({
  items: [
    { id: "record-1", type: "item" },
    { id: "record-2", type: "item" },
  ],
  stage: "stage-id",
});
```

---

## Finding References

Get all records that reference a given record:

```ts
const referencingRecords = await client.items.references("record-id");
```

With optional query params (nested, version):

```ts
const refs = await client.items.references("record-id", {
  nested: true,
});
```

---

## Record Versions

List the version history of a record:

```ts
for await (const version of client.itemVersions.listPagedIterator(
  "record-id",
)) {
  console.log(version.id, version.meta.created_at);
}
```

---

## Field Value Formats

When creating or updating records, field values must match the expected format for each field type. All field values are keyed by the field's `api_key`.

### Simple Field Types

| Field type | Value format | Example |
|---|---|---|
| `string` | `string` | `"Hello World"` |
| `text` | `string` (can contain markdown) | `"# Title\n\nBody text"` |
| `boolean` | `boolean` | `true` |
| `integer` | `number` | `42` |
| `float` | `number` | `3.14` |
| `date` | `string` (ISO 8601 date) | `"2024-01-15"` |
| `date_time` | `string` (ISO 8601 datetime) | `"2024-01-15T10:30:00+00:00"` |
| `color` | `{ red, green, blue, alpha }` | `{ red: 255, green: 0, blue: 0, alpha: 255 }` |
| `json` | JSON-serialized string | `JSON.stringify({ key: "value" })` |
| `slug` | `string` | `"hello-world"` |

### Geo Location

```ts
{
  latitude: 40.7128,
  longitude: -74.0060,
}
```

### SEO / Meta Tags

```ts
{
  title: "Page Title",
  description: "Meta description",
  image: "upload-id", // upload ID string, or null
  twitter_card: "summary_large_image", // or null
  no_index: false, // or null
}
```

### Single File (upload)

Minimal — just the upload ID (uses the upload's default metadata):

```ts
{ upload_id: "upload-id" }
```

With per-field metadata overrides:

```ts
{
  upload_id: "upload-id",
  alt: "Alt text",            // optional, overrides upload default
  title: "Image title",       // optional, overrides upload default
  custom_data: {},             // optional
  focal_point: { x: 0.5, y: 0.5 }, // optional
}
```

### Gallery (multiple files)

Array of file objects (same shape as single file):

```ts
[
  { upload_id: "upload-id-1" },
  { upload_id: "upload-id-2", alt: "Custom alt", title: null, custom_data: {}, focal_point: null },
]
```

### Links

| Field type | Value format | Example |
|---|---|---|
| Single link | `string \| null` | `"linked-record-id"` |
| Multiple links | `string[]` | `["record-id-1", "record-id-2"]` |

### Video

```ts
{
  url: "https://www.youtube.com/watch?v=example",
  title: "Video title",
  width: 1920,
  height: 1080,
  provider: "youtube",
  provider_uid: "example",
  thumbnail_url: "https://img.youtube.com/...",
}
```

### Modular Content, Structured Text, Single Block

These are complex field types — see `references/block-records-and-modular-content.md` and `references/structured-text-and-block-tools.md`.

---

## Complete Example: Create, Publish, Update, Delete

```ts
import { buildClient, ApiError } from "@datocms/cma-client-node";

const client = buildClient({
  apiToken: process.env.DATOCMS_API_TOKEN!,
});

async function main() {
  // Find the model
  const models = await client.itemTypes.list();
  const blogModel = models.find((m) => m.api_key === "blog_post");
  if (!blogModel) throw new Error("blog_post model not found");

  // Create a draft record
  const record = await client.items.create({
    item_type: { id: blogModel.id, type: "item_type" },
    title: "My New Post",
    slug: "my-new-post",
    body: "This is the body content.",
  });
  console.log("Created:", record.id);

  // Publish it
  await client.items.publish(record.id);
  console.log("Published");

  // Update it
  await client.items.update(record.id, {
    title: "My Updated Post",
  });
  console.log("Updated");

  // Re-publish after update
  await client.items.publish(record.id);
  console.log("Re-published");

  // Delete it
  await client.items.destroy(record.id);
  console.log("Deleted");
}

main().catch((error) => {
  if (error instanceof ApiError) {
    console.error("API Error:", error.response.status, error.errors);
  } else {
    console.error(error);
  }
  process.exit(1);
});
```
