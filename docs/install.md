# Install Guide

The public skills can be installed one by one, but they are designed as a
coordinated set. If you want the smoothest companion-skill handoffs, install
the full public set together.

## Recommended Development Install

When you are installing from a local checkout, prefer symlinks over copied
folders. The installed skills stay pointed at the repo, so a single `git pull`
updates the live versions in your host's skills directory.

Install the full public set:

```bash
ln -s /absolute/path/to/repo/skills/datocms-cda <skills-root>/datocms-cda
ln -s /absolute/path/to/repo/skills/datocms-cli <skills-root>/datocms-cli
ln -s /absolute/path/to/repo/skills/datocms-cma <skills-root>/datocms-cma
ln -s /absolute/path/to/repo/skills/datocms-frontend-integrations <skills-root>/datocms-frontend-integrations
ln -s /absolute/path/to/repo/skills/datocms-plugin-builder <skills-root>/datocms-plugin-builder
ln -s /absolute/path/to/repo/skills/datocms-setup <skills-root>/datocms-setup
```

`datocms-setup` is the single public setup entrypoint. It owns all internal
setup recipes, shared references, and recipe-local assets/scripts, so there is
no companion setup bundle to install beyond `skills/datocms-setup`.

## Single-Skill Development Install

If you only need one skill, symlink that folder by its canonical name:

Use an absolute path to the repo checkout as the symlink source:

```bash
ln -s /absolute/path/to/repo/skills/datocms-cda <skills-root>/datocms-cda
```

## Standalone Copy

If you want a detached snapshot that still works after the repo is moved or
deleted, copy the skill folders instead.

Recommended full-set snapshot install:

```bash
cp -r skills/datocms-cda <skills-root>/datocms-cda
cp -r skills/datocms-cli <skills-root>/datocms-cli
cp -r skills/datocms-cma <skills-root>/datocms-cma
cp -r skills/datocms-frontend-integrations <skills-root>/datocms-frontend-integrations
cp -r skills/datocms-plugin-builder <skills-root>/datocms-plugin-builder
cp -r skills/datocms-setup <skills-root>/datocms-setup
```

If you only need one skill, copying a single folder is also supported:

```bash
cp -r skills/datocms-cda <skills-root>/datocms-cda
```

Use the folder names in `skills/` as the source of truth. They match each
skill's `name:` field, so the repo path and the canonical skill name stay
aligned.

## Path Map

Use [docs/skill-catalog.md](skill-catalog.md) as the full canonical path map
for every shipped skill and the internal recipe matrix that `datocms-setup`
covers.
