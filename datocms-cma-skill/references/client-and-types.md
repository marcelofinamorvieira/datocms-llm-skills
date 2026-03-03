# Client Setup, Types, and Error Handling

This reference is always loaded. It covers the CMA client packages, initialization, type system, error handling, and automatic behaviors.

---

## Package Selection

| Package | Runtime | When to use |
|---|---|---|
| `@datocms/cma-client-node` | Node.js | Scripts, API routes, serverless functions, CI/CD, CLI tools. **Default choice.** |
| `@datocms/cma-client-browser` | Browser | SPAs calling CMA directly, browser extensions |
| `@datocms/cma-client` | Universal | Edge runtimes, custom environments. Requires providing `fetchFn`. |

All three packages export the same API surface. The only difference is the default `fetchFn` and, for the Node package, additional upload helpers (`createFromLocalFile`, `createFromUrl`, etc.).

Install with:

```bash
npm install @datocms/cma-client-node
```

---

## Building the Client

```ts
import { buildClient } from "@datocms/cma-client-node";

const client = buildClient({
  apiToken: process.env.DATOCMS_API_TOKEN!,
});
```

### All `ClientConfigOptions`

| Option | Type | Default | Description |
|---|---|---|---|
| `apiToken` | `string \| null` | — | **Required.** Full-access CMA API token. |
| `baseUrl` | `string` | `"https://site-api.datocms.com"` | Base URL of the API. |
| `environment` | `string` | — | Target a specific environment (e.g., `"sandbox-abc"`). When omitted, targets the primary environment. |
| `requestTimeout` | `number` | `30000` | Timeout in milliseconds per request. |
| `autoRetry` | `boolean` | `true` | Auto-retry on rate limits (429) and transient errors with linear incremental backoff. |
| `logLevel` | `LogLevel` | `LogLevel.NONE` | Logging verbosity (`NONE`, `BASIC`, `BODY`, `BODY_AND_HEADERS`). |
| `logFn` | `(message: string) => void` | `console.log` | Custom log function. |
| `extraHeaders` | `Record<string, string>` | — | Additional headers sent with every request. |
| `fetchFn` | `typeof fetch` | — | Custom fetch implementation. Required for `@datocms/cma-client` (base package). |

---

## The Dual API Surface

Every resource method exists in two forms:
- **Simplified** (default): `client.items.create(body)` — uses friendly attribute-based objects, handles serialization automatically
- **Raw**: `client.items.rawCreate(body)` — uses the JSON:API format exactly as the HTTP API expects

**Always use the simplified API** unless you specifically need the raw JSON:API format (e.g., accessing `meta.total_count` from list responses).

```ts
const record = await client.items.create({
  item_type: { id: "model_123", type: "item_type" },
  title: "Hello World",
  slug: "hello-world",
});

console.log(record.id);    // "abc123"
console.log(record.title); // "Hello World"
```

---

## Key Client Resources

| Resource | Property | Common operations |
|---|---|---|
| Records | `client.items` | CRUD, publish, unpublish, bulk ops |
| Record versions | `client.itemVersions` | List version history |
| Uploads (assets) | `client.uploads` | CRUD, bulk tag/destroy, references |
| Upload requests | `client.uploadRequest` | Create pre-signed upload URLs |
| Upload collections | `client.uploadCollections` | Manage asset folders |
| Models (item types) | `client.itemTypes` | CRUD, duplicate, referencing |
| Fields | `client.fields` | CRUD, duplicate, referencing |
| Fieldsets | `client.fieldsets` | CRUD |
| Environments | `client.environments` | Fork, promote, rename, destroy |
| Webhooks | `client.webhooks` | CRUD |
| Webhook calls | `client.webhookCalls` | List call logs, resend |
| Build triggers | `client.buildTriggers` | CRUD, trigger, abort |
| Roles | `client.roles` | CRUD, duplicate |
| API tokens | `client.accessTokens` | CRUD, regenerate |
| Users | `client.users` | List, find, update, destroy |
| Site invitations | `client.siteInvitations` | CRUD |
| Scheduled publication | `client.scheduledPublication` | Create, destroy |
| Scheduled unpublishing | `client.scheduledUnpublishing` | Create, destroy |
| Workflows | `client.workflows` | CRUD |
| Site | `client.site` | Find (get site settings, locales) |
| Audit log events | `client.auditLogEvents` | List audit log |

The client also has resources for SSO (`ssoUsers`, `ssoGroups`, `ssoSettings`), build events, search indexes, plugins, menu items, maintenance mode, and more — these are discoverable via autocomplete.

---

## Type System

### Type Namespaces

```ts
import type { ApiTypes } from "@datocms/cma-client-node";
```

The `ApiTypes` namespace contains all type definitions for the simplified API. Key types:

