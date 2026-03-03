# Blocks and Structured Text

Covers modular content (rich_text), single block, structured text (DAST), block record creation, and block traversal utilities.

---

## Block Records

Block records are content entries that live **inline** within a parent record's modular content, single block, or structured text field. They are instances of block models (`modular_block: true`).

Unlike top-level records, blocks:
- Are not published/unpublished independently
- Cannot be fetched individually via `client.items.find()`
- Must be created inline when creating/updating the parent record
- IDs are server-assigned (you cannot specify a custom ID for new blocks, unlike top-level records)

---

## `buildBlockRecord()`

**Always use `buildBlockRecord()` when creating block records for the simplified API.** It generates a unique ID and formats the block correctly.

```ts
import { buildBlockRecord } from "@datocms/cma-client-node";

const block = buildBlockRecord({
  item_type: { id: "block_model_id", type: "item_type" },
  heading: "My Section",
  body: "Content goes here...",
});
```

The result is a serialized object with the `item_type` relationship and all field values — ready to be used in a modular content or structured text field. The block's ID is assigned server-side when the parent record is saved.

### Updating an Existing Block

When updating a parent record's block field, include the existing block's `id` to update it in place (rather than creating a new block):

```ts
const updatedBlock = buildBlockRecord({
  id: existingBlock.id,
  item_type: { id: "block_model_id", type: "item_type" },
  heading: "Updated Heading",
  body: "Updated content",
});
```

---

## `duplicateBlockRecord()`

Clone an existing block (and all nested blocks) with new IDs:

```ts
import { duplicateBlockRecord, SchemaRepository } from "@datocms/cma-client-node";

const schemaRepo = new SchemaRepository(client);
const clonedBlock = await duplicateBlockRecord(existingBlock, schemaRepo);
```

This recursively processes all nested blocks, giving each a new unique ID.

---

## `generateId()`

Generate a unique ID. This is **not** needed when using `buildBlockRecord()` (IDs are server-assigned). It is only needed when constructing raw JSON:API block objects manually:

```ts
import { generateId } from "@datocms/cma-client-node";

const id = generateId(); // URL-safe base64 UUID v4
```

---

## Modular Content (`rich_text`) Field

A modular content field stores an array of block records:

```ts
import { buildBlockRecord } from "@datocms/cma-client-node";

await client.items.create({
  item_type: { id: modelId, type: "item_type" },
  content: [
    buildBlockRecord({
      item_type: { id: heroBlockId, type: "item_type" },
      heading: "Welcome",
      subheading: "To our site",
    }),
    buildBlockRecord({
      item_type: { id: textBlockId, type: "item_type" },
      body: "Some paragraph text...",
    }),
    buildBlockRecord({
      item_type: { id: ctaBlockId, type: "item_type" },
      label: "Get Started",
      url: "https://example.com",
    }),
  ],
});
```

### Reading Modular Content

Always use `nested: true` to get full block objects:

```ts
const record = await client.items.find("record-id", { nested: true });

// record.content is now an array of block objects
for (const block of record.content) {
  console.log(block.item_type.id, block.heading);
}
```

Without `nested: true`, `record.content` would be an array of block ID strings.

---

## Single Block (`single_block`) Field

A single block field stores exactly one block record (or `null`):

```ts
await client.items.create({
  item_type: { id: modelId, type: "item_type" },
  hero: buildBlockRecord({
    item_type: { id: heroBlockId, type: "item_type" },
    heading: "Hero Title",
    image: { upload_id: "upload-id", alt: "Hero", title: null, custom_data: {}, focal_point: null },
  }),
});
```

---

## Structured Text (`structured_text`) Field

Structured text fields use the DatoCMS Abstract Syntax Tree (DAST) format — a document tree with paragraphs, headings, lists, and embedded blocks/links.

### DAST Document Structure

```ts
{
  schema: "dast",
  document: {
    type: "root",
    children: [
      // Content nodes go here
    ],
  },
}
```

### Text Nodes

```ts
// Paragraph
{
  type: "paragraph",
  children: [{ type: "span", value: "Hello world" }],
}

// Heading (levels 1-6)
{
  type: "heading",
  level: 2,
  children: [{ type: "span", value: "Section Title" }],
}

// Span with marks (bold, italic, etc.)
{
  type: "span",
  marks: ["strong", "emphasis"],
  value: "Bold and italic text",
}

// Link (wraps span children)
{
  type: "link",
  url: "https://example.com",
  children: [{ type: "span", value: "Click here" }],
}
```

