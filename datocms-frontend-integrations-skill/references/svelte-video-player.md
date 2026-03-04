# Svelte Video Player — `<VideoPlayer />`

Svelte component for DatoCMS/Mux video streaming, designed to work with the `video` GraphQL query. Uses the [MUX Player web component](https://github.com/muxinc/elements/blob/main/packages/mux-player/README.md) internally.

---

## Installation

Requires `@mux/mux-player` as a peer dependency (the web component, not the React package):

```bash
npm install @datocms/svelte @mux/mux-player
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

```svelte
<script>
  import { VideoPlayer } from '@datocms/svelte';

  export let data;
</script>

<div>
  <h1>{data.blogPost.title}</h1>
  <VideoPlayer data={data.blogPost.cover.video} />
</div>
```

---

## Props

`<VideoPlayer />` accepts all [attributes of the `<mux-player />` web component](https://github.com/muxinc/elements/blob/main/packages/mux-player/REFERENCE.md) plus `data`:

| Prop | Type | Required | Description |
|---|---|---|---|
| `data` | `Video` object | Yes | Response from DatoCMS `video` GraphQL query |
| `paused` | boolean | No | Control to play or pause the video |

### Default Prop Differences from `<mux-player />`

| Prop | `<VideoPlayer />` Default | `<mux-player />` Default | Notes |
|---|---|---|---|
| `disableCookies` | `true` | `false` | Privacy-first by default |
| `disableTracking` | `true` | `false` | No analytics unless opted in |
| `preload` | `"metadata"` | varies | Optimal UX with saved bandwidth |
| `style.aspectRatio` | `"[width] / [height]"` | none | Auto-set from `data.width`/`data.height` when available |

All other props are forwarded to the internal `<mux-player />` web component.

---

## Mux Data Analytics (Opt-in)

Video playback analytics are **disabled by default**. To enable them:

1. Create a [Mux Data](https://www.mux.com/data) account (free)
2. Pass the `envKey` prop to `<VideoPlayer />`

See [Streaming Video Analytics with Mux Data](https://www.datocms.com/docs/streaming-videos/streaming-video-analytics-with-mux-data) for setup details.
