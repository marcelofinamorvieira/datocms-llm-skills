# Schema: Models, Fields, and Fieldsets

Models (item types) define the content structure. Fields define the attributes of each model. Fieldsets group fields visually.

---

## Creating Models

```ts
const model = await client.itemTypes.create({
  name: "Blog Post",
  api_key: "blog_post",
});
```

### All Model Attributes

| Attribute | Type | Default | Description |
|---|---|---|---|
| `name` | `string` | **required** | Display name |
| `api_key` | `string` | **required** | Unique identifier (snake_case) |
| `singleton` | `boolean` | `false` | Single-instance model (e.g., homepage) |
| `modular_block` | `boolean` | `false` | Block model for modular content |
| `sortable` | `boolean` | `false` | Enable drag-and-drop record ordering |
| `tree` | `boolean` | `false` | Organize records in a tree hierarchy |
| `draft_mode_active` | `boolean` | `false` | Enable draft/published workflow |
| `all_locales_required` | `boolean` | `true` | Require all locales for localized fields |
| `hint` | `string \| null` | `null` | Help text shown in the editor |
| `inverse_relationships_enabled` | `boolean` | `false` | Enable inverse relationships for this model |
| `draft_saving_active` | `boolean` | `false` | Enable draft saving |
| `collection_appearance` | `"compact" \| "table"` | `"table"` | Default collection view in the UI |
| `ordering_direction` | `"asc" \| "desc"` | — | Default sort direction |
| `ordering_meta` | `"created_at" \| "updated_at" \| "first_published_at" \| "published_at"` | — | Sort by meta field |

### Model Relationships

| Relationship | Type | Description |
|---|---|---|
| `ordering_field` | `{ id, type: "field" }` | Sort by a specific field |
| `title_field` | `{ id, type: "field" }` | Field used as SEO title fallback |
| `image_preview_field` | `{ id, type: "field" }` | Field used as SEO image fallback |
| `excerpt_field` | `{ id, type: "field" }` | Field used as SEO excerpt fallback |
| `presentation_title_field` | `{ id, type: "field" }` | Field used as record title in the UI |
| `presentation_image_field` | `{ id, type: "field" }` | Field used as record thumbnail in the UI |
| `workflow` | `{ id, type: "workflow" }` | Assign a workflow to this model |

These relationships are set after creating the model and its fields, since fields must exist first:

```ts
const model = await client.itemTypes.create({
  name: "Blog Post",
  api_key: "blog_post",
  draft_mode_active: true,
});

const titleField = await client.fields.create(model.id, {
  label: "Title",
  api_key: "title",
  field_type: "string",
  validators: { required: {} },
});

// Now set the title field
await client.itemTypes.update(model.id, {
  title_field: { id: titleField.id, type: "field" },
});
```

### Singleton Models

Singleton models have exactly one record instance (e.g., "Homepage", "Global Settings"):

```ts
const homepage = await client.itemTypes.create({
  name: "Homepage",
  api_key: "homepage",
  singleton: true,
});
```

---

## Block Models

Block models are used inside modular content (`rich_text`), single block (`single_block`), and structured text (`structured_text`) fields. They are created like regular models with `modular_block: true`:

```ts
const block = await client.itemTypes.create({
  name: "CTA Block",
  api_key: "cta_block",
  modular_block: true,
});
```

**Block model constraints:**
- Cannot have `sortable: true`
- Cannot have `tree: true`
- Cannot have `draft_mode_active: true`
- Cannot be `singleton: true`
- Records are not created independently — they exist inline within parent records

---

## Listing, Finding, and Deleting Models

```ts
// List all models (including block models)
const allModels = await client.itemTypes.list();

// Separate regular models from block models
const models = allModels.filter((m) => !m.modular_block);
const blockModels = allModels.filter((m) => m.modular_block);

// Find a model by ID
const model = await client.itemTypes.find("model-id");

// Find which models reference a given model
const referencingModels = await client.itemTypes.referencing("model-id");

// Duplicate a model (with all fields)
const duplicated = await client.itemTypes.duplicate("model-id");

// Delete a model
await client.itemTypes.destroy("model-id");
```

