# AGENTS.md

Guidance for AI/code assistants working in this repository.

## Conversation Guidance (Global)

- Ask questions any time a prompt is unclear, ambiguous, or when you have concerns/thoughts that could affect the result.
- If an ask-user-question tool is available, use it for clarification questions so decisions are captured explicitly.
- If a prompt includes a question or discussion and does not explicitly instruct an action, treat that part as planning mode: answer first and do not execute changes for that part until explicitly directed.

## Purpose

This repository powers a personal blog hosted on GitHub Pages and built with Jekyll.
Primary assistant responsibilities are:

1. Help draft and edit blog posts.
2. Keep content and metadata consistent with site conventions.
3. Validate local build behavior before publish.
4. Protect privacy and confidentiality in all published content.

---

## Project Overview

- **Site type:** Jekyll static site
- **Hosting:** GitHub Pages (repository: `ryanguill/ryanguill.github.io`)
- **Primary branch:** `main` (current default branch)
- **Custom domain:** `ryanguill.com` via `CNAME`
- **Build tooling:** Bundler + Jekyll (`bundle exec jekyll ...`)
- **Theme/layout:** Custom layouts/includes in `_layouts` and `_includes`

---

## Repository Structure

- `_posts/`
  Published posts. Filenames determine publish date + slug.

- `_drafts/`
  Unpublished drafts for local preview with `--drafts`.

- `_layouts/`
  Page templates (`default`, `post`, `page`, `archive`).

- `_includes/`
  Shared partials (`head`, `header`, `footer`, etc.).

- `assets/`
  Images/icons/fonts used by posts and global site visuals.

- `resume.html`
  Resume page content. Treat resume updates as separate from blog post work unless explicitly requested.

- `css/` + `_sass/`
  Stylesheet entrypoint and Sass partials.

- `_site/`
  Generated output. **Never edit manually.**

- `_config.yml`
  Jekyll site configuration and global settings.

---

## Post Authoring Rules

### File naming

Create posts in `_posts/` using:

`YYYY-MM-DD-kebab-case-title.md` or `.markdown`

Example: `2026-02-21-my-new-post.md`

### Front matter (required)

Each post should include:

- `layout: post`
- `title: "Post title"`
- `date: YYYY-MM-DD HH:MM:SS`
- `author: Ryan Guill`
- `categories: space-separated category-list`
- `tags: space-separated tag-list`

### Front matter (optional)

- `cover: "/assets/example-image.png"`
- `disqus_disabled: true` (if comments should be off)

### Content conventions

- Prefer Markdown for body content.
- Use fenced code blocks with language identifiers (e.g. `sql`, `ts`, `bash`).
- Keep examples runnable and realistic.
- Add external links for references/fiddles/gists when useful.
- Inline HTML is allowed when needed for formatting demos/tables.

### Standard drafting workflow (rough draft -> post draft)

When writing a new post with the author, follow this process:

1. Start with a planning file in `.plans/rough-draft/` (use `./scripts/new-post-rough-draft "topic"`).
2. Read the rough draft and run an interview pass before drafting the post.
3. Use focused clarification questions (via ask-user-question tool when available).
4. Propose a working brief and outline in the rough draft file.
5. Draft/update the actual post in `_drafts/` once thesis and structure are stable.
6. Iterate in explicit modes: expand, tighten, polish.

The rough draft file is for ideation and decisions; `_drafts/` is for publishable post content.

### Author voice profile (from existing posts)

When drafting or editing posts, preserve these writing characteristics:

- Start with a concrete real-world problem and practical motivation.
- Use a conversational, first-person technical tone (clear, direct, and grounded).
- Explain in progressive layers: context -> core idea -> full implementation -> caveats/tradeoffs.
- Prefer runnable examples with full SQL/TS snippets over abstract summaries.
- Teach by decomposition ("here are the key parts", "inside out", step-by-step breakdowns).
- Include links to references/fiddles/gists so readers can validate and explore.
- Be transparent about uncertainty and tradeoffs; avoid overstating certainty.
- Keep conclusions practical: what to apply, when to use it, and why it helps.

