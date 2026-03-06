# Install Guide

## Core Skills

Core skills can be installed one at a time. Copy the skill folder that matches the canonical skill name into your host's skills directory.

```bash
cp -r skills/datocms-cda <skills-root>/datocms-cda
```

Use the folder names in `skills/` as the source of truth. They now match each skill's `name:` field, so the repo path and the canonical skill name stay aligned.

## Setup Skills

Setup skills are shared bundles. Install the requested setup folder together with any companion skills it references, and preserve the sibling `skills/` and `setup/` layout unless your host rewrites relative references during export.

Example:

```bash
mkdir -p <skills-root>/skills <skills-root>/setup/frontend-foundation
cp -r skills/datocms-frontend-integrations <skills-root>/skills/
cp -r skills/datocms-cda <skills-root>/skills/
cp -r setup/frontend-foundation/datocms-setup-cache-tags <skills-root>/setup/frontend-foundation/
```

## Path Map

Use [docs/skill-catalog.md](skill-catalog.md) as the full canonical path map for every skill and setup flow.
