# Vue Image Components — `<datocms-image>` and `<datocms-naked-image>`

Vue 3 components for progressive/responsive images from DatoCMS, designed to work with the `responsiveImage` GraphQL query.


## Contents

- [`<datocms-naked-image>` vs `<datocms-image>`](#datocms-naked-image-vs-datocms-image)
- [Setup](#setup)
- [GraphQL Query](#graphql-query)
- [Basic Usage](#basic-usage)
- [`<datocms-naked-image>` Props](#datocms-naked-image-props)
- [`<datocms-image>` Props](#datocms-image-props)
- [Layout Modes (`<datocms-image>` only)](#layout-modes-datocms-image-only)

---

## `<datocms-naked-image>` vs `<datocms-image>`

| | `<datocms-naked-image>` | `<datocms-image>` |
|---|---|---|
| JS footprint | Minimum (native lazy loading) | Has JS bundle |
| HTML output | Single `<picture>` element | Multiple wrapper elements around `<picture>` |
| Lazy loading | Native `loading="lazy"` | `IntersectionObserver` (customizable thresholds) |
| Placeholder fade | No crossfade (placeholder is background of image) | Crossfade effect between placeholder and image |
| Transparency | Not recommended if image has alpha channel (placeholder stays behind) | Safe for transparent images |

**When to use which:**
- Use `<datocms-naked-image>` by default — minimal JS, simpler output
- Use `<datocms-image>` when you need crossfade effects, custom lazy-loading thresholds, or images with transparency

---

## Setup

Register globally:

```js
import { DatocmsImagePlugin, DatocmsNakedImagePlugin } from 'vue-datocms';

app.use(DatocmsImagePlugin);
app.use(DatocmsNakedImagePlugin);
```

Or use locally:

```vue
<script setup>
import { Image, NakedImage } from 'vue-datocms';
</script>
```

When using local imports with `<script setup>`, the components are available as `<Image>` and `<NakedImage>`. To use kebab-case names (`<datocms-image>`, `<datocms-naked-image>`), register them via the plugin or in a `components` option.

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
2. **Prefer omitting `srcSet`** from GraphQL — the component auto-generates it from `src` + `src-set-candidates` prop, dramatically reducing response size when many images are returned
3. **Never request both `bgColor` and `base64`** — `base64` takes precedence, so requesting both only increases response size
4. **Omit `sizes` from GraphQL** if you pass `sizes` as a prop to the component

---

## Basic Usage

```vue
<script setup>
import { Image, NakedImage } from 'vue-datocms';

const props = defineProps<{ data: any }>();
</script>

<template>
  <div>
    <h1>{{ data.blogPost.title }}</h1>

    <!-- Minimal JS — native lazy loading -->
    <NakedImage :data="data.blogPost.cover.responsiveImage" />

    <!-- IntersectionObserver, crossfade -->
    <Image :data="data.blogPost.cover.responsiveImage" />
  </div>
</template>
```

---

## `<datocms-naked-image>` Props

| Prop | Type | Default | Description |
|---|---|---|---|
| `data` | `ResponsiveImage` | **(required)** | Response from `responsiveImage` GraphQL query |
| `picture-class` | string | null | Additional CSS class for root `<picture>` tag |
| `picture-style` | CSS properties | null | Additional CSS for root `<picture>` tag |
| `img-class` | string | null | Additional CSS class for `<img>` tag |
| `img-style` | CSS properties | null | Additional CSS for `<img>` tag |
| `priority` | boolean | false | Disables lazy loading, sets `fetchPriority="high"` |
| `sizes` | string | undefined | HTML5 `sizes` attribute (falls back to `data.sizes`) |
| `use-placeholder` | boolean | true | Whether to show blurred image placeholder |
| `src-set-candidates` | Array<number> | `[0.25, 0.5, 0.75, 1, 1.5, 2, 3, 4]` | Width multipliers for auto-generated `srcset` (used when `data` has no `srcSet`) |

### Events

| Event | Description |
|---|---|
| `@load` | Emitted when the image has finished loading |

### Exposed Public Properties

| Property | Type | Description |
|---|---|---|
| `imageRef` | `HTMLImageElement` | `ref()` to the img node |

---

## `<datocms-image>` Props

| Prop | Type | Default | Description |
|---|---|---|---|
| `data` | `ResponsiveImage` | **(required)** | Response from `responsiveImage` GraphQL query |
| `layout` | `'intrinsic' \| 'fixed' \| 'responsive' \| 'fill'` | `"intrinsic"` | Layout behavior as viewport changes size |
| `fade-in-duration` | integer | 500 | Duration (ms) of fade-in transition on load |
| `intersection-threshold` | float | 0 | Visibility percentage to trigger loading (0 = one pixel visible, 1 = fully visible) |
| `intersection-margin` | string | `"0px 0px 0px 0px"` | Margin around placeholder for intersection calculation |
| `priority` | boolean | false | Disables lazy loading, sets `fetchPriority="high"` |
| `sizes` | string | undefined | HTML5 `sizes` attribute (falls back to `data.sizes`) |
| `use-placeholder` | boolean | true | Whether to show blurred image placeholder |
| `src-set-candidates` | Array<number> | `[0.25, 0.5, 0.75, 1, 1.5, 2, 3, 4]` | Width multipliers for auto-generated `srcset` |
| `class` | string | null | Additional CSS class for root node |
| `style` | CSS properties | null | Additional CSS for root node |
| `picture-class` | string | null | Additional CSS class for inner `<picture>` tag |
| `picture-style` | CSS properties | null | Additional CSS for inner `<picture>` tag |
| `img-class` | string | null | Additional CSS class for image inside `<picture>` |
| `img-style` | CSS properties | null | Additional CSS for image inside `<picture>` |
| `placeholder-class` | string | null | Additional CSS class for placeholder image |
| `placeholder-style` | CSS properties | null | Additional CSS for placeholder image |

### Events

| Event | Description |
|---|---|
| `@load` | Emitted when the image has finished loading |

### Exposed Public Properties

| Property | Type | Description |
|---|---|---|
| `rootRef` | `HTMLDivElement` | `ref()` to the root node |
| `imageRef` | `HTMLImageElement` | `ref()` to the img node |

---

## Layout Modes (`<datocms-image>` only)

| Mode | Behavior |
|---|---|
| `intrinsic` (default) | Scales down for smaller viewports, maintains original dimensions for larger viewports |
| `fixed` | Dimensions never change (no responsiveness), like native `<img>` |
| `responsive` | Scales both down and up with viewport |
| `fill` | Stretches to fill parent element (parent must have `position: relative`) |

### Fill Layout Example

```vue
<template>
  <div style="position: relative; width: 200px; height: 500px">
    <Image
      :data="imageData"
      layout="fill"
      :style="{ objectFit: 'cover', objectPosition: '50% 50%' }"
    />
  </div>
</template>
```
