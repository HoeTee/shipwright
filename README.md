<h1 align="center"><img src="docs/media/shipwright-logo.png" width="64" height="64" alt="Shipwright" valign="middle"> Shipwright</h1>

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
  <img src="docs/media/shipwright-hero.png" width="880" alt="shipwright. From the first look to a human merge. -43% Python lines changed.">
</p>

<p align="center">
  <sub>16 real Click bug fixes. The same agent ran with skills and with no skills. 2 runs per arm. <a href="#evidence">Evidence</a>.</sub>
</p>

<p align="center">
  <img src="docs/media/shipwright-workflow.gif" alt="Task, Plan, Build, then Review and Fix loop until clear, then Ship and a human merge.">
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

The [full skill list](docs/skills.md) names all 49 skills.

## Anatomy

Every skill file has the same two front matter fields.
The headings below are the common ones.
A skill keeps only the headings it needs.

```
┌────────────────────────────────────────────────────────────────────┐
│ skills/shipwright-*/SKILL.md                                       │
│                                                                    │
│ ┌─ frontmatter ──────────────────────────────────────────────────┐ │
│ │ name: shipwright-<skill>                                       │ │
│ │ description: when to use it, and when not                      │ │
│ └────────────────────────────────────────────────────────────────┘ │
│ # title                                                            │
│ When to use       -> first lines. A heading on some skills.        │
│ Steps / Procedure -> the work this skill does                      │
│ Handoff           -> who takes the next stage                      │
│ Stop              -> what this skill will not do                   │
│                                                                    │
│ references/*.md   -> most skills. A step names the file.           │
│ scripts/          -> some skills. Checkers and helpers.            │
└────────────────────────────────────────────────────────────────────┘
```

The plugin files in this repo:

```
shipwright/
  skills/                         49 skills. Each has SKILL.md.
    shipwright-*/references/      notes. 38 skills have this.
    shipwright-*/scripts/         helpers. 18 skills have this.
    plugin.json                   points at this folder
    index.json                    OpenCode HTTP catalog
  .claude-plugin/plugin.json      Claude Code plugin
  .claude-plugin/marketplace.json marketplace name
  .codex-plugin/plugin.json       Codex plugin. skills: ./skills/
  docs/                           READMEs and the skill lists
  eval/results/                   the Click round reports
  references/                     rules the skills share
```

OpenCode has no plugin manifest in this repo.
`skills/index.json` is the HTTP catalog.
Your `opencode.jsonc` lists a folder, or that catalog URL.

## Quick start

The fastest install is one command.
It needs Claude Code 2.1.292 or newer.

```bash
claude plugin install shipwright --marketplace HoeTee/shipwright
```

Start a new session after you install.
Then run `/shipwright:shipwright-flow`.

HTML reports need Node.js 20 or newer.
Evaluation scripts need Python 3.

#### Codex

```bash
codex plugin marketplace add HoeTee/shipwright
codex plugin add shipwright@shipwright
```

Start a new thread.
Then call `$shipwright:shipwright-flow`.

#### OpenCode

OpenCode loads skill folders.
It does not use a plugin manifest.

Clone the repo.
Then add the folder to `~/.config/opencode/opencode.jsonc`.

```bash
git clone https://github.com/HoeTee/shipwright ~/shipwright
```

```jsonc
{
  "skills": ["~/shipwright/skills"]
}
```

Or copy or symlink `skills/` into `~/.config/opencode/skills`.
A project can use `.opencode/skills` the same way.

Or skip the clone.
Point at the HTTP catalog.
Keep the final slash.

```jsonc
{
  "skills": ["https://raw.githubusercontent.com/HoeTee/shipwright/main/skills/"]
}
```

The catalog file is `skills/index.json`.
Then ask for `@shipwright-flow`.

Send this prompt.

```text
Use shipwright-flow.
The order list groups dates by UTC. Use the store time zone.
You may edit local files and run tests.
Do not push. Do not open a pull request. Do not merge.
```

## Evidence

<p align="center">
  <img src="docs/media/shipwright-evidence.png" width="880" alt="Share of the no-skills baseline. Python lines: no skills 100%, skills 56.6%, which is 43.4% fewer. The 95% interval is 27.0% to 57.4% fewer.">
</p>

Skills changed 43.4% fewer Python lines. The 95% interval is 27.0% to 57.4% fewer.

<p align="center">
  <img src="docs/media/shipwright-evidence-count.png" width="880" alt="Fewer Python lines on 14 of 16 questions. Same pass rate.">
</p>

Fewer Python lines on 14 of 16 questions. The pass rate is the same.

