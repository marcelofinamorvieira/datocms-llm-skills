# Structured Text and Block Tools

Covers DatoCMS structured text (DAST), embedded block and record-link nodes, and advanced block tooling such as `SchemaRepository`, traversal helpers, and `inspectItem()`.

## Quick Navigation

- [Structured Text (`structured_text`) Field](#structured-text-structured_text-field)
- [Text Nodes](#text-nodes)
- [Lists](#lists)
- [Code Blocks](#code-blocks)
- [Blockquote](#blockquote)
- [Thematic Break](#thematic-break)
- [Block Nodes (Embedded Blocks)](#block-nodes-embedded-blocks)
- [Inline Block Nodes](#inline-block-nodes)
- [Item Link Nodes](#item-link-nodes)
- [Inline Item Nodes](#inline-item-nodes)
- [Structured Text Embedded Content Types](#structured-text-embedded-content-types)
- [Complete Structured Text Example](#complete-structured-text-example)
- [`SchemaRepository`](#schemarepository)
- [Block Traversal Utilities](#block-traversal-utilities)
- [`inspectItem()`](#inspectitem)
- [Common Pitfalls](#common-pitfalls)

---

## Structured Text (`structured_text`) Field

Structured text fields use the DatoCMS Abstract Syntax Tree (DAST) format.

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

---

## Text Nodes

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

// Link
{
  type: "link",
  url: "https://example.com",
  children: [{ type: "span", value: "Click here" }],
}
```

---

## Lists

```ts
{
  type: "list",
  style: "bulleted",
  children: [
    {
      type: "listItem",
      children: [
        {
          type: "paragraph",
          children: [{ type: "span", value: "First item" }],
        },
      ],
    },
  ],
}
```

Ordered lists use `style: "numbered"`.

---

## Code Blocks

```ts
{
  type: "code",
  language: "typescript",
  code: "const x = 42;",
}
```

---

## Blockquote

```ts
{
  type: "blockquote",
  children: [
    {
      type: "paragraph",
      children: [{ type: "span", value: "A wise quote" }],
    },
  ],
}
```

---

## Thematic Break

```ts
{ type: "thematicBreak" }
```

---

## Block Nodes (Embedded Blocks)

Use `block` nodes for full-width embedded block records:

```ts
{
  type: "block",
  item: buildBlockRecord({
    item_type: { id: imageBlockId, type: "item_type" },
    image: {
      upload_id: "upload-id",
      alt: "Photo",
      title: null,
      custom_data: {},
      focal_point: null,
    },
    caption: "A beautiful photo",
  }),
}
```

---

## Inline Block Nodes

Use `inlineBlock` nodes for inline embedded block records:

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

---

## Item Link Nodes

Use `itemLink` when the text should link to an existing top-level record:

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

---

## Inline Item Nodes

Use `inlineItem` to reference an existing record inline:

```ts
{
  type: "paragraph",
  children: [
    { type: "span", value: "Written by " },
    { type: "inlineItem", item: "author-record-id" },
  ],
}
```

---

## Structured Text Embedded Content Types

| Node | `item` value | Position in tree | Use case |
|---|---|---|---|
| `block` | `buildBlockRecord({...})` | Root-level | Full-width embeds such as images, CTAs, or videos |
| `inlineBlock` | `buildBlockRecord({...})` | Inline inside text | Badges, tooltips, inline widgets |
| `itemLink` | `"record-id"` | Inline, wraps text | Hyperlink text to another record |
| `inlineItem` | `"record-id"` | Inline, self-closing | Inline preview or card of another record |

The important distinction is that `block` and `inlineBlock` create new inline block records, while `itemLink` and `inlineItem` reference existing top-level records.

---

## Complete Structured Text Example

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

## `SchemaRepository`

`SchemaRepository` caches schema lookups. Use it when you repeatedly inspect models or fields while traversing nested blocks.

```ts
import { SchemaRepository } from "@datocms/cma-client-node";

const schemaRepo = new SchemaRepository(client);

const allModels = await schemaRepo.getAllItemTypes();
const blogModel = await schemaRepo.getItemTypeByApiKey("blog_post");
const fields = await schemaRepo.getItemTypeFields(blogModel);

await schemaRepo.prefetchAllModelsAndFields();
```

### Key Methods

| Method | Returns |
|---|---|
| `getAllItemTypes()` | All models, including blocks |
| `getAllModels()` | Only regular models |
| `getAllBlockModels()` | Only block models |
| `getItemTypeByApiKey(apiKey)` | A model by `api_key` |
| `getItemTypeById(id)` | A model by ID |
| `getItemTypeFields(itemType)` | All fields for a model |
| `getItemTypeFieldsets(itemType)` | All fieldsets for a model |
| `prefetchAllModelsAndFields()` | Pre-cache all models and fields |

---

## Block Traversal Utilities

These helpers recursively inspect block-bearing field values. They require a `SchemaRepository` so nested block types can be resolved correctly.

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

await visitBlocksInNonLocalizedFieldValue(
  record.content,
  "rich_text",
  schemaRepo,
  (block, path) => console.log(block.item_type.id, path),
);

const ctaBlocks = await findAllBlocksInNonLocalizedFieldValue(
  record.content,
  "rich_text",
  schemaRepo,
  (block) => block.item_type.id === ctaBlockModelId,
);

const withoutCtas = await filterBlocksInNonLocalizedFieldValue(
  record.content,
  "rich_text",
  schemaRepo,
  (block) => block.item_type.id !== ctaBlockModelId,
);

const transformed = await mapBlocksInNonLocalizedFieldValue(
  record.content,
  "rich_text",
  schemaRepo,
  (block) => block.item_type.id === textBlockModelId
    ? { ...block, body: block.body.toUpperCase() }
    : block,
);

const blockCount = await reduceBlocksInNonLocalizedFieldValue(
  record.content,
  "rich_text",
  schemaRepo,
  (count) => count + 1,
  0,
);
```

`filter` and `map` accept an options object with `traversalDirection: "top-down" | "bottom-up"`.

If the field is localized, extract each locale's inner value first. See `references/localization.md` for locale utilities.

---

## `inspectItem()`

`inspectItem()` is a debugging helper that prints a record or block as a readable tree:

```ts
import { inspectItem } from "@datocms/cma-client-node";

const record = await client.items.find("record-id", { nested: true });
console.log(inspectItem(record));
```

You can pass options such as `maxWidth` to control formatting.

---

## Common Pitfalls

### Invalid DAST Tree Structure

DAST has strict parent-child rules:

- Valid `root` children: `paragraph`, `heading`, `list`, `blockquote`, `code`, `thematicBreak`, `block`
- Valid `paragraph` and `heading` children: `span`, `link`, `itemLink`, `inlineItem`, `inlineBlock`

```ts
// Invalid: block inside paragraph
{ type: "paragraph", children: [{ type: "block", item: ... }] }

// Valid: block at root level
{
  type: "root",
  children: [
    { type: "paragraph", children: [{ type: "span", value: "Text" }] },
    { type: "block", item: buildBlockRecord({...}) },
  ],
}
```

### Forgetting `nested: true` for Structured Text Embeds

If you read structured text with embedded blocks without `nested: true`, `block` and `inlineBlock` nodes contain string IDs instead of inline block objects.

### Confusing Block Nodes with Record-Link Nodes

`block` and `inlineBlock` embed new block records. `itemLink` and `inlineItem` reference existing top-level records by string ID. Mixing those up produces API errors.
