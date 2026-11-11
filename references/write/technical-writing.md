# Technical Writing

Write so a tired engineer understands on the first read. Apply all four layers below. Also load **unslop** for AI-tell cleanup.

## Rules above the layers

- Cut every word that does no work.
- Prefer the short everyday word.
- If a rule makes a sentence worse, fix another way or leave it.
- The codebase is the word list: real symbol/file/flag/command names.
- Don’t invent jargon. Propose new offenders as additions to **unslop**, don’t silently edit that skill mid-flight.

Vary rhythm: mix short and medium sentences; avoid metronome lists of equal length.

## Layer 1 — Diátaxis

Pick the genre: tutorial (learning by doing), how-to (goal-oriented steps), reference (accurate inventory), explanation (understanding). Don’t mix genres in one page without clear section labels.

## Layer 2 — Structure

Lead with the conclusion or task. One idea per paragraph. Put actions in imperative steps. Put concepts before details. Tables for comparisons; lists for sequences.

## Layer 3 — Clarity mechanics

Define acronyms once. Keep links descriptive. Show commands in copyable blocks. Separate prerequisites. Call out irreversible steps. State defaults and ranges for flags.

## Layer 4 — Review pass

Read aloud once. Delete throat-clearing. Check every claim against the code or UI you cite. For repo docs, verify paths by reading the repository. Do not invent the tree.

## Delivery

PR descriptions, READMEs, RFCs, and commit messages all follow this skill. For a long explainer meant to be shared, hand the page to shipwright-recap. Do not use a host-only canvas tool.
