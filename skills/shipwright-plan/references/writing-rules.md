# Writing rules

Source: improve, Phase 4 and the `plan` / `review-plan` variants. The file skeleton is [template.md](template.md). The index skeleton is [index.md](index.md). A historical filled sample is [example.md](example.md). Do not edit those two templates.

## Before any plan file

- Record `git rev-parse --short HEAD`. Every plan stamps the commit it was written against. The executor uses it for the drift check.
- If `plans/` already exists from a previous run, reconcile. Do not duplicate. Read `plans/README.md`, keep numbering monotonic, skip findings already planned or listed as rejected, and mark superseded plans stale in the index.
- If `plans/` exists for an unrelated purpose, use `advisor-plans/` and say so.
- Finished plans stay. Numbers only increase.
- A temporary PR review gets a number too. Its Category is `review`. Register it in the index. That is decision 2.
- Excerpts come from your own reads, never from a worker's report. Before writing each plan, open every cited file yourself. A worker's line numbers are leads, not facts. A wrong excerpt fails the plan's own drift check.

## One plan, weakest executor

Write each plan for the weakest plausible executor. The template's quality bar is the checklist. These are the rules behind it:

- All context is inlined: why this matters, exact file paths, current-state excerpts, the repo's conventions with a snippet of one exemplar file. "As discussed" is a broken plan.
- Steps are explicit and ordered. Each step has its own verification command and expected output. That is principle `sequence-verifiable-units`.
- Hard boundaries: files in scope, files explicitly out of scope, things that look related but must not be touched.
- Done criteria are machine-checkable. Commands and expected results, not "works correctly."
- A test plan: what new tests to write, where, and which existing test is the pattern.
- A maintenance note: what future changes will interact with this, and what to watch in review.
- Escape hatches: "if X turns out to be true, STOP and report instead of improvising."
- Domains is one or more of `bugs`, `security`, `test`, `structure`, `perf`, `lean`. That tag is how later stages choose a domain skill.
- No secret values. Locations and credential types only.
- Non-trivial repeated work inside the plan should name a real script or command, not an inline snippet the executor is expected to retype. That is principle `build-the-lever`.

## Selection

Do not write 30 plans. Wait for the audit's selection. If nobody is available to choose, write the top 3–5 by leverage and record that default in `plans/README.md`.

Surface dependency order before numbering. A characterization test lands before the refactor it protects.

One or two files with an obvious approach: do not write a plan. Say so and hand the work to shipwright-build.

## `plan <description>`

Skip the audit. The user already knows what they want. Run recon, investigate just enough to specify it, and write a single plan. Resolve each ambiguity from the codebase first. Only what remains becomes a question. Ask one question at a time, each with a recommended answer.

## `review-plan <file>`

Critique an existing plan against [template.md](template.md) and tighten it. If you authored the plan in this same session, also have a fresh-context worker read it cold and report ambiguities. Self-critique misses gaps you fill from context the executor will not have.

## Run record and evidence appendix

Copy both sections from [template.md](template.md). Do not invent a second `record.md`. Append run-record rows. Do not rewrite earlier rows. The evidence appendix records the branch, the SHA, and links. It is a section of the plan, not a directory. Screenshot files do not go in git.

## Principles named here

`sequence-verifiable-units`, `build-the-lever`, and `outcome-oriented-execution` live in the shared principles directory. Follow the constraint in the template. Do not copy the principle files into the plan.
