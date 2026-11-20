# ryanguill.com

This repository contains the source code and content for my blog published at `https://ryanguill.com`.

## New post planning workflow

- Create a rough-draft planning file:

```bash
./scripts/new-post-rough-draft "post topic idea"
```

- Use `.plans/rough-draft/` for brainstorming, interview notes, and outline decisions.
- Draft publishable content in `_drafts/` once the thesis and structure are stable.
- See `.plans/workflows/agent-post-workflow.md` for the full process.

## Working with an agent on a new post

After creating a rough-draft file, start with a prompt like this:

```text
Read `.plans/rough-draft/YYYY-MM-DD-topic-slug.md` and help me turn it into a post.
First, ask focused clarification questions.
Then suggest a working brief + outline.
Once we align, draft/update `_drafts/YYYY-MM-DD-topic-slug.md`, using today's date for the draft filename (the date we create the draft), not necessarily the rough-draft file date.
Preserve my writing voice and use minimal rewrites for clarity.
```

Suggested iteration prompts:

- `Expand this section with a concrete SQL example and explain it step-by-step.`
- `Tighten this draft for clarity without changing my voice.`
- `Run polish mode: spell check, clarity pass, and editorial checks only.`


## Local setup

This repo uses Jekyll with Ruby via Bundler.

### Required versions

- Ruby `4.0.10` (see `.ruby-version`)
- Bundler (ships with Ruby)

If you use `rbenv`, initialize it in your shell:

```bash
eval "$(rbenv init -)"
```

Install dependencies:

```bash
bundle install
```

## Run locally

Build the site:

```bash
bundle exec jekyll build
```

Serve with drafts for preview:

```bash
bundle exec jekyll serve --drafts
```

If you have a local alias, `jserve` is also supported in this setup.

## Pre-publish checklist

Before publishing content changes:

1. Build locally:

```bash
bundle exec jekyll build
```

2. Run local preview:

```bash
bundle exec jekyll serve --drafts --host 127.0.0.1 --port 4001
```

3. Review affected pages at `http://127.0.0.1:4001` and verify:
- front matter renders correctly
- formatting and code blocks look right
- links work
- spelling is checked and obvious typos are fixed
- confusing or convoluted sentences are clarified while preserving writing voice
- headings use title case, sentences start with a capital letter, and punctuation is present

4. Stop preview server, then commit and push.

## Deployment notes

- Primary branch: `main`
- Hosting: GitHub Pages via GitHub Actions workflow at `.github/workflows/pages.yml`
