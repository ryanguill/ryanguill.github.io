# ryanguill.com

This repository contains the source code and content for my blog published at `https://ryanguill.com`.

## Local setup

This repo uses Jekyll with Ruby via Bundler.

### Required versions

- Ruby `3.2.2` (see `.ruby-version`)
- Bundler `2.5.13` (from `Gemfile.lock`)

If you use `rbenv`, initialize it in your shell:

```bash
eval "$(rbenv init -)"
```

Install bundler + dependencies:

```bash
gem install bundler:2.5.13
bundle _2.5.13_ install
```

## Run locally

Build the site:

```bash
bundle _2.5.13_ exec jekyll build
```

Serve with drafts for preview:

```bash
bundle _2.5.13_ exec jekyll serve --drafts
```

If you have a local alias, `jserve` is also supported in this setup.

## Pre-publish checklist

Before publishing content changes:

1. Build locally:

```bash
bundle _2.5.13_ exec jekyll build
```

2. Run local preview:

```bash
bundle _2.5.13_ exec jekyll serve --drafts --host 127.0.0.1 --port 4001
```

3. Review affected pages at `http://127.0.0.1:4001` and verify:
- front matter renders correctly
- formatting and code blocks look right
- links work

4. Stop preview server, then commit and push.

## Deployment notes

- Primary branch: `main`
- Hosting: GitHub Pages via GitHub Actions workflow at `.github/workflows/pages.yml`