### Lists

```ts
// Unordered list
{
  type: "list",
  style: "bulleted",
  children: [
    {
      type: "listItem",
      children: [
        { type: "paragraph", children: [{ type: "span", value: "First item" }] },
      ],
    },
    {
      type: "listItem",
      children: [
        { type: "paragraph", children: [{ type: "span", value: "Second item" }] },
      ],
    },
  ],
}

// Ordered list
{
  type: "list",
  style: "numbered",
  children: [/* listItems */],
}
```

### Code Blocks

```ts
{
  type: "code",
  language: "typescript",
  code: "const x = 42;",
}
```

### Blockquote

```ts
{
  type: "blockquote",
  children: [
    { type: "paragraph", children: [{ type: "span", value: "A wise quote" }] },
  ],
}
```

### Thematic Break (Horizontal Rule)

```ts
{ type: "thematicBreak" }
```

### Block Nodes (Embedded Blocks)

Embed a block record within structured text:

```ts
{
  type: "block",
  item: buildBlockRecord({
    item_type: { id: imageBlockId, type: "item_type" },
    image: { upload_id: "upload-id", alt: "Photo", title: null, custom_data: {}, focal_point: null },
    caption: "A beautiful photo",
  }),
}
```

### Inline Block Nodes

Embed a block inline within a paragraph:

```ts
{
  type: "paragraph",
  children: [
    { type: "span", value: "Check out this " },
    {
      type: "inlineBlock",
      item: buildBlockRecord({
        item_type: { id: badgeBlockId, type: "item_type" },
        label: "NEW",
        color: "green",
      }),
    },
    { type: "span", value: " feature!" },
  ],
}
```

### Item Link Nodes

Link to another DatoCMS record within text:

```ts
{
  type: "paragraph",
  children: [
    { type: "span", value: "Read our " },
    {
      type: "itemLink",
      item: "linked-record-id",
      children: [{ type: "span", value: "blog post" }],
    },
    { type: "span", value: " for more details." },
  ],
}
```

### Inline Item Nodes

Embed a record reference inline (rendered by the frontend):

```ts
{
  type: "paragraph",
  children: [
    { type: "span", value: "Written by " },
    { type: "inlineItem", item: "author-record-id" },
  ],
}
```

### Structured Text Embedded Content Types

| Node | `item` value | Position in tree | Use case |
|---|---|---|---|
| `block` | `buildBlockRecord({...})` | Root-level (sibling of paragraphs) | Full-width embeds: images, CTAs, videos |
| `inlineBlock` | `buildBlockRecord({...})` | Inline (inside paragraph/heading) | Badges, tooltips, inline widgets |
| `itemLink` | `"record-id"` (string) | Inline (wraps span children) | Text hyperlinked to another record |
| `inlineItem` | `"record-id"` (string) | Inline (self-closing) | Inline preview/card of another record |

**Critical distinction:** `block`/`inlineBlock` create **new block records** using `buildBlockRecord()`. `itemLink`/`inlineItem` reference **existing top-level records** by string ID. Mixing these up causes API errors.

---

### Complete Structured Text Example

```ts
import { buildBlockRecord } from "@datocms/cma-client-node";

await client.items.create({
  item_type: { id: modelId, type: "item_type" },
  content: {
    schema: "dast",
    document: {
      type: "root",
      children: [
        {
          type: "heading",
          level: 1,
          children: [{ type: "span", value: "Welcome to Our Blog" }],
        },
        {
          type: "paragraph",
          children: [
            { type: "span", value: "This is an " },
            { type: "span", marks: ["strong"], value: "important" },
            { type: "span", value: " announcement." },
          ],
        },
        {
          type: "block",
          item: buildBlockRecord({
            item_type: { id: imageBlockId, type: "item_type" },
            image: {
              upload_id: "upload-id",
              alt: "Banner",
              title: null,
              custom_data: {},
              focal_point: null,
            },
          }),
        },
        {
          type: "paragraph",
          children: [
            { type: "span", value: "Check out our " },
            {
              type: "itemLink",
              item: "about-page-id",
              children: [{ type: "span", value: "about page" }],
            },
            { type: "span", value: " for more info." },
          ],
        },
      ],
    },
  },
});
```

