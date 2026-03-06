# Access Control

Covers roles, API tokens, users, and invitations.

---

## Roles

Roles define what users and API tokens can do. DatoCMS uses a **positive/negative permission model** — you grant permissions explicitly.

### Creating a Role

```ts
const role = await client.roles.create({
  name: "Content Editor",
  // Administrative permissions (all boolean, all default false)
  can_edit_favicon: false,
  can_edit_site: false,
  can_edit_schema: false,
  can_manage_menu: false,
  can_edit_environment: false,
  can_promote_environments: false,
  can_manage_environments: false,
  can_manage_users: false,
  can_manage_shared_filters: true,
  can_manage_build_triggers: false,
  can_manage_webhooks: false,
  can_manage_upload_collections: true,
  can_manage_search_indexes: false,
  can_manage_sso: false,
  can_manage_workflows: false,
  can_manage_access_tokens: false,
  can_access_audit_log: false,
  can_access_build_events_log: false,
  can_access_search_index_events_log: false,
  can_perform_site_search: false,
  // Environment access
  environments_access: "primary_only",
  // Per-model permissions
  positive_item_type_permissions: [
    {
      environment: "main",
      item_type: "model_123",
      action: "all",
      localization_scope: null,
    },
  ],
  negative_item_type_permissions: [],
  // Per-upload permissions
  positive_upload_permissions: [
    { environment: "main", action: "all" },
  ],
  negative_upload_permissions: [],
});
```

### Environment Access Levels

| Value | Description |
|---|---|
| `"all"` | Access all environments |
| `"primary_only"` | Access only the primary environment |
| `"sandbox_only"` | Access only sandbox environments |
| `"none"` | No environment access |

### Item Type Permissions

Positive permissions grant access; negative permissions revoke access (for exceptions).

```ts
// Grant full access to blog_post model
positive_item_type_permissions: [
  {
    environment: "main",
    item_type: blogModelId,
    action: "all",
    localization_scope: null,
  },
]

// Grant read-only access
positive_item_type_permissions: [
  {
    environment: "main",
    item_type: blogModelId,
    action: "read",
    localization_scope: null,
  },
]
```

Available `action` values:
- `"all"` — Full CRUD + publish
- `"read"` — Read only
- `"create"` — Create records
- `"update"` — Update records
- `"duplicate"` — Duplicate records
- `"delete"` — Delete records
- `"publish"` — Publish/unpublish records
- `"edit_creator"` — Change the creator of a record
- `"take_over"` — Take over editing from another user
- `"move_to_stage"` — Move records between workflow stages (use with `on_stage`/`to_stage`)

The `localization_scope` field controls which content the permission covers:
- `null` — All content (default)
- `"all"` — All locales
- `"localized"` — Only localized fields (combine with `locale` to target a specific locale)
- `"not_localized"` — Only non-localized fields

### Upload Permissions

```ts
positive_upload_permissions: [
  { environment: "main", action: "all" },
]

// Or more granular:
positive_upload_permissions: [
  { environment: "main", action: "read" },
  { environment: "main", action: "create" },
  { environment: "main", action: "update" },
  { environment: "main", action: "delete" },
]
```

Available upload `action` values: `"all"`, `"read"`, `"create"`, `"update"`, `"delete"`, `"edit_creator"`, `"replace_asset"`, `"move"`

### Role Inheritance

A role can inherit permissions from another role:

```ts
const advancedEditor = await client.roles.create({
  name: "Advanced Editor",
  inherits_permissions_from: [{ id: baseEditorRoleId, type: "role" }],
  // Additional permissions on top of inherited ones
  can_manage_shared_filters: true,
});
```

### Listing, Finding, Updating, Deleting Roles

```ts
// List all roles
const roles = await client.roles.list();

// Find by ID
const role = await client.roles.find("role-id");

// Duplicate a role
const duplicated = await client.roles.duplicate("role-id");

// Update
await client.roles.update("role-id", {
  name: "Renamed Role",
  can_manage_shared_filters: true,
});

// Delete
await client.roles.destroy("role-id");
```

---

## API Tokens

API tokens authenticate API requests and are each associated with a single role (or `null`).

### Creating an API Token

```ts
const token = await client.accessTokens.create({
  name: "CI/CD Token",
  role: { id: roleId, type: "role" },
  can_access_cda: true,
  can_access_cda_preview: true,
  can_access_cma: true,
});

console.log("Token:", token.token); // Only shown once!
```

**Important:** The `token` value is only returned when creating or regenerating a token. In list/find responses, the `token` field is `null`. Store the token securely at creation time.

