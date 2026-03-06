# Scheduling and Workflows

Covers scheduled publication/unpublication and workflow management.

---

## Scheduled Publication

Schedule a record to be published at a future date and time.

### Create a Scheduled Publication

```ts
await client.scheduledPublication.create("record-id", {
  publication_scheduled_at: "2024-12-25T09:00:00+00:00",
});
```

The `publication_scheduled_at` value must be an ISO 8601 datetime string in the future.

### Selective Publication (Specific Locales)

Publish only certain locales at the scheduled time:

```ts
await client.scheduledPublication.create("record-id", {
  publication_scheduled_at: "2024-12-25T09:00:00+00:00",
  selective_publication: {
    content_in_locales: ["en", "fr"],
    non_localized_content: true,
  },
});
```

| Option | Type | Description |
|---|---|---|
| `content_in_locales` | `string[]` | Locales to publish |
| `non_localized_content` | `boolean` | Whether to also publish non-localized fields |

### Cancel a Scheduled Publication

```ts
await client.scheduledPublication.destroy("record-id");
```

---

## Scheduled Unpublishing

Schedule a record to be unpublished at a future date and time.

### Create a Scheduled Unpublishing

```ts
await client.scheduledUnpublishing.create("record-id", {
  unpublishing_scheduled_at: "2025-01-31T23:59:00+00:00",
});
```

### Selective Unpublishing (Specific Locales)

Unpublish only certain locales at the scheduled time:

```ts
await client.scheduledUnpublishing.create("record-id", {
  unpublishing_scheduled_at: "2025-01-31T23:59:00+00:00",
  content_in_locales: ["en", "fr"],
});
```

When `content_in_locales` is `null` or omitted, the entire record is unpublished.

### Cancel a Scheduled Unpublishing

```ts
await client.scheduledUnpublishing.destroy("record-id");
```

---

## Combining Publish and Unpublish Schedules

You can schedule both publication and unpublication for the same record, creating a time-limited visibility window:

```ts
// Publish on Christmas
await client.scheduledPublication.create("promo-record-id", {
  publication_scheduled_at: "2024-12-25T00:00:00+00:00",
});

// Unpublish on New Year's
await client.scheduledUnpublishing.create("promo-record-id", {
  unpublishing_scheduled_at: "2025-01-01T00:00:00+00:00",
});
```

---

## Workflows

Workflows define a sequence of stages that records must pass through before publishing (e.g., Draft → Review → Approved → Published).

### Creating a Workflow

```ts
const workflow = await client.workflows.create({
  name: "Editorial Review",
  api_key: "editorial_review",
  stages: [
    { id: "draft", name: "Draft", description: "Initial content creation", initial: true },
    { id: "review", name: "In Review", description: "Pending editorial review", initial: false },
    { id: "approved", name: "Approved", description: "Ready for publication", initial: false },
  ],
});
```

### Assigning a Workflow to a Model

When creating or updating a model, associate a workflow:

```ts
await client.itemTypes.update(model.id, {
  workflow: { id: workflow.id, type: "workflow" },
});
```

### Moving a Record Between Stages

Use bulk move to stage (even for a single record):

```ts
await client.items.bulkMoveToStage({
  items: [{ id: "record-id", type: "item" }],
  stage: "review",
});
```

### Listing Workflows

```ts
const workflows = await client.workflows.list();

for (const workflow of workflows) {
  console.log(workflow.name, workflow.stages);
}
```

### Finding, Updating, Deleting Workflows

```ts
// Find by ID
const workflow = await client.workflows.find("workflow-id");

// Update
await client.workflows.update("workflow-id", {
  name: "Updated Workflow",
  stages: [
    { id: "draft", name: "Draft", description: "", initial: true },
    { id: "review", name: "Peer Review", description: "", initial: false },
    { id: "legal", name: "Legal Review", description: "", initial: false },
    { id: "approved", name: "Ready to Publish", description: "", initial: false },
  ],
});

// Delete
await client.workflows.destroy("workflow-id");
```

---

## Complete Example: Set Up Editorial Workflow

```ts
import { buildClient } from "@datocms/cma-client-node";

const client = buildClient({
  apiToken: process.env.DATOCMS_API_TOKEN!,
});

async function setupEditorialWorkflow() {
  // Create the workflow
  const workflow = await client.workflows.create({
    name: "Editorial",
    api_key: "editorial",
    stages: [
      { id: "draft", name: "Draft", description: "Initial content creation", initial: true },
      { id: "review", name: "Editorial Review", description: "Pending editorial review", initial: false },
      { id: "approved", name: "Approved", description: "Ready for publication", initial: false },
    ],
  });

  // Get the blog post model
  const models = await client.itemTypes.list();
  const blogModel = models.find((m) => m.api_key === "blog_post");
  if (!blogModel) throw new Error("blog_post model not found");

  // Assign the workflow to the model
  await client.itemTypes.update(blogModel.id, {
    workflow: { id: workflow.id, type: "workflow" },
  });

  console.log("Editorial workflow configured for blog posts");

  // Create a record in draft stage
  const record = await client.items.create({
    item_type: { id: blogModel.id, type: "item_type" },
    title: "New Blog Post",
    slug: "new-blog-post",
  });

  // Move it to review
  await client.items.bulkMoveToStage({
    items: [{ id: record.id, type: "item" }],
    stage: "review",
  });

  console.log("Record moved to review stage");
}

setupEditorialWorkflow().catch(console.error);
```