---

## Recursive Nesting: Blocks Within Blocks

Block models can have `rich_text`, `single_block`, or `structured_text` fields — which themselves contain more blocks. Nesting is allowed up to **5 levels deep** (a technical limit enforced by the API) and is the most complex part of the DatoCMS API.

**Example:** A "Section" block whose `rich_text` field contains more blocks:

```ts
await client.items.create({
  item_type: { id: pageModelId, type: "item_type" },
  sections: [
    buildBlockRecord({
      item_type: { id: sectionBlockId, type: "item_type" },
      title: "Features",
      // This block's rich_text field contains MORE blocks:
      content: [
        buildBlockRecord({
          item_type: { id: textBlockId, type: "item_type" },
          body: "Our top features...",
        }),
        buildBlockRecord({
          item_type: { id: ctaBlockId, type: "item_type" },
          label: "Try free",
          url: "/signup",
        }),
      ],
    }),
  ],
});
```

The same pattern applies when a block has a `structured_text` field — its DAST `block`/`inlineBlock` nodes use `buildBlockRecord()`, and those inner blocks can themselves have block-bearing fields, continuing the recursion.

**Every `buildBlockRecord()` at every nesting depth is required.** Each block needs its own `item_type`. Block IDs are assigned server-side.

---

## `SchemaRepository`

A caching layer for schema lookups. Use it when performing operations that need model/field information repeatedly:

```ts
import { SchemaRepository } from "@datocms/cma-client-node";

const schemaRepo = new SchemaRepository(client);

// These are cached after the first call
const allModels = await schemaRepo.getAllItemTypes();
const blogModel = await schemaRepo.getItemTypeByApiKey("blog_post");
const fields = await schemaRepo.getItemTypeFields(blogModel);

// Filter by kind
const regularModels = await schemaRepo.getAllModels();
const blockModels = await schemaRepo.getAllBlockModels();

// Pre-fetch all models and fields for best performance in batch operations
await schemaRepo.prefetchAllModelsAndFields();
```

### Key Methods

| Method | Returns |
|---|---|
| `getAllItemTypes()` | All models (including blocks) |
| `getAllModels()` | Only regular models |
| `getAllBlockModels()` | Only block models |
| `getItemTypeByApiKey(apiKey)` | Single model by api_key |
| `getItemTypeById(id)` | Single model by ID |
| `getItemTypeFields(itemType)` | All fields for a model |
| `getItemTypeFieldsets(itemType)` | All fieldsets for a model |
| `prefetchAllModelsAndFields()` | Pre-cache all models and fields |

---

## Block Traversal Utilities

These async utilities recursively traverse blocks in field values. They require a `SchemaRepository` for resolving nested block types. All are imported from the same package as `buildClient`.

All traversal functions share the same signature pattern: `(fieldValue, fieldType, schemaRepo, callback)`.

```ts
import {
  visitBlocksInNonLocalizedFieldValue,
  findAllBlocksInNonLocalizedFieldValue,
  filterBlocksInNonLocalizedFieldValue,
  mapBlocksInNonLocalizedFieldValue,
  reduceBlocksInNonLocalizedFieldValue,
  SchemaRepository,
} from "@datocms/cma-client-node";

const schemaRepo = new SchemaRepository(client);

// Visit every block
await visitBlocksInNonLocalizedFieldValue(
  record.content, "rich_text", schemaRepo,
  (block, path) => console.log(block.item_type.id, path),
);

// Find blocks matching a predicate → returns { item, path }[]
const ctaBlocks = await findAllBlocksInNonLocalizedFieldValue(
  record.content, "rich_text", schemaRepo,
  (block) => block.item_type.id === ctaBlockModelId,
);

// Filter out blocks (returns modified field value)
const withoutCtas = await filterBlocksInNonLocalizedFieldValue(
  record.content, "rich_text", schemaRepo,
  (block) => block.item_type.id !== ctaBlockModelId,
);

// Transform blocks (returns modified field value)
const transformed = await mapBlocksInNonLocalizedFieldValue(
  record.content, "rich_text", schemaRepo,
  (block) => block.item_type.id === textBlockModelId
    ? { ...block, body: block.body.toUpperCase() }
    : block,
);

// Reduce blocks to a value
const blockCount = await reduceBlocksInNonLocalizedFieldValue(
  record.content, "rich_text", schemaRepo,
  (count) => count + 1, 0,
);
```

