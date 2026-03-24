# Access Control

Covers roles, API tokens, users, and invitations.

## Quick Navigation

- [Roles](#roles)
- [API Tokens](#api-tokens)
- [Users](#users)
- [Site Invitations](#site-invitations)
- [SSO Users and Groups](#sso-users-and-groups)
- [Complete Example: Set Up a Content Editor Role with Token](#complete-example-set-up-a-content-editor-role-with-token)

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

### Resending an Invitation

```ts
await client.siteInvitations.resend("invitation-id");
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

## Type Reference

**Import:** `import type { ApiTypes } from "@datocms/cma-client-node";`

Type properties are based on `@datocms/cma-client@5.x`. Properties may differ on other versions.

### Permission Object Shapes

The four permission arrays on roles (`positive_item_type_permissions`, `negative_item_type_permissions`, `positive_upload_permissions`, `negative_upload_permissions`) share a common shape. They are documented here once to avoid repetition.

#### Item Type Permission Object

Used in `positive_item_type_permissions` and `negative_item_type_permissions`.

| Field | Type | Description |
|---|---|---|
| `item_type` | `string \| null` (optional) | Model ID to scope to, or `null` for all models |
| `workflow` | `string \| null` (optional) | Workflow ID to scope to, or `null` for any workflow |
| `on_stage` | `string \| null` (optional) | Workflow stage the record must be on |
| `to_stage` | `string \| null` (optional) | Target workflow stage (for `move_to_stage` action) |
| `environment` | `string` | Environment ID this permission applies to |
| `action` | `"all" \| "read" \| "update" \| "create" \| "duplicate" \| "delete" \| "publish" \| "edit_creator" \| "take_over" \| "move_to_stage"` | Permitted action |
| `on_creator` | `"anyone" \| "self" \| "role" \| null` (optional) | Restrict to records by a certain creator |
| `localization_scope` | `"all" \| "localized" \| "not_localized" \| null` (optional) | Content scope for the permission |
| `locale` | `string \| null` (optional) | Specific locale (required when `localization_scope` is `"localized"`) |

#### Upload Permission Object

Used in `positive_upload_permissions` and `negative_upload_permissions`.

| Field | Type | Description |
|---|---|---|
| `environment` | `string` | Environment ID this permission applies to |
| `action` | `"all" \| "read" \| "update" \| "create" \| "delete" \| "edit_creator" \| "replace_asset"` | Permitted action |
| `on_creator` | `"anyone" \| "self" \| "role" \| null` (optional) | Restrict to uploads by a certain creator |
| `localization_scope` | `"all" \| "localized" \| "not_localized" \| null` (optional) | Content scope for the permission |
| `locale` | `string \| null` (optional) | Specific locale (required when `localization_scope` is `"localized"`) |

#### Build Trigger Permission Object

Used in `positive_build_trigger_permissions` and `negative_build_trigger_permissions`.

| Field | Type | Description |
|---|---|---|
| `build_trigger` | `string \| null` (optional) | Build trigger ID, or `null` for all triggers |

---

### `ApiTypes.Role`

Returned by `list()`, `find()`, `create()`, `update()`, `duplicate()`, and `destroy()`.

| Field | Type | Description |
|---|---|---|
| `id` | `string` | Role ID |
| `type` | `"role"` | JSON API resource type |
| `name` | `string` | The name of the role |
| `can_edit_favicon` | `boolean` | Can edit favicon, global SEO settings, and no-index policy |
| `can_edit_site` | `boolean` | Can change project global properties |
| `can_edit_schema` | `boolean` | Can create/edit models and plugins |
| `can_manage_menu` | `boolean` | Can customize content navigation bar |
| `can_edit_environment` | `boolean` | Can change locales, timezone, and UI theme |
| `can_promote_environments` | `boolean` | Can promote environments to primary and manage maintenance mode |
| `environments_access` | `"all" \| "primary_only" \| "sandbox_only" \| "none"` | Which environments the role can access |
| `can_manage_users` | `boolean` | Can create/edit roles and invite/remove collaborators |
| `can_manage_shared_filters` | `boolean` | Can create/edit shared filters |
| `can_manage_upload_collections` | `boolean` | Can create/edit upload collections |
| `can_manage_build_triggers` | `boolean` | Can create/edit build triggers |
| `can_manage_webhooks` | `boolean` | Can create/edit webhooks |
| `can_manage_environments` | `boolean` | Can create/delete sandbox environments and promote them |
| `can_manage_sso` | `boolean` | Can manage Single Sign-On settings |
| `can_access_audit_log` | `boolean` | Can access audit log |
| `can_manage_workflows` | `boolean` | Can create/edit workflows |
| `can_manage_access_tokens` | `boolean` | Can manage API tokens |
| `can_perform_site_search` | `boolean` | Can perform Site Search API calls |
| `can_access_build_events_log` | `boolean` | Can access the build events log |
| `positive_item_type_permissions` | [Item Type Permission Object](#item-type-permission-object)`[]` | Allowed actions on models |
| `negative_item_type_permissions` | [Item Type Permission Object](#item-type-permission-object)`[]` | Prohibited actions on models |
| `positive_upload_permissions` | [Upload Permission Object](#upload-permission-object)`[]` | Allowed actions on uploads |
| `negative_upload_permissions` | [Upload Permission Object](#upload-permission-object)`[]` | Prohibited actions on uploads |
| `positive_build_trigger_permissions` | [Build Trigger Permission Object](#build-trigger-permission-object)`[]` | Allowed build triggers |
| `negative_build_trigger_permissions` | [Build Trigger Permission Object](#build-trigger-permission-object)`[]` | Prohibited build triggers |
| `inherits_permissions_from` | `{ id: string; type: "role" }[]` | Roles this role inherits permissions from |
| `meta.final_permissions` | `object` | The computed final set of permissions (same shape as the role's own permission fields, including inherited ones) |

### `ApiTypes.RoleCreateSchema`

Input for `client.roles.create()`.

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | `string` | **Yes** | The name of the role |
| `can_edit_favicon` | `boolean` | No | Can edit favicon, global SEO settings, and no-index policy |
| `can_edit_site` | `boolean` | No | Can change project global properties |
| `can_edit_schema` | `boolean` | No | Can create/edit models and plugins |
| `can_manage_menu` | `boolean` | No | Can customize content navigation bar |
| `can_edit_environment` | `boolean` | No | Can change locales, timezone, and UI theme |
| `can_promote_environments` | `boolean` | No | Can promote environments to primary and manage maintenance mode |
| `environments_access` | `"all" \| "primary_only" \| "sandbox_only" \| "none"` | No | Which environments the role can access |
| `can_manage_users` | `boolean` | No | Can create/edit roles and invite/remove collaborators |
| `can_manage_shared_filters` | `boolean` | No | Can create/edit shared filters |
| `can_manage_upload_collections` | `boolean` | No | Can create/edit upload collections |
| `can_manage_build_triggers` | `boolean` | No | Can create/edit build triggers |
| `can_manage_webhooks` | `boolean` | No | Can create/edit webhooks |
| `can_manage_environments` | `boolean` | No | Can create/delete sandbox environments and promote them |
| `can_manage_sso` | `boolean` | No | Can manage Single Sign-On settings |
| `can_access_audit_log` | `boolean` | No | Can access audit log |
| `can_manage_workflows` | `boolean` | No | Can create/edit workflows |
| `can_manage_access_tokens` | `boolean` | No | Can manage API tokens |
| `can_perform_site_search` | `boolean` | No | Can perform Site Search API calls |
| `can_access_build_events_log` | `boolean` | No | Can access the build events log |
| `positive_item_type_permissions` | [Item Type Permission Object](#item-type-permission-object)`[]` | No | Allowed actions on models |
| `negative_item_type_permissions` | [Item Type Permission Object](#item-type-permission-object)`[]` | No | Prohibited actions on models |
| `positive_upload_permissions` | [Upload Permission Object](#upload-permission-object)`[]` | No | Allowed actions on uploads |
| `negative_upload_permissions` | [Upload Permission Object](#upload-permission-object)`[]` | No | Prohibited actions on uploads |
| `positive_build_trigger_permissions` | [Build Trigger Permission Object](#build-trigger-permission-object)`[]` | No | Allowed build triggers |
| `negative_build_trigger_permissions` | [Build Trigger Permission Object](#build-trigger-permission-object)`[]` | No | Prohibited build triggers |
| `inherits_permissions_from` | `{ id: string; type: "role" }[]` | No | Roles this role inherits permissions from |

### `ApiTypes.RoleUpdateSchema`

Input for `client.roles.update()`. All fields are optional.

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | `string` | No | The name of the role |
| `can_edit_favicon` | `boolean` | No | Can edit favicon, global SEO settings, and no-index policy |
| `can_edit_site` | `boolean` | No | Can change project global properties |
| `can_edit_schema` | `boolean` | No | Can create/edit models and plugins |
| `can_manage_menu` | `boolean` | No | Can customize content navigation bar |
| `can_edit_environment` | `boolean` | No | Can change locales, timezone, and UI theme |
| `can_promote_environments` | `boolean` | No | Can promote environments to primary and manage maintenance mode |
| `environments_access` | `"all" \| "primary_only" \| "sandbox_only" \| "none"` | No | Which environments the role can access |
| `can_manage_users` | `boolean` | No | Can create/edit roles and invite/remove collaborators |
| `can_manage_shared_filters` | `boolean` | No | Can create/edit shared filters |
| `can_manage_upload_collections` | `boolean` | No | Can create/edit upload collections |
| `can_manage_build_triggers` | `boolean` | No | Can create/edit build triggers |
| `can_manage_webhooks` | `boolean` | No | Can create/edit webhooks |
| `can_manage_environments` | `boolean` | No | Can create/delete sandbox environments and promote them |
| `can_manage_sso` | `boolean` | No | Can manage Single Sign-On settings |
| `can_access_audit_log` | `boolean` | No | Can access audit log |
| `can_manage_workflows` | `boolean` | No | Can create/edit workflows |
| `can_manage_access_tokens` | `boolean` | No | Can manage API tokens |
| `can_perform_site_search` | `boolean` | No | Can perform Site Search API calls |
| `can_access_build_events_log` | `boolean` | No | Can access the build events log |
| `positive_item_type_permissions` | [Item Type Permission Object](#item-type-permission-object)`[]` | No | Allowed actions on models |
| `negative_item_type_permissions` | [Item Type Permission Object](#item-type-permission-object)`[]` | No | Prohibited actions on models |
| `positive_upload_permissions` | [Upload Permission Object](#upload-permission-object)`[]` | No | Allowed actions on uploads |
| `negative_upload_permissions` | [Upload Permission Object](#upload-permission-object)`[]` | No | Prohibited actions on uploads |
| `positive_build_trigger_permissions` | [Build Trigger Permission Object](#build-trigger-permission-object)`[]` | No | Allowed build triggers |
| `negative_build_trigger_permissions` | [Build Trigger Permission Object](#build-trigger-permission-object)`[]` | No | Prohibited build triggers |
| `inherits_permissions_from` | `{ id: string; type: "role" }[]` | No | Roles this role inherits permissions from |

---

### `ApiTypes.AccessToken`

Returned by `list()`, `find()`, `create()`, `update()`, `regenerateToken()`, and `destroy()`.

| Field | Type | Description |
|---|---|---|
| `id` | `string` | API token ID |
| `type` | `"access_token"` | JSON API resource type |
| `name` | `string` | Name of the API token |
| `token` | `string \| null` (optional) | The actual API token value. Only returned on create/regenerate; `null` otherwise |
| `can_access_cda` | `boolean` | Whether this token can access the Content Delivery API published content endpoint |
| `can_access_cda_preview` | `boolean` | Whether this token can access the Content Delivery API draft content endpoint |
| `can_access_cma` | `boolean` | Whether this token can access the Content Management API |
| `hardcoded_type` | `string \| null` | Internal token type identifier |
| `role` | `{ id: string; type: "role" } \| null` | Associated role |

### `ApiTypes.AccessTokenCreateSchema`

Input for `client.accessTokens.create()`.

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | `string` | **Yes** | Name of the API token |
| `can_access_cda` | `boolean` | **Yes** | Whether this token can access the Content Delivery API published content endpoint |
| `can_access_cda_preview` | `boolean` | **Yes** | Whether this token can access the Content Delivery API draft content endpoint |
| `can_access_cma` | `boolean` | **Yes** | Whether this token can access the Content Management API |
| `role` | `{ id: string; type: "role" } \| null` | **Yes** | Associated role |

### `ApiTypes.AccessTokenUpdateSchema`

Input for `client.accessTokens.update()`.

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | `string` | **Yes** | Name of the API token |
| `can_access_cda` | `boolean` | **Yes** | Whether this token can access the Content Delivery API published content endpoint |
| `can_access_cda_preview` | `boolean` | **Yes** | Whether this token can access the Content Delivery API draft content endpoint |
| `can_access_cma` | `boolean` | **Yes** | Whether this token can access the Content Management API |
| `role` | `{ id: string; type: "role" } \| null` | **Yes** | Associated role |

---

### `ApiTypes.User`

Returned by `list()`, `find()`, `update()`, and `destroy()`.

| Field | Type | Description |
|---|---|---|
| `id` | `string` | User ID |
| `type` | `"user"` | JSON API resource type |
| `email` | `string` | User email address |
| `is_2fa_active` | `boolean` | Whether 2-factor authentication is active |
| `full_name` | `string` | Full name |
| `is_active` | `boolean` | Whether the user is active |
| `role` | `{ id: string; type: "role" }` | Associated role |
| `meta.last_access` | `string \| null` (optional) | Date of last reading/interaction |

### `ApiTypes.UserUpdateSchema`

Input for `client.users.update()`.

| Field | Type | Required | Description |
|---|---|---|---|
| `is_active` | `boolean` | No | Whether the user is active |
| `role` | `{ id: string; type: "role" }` | No | Associated role |

---

### `ApiTypes.SiteInvitation`

Returned by `list()`, `find()`, `create()`, `update()`, `destroy()`, and `resend()`.

| Field | Type | Description |
|---|---|---|
| `id` | `string` | Invitation ID |
| `type` | `"site_invitation"` | JSON API resource type |
| `email` | `string` | Invitee email address |
| `expired` | `boolean` | Whether this invitation has expired |
| `invitation_link` | `string \| null` (optional) | The link to join the project. Only shown on creation and reset |
| `role` | `{ id: string; type: "role" }` | Associated role |

### `ApiTypes.SiteInvitationCreateSchema`

Input for `client.siteInvitations.create()`.

| Field | Type | Required | Description |
|---|---|---|---|
| `email` | `string` | **Yes** | Email of the person to invite |
| `role` | `{ id: string; type: "role" }` | **Yes** | Role to assign to the invitee |

### `ApiTypes.SiteInvitationUpdateSchema`

Input for `client.siteInvitations.update()`.

| Field | Type | Required | Description |
|---|---|---|---|
| `role` | `{ id: string; type: "role" }` | No | Updated role assignment |

---

### `ApiTypes.SsoUser`

Returned by `list()`, `find()`, `copyUsers()`, and `destroy()`. SSO users cannot be updated directly -- their attributes are managed by the identity provider.

| Field | Type | Description |
|---|---|---|
| `id` | `string` | SSO user ID |
| `type` | `"sso_user"` | JSON API resource type |
| `username` | `string` | Email / username |
| `external_id` | `string \| null` | Identity provider ID |
| `is_active` | `boolean` | Whether this user is active on the identity provider |
| `first_name` | `string \| null` | First name |
| `last_name` | `string \| null` | Last name |
| `groups` | `{ id: string; type: "sso_group" }[]` | SSO groups this user belongs to |
| `role` | `{ id: string; type: "role" } \| null` | Directly assigned role (if any) |
| `meta.last_access` | `string \| null` | Date of last reading/interaction |

---

### `ApiTypes.SsoGroup`

Returned by `list()`, `copyRoles()`, `update()`, and `destroy()`.

| Field | Type | Description |
|---|---|---|
| `id` | `string` | SSO group ID |
| `type` | `"sso_group"` | JSON API resource type |
| `name` | `string` | Name of the group |
| `priority` | `number` | When a user belongs to multiple groups, the role from the highest-priority group is used |
| `role` | `{ id: string; type: "role" }` | Role assigned to this group |
| `users` | `{ id: string; type: "sso_user" }[]` | SSO users in this group |

### `ApiTypes.SsoGroupUpdateSchema`

Input for `client.ssoGroups.update()`.

| Field | Type | Required | Description |
|---|---|---|---|
| `priority` | `number` | **Yes** | Priority for role resolution across groups |
| `role` | `{ id: string; type: "role" }` | **Yes** | Role to assign to this group |

---

### `ApiTypes.SsoSettings`

Returned by `find()` and `update()`.

| Field | Type | Description |
|---|---|---|
| `id` | `string` | SSO settings ID |
| `type` | `"sso_settings"` | JSON API resource type |
| `idp_saml_metadata_url` | `string \| null` | URL of Identity Provider SAML Metadata endpoint |
| `idp_saml_metadata_xml` | `string \| null` (optional) | Identity Provider SAML Metadata XML |
| `scim_base_url` | `string` | DatoCMS SCIM base URL |
| `saml_acs_url` | `string` | DatoCMS SAML ACS URL |
| `sp_saml_metadata_url` | `string` | DatoCMS SAML Metadata URL |
| `sp_saml_base_url` | `string` | DatoCMS SAML Base URL |
| `saml_token` | `string` | DatoCMS SAML Token |
| `scim_api_token` | `string` (optional) | DatoCMS SCIM API Token |
| `default_role` | `{ id: string; type: "role" } \| null` | Default role for new SSO users |

### `ApiTypes.SsoSettingsUpdateSchema`

Input for `client.ssoSettings.update()`.

| Field | Type | Required | Description |
|---|---|---|---|
| `idp_saml_metadata_url` | `string \| null` | No | URL of Identity Provider SAML Metadata endpoint |
| `idp_saml_metadata_xml` | `string \| null` | No | Identity Provider SAML Metadata XML |
| `default_role` | `{ id: string; type: "role" }` | No | Default role for new SSO users |

---

### `ApiTypes.Account`

Returned by `client.account.find()`. Represents the project owner.

| Field | Type | Description |
|---|---|---|
| `id` | `string` | Account ID |
| `type` | `"account"` | JSON API resource type |
| `email` | `string` | Email address |
| `first_name` | `string \| null` | First name |
| `last_name` | `string \| null` | Last name |
| `company` | `string \| null` | Company name |

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
