# Webhooks and Build Triggers

Covers webhook configuration, build trigger management, and deploy operations.

## Quick Navigation

- [Webhooks](#webhooks)
- [Webhook Call Logs](#webhook-call-logs)
- [Receiving Webhooks (Payload & Behavior)](#receiving-webhooks-payload--behavior)
- [Cache Tags Invalidation Webhook](#cache-tags-invalidation-webhook)
- [Build Triggers](#build-triggers)
- [Triggering and Aborting Deploys](#triggering-and-aborting-deploys)
- [Listing, Updating, Deleting Build Triggers](#listing-updating-deleting-build-triggers)
- [Build Events](#build-events)
- [Type Reference](#type-reference)
- [Complete Example: Set Up Webhook + Build Trigger](#complete-example-set-up-webhook--build-trigger)

---

## Webhooks

Webhooks send HTTP notifications when events occur in DatoCMS.

### Creating a Webhook

```ts
const webhook = await client.webhooks.create({
  name: "Notify on publish",
  url: "https://example.com/webhook",
  headers: {
    Authorization: "Bearer secret-token",
  },
  events: [
    {
      entity_type: "item",
      event_types: ["publish", "unpublish"],
    },
  ],
  custom_payload: null,
  http_basic_user: null,
  http_basic_password: null,
  enabled: true,
  payload_api_version: "3",
  nested_items_in_payload: false,
});
```

### Webhook Event Configuration

Each event entry specifies an `entity_type` and the `event_types` to listen for:

| `entity_type` | Available `event_types` |
|---|---|
| `item` | `create`, `update`, `delete`, `publish`, `unpublish` |
| `item_type` | `create`, `update`, `delete` |
| `upload` | `create`, `update`, `delete` |
| `build_trigger` | `deploy_started`, `deploy_succeeded`, `deploy_failed` |
| `environment` | `create`, `delete`, `promote` |
| `maintenance_mode` | `change` |
| `sso_user` | `create`, `update`, `delete` |
| `cda_cache_tags` | `invalidate` |

### Event Filters

Narrow webhook events to specific models or conditions. Filters are defined **inside each `events[]` entry**:

```ts
const webhook = await client.webhooks.create({
  name: "Blog post changes",
  url: "https://example.com/webhook",
  headers: {},
  events: [
    {
      entity_type: "item",
      event_types: ["create", "update"],
      filters: [
        {
          entity_type: "item_type",
          entity_ids: [blogModelId], // Only blog_post records
        },
      ],
    },
  ],
  custom_payload: null,
  http_basic_user: null,
  http_basic_password: null,
  enabled: true,
  payload_api_version: "3",
});
```

Each filter entry has:
- `entity_type`: `"item_type"` | `"item"` | `"build_trigger"` | `"environment"` | `"environment_type"`
- `entity_ids`: array of string IDs to match

### Custom Payloads (Mustache Templating)

Send a custom payload instead of the default JSON:API body:

```ts
const webhook = await client.webhooks.create({
  name: "Slack notification",
  url: "https://hooks.slack.com/services/...",
  headers: { "Content-Type": "application/json" },
  events: [{ entity_type: "item", event_types: ["publish"] }],
  custom_payload: JSON.stringify({
    text: "Record {{entity.attributes.title}} was published!",
  }),
  http_basic_user: null,
  http_basic_password: null,
  enabled: true,
  payload_api_version: "3",
});
```

### Webhook Attributes

| Attribute | Type | Description |
|---|---|---|
| `name` | `string` | **Required.** Display name |
| `url` | `string` | **Required.** Endpoint URL |
| `headers` | `Record<string, string>` | **Required.** Custom headers (can be `{}`) |
| `events` | `array` | **Required.** Event configurations (each entry has `entity_type`, `event_types`, and optional `filters`) |
| `custom_payload` | `string \| null` | **Required.** Mustache template for custom payloads (pass `null` for default payload) |
| `http_basic_user` | `string \| null` | **Required.** HTTP Basic auth username (pass `null` if unused) |
| `http_basic_password` | `string \| null` | **Required.** HTTP Basic auth password (pass `null` if unused) |
| `enabled` | `boolean` | Whether the webhook is active |
| `payload_api_version` | `string` | API version for payloads (use `"3"`) |
| `nested_items_in_payload` | `boolean` | Include nested blocks in the payload |
| `auto_retry` | `boolean` | Automatically retry on timeout or error |

### Listing, Finding, Updating, Deleting Webhooks

```ts
// List all
const webhooks = await client.webhooks.list();

// Find by ID
const webhook = await client.webhooks.find("webhook-id");

// Update
await client.webhooks.update("webhook-id", {
  enabled: false,
});

// Delete
await client.webhooks.destroy("webhook-id");
```

---

## Webhook Call Logs

Review the history of webhook deliveries:

```ts
for await (const call of client.webhookCalls.listPagedIterator()) {
  console.log(
    call.id,
    call.response_status,
    call.created_at,
  );
}
```

### Filter by Webhook

```ts
for await (const call of client.webhookCalls.listPagedIterator({
  filter: { webhook_id: "webhook-id" },
})) {
  console.log(call.response_status);
}
```

### Find a Specific Webhook Call

```ts
const call = await client.webhookCalls.find("webhook-call-id");

console.log(call.request_url);
console.log(call.request_headers);
console.log(call.request_payload);
console.log(call.response_status);
console.log(call.response_headers);
console.log(call.response_payload);
```

### Resend a Failed Webhook

```ts
await client.webhookCalls.resendWebhook("webhook-call-id");
```

---

## Receiving Webhooks (Payload & Behavior)

When building a webhook handler, your endpoint receives a POST request with a JSON body. Unless you set a `custom_payload`, the default payload contains:

| Field | Description |
|---|---|
| `site_id` | The DatoCMS project ID |
| `webhook_id` | ID of the webhook that fired |
| `webhook_call_id` | Unique ID for this specific delivery attempt |
| `environment` | Environment name (e.g. `"main"`) |
| `is_environment_primary` | `true` if the event occurred on the primary environment |
| `event_triggered_at` | ISO 8601 timestamp of when the event occurred |
| `entity_type` | `"item"`, `"item_type"`, `"upload"`, etc. |
| `event_type` | `"create"`, `"update"`, `"publish"`, etc. |
| `entity` | Full serialized entity at the time of the event |
| `previous_entity` | Previous state of the entity (only present on `update` events, `null` otherwise) |
| `related_entities` | Associated entities (e.g. the model for a record event) |

### Timeouts and Retries

- **Connection timeout:** 2 seconds — your endpoint must accept the connection within 2s.
- **Execution timeout:** 8 seconds — your endpoint must respond within 8s total.
- **Auto-retry** (when `auto_retry: true`): up to 7 retries with escalating delays — 2 min, 6 min, 30 min, 1 hr, 5 hrs, 1 day, 2 days.

If your handler needs to do heavy processing, accept the webhook immediately (return 200) and process asynchronously.

### Event Lifecycle with Draft/Published

When a model has draft/published enabled:

| Action | Events fired |
|---|---|
| Create new record | `create` (status: draft) |
| Publish a draft | `publish` (status: published) |
| Edit a published record | `update` (status: updated) |
| Re-publish after edit | `publish` (status: published) |
| Unpublish | `unpublish` (status: draft) |
| Delete a published record | `unpublish` + `delete` |

When a model does **not** have draft/published enabled:

| Action | Events fired |
|---|---|
| Create new record | `create` + `publish` |
| Update a record | `update` + `publish` |
| Delete a record | `unpublish` + `delete` |

---

## Cache Tags Invalidation Webhook

To programmatically create a webhook that fires when CDA cache tags need invalidation, use the `cda_cache_tags` / `invalidate` event type:

```ts
const webhook = await client.webhooks.create({
  name: "Cache tags invalidation",
  url: "https://example.com/api/revalidate",
  headers: {
    Authorization: `Bearer ${process.env.CACHE_INVALIDATION_WEBHOOK_SECRET}`,
  },
  events: [
    {
      entity_type: "cda_cache_tags",
      event_types: ["invalidate"],
    },
  ],
  custom_payload: null,
  http_basic_user: null,
  http_basic_password: null,
  enabled: true,
  payload_api_version: "3",
  nested_items_in_payload: false,
});
```

**Webhook payload format:**
```json
{
  "entity_type": "cda_cache_tags",
  "event_type": "invalidate",
  "entity": {
    "id": "cda_cache_tags",
    "type": "cda_cache_tags",
    "attributes": {
      "tags": ["N*r;L", "6-KZ@", "t#k[uP"]
    }
  }
}
```

**Note:** This event type does not support filters — the webhook always fires for all cache tag changes. You cannot narrow it to specific models or records.

For details on how cache tags work and the two architectural patterns (CDN-first vs framework-centric), see `skills/datocms-cda/references/draft-caching-environments.md` → "Cache Tags".

---

## Build Triggers

Build triggers connect DatoCMS to deployment platforms. When content changes, DatoCMS can trigger a rebuild of your frontend.

### Creating a Build Trigger

#### Custom Webhook Adapter

```ts
const trigger = await client.buildTriggers.create({
  name: "Deploy to production",
  adapter: "custom",
  adapter_settings: {
    trigger_url: "https://example.com/deploy",
    headers: { Authorization: "Bearer deploy-token" },
    payload: { project: "my-site" },
  },
  frontend_url: "https://www.example.com",
  autotrigger_on_scheduled_publications: true,
  enabled: true,
});
```

#### Netlify Adapter

```ts
const trigger = await client.buildTriggers.create({
  name: "Deploy to Netlify",
  adapter: "netlify",
  adapter_settings: {
    site_id: "netlify-site-id",
    trigger_url: "https://api.netlify.com/build_hooks/...",
    access_token: "netlify-access-token",
    branch: "main",
  },
  frontend_url: "https://www.example.com",
  autotrigger_on_scheduled_publications: true,
  enabled: true,
});
```

#### Vercel Adapter

```ts
const trigger = await client.buildTriggers.create({
  name: "Deploy to Vercel",
  adapter: "vercel",
  adapter_settings: {
    project_id: "vercel-project-id",
    team_id: "vercel-team-id",
    deploy_hook_url: "https://api.vercel.com/v1/integrations/deploy/...",
    token: "vercel-token",
    branch: "main",
  },
  frontend_url: "https://www.example.com",
  autotrigger_on_scheduled_publications: true,
  enabled: true,
});
```

### Build Trigger Attributes

| Attribute | Type | Description |
|---|---|---|
| `name` | `string` | **Required.** Display name |
| `adapter` | `"custom" \| "netlify" \| "vercel" \| "gitlab"` | **Required.** Deployment adapter |
| `adapter_settings` | `Record<string, unknown>` | Adapter-specific configuration (depends on adapter type) |
| `webhook_token` | `string` | Optional unique token for the webhook |
| `frontend_url` | `string \| null` | **Required.** Public URL of the frontend |
| `autotrigger_on_scheduled_publications` | `boolean` | **Required.** Auto-trigger on scheduled publish/unpublish |
| `enabled` | `boolean` | Whether the trigger is active |

---

## Triggering and Aborting Deploys

### Trigger a Deploy

```ts
await client.buildTriggers.trigger("trigger-id");
```

### Abort a Running Deploy

```ts
await client.buildTriggers.abort("trigger-id");
```

### Trigger Site Search Re-indexing

```ts
await client.buildTriggers.reindex("trigger-id");
```

### Abort a Running Search Indexing

```ts
await client.buildTriggers.abortIndexing("trigger-id");
```

---

## Listing, Updating, Deleting Build Triggers

```ts
// List all
const triggers = await client.buildTriggers.list();

// Find by ID
const trigger = await client.buildTriggers.find("trigger-id");

// Update
await client.buildTriggers.update("trigger-id", {
  enabled: false,
});

// Delete
await client.buildTriggers.destroy("trigger-id");
```

---

## Build Events

Review the history of deployments:

```ts
for await (const event of client.buildEvents.listPagedIterator()) {
  console.log(event.id, event.event_type, event.created_at);
}
```

---

## Type Reference

These types are auto-generated from the DatoCMS CMA API schema. Always refer to the installed package for the most up-to-date definitions:

```ts
import type {
  Webhook,
  WebhookCreateSchema,
  WebhookUpdateSchema,
  WebhookCall,
  WebhookCallInstancesHrefSchema,
  BuildTrigger,
  BuildTriggerCreateSchema,
  BuildTriggerUpdateSchema,
  BuildEvent,
  BuildEventInstancesHrefSchema,
} from "@datocms/cma-client";
```

> **Versioning note:** The exact shape of these types may change between `@datocms/cma-client` versions. If a property listed below does not match your installed version, the installed `.d.ts` file is the source of truth.

### Webhook (Response)

Returned by `client.webhooks.create()`, `find()`, `update()`, `list()`, and `destroy()`.

| Property | Type |
|---|---|
| `id` | `string` |
| `type` | `'webhook'` |
| `name` | `string` |
| `enabled` | `boolean` |
| `url` | `string` |
| `custom_payload` | `string \| null` |
| `http_basic_user` | `string \| null` |
| `http_basic_password` | `string \| null` |
| `headers` | `Record<string, string>` |
| `events` | `Array<{ entity_type, event_types, filters? }>` (see Events shape below) |
| `payload_api_version` | `string` |
| `nested_items_in_payload` | `boolean` |
| `auto_retry` | `boolean` |

**Events array shape** (applies to `Webhook`, `WebhookCreateSchema`, and `WebhookUpdateSchema`):

Each entry in the `events` array has:

| Property | Type |
|---|---|
| `entity_type` | `'item_type' \| 'item' \| 'upload' \| 'build_trigger' \| 'environment' \| 'maintenance_mode' \| 'sso_user' \| 'cda_cache_tags'` |
| `event_types` | `Array<'create' \| 'update' \| 'delete' \| 'publish' \| 'unpublish' \| 'promote' \| 'deploy_started' \| 'deploy_succeeded' \| 'deploy_failed' \| 'change' \| 'invalidate'>` |
| `filters?` | `Array<{ entity_type: 'item_type' \| 'item' \| 'build_trigger' \| 'environment' \| 'environment_type', entity_ids: [string, ...string[]] }> \| null` |

### WebhookCreateSchema (Input)

Passed to `client.webhooks.create()`.

| Property | Type | Required | Description |
|---|---|---|---|
| `name` | `string` | Yes | Unique name for the webhook |
| `url` | `string` | Yes | The URL to be called |
| `headers` | `Record<string, string>` | Yes | Additional headers (pass `{}` if none) |
| `events` | `Array<{ entity_type, event_types, filters? }>` | Yes | Event configurations (see Events shape above) |
| `custom_payload` | `string \| null` | Yes | Mustache template string for a custom payload body, or `null` for the default JSON:API payload. When set, the entire request body is replaced by this rendered template. |
| `http_basic_user` | `string \| null` | Yes | HTTP Basic auth username (pass `null` if unused) |
| `http_basic_password` | `string \| null` | Yes | HTTP Basic auth password (pass `null` if unused) |
| `enabled` | `boolean` | No | Whether the webhook is active (defaults to enabled) |
| `payload_api_version` | `string` | No | API version for serializing entities in the payload |
| `nested_items_in_payload` | `boolean` | No | Whether records in the payload show blocks expanded |
| `auto_retry` | `boolean` | No | Retry on timeout or error |

### WebhookUpdateSchema (Input)

Passed to `client.webhooks.update()`. All fields are optional -- only include what you want to change.

| Property | Type | Required | Description |
|---|---|---|---|
| `name` | `string` | No | Unique name for the webhook |
| `url` | `string` | No | The URL to be called |
| `headers` | `Record<string, string>` | No | Additional headers |
| `events` | `Array<{ entity_type, event_types, filters? }>` | No | Event configurations (see Events shape above) |
| `custom_payload` | `string \| null` | No | Mustache template string, or `null` for default payload |
| `http_basic_user` | `string \| null` | No | HTTP Basic auth username |
| `http_basic_password` | `string \| null` | No | HTTP Basic auth password |
| `enabled` | `boolean` | No | Whether the webhook is active |
| `payload_api_version` | `string` | No | API version for serializing entities in the payload |
| `nested_items_in_payload` | `boolean` | No | Whether records in the payload show blocks expanded |
| `auto_retry` | `boolean` | No | Retry on timeout or error |

### WebhookCall (Response)

Returned by `client.webhookCalls.find()` and `client.webhookCalls.listPagedIterator()`.

| Property | Type |
|---|---|
| `id` | `string` |
| `type` | `'webhook_call'` |
| `entity_type` | `'item_type' \| 'item' \| 'upload' \| 'build_trigger' \| 'environment' \| 'maintenance_mode' \| 'sso_user' \| 'cda_cache_tags'` |
| `event_type` | `'create' \| 'update' \| 'delete' \| 'publish' \| 'unpublish' \| 'promote' \| 'deploy_started' \| 'deploy_succeeded' \| 'deploy_failed' \| 'change' \| 'invalidate'` |
| `created_at` | `string` |
| `request_url` | `string` |
| `request_headers` | `Record<string, unknown>` |
| `request_payload` | `string` (JSON-encoded; use `JSON.parse()` to decode) |
| `response_status` | `number \| null` |
| `response_headers` | `Record<string, unknown> \| null` |
| `response_payload` | `string \| null` |
| `attempted_auto_retries_count` | `number` |
| `last_sent_at` | `string` |
| `next_retry_at` | `string \| null` |
| `status` | `'pending' \| 'success' \| 'failed' \| 'rescheduled'` |
| `webhook` | `{ type: 'webhook', id: string }` |

### WebhookCallInstancesHrefSchema (Query Parameters)

Passed to `client.webhookCalls.listPagedIterator()`.

| Property | Type | Required | Description |
|---|---|---|---|
| `page.offset` | `number` | No | Zero-based offset (defaults to 0) |
| `page.limit` | `number` | No | Max entities to return (defaults to 30, max 500) |
| `filter.ids` | `string` | No | IDs to fetch, comma separated |
| `filter.fields.webhook_id.eq` | `string` | No | Filter by webhook ID |
| `filter.fields.entity_type.eq` | `'item_type' \| 'item' \| 'upload' \| 'build_trigger' \| 'environment' \| 'maintenance_mode' \| 'sso_user' \| 'cda_cache_tags'` | No | Filter by entity type |
| `filter.fields.event_type.eq` | `'create' \| 'update' \| 'delete' \| 'publish' \| 'unpublish' \| 'promote' \| 'deploy_started' \| 'deploy_succeeded' \| 'deploy_failed' \| 'change' \| 'invalidate'` | No | Filter by event type |
| `filter.fields.status.eq` | `'pending' \| 'success' \| 'failed' \| 'rescheduled'` | No | Filter by delivery status |
| `filter.fields.last_sent_at.gt` / `.lt` | `string` | No | Filter by last sent timestamp |
| `filter.fields.next_retry_at.gt` / `.lt` | `string` | No | Filter by next retry timestamp |
| `filter.fields.created_at.gt` / `.lt` | `string` | No | Filter by creation timestamp |
| `order_by` | `'webhook_id_asc' \| 'webhook_id_desc' \| 'created_at_asc' \| 'created_at_desc' \| 'last_sent_at_asc' \| 'last_sent_at_desc' \| 'next_retry_at_asc' \| 'next_retry_at_desc'` | No | Sort order |

### BuildTrigger (Response)

Returned by `client.buildTriggers.create()`, `find()`, `update()`, `list()`, and `destroy()`.

| Property | Type |
|---|---|
| `id` | `string` |
| `type` | `'build_trigger'` |
| `name` | `string` |
| `adapter` | `'custom' \| 'netlify' \| 'vercel' \| 'circle_ci' \| 'gitlab' \| 'travis'` |
| `adapter_settings` | `Record<string, unknown>` |
| `last_build_completed_at` | `string \| null` |
| `build_status` | `string` |
| `webhook_token` | `string` (optional) |
| `webhook_url` | `string` |
| `indexing_status` | `string` |
| `frontend_url` | `string \| null` |
| `autotrigger_on_scheduled_publications` | `boolean` |
| `indexing_enabled` | `boolean` |

### BuildTriggerCreateSchema (Input)

Passed to `client.buildTriggers.create()`.

The `adapter_settings` object varies by adapter type. See the [Creating a Build Trigger](#creating-a-build-trigger) section above for adapter-specific examples (custom, Netlify, Vercel).

| Property | Type | Required | Description |
|---|---|---|---|
| `name` | `string` | Yes | Name of the build trigger |
| `adapter` | `'custom' \| 'netlify' \| 'vercel' \| 'circle_ci' \| 'gitlab' \| 'travis'` | Yes | Deployment adapter type |
| `adapter_settings` | `Record<string, unknown>` | Yes | Adapter-specific configuration. Shape depends on `adapter`: **custom** expects `{ trigger_url, headers, payload }`. **netlify** expects `{ site_id, trigger_url, access_token, branch }`. **vercel** expects `{ project_id, team_id, deploy_hook_url, token, branch }`. |
| `frontend_url` | `string \| null` | Yes | Public URL of the frontend (also used as Site Search start URL) |
| `autotrigger_on_scheduled_publications` | `boolean` | Yes | Auto-trigger on scheduled publish/unpublish |
| `indexing_enabled` | `boolean` | Yes | Whether Site Search spidering is enabled |
| `webhook_token` | `string` | No | Unique token for the webhook |

### BuildTriggerUpdateSchema (Input)

Passed to `client.buildTriggers.update()`. All fields are optional -- only include what you want to change.

| Property | Type | Required | Description |
|---|---|---|---|
| `name` | `string` | No | Name of the build trigger |
| `adapter` | `'custom' \| 'netlify' \| 'vercel' \| 'circle_ci' \| 'gitlab' \| 'travis'` | No | Deployment adapter type |
| `adapter_settings` | `Record<string, unknown>` | No | Adapter-specific configuration (see `BuildTriggerCreateSchema` for shape details) |
| `frontend_url` | `string \| null` | No | Public URL of the frontend |
| `autotrigger_on_scheduled_publications` | `boolean` | No | Auto-trigger on scheduled publish/unpublish |
| `indexing_enabled` | `boolean` | No | Whether Site Search spidering is enabled |

### BuildEvent (Response)

Returned by `client.buildEvents.listPagedIterator()`.

| Property | Type |
|---|---|
| `id` | `string` |
| `type` | `'build_event'` |
| `event_type` | `'request_success' \| 'request_failure' \| 'response_success' \| 'response_failure' \| 'request_aborted' \| 'response_unprocessable' \| 'indexing_started' \| 'indexing_success' \| 'indexing_failure'` |
| `created_at` | `string` |
| `data` | `Record<string, unknown>` |
| `build_trigger` | `{ type: 'build_trigger', id: string }` |

### BuildEventInstancesHrefSchema (Query Parameters)

Passed to `client.buildEvents.listPagedIterator()`.

| Property | Type | Required | Description |
|---|---|---|---|
| `page.offset` | `number` | No | Zero-based offset (defaults to 0) |
| `page.limit` | `number` | No | Max entities to return (defaults to 30, max 500) |
| `filter.ids` | `string` | No | IDs to fetch, comma separated |
| `filter.fields.build_trigger_id.eq` | `string` | No | Filter by build trigger ID |
| `filter.fields.event_type.eq` | `'request_success' \| 'request_failure' \| 'response_success' \| 'response_failure' \| 'request_aborted' \| 'response_unprocessable' \| 'indexing_started' \| 'indexing_success' \| 'indexing_failure'` | No | Filter by event type |
| `filter.fields.created_at.gt` / `.lt` | `string` | No | Filter by creation timestamp |
| `order_by` | `'build_trigger_id_asc' \| 'build_trigger_id_desc' \| 'created_at_asc' \| 'created_at_desc' \| 'event_type_asc' \| 'event_type_desc'` | No | Sort order |

---

## Complete Example: Set Up Webhook + Build Trigger

```ts
import { buildClient } from "@datocms/cma-client-node";

const client = buildClient({
  apiToken: process.env.DATOCMS_API_TOKEN!,
});

async function setupDeployPipeline() {
  // Create a webhook that notifies Slack on publish
  await client.webhooks.create({
    name: "Slack: content published",
    url: process.env.SLACK_WEBHOOK_URL!,
    headers: { "Content-Type": "application/json" },
    events: [
      { entity_type: "item", event_types: ["publish"] },
    ],
    custom_payload: JSON.stringify({
      text: "Content published in DatoCMS!",
    }),
    http_basic_user: null,
    http_basic_password: null,
    enabled: true,
    payload_api_version: "3",
  });

  // Create a build trigger for the frontend
  const trigger = await client.buildTriggers.create({
    name: "Production deploy",
    adapter: "custom",
    adapter_settings: {
      trigger_url: process.env.DEPLOY_HOOK_URL!,
      headers: {},
      payload: {},
    },
    frontend_url: "https://www.example.com",
    autotrigger_on_scheduled_publications: true,
    enabled: true,
  });

  console.log("Deploy pipeline configured. Trigger ID:", trigger.id);
}

setupDeployPipeline().catch(console.error);
```
