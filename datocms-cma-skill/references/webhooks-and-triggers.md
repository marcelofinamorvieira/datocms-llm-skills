# Webhooks and Build Triggers

Covers webhook configuration, build trigger management, and deploy operations.

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

For details on how cache tags work and the two architectural patterns (CDN-first vs framework-centric), see `datocms-cda-skill/references/draft-caching-environments.md` → "Cache Tags".

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
