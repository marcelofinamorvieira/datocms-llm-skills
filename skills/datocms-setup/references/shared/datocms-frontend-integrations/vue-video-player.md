# Vue Video Player — `<VideoPlayer>`

Vue 3 component for DatoCMS/Mux video streaming, designed to work with the `video` GraphQL query. Wraps the `<mux-player>` [web component](https://developer.mozilla.org/en-US/docs/Web/API/Web_components).


## Contents

- [Installation](#installation)
- [Setup](#setup)
- [GraphQL Query](#graphql-query)
- [Basic Usage](#basic-usage)
- [Props](#props)
- [Mux Data Analytics (Opt-in)](#mux-data-analytics-opt-in)

---

## Installation

Requires `@mux/mux-player` as a peer dependency (note: **not** `@mux/mux-player-react`):

```bash
npm install vue-datocms @mux/mux-player
```

---

## Setup

Register globally:

```js
import { DatocmsVideoPlayerPlugin } from 'vue-datocms';

app.use(DatocmsVideoPlayerPlugin);
```

Or use locally:

```vue
<script setup>
import { VideoPlayer } from 'vue-datocms';
</script>
```

---

## GraphQL Query

```graphql
query {
  blogPost {
    cover {
      video {
        # Required — identifies the video to stream
        muxPlaybackId

        # Optional but recommended:
        title       # displayed in upper left corner of player
        width       # used with height for aspect ratio (prevents layout jumps)
        height
        blurUpThumb # blurred placeholder while video loads
        alt         # enables Content Link for click-to-edit overlays
      }
    }
  }
}
```

### Video Object Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `muxPlaybackId` | string | Yes | Identifies the video to stream from Mux CDN |
| `title` | string | No | Displayed in the player overlay |
| `width` | integer | No | Video width (used with `height` for `aspectRatio` style) |
| `height` | integer | No | Video height (used with `width` for `aspectRatio` style) |
| `blurUpThumb` | string | No | Base64-encoded blurred placeholder |
| `alt` | string | No | Alt text (also enables Content Link overlays) |

---

## Basic Usage

```vue
<script setup>
import { VideoPlayer } from 'vue-datocms';

const props = defineProps<{ data: any }>();
</script>

<template>
  <div>
    <h1>{{ data.blogPost.title }}</h1>
    <VideoPlayer :data="data.blogPost.cover.video" />
  </div>
</template>
```

---

## Props

`<VideoPlayer>` accepts all [`<mux-player>` attributes](https://github.com/muxinc/elements/blob/main/packages/mux-player/REFERENCE.md) plus `data`:

| Prop | Type | Required | Description |
|---|---|---|---|
| `data` | `Video` object | Yes | Response from DatoCMS `video` GraphQL query |

### Default Prop Differences from `<mux-player>`

| Prop | `<VideoPlayer>` Default | `<mux-player>` Default | Notes |
|---|---|---|---|
| `disable-cookies` | `true` | `false` | Privacy-first by default |
| `preload` | `"metadata"` | varies | Optimal UX with saved bandwidth |
| `style.aspectRatio` | `"[width] / [height]"` | none | Auto-set from `data.width`/`data.height` when available |

All other props are forwarded directly to `<mux-player>`.

---

## Mux Data Analytics (Opt-in)

Video playback analytics are **disabled by default**. To enable them:

1. Create a [Mux Data](https://www.mux.com/data) account (free)
2. Pass the `env-key` prop to `<VideoPlayer>`

See [Streaming Video Analytics with Mux Data](https://www.datocms.com/docs/streaming-videos/streaming-video-analytics-with-mux-data) for setup details.
