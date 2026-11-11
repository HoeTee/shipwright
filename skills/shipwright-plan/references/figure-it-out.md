# Figure it out, frame and design

Source: pstack `figure-it-out`, Phase A and Phase B. Use this when no narrower skill fits: a large migration, an ambitious multi-part change, or work a person will review after stepping away. Phases C through E (the hypothesis loop, the decision trail, the final check against the predicate) are shipwright-autopilot. This file stops when the phase list exists.

The deliverable before any code is the workflow itself: a sequence of phases that scales rigor to the task, runs as a series of checks, and leaves a decision trail a person can audit.

## Phase A. Frame

Ground first, then commit. Do not start the run until you can state:

- The definition of done as a falsifiable predicate. That is principle [prove-it-works](../../../references/principles/prove-it-works.md).
- Scope, quantified: rough units and effort, plus the blockers grounding surfaced.
- The rigor level, biased high. One-way doors and a high blast radius get more. Reversible low-stakes steps get less. Rigor is gates and artifacts, not "try harder."

Present the framing and the tradeoffs before committing to a long run. Reversible work may proceed (principle [never-block-on-the-human](../../../references/principles/never-block-on-the-human.md)), but a multi-hour run earns one checkpoint. Ask that one checkpoint as a question with a recommended answer.

## Phase B. Design the workflow

Decompose into atomic units that can land independently. Sequence the riskiest unknown first. Scaffold and verification come before features. That is principle [foundational-thinking](../../../references/principles/foundational-thinking.md).

- Build the verification harness before the work, with the baseline captured from the pre-change state, so the check reads as "old value versus new value."
- For a one-way-door design decision, run shipwright-architect. It runs shipwright-arena. Skip architect for mechanical work whose shape is already concrete. A second arena over a settled design is over-engineering. That is principle [laziness-protocol](../../../references/principles/laziness-protocol.md).
- Decide what fans out. Parallelize only across seams, and give each worker its own worktree or branch. That is principle [separate-before-serializing-shared-state](../../../references/principles/separate-before-serializing-shared-state.md). Do not over-fan. Dispatch is `skills/shipwright-how/references/hosts.md`.
- Write the designed phase list down. That list is what the person reviews. Each phase names the evidence that shows it is done.

Then stop. Hand the list to shipwright-autopilot for an unattended run, or to shipwright-build when someone is still here and the units are ordinary plan steps. shipwright-trail keeps the decision log when the run is long. Do not execute the list in this skill.

## Reply

The framing, the rigor level and why, the phase list, and what is still open. No code.
