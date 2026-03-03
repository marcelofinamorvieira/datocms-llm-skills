# Draft Mode, Caching, and Environments

Covers draft/preview mode, strict mode (`excludeInvalid`), environment targeting, cache tags, CDN behavior, and Content Link / visual editing.

---

## Draft / Preview Mode

Set `includeDrafts: true` to include draft (unpublished) content in responses:

```ts
const data = await executeQuery(query, {
  token: process.env.DATOCMS_CDA_TOKEN!,
  includeDrafts: true,
});
```

**Critical gotcha:** The `X-Include-Drafts` header can **only be `true`** — omit it entirely for published content. Setting it to `false` returns an `INVALID_X_INCLUDE_DRAFTS_HEADER` error. The `@datocms/cda-client` handles this correctly (it omits the header when `includeDrafts` is falsy).

When `includeDrafts` is enabled, the `_status` meta field becomes meaningful:
- `published` — the record is published and what you see is the published version
- `draft` — the record has never been published
- `updated` — the record is published but has unpublished changes (what you see includes those changes)

Without `includeDrafts`, all returned records are published — `_status` is always `published`.

---

## Strict Mode (`excludeInvalid`)

Set `excludeInvalid: true` to filter out invalid records and **narrow GraphQL types**:

```ts
const data = await executeQuery(query, {
  token: process.env.DATOCMS_CDA_TOKEN!,
  excludeInvalid: true,
});
```

When enabled:
- Records that fail validation rules are excluded from results
- Fields with "Required" validation become non-nullable in the GraphQL schema (e.g., `String` → `String!`)
- Asset fields with image transformation validation: `focalPoint`, `width`, `height`, `responsiveImage` become non-nullable
- Video asset fields: `video` property becomes non-nullable
- Asset fields with required alt/title validation: those properties become non-nullable

**Recommended for production** — it ensures you never receive invalid or incomplete records and gives stronger type guarantees.

**Warning:** After adding or removing validations on existing models, DatoCMS re-validates all records. During this re-validation phase, requests with `excludeInvalid: true` **will return errors** (not just fewer results). This can take several minutes depending on record volume.

**Safer alternative:** Use `filter: { _isValid: { eq: true } }` in your query instead of `excludeInvalid`. This filters out invalid records without the re-validation error risk, though it does not narrow GraphQL types to non-nullable.

---

## Environment Targeting

Target a specific DatoCMS environment (instead of the primary):

```ts
const data = await executeQuery(query, {
  token: process.env.DATOCMS_CDA_TOKEN!,
  environment: "staging",
});
```

Omit the `environment` option to use the primary environment.

---

## Cache Tags

Enable cache tags to receive opaque tag strings in the response headers. These are used for targeted CDN cache invalidation.

**You must use `rawExecuteQuery`** to access response headers:

```ts
import { rawExecuteQuery } from "@datocms/cda-client";

const [data, response] = await rawExecuteQuery(query, {
  token: process.env.DATOCMS_CDA_TOKEN!,
  returnCacheTags: true,
});

const cacheTags = response.headers.get("x-cache-tags");
// Opaque space-separated strings used for CDN invalidation
```

### Cache Invalidation via Webhook

DatoCMS sends a webhook when cache tags need invalidation. Configure it in Project Settings under "Content Delivery API Cache Tags" → "Invalidate" event.

**Webhook payload:**
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

Use this webhook to purge your CDN cache. Common CDN tag headers: `Cache-Tag` (Netlify, Cloudflare), `CDN-Tag` (Bunny), Surrogate Keys (Fastly). For Next.js, use `revalidateTag()` with each tag.

### CDN Caching Behavior

- All CDA queries are cached by DatoCMS's CDN
- Cache is selectively invalidated when content changes
- Queries exceeding **8 KB gzip-compressed** bypass the CDN and hit the origin directly
- Response headers indicate caching status:
  - `X-Cacheable-On-Cdn` — whether the query is cached on CDN

**Tip:** Keep queries under the 8 KB gzip limit for best performance. Oversized queries bypass CDN and face stricter rate limits.

---

## Content Link / Visual Editing (Enterprise)

**Note:** Content Link / Visual Editing is an **Enterprise feature**. Non-Enterprise projects will receive an `INVALID_X_VISUAL_EDITING_HEADER` error.

Enable Content Link to embed editing metadata in responses, allowing visual editing integrations (e.g., Vercel Visual Editing):

```ts
const data = await executeQuery(query, {
  token: process.env.DATOCMS_CDA_TOKEN!,
  contentLink: "vercel-v1",
  baseEditingUrl: "https://your-project.admin.datocms.com",
});
```

| Option | Description |
|---|---|
| `contentLink: 'vercel-v1'` | Embed Vercel Visual Editing metadata |
| `contentLink: 'v1'` | Embed generic Content Link metadata |
| `baseEditingUrl` | The DatoCMS admin URL for your project |

When enabled, string fields in the response include additional metadata that Vercel's Visual Editing toolbar uses to create direct links to the DatoCMS editor.

Setting `baseEditingUrl` alone (without `contentLink`) enables the `_editingUrl` field on records, which returns a direct URL to edit that record in the DatoCMS admin.
