# Overall Site Plan (Feb 2026)

This file tracks site improvements we intend to make, including deferred work.

## Immediate Completed Work

- [x] Add `AGENTS.md` with authoring rules, privacy policy, and publish workflow.
- [x] Fix canonical base URL to custom domain (`https://ryanguill.com`).
- [x] Remove duplicate hardcoded analytics snippet and use config-driven include.

## Modernization Plan (Next)

### 1) Stabilize local toolchain

- [x] Add `.ruby-version` and document supported Ruby/Bundler versions.
- [x] Ensure `bundle install` works on a clean machine with clear setup docs.
- [x] Decide whether to pin Jekyll to an explicit version in `Gemfile`.

### 2) Move to GitHub Actions deploy flow

- [x] Add a GitHub Actions workflow to build and deploy the static site.
- [x] Build with explicit Jekyll/Bundler versions in CI.
- [x] Deploy generated site via Pages action so plugin behavior is predictable.
- [x] After the CI deploy flow is stable and green, rename the primary branch from `master` to `main`.
- [x] During branch rename, walk through required GitHub/repo settings updates and local git updates with user.

#### GitHub Actions cutover checklist

Cutover (safe sequence):

- [x] Push workflow and verify at least one successful run on `maint-feb-2026` and `master`.
- [x] In GitHub repo settings, set Pages source to **GitHub Actions**.
- [x] Push a tiny docs-only commit to `master` and verify deployment URL + page content.

Status note: Pages source was switched to GitHub Actions on 2026-02-21.
Status note: Default branch was renamed from `master` to `main` on 2026-02-21.

Post-cutover hardening:

- [x] Remove `master` from `github-pages` environment deployment branch policies.
- [x] Keep only `main` allowed for deploy to `github-pages` environment.

### 3) Resolve archive/tag behavior

- [x] Audit tag/category links rendered on post pages.
- [x] Fix dead tag links on production (404 currently).
- [x] Pick one approach:
  - keep archive links and ensure generation in CI deploy path, or
  - disable archive links until fully supported.
  - Current choice: disable tag archive links in post template unless `jekyll-archives` is explicitly enabled in plugins.

### 4) Dependency and legacy config cleanup

- [x] Review and modernize `Gemfile` constraints.
- [x] Keep one analytics strategy only (config-driven).
- [x] Review old config entries and remove obsolete options safely.

Status note: legacy social `protocols` config and Open Source Protocol meta tags were removed; social preview tags now use `page.cover` -> `site.cover` -> `site.logo` fallback.

### 5) Publishing standards and checks

- [x] Keep a lightweight pre-publish checklist.
- [x] Validate local build before publishing.
- [x] Verify canonical URLs, feed links, and metadata on live posts.

### 6) Branch rename (timed)

- [x] Execute `master` -> `main` rename only after steps 1-4 are complete and deployment is verified.
- [x] Update default branch in GitHub settings and confirm Pages/Actions reference the new branch.
- [x] Update local branch tracking and any branch-specific docs/scripts.
- [x] Delete remote `master` branch after confirming stable deploy from `main`.

## Incident Recovery Notes

If deployments fail in the future and need emergency rollback:

- [ ] In GitHub repo settings, switch Pages source back to **Deploy from a branch**.
- [ ] Select `main` and `/ (root)` as source.
- [ ] Disable the Pages workflow (or leave it idle) until issues are fixed.
- [ ] Push a tiny commit to retrigger the old publish path.
- [ ] Verify homepage + latest post + feed render correctly.

## Agent Capability Plan (Required)

Goal: ensure the coding agent can fully maintain and verify this site end-to-end before publish.

### A) Local execution and preview

- [x] Make sure agent can install dependencies in this repo.
- [x] Make sure agent can run `bundle exec jekyll serve --drafts` locally.
- [x] Make sure agent can run `bundle exec jekyll build` locally.

### B) Local verification workflow

- [x] Define a standard local verification flow the agent must run for post changes.
- [x] Verify rendered output locally (content, formatting, links, metadata).
- [x] Include a local preview step so you can review before publish.

### C) Operational readiness

- [x] Document required tools for agent operation (Ruby, Bundler, Jekyll).
- [x] Ensure commands are repeatable on this machine.
- [x] Keep instructions current in `AGENTS.md` and/or `README.md`.

## Deferred / Later

- [ ] Evaluate JS ecosystem migration options (11ty, Astro) with effort estimate.
- [ ] If migration is chosen, create a separate migration plan and phased rollout.

## Post Drafting Template

Use this structure as a starting point for new posts (adapt as needed):

1. Motivation / real-world problem
2. Core idea or approach summary
3. Implementation walkthrough (step-by-step)
4. Runnable examples (SQL/TS/etc.)
5. Caveats, tradeoffs, and alternatives
6. Practical conclusion (when to apply and why)

Authoring notes:

- Keep voice conversational, first-person, and technically grounded.
- Prefer concrete examples over abstract explanation.
- Include references (docs, dbfiddle, gist) where useful.
- Preserve style and phrasing; only make minimal clarity/editorial edits.