Do not rewrite into a different voice. Keep edits minimal and preserve author phrasing unless clarity, accuracy, or correctness requires change.

---

## Privacy and Content Safety Policy (Strict)

Assistants must **not** include confidential or identifying data unless it is already clearly public and approved for publication.

### Never include

- Secrets/tokens/credentials/API keys.
- Internal URLs, private repo paths, or private system identifiers.
- Proprietary source code copied from employer/client systems.
- Customer names, contract values, pricing specifics, or internal architecture details that are not already public.
- Any personal data (email/phone/address) beyond existing intentionally public profile details.

### Required sanitization

When discussing real-world work:

- Generalize company/customer details.
- Redact unique identifiers and sensitive IDs.
- Replace real values with fabricated but realistic examples.
- Prefer synthetic datasets and anonymized scenarios.

If uncertain whether something is safe to publish, treat it as confidential and rewrite.

---

## Taxonomy and URL Guidance

- Categories and tags are both used in front matter.
- Category choices affect URL/permalink structure for posts.
- Avoid changing categories/titles on already-published posts unless intentional (can change URLs and references).
- Tag/category archive behavior may differ between local builds and GitHub Pages deployments depending on plugin support.

---

## Local Development Workflow

### Setup

```bash
eval "$(rbenv init -)"
gem install bundler:2.5.13
bundle _2.5.13_ install
```

### Preview (including drafts)

```bash
bundle _2.5.13_ exec jekyll serve --drafts --host 127.0.0.1 --port 4001
```

### Production build check

```bash
bundle _2.5.13_ exec jekyll build
```

Run build checks before publishing content changes.

### Standard local verification workflow

For post/content changes, run this sequence before publishing:

1. `bundle _2.5.13_ exec jekyll build`
2. `bundle _2.5.13_ exec jekyll serve --drafts --host 127.0.0.1 --port 4001`
3. Review the affected page(s) in local preview (`http://127.0.0.1:4001`).
4. Run content QA checks:
   - Verify formatting, code blocks, links, and front matter render as expected.
   - Run spell check and fix obvious mistakes.
   - Run a clarity pass: flag confusing or overly convoluted sentences/paragraphs while preserving author voice.
   - Apply basic editorial checks: headings in title case, sentences start with a capital letter, and punctuation is present.
5. Stop local server and proceed to commit/push only after checks pass.

---

## Publishing Workflow

1. Write/edit post in `_posts/` (or finalize from `_drafts/`).
2. Verify front matter and links.
3. Run local build and resolve issues.
4. Commit and push to `main`.
5. Verify live post rendering, RSS visibility, and metadata after deployment.

---

## Editing Guardrails for Assistants

- Preserve existing writing voice and formatting style.
- For clarity checks, prefer flagging issues and suggesting targeted edits or minimal rewrites rather than broad stylistic rewrites.
- Treat blog content and resume content as separate concerns; do not edit `resume.html` unless explicitly requested.
- Do not mass-reformat old posts unless asked.
- Avoid introducing new site dependencies/plugins without explicit approval.
- Do not edit generated output in `_site/`.
- Keep changes scoped to the user request.

---

## Quality Checklist for New Posts

Before finalizing a post, verify:

- Filename/date/title alignment is correct.
- Front matter is complete and valid YAML.
- Categories/tags are intentional and relevant.
- Code blocks are language-tagged and formatted.
- Spelling has been reviewed and corrected.
- Clarity pass completed (confusing or convoluted sections identified/fixed while preserving voice).
- Basic editorial quality is met (heading capitalization, sentence capitalization, punctuation).
- External links work and are trustworthy.
- No confidential data is present.
- Local Jekyll build succeeds.

---

## Known Caveats (Initial)

- GitHub Pages has plugin restrictions; behavior may differ from local Jekyll for unsupported plugins.
- `jekyll-archives` usage should be treated carefully for GH Pages compatibility.
- Canonical URL configuration and custom-domain consistency should be periodically reviewed.
- Legacy integrations (analytics/comments/sharing scripts) should be reviewed occasionally for correctness and relevance.
