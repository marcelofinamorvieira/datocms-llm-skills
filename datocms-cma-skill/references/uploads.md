# Uploads (Assets)

Uploads are the files and media assets in DatoCMS. The CMA provides both low-level upload primitives and high-level convenience methods (Node.js only) for common upload workflows.

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

### List with Pagination

```ts
for await (const upload of client.uploads.listPagedIterator()) {
  console.log(upload.id, upload.filename);
}
```

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
    {
      upload_id: upload1.id,
      alt: "First image",
      title: null,
      custom_data: {},
      focal_point: null,
    },
    {
      upload_id: upload2.id,
      alt: "Second image",
      title: null,
      custom_data: {},
      focal_point: null,
    },
  ],
});
```

**Important:** Even when the upload already has `default_field_metadata`, the file/gallery field value requires its own `alt`, `title`, `custom_data`, and `focal_point` properties. These per-field values override the upload's defaults.

---

## Finding Records That Use an Upload

```ts
const referencingRecords = await client.uploads.references("upload-id");
```

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
