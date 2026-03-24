# Uploads (Assets)

Uploads are the files and media assets in DatoCMS. The CMA provides both low-level upload primitives and high-level convenience methods (Node.js only) for common upload workflows.

## Quick Navigation

- [Node.js Convenience Methods](#nodejs-convenience-methods)
- [The Raw Upload Flow (Any Environment)](#the-raw-upload-flow-any-environment)
- [Browser Upload Helper](#browser-upload-helper)
- [Upload Metadata](#upload-metadata)
- [Listing and Finding Uploads](#listing-and-finding-uploads)
- [Updating Upload Metadata](#updating-upload-metadata)
- [Deleting Uploads](#deleting-uploads)
- [Bulk Operations](#bulk-operations)
- [Upload Collections (Folders)](#upload-collections-folders)
- [Using Uploads in Record Fields](#using-uploads-in-record-fields)
- [Finding Records That Use an Upload](#finding-records-that-use-an-upload)
- [Type Reference](#type-reference)
- [Complete Example: Upload and Use in Record](#complete-example-upload-and-use-in-record)

---

## Node.js Convenience Methods

The `@datocms/cma-client-node` package extends the base Upload resource with helper methods that handle the entire upload flow (request URL → upload to S3 → create upload record).

### Upload from Local File

```ts
const upload = await client.uploads.createFromLocalFile({
  localPath: "./images/photo.jpg",
  // All other fields are optional:
  filename: "custom-name.jpg",
  default_field_metadata: {
    en: {
      alt: "A beautiful photo",
      title: "Photo Title",
      custom_data: {},
      focal_point: null,
    },
  },
  tags: ["photography", "nature"],
  copyright: "© 2024 Author",
  author: "John Doe",
  notes: "Internal note about this asset",
});

console.log(upload.id); // The upload ID to use in record fields
```

### Upload from URL

```ts
const upload = await client.uploads.createFromUrl({
  url: "https://example.com/image.png",
  filename: "downloaded-image.png", // optional, inferred from URL if omitted
  default_field_metadata: {
    en: {
      alt: "Downloaded image",
      title: null,
      custom_data: {},
      focal_point: null,
    },
  },
});
```

### Skip Creation if Already Exists

If you are uploading the same file repeatedly (e.g., in a migration script), use `skipCreationIfAlreadyExists` to avoid duplicates. It checks the file's MD5 hash against existing uploads:

```ts
const upload = await client.uploads.createFromLocalFile({
  localPath: "./images/logo.png",
  skipCreationIfAlreadyExists: true,
});
```

### Track Upload Progress

Both `createFromLocalFile` and `createFromUrl` accept an `onProgress` callback:

```ts
const upload = await client.uploads.createFromLocalFile({
  localPath: "./video/big-file.mp4",
  onProgress: (info) => {
    switch (info.type) {
      case "REQUESTING_UPLOAD_URL":
        console.log("Requesting upload URL...");
        break;
      case "UPLOADING_FILE":
        console.log(`Uploading: ${info.payload.progress}%`);
        break;
    }
  },
});
```

Progress event types:
- `REQUESTING_UPLOAD_URL` — Requesting a signed upload URL from DatoCMS (payload: `{ filename }`)
- `UPLOADING_FILE` — Uploading to S3 (payload: `{ progress }` as 0–100)
- `DOWNLOADING_FILE` — (For URL uploads) Downloading the remote file first (payload: `{ url, progress }`)
- `CREATING_UPLOAD_OBJECT` — Creating the upload record in DatoCMS after S3 upload completes

### Update an Existing Upload's File

Replace the file of an existing upload while keeping its ID and metadata:

```ts
const updated = await client.uploads.updateFromLocalFile("upload-id", {
  localPath: "./images/new-version.jpg",
});
```

```ts
const updated = await client.uploads.updateFromUrl("upload-id", {
  url: "https://example.com/new-version.png",
});
```

### Upload File and Get Path Only

If you need just the S3 path (to use with `client.uploads.create()` separately):

```ts
import { uploadLocalFileAndReturnPath } from "@datocms/cma-client-node";

const path = await uploadLocalFileAndReturnPath(client, "./images/photo.jpg", {
  filename: "photo.jpg",
  onProgress: (info) => console.log(info.type, info.payload),
});

// Now create the upload record manually
const upload = await client.uploads.create({
  path,
  default_field_metadata: {
    en: { alt: "Photo", title: null, custom_data: {}, focal_point: null },
  },
});
```

---

## The Raw Upload Flow (Any Environment)

If not using Node.js convenience methods (e.g., in a browser or edge environment), the upload process has 3 steps:

### Step 1: Request an Upload URL

```ts
const { id: path, url, request_headers } = await client.uploadRequest.create({
  filename: "photo.jpg",
});
```

### Step 2: Upload the File to S3

Use the `request_headers` returned from Step 1 — they contain the required headers for the PUT request:

```ts
await fetch(url, {
  method: "PUT",
  body: fileBuffer, // or File/Blob in browser
  headers: request_headers,
});
```

### Step 3: Create the Upload Record

```ts
const upload = await client.uploads.create({
  path,
  default_field_metadata: {
    en: {
      alt: "A photo",
      title: "Photo Title",
      custom_data: {},
      focal_point: null,
    },
  },
  tags: ["photo"],
});
```

---

## Browser Upload Helper

The `@datocms/cma-client-browser` package provides:

```ts
const upload = await client.uploads.createFromFileOrBlob({
  file: fileInput.files[0], // File or Blob
  filename: "photo.jpg",
  default_field_metadata: { /* ... */ },
});
```

And for updating:

```ts
await client.uploads.updateFromFileOrBlob("upload-id", {
  file: newFile,
});
```

---

## Upload Metadata

### `default_field_metadata`

Per-locale metadata for the asset. Each locale key contains:

```ts
{
  en: {
    alt: "Alternative text",       // string | null
    title: "Image title",          // string | null
    custom_data: { key: "value" }, // Record<string, string>
    focal_point: { x: 0.5, y: 0.5 }, // { x: number, y: number } | null
  },
  it: {
    alt: "Testo alternativo",
    title: "Titolo immagine",
    custom_data: {},
    focal_point: null,
  },
}
```

### Other Upload Attributes

| Attribute | Type | Description |
|---|---|---|
| `tags` | `string[]` | Searchable tags |
| `copyright` | `string \| null` | Copyright notice |
| `author` | `string \| null` | Author name |
| `notes` | `string \| null` | Internal notes (not public) |

---

## Listing and Finding Uploads

Upload pagination uses the same iterator pattern as records. See `references/filtering-and-pagination.md` for iterator options and page-size guidance.

### Filter Uploads

```ts
for await (const upload of client.uploads.listPagedIterator({
  filter: {
    type: "image",     // "image", "video", "file"
    query: "landscape", // Text search
  },
})) {
  console.log(upload.filename);
}
```

### Find by ID

```ts
const upload = await client.uploads.find("upload-id");

// Key response properties (beyond metadata):
// upload.url, upload.filename, upload.size, upload.width, upload.height,
// upload.format, upload.mime_type, upload.is_image, upload.md5,
// upload.blurhash, upload.tags, upload.smart_tags
```

---

## Updating Upload Metadata

```ts
await client.uploads.update("upload-id", {
  default_field_metadata: {
    en: {
      alt: "Updated alt text",
      title: "Updated title",
      custom_data: {},
      focal_point: { x: 0.3, y: 0.7 },
    },
  },
  tags: ["updated", "tags"],
  copyright: "© 2024 New Author",
});
```

---

## Deleting Uploads

```ts
await client.uploads.destroy("upload-id");
```

---

## Bulk Operations

### Bulk Tag

Add tags to multiple uploads at once:

```ts
await client.uploads.bulkTag({
  uploads: [
    { id: "upload-1", type: "upload" },
    { id: "upload-2", type: "upload" },
  ],
  tags: ["new-tag"],
});
```

### Bulk Set Collection (Folder)

Move multiple uploads to a folder:

```ts
await client.uploads.bulkSetUploadCollection({
  uploads: [
    { id: "upload-1", type: "upload" },
    { id: "upload-2", type: "upload" },
  ],
  upload_collection: { id: "collection-id", type: "upload_collection" },
  // or null to remove from folder:
  // upload_collection: null,
});
```

### Bulk Destroy

```ts
await client.uploads.bulkDestroy({
  uploads: [
    { id: "upload-1", type: "upload" },
    { id: "upload-2", type: "upload" },
  ],
});
```

---

## Upload Collections (Folders)

### Create a Folder

```ts
const folder = await client.uploadCollections.create({
  label: "Blog Images",
});
```

### List Folders

```ts
const folders = await client.uploadCollections.list();
```

### Update a Folder

```ts
await client.uploadCollections.update("collection-id", {
  label: "Renamed Folder",
});
```

### Delete a Folder

```ts
await client.uploadCollections.destroy("collection-id");
```

---

## Using Uploads in Record Fields

### Single File Field

```ts
// Minimal — uses upload's default metadata
await client.items.create({
  item_type: { id: modelId, type: "item_type" },
  cover_image: {
    upload_id: upload.id,
  },
});

// With per-field metadata overrides
await client.items.create({
  item_type: { id: modelId, type: "item_type" },
  cover_image: {
    upload_id: upload.id,
    alt: "Cover image",
    title: null,
    custom_data: {},
    focal_point: null,
  },
});
```

### Gallery Field

```ts
await client.items.create({
  item_type: { id: modelId, type: "item_type" },
  gallery: [
    { upload_id: upload1.id },
    { upload_id: upload2.id, alt: "Custom alt for second image" },
  ],
});
```

**Note:** When the upload's `default_field_metadata` is sufficient, you can pass just `{ upload_id: "..." }`. To override defaults for a specific field usage, provide `alt`, `title`, `custom_data`, and/or `focal_point` — these per-field values override the upload's defaults.

---

## Finding Records That Use an Upload

```ts
const referencingRecords = await client.uploads.references("upload-id", {
  nested: true,
});
```

---

## Type Reference

**Import:** `import type { ApiTypes } from "@datocms/cma-client-node";`

> Types shown here are from the current `@datocms/cma-client` package. Always check the installed version for any differences.

### `Upload` (response)

Returned by `client.uploads.find()`, `client.uploads.create()`, iterators, etc.

| Property | Type | Description |
|---|---|---|
| `id` | `string` | Upload ID |
| `type` | `"upload"` | JSON API type |
| `size` | `number` | Size of the upload in bytes |
| `width` | `null \| number` | Width of image (null for non-images) |
| `height` | `null \| number` | Height of image (null for non-images) |
| `path` | `string` | Upload path on storage |
| `basename` | `string` | Upload basename (filename without extension) |
| `filename` | `string` | Upload filename |
| `url` | `string` | Upload URL |
| `format` | `string \| null` | File format |
| `author` | `string \| null` | Author |
| `copyright` | `string \| null` | Copyright notice |
| `notes` | `string \| null` | Internal notes |
| `md5` | `string` | The MD5 hash of the asset |
| `duration` | `number \| null` | Seconds of duration for video |
| `frame_rate` | `number \| null` | Frame rate (FPS) for video |
| `blurhash` | `string \| null` | Blurhash for the asset |
| `thumbhash` | `string \| null` | Base64-encoded ThumbHash for the asset |
| `mux_playback_id` | `string \| null` | Public Mux playback ID for video |
| `mux_mp4_highest_res` | `null \| "high" \| "medium" \| "low"` | Maximum quality of MP4 rendition available |
| `default_field_metadata` | `Record<string, FieldMetadata>` | Per-locale default metadata (see nested shape below) |
| `is_image` | `boolean` | Whether this upload is an image |
| `created_at` | `null \| string` | Date of upload (ISO 8601) |
| `updated_at` | `null \| string` | Date of last update (ISO 8601) |
| `mime_type` | `null \| string` | Mime type of upload |
| `tags` | `string[]` | Tags |
| `smart_tags` | `string[]` | Auto-generated smart tags |
| `exif_info` | `Record<string, unknown>` | Exif information |
| `colors` | `Array<{ red: number; green: number; blue: number; alpha: number }>` | Dominant colors of the image (each value 0-255) |
| `upload_collection` | `{ type: "upload_collection"; id: string } \| null` | Parent upload collection (folder) |
| `creator` | `{ type: string; id: string }` | The account, token, user, SSO user, or organization that created this upload |

**`default_field_metadata[locale]` nested shape:**

| Property | Type | Description |
|---|---|---|
| `alt` | `string \| null` | Alternate text for the asset |
| `title` | `string \| null` | Title for the asset |
| `custom_data` | `Record<string, unknown>` | Object with arbitrary metadata |
| `focal_point` | `{ x: number; y: number } \| null` | Focal point for images (x and y are floats between 0 and 1) |

---

### `UploadCreateSchema` (input for `client.uploads.create()`)

| Property | Type | Required | Description |
|---|---|---|---|
| `path` | `string` | Yes | Upload path (from upload request) |
| `copyright` | `string \| null` | No | Copyright notice |
| `author` | `string \| null` | No | Author |
| `notes` | `string \| null` | No | Internal notes |
| `default_field_metadata` | `Record<string, FieldMetadata>` | No | Per-locale default metadata (same nested shape as response, but all inner fields are optional) |
| `tags` | `string[]` | No | Tags |
| `upload_collection` | `{ type: "upload_collection"; id: string } \| null` | No | Parent upload collection (folder) |

---

### `UploadUpdateSchema` (input for `client.uploads.update()`)

| Property | Type | Required | Description |
|---|---|---|---|
| `path` | `string` | No | Upload path (to replace file) |
| `basename` | `string` | No | Upload basename |
| `copyright` | `string \| null` | No | Copyright notice |
| `author` | `string \| null` | No | Author |
| `notes` | `string \| null` | No | Internal notes |
| `tags` | `string[]` | No | Tags |
| `default_field_metadata` | `Record<string, FieldMetadata>` | No | Per-locale default metadata (same nested shape as response, but all inner fields are optional) |
| `upload_collection` | `{ type: "upload_collection"; id: string } \| null` | No | Parent upload collection (folder) |

---

### `UploadInstancesHrefSchema` (query params for `client.uploads.list()` / iterators)

| Property | Type | Required | Description |
|---|---|---|---|
| `filter` | `object` | No | Attributes to filter uploads |
| `filter.ids` | `string` | No | IDs to fetch, comma separated |
| `filter.query` | `string` | No | Textual query to match (uses `locale` if defined, otherwise main locale) |
| `filter.fields` | `Record<string, unknown>` | No | Same as GraphQL API upload filters (use snake_case for field names) |
| `locale` | `string` | No | When `filter.query` or `filter.fields` is defined, filter by this locale (default: main locale) |
| `order_by` | `string` | No | Fields used to order results. Format: `<field_name>_<ASC\|DESC>`, comma separated |
| `page` | `object` | No | Parameters to control offset-based pagination |
| `page.offset` | `number` | No | Zero-based offset of first entity returned (default: 0) |
| `page.limit` | `number` | No | Maximum number of entities to return (default: 30, max: 500) |

---

### `UploadReferencesHrefSchema` (query params for `client.uploads.references()`)

| Property | Type | Required | Description |
|---|---|---|---|
| `nested` | `boolean` | No | For Modular Content, Structured Text, and Single Block fields, return full payload for nested blocks instead of IDs |
| `version` | `null \| "current" \| "published" \| "published-or-current"` | No | Retrieve only the selected version type linked to the upload |

---

### Bulk Operation Schemas

**`UploadBulkTagSchema`** (input for `client.uploads.bulkTag()`): `{ tags: string[]; uploads: Array<{ type: "upload"; id: string }> }` -- adds the specified tags to the listed uploads.

**`UploadBulkSetUploadCollectionSchema`** (input for `client.uploads.bulkSetUploadCollection()`): `{ upload_collection: { type: "upload_collection"; id: string } | null; uploads: Array<{ type: "upload"; id: string }> }` -- moves the listed uploads to a folder (or removes from folder when `null`).

**`UploadBulkDestroySchema`** (input for `client.uploads.bulkDestroy()`): `{ uploads: Array<{ type: "upload"; id: string }> }` -- deletes the listed uploads.

---

### `UploadRequest` (response from `client.uploadRequest.create()`)

| Property | Type | Description |
|---|---|---|
| `id` | `string` | The S3 path where the file will be stored (use as `path` in `client.uploads.create()`) |
| `type` | `"upload_request"` | JSON API type |
| `url` | `string` | The URL to use to upload the file with a raw/binary PUT request |
| `request_headers` | `Record<string, unknown>` | Additional headers to include in the direct PUT upload request |

### `UploadRequestCreateSchema` (input for `client.uploadRequest.create()`)

| Property | Type | Required | Description |
|---|---|---|---|
| `filename` | `string` | No | The original file name |

---

### `UploadCollection` (response)

Returned by `client.uploadCollections.find()`, `client.uploadCollections.create()`, `client.uploadCollections.list()`, etc.

| Property | Type | Description |
|---|---|---|
| `id` | `string` | Upload collection ID |
| `type` | `"upload_collection"` | JSON API type |
| `label` | `string` | The label of the upload collection |
| `position` | `number` | Ordering index |
| `parent` | `{ type: "upload_collection"; id: string } \| null` | Parent collection |
| `children` | `Array<{ type: "upload_collection"; id: string }>` | Child collections |

### `UploadCollectionCreateSchema` (input for `client.uploadCollections.create()`)

| Property | Type | Required | Description |
|---|---|---|---|
| `label` | `string` | Yes | The label of the upload collection |
| `position` | `number` | No | Ordering index |
| `parent` | `{ type: "upload_collection"; id: string } \| null` | No | Parent collection |

### `UploadCollectionUpdateSchema` (input for `client.uploadCollections.update()`)

| Property | Type | Required | Description |
|---|---|---|---|
| `label` | `string` | No | The label of the upload collection |
| `position` | `number` | No | Ordering index |
| `parent` | `{ type: "upload_collection"; id: string } \| null` | No | Parent collection |
| `children` | `Array<{ type: "upload_collection"; id: string }>` | No | Child collections |

### `UploadCollectionInstancesHrefSchema` (query params for `client.uploadCollections.list()`)

| Property | Type | Required | Description |
|---|---|---|---|
| `filter` | `object` | No | Filter attributes |
| `filter.ids` | `string` | Yes (if filter provided) | IDs to fetch, comma separated |

---

## Complete Example: Upload and Use in Record

```ts
import { buildClient } from "@datocms/cma-client-node";

const client = buildClient({
  apiToken: process.env.DATOCMS_API_TOKEN!,
});

async function uploadAndCreateRecord() {
  // Upload the image
  const upload = await client.uploads.createFromLocalFile({
    localPath: "./images/hero.jpg",
    default_field_metadata: {
      en: {
        alt: "Hero banner",
        title: "Homepage Hero",
        custom_data: {},
        focal_point: { x: 0.5, y: 0.3 },
      },
    },
    tags: ["hero", "homepage"],
  });

  // Use it in a record
  const record = await client.items.create({
    item_type: { id: "model_123", type: "item_type" },
    title: "Homepage",
    hero_image: {
      upload_id: upload.id,
      alt: "Hero banner",
      title: "Homepage Hero",
      custom_data: {},
      focal_point: { x: 0.5, y: 0.3 },
    },
  });

  console.log("Record created:", record.id);
}

uploadAndCreateRecord().catch(console.error);
```
