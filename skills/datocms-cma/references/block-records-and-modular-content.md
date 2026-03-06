# Block Records and Modular Content

Covers block record creation, modular content (`rich_text`), single-block fields, nested block payloads, and the most common pitfalls when updating block-bearing fields.

## Quick Navigation

- [Block Records](#block-records)
- [`buildBlockRecord()`](#buildblockrecord)
- [`duplicateBlockRecord()`](#duplicateblockrecord)
- [`generateId()`](#generateid)
- [Modular Content (`rich_text`) Field](#modular-content-rich_text-field)
- [Single Block (`single_block`) Field](#single-block-single_block-field)
- [Recursive Nesting: Blocks Within Blocks](#recursive-nesting-blocks-within-blocks)
- [Working with Localized Block Fields](#working-with-localized-block-fields)
- [Common Pitfalls](#common-pitfalls)

---

## Block Records

Block records are content entries that live inline within a parent record's modular content, single-block, or structured text field. They are instances of block models (`modular_block: true`).

Unlike top-level records, blocks:

- Are not published or unpublished independently
- Cannot be fetched individually via `client.items.find()`
- Must be created inline when creating or updating the parent record
- Receive their IDs from the server unless you are updating an existing block in place

---

## `buildBlockRecord()`

Prefer `buildBlockRecord()` when creating block records for the simplified API. It serializes the block body into the shape expected by DatoCMS.

```ts
import { buildBlockRecord } from "@datocms/cma-client-node";

const block = buildBlockRecord({
  item_type: { id: "block_model_id", type: "item_type" },
  heading: "My Section",
  body: "Content goes here...",
});
```

The returned object is ready to use in modular content, single-block, or structured text payloads.

### Updating an Existing Block

When updating a parent record's block field, include the existing block's `id` to update that block in place instead of creating a new one:

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

Clone an existing block, including nested blocks, with fresh IDs:

```ts
import { duplicateBlockRecord, SchemaRepository } from "@datocms/cma-client-node";

const schemaRepo = new SchemaRepository(client);
const clonedBlock = await duplicateBlockRecord(existingBlock, schemaRepo);
```

Use this when you need a deep copy of a block subtree instead of mutating the original.

---

## `generateId()`

Use `generateId()` only when you intentionally build raw JSON:API block objects yourself. It is not needed when using `buildBlockRecord()`.

```ts
import { generateId } from "@datocms/cma-client-node";

const id = generateId();
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

Pass `nested: true` when you need the full block objects back:

```ts
const record = await client.items.find("record-id", { nested: true });

for (const block of record.content) {
  console.log(block.item_type.id, block.heading);
}
```

Without `nested: true`, `record.content` is an array of block ID strings.

---

## Single Block (`single_block`) Field

A single-block field stores exactly one block record or `null`:

```ts
await client.items.create({
  item_type: { id: modelId, type: "item_type" },
  hero: buildBlockRecord({
    item_type: { id: heroBlockId, type: "item_type" },
    heading: "Hero Title",
    image: {
      upload_id: "upload-id",
      alt: "Hero",
      title: null,
      custom_data: {},
      focal_point: null,
    },
  }),
});
```

The same `nested: true` rule applies when reading single-block fields back from the API.

---

## Recursive Nesting: Blocks Within Blocks

Block models can themselves contain `rich_text`, `single_block`, or `structured_text` fields. Nesting is allowed up to 5 levels deep.

```ts
await client.items.create({
  item_type: { id: pageModelId, type: "item_type" },
  sections: [
    buildBlockRecord({
      item_type: { id: sectionBlockId, type: "item_type" },
      title: "Features",
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

Every nested block still needs its own `item_type`. When the nested field is structured text, its `block` and `inlineBlock` nodes also use `buildBlockRecord()`.

---

## Working with Localized Block Fields

When a block-bearing field is localized, the outer value is a locale object and the inner value is the block array or block object:

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

For the locale-object conventions and helper utilities, see `references/localization.md`.

---

## Common Pitfalls

### Forgetting `nested: true`

Without `nested: true`, block-bearing fields return strings instead of inline block objects:

```ts
const record = await client.items.find("record-id");
// record.content -> ["block-id-1", "block-id-2"]

const nestedRecord = await client.items.find("record-id", { nested: true });
// nestedRecord.content -> [{ id: "...", item_type: {...}, ... }, ...]
```

This also applies to `listPagedIterator()` query params when you need inline block data.

### Sending Partial Block Arrays on Update

When updating a record's block-bearing field, send the complete field value. There is no partial block patching.

```ts
const record = await client.items.find("record-id", { nested: true });

const updatedContent = record.content.map((block) =>
  block.item_type.id === ctaBlockId
    ? buildBlockRecord({ ...block, label: "New Label" })
    : buildBlockRecord(block),
);

await client.items.update("record-id", { content: updatedContent });
```

### Mixing Block Utilities with Raw Record Links

`buildBlockRecord()` creates new inline block records. If you need top-level record references inside structured text, use `itemLink` or `inlineItem` nodes instead. See `references/structured-text-and-block-tools.md`.
