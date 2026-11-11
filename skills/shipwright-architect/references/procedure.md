# Architect procedure

Source: pstack `architect`. The host tooling map is removed. Dispatch is `skills/shipwright-how/references/hosts.md`. Red-flag screen: [design-red-flags.md](design-red-flags.md). Rationale shape: [rationale-template.md](rationale-template.md). Each candidate's prompt: [runner-prompt.md](runner-prompt.md).

Sketch types, function signatures, class shapes, and module boundaries with `not implemented` bodies and pseudocode. Synthesize across more than one candidate, then fill in code against the chosen sketch.

The caller's usage is written first. The type sketch is derived from it.

## Phase A. Ground

Build a real mental model of every system the new code touches. Run shipwright-how over the relevant subsystems. Naming a file is not grounding. Produce the architectural explanation how prescribes. If the design redefines ownership or layering, also run shipwright-why on the existing shape so the rationale becomes a constraint, not a guess.

Skip Phase A only when the work is genuinely greenfield with no surrounding system to integrate.

## Phase B. Sketch

Run shipwright-arena with the design-sketch task and the Phase A grounding. Pass [runner-prompt.md](runner-prompt.md) as each runner's prompt. Do not copy arena's phases into this file. What this phase adds:

- Take runners from the `architect runners` line in the model file from the host dispatch note. If that line is missing, use two runners on the host's strongest available models from two families, and say which. Alias and rejected entries follow shipwright-arena.
- Design it twice. Require at least two structurally distinct candidates before synthesis, even when the first looks sufficient. That is principle `exhaust-the-design-space`. Whole-shape alternatives, not point fixes inside one shape.
- Screen every candidate against [design-red-flags.md](design-red-flags.md) before synthesis. Assume the next contributor is an agent that sees only the files it opened, copies the nearest example, and takes the shortest path that compiles. Prefer the design where a change that looks right from one file is right for the whole repo. shipwright-structure owns the ongoing structure checks. This list is the screen the design step runs.
- Compare viable candidates on interface depth. Prefer the design that hides more complexity behind a smaller, simpler public surface. A rich interface can keep call chains short by concentrating capability instead of scattering it across layers.

Arena returns one synthesized design package. Its synthesis decision fills the rationale's "Synthesis decision" section.

## Phase C. Agree

Default: proceed directly to implementation with the synthesized design. No human checkpoint.

Opt in to a checkpoint when the invoker explicitly asks to stop and show the design before implementing. Then surface the synthesized design and pause.

The synthesis can ship as its own commit either way, as the scaffold-first reading of principle `foundational-thinking`. Planned and scoped breakage during fill-in is fine, per principle `outcome-oriented-execution`. For adversarial pressure on the design before implementing, run shipwright-interrogate on the synthesized sketch.

If the human pushes back on the shape, in a checkpoint or after the fact, treat that as Phase A evidence. Re-ground and re-run Phase B before writing more code.

## Phase D. Implement against the sketch

Replace `not implemented` bodies with code, and pseudocode with logic. The synthesized sketch is the contract. Deviations are signal to surface, not friction to absorb silently. If a function needs a parameter the sketch did not anticipate, ask whether the sketch was wrong, the requirement was missed, or the implementation is overreaching.

This phase writes code only when the mode is `change` and the user authorized local edits. In `plan` mode, stop at the sketch and the rationale and hand them to shipwright-plan.

## Phase E. Scrap when the architecture is wrong

If implementation keeps producing friction the sketch cannot absorb, throw the sketch out. Do not bolt fixes onto a wrong design. That is principle `redesign-from-first-principles` and principle `fix-root-causes`.

The signal is a pattern, not a single instance.

- The same shape of workaround appearing repeatedly across unrelated code.
- Multiple unrelated edge cases that all need special-case branches.
- Types that need escape hatches (`any`, casts, optional fields always set in practice) to compile.
- The "we need a lock" reflex when the sketch said the state was not shared.
- Callers having to know the abstraction's internal rules to use it.
- Two or more independent Phase D deviations of the same shape.

Use judgment. A few edge cases do not condemn an architecture. Some problems are legitimately complex. Complexity in the data is not complexity in the design.

When you scrap:

1. Re-run shipwright-how over what has been built.
2. Redesign as if the new constraints had been day-one assumptions.
3. Subtract before adding. That is principle `subtract-before-you-add`. The new sketch should be smaller than the old one before it grows.
4. Return to Phase B and re-run arena.

## Outputs

One file with new types and signatures for small changes. A module map plus type definitions for larger work. The rationale ships alongside, shaped per [rationale-template.md](rationale-template.md), including the usage sketch and the synthesis decision.

## Principles named in the runner

`separate-before-serializing-shared-state`, `encode-lessons-in-structure`, `boundary-discipline`, `make-operations-idempotent`, `laziness-protocol`, `minimize-reader-load`, and `model-the-domain` are named in [runner-prompt.md](runner-prompt.md). They live in the shared principles directory. The runner already states the constraint on the same line. Do not copy the principle text into the sketch.