**Important:** Deleting a model also deletes all its records and fields. This is an async job — the client waits for completion automatically.

---

## Creating Fields

Fields are created on a model. The `field_type` determines the kind of content the field stores.

```ts
const field = await client.fields.create(model.id, {
  label: "Title",
  api_key: "title",
  field_type: "string",
  validators: { required: {} },
});
```

### All Field Types

| `field_type` | Description | Value format |
|---|---|---|
| `string` | Single-line text | `string` |
| `text` | Multi-line text / markdown | `string` |
| `boolean` | True/false toggle | `boolean` |
| `integer` | Whole number | `number` |
| `float` | Decimal number | `number` |
| `date` | Date only | `"YYYY-MM-DD"` |
| `date_time` | Date and time | ISO 8601 string |
| `color` | RGBA color | `{ red, green, blue, alpha }` |
| `json` | Arbitrary JSON | any JSON value |
| `slug` | URL slug | `string` |
| `lat_lon` | Geo coordinates | `{ latitude, longitude }` |
| `seo` | SEO meta tags | `{ title, description, image, twitter_card }` |
| `file` | Single upload/asset | `{ upload_id, alt, title, custom_data, focal_point }` |
| `gallery` | Multiple uploads | Array of file objects |
| `link` | Single record link | record ID string |
| `links` | Multiple record links | Array of record IDs |
| `video` | External video embed | `{ url, title, width, height, ... }` |
| `rich_text` | Modular content (blocks) | Array of block records |
| `single_block` | Single block | Block record object |
| `structured_text` | Structured text (DAST) | DAST document |

### Field Attributes

| Attribute | Type | Description |
|---|---|---|
| `label` | `string` | **Required.** Display label |
| `api_key` | `string` | **Required.** Unique key within the model (snake_case) |
| `field_type` | `string` | **Required.** One of the types above |
| `localized` | `boolean` | Whether the field is localized (default `false`) |
| `validators` | `object` | Validation rules (see below) |
| `appearance` | `object` | Editor appearance configuration |
| `default_value` | varies | Default value for new records. For localized fields, a locale-keyed object (e.g., `{ en: "default" }`) |
| `hint` | `string \| null` | Help text shown in the editor |
| `position` | `number` | Ordering index within the model |

---

## Validators

Validators enforce constraints on field values. They are specified as an object where keys are validator names and values are validator configurations.

### Common Validators

| Validator | Applies to | Configuration | Description |
|---|---|---|---|
| `required` | All fields | `{}` | Field must have a value |
| `unique` | string, slug, integer, float | `{}` | Value must be unique across records |
| `length` | string, text, json, structured_text | `{ min?: number, max?: number, eq?: number }` | Character/element count |
| `format` | string | `{ predefined_pattern?: string, custom_pattern?: string }` | Regex pattern matching |
| `number_range` | integer, float | `{ min?: number, max?: number }` | Numeric range |
| `date_range` | date | `{ min?: string, max?: string }` | Date range |
| `date_time_range` | date_time | `{ min?: string, max?: string }` | DateTime range |
| `enum` | string, integer, float | `{ values: string[] }` | Allowed values |
| `file_size` | file, gallery | `{ min_value?: number, max_value?: number, min_unit?: "B"\|"KB"\|"MB", max_unit?: "B"\|"KB"\|"MB" }` | File size limits |
| `image_dimensions` | file, gallery | `{ width_min_value?, width_max_value?, height_min_value?, height_max_value? }` | Image dimension constraints |
| `extension` | file, gallery | `{ extensions: string[] }` or `{ predefined_list: "image"\|"transformable_image"\|"video"\|"document" }` | Allowed file types |
| `image_aspect_ratio` | file, gallery | `{ min_ar_numerator?, min_ar_denominator?, eq_ar_numerator?, eq_ar_denominator?, max_ar_numerator?, max_ar_denominator? }` | Image aspect ratio constraints |
| `required_alt_title` | file, gallery | `{ title?: boolean, alt?: boolean }` | Require alt/title metadata |
| `required_seo_fields` | seo | `{ title?: boolean, description?: boolean, image?: boolean, twitter_card?: boolean }` | Require specific SEO sub-fields |
| `title_length` | seo | `{ min?: number, max?: number }` | SEO title character limits |
| `description_length` | seo | `{ min?: number, max?: number }` | SEO description character limits |
| `slug_format` | slug | `{ custom_pattern?: string, predefined_pattern?: "webpage_slug" }` | Slug format constraints |
| `sanitized_html` | text | `{ sanitize_before_validation: boolean }` | HTML sanitization |

