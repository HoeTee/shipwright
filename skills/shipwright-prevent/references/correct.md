<!--
Adapted from the pstack correct skill.
The host tooling map is replaced with a host-neutral note.
-->

# Make the mistake impossible

The user keeps correcting agents in this repo for the same mistakes. Change the repo so the next agent cannot make them.

Assume every contributor is an agent that sees only the files it opened, copies the nearest example, and takes the shortest path that compiles. Design the repo so a change that looks right from one file is right for the whole repo.

Principle `encode-lessons-in-structure` says the same thing in one line: the second time you write an instruction, encode it. If the lesson needs judgment and cannot be encoded, make the instruction more prominent and add an example of the failure. When a structural fix exists, use only that fix. The prose is the symptom. The principle file lives in shared `references/principles/`.

## Find the mistake classes

First, read recent commits, reverts, review comments, agent instruction files, and comments that explain workarounds. Group the mistakes into classes. A class counts once it has happened twice.

## Fix each class at the highest level that works

1. **Eliminate it with architecture.** Give each piece of state one owner and each task one supported way. Hide internals so the wrong import fails. Replace hand-synced lists with one source of truth. Delete old ways and dead code an agent would copy. The red flags are in shipwright-structure.
2. **Enforce it with types so the bad state cannot be written.** If bad code still compiles, add a lint or CI check whose error names the file, type, or function to use instead. If the pattern is already common, fail only when a change adds more.
3. **Test the behavior.** Fix or delete any test that still passes when the behavior it checks breaks, or that fails when only the internals change. Principle `test-behavior-not-implementation` is the shared form.
4. **Write docs or agent rules last, only for judgment calls.** Nothing fails when an agent skips them.

## Fix and prove

Then fix the most frequent classes now, one commit each. Prove each new check fails on a real past mistake. Run the same command locally and in CI. Exceptions go on the offending line with a reason, an expiry date, and a human's approval.

`scripts/check_rule_table.py` reads the rule table and exits non-zero when a row is enforced only by prose.

## Keep the rule table

Last, keep a table in the agent instruction file that pairs each rule with what enforces it. When the user corrects you, fix the mistake and add the rule. If the rule was already there and nothing enforces it, that is a repeat, so fix it at the highest level in the same change. Drop a rule once its mistake cannot happen.

The table uses English headings:

```markdown
| Rule | Enforcement |
| --- | --- |
| One owner for order status | import of order.internal fails the build |
```

**Reply:** each class with its evidence, the level you picked, and why a higher level did not work.

## Platforms

Codex, Claude Code, and OpenCode follow the same ladder. Read the repo with the host's file tools. Edit only what the current authorization allows. A check that should fail the build belongs in the repo's existing lint, typecheck, or test command, the one CI already runs.
