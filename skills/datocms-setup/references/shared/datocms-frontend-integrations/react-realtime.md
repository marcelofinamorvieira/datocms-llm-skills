# React Real-Time Updates — `useQuerySubscription`

React hook for live content updates via DatoCMS's [Real-time Updates API](https://www.datocms.com/docs/real-time-updates-api/api-reference). Receives updated query results in real-time over Server-Sent Events (SSE) and reconnects automatically on network failures.


## Contents

- [Basic Usage](#basic-usage)
- [Hook Signature](#hook-signature)
- [Initialization Options](#initialization-options)
- [Connection Status](#connection-status)
- [Error Object](#error-object)
- [Integration with Draft Mode](#integration-with-draft-mode)
- [Critical: The `fetcher` Gotcha](#critical-the-fetcher-gotcha)

---

## Basic Usage

```jsx
import { useQuerySubscription } from 'react-datocms';

function App() {
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

  return (
    <div>
      <p>Connection status: {statusMessage[status]}</p>
      {error && (
        <div>
          <h1>Error: {error.code}</h1>
          <div>{error.message}</div>
          {error.response && (
            <pre>{JSON.stringify(error.response, null, 2)}</pre>
          )}
        </div>
      )}
      {data && (
        <ul>
          {data.allBlogPosts.map((blogPost) => (
            <li key={blogPost.slug}>{blogPost.title}</li>
          ))}
        </ul>
      )}
    </div>
  );
}
```

---

## Hook Signature

```ts
const {
  data: QueryResult | undefined,
  error: ChannelErrorData | null,
  status: ConnectionStatus,
} = useQuerySubscription(options);
```

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

```jsx
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
```

---

## Critical: The `fetcher` Gotcha

**Always define `fetcher` as a `const` outside the component scope.** If defined inline, it creates a new function reference on every render, causing an infinite render loop.

### Correct

```jsx
const fetcher = (baseUrl, { headers, method, body }) => {
  return fetch(baseUrl, {
    headers: {
      ...headers,
      'X-Custom-Header': 'value',
    },
    method,
    body,
  });
};

function Home() {
  const { data } = useQuerySubscription({
    fetcher,
    query: QUERY,
    token: 'YOUR_TOKEN',
  });

  return /* ... */;
}
```

### Incorrect (causes infinite render loop)

```jsx
function Home() {
  const { data } = useQuerySubscription({
    // This creates a new function every render!
    fetcher: (baseUrl, { headers, method, body }) => {
      return fetch(baseUrl, { headers, method, body });
    },
    query: QUERY,
    token: 'YOUR_TOKEN',
  });

  return /* ... */;
}
```
