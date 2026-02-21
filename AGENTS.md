# AGENTS.md

Guidance for AI/code assistants working in this repository.

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
- **Primary branch:** `master` (current default branch)
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
bundle install
```

### Preview (including drafts)

```bash
bundle exec jekyll serve --drafts
```

### Production build check

```bash
bundle exec jekyll build
```

Run build checks before publishing content changes.

---

## Publishing Workflow

1. Write/edit post in `_posts/` (or finalize from `_drafts/`).
2. Verify front matter and links.
3. Run local build and resolve issues.
4. Commit and push to `master`.
5. Verify live post rendering, RSS visibility, and metadata after deployment.

---

## Editing Guardrails for Assistants

- Preserve existing writing voice and formatting style.
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
- External links work and are trustworthy.
- No confidential data is present.
- Local Jekyll build succeeds.

---

## Known Caveats (Initial)

- GitHub Pages has plugin restrictions; behavior may differ from local Jekyll for unsupported plugins.
- `jekyll-archives` usage should be treated carefully for GH Pages compatibility.
- Canonical URL configuration and custom-domain consistency should be periodically reviewed.
- Legacy integrations (analytics/comments/sharing scripts) should be reviewed occasionally for correctness and relevance.