### Token Attributes

| Attribute | Type | Description |
|---|---|---|
| `name` | `string` | **Required.** Display name |
| `role` | `{ id, type: "role" }` | **Required.** Associated role |
| `can_access_cda` | `boolean` | Access to Content Delivery API |
| `can_access_cda_preview` | `boolean` | Access to CDA preview endpoint |
| `can_access_cma` | `boolean` | Access to Content Management API |

### Listing, Finding, Updating Tokens

```ts
// List all tokens
const tokens = await client.accessTokens.list();

// Find by ID
const token = await client.accessTokens.find("token-id");

// Update (change name, role, etc.)
await client.accessTokens.update("token-id", {
  name: "Updated Name",
});

// Regenerate the token value
const regenerated = await client.accessTokens.regenerateToken("token-id");
console.log("New token:", regenerated.token);

// Delete
await client.accessTokens.destroy("token-id");
```

---

## Users

Manage collaborators on the DatoCMS project.

### Listing Users

```ts
const users = await client.users.list();

for (const user of users) {
  console.log(user.email, user.role?.id);
}
```

### Finding a User

```ts
const user = await client.users.find("user-id");
```

### Updating a User's Role

```ts
await client.users.update("user-id", {
  role: { id: newRoleId, type: "role" },
});
```

### Removing a User

```ts
await client.users.destroy("user-id");
```

---

## Site Invitations

Invite new collaborators to the project.

### Creating an Invitation

```ts
const invitation = await client.siteInvitations.create({
  email: "newuser@example.com",
  role: { id: roleId, type: "role" },
});
```

### Listing, Deleting Invitations

```ts
const invitations = await client.siteInvitations.list();

// Cancel an invitation
await client.siteInvitations.destroy("invitation-id");
```

---

## SSO Users and Groups

For projects using Single Sign-On.

### SSO Users

```ts
// List SSO users
const ssoUsers = await client.ssoUsers.list();

// Find SSO user
const user = await client.ssoUsers.find("sso-user-id");

// Copy existing editors as SSO users
await client.ssoUsers.copyUsers();

// Remove SSO user
await client.ssoUsers.destroy("sso-user-id");
```

**Note:** SSO users cannot be updated directly — their attributes are managed by the identity provider. Use `copyUsers()` to import existing project editors as SSO users.

### SSO Groups

SSO groups are provisioned from the identity provider, not created individually. Use `copyRoles()` to sync groups from the IdP.

```ts
// List SSO groups
const groups = await client.ssoGroups.list();

// Sync roles from identity provider for a specific group
await client.ssoGroups.copyRoles("group-id");

// Update a group's role assignment
await client.ssoGroups.update("group-id", {
  role: { id: roleId, type: "role" },
  priority: 1,
});

// Delete
await client.ssoGroups.destroy("group-id");
```

### SSO Settings

```ts
// Get SSO settings
const settings = await client.ssoSettings.find();

// Update SSO settings
await client.ssoSettings.update({
  default_role: { id: roleId, type: "role" },
});
```

---

## Complete Example: Set Up a Content Editor Role with Token

```ts
import { buildClient } from "@datocms/cma-client-node";

const client = buildClient({
  apiToken: process.env.DATOCMS_API_TOKEN!,
});

async function setupEditorAccess() {
  // Get the blog_post model ID
  const models = await client.itemTypes.list();
  const blogModel = models.find((m) => m.api_key === "blog_post");
  if (!blogModel) throw new Error("blog_post model not found");

  // Create a role that can manage blog posts and uploads
  const role = await client.roles.create({
    name: "Blog Editor",
    can_edit_schema: false,
    can_edit_site: false,
    can_manage_users: false,
    can_manage_build_triggers: false,
    can_manage_webhooks: false,
    environments_access: "primary_only",
    positive_item_type_permissions: [
      {
        environment: "main",
        item_type: blogModel.id,
        action: "all",
        localization_scope: null,
      },
    ],
    negative_item_type_permissions: [],
    positive_upload_permissions: [{ environment: "main", action: "all" }],
    negative_upload_permissions: [],
  });

  // Create an API token with this role
  const token = await client.accessTokens.create({
    name: "Blog Editor Token",
    role: { id: role.id, type: "role" },
    can_access_cda: true,
    can_access_cda_preview: true,
    can_access_cma: true,
  });

  console.log("Role created:", role.id);
  console.log("API Token (save this!):", token.token);
}

setupEditorAccess().catch(console.error);
```
