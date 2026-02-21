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
