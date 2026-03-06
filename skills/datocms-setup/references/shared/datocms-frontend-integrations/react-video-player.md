# React Video Player — `<VideoPlayer />`

React component for DatoCMS/Mux video streaming, designed to work with the `video` GraphQL query.


## Contents

- [Installation](#installation)
- [GraphQL Query](#graphql-query)
- [Basic Usage](#basic-usage)
- [Props](#props)
- [`useVideoPlayer` Hook](#usevideoplayer-hook)
- [Mux Data Analytics (Opt-in)](#mux-data-analytics-opt-in)

---

## Installation

Requires `@mux/mux-player-react` as a peer dependency:

```bash
npm install react-datocms @mux/mux-player-react
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

```jsx
import { VideoPlayer } from 'react-datocms';

function BlogPost({ data }) {
  return (
    <div>
      <h1>{data.blogPost.title}</h1>
      <VideoPlayer data={data.blogPost.cover.video} />
    </div>
  );
}
```

---

## Props

`<VideoPlayer />` accepts all [MuxPlayer props](https://github.com/muxinc/elements/blob/main/packages/mux-player-react/REFERENCE.md) plus `data`:

| Prop | Type | Required | Description |
|---|---|---|---|
| `data` | `Video` object | Yes | Response from DatoCMS `video` GraphQL query |

### Default Prop Differences from `<MuxPlayer />`

| Prop | `<VideoPlayer />` Default | `<MuxPlayer />` Default | Notes |
|---|---|---|---|
| `disableCookies` | `true` | `false` | Privacy-first by default |
| `disableTracking` | `true` | `false` | No analytics unless opted in |
| `preload` | `"metadata"` | varies | Optimal UX with saved bandwidth |
| `style.aspectRatio` | `"[width] / [height]"` | none | Auto-set from `data.width`/`data.height` when available |

All other props are forwarded directly to `<MuxPlayer />`.

---

## `useVideoPlayer` Hook

For custom player wrappers, use `useVideoPlayer` to transform DatoCMS video data into `<MuxPlayer />` props:

```jsx
import { useVideoPlayer } from 'react-datocms';
import MuxPlayer from '@mux/mux-player-react';

function CustomPlayer({ videoData }) {
  const props = useVideoPlayer({ data: videoData });

  // props = {
  //   playbackId: 'ip028MAXF026dU900bKiyNDttjonw7A1dFY',
  //   title: 'Title',
  //   style: { aspectRatio: '1080 / 1920' },
  //   placeholder: 'data:image/bmp;base64,...',
  // }

  return <MuxPlayer {...props} />;
}
```

---

## Mux Data Analytics (Opt-in)

Video playback analytics are **disabled by default**. To enable them:

1. Create a [Mux Data](https://www.mux.com/data) account (free)
2. Pass the `envKey` prop to `<VideoPlayer />`

See [Streaming Video Analytics with Mux Data](https://www.datocms.com/docs/streaming-videos/streaming-video-analytics-with-mux-data) for setup details.
