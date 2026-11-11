<!-- Host note: Codex, Claude Code, and OpenCode follow this procedure. Spawn a separate worker when the host has subagents. Models come from shipwright-setup. Verify on the product's real interface. -->

Status: disabled. Do not read this on an ordinary task. autopilot-full is not in shipwright. Never merge.

### Autopilot-stack

Do not run a playbook that merges. The no-merge rules below replace that playbook.

1. **In place of step 5, stop at verified.** Stop when each PR is verified and green at its current head, then hand the PRs to the operator. After the handoff, nobody pushes without the operator's go. Every loop tick prompt names this file, so each tick sees the no-merge rule.
2. **Stack a PR only when it builds on another PR.** This is the one exception to step 3. Base the PR on the other PR's branch in place of trunk, per **Size and stacks** in `playbooks/opening-a-pr.md`. In place of step 2's rebase onto trunk, each PR rebases onto its parent PR's branch, and the stack root rebases onto trunk. A new head on the lower PR restacks the PRs above it, and a PR whose `git patch-id` the restack leaves unchanged keeps its verdict.

**Reply:** list each PR with its verdict, in place of what merged.

## No-merge operating rules

1. The operator's gates come first. Work the operator named as theirs stops at merge-ready.
2. One owner per PR. The owner builds, opens the PR when that is authorized, proves the change on the real interface, and follows the babysit procedure to green. The owner does not merge.
3. Run shipwright-write and shipwright-comments before review.
4. Force-push only the owner's own branch, with `--force-with-lease` pinned to the SHA last pushed. On a push the owner did not make, stop and report.
5. Run owners in parallel off trunk. The only stack exception is the source step above: a PR that builds on another PR rebases onto that parent, and the stack root rebases onto trunk.
6. A verifier that did not write the code checks the current head. A verdict covers one SHA. Compare patch-id with shipwright-land before reusing a verdict.
7. Stop when each PR is verified and green at its current head. Hand the list to the operator. After that, nobody pushes without the operator's go.
8. Do not grant or bypass an approval the forge enforces. A disabled or soft-failed check stays visible.
