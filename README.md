<div align="center">

**English** · [简体中文](docs/README.zh-CN.md) · [日本語](docs/README.ja.md) · [한국어](docs/README.ko.md)

# Shipwright

Full-lifecycle coding skills for Codex, Claude Code, and OpenCode.

[HoeTee/shipwright](https://github.com/HoeTee/shipwright)

</div>

## Philosophy

Shipwright is the coding lifecycle in one plugin. Every task sits on a stage and in one or more domains.

A stage skill carries process only: when to start, what to hand on, and where to stop. A domain skill carries knowledge only: what to check during that stage. The stage skill reads the domain section for the current stage, so each rule lives in one place.

Five rules hold that lifecycle together.

**The smallest complete change.** Finish the task that was asked for, including the callers and checks it touches, and leave out anything nobody asked for. From [Ponytail](https://github.com/DietrichGebert/ponytail).

**Plans are self-contained records.** A plan is written for an agent that did not see the conversation. It contains the real code excerpts, the commands, a run record, and an evidence appendix. Finished plans stay in `plans/`. From [improve](https://github.com/shadcn/improve).

**Prove it on the real artifact.** A report is an HTML page. The product's behavior is shown with evidence from the version under test. A cached screenshot is not evidence. From [pstack](https://github.com/cursor/plugins/tree/main/pstack).

**AI review is bounded, and a person decides.** After a pull request is open, each AI review counts. The default cap is three, and it is defined in `shipwright-fix`. A person makes the final call for that commit. Silence is not approval, and the agent does not merge on its own. From [code-review-lifecycle](https://github.com/HoeTee/code-review-lifecycle-skill).

**Heavy orchestration is opt-in.** Swarm, arena, autopilot, and multi-PR plans stay off until someone asks for them. The ordinary path is one stage at a time.

## The core flow

## Why a plugin of focused skills

## Comparison

## Install

## Quick start

## FAQ

## Repository guide

## License
