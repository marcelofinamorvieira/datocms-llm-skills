# Filtering and Pagination

Covers querying patterns for listing records: pagination, filtering by fields, text search, sorting, and efficient counting.

---

## Pagination Basics

The CMA uses offset/limit pagination. A single `list()` call returns one page of results.

```ts
const firstPage = await client.items.list({
  filter: { type: "blog_post" },
  page: { offset: 0, limit: 20 },
});
```

| Parameter | Type | Default | Max |
|---|---|---|---|
| `page.offset` | `number` | `0` | — |
| `page.limit` | `number` | `30` | `500` (`30` when `nested: true`) |

**Important:** Never manually implement pagination loops. Always use `listPagedIterator()`.

---

## `listPagedIterator()` — Auto-Pagination

The recommended way to iterate over all records in a collection:

```ts
for await (const record of client.items.listPagedIterator({
  filter: { type: "blog_post" },
})) {
  console.log(record.id, record.title);
}
```

This automatically fetches pages sequentially, yielding one record at a time.

### Iterator Options

Pass a second argument to control concurrency and page size:

```ts
for await (const record of client.items.listPagedIterator(
  {
    filter: { type: "blog_post" },
    order_by: "_created_at_DESC",
  },
  {
    concurrency: 5,  // Fetch 5 pages in parallel
    perPage: 100,    // 100 records per page
  },
)) {
  console.log(record.title);
}
```

| Option | Type | Default | Description |
|---|---|---|---|
| `concurrency` | `number` | `1` | Number of concurrent page fetches (1–10). Higher values fetch faster but consume rate limits faster. |
| `perPage` | `number` | `30` | Records per page (max 500). |

**When to use high concurrency:** Read-only scripts that need to fetch thousands of records quickly. Use `concurrency: 1` when the loop also performs writes (to avoid burning rate limit budget).

**Important:** When using `nested: true` in query params, the maximum page size drops to **30** (from the usual 500). The iterator respects this automatically, but be aware it will require more page fetches for large collections.

### Collecting Results into an Array

```ts
const allPosts = [];

for await (const post of client.items.listPagedIterator({
  filter: { type: "blog_post" },
})) {
  allPosts.push(post);
}
```

### Paginated Resources

Most resources with `list()` also have `listPagedIterator()`:

- `client.items.listPagedIterator()`
- `client.uploads.listPagedIterator()`
- `client.webhookCalls.listPagedIterator()`
- `client.buildEvents.listPagedIterator()`
- `client.itemVersions.listPagedIterator()`

Resources with small collections (models, fields, roles, webhooks, etc.) only have `list()` which returns all items at once.

**Note:** `client.auditLogEvents` uses cursor-based pagination, not offset/limit. Use `rawQuery()` for paginated access:

```ts
let nextToken: string | undefined;

do {
  const result = await client.auditLogEvents.rawQuery({
    data: {
      type: "audit_log_query",
      attributes: {
        next_token: nextToken,
      },
    },
  });
  for (const event of result.data) {
    console.log(event.id, event.attributes.action_name);
  }
  nextToken = result.meta.next_token ?? undefined;
} while (nextToken);
```

The simplified `query()` returns a flat `AuditLogEvent[]` (with `event.action_name` directly, no `.attributes` wrapper), but loses `meta.next_token` so it cannot paginate.

---

## Filtering Records

### By Model Type

```ts
// By model api_key
const posts = await client.items.list({
  filter: { type: "blog_post" },
});

// By model ID
const posts = await client.items.list({
  filter: { type: "model_123" },
});

// Multiple model types (comma-separated)
const mixed = await client.items.list({
  filter: { type: "blog_post,news_article" },
});
```

**Important:** Always specify `filter.type` when listing records. Without it, you get records from all models mixed together. Note: `filter.fields` and `order_by` require a single `filter.type` — they cannot be used with comma-separated multi-type filters.

### By Text Search

Full-text search across all text fields:

```ts
const results = await client.items.list({
  filter: {
    type: "blog_post",
    query: "search term",
  },
});
```

**Important:** New or updated content has a ~30-second indexing delay before appearing in `query` text search results. Don't rely on immediate text search after creating/updating records.

### By Specific Record IDs

```ts
const records = await client.items.list({
  filter: {
    type: "blog_post",
    ids: "record-1,record-2,record-3",
  },
});
```

---

## Field-Specific Filters

Filter by specific field values using `filter.fields`:

```ts
const records = await client.items.list({
  filter: {
    type: "blog_post",
    fields: {
      title: { matches: { pattern: "tutorial", case_sensitive: false } },
      published_date: { gt: "2024-01-01" },
    },
  },
});
```

### Filter Operators by Field Type

#### String / Text / Slug

| Operator | Description | Example |
|---|---|---|
| `eq` | Equals | `{ eq: "exact value" }` |
| `neq` | Not equals | `{ neq: "value" }` |
| `matches` | Pattern match | `{ matches: { pattern: "hello", case_sensitive: false } }` |
| `not_matches` | Does not match | `{ not_matches: { pattern: "hello" } }` |
| `exists` | Has any value | `{ exists: true }` |
| `not_exists` | Has no value | `{ not_exists: true }` |

#### Integer / Float

| Operator | Description | Example |
|---|---|---|
| `eq` | Equals | `{ eq: 42 }` |
| `neq` | Not equals | `{ neq: 42 }` |
| `lt` | Less than | `{ lt: 100 }` |
| `lte` | Less than or equal | `{ lte: 100 }` |
| `gt` | Greater than | `{ gt: 0 }` |
| `gte` | Greater than or equal | `{ gte: 0 }` |
| `exists` / `not_exists` | Null check | `{ exists: true }` |

