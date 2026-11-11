# How procedure

Source: pstack `how`, with the host tooling map removed. Dispatch is [hosts.md](hosts.md). The Chinese operating card is `SKILL.md`.

Explore the codebase to answer "how does X work?" Produce an architectural explanation at the level of a senior engineer onboarding onto a subsystem: enough for a working mental model, not annotated source code.

Every explorer and every explainer is an independent read-only worker. Read the `how explorer` and `how explainer` lines from the model file in [hosts.md](hosts.md). One explainer does not also explore a complex question.

## Assess complexity

If the scope is ambiguous, state the interpretation and explore. The user can redirect.

- **Simple** (a single module, a small utility, a narrow question such as "how does function X work"): no explorers. One explainer explores and explains in one pass, built from [explainer-prompt.md](explainer-prompt.md) without the Explorer Findings section. Go to Present.
- **Complex** (a subsystem spanning multiple files or services, a cross-cutting feature, a full architectural overview): Explore, then Synthesize.

When in doubt, take the simple path.

## Explore (complex only)

Decompose the question into 2 to 4 angles, each a distinct slice of the subsystem. Dispatch all explorers in a single round. Each prompt is [explorer-prompt.md](explorer-prompt.md) with its angle filled in.

## Synthesize (complex only)

Once all explorers have returned, dispatch one explainer with [explainer-prompt.md](explainer-prompt.md) and every explorer's findings filled in.

## Present

Present the explainer's output. Light edits for clarity or context from the conversation are fine. Do not substantially rewrite it.

## Output format

Use the sections defined in [explainer-prompt.md](explainer-prompt.md). Drop any that do not apply: Overview, Key Concepts, How It Works, Where Things Live, Gotchas.

## What the explanation must establish

Keep the question's scope. Do not start a review or a design.

1. Read the project entry points and any existing index first. Locate the module the user's action actually hits.
2. From that entry, trace the input source, branches, state changes, return value, and side effects. When explaining a function, name its inputs and outputs.
3. Across an API, process, or script, check the fields on both sides, who owns the data, and how failure propagates. Do not stop at a list of function names.
4. Organize the answer by behavior a user can observe. Attach the current `file:line`. Design motive goes to shipwright-why.
5. Keep using context that is already valid. Run an entry point only when new behavioral evidence is required, and only inside the granted authorization.
6. Say when the code does not determine the answer. A static inference is not a run that passed.

Positive: explain how an upload creates a task, who consumes the task, and how the result comes back, pointing at the code.
Negative: tell a story from module names, or write a static inference as if it had been run.

## Architecture facts for a rules draft

When the caller is drafting `CLAUDE.md` or `REVIEW.md`, add the table in [architecture-facts.md](architecture-facts.md) on top of the call chain. Record only the existing structure that this review needs. Do not start a design, an implementation, or a comparison of options. Hand the table to shipwright-rules. Do not write the project files.

## Domain handoff

This skill does not carry domain checklists.

- Call chain and state ownership: shipwright-bugs.
- Existing tests and the commands that run them: shipwright-test.
- Hot path: shipwright-perf.

Large raw output stays with the worker. The main thread keeps the findings. That is principle [guard-the-context-window](../../../references/principles/guard-the-context-window.md) in the shared principles directory.
