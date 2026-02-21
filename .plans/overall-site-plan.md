# Overall Site Plan (Feb 2026)

This file tracks site improvements we intend to make, including deferred work.

## Immediate Completed Work

- [x] Add `AGENTS.md` with authoring rules, privacy policy, and publish workflow.
- [x] Fix canonical base URL to custom domain (`https://ryanguill.com`).
- [x] Remove duplicate hardcoded analytics snippet and use config-driven include.

## Modernization Plan (Next)

### 1) Stabilize local toolchain

- [ ] Add `.ruby-version` and document supported Ruby/Bundler versions.
- [ ] Ensure `bundle install` works on a clean machine with clear setup docs.
- [ ] Decide whether to pin Jekyll to an explicit version in `Gemfile`.

### 2) Move to GitHub Actions deploy flow

- [ ] Add a GitHub Actions workflow to build and deploy the static site.
- [ ] Build with explicit Jekyll/Bundler versions in CI.
- [ ] Deploy generated site via Pages action so plugin behavior is predictable.
- [ ] Keep `master` as source branch unless intentionally changed.

### 3) Resolve archive/tag behavior

- [ ] Audit tag/category links rendered on post pages.
- [ ] Fix dead tag links on production (404 currently).
- [ ] Pick one approach:
  - keep archive links and ensure generation in CI deploy path, or
  - disable archive links until fully supported.

### 4) Dependency and legacy config cleanup

- [ ] Review and modernize `Gemfile` constraints.
- [ ] Keep one analytics strategy only (config-driven).
- [ ] Review old config entries and remove obsolete options safely.

### 5) Publishing standards and checks

- [ ] Keep a lightweight pre-publish checklist.
- [ ] Validate local build before publishing.
- [ ] Verify canonical URLs, feed links, and metadata on live posts.

## Agent Capability Plan (Required)

Goal: ensure the coding agent can fully maintain and verify this site end-to-end before publish.

### A) Local execution and preview

- [ ] Make sure agent can install dependencies in this repo.
- [ ] Make sure agent can run `bundle exec jekyll serve --drafts` locally.
- [ ] Make sure agent can run `bundle exec jekyll build` locally.

### B) Local verification workflow

- [ ] Define a standard local verification flow the agent must run for post changes.
- [ ] Verify rendered output locally (content, formatting, links, metadata).
- [ ] Include a local preview step so you can review before publish.

### C) Operational readiness

- [ ] Document required tools for agent operation (Ruby, Bundler, Jekyll).
- [ ] Ensure commands are repeatable on this machine.
- [ ] Keep instructions current in `AGENTS.md` and/or `README.md`.

## Deferred / Later

- [ ] Evaluate JS ecosystem migration options (11ty, Astro) with effort estimate.
- [ ] If migration is chosen, create a separate migration plan and phased rollout.