#### Date / DateTime

| Operator | Description | Example |
|---|---|---|
| `eq` | Equals | `{ eq: "2024-01-15" }` |
| `neq` | Not equals | `{ neq: "2024-01-15" }` |
| `lt` | Before | `{ lt: "2024-06-01" }` |
| `lte` | Before or on | `{ lte: "2024-06-01" }` |
| `gt` | After | `{ gt: "2024-01-01" }` |
| `gte` | On or after | `{ gte: "2024-01-01" }` |
| `exists` / `not_exists` | Null check | `{ exists: true }` |

#### Boolean

| Operator | Description | Example |
|---|---|---|
| `eq` | Equals | `{ eq: true }` |

#### Link (single record reference)

| Operator | Description | Example |
|---|---|---|
| `eq` | Links to specific record | `{ eq: "record-id" }` |
| `neq` | Does not link to | `{ neq: "record-id" }` |
| `exists` / `not_exists` | Has/doesn't have a link | `{ exists: true }` |

#### Links (multiple record references)

| Operator | Description | Example |
|---|---|---|
| `any_in` | Contains any of | `{ any_in: ["id-1", "id-2"] }` |
| `all_in` | Contains all of | `{ all_in: ["id-1", "id-2"] }` |
| `eq` | Exact set match | `{ eq: ["id-1", "id-2"] }` |
| `not_in` | Contains none of | `{ not_in: ["id-1"] }` |
| `exists` / `not_exists` | Has/doesn't have links | `{ exists: true }` |

#### File / Gallery

| Operator | Description | Example |
|---|---|---|
| `exists` / `not_exists` | Has/doesn't have file(s) | `{ exists: true }` |

---

## Meta Filters

Filter by record metadata:

```ts
const records = await client.items.list({
  filter: {
    type: "blog_post",
    fields: {
      _status: { eq: "published" },          // "draft", "updated", "published"
      _created_at: { gt: "2024-01-01" },
      _updated_at: { gt: "2024-06-01" },
      _published_at: { gt: "2024-01-01" },
      _is_valid: { eq: true },               // Only valid records
    },
  },
});
```

| Meta field | Operators | Values |
|---|---|---|
| `_status` | `eq`, `neq` | `"draft"`, `"updated"`, `"published"` |
| `_created_at` | `eq`, `lt`, `lte`, `gt`, `gte` | ISO 8601 datetime string |
| `_updated_at` | `eq`, `lt`, `lte`, `gt`, `gte` | ISO 8601 datetime string |
| `_published_at` | `eq`, `lt`, `lte`, `gt`, `gte`, `exists`, `not_exists` | ISO 8601 datetime string |
| `_is_valid` | `eq` | `true`, `false` |
| `_first_published_at` | `eq`, `lt`, `lte`, `gt`, `gte`, `exists`, `not_exists` | ISO 8601 datetime string |

### Filter Only Valid Records

```ts
const validRecords = await client.items.list({
  filter: {
    type: "blog_post",
    only_valid: "true",
  },
});
```

---

## Sorting

Sort records using `order_by`:

```ts
const records = await client.items.list({
  filter: { type: "blog_post" },
  order_by: "published_date_DESC",
});
```

### Sort Format

`order_by` accepts a string: `"field_api_key_DIRECTION"` where direction is `ASC` or `DESC`.

```ts
// Sort by a field
order_by: "title_ASC"
order_by: "published_date_DESC"
order_by: "position_ASC"

// Sort by meta fields
order_by: "_created_at_DESC"
order_by: "_updated_at_DESC"
order_by: "_published_at_DESC"
order_by: "_first_published_at_ASC"

// Sort by relevance (when using text search)
order_by: "_rank_DESC"
```

### Multiple Sort Fields

Pass a comma-separated string:

```ts
order_by: "published_date_DESC,title_ASC"
```

---

## Getting Total Count

To get just the count without fetching records, set `page.limit: 0`:

```ts
const response = await client.items.rawList({
  filter: { type: "blog_post" },
  page: { offset: 0, limit: 0 },
});

const totalCount = response.meta.total_count;
```

**Important:** Use `rawList()` (not `list()`) when you only need the count, because the simplified `list()` does not expose `meta.total_count` directly.

---

## Locale-Specific Filtering

Filter by locale when querying localized fields:

```ts
const records = await client.items.list({
  filter: {
    type: "blog_post",
    fields: {
      title: { matches: { pattern: "ciao" } },
    },
  },
  locale: "it",
});
```

---

## Complete Example: Advanced Querying

```ts
import { buildClient } from "@datocms/cma-client-node";

const client = buildClient({
  apiToken: process.env.DATOCMS_API_TOKEN!,
});

async function advancedQuery() {
  // Find all published blog posts from 2024, sorted by date
  let count = 0;

  for await (const post of client.items.listPagedIterator(
    {
      filter: {
        type: "blog_post",
        fields: {
          _status: { eq: "published" },
          published_date: { gte: "2024-01-01" },
        },
      },
      order_by: "published_date_DESC",
      nested: true,
    },
    { perPage: 100, concurrency: 3 },
  )) {
    count++;
    console.log(`${count}. ${post.title} (${post.published_date})`);
  }

  console.log(`Total: ${count} posts`);
}

advancedQuery().catch(console.error);
```
