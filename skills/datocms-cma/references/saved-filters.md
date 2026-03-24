# Saved Filters

Covers saved filter presets for both the record listing view (record filters) and the media library view (upload filters) in the DatoCMS dashboard.

## Quick Navigation

- [Record Filters](#record-filters)
- [Creating a Record Filter](#creating-a-record-filter)
- [Listing Record Filters](#listing-record-filters)
- [Finding a Record Filter](#finding-a-record-filter)
- [Updating a Record Filter](#updating-a-record-filter)
- [Deleting a Record Filter](#deleting-a-record-filter)
- [Upload Filters](#upload-filters)
- [Creating an Upload Filter](#creating-an-upload-filter)
- [Listing Upload Filters](#listing-upload-filters)
- [Finding an Upload Filter](#finding-an-upload-filter)
- [Updating an Upload Filter](#updating-an-upload-filter)
- [Deleting an Upload Filter](#deleting-an-upload-filter)
- [Complete Example](#complete-example-create-shared-filters-for-content-team)

---

## Record Filters

Record filters (`itemTypeFilters`) are saved filter presets for the record listing view. They let team members quickly access commonly used filter/sort/column configurations for a specific model.

### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `name` | `string` | Filter display name |
| `filter` | `object` | Serialized filter state (query, field filters, meta filters) |
| `columns` | `string[] \| null` | Visible columns in the listing |
| `order_by` | `string \| null` | Sort order (e.g., `"_updated_at_DESC"`) |
| `shared` | `boolean` | Whether the filter is visible to all team members |
| `item_type` | `{ id: string; type: "item_type" }` | Model this filter applies to |

---

## Creating a Record Filter

```ts
const blogPostModelId = "abc123"; // the ID of the model to filter

const draftPostsFilter = await client.itemTypeFilters.create({
  name: "Draft Blog Posts",
  filter: {
    query: "",
    fields: {},
    meta: { status: { eq: "draft" } },
  },
  columns: null,
  order_by: "_updated_at_DESC",
  shared: true,
  item_type: { id: blogPostModelId, type: "item_type" },
});

console.log("Created record filter:", draftPostsFilter.id);
```

**Important:** The `filter` object structure mirrors the internal filter state of the DatoCMS UI. The exact shape depends on which field and meta filters are active.

---

## Listing Record Filters

```ts
const recordFilters = await client.itemTypeFilters.list();

for (const filter of recordFilters) {
  const visibility = filter.shared ? "shared" : "private";
  console.log(`${filter.name} (${visibility})`);
}
```

---

## Finding a Record Filter

```ts
const recordFilter = await client.itemTypeFilters.find("filter-id");
console.log(recordFilter.name, recordFilter.order_by);
```

---

## Updating a Record Filter

```ts
const updatedRecordFilter = await client.itemTypeFilters.update("filter-id", {
  name: "Draft Blog Posts (Updated)",
  shared: false,
});

console.log("Updated filter:", updatedRecordFilter.name);
```

---

## Deleting a Record Filter

```ts
await client.itemTypeFilters.destroy("filter-id");
console.log("Record filter deleted");
```

---

## Upload Filters

Upload filters (`uploadFilters`) are saved filter presets for the media library view. They help team members quickly filter assets by type, tags, or search queries.

### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `name` | `string` | Filter display name |
| `filter` | `object` | Serialized filter state (type, query, tags) |
| `shared` | `boolean` | Whether the filter is visible to all team members |

---

## Creating an Upload Filter

```ts
const untaggedImagesFilter = await client.uploadFilters.create({
  name: "Untagged Images",
  filter: {
    type: "image",
    query: "",
    tags: { eq: [] },
  },
  shared: true,
});

console.log("Created upload filter:", untaggedImagesFilter.id);
```

---

## Listing Upload Filters

```ts
const uploadFilters = await client.uploadFilters.list();

for (const filter of uploadFilters) {
  const visibility = filter.shared ? "shared" : "private";
  console.log(`${filter.name} (${visibility})`);
}
```

---

## Finding an Upload Filter

```ts
const uploadFilter = await client.uploadFilters.find("filter-id");
console.log(uploadFilter.name);
```

---

## Updating an Upload Filter

```ts
const updatedUploadFilter = await client.uploadFilters.update("filter-id", {
  name: "Untagged Images (All Types)",
  filter: {
    type: "all",
    query: "",
    tags: { eq: [] },
  },
});

console.log("Updated upload filter:", updatedUploadFilter.name);
```

---

## Deleting an Upload Filter

```ts
await client.uploadFilters.destroy("filter-id");
console.log("Upload filter deleted");
```

---

## Complete Example: Create Shared Filters for Content Team

```ts
import { buildClient, ApiError } from "@datocms/cma-client-node";

async function createSharedFiltersForContentTeam() {
  const client = buildClient({
    apiToken: process.env.DATOCMS_API_TOKEN!,
  });

  // Step 1: Find the blog_post model by listing all models
  const models = await client.itemTypes.list();
  const blogPostModel = models.find((model) => model.api_key === "blog_post");

  if (!blogPostModel) {
    throw new Error("blog_post model not found");
  }

  console.log("Found blog_post model:", blogPostModel.id);

  // Step 2: Create a record filter for draft blog posts
  const draftPostsFilter = await client.itemTypeFilters.create({
    name: "Draft Blog Posts",
    filter: {
      query: "",
      fields: {},
      meta: { status: { eq: "draft" } },
    },
    columns: null,
    order_by: "_updated_at_DESC",
    shared: true,
    item_type: { id: blogPostModel.id, type: "item_type" },
  });

  console.log("Created record filter:", draftPostsFilter.id, draftPostsFilter.name);

  // Step 3: Create an upload filter for untagged images
  const untaggedImagesFilter = await client.uploadFilters.create({
    name: "Untagged Images",
    filter: {
      type: "image",
      query: "",
      tags: { eq: [] },
    },
    shared: true,
  });

  console.log("Created upload filter:", untaggedImagesFilter.id, untaggedImagesFilter.name);

  // Step 4: List all record filters
  const allRecordFilters = await client.itemTypeFilters.list();

  console.log(`\nAll record filters (${allRecordFilters.length}):`);

  for (const filter of allRecordFilters) {
    const visibility = filter.shared ? "shared" : "private";
    const modelId = filter.item_type.id;
    console.log(`  - ${filter.name} (${visibility}, model: ${modelId})`);
  }

  // Step 5: List all upload filters
  const allUploadFilters = await client.uploadFilters.list();

  console.log(`\nAll upload filters (${allUploadFilters.length}):`);

  for (const filter of allUploadFilters) {
    const visibility = filter.shared ? "shared" : "private";
    console.log(`  - ${filter.name} (${visibility})`);
  }

  // Step 6: Update the record filter to also customize visible columns
  const updatedRecordFilter = await client.itemTypeFilters.update(draftPostsFilter.id, {
    columns: ["title", "_status", "_updated_at"],
  });

  console.log("\nUpdated record filter columns:", updatedRecordFilter.columns);

  // Step 7: Clean up — delete the filters we created
  await client.itemTypeFilters.destroy(draftPostsFilter.id);
  console.log("Deleted record filter:", draftPostsFilter.id);

  await client.uploadFilters.destroy(untaggedImagesFilter.id);
  console.log("Deleted upload filter:", untaggedImagesFilter.id);

  console.log("\nDone! Shared filters created, listed, updated, and cleaned up.");
}

createSharedFiltersForContentTeam().catch((error) => {
  if (error instanceof ApiError) {
    console.error("API Error:", error.response.status, error.errors);
  } else {
    console.error(error);
  }
  process.exit(1);
});
```