- `ApiTypes.Item` — A record (response)
- `ApiTypes.ItemCreateSchema` — Body for creating a record
- `ApiTypes.ItemUpdateSchema` — Body for updating a record
- `ApiTypes.ItemType` — A model definition (response)
- `ApiTypes.ItemTypeCreateSchema` — Body for creating a model
- `ApiTypes.Field` — A field definition (response)
- `ApiTypes.FieldCreateSchema` — Body for creating a field
- `ApiTypes.Upload` — An upload/asset (response)
- `ApiTypes.UploadCreateSchema` — Body for creating an upload
- `ApiTypes.Webhook` — A webhook (response)
- `ApiTypes.WebhookCreateSchema` — Body for creating a webhook
- `ApiTypes.Role` — A role (response)
- `ApiTypes.RoleCreateSchema` — Body for creating a role
- `ApiTypes.Environment` — An environment (response)
- `ApiTypes.AccessToken` — An API token (response)
- `ApiTypes.Workflow` — A workflow (response)

The `RawApiTypes` namespace contains the JSON:API equivalents for use with `raw*()` methods.

Many methods accept an optional generic `D extends ItemTypeDefinition` for per-model type safety, but this is advanced — without the generic, methods return loosely-typed objects that work fine.

**Legacy aliases:** `SimpleSchemaTypes` = `ApiTypes`, `SchemaTypes` = `RawApiTypes`. Use `ApiTypes`/`RawApiTypes` in new code.

---

## Error Handling

### `ApiError`

Thrown when the API returns a non-2xx response (except 429 rate limits, which are auto-retried).

```ts
import { ApiError } from "@datocms/cma-client-node";

try {
  await client.items.create({
    item_type: { id: "model_123", type: "item_type" },
    title: "Hello",
  });
} catch (error) {
  if (error instanceof ApiError) {
    console.log(error.response.status); // e.g., 422
    console.log(error.errors); // Array of ErrorEntity objects

    // Find a specific error by code
    const uniqueError = error.findError("VALIDATION_UNIQUE");
    if (uniqueError) {
      console.log("Duplicate value:", uniqueError.attributes.details);
    }
  }
  throw error;
}
```

**`ApiError` properties:**

| Property | Type | Description |
|---|---|---|
| `request` | `{ url, method, headers, body? }` | The request that failed |
| `response` | `{ status, statusText, headers, body? }` | The error response |
| `errors` | `ErrorEntity[]` | Parsed error entities from the response body |

**`findError(codeOrCodes, filterDetails?)` method:**

```ts
// Find by single error code
const err = error.findError("VALIDATION_UNIQUE");

// Find by multiple codes
const err = error.findError(["VALIDATION_UNIQUE", "VALIDATION_REQUIRED"]);

// Find with detail filter (object)
const err = error.findError("INVALID_FIELD", { field: "title" });

// Find with detail filter (function)
const err = error.findError("INVALID_FIELD", (details) => details.field === "title");
```

Each `ErrorEntity` has this shape:

```ts
{
  id: string;
  type: "api_error";
  attributes: {
    code: string;          // e.g., "VALIDATION_UNIQUE"
    transient?: true;      // Present if the error is transient
    doc_url: string;       // Link to documentation
    details: Record<string, unknown>;
  };
}
```

### `TimeoutError`

Thrown when a request exceeds `requestTimeout` and `autoRetry` is `false` (or retries are exhausted).

```ts
import { TimeoutError } from "@datocms/cma-client-node";

try {
  await client.items.list();
} catch (error) {
  if (error instanceof TimeoutError) {
    console.log("Request timed out:", error.request.url);
  }
}
```

---

## Automatic Behaviors

### Rate Limit Retry

When `autoRetry` is `true` (the default), the client automatically retries 429 (Too Many Requests) responses with linear incremental backoff. **Do not add your own retry logic for rate limits.**

### Transient Error Retry

Transient server errors (5xx with `transient: true` in the error entity) are also auto-retried when `autoRetry` is enabled.

### Async Job Polling

Some operations return a 202 (Accepted) response with a job ID instead of the final result. The client automatically polls `client.jobResults.find()` until the job completes and returns the final result.

Operations that use async jobs include: `environments.fork()`, `environments.destroy()`, `itemTypes.update()`, `itemTypes.destroy()`, `fields.create()`, `fields.update()`, `fields.destroy()`, `items.duplicate()`, and all bulk operations (`bulkPublish`, `bulkUnpublish`, `bulkDestroy`, `bulkMoveToStage`).

**Do not manually poll `client.jobResults`.** The client handles this transparently.

---

## Technical Limits

| Limit | Value |
|---|---|
| Max record size | 300 KB (including nested blocks; excludes assets and linked records) |
| Max blocks per record | 600 |
| Max nested block depth | 5 levels |
| Max upload size | 1 GB per asset |
| Rate limit | 60 requests per 3 seconds (auto-retried when `autoRetry` is enabled) |
| Bulk operation batch | 200 items per request (`bulkPublish`, `bulkDestroy`, etc.) |

Exceeding these triggers `TECHNICAL_LIMIT_REACHED` or `TOO_MANY_OPERATIONS` errors.

---

## Getting Site Information

To get site-level settings (locales, timezone, etc.):

```ts
const site = await client.site.find();
console.log(site.locales); // ["en", "it", "de"]
console.log(site.name);    // "My DatoCMS Project"
```

This is useful for determining available locales before working with localized content.
