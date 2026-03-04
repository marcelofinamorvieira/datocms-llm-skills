# Vue Real-Time Updates — `useQuerySubscription`

Vue 3 composable for live content updates via DatoCMS's [Real-time Updates API](https://www.datocms.com/docs/real-time-updates-api/api-reference). Receives updated query results in real-time over Server-Sent Events (SSE) and reconnects automatically on network failures.

---

## Basic Usage

```vue
<script setup>
import { useQuerySubscription } from 'vue-datocms';

const { status, error, data } = useQuerySubscription({
  query: `
    query {
      allBlogPosts {
        slug
        title
      }
    }
  `,
  token: 'YOUR_API_TOKEN',
});

const statusMessage = {
  connecting: 'Connecting to DatoCMS...',
  connected: 'Connected to DatoCMS, receiving live updates!',
  closed: 'Connection closed',
};
</script>

<template>
  <div>
    <p>Connection status: {{ statusMessage[status] }}</p>

    <div v-if="error">
      <h1>Error: {{ error.code }}</h1>
      <div>{{ error.message }}</div>
      <pre v-if="error.response">{{ JSON.stringify(error.response, null, 2) }}</pre>
    </div>

    <ul v-if="data">
      <li v-for="blogPost in data.allBlogPosts" :key="blogPost.slug">
        {{ blogPost.title }}
      </li>
    </ul>
  </div>
</template>
```

---

## Composable Signature

```ts
const {
  data: Ref<QueryResult | undefined>,
  error: Ref<ChannelErrorData | null>,
  status: Ref<ConnectionStatus>,
} = useQuerySubscription(options);
```

**Important:** Unlike the React hook, the returned `data`, `error`, and `status` are Vue `Ref` values. Access their values with `.value` in `<script>` and use them directly in `<template>`.

---

## Initialization Options

| Option | Type | Required | Default | Description |
|---|---|---|---|---|
| `enabled` | boolean | No | `true` | Whether the subscription is active |
| `query` | string \| `TypedDocumentNode` | Yes | — | The GraphQL query to subscribe to |
| `token` | string | Yes | — | DatoCMS API token |
| `variables` | Object | No | — | GraphQL variables for the query |
| `includeDrafts` | boolean | No | — | If true, returns draft records |
| `excludeInvalid` | boolean | No | — | If true, filters out invalid records |
| `environment` | string | No | primary | DatoCMS environment name |
| `contentLink` | `'v1'` \| undefined | No | — | Enables Content Link metadata embedding |
| `baseEditingUrl` | string | No | — | Base URL of the DatoCMS project (for Content Link) |
| `cacheTags` | boolean | No | — | If true, receives Cache Tags with the query |
| `initialData` | Object | No | — | Initial data for first render (e.g., server-fetched data) |
| `reconnectionPeriod` | number | No | `1000` | Milliseconds to wait before reconnecting on network error |
| `fetcher` | fetch-like function | No | `window.fetch` | Custom fetch function for the registration query |
| `eventSourceClass` | EventSource-like class | No | `window.EventSource` | Custom EventSource class for SSE connection |
| `baseUrl` | string | No | `https://graphql-listen.datocms.com` | Base URL for the subscription endpoint |

---

## Connection Status

| Status | Description |
|---|---|
| `connecting` | Subscription channel is trying to connect |
| `connected` | Channel is open, receiving live updates |
| `closed` | Channel permanently closed due to fatal error (e.g., invalid query) |

---

## Error Object

| Property | Type | Description |
|---|---|---|
| `code` | string | Error code (e.g., `INVALID_QUERY`) |
| `message` | string | Human-friendly error description |
| `response` | Object | Raw response from endpoint (if available) |

---

## Integration with Draft Mode

When used in a draft mode context, pass the relevant options:

```vue
<script setup>
import { useQuerySubscription } from 'vue-datocms';

const { data } = useQuerySubscription({
  query: QUERY,
  token: draftModeToken,
  includeDrafts: true,
  excludeInvalid: true,
  // For Content Link (visual editing):
  contentLink: 'v1',
  baseEditingUrl: 'https://your-project.admin.datocms.com/environments/main',
  // Server-fetched data as initial render:
  initialData: serverData,
});
</script>
```

---

## Full Example with SEO

```vue
<script setup>
import { Image, StructuredText, toHead, useQuerySubscription } from 'vue-datocms';
import { useHead } from '@unhead/vue';
import { computed } from 'vue';

const query = `
  query AppQuery($first: IntType) {
    page: blog {
      seo: _seoMetaTags {
        attributes
        content
        tag
      }
    }
    site: _site {
      favicon: faviconMetaTags {
        attributes
        content
        tag
      }
    }
    blogPosts: allBlogPosts(first: $first) {
      id
      title
      slug
      excerpt { value }
      coverImage {
        responsiveImage(imgixParams: { w: 550, auto: format }) {
          src
          width
          height
          alt
          base64
        }
      }
    }
  }
`;

const { data, error, status } = useQuerySubscription({
  query,
  variables: { first: 4 },
  token: 'YOUR_API_TOKEN',
});

const metaTags = computed(() =>
  toHead(
    data.value ? [...data.value.page.seo, ...data.value.site.favicon] : [],
  ),
);

useHead(metaTags);

const statusMessage = {
  connecting: 'Connecting to DatoCMS...',
  connected: 'Connected to DatoCMS, receiving live updates!',
  closed: 'Connection closed',
};
</script>

<template>
  <div>
    <div>
      <span v-if="status === 'connected'" class="connected-badge" />
      {{ statusMessage[status] }}
    </div>

    <div v-if="error">
      <h1>Error: {{ error.code }}</h1>
      <div>{{ error.message }}</div>
      <pre v-if="error.response">{{ JSON.stringify(error.response, null, 2) }}</pre>
    </div>

    <div v-if="data">
      <article v-for="blogPost in data.blogPosts" :key="blogPost.id">
        <Image :data="blogPost.coverImage.responsiveImage" />
        <h2>{{ blogPost.title }}</h2>
        <StructuredText :data="blogPost.excerpt" />
      </article>
    </div>
  </div>
</template>
```

---

## Critical: The `fetcher` Gotcha

**Always define `fetcher` as a `const` outside the `<script setup>` or outside the component scope.** If defined inline in the options object that gets recreated on every render, it creates a new function reference each time, causing an infinite loop.

### Correct

```vue
<script setup>
import { useQuerySubscription } from 'vue-datocms';

const fetcher = (baseUrl, { headers, method, body }) => {
  return fetch(baseUrl, {
    headers: { ...headers, 'X-Custom-Header': 'value' },
    method,
    body,
  });
};

const { data } = useQuerySubscription({
  fetcher,
  query: QUERY,
  token: 'YOUR_TOKEN',
});
</script>
```

### Incorrect (causes infinite loop)

```vue
<script setup>
import { useQuerySubscription } from 'vue-datocms';

// Reactive object recreated on re-render
const { data } = useQuerySubscription({
  fetcher: (baseUrl, { headers, method, body }) => {
    return fetch(baseUrl, { headers, method, body });
  },
  query: QUERY,
  token: 'YOUR_TOKEN',
});
</script>
```
