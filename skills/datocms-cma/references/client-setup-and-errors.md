# Client Setup and Error Handling

This reference is always loaded. It covers package selection, `buildClient()` setup, token and environment configuration, and the error types you should handle in most CMA scripts.

## Quick Navigation

- [Package Selection](#package-selection)
- [Building the Client](#building-the-client)
- [Common Resources](#common-resources)
- [Error Handling](#error-handling)

---

## Package Selection

| Package | Runtime | When to use |
|---|---|---|
| `@datocms/cma-client` | Universal | Recommended for most cases. Works anywhere with native `fetch`. Only provide `fetchFn` if the runtime lacks it. |
| `@datocms/cma-client-node` | Node.js | Use when you need Node.js upload helpers such as `createFromLocalFile()` or `createFromUrl()`. |
| `@datocms/cma-client-browser` | Browser | Use when you need browser upload helpers such as `createFromFileOrBlob()`. |

All three packages expose the same core CMA resources. The main differences are the environment-specific upload convenience methods.

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

### Common `ClientConfigOptions`

| Option | Type | Default | Description |
|---|---|---|---|
| `apiToken` | `string \| null` | — | Required. Use a CMA-capable token with the permissions your task needs. |
| `environment` | `string` | — | Targets a sandbox environment. Omit to use the primary environment. |
| `requestTimeout` | `number` | `30000` | Timeout in milliseconds per request. |
| `autoRetry` | `boolean` | `true` | Retries rate limits and transient server failures automatically. |
| `logLevel` | `LogLevel` | `LogLevel.NONE` | Logging verbosity. |
| `logFn` | `(message: string) => void` | `console.log` | Custom log function. |
| `extraHeaders` | `Record<string, string>` | — | Additional headers for every request. |
| `fetchFn` | `typeof fetch` | — | Custom fetch implementation for runtimes without native fetch. |

**Token guidance:**

- CMA operations require `can_access_cma: true`
- Schema changes require a role with `can_edit_schema: true`
- Public browser tokens or read-only CDA tokens are not sufficient for CMA writes

---

## Common Resources

| Resource | Property | Common operations |
|---|---|---|
| Records | `client.items` | CRUD, publish, unpublish, bulk operations |
| Uploads | `client.uploads` | CRUD, bulk tag/destroy, references |
| Models | `client.itemTypes` | CRUD, duplicate, referencing |
| Fields | `client.fields` | CRUD, duplicate, referencing |
| Environments | `client.environments` | Fork, promote, rename, destroy |
| Webhooks | `client.webhooks` | CRUD |
| Build triggers | `client.buildTriggers` | CRUD, trigger, abort |
| Roles | `client.roles` | CRUD, duplicate |
| API tokens | `client.accessTokens` | CRUD, regenerate |
| Workflows | `client.workflows` | CRUD |
| Site | `client.site` | Find site settings such as locales |

The client also exposes resources for record versions, webhook calls, audit logs, SSO, search indexes, plugins, maintenance mode, and more.

---

## Error Handling

### `ApiError`

Thrown when the API returns a non-2xx response other than rate limits that are retried automatically.

```ts
import { ApiError } from "@datocms/cma-client-node";

try {
  await client.items.create({
    item_type: { id: "model_123", type: "item_type" },
    title: "Hello",
  });
} catch (error) {
  if (error instanceof ApiError) {
    console.log(error.response.status);
    console.log(error.errors);

    const uniqueError = error.findError("VALIDATION_UNIQUE");
    if (uniqueError) {
      console.log(uniqueError.attributes.details);
    }
  }
  throw error;
}
```

**Useful `ApiError` members:**

| Property | Type | Description |
|---|---|---|
| `request` | `{ url, method, headers, body? }` | The failed request |
| `response` | `{ status, statusText, headers, body? }` | The API response |
| `errors` | `ErrorEntity[]` | Parsed DatoCMS error entities |
| `findError()` | method | Finds errors by code and optional detail filters |

### `TimeoutError`

Thrown when a request exceeds `requestTimeout` and retries do not recover.

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
