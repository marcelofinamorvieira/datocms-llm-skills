# Dashboard and Schema Menu Items

Covers managing sidebar navigation in DatoCMS: dashboard menu items control the content editor sidebar, while schema menu items organize how models appear in the schema editor.

## Quick Navigation

- [Dashboard Menu Items Overview](#dashboard-menu-items-overview)
- [Creating a Dashboard Menu Item](#creating-a-dashboard-menu-item)
- [Creating Nested Menu Structures](#creating-nested-menu-structures)
- [Listing and Reordering Dashboard Menu Items](#listing-and-reordering-dashboard-menu-items)
- [Updating a Dashboard Menu Item](#updating-a-dashboard-menu-item)
- [Deleting a Dashboard Menu Item](#deleting-a-dashboard-menu-item)
- [Schema Menu Items Overview](#schema-menu-items-overview)
- [Creating a Schema Menu Item](#creating-a-schema-menu-item)
- [Listing and Organizing Schema Menu Items](#listing-and-organizing-schema-menu-items)
- [Updating a Schema Menu Item](#updating-a-schema-menu-item)
- [Deleting a Schema Menu Item](#deleting-a-schema-menu-item)
- [Complete Example](#complete-example-organize-dashboard-navigation)

---

## Dashboard Menu Items Overview

Dashboard menu items define the sidebar navigation in the DatoCMS content editor. Each menu item can link to a model (item type) or an external URL. Menu items support nesting via a parent reference, allowing you to create grouped folder structures.

### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `label` | `string` | Display label in the sidebar |
| `position` | `number` | Sort order among sibling items |
| `external_url` | `string \| null` | URL for external link items |
| `open_in_new_tab` | `boolean` | Whether external links open in a new tab |
| `item_type` | `{ id: string; type: "item_type" } \| null` | Model this menu item links to |
| `parent` | `{ id: string; type: "menu_item" } \| null` | Parent menu item for nesting |

**Important:** A menu item must reference either an `item_type` or an `external_url`, but not both. A parent folder item typically has neither.

---

## Creating a Dashboard Menu Item

Link a menu item to an existing model:

```ts
const blogMenuItem = await client.menuItems.create({
  label: "Blog Posts",
  position: 1,
  item_type: {
    id: blogModelId,
    type: "item_type",
  },
});

console.log("Created menu item:", blogMenuItem.id, blogMenuItem.label);
```

Create a menu item that links to an external URL:

```ts
const externalMenuItem = await client.menuItems.create({
  label: "Analytics Dashboard",
  position: 2,
  external_url: "https://analytics.example.com",
  open_in_new_tab: true,
});
```

---

## Creating Nested Menu Structures

Create a parent folder, then add child items beneath it:

```ts
const parentFolder = await client.menuItems.create({
  label: "Content",
  position: 1,
});

const blogChild = await client.menuItems.create({
  label: "Blog Posts",
  position: 1,
  item_type: {
    id: blogModelId,
    type: "item_type",
  },
  parent: {
    id: parentFolder.id,
    type: "menu_item",
  },
});

const authorChild = await client.menuItems.create({
  label: "Authors",
  position: 2,
  item_type: {
    id: authorModelId,
    type: "item_type",
  },
  parent: {
    id: parentFolder.id,
    type: "menu_item",
  },
});
```

**Important:** Child items use `position` to define their order within the parent folder.

---

## Listing and Reordering Dashboard Menu Items

```ts
const allMenuItems = await client.menuItems.list();

for (const menuItem of allMenuItems) {
  const parentLabel = menuItem.parent ? `(child of ${menuItem.parent.id})` : "(top-level)";
  console.log(menuItem.id, menuItem.label, parentLabel);
}
```

### Reordering Items

Update the `position` attribute to change sort order:

```ts
await client.menuItems.update(menuItemId, {
  position: 5,
});
```

---

## Updating a Dashboard Menu Item

```ts
const updatedMenuItem = await client.menuItems.update(menuItemId, {
  label: "All Blog Posts",
  position: 3,
});

console.log("Updated:", updatedMenuItem.label);
```

### Moving an Item Into a Folder

```ts
await client.menuItems.update(menuItemId, {
  parent: {
    id: parentFolderId,
    type: "menu_item",
  },
  position: 1,
});
```

### Moving an Item to the Top Level

```ts
await client.menuItems.update(menuItemId, {
  parent: null,
  position: 1,
});
```

---

## Deleting a Dashboard Menu Item

```ts
await client.menuItems.destroy(menuItemId);
```

**Important:** Deleting a parent folder does not automatically delete its children. Remove or reassign child items first.

---

## Finding a Dashboard Menu Item

```ts
const menuItem = await client.menuItems.find(menuItemId);
console.log(menuItem.label, menuItem.position);
```

---

## Schema Menu Items Overview

Schema menu items control how models are organized in the schema editor sidebar. Like dashboard menu items, they support nesting via a parent reference, allowing you to group related models into folders.

### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `label` | `string` | Display label in the schema sidebar |
| `position` | `number` | Sort order among sibling items |
| `kind` | `string` | Item kind |
| `item_type` | `{ id: string; type: "item_type" } \| null` | Model this schema menu item references |
| `parent` | `{ id: string; type: "schema_menu_item" } \| null` | Parent schema menu item for nesting |

---

## Creating a Schema Menu Item

```ts
const schemaMenuItem = await client.schemaMenuItems.create({
  label: "Blog Models",
  position: 1,
});

console.log("Created schema menu item:", schemaMenuItem.id);
```

Create a schema menu item linked to a model:

```ts
const blogSchemaItem = await client.schemaMenuItems.create({
  label: "Blog Post",
  position: 1,
  item_type: {
    id: blogModelId,
    type: "item_type",
  },
  parent: {
    id: schemaFolderId,
    type: "schema_menu_item",
  },
});
```

---

## Listing and Organizing Schema Menu Items

```ts
const allSchemaMenuItems = await client.schemaMenuItems.list();

const topLevelItems = allSchemaMenuItems.filter((item) => !item.parent);
const nestedItems = allSchemaMenuItems.filter((item) => item.parent);

console.log("Top-level schema items:", topLevelItems.length);
console.log("Nested schema items:", nestedItems.length);
```

---

## Updating a Schema Menu Item

```ts
const updatedSchemaItem = await client.schemaMenuItems.update(schemaMenuItemId, {
  label: "Blog & News Models",
  position: 2,
});

console.log("Updated:", updatedSchemaItem.label);
```

---

## Deleting a Schema Menu Item

```ts
await client.schemaMenuItems.destroy(schemaMenuItemId);
```

---

## Finding a Schema Menu Item

```ts
const schemaMenuItem = await client.schemaMenuItems.find(schemaMenuItemId);
console.log(schemaMenuItem.label, schemaMenuItem.position);
```

---

## Type Reference

```ts
import type {
  MenuItem,
  MenuItemCreateSchema,
  MenuItemUpdateSchema,
  MenuItemInstancesHrefSchema,
  SchemaMenuItem,
  SchemaMenuItemCreateSchema,
  SchemaMenuItemUpdateSchema,
  SchemaMenuItemInstancesHrefSchema,
} from "@datocms/cma-client";
```

> **Note:** These types are auto-generated from the DatoCMS CMA API schema. Field optionality and exact shapes may change between client versions. Always refer to the installed version's types as the source of truth.

### MenuItem (response)

Returned by `client.menuItems.create()`, `update()`, `find()`, and each element in `list()`.

| Field | Type | Description |
|-------|------|-------------|
| `id` | `string` | UUID of the menu item |
| `type` | `"menu_item"` | JSON API type |
| `label` | `string` | Display label in the sidebar |
| `external_url` | `null \| string` | URL for external link items |
| `position` | `number` | Ordering index |
| `open_in_new_tab` | `boolean` | Whether external links open in a new tab |
| `item_type` | `ItemTypeData \| null` | `{ type: "item_type"; id: string }` — model this item links to |
| `item_type_filter` | `ItemTypeFilterData \| null` | `{ type: "item_type_filter"; id: string }` — saved filter reference |
| `parent` | `null \| MenuItemData` | `{ type: "menu_item"; id: string }` — parent menu item for nesting |
| `children` | `MenuItemData[]` | `{ type: "menu_item"; id: string }[]` — child menu item references |

### MenuItemCreateSchema (input for `create`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `string` | no | Optional client-side UUID |
| `type` | `"menu_item"` | no | JSON API type |
| `label` | `string` | **yes** | Display label in the sidebar |
| `external_url` | `null \| string` | no | URL for external link items |
| `position` | `number` | no | Ordering index |
| `open_in_new_tab` | `boolean` | no | Whether external links open in a new tab |
| `item_type` | `ItemTypeData \| null` | no | Model this item links to |
| `item_type_filter` | `ItemTypeFilterData \| null` | no | Saved filter reference |
| `parent` | `null \| MenuItemData` | no | Parent menu item for nesting |

### MenuItemUpdateSchema (input for `update`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `string` | no | UUID of the menu item |
| `type` | `"menu_item"` | no | JSON API type |
| `label` | `string` | no | Display label in the sidebar |
| `external_url` | `null \| string` | no | URL for external link items |
| `position` | `number` | no | Ordering index |
| `open_in_new_tab` | `boolean` | no | Whether external links open in a new tab |
| `item_type` | `ItemTypeData \| null` | no | Model this item links to |
| `item_type_filter` | `ItemTypeFilterData \| null` | no | Saved filter reference |
| `parent` | `null \| MenuItemData` | no | Parent menu item for nesting |

### MenuItemInstancesHrefSchema (query parameters for `list`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `filter` | `{ ids: string }` | no | IDs to fetch, comma separated |

### SchemaMenuItem (response)

Returned by `client.schemaMenuItems.create()`, `update()`, `find()`, and each element in `list()`.

| Field | Type | Description |
|-------|------|-------------|
| `id` | `string` | UUID of the schema menu item |
| `type` | `"schema_menu_item"` | JSON API type |
| `label` | `null \| string` | Display label (only present when the item is not linked to an item type) |
| `position` | `number` | Ordering index |
| `kind` | `"item_type" \| "modular_block"` | Whether this refers to an item type or a modular block |
| `item_type` | `ItemTypeData \| null` | `{ type: "item_type"; id: string }` — model this item references |
| `parent` | `null \| SchemaMenuItemData` | `{ type: "schema_menu_item"; id: string }` — parent for nesting |
| `children` | `SchemaMenuItemData[]` | `{ type: "schema_menu_item"; id: string }[]` — child references |

### SchemaMenuItemCreateSchema (input for `create`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `string` | no | Optional client-side UUID |
| `type` | `"schema_menu_item"` | no | JSON API type |
| `label` | `null \| string` | **yes** | Display label (null when linked to an item type) |
| `position` | `number` | no | Ordering index |
| `kind` | `"item_type" \| "modular_block"` | **yes** | Whether this refers to an item type or a modular block |
| `item_type` | `ItemTypeData \| null` | no | Model this item references |
| `parent` | `null \| SchemaMenuItemData` | no | Parent schema menu item for nesting |

### SchemaMenuItemUpdateSchema (input for `update`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `string` | no | UUID of the schema menu item |
| `type` | `"schema_menu_item"` | no | JSON API type |
| `label` | `null \| string` | no | Display label (null when linked to an item type) |
| `position` | `number` | no | Ordering index |
| `kind` | `"item_type" \| "modular_block"` | no | Whether this refers to an item type or a modular block |
| `item_type` | `ItemTypeData \| null` | no | Model this item references |
| `parent` | `null \| SchemaMenuItemData` | no | Parent schema menu item for nesting |
| `children` | `SchemaMenuItemData[]` | no | Child schema menu item references |

### SchemaMenuItemInstancesHrefSchema (query parameters for `list`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `filter` | `{ ids: string }` | no | IDs to fetch, comma separated |

---

## Complete Example: Organize Dashboard Navigation

```ts
import { buildClient, ApiError } from "@datocms/cma-client-node";

async function organizeDashboardNavigation() {
  const client = buildClient({
    apiToken: process.env.DATOCMS_API_TOKEN!,
  });

  // Step 1: Fetch existing models to link menu items to
  const allModels = await client.itemTypes.list();

  const blogModel = allModels.find((model) => model.api_key === "blog_post");
  const authorModel = allModels.find((model) => model.api_key === "author");

  if (!blogModel || !authorModel) {
    console.error("Required models (blog_post, author) not found.");
    process.exit(1);
  }

  // Step 2: Create a parent folder in the dashboard sidebar
  console.log("Creating dashboard menu folder...");

  const contentFolder = await client.menuItems.create({
    label: "Content",
    position: 1,
  });

  console.log("Created folder:", contentFolder.id, contentFolder.label);

  // Step 3: Add child menu items linking to models
  console.log("Adding child menu items...");

  const blogMenuItem = await client.menuItems.create({
    label: "Blog Posts",
    position: 1,
    item_type: {
      id: blogModel.id,
      type: "item_type",
    },
    parent: {
      id: contentFolder.id,
      type: "menu_item",
    },
  });

  console.log("Created child:", blogMenuItem.label);

  const authorMenuItem = await client.menuItems.create({
    label: "Authors",
    position: 2,
    item_type: {
      id: authorModel.id,
      type: "item_type",
    },
    parent: {
      id: contentFolder.id,
      type: "menu_item",
    },
  });

  console.log("Created child:", authorMenuItem.label);

  // Step 4: Add an external link at the top level
  const analyticsMenuItem = await client.menuItems.create({
    label: "Analytics",
    position: 2,
    external_url: "https://analytics.example.com",
    open_in_new_tab: true,
  });

  console.log("Created external link:", analyticsMenuItem.label);

  // Step 5: Reorder items — move Authors above Blog Posts
  console.log("\nReordering dashboard menu items...");

  await client.menuItems.update(authorMenuItem.id, {
    position: 1,
  });

  await client.menuItems.update(blogMenuItem.id, {
    position: 2,
  });

  console.log("Authors moved to position 1, Blog Posts to position 2");

  // Step 6: Update the folder label to be more descriptive
  const updatedFolder = await client.menuItems.update(contentFolder.id, {
    label: "Editorial Content",
  });

  console.log("Renamed folder to:", updatedFolder.label);

  // Step 7: List all dashboard menu items to verify structure
  const allMenuItems = await client.menuItems.list();

  console.log("\nDashboard menu structure:");

  const topLevelMenuItems = allMenuItems.filter((item) => !item.parent);
  const childMenuItems = allMenuItems.filter((item) => item.parent);

  for (const item of topLevelMenuItems) {
    const linkInfo = item.external_url
      ? `-> ${item.external_url}`
      : item.item_type
        ? `-> model ${item.item_type.id}`
        : "(folder)";
    console.log(`${item.position}. ${item.label} ${linkInfo}`);

    const children = childMenuItems
      .filter((child) => child.parent?.id === item.id)
      .sort((a, b) => a.position - b.position);

    for (const child of children) {
      const childLink = child.item_type
        ? `-> model ${child.item_type.id}`
        : `-> ${child.external_url}`;
      console.log(`  ${child.position}. ${child.label} ${childLink}`);
    }
  }

  // Step 8: Organize schema menu items into folders
  console.log("\nOrganizing schema menu items...");

  const blogSchemaFolder = await client.schemaMenuItems.create({
    label: "Blog Models",
    position: 1,
  });

  console.log("Created schema folder:", blogSchemaFolder.id, blogSchemaFolder.label);

  const blogSchemaItem = await client.schemaMenuItems.create({
    label: "Blog Post",
    position: 1,
    item_type: {
      id: blogModel.id,
      type: "item_type",
    },
    parent: {
      id: blogSchemaFolder.id,
      type: "schema_menu_item",
    },
  });

  console.log("Added to schema folder:", blogSchemaItem.label);

  const authorSchemaItem = await client.schemaMenuItems.create({
    label: "Author",
    position: 2,
    item_type: {
      id: authorModel.id,
      type: "item_type",
    },
    parent: {
      id: blogSchemaFolder.id,
      type: "schema_menu_item",
    },
  });

  console.log("Added to schema folder:", authorSchemaItem.label);

  // Step 9: Update a schema menu item label
  const renamedSchemaItem = await client.schemaMenuItems.update(blogSchemaItem.id, {
    label: "Blog Post Model",
  });

  console.log("Renamed schema item to:", renamedSchemaItem.label);

  // Step 10: List all schema menu items to verify structure
  const allSchemaItems = await client.schemaMenuItems.list();

  const topLevelSchemaItems = allSchemaItems.filter((item) => !item.parent);
  const nestedSchemaItems = allSchemaItems.filter((item) => item.parent);

  console.log("\nSchema menu structure:");

  for (const item of topLevelSchemaItems) {
    const modelInfo = item.item_type ? `-> model ${item.item_type.id}` : "(folder)";
    console.log(`${item.position}. ${item.label} ${modelInfo}`);

    const children = nestedSchemaItems
      .filter((child) => child.parent?.id === item.id)
      .sort((a, b) => a.position - b.position);

    for (const child of children) {
      const childModel = child.item_type ? `-> model ${child.item_type.id}` : "(folder)";
      console.log(`  ${child.position}. ${child.label} ${childModel}`);
    }
  }

  console.log("\nDashboard and schema navigation organized successfully!");
}

organizeDashboardNavigation().catch((error) => {
  if (error instanceof ApiError) {
    console.error("API error:", error.response.status, error.errors);
  } else {
    console.error(error);
  }
  process.exit(1);
});
```
