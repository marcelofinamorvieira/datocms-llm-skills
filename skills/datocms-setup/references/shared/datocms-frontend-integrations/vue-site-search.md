# Vue Site Search — `useSiteSearch`

Vue 3 composable for building a [DatoCMS Site Search](https://www.datocms.com/docs/site-search) widget. Handles all form logic (query, pagination, locale) — you control the rendering.


## Contents

- [Installation](#installation)
- [Basic Usage](#basic-usage)
- [Initialization Options](#initialization-options)
- [Returned Data Shape](#returned-data-shape)
- [Rendering Highlights](#rendering-highlights)
- [Complete Example with Pagination](#complete-example-with-pagination)

---

## Installation

Requires `@datocms/cma-client-browser` for API requests:

```bash
npm install vue-datocms @datocms/cma-client-browser
```

---

## Basic Usage

```vue
<script setup>
import { useSiteSearch } from 'vue-datocms';
import { buildClient } from '@datocms/cma-client-browser';

const client = buildClient({ apiToken: 'YOUR_API_TOKEN' });

const { state, error, data } = useSiteSearch({
  client,
  searchIndexId: '7497',
});
</script>

<template>
  <div>
    <input type="search" v-model="state.query" placeholder="Search..." />

    <div v-if="!data && !error">Loading...</div>
    <div v-if="error">Error: {{ error }}</div>

    <ul v-if="data">
      <li v-for="result in data.pageResults" :key="result.id">
        <a :href="result.url">{{ result.title }}</a>
        <div>{{ result.bodyExcerpt }}</div>
      </li>
    </ul>
  </div>
</template>
```

**Key difference from React:** State is reactive — use `v-model` for the query input and direct assignment (`state.query = ...`, `state.page = ...`) instead of setter functions (`state.setQuery()`, `state.setPage()`).

---

## Initialization Options

| Option | Type | Required | Default | Description |
|---|---|---|---|---|
| `client` | CMA Client instance | Yes | — | Instance from `buildClient()` of `@datocms/cma-client-browser` |
| `searchIndexId` | string | Yes | — | [Search index ID](https://www.datocms.com/docs/site-search/base-integration#performing-searches) |
| `fuzzySearch` | boolean | No | `false` | Enable approximate matching |
| `resultsPerPage` | number | No | `8` | Results per page |
| `initialState.query` | string | No | `''` | Initial search query |
| `initialState.locale` | string | No | `null` | Initial locale filter |
| `initialState.page` | number | No | `0` | Initial page number |

---

## Returned Data Shape

```ts
{
  state: {
    query: string;       // use v-model or direct assignment
    locale: string | undefined;
    page: number;
  };
  error?: string;
  data?: {
    pageResults: Array<{
      id: string;
      title: string;
      titleHighlights: ResultHighlight[];
      bodyExcerpt: string;
      bodyHighlights: ResultHighlight[];
      url: string;
      raw: RawSearchResult;
    }>;
    totalResults: number;
    totalPages: number;
  };
}
```

### Highlight Types

**Key difference from React:** Instead of a `highlightMatch` callback that returns a ReactNode, Vue returns raw highlight data as `HighlightPiece` arrays that you render in your template:

```ts
type ResultHighlight = HighlightPiece[];

type HighlightPiece = {
  text: string;
  isMatch: boolean;
};
```

- **`state`** — Reactive form state. Changing any value triggers a new API request.
- **`error`** — Error message string on API failure, otherwise `undefined`.
- **`data`** — Search results, `undefined` while loading.
- If both `error` and `data` are `undefined`/`null`, the form is loading — show a spinner.

---

## Rendering Highlights

Use `titleHighlights` and `bodyHighlights` to render search match highlighting in templates:

```vue
<template>
  <div v-for="result in data.pageResults" :key="result.id">
    <!-- Title with highlights -->
    <a :href="result.url">
      <strong v-if="result.titleHighlights.length > 0">
        <template v-for="highlight in result.titleHighlights">
          <template v-for="piece in highlight">
            <mark v-if="piece.isMatch">{{ piece.text }}</mark>
            <template v-else>{{ piece.text }}</template>
          </template>
        </template>
      </strong>
      <strong v-else>{{ result.title }}</strong>
    </a>

    <!-- Body excerpts with highlights -->
    <div v-for="highlight in result.bodyHighlights">
      <template v-for="piece in highlight">
        <mark v-if="piece.isMatch">{{ piece.text }}</mark>
        <template v-else>{{ piece.text }}</template>
      </template>
    </div>
  </div>
</template>
```

---

## Complete Example with Pagination

```vue
<script setup>
import { useSiteSearch } from 'vue-datocms';
import { buildClient } from '@datocms/cma-client-browser';

const client = buildClient({ apiToken: 'YOUR_API_TOKEN' });

const { state, error, data } = useSiteSearch({
  client,
  searchIndexId: '7497',
  fuzzySearch: true,
  initialState: { locale: 'en' },
  resultsPerPage: 10,
});
</script>

<template>
  <div>
    <div>
      <input
        type="search"
        v-model="state.query"
        placeholder="Search..."
      />
      <select v-model="state.locale">
        <option value="en">English</option>
        <option value="it">Italian</option>
      </select>
    </div>

    <div v-if="!data && !error">Loading...</div>
    <div v-if="error">Error! {{ error }}</div>

    <div v-if="data">
      <div v-for="result in data.pageResults" :key="result.id">
        <a :href="result.url">
          <strong v-if="result.titleHighlights.length > 0">
            <template v-for="highlight in result.titleHighlights">
              <template v-for="piece in highlight">
                <mark v-if="piece.isMatch">{{ piece.text }}</mark>
                <template v-else>{{ piece.text }}</template>
              </template>
            </template>
          </strong>
          <strong v-else>{{ result.title }}</strong>
        </a>

        <div v-for="highlight in result.bodyHighlights">
          <template v-for="piece in highlight">
            <mark v-if="piece.isMatch">{{ piece.text }}</mark>
            <template v-else>{{ piece.text }}</template>
          </template>
        </div>
      </div>

      <p>Total results: {{ data.totalResults }}</p>

      <div>
        <button
          v-if="state.page > 0"
          @click="state.page = state.page - 1"
        >
          Previous
        </button>
        <button
          v-if="state.page < data.totalPages"
          @click="state.page = state.page + 1"
        >
          Next
        </button>
      </div>
    </div>
  </div>
</template>
```
