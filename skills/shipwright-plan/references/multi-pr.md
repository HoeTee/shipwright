# Multi-PR plan

Source: pstack `playbooks/multi-phase-plan.md`. **Off unless the user explicitly enables a multi-PR program.** A normal shipwright plan uses [template.md](template.md), one file per change, and does not use this skeleton.

Shipwright does not merge by itself. The source playbook's self-merge option is not part of this plugin. When this reference is enabled, the operator lands the PRs. A stack uses shipwright-autopilot's stack reference. A standing program uses its orchestrate reference. Both of those are off unless that skill enables them.

You own the plan, not the code. The plan is a checklist an owner runs box by box and the operator audits from the evidence. Do not implement.

1. When the change is one or two files with an obvious approach, skip the plan. Say so and stop. Hand the work to shipwright-build.
2. Settle an open question by prototype before you write, one prototype per question, through shipwright-prototype. Keep the branch, the SHA, and the screenshot links for Appendix A. Ask the operator only about a product or preference call that no run can settle. Give options. That is principle [never-block-on-the-human](../../../references/principles/never-block-on-the-human.md).
3. Explore with independent workers. Each returns file pointers, conventions, test commands, and entry points. No inlined dumps. That is principle [guard-the-context-window](../../../references/principles/guard-the-context-window.md).
4. Copy the skeleton below into the plan file and fill every placeholder. Write it under `plans/` (or `advisor-plans/`) unless the operator names another path. Keep every heading and every sub-block in the order shown. One section per PR. One PR is one change with its own evidence. That is principle [sequence-verifiable-units](../../../references/principles/sequence-verifiable-units.md). Name the execution reference in "How to read this".
5. Write the body as a how-to. Appendices hold explanation and reference. Each heading states the task or the finding. No long dashes. No mid-sentence colons. Then run shipwright-write's wording pass.
6. Run `node skills/shipwright-autopilot/scripts/check-plan.mjs <plan.md>` and fix every line it prints. The checker is the original script in shipwright-autopilot. It is not a default step of an ordinary plan. That is principle [encode-lessons-in-structure](../../../references/principles/encode-lessons-in-structure.md).
7. Hand back. Post the plan path and the script's output, then stop. Execution starts on the operator's explicit go.

## Verification rule

Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked. That sentence is the verification rule. Every verification block opens with it. The live block is mandatory.

Ten lanes at the PR head drive the real surface. Each lane is one box with a concrete scenario, the screenshot it saves, and its pass predicate. Screenshot files go to `/tmp/shipwright-<plan-id>/<sha7>/worker-<n>/laneNN-<slug>.png`. One lane is the regression lane against trunk. It runs the same load-bearing scenario on trunk and head. If trunk does not have the feature, the lane records that fact and gates the behavior the diff adds plus the end state the user waits for, instead of inventing a trunk result.

The perf gate is dual-sided. Trunk and head must both produce the named metric. If trunk lacks the feature, also isolate the work the diff adds and set an absolute budget for that work plus the end-to-end state the user waits for. Do not claim a ratio between unlike scenarios. The perf block names the metric, the interleaved probe, the trunk baseline measured first, and the rule with the number that fails.

A PR that changes an interaction is review-gated. The operator reviews it before merge, with screenshots and a 30 to 60 second video. shipwright-signoff owns that packet. This checklist only reserves the boxes. A PR that changes no interaction writes `**Review gate.** None. <PR id> is not review-gated.` and no boxes under it.

## Surface

Drive the real surface. A browser, Electron, or web UI is driven in the browser. A CLI or TUI is driven from the terminal. Native mobile uses the simulator the repo already has. A PR that touches two surfaces gets lanes on both. A surface you cannot drive is a risk in Appendix C, and its live block still names how each lane is driven.

## Skeleton

Copy from the next heading down. Replace every `<placeholder>`.

````markdown
# <Program> plan

<Under ten lines. What changes, for whom, the rule the program enforces, and the PR ids in order.>

## How to read this

One box is one unit of work. Every box names the evidence that checks it. A nested box is a sub-step of the box above it. Check a box only when its evidence exists, a file, a log line, a screenshot, a test run, or a SHA. The body is a how-to. The appendices explain and record.

