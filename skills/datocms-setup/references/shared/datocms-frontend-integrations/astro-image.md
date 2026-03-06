# Astro Image Component — `<Image />`

Astro component for progressive/responsive images from DatoCMS, designed to work with the `responsiveImage` GraphQL query. Unlike React (which offers `<SRCImage />` and `<Image />`) and Svelte (which offers `<NakedImage />` and `<Image />`), `@datocms/astro` provides a **single `<Image />`** component that is completely native with zero JavaScript footprint.


## Contents

- [Setup](#setup)
- [Out-of-the-Box Features](#out-of-the-box-features)
- [GraphQL Query](#graphql-query)
- [Basic Usage](#basic-usage)
- [`<Image />` Props](#image-props)
- [Key Differences from React and Svelte](#key-differences-from-react-and-svelte)

---

## Setup

```js
import { Image } from '@datocms/astro/Image';
```

**Note:** `@datocms/astro` uses subpath imports — always import from `@datocms/astro/Image`, not from `@datocms/astro`.

---

## Out-of-the-Box Features

- Completely native, with no JavaScript footprint
- Offers optimized version of images for browsers that support WebP/AVIF format
- Generates multiple smaller images so smartphones and tablets don't download desktop-sized images
- Efficiently lazy loads images to speed initial page load and save bandwidth
- Holds the image position so your page doesn't jump while images load
- Uses either blur-up or background color techniques to show a preview of the image while it loads

---

## GraphQL Query

```graphql
query {
  blogPost {
    cover {
      responsiveImage(
        imgixParams: { fit: crop, w: 300, h: 300, auto: format }
      ) {
        # Always required
        src
        width
        height

        # Strongly suggested
        alt
        title

        # Placeholder (pick ONE — base64 takes precedence if both present)
        base64    # blur-up placeholder, JPEG, base64-encoded
        # bgColor # OR background color placeholder

        # Optional (can be omitted to reduce response size)
        # srcSet  # omit to let component auto-generate from src
        # sizes   # omit if passing sizes prop to component
      }
    }
  }
}
```

### `ResponsiveImage` Object Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `src` | string | Yes | The `src` attribute for the image |
| `width` | integer | Yes | The width of the image |
| `height` | integer | Yes | The height of the image |
| `alt` | string | No | Alternate text (strongly suggested) |
| `title` | string | No | Title attribute (strongly suggested) |
| `sizes` | string | No | HTML5 `sizes` attribute (omit if passing `sizes` prop to component) |
| `base64` | string | No | Base64-encoded thumbnail for blur-up placeholder |
| `bgColor` | string | No | Background color placeholder (omit if requesting `base64`) |
| `srcSet` | string | No | HTML5 `srcSet` (can be omitted — component auto-generates from `src`) |
| `webpSrcSet` | string | No | **Deprecated** — use `{ auto: format }` imgixParams instead |

### Best Practices

1. **Always use `{ auto: format }`** in `imgixParams` — serves WebP/AVIF automatically without increasing response size
2. **Prefer omitting `srcSet`** from GraphQL — the component auto-generates it from `src` + `srcSetCandidates` prop, dramatically reducing response size when many images are returned
3. **Never request both `bgColor` and `base64`** — `base64` takes precedence, so requesting both only increases response size
4. **Omit `sizes` from GraphQL** if you pass `sizes` as a prop to the component

---

## Basic Usage

```astro
---
import { Image } from '@datocms/astro/Image';
import { executeQuery } from '@datocms/cda-client';

const query = `
  query {
    blogPost {
      title
      cover {
        responsiveImage(imgixParams: { fit: crop, w: 300, h: 300, auto: format }) {
          src
          width
          height
          alt
          title
          base64
          sizes
        }
      }
    }
  }
`;

const { blogPost } = await executeQuery(query, { token: '<YOUR-API-TOKEN>' });
---

<h1>{blogPost.title}</h1>
<Image data={blogPost.cover.responsiveImage} />
```

---

## `<Image />` Props

| Prop | Type | Default | Description |
|---|---|---|---|
| `data` | `ResponsiveImage` | **(required)** | Response from `responsiveImage` GraphQL query |
| `pictureClass` | string | null | Additional CSS class for root `<picture>` tag |
| `pictureStyle` | CSS properties | null | Additional CSS for root `<picture>` tag |
| `imgClass` | string | null | Additional CSS class for the `<img>` tag |
| `imgStyle` | CSS properties | null | Additional CSS for the `<img>` tag |
| `priority` | boolean | false | Disables lazy loading, sets `fetchPriority="high"` |
| `sizes` | string | undefined | HTML5 `sizes` attribute (falls back to `data.sizes`) |
| `usePlaceholder` | boolean | true | Whether to show blurred image placeholder |
| `srcSetCandidates` | Array<number> | `[0.25, 0.5, 0.75, 1, 1.5, 2, 3, 4]` | Width multipliers for auto-generated `srcset` (used when `data` has no `srcSet`) |
| `referrerPolicy` | string | `no-referrer-when-downgrade` | Defines which referrer is sent when fetching the image |

---

## Key Differences from React and Svelte

| Feature | React | Svelte | Astro |
|---|---|---|---|
| Components | `<SRCImage />` (zero JS) + `<Image />` (crossfade) | `<NakedImage />` (minimal JS) + `<Image />` (crossfade) | Single `<Image />` (zero JS) |
| Import | `from 'react-datocms'` | `from '@datocms/svelte'` | `from '@datocms/astro/Image'` |
| Layout modes | `intrinsic`, `fixed`, `responsive`, `fill` | `intrinsic`, `fixed`, `responsive`, `fill` | Not applicable (native `<picture>`) |
| Crossfade | `<Image />` only | `<Image />` only | Not available |
| IntersectionObserver | `<Image />` only | `<Image />` only | Not used (native lazy loading) |

Since Astro's `<Image />` produces a completely native `<picture>` element with no JavaScript, it doesn't support layout modes, crossfade effects, or IntersectionObserver-based lazy loading. It uses the browser's native `loading="lazy"` instead.
