# Plugins

Covers programmatic management of plugins installed on a DatoCMS project: installing from the marketplace or custom URLs, listing, updating parameters, finding fields that use a plugin, and uninstalling. This does **not** cover building plugins (see the datocms-plugin-builder skill for that).

## Quick Navigation

- [Installing a Plugin](#installing-a-plugin)
- [Plugin Attributes](#plugin-attributes)
- [Listing Plugins](#listing-plugins)
- [Finding a Plugin](#finding-a-plugin)
- [Updating a Plugin](#updating-a-plugin)
- [Updating Plugin Parameters](#updating-plugin-parameters)
- [Finding Fields Using a Plugin](#finding-fields-using-a-plugin)
- [Deleting a Plugin](#deleting-a-plugin)
- [Complete Example: Audit and Configure Plugins](#complete-example-audit-and-configure-plugins)

---

## Installing a Plugin

Install a plugin from the DatoCMS marketplace by its package name:

```ts
const marketplacePlugin = await client.plugins.create({
  package_name: "datocms-plugin-tag-editor",
});

console.log("Installed:", marketplacePlugin.name, marketplacePlugin.id);
```

Install a custom or private plugin by providing its URL:

```ts
const customPlugin = await client.plugins.create({
  url: "https://my-plugin.example.com",
});

console.log("Installed custom plugin:", customPlugin.name, customPlugin.id);
```

**Important:** You must provide either `package_name` (for marketplace plugins) or `url` (for custom plugins), but not both.

---

## Plugin Attributes

| Attribute | Type | Description |
|---|---|---|
| `id` | `string` | Plugin ID |
| `package_name` | `string \| null` | Marketplace package name |
| `name` | `string` | Display name |
| `description` | `string \| null` | Plugin description |
| `url` | `string \| null` | Custom plugin URL |
| `plugin_type` | `string` | Plugin type |
| `field_types` | `string[]` | Field types this plugin can be used with |
| `parameter_definitions` | `object` | Plugin parameter schema |
| `parameters` | `object` | Instance-specific parameter values |
| `package_version` | `string \| null` | Installed version |
| `permissions` | `string[]` | Requested permissions |

---

## Listing Plugins

```ts
const allPlugins = await client.plugins.list();

for (const plugin of allPlugins) {
  const source = plugin.package_name ?? plugin.url ?? "unknown";
  console.log(`${plugin.name} (${plugin.id}) — source: ${source}`);
}
```

### Filtering by Type

```ts
const allPlugins = await client.plugins.list();

const marketplacePlugins = allPlugins.filter((p) => p.package_name !== null);
const customPlugins = allPlugins.filter((p) => p.url !== null);

console.log("Marketplace plugins:", marketplacePlugins.length);
console.log("Custom plugins:", customPlugins.length);
```

---

## Finding a Plugin

```ts
const plugin = await client.plugins.find("plugin-id");

console.log(plugin.name, plugin.package_version);
```

---

## Updating a Plugin

```ts
const updatedPlugin = await client.plugins.update("plugin-id", {
  parameters: { showAdvancedOptions: true },
});

console.log("Updated:", updatedPlugin.name);
```

---

## Updating Plugin Parameters

The `parameters` object stores project-specific configuration for the plugin. The shape of this object depends on the plugin's `parameter_definitions`.

```ts
const plugin = await client.plugins.find("plugin-id");

console.log("Current parameters:", JSON.stringify(plugin.parameters, null, 2));

const updatedPlugin = await client.plugins.update(plugin.id, {
  parameters: {
    ...plugin.parameters,
    apiEndpoint: "https://api.example.com/v2",
    maxResults: 50,
    enableCache: true,
  },
});

console.log("Updated parameters:", JSON.stringify(updatedPlugin.parameters, null, 2));
```

**Important:** Spread the existing `parameters` before adding new values to avoid accidentally removing other configuration keys.

---

## Finding Fields Using a Plugin

Retrieve all fields that are currently using a specific plugin. This is useful for auditing before uninstalling or reconfiguring a plugin.

```ts
const fieldsUsingPlugin = await client.plugins.fields("plugin-id");

for (const field of fieldsUsingPlugin) {
  console.log(`Field "${field.label}" (${field.api_key}) on model ${field.item_type.id}`);
}
```

### Checking If a Plugin Is Safe to Remove

```ts
const fieldsUsingPlugin = await client.plugins.fields("plugin-id");

const pluginIsInUse = fieldsUsingPlugin.length > 0;

if (pluginIsInUse) {
  console.log(`Cannot remove: ${fieldsUsingPlugin.length} field(s) still use this plugin.`);
  for (const field of fieldsUsingPlugin) {
    console.log(`  - ${field.label} (${field.api_key})`);
  }
} else {
  console.log("Plugin is not in use and can be safely removed.");
}
```

---

## Deleting a Plugin

```ts
await client.plugins.destroy("plugin-id");

console.log("Plugin uninstalled.");
```

**Important:** Deleting a plugin that is still assigned to fields will break those fields. Always check with `client.plugins.fields()` first.

---

## Type Reference

```ts
import type {
  Plugin,
  PluginCreateSchema,
  PluginUpdateSchema,
} from "@datocms/cma-client/dist/types/generated/ApiTypes";
```

> **Note:** These types are auto-generated from the DatoCMS CMA OpenAPI schema. Always refer to the installed package version for the most up-to-date definitions.

### `Plugin` (response type)

Returned by `client.plugins.create()`, `client.plugins.find()`, `client.plugins.update()`, `client.plugins.list()`, and `client.plugins.destroy()`.

| Field | Type | Description |
|---|---|---|
| `id` | `string` | Plugin ID |
| `type` | `"plugin"` | JSON API resource type |
| `name` | `string` | The name of the plugin |
| `description` | `null \| string` | A description of the plugin |
| `package_name` | `null \| string` | NPM package name of the plugin (or null if it's a private plugin) |
| `package_version` | `null \| string` | The installed version of the plugin (or null if it's a private plugin) |
| `url` | `string` | The entry point URL of the plugin |
| `parameters` | `{ [k: string]: unknown }` | Global plugin configuration. Plugins can persist whatever information they want in this object to reuse it later |
| `permissions` | `"currentUserAccessToken"[]` | Permissions granted to this plugin |
| `plugin_type` | `"field_editor" \| "sidebar" \| "field_addon" \| null` | The type of field extension a legacy plugin implements |
| `field_types` | `null \| ("boolean" \| "date" \| "date_time" \| "float" \| "integer" \| "string" \| "text" \| "lat_lon" \| "json" \| "seo" \| "link" \| "links" \| "video" \| "color" \| "slug" \| "rich_text" \| "file" \| "gallery")[]` | On which types of field in which a legacy plugin can be used |
| `parameter_definitions` | `null \| { global: unknown[]; instance: unknown[] }` | The schema for the parameters a legacy plugin can persist |
| `meta` | `{ version: string }` | Metadata. `version` indicates `"1"` for legacy plugins, `"2"` for new plugins |

### `PluginCreateSchema` (input for `client.plugins.create()`)

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | `string` | No | Plugin ID |
| `type` | `"plugin"` | No | JSON API resource type |
| `package_name` | `null \| string` | No | NPM package name of the public plugin you want to install. For public plugins, that's the only attribute you need to pass |
| `name` | `string` | No | The name of the plugin. Only to be passed if package name key is not specified |
| `description` | `null \| string` | No | A description of the plugin. Only to be passed if package name key is not specified |
| `url` | `string` | No | The entry point URL of the plugin. Only to be passed if package name key is not specified |
| `permissions` | `"currentUserAccessToken"[]` | No | Permissions granted to this plugin. Only to be passed if package name key is not specified |
| `plugin_type` | `"field_editor" \| "sidebar" \| "field_addon"` | No | The type of field extension this legacy plugin implements. Only to be passed if package name key is not specified |
| `field_types` | `("boolean" \| "date" \| "date_time" \| "float" \| "integer" \| "string" \| "text" \| "lat_lon" \| "json" \| "seo" \| "link" \| "links" \| "video" \| "color" \| "slug" \| "rich_text" \| "file" \| "gallery")[]` | No | On which types of field in which this legacy plugin can be used. Only to be passed if package name key is not specified |
| `parameter_definitions` | `{ global: unknown[]; instance: unknown[] }` | No | The schema for the parameters this legacy plugin can persist |
| `package_version` | `null \| string` | No | NPM version of the plugin |

### `PluginUpdateSchema` (input for `client.plugins.update()`)

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | `string` | No | Plugin ID |
| `type` | `"plugin"` | No | JSON API resource type |
| `name` | `string` | No | The name of the plugin |
| `description` | `null \| string` | No | A description of the plugin |
| `url` | `string` | No | The entry point URL of the plugin |
| `parameters` | `{ [k: string]: unknown }` | No | Global plugin configuration. Plugins can persist whatever information they want in this object to reuse it later |
| `package_version` | `null \| string` | No | The installed version of the plugin (or null if it's a private plugin) |
| `permissions` | `"currentUserAccessToken"[]` | No | Permissions granted to this plugin |
| `meta` | `{ [k: string]: unknown }` | No | Additional metadata |

---

## Complete Example: Audit and Configure Plugins

Lists all installed plugins, finds which fields use a specific plugin, and updates its parameters.

```ts
import { buildClient, ApiError } from "@datocms/cma-client-node";

async function auditAndConfigurePlugins() {
  const client = buildClient({
    apiToken: process.env.DATOCMS_API_TOKEN!,
  });

  // Step 1: List all installed plugins and categorize them
  const allPlugins = await client.plugins.list();

  const marketplacePlugins = allPlugins.filter((p) => p.package_name !== null);
  const customPlugins = allPlugins.filter((p) => p.url !== null);

  console.log(`Total plugins installed: ${allPlugins.length}`);
  console.log(`  Marketplace: ${marketplacePlugins.length}`);
  console.log(`  Custom: ${customPlugins.length}`);
  console.log("---");

  // Step 2: Print details for each plugin
  for (const plugin of allPlugins) {
    const source = plugin.package_name ?? plugin.url ?? "unknown";
    const version = plugin.package_version ? ` v${plugin.package_version}` : "";
    console.log(`${plugin.name}${version} (ID: ${plugin.id})`);
    console.log(`  Source: ${source}`);
    console.log(`  Type: ${plugin.plugin_type}`);
    console.log(`  Field types: ${plugin.field_types.join(", ") || "none"}`);
    console.log(`  Permissions: ${plugin.permissions.join(", ") || "none"}`);
  }

  console.log("---");

  // Step 3: Find a specific plugin by package name
  const targetPackageName = "datocms-plugin-tag-editor";

  const targetPlugin = allPlugins.find(
    (p) => p.package_name === targetPackageName,
  );

  if (!targetPlugin) {
    console.log(`Plugin "${targetPackageName}" is not installed. Installing...`);

    const installedPlugin = await client.plugins.create({
      package_name: targetPackageName,
    });

    console.log(`Installed "${installedPlugin.name}" (ID: ${installedPlugin.id})`);
    return;
  }

  console.log(`Found "${targetPlugin.name}" (ID: ${targetPlugin.id})`);

  // Step 4: Audit which fields use this plugin
  const fieldsUsingPlugin = await client.plugins.fields(targetPlugin.id);

  console.log(`Fields using this plugin: ${fieldsUsingPlugin.length}`);

  for (const field of fieldsUsingPlugin) {
    console.log(`  - "${field.label}" (${field.api_key}) on model ${field.item_type.id}`);
  }

  // Step 5: Update the plugin's project-level parameters
  console.log("---");
  console.log("Current parameters:", JSON.stringify(targetPlugin.parameters, null, 2));

  const updatedPlugin = await client.plugins.update(targetPlugin.id, {
    parameters: {
      ...targetPlugin.parameters,
      autoSuggest: true,
      maxTags: 25,
    },
  });

  console.log("Updated parameters:", JSON.stringify(updatedPlugin.parameters, null, 2));

  // Step 6: Remove unused custom plugins
  console.log("---");
  console.log("Checking for unused custom plugins...");

  for (const customPlugin of customPlugins) {
    const fieldsUsing = await client.plugins.fields(customPlugin.id);

    if (fieldsUsing.length === 0) {
      console.log(`"${customPlugin.name}" is unused. Removing...`);
      await client.plugins.destroy(customPlugin.id);
      console.log(`  Removed.`);
    } else {
      console.log(`"${customPlugin.name}" is used by ${fieldsUsing.length} field(s). Keeping.`);
    }
  }

  console.log("Plugin audit and configuration complete.");
}

auditAndConfigurePlugins().catch((error) => {
  if (error instanceof ApiError) {
    console.error("API error:", error.response.status, error.errors);
  } else {
    console.error(error);
  }
  process.exit(1);
});
```