<p align="center">
  <img src="docs/media/shipwright-evidence-tests.png" width="880" alt="Runs whose diff changed test lines. No skills 27 of 32, which is 84%. Skills 32 of 32, which is 100%.">
</p>

The diff changed test lines on 32 of 32 skill runs, and on 27 of 32 runs with no skills.

<p align="center">
  <img src="docs/media/shipwright-evidence-q03.png" width="880" alt="One sentinel run. Python lines, tests excluded: no skill 17, shipwright 4. Both edited src/click/_utils.py and the sentinel test. Both passed. Records do not include the diff.">
</p>

One sentinel run: 4 Python lines with skills, 17 without. Both passed. One example.

Method and limits: [report](eval/results/2026-11-round2/report.md).

## FAQ

- **Which agents can run it?** Claude Code, Codex, and OpenCode use the same skills. Only the install command and the call change.
- **How do I install it?** Use the Quick start above, then start a new session. An old session keeps the files from when it started.
- **Do I need all 49 skills?** No. Call shipwright-flow. The eight skills in the table cover the path, and the rest stay quiet until needed.
- **When does the review loop stop?** Review reports findings and does not edit. Fix makes the repairs, the limit is 3 from the open pull request, and silence is not approval.
- **Can the agent merge by itself?** No. Ship opens the pull request and stops. Land merges only after a non-author checks the change and you allow it.
- **What did the eval measure?** The same agent ran with skills and with no skills on 16 real Click bug fixes, two runs each. Skills changed 43.4% fewer Python lines, the pass rate was the same, and a third repeat did not run.
- **How do I update it?** Run the same install commands again, then start a new session.
- **Does it spend extra tokens?** Shipwright does not set a token price, and the eval did not measure a token bill. You pay your host's normal model cost.

## Philosophy

**Plan, then cut**

Write the plan before you touch the code.
The next agent should run it with no extra chat.
Then make the smallest change that does the job.
Smaller diff, fewer bugs. That's it.

**Prove it**

Don't write code you can't prove works.
Run a command on this change, because a saved screenshot is not proof.
Review finds the holes and does not edit.
Fix patches them, and the AI review stops at 3.

**You merge**

The agent can open the pull request.
It does not get to merge it.
Someone who did not write the change has to look.
Then you say yes.

**Show the run**

If we did not measure it, we do not claim it.
The numbers here come from a real run of this project.
Another project's numbers are not ours.
Extra modes stay off until you ask.

## How Shipwright compares

Each row says what you get from that repo, and what you get from Shipwright.

| | What you get from it | What you get from Shipwright |
| --- | --- | --- |
| [Ponytail](https://github.com/DietrichGebert/ponytail) | The agent writes only the code the task needs. A deferred shortcut is collected into a ledger. | You get that small change and that ledger. The task also runs from a plan to a pull request a person merges. |
| [pstack](https://github.com/cursor/plugins/tree/main/pstack) by poteto | A daily mode runs a playbook for the task. It can check the product and prove one hard property. It can also run agents in parallel, or run overnight through a merge. | You can still check the product and prove one hard property. Parallel work and overnight work stay off until you ask. An overnight run does not merge by itself. |
| [improve](https://github.com/shadcn/improve) | You get an audit and a plan. A cheaper agent can implement that plan. This skill does not edit the product code, and you still merge. | The same task continues into the code change, the review, and an open pull request. A person merges. |
| [code-review-lifecycle](https://github.com/HoeTee/code-review-lifecycle-skill) | It reviews a change, fixes confirmed defects, and stops for a person. The AI review stops at 3 rounds. | The AI review still stops at 3, and a person still decides. The task also has a plan and a build before that review. |
| [agent-skills](https://github.com/addyosmani/agent-skills) | Commands take a task from a spec through code, tests, a review, and a production launch check. After one plan approval, it builds, tests, and commits each task, and pauses on a failure or a risky step. | One path takes that task from a plan through the change, a review, and an open pull request. A person decides the merge. |

Ponytail publishes its own measurements. Those numbers are not Shipwright results.
The eval questions are 16 real fixes from [Click](https://github.com/pallets/click). The images use the design method in [garden-skills](https://github.com/ConardLi/garden-skills).

## Feedback and contributions

Report a problem in [Issues](https://github.com/HoeTee/shipwright/issues).
Send a change in [pull requests](https://github.com/HoeTee/shipwright/pulls).
Read [CONTRIBUTING-skills.md](CONTRIBUTING-skills.md) before you edit a skill.

## License

MIT © HoeTee/shipwright
