# Quick audit, plain language

Source: ponytail-audit (MIT, DietrichGebert/ponytail). This is the `quick` effort level, and it is also the plain-language rendering for any vetted audit. It changes no code.

Audit what the user names: a folder, a package, or the whole repo. Nothing named means the whole repo, still limited by the effort table in [effort.md](effort.md). `quick` stays on hotspots and on bugs, security, and test, and it keeps about six HIGH-confidence findings. The lean deletion list below is part of this pass. Lean's ongoing rules live in shipwright-lean.

Reply in the user's language. Very simple language: short sentences, everyday words. Explain a technical term the first time you use it. The reader may never have seen this code.

## Map first

- Read the README, the deploy and build config, the dependency list, the entry points (main, routes, handlers, jobs, CLI commands), and the tests.
- Find the expected load: one person running a script, or many users and processes at once. Judge scale against that, and say which load you assumed.
- Trace the main flows end to end: where data comes in, what is stored, what goes out. Read those paths fully: input from users, money, auth, data writes, background jobs, anything shared between processes.
- A big repo: go deep where a mistake costs the most, not file by file. Say which parts you did not read.

## Look for

Order of importance: correct, safe, holds under load, tested, fast, lean. Lean still matters. Every extra line must be read, tested, and fixed later.

1. **Bug.** Wrong result, crash, missed edge case (empty, zero, last item, rounding, time zones), callers that disagree with what a function returns, the same rule applied differently in two places.
2. **Risk.** Security holes (injection, weak randomness, secrets in code, missing checks on input from users), data loss (errors swallowed, writes in the wrong order, no transaction).
3. **Scale.** Fine for one user, wrong for many: check-then-write races, the same work done by every process, memory or lists that only grow, a query per item, O(n^2) on big input, per-process state that must be shared.
4. **Missing test.** Risky logic (a branch, a parser, money, security, data writes) with no test that fails when it breaks. One good test, not coverage.
5. **Speed.** Big slowdowns are problems. Small wins (work repeated in a hot loop) are suggestions. Some software counts every millisecond.
6. **Lean.** Code that should not exist or should be smaller.
   - delete: dead code, unused options, flags and config, speculative features
   - reuse: two helpers doing the same thing (keep one, name the path)
   - stdlib or native: the standard library or platform already does it; a dependency doing what a few lines or the platform can do
   - yagni: an interface with one implementation, a factory with one product, a wrapper that only passes calls through
   - merge: near-copies that must change together
   - split: one function or class doing several unrelated jobs, so it is hard to read or test. Split by job, never by line count, and never into helpers that exist only to make a function shorter.

The deeper category checklists for a `standard` or `deep` audit are the domain skills plus [deps.md](deps.md) and [dx.md](dx.md). Do not paste them into a quick pass.

## Check before you report

- Every finding needs a concrete case: "this input or situation leads to this wrong result". No case, no finding.
- Before calling code unused, search the whole tree for it, including tests, fixtures, config, and string or dynamic references.
- A shortcut marked with a `shortcut:` comment (or the older `ponytail:` prefix) that names its limit is a decision, not a finding, unless the expected load already crosses it. The ledger of those comments is shipwright-debt.
- Propose the smallest fix that works. Prefer fixes that delete code. Never add layers, frameworks, or config the problem does not need.
- No style taste, no "consider", no vague worries.
- Never reproduce secret values. Cite `file:line` and the credential type only.

## Output

Start with `What this repo does:` in two or three sentences, and the load you assumed.

Then the findings in three groups, most important first. Skip empty groups.

- **Must fix.** Bug, security, data loss, or it breaks at the expected load. These are P0 or P1.
- **Should fix.** Risky code without a test, real slowness, duplication, a function that mixes jobs, code that should not exist. These are P1 or P2 when they are real defects.
- **Nice to have.** Small speed-ups and shorter forms. These are non-blocking suggestions. Do not force them into P2.

Number findings across all groups, so the user can say "fix 2 and 5". At most 20 findings. If you left smaller ones out, say how many. Every finding has all four parts, each one or two short sentences:

```text
2. Orders land on the wrong day (`billing/close_day.py:L40-52`)
   - What this is: At midnight this job closes the day and bills all orders of that day.
   - Problem: It takes "today" from the server clock, which runs in UTC. An order placed at 00:30 in Berlin is billed on the day before.
   - Fix: Compute the day once in the shop's time zone. One line, nothing else changes.
   - If we skip it: Late orders show the wrong date, and accounting fixes them by hand.
```

End with:

- `Verdict:` one line, healthy, or what to fix first.
- `Lean: -<N> lines, -<M> dependencies possible.` when lean findings exist.
- `Not checked:` the parts you did not read or could not run.

Nothing found: `What this repo does:`, then `Healthy. Nothing to fix.` and one line on what you checked.

One-shot report. Changes no code. The P0/P1/P2 record for anything that will become a plan still uses the shape in [subagent-brief.md](subagent-brief.md).
