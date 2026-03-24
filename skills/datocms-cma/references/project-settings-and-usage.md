# Project Settings and Usage

Covers project-level configuration and introspection: site settings, maintenance mode, public info, white-label branding, subscription limits, subscription features, daily usage data, and usage counters.

## Quick Navigation

- [Site Settings](#site-settings)
- [Maintenance Mode](#maintenance-mode)
- [Public Project Info](#public-project-info)
- [White-Label Settings](#white-label-settings)
- [Subscription Limits](#subscription-limits)
- [Subscription Features](#subscription-features)
- [Daily Usages](#daily-usages)
- [Usage Counters](#usage-counters)
- [Complete Example: Pre-Migration Environment Check](#complete-example-pre-migration-environment-check)

---

## Site Settings

Read and update project-wide settings including locales, timezone, global SEO defaults, and favicon.

### Reading Site Settings

```ts
const siteSettings = await client.site.find();

console.log("Project name:", siteSettings.name);
console.log("Locales:", siteSettings.locales);
console.log("Timezone:", siteSettings.timezone);
console.log("Theme:", siteSettings.theme);
console.log("No-index enabled:", siteSettings.no_index);
```

### Updating Site Settings

```ts
await client.site.update({
  name: "My Awesome Project",
  timezone: "Europe/Rome",
  no_index: false,
});
```

### Key Writable Attributes

| Attribute | Type | Default | Description |
|---|---|---|---|
| `name` | `string` | — | Project display name |
| `locales` | `string[]` | `["en"]` | Available locales; the first element is the primary locale |
| `timezone` | `string` | `"UTC"` | IANA timezone string (e.g. `"America/New_York"`) |
| `no_index` | `boolean` | `false` | When `true`, tells search engines not to index the project |
| `favicon` | `{ upload_id }` | `null` | Upload reference used as the project favicon |
| `global_seo` | `object` | `null` | Global SEO defaults (see below) |

### Global SEO Object

```ts
await client.site.update({
  global_seo: {
    site_name: "My Site",
    title_suffix: " | My Site",
    twitter_account: "@mysite",
    facebook_page_url: "https://facebook.com/mysite",
    fallback_seo: {
      title: "My Site — Default Title",
      description: "Default meta description for all pages.",
      image: "upload-id-here",
    },
  },
});
```

### Managing Locales

```ts
const siteSettings = await client.site.find();

// Add a new locale
const updatedLocales = [...siteSettings.locales, "fr"];
await client.site.update({ locales: updatedLocales });
```

**Important:** The first locale in the array is the primary locale. Changing the order of `locales` changes which locale is primary. Adding a new locale does NOT automatically populate existing records with content for that locale — you must update records individually.

---

## Maintenance Mode

Activate or deactivate maintenance mode on the primary environment. When active, the primary environment becomes read-only.

### Checking Maintenance Mode Status

```ts
const maintenanceStatus = await client.maintenanceMode.find();
console.log("Maintenance active:", maintenanceStatus.active);
```

### Activating Maintenance Mode

```ts
await client.maintenanceMode.activate();
console.log("Primary environment is now read-only.");
```

### Deactivating Maintenance Mode

```ts
await client.maintenanceMode.deactivate();
console.log("Primary environment is writable again.");
```

**Important:** A typical use case is activating maintenance mode before promoting a sandbox environment, then deactivating it after promotion completes. This prevents content editors from making changes that would be lost during promotion. See `references/environments.md` for the full promotion workflow.

---

## Public Project Info

Retrieve basic public information about the project.

```ts
const publicInfo = await client.publicInfo.find();

console.log("Project name:", publicInfo.name);
```

Use case: health checks, project identification scripts, or verifying that the API token points to the expected project.

---

## White-Label Settings

Customize the DatoCMS UI branding with a custom logo, colors, and other visual elements.

### Reading White-Label Settings

```ts
const brandingSettings = await client.whiteLabelSettings.find();
console.log("Current branding:", brandingSettings);
```

### Updating White-Label Settings

```ts
await client.whiteLabelSettings.update({
  custom_logo: { upload_id: "logo-upload-id" },
  custom_colors: {
    primary: "#FF5733",
    accent: "#33FF57",
  },
});
```

**Important:** White-label settings are an Enterprise plan feature only. Attempting to use these endpoints on a non-Enterprise plan will result in an error.

---

## Subscription Limits

Query the plan limits for the current project. Useful for pre-flight checks before bulk operations.

### Listing All Limits

```ts
const allLimits = await client.subscriptionLimits.list();

for (const limit of allLimits) {
  const maxValue = limit.limit === null ? "unlimited" : limit.limit;
  console.log(`${limit.id}: ${limit.current_usage} / ${maxValue}`);
}
```

### Finding a Specific Limit

```ts
const recordsLimit = await client.subscriptionLimits.find("records");

const maxRecords = recordsLimit.limit === null ? Infinity : recordsLimit.limit;
const remainingCapacity = maxRecords - recordsLimit.current_usage;

console.log(`Records: ${recordsLimit.current_usage} used, ${remainingCapacity} remaining`);
```

### Limit Object Attributes

| Attribute | Type | Description |
|---|---|---|
| `id` | `string` | Limit identifier (e.g. `"records"`, `"uploadable_bytes"`, `"item_types"`) |
| `limit` | `number \| null` | Maximum allowed value, or `null` for unlimited |
| `current_usage` | `number` | Current usage count |

---

## Subscription Features

Query which features are enabled on the current plan.

### Listing All Features

```ts
const allFeatures = await client.subscriptionFeatures.list();

for (const feature of allFeatures) {
  const status = feature.enabled ? "enabled" : "disabled";
  console.log(`${feature.id}: ${status}`);
}
```

### Feature Object Attributes

| Attribute | Type | Description |
|---|---|---|
| `id` | `string` | Feature identifier (e.g. `"sso"`, `"workflows"`, `"localization"`) |
| `enabled` | `boolean` | Whether the feature is available on the current plan |

Use case: check whether SSO, workflows, localization, or other gated features are available before attempting to use them in automation scripts.

---

## Daily Usages

Retrieve historical usage data broken down by day. Useful for building usage dashboards or analyzing trends.

```ts
const dailyUsageEntries = await client.dailyUsages.list();

for (const entry of dailyUsageEntries) {
  console.log(entry);
}
```

Use case: usage dashboards, trend analysis, and billing reconciliation.

---

## Usage Counters

Retrieve the current value of a specific usage counter for real-time quota monitoring.

```ts
const apiCallsCounter = await client.usageCounters.find("api-calls");
console.log("Current API calls:", apiCallsCounter);
```

Use case: real-time quota monitoring, alerting when usage approaches plan limits.

---

## Type Reference

**Import:** `import type { ApiTypes } from "@datocms/cma-client-node";`

> **Note:** These types are auto-generated from the DatoCMS CMA OpenAPI schema. Always refer to the installed package version as the source of truth, since properties may change between releases.

### `ApiTypes.Site` (Response)

Returned by `client.site.find()`. Key properties are listed below; additional properties exist for internal settings.

| Property | Type | Description |
|---|---|---|
| `id` | `SiteIdentity` | Unique project identifier |
| `name` | `string` | Project display name |
| `locales` | `[string, ...string[]]` | Available locales (first element is the primary locale) |
| `timezone` | `string` | IANA timezone string (e.g. `"America/New_York"`) |
| `no_index` | `boolean` | Whether search engines should be told not to index the project |
| `favicon` | `string \| null` | Upload ID used as the project favicon |
| `global_seo` | `object \| null` | Global SEO defaults (site_name, fallback_seo, title_suffix, facebook_page_url, twitter_account) |
| `theme` | `object` | Admin UI theme with `type` (`"custom"` or `"monochromatic"`), `hue`, color objects (`primary_color`, `light_color`, `accent_color`, `dark_color`), and `logo` |
| `domain` | `string \| null` | Custom domain for the administrative area |
| `internal_domain` | `string \| null` | DatoCMS internal domain for the administrative area |
| `google_maps_api_token` | `string \| null` | Google API key for the LatLon widget |
| `imgix_host` | `string \| null` | Imgix host |
| `last_data_change_at` | `string \| null` | ISO timestamp of the last data change |
| `require_2fa` | `boolean` | Whether all users must use two-factor authentication |
| `ip_tracking_enabled` | `boolean` | Whether IPs are tracked in the usage section |
| `force_use_of_sandbox_environments` | `boolean` | If enabled, blocks schema changes on the primary environment |
| `assets_cdn_default_settings` | `object` | Default CDN parameters for images (q, auto, cs) and videos (disable_serving_raw_videos) |
| `item_types` | `ItemTypeData[]` | Relationship data for the project's models |
| `meta` | `SiteMeta` | Meta attributes (created_at, draft_mode_default, etc.) |

### `ApiTypes.SiteUpdateSchema` (Input)

Passed to `client.site.update()`. All properties are optional (partial update). Commonly used properties are listed below.

| Property | Type | Required | Description |
|---|---|---|---|
| `name` | `string` | No | Project display name |
| `locales` | `[string, ...string[]]` | No | Available locales; first element becomes the primary locale |
| `timezone` | `string` | No | IANA timezone string |
| `no_index` | `boolean` | No | Whether search engines should not index the project |
| `favicon` | `string \| null` | No | Upload ID for the favicon |
| `global_seo` | `object \| null` | No | Global SEO defaults (same structure as the response type) |
| `theme` | `object` | No | Admin UI theme — either `{ type: "monochromatic", hue, logo }` or `{ type: "custom", logo, primary_color, light_color, accent_color, dark_color? }` |
| `require_2fa` | `boolean` | No | Require two-factor authentication for all users |
| `ip_tracking_enabled` | `boolean` | No | Track IPs in the usage section |
| `force_use_of_sandbox_environments` | `boolean` | No | Block schema changes on the primary environment |
| `meta` | `object` | No | Opt-in product updates (improved_timezone_management, improved_hex_management, draft_mode_default, etc.) |

### `ApiTypes.SiteSelfHrefSchema` (Query Parameters)

Optional parameters when calling `client.site.find()`.

| Property | Type | Required | Description |
|---|---|---|---|
| `include` | `string` | No | Comma-separated relationship paths to include (allowed: `item_types`, `item_types.fields`, `item_types.fieldsets`, `item_types.singleton_item`, `account`) |

### `ApiTypes.MaintenanceMode` (Response)

Returned by `client.maintenanceMode.find()`.

| Property | Type | Description |
|---|---|---|
| `id` | `MaintenanceModeIdentity` | Resource identifier |
| `active` | `boolean` | Whether maintenance mode is currently active |

### `ApiTypes.MaintenanceModeActivateHrefSchema` (Query Parameters)

Optional parameters when calling `client.maintenanceMode.activate()`.

| Property | Type | Required | Description |
|---|---|---|---|
| `force` | `boolean` | No | Force activation even if collaborators are currently editing records |

### `ApiTypes.PublicInfo` (Response)

Returned by `client.publicInfo.find()`.

| Property | Type | Description |
|---|---|---|
| `id` | `PublicInfoIdentity` | Resource identifier |
| `name` | `string` | Project name |
| `sso_saml_init_url` | `string \| null` | Single Sign-On URL, if configured |
| `logo_url` | `string \| null` | Logo URL, if present |
| `white_label` | `boolean` | Whether the project is in white-label mode |
| `custom_i18n_messages_template_url` | `string \| null` | Template URL for custom i18n messages (white-label only) |
| `theme` | `object` | Color scheme with `primary_color`, `light_color`, `accent_color`, `dark_color` (each has `red`, `green`, `blue`, `alpha`) |
| `extras` | `object \| null` | Additional info on authenticated requests: `blocks_depth`, `blocks_per_item`, `maximum_single_upload_bytes` |

### `ApiTypes.WhiteLabelSettings` (Response)

Returned by `client.whiteLabelSettings.find()`.

| Property | Type | Description |
|---|---|---|
| `id` | `WhiteLabelSettingsIdentity` | Resource identifier |
| `custom_i18n_messages_template_url` | `string \| null` | URL of custom i18n messages (`:locale` placeholder represents the current DatoCMS UI locale) |

### `ApiTypes.WhiteLabelSettingsUpdateSchema` (Input)

Passed to `client.whiteLabelSettings.update()`.

| Property | Type | Required | Description |
|---|---|---|---|
| `custom_i18n_messages_template_url` | `string \| null` | No | URL of custom i18n messages (`:locale` placeholder for locale) |

### `ApiTypes.SubscriptionLimit` (Response)

Returned by `client.subscriptionLimits.list()` and `client.subscriptionLimits.find()`.

| Property | Type | Description |
|---|---|---|
| `id` | `SubscriptionLimitIdentity` | Limit identifier (e.g. `"records"`, `"uploadable_bytes"`) |
| `code` | `string` | Codename for the limit |
| `usage` | `number` | Current usage count |
| `limit` | `number \| null` | Maximum allowed value, or `null` for unlimited |

### `ApiTypes.SubscriptionFeature` (Response)

Returned by `client.subscriptionFeatures.list()`.

| Property | Type | Description |
|---|---|---|
| `id` | `SubscriptionFeatureIdentity` | Feature identifier (e.g. `"sso"`, `"workflows"`) |
| `code` | `string` | Codename for the feature |
| `enabled` | `boolean` | Whether the feature is available on the current plan |
| `in_use` | `boolean` (optional) | Whether the project is currently using the feature |

### `ApiTypes.DailyUsage` (Response)

Returned by `client.dailyUsages.list()`.

| Property | Type | Description |
|---|---|---|
| `id` | `DailyUsageIdentity` | Resource identifier |
| `date` | `string` | The date the data refer to |
| `cda_api_calls` | `number` | Number of Content Delivery API calls |
| `cma_api_calls` | `number` | Number of Content Management API calls |
| `cda_traffic_bytes` | `number` | Content Delivery API traffic in bytes |
| `cma_traffic_bytes` | `number` | Content Management API traffic in bytes |
| `assets_traffic_bytes` | `number` | Upload/asset request traffic in bytes |
| `mux_delivered_seconds` | `number` | Regular video streaming (max 1080p), in seconds |
| `mux_high_resolution_delivered_seconds` | `number` | High-res video streaming (> 1080p), in seconds |
| `mux_encoded_seconds` | `number` | Video encoding seconds |

### `ApiTypes.UsageCounter` (Response)

Returned by `client.usageCounters.find()`.

| Property | Type | Description |
|---|---|---|
| `id` | `UsageCounterIdentity` | Counter identifier (e.g. `"api-calls"`) |
| `result` | `Array<{ value: string; counter: number }>` | Array of occurrence/counter pairs |

### `ApiTypes.UsageCounterSelfHrefSchema` (Query Parameters)

Optional parameters when calling `client.usageCounters.find()`.

| Property | Type | Required | Description |
|---|---|---|---|
| `period` | `"today" \| "current_month" \| "last_month"` | No | Time period for the counter data |

### `ApiTypes.SitePlan`

The `SitePlan` type exists but is omitted from this reference due to its size. Refer to the installed `@datocms/cma-client` package types for the full definition.

---

## Complete Example: Pre-Migration Environment Check

A script that reads site settings, checks subscription limits, verifies maintenance mode status, activates maintenance mode, and logs everything — a typical pre-flight check before promoting a sandbox environment.

```ts
import { buildClient, ApiError } from "@datocms/cma-client-node";

const client = buildClient({
  apiToken: process.env.DATOCMS_API_TOKEN!,
});

async function preMigrationCheck() {
  // Step 1: Read site settings
  console.log("=== Site Settings ===");
  const siteSettings = await client.site.find();

  console.log("Project name:", siteSettings.name);
  console.log("Primary locale:", siteSettings.locales[0]);
  console.log("All locales:", siteSettings.locales.join(", "));
  console.log("Timezone:", siteSettings.timezone);

  const hasGlobalSeo = siteSettings.global_seo !== null;
  console.log("Global SEO configured:", hasGlobalSeo);

  // Step 2: Check subscription limits
  console.log("\n=== Subscription Limits ===");
  const allLimits = await client.subscriptionLimits.list();

  const criticalLimitIds = ["records", "uploadable_bytes", "item_types", "fields"];

  for (const limit of allLimits) {
    const isCritical = criticalLimitIds.includes(limit.id);
    const maxValue = limit.limit === null ? "unlimited" : limit.limit;
    const prefix = isCritical ? "[CRITICAL]" : "[INFO]";

    console.log(`${prefix} ${limit.id}: ${limit.current_usage} / ${maxValue}`);

    if (isCritical && limit.limit !== null) {
      const usagePercentage = (limit.current_usage / limit.limit) * 100;

      if (usagePercentage > 90) {
        console.warn(`  WARNING: ${limit.id} is at ${usagePercentage.toFixed(1)}% capacity!`);
      }
    }
  }

  // Step 3: Check subscription features
  console.log("\n=== Subscription Features ===");
  const allFeatures = await client.subscriptionFeatures.list();

  for (const feature of allFeatures) {
    const status = feature.enabled ? "enabled" : "disabled";
    console.log(`${feature.id}: ${status}`);
  }

  // Step 4: Check current maintenance mode status
  console.log("\n=== Maintenance Mode ===");
  const maintenanceStatus = await client.maintenanceMode.find();
  console.log("Currently active:", maintenanceStatus.active);

  if (maintenanceStatus.active) {
    console.log("Maintenance mode is already active. Proceeding with migration.");
    return;
  }

  // Step 5: Activate maintenance mode before migration
  console.log("Activating maintenance mode...");
  await client.maintenanceMode.activate();

  const confirmStatus = await client.maintenanceMode.find();
  console.log("Maintenance mode activated:", confirmStatus.active);

  // Step 6: Log summary
  console.log("\n=== Pre-Migration Summary ===");
  console.log(`Project: ${siteSettings.name}`);
  console.log(`Locales: ${siteSettings.locales.length} configured`);
  console.log(`Timezone: ${siteSettings.timezone}`);
  console.log(`Limits checked: ${allLimits.length}`);
  console.log(`Features checked: ${allFeatures.length}`);
  console.log("Maintenance mode: ACTIVE");
  console.log("\nReady for environment promotion.");
  console.log("Remember to deactivate maintenance mode after promotion:");
  console.log("  await client.maintenanceMode.deactivate();");
}

preMigrationCheck().catch((error) => {
  if (error instanceof ApiError) {
    console.error("Pre-migration check failed:", error.response.status, error.errors);
  } else {
    console.error(error);
  }
  process.exit(1);
});
```