The program runs the named shipwright-autopilot reference (stack or orchestrate). Both stay off unless that skill enables them. Shipwright does not merge. <Who stops at merge-ready, and which PR ids are the operator's items.>

Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.

## Program checklist

### Arm the program

- [ ] State the protocol and this plan to the operator, then stop. Start execution only on the operator's explicit go.
- [ ] Read these from trunk at program start. Re-read them at every tick.
  - [ ] `git show origin/main:<the shipwright-autopilot reference this program named>`
  - [ ] `git show origin/main:skills/shipwright-swarm/SKILL.md`
  - [ ] `git show origin/main:<the surface-driving notes this program uses>`
  - [ ] `git show origin/main:skills/shipwright-ship/SKILL.md`
  - [ ] `git show origin/main:skills/<each other skill the program uses>/SKILL.md`
- [ ] On the operator's go, arm a one-hour cadence with the tick prompt below. Never leave the cadence to memory. If the host cannot schedule it, the operator re-invokes the tick.
- [ ] Use this tick prompt, verbatim. "Re-read the execution reference from trunk. Audit the operation against it and fix drift in this tick. Probe every active lane and judge progress by side effects only. Stand down a stuck lane and dispatch its replacement now. Then post a short status message to the operator in chat only when the audit found a tracked change that no earlier status message reported, such as a PR opened, a code-ready head, a round launched or closed, a verdict, a merge, a stuck agent and the action taken, a blocker added or cleared, or a decision only the operator can make. Name every such change and nothing else. Do not repeat a table, the merged list, or an unchanged blocker. If the audit found none, end the turn with no reply text. Either way, log this tick's row in the decision trail. The row names the items reported, or none."
- [ ] On the operator's hold or stand-down, send every owner a zero-writes order at once.

### Spawn owners

- [ ] Spawn one owner per PR with the lifecycle the execution reference names.
- [ ] Follow this dependency graph. Start dependent work only after its parent merges, or base it on the parent branch when the execution reference stacks.
  - [ ] <PR id> and <PR id> are independent and first. Both branch from `main`.
  - [ ] <PR id> after <PR id>.
- [ ] Hold the file boundaries. <PR id or class> touches only `<glob>`.
- [ ] Hold the review gate. <PR ids> change an interaction. They wait for the operator's review in chat with screenshots and a video before merge. shipwright-signoff holds that review.

### PR mechanics, for every PR

- [ ] Resolve the forge once. Default to `gh`. If `command -v origin` succeeds and Origin can resolve the repository, use `origin pr` for every PR operation. Record any fallback to `gh`. Never require `gt`.
- [ ] Open the PR ready, never draft, per shipwright-ship. Use the run's built-in PR tool when it has one, else `origin pr create --status open --base <base-branch>` or `gh pr create --base <base-branch>` according to the resolved forge. A stack child targets its parent branch.
- [ ] Run the repo's lint and typecheck once before the PR-facing push. Push with hooks on.
- [ ] Run shipwright-write's wording pass before each commit and shipwright-comments before review.
- [ ] Triage every review-bot comment per shipwright-ship's triage notes.
- [ ] Rebase onto current trunk before the code-ready report. Keep that merge base in fix rounds. Rebase again only at merge prep, on a `git merge-tree` conflict with trunk, on a CI failure that comes from a change on trunk, or when a known concurrent change to the same files lands.

### Verdict and merge, for every PR

- [ ] A full parallel pass runs once, at the code-ready head, per shipwright-swarm. Another full pass runs only for new behavior, a redesign, or a large new diff. A rebase, a merge-conflict resolution, or a minor fix gets a single verifier at the new head, and a wording-only change gets none. One pass gates the lane. The ten live lanes from the PR's **Verify, live** block. The perf lane from its **Verify, perf** block. Two or more audit lanes, each with its own focus, that read the diff and the receipts and distrust the PR body. The root reads the receipts in the merge-ready report before the verdict.
- [ ] Judge every finding by the execution reference's blocking rule. The verdict is clean when none blocks. A failure on trunk behavior in a lane marked `Regression lane against trunk.` is recorded against trunk and does not block the PR. A new head gets a fresh verdict, except for results that stay valid under the patch-id rule in shipwright-land.
- [ ] <The handoff rule. Shipwright does not merge. The operator lands PRs bottom-up after shipwright-land's patch-id check.>

