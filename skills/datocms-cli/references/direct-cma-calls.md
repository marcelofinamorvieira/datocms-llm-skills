# Direct CMA Calls

Use `cma:call` for one-off Content Management API operations from the terminal
when a reusable script would be overkill.

The command surface is dynamic: available resources and methods reflect the CLI
and API surface shipped in the installed package. Always inspect
`npx datocms cma:call --help` before assuming a resource/method pair exists.

## Command shape

```bash
npx datocms cma:call <resource> <method> [...pathArgs]
```

Examples:

```bash
npx datocms cma:call roles list
npx datocms cma:call roles find 123
npx datocms cma:call roles create --data '{name: "Editor", can_edit_site: true}'
npx datocms cma:call items list --params '{filter: {type: "blog_post"}}'
npx datocms cma:call items list --environment staging
```

## Guidance

- Use `--data` for create/update request bodies and `--params` for query parameters
- Add `--environment` when targeting a sandbox
- Use `--profile` or `--api-token` when the command must run against a non-default CLI profile or explicit credential
- Prefer `datocms-cma` instead when the task needs loops, branching, retries, typed helpers, or code that should live in the repo
