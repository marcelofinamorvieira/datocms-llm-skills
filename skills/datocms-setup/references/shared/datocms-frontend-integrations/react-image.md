# React Image Components — `<SRCImage />` and `<Image />`

React components for progressive/responsive images from DatoCMS, designed to work with the `responsiveImage` GraphQL query.


## Contents

- [`<SRCImage />` vs `<Image />`](#srcimage-vs-image-)
- [GraphQL Query](#graphql-query)
- [Basic Usage](#basic-usage)
- [`<SRCImage />` Props](#srcimage-props)
- [`<Image />` Props](#image-props)
- [Layout Modes (`<Image />` only)](#layout-modes-image-only)
- [Handling Dynamic `data` Changes](#handling-dynamic-data-changes)

---

## `<SRCImage />` vs `<Image />`

| | `<SRCImage />` | `<Image />` |
|---|---|---|
| Component type | React Server Component | Client Component |
| JS footprint | None (zero JS) | Has JS bundle |
| HTML output | Single `<picture>` element | Multiple wrapper elements around `<picture>` |
| Lazy loading | Native `loading="lazy"` | `IntersectionObserver` (customizable thresholds) |
| Placeholder fade | No crossfade (placeholder is background of image) | Crossfade effect between placeholder and image |
| Transparency | Not recommended if image has alpha channel (placeholder stays behind) | Safe for transparent images |

**When to use which:**
- Use `<SRCImage />` by default — zero JS, simpler output, works as RSC
- Use `<Image />` when you need crossfade effects, custom lazy-loading thresholds, or images with transparency

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

```jsx
import { Image, SRCImage } from 'react-datocms';

function BlogPost({ data }) {
  return (
    <div>
      <h1>{data.blogPost.title}</h1>

      {/* Server Component — native lazy loading, zero JS */}
      <SRCImage data={data.blogPost.cover.responsiveImage} />

      {/* Client Component — IntersectionObserver, crossfade */}
      <Image data={data.blogPost.cover.responsiveImage} />
    </div>
  );
}
```

---

## `<SRCImage />` Props

| Prop | Type | Default | Description |
|---|---|---|---|
| `data` | `ResponsiveImage` | **(required)** | Response from `responsiveImage` GraphQL query |
| `pictureClassName` | string | null | Additional className for root `<picture>` tag |
| `pictureStyle` | CSS properties | null | Additional CSS for root `<picture>` tag |
| `imgClassName` | string | null | Additional className for `<img>` tag |
| `imgStyle` | CSS properties | null | Additional CSS for `<img>` tag |
| `priority` | boolean | false | Disables lazy loading, sets `fetchPriority="high"` |
| `sizes` | string | undefined | HTML5 `sizes` attribute (falls back to `data.sizes`) |
| `usePlaceholder` | boolean | true | Whether to show blurred image placeholder |
| `srcSetCandidates` | Array<number> | `[0.25, 0.5, 0.75, 1, 1.5, 2, 3, 4]` | Width multipliers for auto-generated `srcset` (used when `data` has no `srcSet`) |

---

## `<Image />` Props

| Prop | Type | Default | Description |
|---|---|---|---|
| `data` | `ResponsiveImage` | **(required)** | Response from `responsiveImage` GraphQL query |
| `layout` | `'intrinsic' \| 'fixed' \| 'responsive' \| 'fill'` | `"intrinsic"` | Layout behavior as viewport changes size |
| `fadeInDuration` | integer | 500 | Duration (ms) of fade-in transition on load |
| `intersectionThreshold` | float | 0 | Visibility percentage to trigger loading (0 = one pixel visible, 1 = fully visible) |
| `intersectionMargin` | string | `"0px 0px 0px 0px"` | Margin around placeholder for intersection calculation |
| `priority` | boolean | false | Disables lazy loading, sets `fetchPriority="high"` |
| `sizes` | string | undefined | HTML5 `sizes` attribute (falls back to `data.sizes`) |
| `onLoad` | `() => void` | undefined | Callback when image finishes loading |
| `usePlaceholder` | boolean | true | Whether to show blurred image placeholder |
| `srcSetCandidates` | Array<number> | `[0.25, 0.5, 0.75, 1, 1.5, 2, 3, 4]` | Width multipliers for auto-generated `srcset` |
| `className` | string | null | Additional CSS className for root node |
| `style` | CSS properties | null | Additional CSS for root node |
| `pictureClassName` | string | null | Additional CSS class for inner `<picture>` tag |
| `pictureStyle` | CSS properties | null | Additional CSS for inner `<picture>` tag |
| `imgClassName` | string | null | Additional CSS class for image inside `<picture>` |
| `imgStyle` | CSS properties | null | Additional CSS for image inside `<picture>` |
| `placeholderClassName` | string | null | Additional CSS class for placeholder image |
| `placeholderStyle` | CSS properties | null | Additional CSS for placeholder image |

---

## Layout Modes (`<Image />` only)

| Mode | Behavior |
|---|---|
| `intrinsic` (default) | Scales down for smaller viewports, maintains original dimensions for larger viewports |
| `fixed` | Dimensions never change (no responsiveness), like native `<img>` |
| `responsive` | Scales both down and up with viewport |
| `fill` | Stretches to fill parent element (parent must have `position: relative`) |

### Fill Layout Example

```jsx
<div style={{ position: 'relative', width: 200, height: 500 }}>
  <Image
    data={imageData}
    layout="fill"
    objectFit="cover"
    objectPosition="50% 50%"
  />
</div>
```

---

## Handling Dynamic `data` Changes

When the `data` prop changes, the component behaves like a regular `<img>` — the old image stays visible until the new one loads. To force an immediate swap (old image disappears while new one loads), use a `key` prop:

```jsx
<Image
  key={imageData.src}
  data={imageData}
/>
```
