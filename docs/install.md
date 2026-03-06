# Install Guide

Use the root [README](../README.md#install) for the fast local install commands.
This page keeps the deeper variants that are useful once you want something
other than the default "install the full set into my local skills folder".

## When To Use This Page

- You only want one skill instead of the full set.
- You want a detached copy instead of symlinks.
- You want the canonical path map for each shipped skill.

## Single-Skill Install

If you only need one skill, link just that folder by its canonical name.

Example:

```bash
repo_root="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
skills_dir="${CODEX_HOME:-$HOME/.codex}/skills"

mkdir -p "$skills_dir"
ln -sfn "$repo_root/skills/datocms-cda" "$skills_dir/datocms-cda"
```

The folder names inside `skills/` match each skill's `name:` field, so the repo
path and the canonical skill name stay aligned.

## Detached Snapshot Install

If you want a copy that still works after the repo is moved or deleted, copy the
skill folders instead of symlinking them.

Example:

```bash
repo_root="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
skills_dir="${CODEX_HOME:-$HOME/.codex}/skills"

mkdir -p "$skills_dir/datocms-cda"
cp -R "$repo_root/skills/datocms-cda/." "$skills_dir/datocms-cda"
```

## Canonical Skill Paths

- `skills/datocms-cda`
- `skills/datocms-cli`
- `skills/datocms-cma`
- `skills/datocms-frontend-integrations`
- `skills/datocms-plugin-builder`
- `skills/datocms-setup`

`datocms-setup` already contains its internal recipes, shared references, and
recipe-local scripts/assets, so there is no second setup bundle to install.