### Relational Validators

| Validator | Applies to | Configuration |
|---|---|---|
| `item_item_type` | link | `{ on_publish_with_unpublished_references_strategy?: "fail" \| "publish_references", on_reference_unpublish_strategy?: "fail" \| "unpublish" \| "delete_references", on_reference_delete_strategy?: "fail" \| "delete_references" \| "set_to_null", item_types: string[] }` |
| `items_item_type` | links | Same as `item_item_type` above |
| `size` | links, gallery | `{ min?: number, max?: number, eq?: number, multiple_of?: number }` — controls collection size |
| `rich_text_blocks` | rich_text | `{ item_types: string[] }` |
| `single_block_blocks` | single_block | `{ item_types: string[] }` |
| `structured_text_blocks` | structured_text | `{ item_types: string[] }` |
| `structured_text_inline_blocks` | structured_text | `{ item_types: string[] }` |
| `structured_text_links` | structured_text | `{ on_publish_with_unpublished_references_strategy?: ..., on_reference_unpublish_strategy?: ..., on_reference_delete_strategy?: ..., item_types: string[] }` |

### Example: Creating a Link Field with Validators

```ts
await client.fields.create(model.id, {
  label: "Author",
  api_key: "author",
  field_type: "link",
  validators: {
    item_item_type: {
      item_types: [authorModelId],
      on_publish_with_unpublished_references_strategy: "fail",
      on_reference_unpublish_strategy: "fail",
      on_reference_delete_strategy: "set_to_null",
    },
  },
});
```

### Example: Creating a Structured Text Field

```ts
await client.fields.create(model.id, {
  label: "Content",
  api_key: "content",
  field_type: "structured_text",
  validators: {
    structured_text_blocks: {
      item_types: [ctaBlockId, imageBlockId],
    },
    structured_text_inline_blocks: {
      item_types: [badgeBlockId], // Block models allowed as inline blocks
    },
    structured_text_links: {
      item_types: [blogPostModelId, pageModelId],
      on_publish_with_unpublished_references_strategy: "fail",
      on_reference_unpublish_strategy: "fail",
      on_reference_delete_strategy: "fail",
    },
  },
});
```

**Note:** `structured_text_blocks` controls which block models can appear as root-level `block` nodes, `structured_text_inline_blocks` controls `inlineBlock` nodes inside paragraphs/headings, and `structured_text_links` controls which models can be linked via `itemLink`/`inlineItem` nodes.

---

## Field Appearances

The `appearance` attribute configures the editor widget for the field.

```ts
await client.fields.create(model.id, {
  label: "Body",
  api_key: "body",
  field_type: "text",
  appearance: {
    editor: "markdown",
    parameters: {
      toolbar: ["heading", "bold", "italic", "code", "unordered_list", "ordered_list", "link"],
    },
    addons: [],
  },
});
```

Each field type has a default editor. Common built-in editors:

