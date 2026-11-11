<!--
Adapted from ponytail-review and ponytail-audit, Risk item (MIT).
https://github.com/DietrichGebert/ponytail
Plus the lifecycle rule that a shortcut comment does not exempt security
or data integrity (code-review-lifecycle adversarial review and the
shortcut rows of validation-scenarios).
-->

# Risk

Ponytail's Risk item, same wording for one change and for a whole repo:

- Security holes: injection, weak randomness, secrets, missing checks on input from users.
- Data loss: errors swallowed, writes in the wrong order, no transaction.

On a whole-repo pass the secrets phrase is "secrets in code". On a change pass it is "secrets". Both apply: a secret newly introduced in a diff and a secret already committed are both findings. Name the credential type and the `file:line` only.

Weak randomness means a non-cryptographic generator used for a secret, a token, or an identifier that grants access. The safer API is the platform's cryptographic generator. Do not include a sample of a weak generator in the finding.

## Safer API, not a demonstration

For every Risk finding, name the code pattern, the production impact, and the safer API or the validation boundary. Plans stay at code changes, configuration changes, and tests. No runnable demonstration string. No step-by-step misuse.

## What is not a finding

- A standard platform convention, unless this implementation adds risk beyond that convention.
- A tradeoff recorded in an ADR or decision doc, unless the code has drifted from the doc. Drift is the finding.
- A `shortcut:` or older `ponytail:` comment whose ceiling still holds, when the comment is about a capacity limit and not about a missing security check.

## What a comment cannot waive

When a `shortcut:` or older `ponytail:` comment is present, check the recorded ceiling and the condition for looking again.

- The ceiling still holds: do not re-report the accepted limit.
- Real use already crosses the ceiling: report the concrete consequence.
- The comment names no condition for looking again: that is usually a suggestion, unless the line is a security or data-integrity hole.
- The comment never exempts security, data integrity, or a project requirement. A permission hole next to a still-valid ceiling is still reported. Keep the capacity decision if it still holds, and report the security issue on its own.

Lifecycle states the same rule: 保留仍成立的设计决定，安全问题照常核实报告。注释不能成为安全或数据约束的豁免。

## Dependency advisories

Read-only ecosystem audit, then filter:

```bash
npm audit --json | python skills/shipwright-security/scripts/filter_advisories.py --ecosystem npm
pip-audit --format json | python skills/shipwright-security/scripts/filter_advisories.py --ecosystem pip
cargo audit --json | python skills/shipwright-security/scripts/filter_advisories.py --ecosystem cargo
```

Run the command the repo already uses. Do not install packages to perform the audit. Report a critical or high advisory only when it affects reachable runtime code or a build or distribution path. The script does not fetch exploit details and does not run them.
