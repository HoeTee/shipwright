# Contributing skills

This repository is the shipwright skeleton. Forty-nine skills are laid out under `skills/shipwright-*/`. `shipwright-flow` is written. The other skill bodies are one-line stubs.

Parallel agents each take one group below. Stay inside that group's skill directories. Do not edit another group's `SKILL.md`.

Link only to files that exist in your change. Shared references that are not created yet should be named in prose, not linked, until Group D adds them. CI checks that every markdown link in a skill resolves.

Directory names, file names, paths, path placeholders, and headings that become a file or section in a user project are English. Skill prose stays Chinese.

## Shared files

Nobody edits these while filling a group. They are the skeleton contract.

- `README.md`
- `docs/README.zh-CN.md`
- `docs/README.ja.md`
- `docs/README.ko.md`
- `CONTRIBUTING-skills.md`
- `.github/workflows/ci.yml`
- `tests/test_skill_layout.py`
- `.claude-plugin/`
- `.codex-plugin/`
- `skills/plugin.json`
- `agents/openai.yaml`
- `skills/shipwright-plan/references/template.md`
- `skills/shipwright-plan/references/index.md`
- `references/principles/README.md`
- `scripts/build_opencode_index.py`

`skills/index.json` is the OpenCode HTTP catalog. It is generated. When a file inside a skill directory changes, run `python scripts/build_opencode_index.py` and commit the result. Do not hand-edit it. The version is a hash of the file bytes.

Leave the legacy skill and the renderer where they are. CI still runs the renderer tests from `scripts/`.

- root `SKILL.md`
- existing files in `references/` other than `references/principles/`
- `scripts/` other than `scripts/build_opencode_index.py`
- `assets/`

`shipwright-flow` is already the router. Group A owns that directory, and the body is in place. Change it only to fix a routing error.

Group A owns `skills/shipwright-plan/SKILL.md` and may add other files under that skill. The two template files listed above stay as they are.

## Group A — stage and process skills

Process only: when to start, what to hand on, and where to stop. Domain checklists belong to Group B and Group C.

| Skill | Duty |
| --- | --- |
| `shipwright-flow` | Route the task. Already written. |
| `shipwright-how` | How a piece of code runs: entry, call chain, state. |
| `shipwright-why` | Why it was built that way, with confidence levels. |
| `shipwright-teach` | Plain-language explanation from how and why. |
| `shipwright-recall` | Pick up an earlier session's decisions. |
| `shipwright-audit` | Audit a repo or a scope, then rank findings. |
| `shipwright-roadmap` | Feature direction grounded in the repo. |
| `shipwright-diagnose` | Reproduce and find a cause. Read only. |
| `shipwright-impact` | What else a change can break. |
| `shipwright-plan` | Write `plans/NNN` and the index. |
| `shipwright-architect` | Design across a function boundary. |
| `shipwright-prototype` | A throwaway prototype that answers a fork. |
| `shipwright-build` | Implement a plan and bring back evidence. |
| `shipwright-autopilot` | Unattended run. Never merges. |
| `shipwright-review` | Verified findings on a pinned version. Read only. |
| `shipwright-fix` | Review-fix loop. Owns the AI review cap. |
| `shipwright-interrogate` | Adversaries prove problems by running. |
| `shipwright-comments` | Remove bad comments before review. |
| `shipwright-ship` | Open the PR and follow CI until it is mergeable. |
| `shipwright-signoff` | Human final-review packet. |
| `shipwright-land` | Merge only a version a non-author verified. |
| `shipwright-deploy` | Release and check the target environment. |
| `shipwright-recover` | Triage a failure: roll back or fix. |
| `shipwright-reconcile` | Reconcile `plans/`. |
| `shipwright-debt` | Ledger of `shortcut:` comments. |
| `shipwright-prevent` | Make a repeated mistake structurally impossible. |
| `shipwright-reflect` | Propose a skill change from the session. |

## Group B — domain skills

Knowledge only: what each stage checks. No lifecycle routing.

| Skill | Duty |
| --- | --- |
| `shipwright-bugs` | Correctness and reliability. |
| `shipwright-security` | Boundaries, access, injection, secrets. |
| `shipwright-structure` | Shape, layering, duplication, deletion. |
| `shipwright-perf` | Measure first, then the performance checks. |
| `shipwright-lean` | Smallest complete change. On by default while writing code. |

`shipwright-test` is Group C, not Group B.

## Group C — verify, prove, eval, and test

| Skill | Duty |
| --- | --- |
| `shipwright-test` | Test layers, TDD, behavior tests, and the shared evidence rules. |
| `shipwright-verify-create` | Create a project `verify-<app>` skill and feature map. |
| `shipwright-verify-maintain` | Re-run and correct that feature map. |
| `shipwright-prove-create` | Formal verification for the highest-cost properties. |
| `shipwright-prove-maintain` | Re-align a proof after the code changes. |
| `shipwright-eval` | On-demand with/without or version comparison. Not part of every PR. |

## Group D — principles, references, and the remaining skills

Skills:

| Skill | Duty |
| --- | --- |
| `shipwright-help` | Quick reference and prompts. Does not start the work. |
| `shipwright-setup` | Local model and Git host setup. |
| `shipwright-rules` | Draft `AGENTS.md`, `CLAUDE.md`, and `REVIEW.md`. Write only after confirmation. |
| `shipwright-swarm` | Parallel workers, one report, evidence path and SHA. |
| `shipwright-arena` | Several candidates, then one synthesized result. |
| `shipwright-trail` | Decision log. |
| `shipwright-recap` | HTML result page and the progress page. |
| `shipwright-write` | Docs, PR text, commit messages. |
| `shipwright-readme` | Principles for a project README. shipwright-write hands that page here. |
| `shipwright-skillsmith` | Author or edit a skill. |
| `shipwright-cleanup` | Clean worktrees after the task ends. Do not delete plans or live evidence early. |

Shared references this group adds. Do not edit `references/principles/README.md`; add the files it names.

- [references/recon.md](references/recon.md)
- [references/scope.md](references/scope.md)
- [references/finding.md](references/finding.md)
- [references/evidence.md](references/evidence.md)
- [references/platforms.md](references/platforms.md) for Codex, Claude Code, and OpenCode
- `references/principles/<slug>.md` for each slug in `references/principles/README.md`

## Platforms

- Claude Code: `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`
- Codex: `.codex-plugin/plugin.json` with `skills` pointing at `./skills/`
- OpenCode has no Claude-style plugin manifest for a skill bundle. It loads `SKILL.md` directories and an HTTP catalog. This repo ships that catalog as `skills/index.json`. See [OpenCode skills](https://opencode.ai/docs/skills/).

Install commands and links in this repo use `HoeTee/shipwright`.