| Field type | Editors |
|---|---|
| `string` | `"single_line"`, `"string_select"`, `"string_radio_group"` |
| `text` | `"markdown"`, `"wysiwyg"`, `"textarea"` |
| `boolean` | `"boolean"` |
| `integer` / `float` | `"integer"` / `"float"` |
| `date` / `date_time` | `"date_picker"` / `"date_time_picker"` |
| `file` | `"file"` |
| `gallery` | `"gallery"` |
| `link` | `"link_select"`, `"link_embed"` |
| `links` | `"links_select"`, `"links_embed"` |
| `structured_text` | `"structured_text"` |
| `rich_text` | `"rich_text"` |

---

## Listing, Finding, and Deleting Fields

```ts
// List all fields of a model
const fields = await client.fields.list(model.id);

// Find a specific field
const field = await client.fields.find("field-id");

// Find fields referencing a model
const referencingFields = await client.fields.referencing(model.id);

// Duplicate a field
const duplicated = await client.fields.duplicate("field-id");

// Update a field
await client.fields.update("field-id", {
  label: "New Label",
  validators: { required: {} },
});

// Delete a field
await client.fields.destroy("field-id");
```

**Important:** Creating, updating, and deleting fields are all async jobs — the client automatically waits for propagation.

---

## Fieldsets

Fieldsets group fields visually in the editor UI. They do not affect API behavior.

### Create a Fieldset

```ts
const fieldset = await client.fieldsets.create(model.id, {
  title: "SEO Settings",
  hint: "Configure search engine optimization",
  collapsible: true,
  start_collapsed: true,
});
```

### Assign a Field to a Fieldset

When creating or updating a field, set the `fieldset` relationship:

```ts
await client.fields.create(model.id, {
  label: "Meta Title",
  api_key: "meta_title",
  field_type: "string",
  fieldset: { id: fieldset.id, type: "fieldset" },
});
```

### List, Update, Delete Fieldsets

```ts
const fieldsets = await client.fieldsets.list(model.id);
await client.fieldsets.update("fieldset-id", { title: "Updated Title" });
await client.fieldsets.destroy("fieldset-id");
```

---

## Complete Example: Create a Blog Post Model with Fields

```ts
import { buildClient } from "@datocms/cma-client-node";

const client = buildClient({
  apiToken: process.env.DATOCMS_API_TOKEN!,
});

async function createBlogSchema() {
  // Create the model
  const model = await client.itemTypes.create({
    name: "Blog Post",
    api_key: "blog_post",
    draft_mode_active: true,
  });

  // Create fields
  const titleField = await client.fields.create(model.id, {
    label: "Title",
    api_key: "title",
    field_type: "string",
    validators: { required: {} },
  });

  await client.fields.create(model.id, {
    label: "Slug",
    api_key: "slug",
    field_type: "slug",
    validators: {
      required: {},
      unique: {},
      slug_title_field: { title_field_id: titleField.id },
    },
  });

  await client.fields.create(model.id, {
    label: "Published Date",
    api_key: "published_date",
    field_type: "date",
    validators: { required: {} },
  });

  await client.fields.create(model.id, {
    label: "Cover Image",
    api_key: "cover_image",
    field_type: "file",
    validators: { required: {} },
  });

  await client.fields.create(model.id, {
    label: "Excerpt",
    api_key: "excerpt",
    field_type: "text",
    validators: { required: {}, length: { max: 300 } },
    appearance: {
      editor: "textarea",
      parameters: {},
      addons: [],
    },
  });

  await client.fields.create(model.id, {
    label: "Content",
    api_key: "content",
    field_type: "structured_text",
    validators: {
      structured_text_blocks: { item_types: [] },
      structured_text_links: { item_types: [] },
    },
  });

  // Set title and excerpt fields on the model
  await client.itemTypes.update(model.id, {
    title_field: { id: titleField.id, type: "field" },
  });

  console.log("Blog Post model created:", model.id);
}

createBlogSchema().catch(console.error);
```
