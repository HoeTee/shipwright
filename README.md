<h1 align="center">Shipwright</h1>

<p align="center">
  <em>Shipwright takes one coding task from the first look to a human merge decision.</em>
</p>

<p align="center">
  <a href="https://github.com/HoeTee/shipwright/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/HoeTee/shipwright/ci.yml?style=flat-square&label=CI" alt="CI"></a>
  <a href="https://github.com/HoeTee/shipwright/releases/tag/v1.0.0"><img src="https://img.shields.io/badge/release-v1.0.0-111111?style=flat-square" alt="Release v1.0.0"></a>
  <a href="references/platforms.md"><img src="https://img.shields.io/badge/works%20with-Codex%20%C2%B7%20Claude%20Code%20%C2%B7%20OpenCode-111111?style=flat-square" alt="Works with Codex, Claude Code, and OpenCode"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-111111?style=flat-square" alt="MIT license"></a>
</p>

<p align="center">
  <sub><a href="docs/README.zh-CN.md">Chinese</a> &middot; <a href="docs/README.ja.md">Japanese</a> &middot; <a href="docs/README.ko.md">Korean</a></sub>
</p>

<p align="center">
  <img src="docs/media/shipwright-hero.png" width="880" alt="-43% Python lines changed. Same pass rate: 30/32 vs 30/32.">
</p>

<p align="center">
  <sub>16 real Click bug fixes. The same agent ran with skills and with no skills. 2 runs per arm. <a href="#numbers">Numbers</a>.</sub>
</p>

<p align="center">
  <img src="docs/media/shipwright-workflow.png" alt="Task, Plan, Build, Review and Fix, Ship, then a human merge.">
</p>

| What you're doing | Skill | Key principle |
| --- | --- | --- |
| Start a task | [shipwright-flow](skills/shipwright-flow/SKILL.md) | Record the stage and what you allow. |
| Write the plan | [shipwright-plan](skills/shipwright-plan/SKILL.md) | Write a plan a new agent can run. |
| Make the change | [shipwright-build](skills/shipwright-build/SKILL.md) | Bring back proof from the real product. |
| Check the change | [shipwright-review](skills/shipwright-review/SKILL.md) | Report findings. Do not edit. |
| Fix a blocker | [shipwright-fix](skills/shipwright-fix/SKILL.md) | Own the AI review limit. |
| Open the pull request | [shipwright-ship](skills/shipwright-ship/SKILL.md) | Follow CI. Do not merge. |
| Prepare the packet | [shipwright-signoff](skills/shipwright-signoff/SKILL.md) | A person reads this packet. |
| Merge | [shipwright-land](skills/shipwright-land/SKILL.md) | Merge after a non-author checks it and you allow it. |

The [full skill list](docs/skills.md) names all 48 skills.

## Quick start

The fastest install is one command.
It needs Claude Code 2.1.292 or newer.

```bash
claude plugin install shipwright --marketplace HoeTee/shipwright
```

HTML reports need Node.js 20 or newer.
Evaluation scripts need Python 3.

<details>
<summary>Claude Code</summary>

Start a new session after you install.
Then run `/shipwright:shipwright-flow`.

</details>

<details>
<summary>Codex</summary>

```bash
codex plugin marketplace add HoeTee/shipwright
codex plugin add shipwright@shipwright
```

Start a new thread.
Then call `$shipwright:shipwright-flow`.

</details>

<details>
<summary>OpenCode</summary>

Put this entry in `opencode.json`.
Keep the final slash.

```json
{
  "skills": ["https://raw.githubusercontent.com/HoeTee/shipwright/main/skills/"]
}
```

Then ask for `@shipwright-flow`.

</details>

Send this prompt.

```text
Use shipwright-flow.
The order list groups dates by UTC. Use the store time zone.
You may edit local files and run tests.
Do not push. Do not open a pull request. Do not merge.
```

## Numbers

<p align="center">
  <img src="eval/results/2026-11-round2/chart.png" width="880" alt="Click round 2. Plain is 100. Skills is 56.6. Hidden tests passed 30 of 32 runs on each arm.">
</p>

Skills changed 43% fewer Python lines than the same agent with no skills.
Hidden tests passed 30 of 32 runs on each arm. The pass rate is the same.
The 95% interval is 27% to 57% fewer lines. The [report](eval/results/2026-11-round2/report.md) has the method and the limits.

## FAQ

<details>
<summary>Does install start the work?</summary>

Install only adds the skills.
A new session starts the task.

</details>

<details>
<summary>Will the agent merge?</summary>

[shipwright-ship](skills/shipwright-ship/SKILL.md) stops when the pull request can merge.
[shipwright-land](skills/shipwright-land/SKILL.md) merges only after you allow it.

</details>

<details>
<summary>Where is the review limit?</summary>

The default limit is 3.
Only [shipwright-fix](skills/shipwright-fix/SKILL.md) defines it.
The count starts when the pull request opens.
Work before that pull request does not count.
Silence is not approval.

</details>

<details>
<summary>Where does proof go?</summary>

Proof goes under `/tmp/shipwright-<plan-id>/<short-sha>/`.
A cached screenshot is not proof.

</details>

## Philosophy

Keep each change small and complete, and add no unrequested work.

A plan in `plans/` records the notes, the commands, the run, and the proof.

Prove the change on the real product, not from a cached screenshot.

AI review has a limit of 3, and a person decides the merge.

Swarm, arena, autopilot, and multi-PR plans stay off until you ask.

## Credits and comparison

Shipwright keeps four ideas.

| Source | What Shipwright keeps |
| --- | --- |
| [Ponytail](https://github.com/DietrichGebert/ponytail) | [shipwright-lean](skills/shipwright-lean/SKILL.md) and the shortcut ledger in [shipwright-debt](skills/shipwright-debt/SKILL.md) |
| [pstack](https://github.com/cursor/plugins/tree/main/pstack) | The shared verify pair and the shared prove pair |
| [improve](https://github.com/shadcn/improve) | [shipwright-audit](skills/shipwright-audit/SKILL.md) and the plan template |
| [code-review-lifecycle](https://github.com/HoeTee/code-review-lifecycle-skill) | The review limit in [shipwright-fix](skills/shipwright-fix/SKILL.md) and the human packet in [shipwright-signoff](skills/shipwright-signoff/SKILL.md) |

Ponytail publishes its own measurements.
Those numbers are not Shipwright results.

## Feedback and contributions

Report a problem in [Issues](https://github.com/HoeTee/shipwright/issues).
Send a change in [pull requests](https://github.com/HoeTee/shipwright/pulls).
Read [CONTRIBUTING-skills.md](CONTRIBUTING-skills.md) before you edit a skill.

## License

MIT © HoeTee/shipwright
