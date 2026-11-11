<!--
Lean checklists from ponytail-review (one change) and ponytail-audit
(whole repo), MIT, https://github.com/DietrichGebert/ponytail
The report shape stays in shipwright-review and shipwright-audit.
Shortcut handling also includes the lifecycle rows for shortcut comments.
-->

# Lean checks

Lean still matters: every extra line must be read, tested, and fixed later. Code that should not exist, or should be smaller.

## On one change

- delete: dead code, unused options, speculative features.
- reuse: the repo already has this helper (name the path).
- stdlib / native: the standard library or platform already does it; a new dependency for a few lines.
- yagni: abstraction with one implementation, config nobody sets.
- merge: near-copies that must change together.
- split: one function doing several unrelated jobs, so it is hard to read or test. Split by job, never by line count, and never into helpers that exist only to make a function shorter.

## On a whole repo

- delete: dead code, unused options, flags and config, speculative features.
- reuse: two helpers doing the same thing (keep one, name the path).
- stdlib / native: the standard library or platform already does it; a dependency doing what a few lines or the platform can do.
- yagni: interface with one implementation, factory with one product, wrapper that only passes calls through.
- merge: near-copies that must change together.
- split: one function or class doing several unrelated jobs, so it is hard to read or test. Split by job, never by line count, and never into helpers that exist only to make a function shorter.

Before calling code unused, search the whole tree, including tests, fixtures, config, and string or dynamic references.

A concrete case is required. Style taste, "consider", and vague worries are not findings. Prefer a fix that deletes code. Do not add a layer, a framework, or config the problem does not need.

When the load is unknown and the code could be shorter, say the load is unknown. If there is no actual defect and no project rule, the shorter form is a non-blocking suggestion. Do not demand a redesign for an imaginary scale, and do not block on it.

## Shortcut comments

Form: `shortcut: <the limit>, <when to upgrade>`. Older code may say `ponytail:`.

A marker that names its limit is a decision, not a finding, unless the expected load already crosses that limit. When real use crosses it, report the concrete consequence and the severity. A marker with no condition for looking again is usually a suggestion (`no-trigger` in the shipwright-debt ledger).

The comment does not exempt security, data integrity, or a project requirement. A permission hole beside a ceiling that still holds is still a security finding. Keep the capacity decision.

shipwright-debt collects the markers. The scan is `skills/shipwright-debt/scripts/scan_shortcuts.py`.
