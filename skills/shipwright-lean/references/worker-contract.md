# Worker contract

Inline this file into the brief of an independent implementer who writes code. The parent loads it only when dispatching that implementer, not on every task. Do not paste `smallest-change.md` into the parent. The two lines in `references/principles/laziness-protocol.md` are not a substitute for this contract. Fewer lines are not this contract. The implementer does not inherit the conversation.

Before writing, load these when the path resolves:

- `skills/shipwright-lean/SKILL.md`
- `skills/shipwright-lean/references/smallest-change.md`

Those files own the ladder and the level. This contract still binds when a path does not resolve. A missing file is not permission to keep only a shorter summary.

## Reuse first

Take the first option that fully works:

1. Skip features, options, and flexibility nobody asked for.
2. Reuse what this repo already has, the way the surrounding code uses it.
3. Use the standard library or platform. A house component beats a native widget.
4. Use an installed dependency. Do not add one for a few lines.
5. One line a reader gets at a glance, when that line is the whole change.
6. Otherwise the minimum code that works.

## Complete

The diff stays small and finishes the change. Include the callers, tests, fixtures, config, and exports the change must reach or would break. Do not leave them out to shorten the diff.

## Never cut

Do not cut these to save lines: validation at trust boundaries, error handling that prevents data loss, security, accessibility, the calibration real hardware needs, anything the user asked for.

## Shortcut

A known ceiling is a comment: `shortcut: <the limit>, <when to upgrade>`. An older `ponytail:` comment with the same two parts counts. The comment does not exempt security, data integrity, or a project requirement.

## Level

Stay at the level the user last set. Full is the default. Do not reset it because the work moved to a new brief.
