# Environments

Covers sandbox environment management: listing, forking, promoting, renaming, and deleting environments.

## Quick Navigation

- [Overview](#overview)
- [Listing Environments](#listing-environments)
- [Finding an Environment](#finding-an-environment)
- [Forking (Creating a Sandbox)](#forking-creating-a-sandbox)
- [Promoting a Sandbox](#promoting-a-sandbox)
- [Renaming an Environment](#renaming-an-environment)
- [Deleting an Environment](#deleting-an-environment)
- [Environment-Aware Client](#environment-aware-client)
- [CI/CD Pattern: Fork → Migrate → Promote](#cicd-pattern-fork--migrate--promote)

---

## Overview

DatoCMS environments provide isolated copies of your schema and content. The **primary** environment is the production environment. **Sandbox** environments are forks you can experiment with safely.

Common workflow:
1. Fork the primary environment → create a sandbox
2. Make schema/content changes in the sandbox
3. Promote the sandbox → it becomes the new primary

---

## Listing Environments

```ts
const environments = await client.environments.list();

for (const env of environments) {
  console.log(env.id, env.meta.primary ? "(primary)" : "(sandbox)");
}
```

### Identifying Primary vs Sandbox

```ts
const environments = await client.environments.list();
const primary = environments.find((e) => e.meta.primary);
const sandboxes = environments.filter((e) => !e.meta.primary);
```

---

## Finding an Environment

```ts
const env = await client.environments.find("my-sandbox");
console.log(env.id, env.meta.status); // "ready", "creating", etc.
```

---

## Forking (Creating a Sandbox)

Fork the primary environment to create a sandbox:

```ts
const sandbox = await client.environments.fork("main", {
  id: "my-feature-branch",
});

console.log("Sandbox created:", sandbox.id);
```

The first argument is the source environment ID (usually the primary). The second argument specifies the new sandbox ID.

### Fork Options

The third argument accepts query parameters to control fork behavior:

```ts
const sandbox = await client.environments.fork(
  "main",
  { id: "my-feature-branch" },
  { fast: true, force: true },
);
```

| Option | Type | Default | Description |
|---|---|---|---|
| `fast` | `boolean` | `false` | Faster fork, but prevents writes to the source environment during the process |
| `force` | `boolean` | `false` | Force the fork even if collaborators are actively editing records |
| `immediate_return` | `boolean` | `false` | Return immediately instead of waiting for the fork to complete |

**Important:** Forking is an async job. By default the client automatically waits for the fork to complete before returning (unless `immediate_return: true`).

---

## Promoting a Sandbox

Promote a sandbox to make it the new primary environment:

```ts
await client.environments.promote("my-feature-branch");
```

After promotion:
- The sandbox becomes the primary environment
- The old primary is demoted to a sandbox
- All API tokens targeting the primary now point to the promoted environment

**Important:** This is an irreversible operation in practice. Always verify the sandbox content before promoting.

---

## Renaming an Environment

```ts
await client.environments.rename("old-name", {
  id: "new-name",
});
```

---

## Deleting an Environment

```ts
await client.environments.destroy("my-sandbox");
```

**Important:** This is an async job and permanently deletes all schema and content in the environment.

---

## Environment-Aware Client

To target a specific environment with all API calls:

```ts
import { buildClient } from "@datocms/cma-client-node";

const sandboxClient = buildClient({
  apiToken: process.env.DATOCMS_API_TOKEN!,
  environment: "my-sandbox",
});

// All operations now target the sandbox
const records = await sandboxClient.items.list({
  filter: { type: "blog_post" },
});
```

---

## CI/CD Pattern: Fork → Migrate → Promote

A common pattern for deploying schema changes through CI/CD:

```ts
import { buildClient, ApiError } from "@datocms/cma-client-node";

async function deployMigration() {
  const primaryClient = buildClient({
    apiToken: process.env.DATOCMS_API_TOKEN!,
  });

  const sandboxId = `migration-${Date.now()}`;

  // Step 1: Fork the primary environment
  console.log("Forking primary environment...");
  await primaryClient.environments.fork("main", { id: sandboxId });

  // Step 2: Apply migrations to the sandbox
  const sandboxClient = buildClient({
    apiToken: process.env.DATOCMS_API_TOKEN!,
    environment: sandboxId,
  });

  console.log("Applying migrations...");
  // ... perform schema changes, data migrations, etc.
  await sandboxClient.fields.create("model-id", {
    label: "New Field",
    api_key: "new_field",
    field_type: "string",
  });

  // Step 3: Promote the sandbox
  console.log("Promoting sandbox to primary...");
  await primaryClient.environments.promote(sandboxId);

  console.log("Migration complete!");
}

deployMigration().catch((error) => {
  if (error instanceof ApiError) {
    console.error("Migration failed:", error.response.status, error.errors);
  } else {
    console.error(error);
  }
  process.exit(1);
});
```
