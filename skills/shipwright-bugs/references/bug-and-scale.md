<!--
Adapted from ponytail-review and ponytail-audit (MIT).
https://github.com/DietrichGebert/ponytail
Bug and Scale checklists only. The report shape belongs to shipwright-review.
The repo-wide audit procedure belongs to shipwright-audit.
-->

# Bug and scale

Order of importance when several domains apply: correct, then safe, then holds under load. Safety checks live in shipwright-security. Measured slowness lives in shipwright-perf.

## Load you assume

Find the expected load in the repo (README, deploy config): one person running a script, or many users and processes at once. Judge scale against that, and say which load you assumed. When the load is unknown, say so. Do not demand a redesign for an imaginary scale.

## Bug

On one change (ponytail-review):

- Wrong result, crash, missed edge case (empty, zero, last item, rounding, time zones).
- A caller broken by the change.
- A fix applied in one caller while the shared function stays broken.

On a whole repo (ponytail-audit):

- Wrong result, crash, missed edge case (empty, zero, last item, rounding, time zones).
- Callers that disagree with what a function returns.
- The same rule applied differently in two places.

A concrete case is required: this input or situation leads to this wrong result. No case, no finding. Re-read the lines and confirm the caller exists, the value can really be empty, and the code really does what the finding says.

## Scale

Fine for one user, wrong for many:

- Check-then-write races.
- The same work done by every process.
- Memory or lists that only grow.
- A query per item.
- O(n^2) on big input.
- Per-process state that must be shared.

Same wording in ponytail-review and ponytail-audit. Judge it against the load you named. A `shortcut:` comment that names a ceiling is a recorded decision until the expected load crosses that ceiling. When the real load already crosses it, report the concrete consequence. The comment format and the ledger live in shipwright-lean and shipwright-debt.

## Shared root cause

Before editing a bug, search every caller of the function you touch, then fix the root cause once in the shared code. A patch on each caller that leaves the shared function broken is still the bug.

Two or more fixes that share one premise and fail the same gate: write the premise down and test it before another fix that assumes it (principle [attack-the-premise](../../../references/principles/attack-the-premise.md)).

## Idempotent retries

Webhooks, queues, and lifecycle steps need an answer to three questions (principle [make-operations-idempotent](../../../references/principles/make-operations-idempotent.md)):

1. What happens if this runs twice in a row?
2. What happens if the previous run crashed at every possible point?
3. Does re-execution converge to the same end state?

If any answer depends on leftover state, the operation needs a reconciliation step. Derive the step from the state that exists now.

## Shared mutable state

When concurrent actors might write the same file, branch, key, or object, first ask whether they need that same mutable object (principle [separate-before-serializing-shared-state](../../../references/principles/separate-before-serializing-shared-state.md)). Give each actor its own file, key, branch, or state directory, and merge only at the read boundary. Serialize with a lock, a single writer, or a compare-and-swap only when one shared write target is a real invariant.

## Same-interface evidence

A bug that shows up in a user-visible interface is reproduced there before the fix, and checked there after the fix, on the same screen and the same steps. A unit test does not stand in for that check. Cached or older screenshots do not count. Paths, names, and redaction live in the shared [evidence.md](../../../references/evidence.md) (shipwright-test maintains it).
