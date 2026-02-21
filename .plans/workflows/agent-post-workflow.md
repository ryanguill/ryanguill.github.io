# Agent-Assisted Post Workflow

This workflow standardizes how we go from rough ideas to a publish-ready post.

## 1) Start a rough draft

Run:

```bash
./scripts/new-post-rough-draft "your topic idea"
```

This creates a dated file in `.plans/rough-draft/` from the template.

## 2) Capture ideas fast

In the rough draft file, add any disconnected thoughts:

- thesis fragments
- title ideas
- examples/snippets
- caveats
- references

Do not optimize for polish at this stage.

## 3) Agent interview phase

Ask the agent to:

1. Read the rough draft file.
2. Ask focused clarification questions.
3. Propose 2-3 title options.
4. Build a concise working brief and outline.
5. Identify missing proof/examples.

## 4) Draft phase

Once the thesis/outline are stable, ask the agent to draft into `_drafts/`:

- `_drafts/YYYY-MM-DD-slug.md`

The rough draft file remains the planning record.

## 5) Iteration modes

Use one mode at a time to keep edits intentional:

- `Expand`: add substance/examples.
- `Tighten`: improve flow and clarity only.
- `Polish`: spelling/editorial checks, minimal rewrites.

## 6) Final QA and publish

Run the pre-publish checklist in `AGENTS.md` / `README.md`:

1. Local build
2. Local preview
3. Spell check
4. Clarity pass
5. Editorial checks
6. Push and verify deploy