### Boot recipe, for every live lane

Each live lane runs at the PR head and drives the real surface.

- [ ] `git fetch origin <head-branch> && git checkout <head SHA>`.
- [ ] <Start the backend and the surface. Wait for ready.>
- [ ] <Deliver input only through the real surface. Name the read-only diagnostics.>
- [ ] Save every screenshot to `/tmp/shipwright-<plan-id>/<sha7>/worker-<n>/laneNN-<slug>.png` and return the paths with the report.

## <Task as a verb phrase> (<PR id>)

**Depends on.** <PR id, or None.>

**Files.**

- [ ] Edit `<path>`.
- [ ] Create `<path>`.
- [ ] Delete `<path>`.

**Build.**

- [ ] <One change. Name the symbol and the file.>

**You see.**

- [ ] <One observable result, with the exact log line or screen state.>

**Verify, unit.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.

- [ ] <Test file and the case it gains.> Run `<command>`.

**Verify, live.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked. Ten lanes on `<model>` at the PR head, per the boot recipe.

- [ ] Lane 1. Regression lane against trunk. Run <the same load-bearing scenario> at trunk and head. If trunk lacks the feature, record that and gate <the behavior the diff adds plus the end state the user waits for>. Save `lane01-<slug>.png`. Pass when <predicate>.
- [ ] Lane 2. <Scenario.> Save `lane02-<slug>.png`. Pass when <predicate>.
- [ ] Lane 3. <Scenario.> Save `lane03-<slug>.png`. Pass when <predicate>.
- [ ] Lane 4. <Scenario.> Save `lane04-<slug>.png`. Pass when <predicate>.
- [ ] Lane 5. <Scenario.> Save `lane05-<slug>.png`. Pass when <predicate>.
- [ ] Lane 6. <Scenario.> Save `lane06-<slug>.png`. Pass when <predicate>.
- [ ] Lane 7. <Scenario.> Save `lane07-<slug>.png`. Pass when <predicate>.
- [ ] Lane 8. <Scenario.> Save `lane08-<slug>.png`. Pass when <predicate>.
- [ ] Lane 9. <Scenario.> Save `lane09-<slug>.png`. Pass when <predicate>.
- [ ] Lane 10. <Scenario.> Save `lane10-<slug>.png`. Pass when <predicate>.

**Verify, perf.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.

- [ ] Metric. <What is measured at both trunk and head. If trunk lacks the feature, also name the diff-added work and the end-to-end state the user waits for.>
- [ ] Probe. <The command or procedure, run at trunk and at the head, interleaved. Both sides must produce the metric.>
- [ ] Baseline. Record the trunk <value> first.
- [ ] Rule. <Head against trunk, with the number that fails. If the scenarios differ, add absolute budgets for the diff-added work and the user-visible end state instead of an invalid ratio.>

**Review gate.** The operator reviews before merge.

- [ ] Copy lane <n> screenshots into the PR attachments and record the URLs in the plan's evidence appendix.
- [ ] Record a 30 to 60 second video of the change. Upload it as a PR attachment. Save the local file only under `/tmp/shipwright-<plan-id>/<sha7>/review.mp4`.
- [ ] Post the screenshots and the video for shipwright-signoff. Stop at merge-ready. Wait for the operator.

**Merge.**

- [ ] A clean verdict at the exact head SHA.
- [ ] Review-bot triage done.
- [ ] Rebased onto current trunk after the verdict, patch-id unchanged.
- [ ] The operator lands it bottom-up. This program does not merge.

## Close the program

- [ ] Every box above is checked with its evidence.
- [ ] Reply to the operator with the report the execution reference names.

## Appendix A. Prototype evidence

<Each open question a prototype answered, with the branch, the SHA, and the artifact links. Each question that stays unproven.>

## Appendix B. Alternatives rejected

<Each approach weighed and why it lost.>

## Appendix C. Risks

<Each risk with the PR it lands in and what the owner watches.>

## Appendix D. Links and reading list

<Docs to read before editing. Which PRs use shipwright-how and shipwright-interrogate. The trail is shipwright-trail.>
````

**Reply:** the plan path, the PR ids with their dependencies and the review-gated set, what the prototypes proved and what stays unproven, and the check script's output.
