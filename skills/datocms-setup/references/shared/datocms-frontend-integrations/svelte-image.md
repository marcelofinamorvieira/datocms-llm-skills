# Svelte Image Components — `<Image />` and `<NakedImage />`

Svelte components for progressive/responsive images from DatoCMS, designed to work with the `responsiveImage` GraphQL query.


## Contents

- [`<NakedImage />` vs `<Image />`](#nakedimage-vs-image-)
- [Setup](#setup)
- [GraphQL Query](#graphql-query)
- [Basic Usage](#basic-usage)
- [`<NakedImage />` Props](#nakedimage-props)
- [`<Image />` Props](#image-props)
- [Layout Modes (`<Image />` only)](#layout-modes-image-only)
- [Handling Dynamic `data` Changes](#handling-dynamic-data-changes)

---

## `<NakedImage />` vs `<Image />`

| | `<NakedImage />` | `<Image />` |
|---|---|---|
| JS footprint | Minimum (native lazy loading) | Has JS bundle |
| HTML output | Single `<picture>` element | Multiple wrapper elements around `<picture>` |
| Lazy loading | Native `loading="lazy"` | `IntersectionObserver` (customizable thresholds) |
| Placeholder fade | No crossfade (placeholder is background of image) | Crossfade effect between placeholder and image |
| Transparency | Not recommended if image has alpha channel (placeholder stays behind) | Safe for transparent images |

**When to use which:**
- Use `<NakedImage />` by default — minimal JS, simpler output
- Use `<Image />` when you need crossfade effects, custom lazy-loading thresholds, or images with transparency

---

## Setup

```js
import { Image, NakedImage } from '@datocms/svelte';
```

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

```svelte
<script>
  import { Image, NakedImage } from '@datocms/svelte';

  export let data;
</script>

<div>
  <h1>{data.blogPost.title}</h1>

  <!-- Minimal JS — native lazy loading -->
  <NakedImage data={data.blogPost.cover.responsiveImage} />

  <!-- IntersectionObserver, crossfade effect -->
  <Image data={data.blogPost.cover.responsiveImage} />
</div>
```

---

## `<NakedImage />` Props

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

### Events

| Event | Description |
|---|---|
| `on:load` | Emitted when the image has finished loading |

---

## `<Image />` Props

| Prop | Type | Default | Description |
|---|---|---|---|
| `data` | `ResponsiveImage` | **(required)** | Response from `responsiveImage` GraphQL query |
| `class` | string | null | Additional CSS class of root node |
| `style` | string | null | Additional CSS rules for the root node |
| `pictureClass` | string | null | Additional CSS class for the inner `<picture>` tag |
| `pictureStyle` | string | null | Additional CSS for the inner `<picture>` tag |
| `imgClass` | string | null | Additional CSS class for the image inside `<picture>` |
| `imgStyle` | string | null | Additional CSS for the image inside `<picture>` |
| `layout` | `'intrinsic' \| 'fixed' \| 'responsive' \| 'fill'` | `"intrinsic"` | Layout behavior as viewport changes size |
| `fadeInDuration` | integer | 500 | Duration (ms) of fade-in transition on load |
| `intersectionThreshold` | float | 0 | Visibility percentage to trigger loading (0 = one pixel visible, 1 = fully visible) |
| `intersectionMargin` | string | `"0px 0px 0px 0px"` | Margin around placeholder for intersection calculation |
| `lazyLoad` | boolean | true | Whether to enable lazy loading |
| `explicitWidth` | boolean | false | Whether the image wrapper should explicitly declare the width |
| `objectFit` | string | null | How the image fits its parent when using `layout="fill"` |
| `objectPosition` | string | null | How the image is positioned within its parent when using `layout="fill"` |
| `priority` | boolean | false | Disables lazy loading, sets `fetchPriority="high"` |
| `srcSetCandidates` | Array<number> | `[0.25, 0.5, 0.75, 1, 1.5, 2, 3, 4]` | Width multipliers for auto-generated `srcset` |
| `sizes` | string | undefined | HTML5 `sizes` attribute (falls back to `data.sizes`) |
| `onLoad` | `() => void` | undefined | Callback when image finishes loading |
| `usePlaceholder` | boolean | true | Whether to show blurred image placeholder |
| `referrerPolicy` | string | `no-referrer-when-downgrade` | Defines which referrer is sent when fetching the image |

### Events

| Event | Description |
|---|---|
| `on:load` | Emitted when the image has finished loading |

---

## Layout Modes (`<Image />` only)

| Mode | Behavior |
|---|---|
| `intrinsic` (default) | Scales down for smaller viewports, maintains original dimensions for larger viewports |
| `fixed` | Dimensions never change (no responsiveness), like native `<img>` |
| `responsive` | Scales both down and up with viewport |
| `fill` | Stretches to fill parent element (parent must have `position: relative`) |

### Fill Layout Example

```svelte
<div style="position: relative; width: 200px; height: 500px;">
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

When the `data` prop changes, the component behaves like a regular `<img>` — the old image stays visible until the new one loads. To force an immediate swap (old image disappears while new one loads), use a `{#key}` block:

```svelte
{#key imageData.src}
  <Image data={imageData} />
{/key}
```
