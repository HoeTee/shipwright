---
title: How Shipwright works
subtitle: One skill does one stage. A person makes the merge decision.
lang: en
template: doc
theme: blueprint
mode: light
source: Current skill instructions in this repository
---

Shipwright is a set of skills for the coding lifecycle.
You name the stage, or you ask shipwright-flow to select the stage.
The agent does not merge unless you authorize shipwright-land.

## A The short path

Task goes to Plan, then Build, then Review.
The Review step and the Fix step loop until no finding blocks the change.
A clear review goes to Ship, then to a human merge.
The README picture shows this path.
The next section shows every stage.

## B The path

```flow TB
(Task) -> shipwright-flow
shipwright-flow -> Understand
Understand -> Discover
Discover -> Plan
Plan -> Build
Build -> Review
Review -> shipwright-fix: blocking finding
shipwright-fix -> Review: new commit
Review -> shipwright-ship: no blocker
shipwright-ship -> shipwright-signoff
shipwright-signoff -> *shipwright-land: you allow merge
group Review loop: Review, shipwright-fix
```

Enter at a stage you already know.
A small and clear change can go to shipwright-build.
An audit does not become a plan until you ask for a plan.

After you open a pull request, each AI review counts.
The default limit is 3.
shipwright-fix defines this limit.
Work before the pull request does not count.
The count does not reset when you change method, resume a session, or open the same pull request again.

shipwright-ship stops when the pull request can merge.
shipwright-ship does not merge.
shipwright-signoff prepares the packet for a person.
shipwright-land merges one head after a non-author verifies it and you allow the merge.

## C Stage results

| Stage | Skill | Result |
| --- | --- | --- |
| Select stage | shipwright-flow | Stage, scope, and authorization |
| Understand | shipwright-how, shipwright-why | How the code runs, and why it is built this way |
| Discover | shipwright-audit, shipwright-diagnose | Ranked findings, or a reproduced bug |
| Plan | shipwright-plan | A plan in plans/ that a new agent can run |
| Build | shipwright-build | The change and evidence from the real product |
| Review | shipwright-review, shipwright-fix | Findings on one commit, then a fix inside the limit |
| Pull request | shipwright-ship, shipwright-signoff, shipwright-land | A pull request, a human packet, and a merge only when you allow it |

## D Sources

[shipwright-flow](../../skills/shipwright-flow/SKILL.md) · [shipwright-fix](../../skills/shipwright-fix/SKILL.md) · [shipwright-signoff](../../skills/shipwright-signoff/SKILL.md) · [shipwright-land](../../skills/shipwright-land/SKILL.md)