`filter` and `map` accept an options object with `traversalDirection: "top-down" | "bottom-up"` (default: `"top-down"`).

The `path` parameter in callbacks is a `readonly (string | number)[]` tracking the block's position in the tree (e.g., `["content", 2, "nested_blocks", 0]`).

---

## `inspectItem()`

Debug utility that formats a record/block as a human-readable tree:

```ts
import { inspectItem } from "@datocms/cma-client-node";

const record = await client.items.find("record-id", { nested: true });
console.log(inspectItem(record));
```

Output is a formatted tree showing all field values, nested blocks, and structured text nodes. Useful for debugging complex content structures.

Options:

```ts
inspectItem(record, { maxWidth: 120 }); // Control line width
```

---

## Working with Localized Block Fields

When a block-containing field is localized, the outer value is a locale object, and the inner value is the block array/object:

```ts
await client.items.create({
  item_type: { id: modelId, type: "item_type" },
  content: {
    en: [
      buildBlockRecord({
        item_type: { id: textBlockId, type: "item_type" },
        body: "English content",
      }),
    ],
    it: [
      buildBlockRecord({
        item_type: { id: textBlockId, type: "item_type" },
        body: "Contenuto italiano",
      }),
    ],
  },
});
```

**Important:** The block traversal utilities (`visitBlocksInNonLocalizedFieldValue`, etc.) work on **non-localized** field values. For localized fields, extract each locale's value first, then pass it to the utility. Use the normalized field value utilities from `references/localization.md` to handle this uniformly.

---

## Common Pitfalls

**1. Forgetting `nested: true` when reading blocks**

Without it, block-bearing fields return **string IDs** instead of full objects:

```ts
// ❌ record.content → ["block-id-1", "block-id-2"] — just strings!
const record = await client.items.find("record-id");

// ✅ record.content → [{ id: "...", item_type: {...}, heading: "..." }, ...]
const record = await client.items.find("record-id", { nested: true });
```

This also applies to `listPagedIterator()` — pass `nested: true` in the query params. For structured text, without `nested: true` the DAST `block`/`inlineBlock` nodes contain string IDs instead of full block objects.

**2. Invalid DAST tree structure**

DAST has strict parent-child rules:

- Valid `root` children: `paragraph`, `heading`, `list`, `blockquote`, `code`, `thematicBreak`, `block`
- Valid `paragraph`/`heading` children: `span`, `link`, `itemLink`, `inlineItem`, `inlineBlock`

```ts
// ❌ block inside paragraph — invalid
{ type: "paragraph", children: [{ type: "block", item: ... }] }

// ✅ block at root level (sibling of paragraphs)
{ type: "root", children: [
  { type: "paragraph", children: [{ type: "span", value: "Text" }] },
  { type: "block", item: buildBlockRecord({...}) },
] }

// ❌ span directly under root — invalid
{ type: "root", children: [{ type: "span", value: "Text" }] }

// ✅ span inside paragraph
{ type: "root", children: [
  { type: "paragraph", children: [{ type: "span", value: "Text" }] },
] }
```

**3. Sending partial block arrays on update**

When updating a record's block-bearing field, you must send the **complete** field value — all blocks, not just the changed ones. There is no partial block update:

```ts
const record = await client.items.find("record-id", { nested: true });

// Modify one block, preserve others — send the full array
const updatedContent = record.content.map((block) =>
  block.item_type.id === ctaBlockId
    ? buildBlockRecord({ ...block, label: "New Label" })
    : buildBlockRecord(block),
);

await client.items.update("record-id", { content: updatedContent });
```

**4. Confusing block nodes vs record-link nodes in structured text**

`block`/`inlineBlock` embed **new block records** (`item` = `buildBlockRecord()`). `itemLink`/`inlineItem` reference **existing top-level records** (`item` = string ID). Using a string ID where a block record is expected (or vice versa) causes API errors.
