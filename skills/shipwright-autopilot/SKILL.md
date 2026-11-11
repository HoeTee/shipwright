---
name: shipwright-autopilot
description: "长时间无人值守：定判定条件、循环推进、干净暂停；多 PR 编排放 references 默认不启用。用于：我去睡了，做完它。不要用于：一次性小任务用 build；永远不自己合并。"
---

# shipwright-autopilot

何时用：任务要跨过一段时间无人值守，而且完成标准可以写成一条能判定真假的条件。
何时不用：一次就能做完的改动用 shipwright-build。本 skill 永远不合并。

## Procedure

1. 先写下退出条件，再动手。例子：测试全绿、原复现已消失、图像差异为零。条件在中途不能放宽。见 [autonomous-run.md](references/autonomous-run.md)。
2. 每一轮只做证据所要求的最小改动，对着退出条件验证，有推进就提交，没有推进就撤回。原则 sequence-verifiable-units、outcome-oriented-execution、never-block-on-the-human、build-the-lever 见 [principles](../../references/principles/README.md)，不要另抄。
3. 没有现成剧本时，按 [hypothesis.md](references/hypothesis.md) 把每个单元当成一次实验：写出假设，改一小步，在真实产物上测量，不成立就回退。框定判定条件和设计阶段属于 shipwright-plan 和 shipwright-architect。决策日志交给 shipwright-trail。
4. 可逆的事先做再报。只把不可逆动作、没有实验能解决的产品取舍、或真正的死胡同交给用户。
5. 有事件就等事件。没有事件订阅时用粗间隔复查，不要空转轮询。
6. 用户明确要求暂停时，按 [pause.md](references/pause.md) 停在安全边界：收尾或回退当前一步，不新开 PR，不新推送，把未提交改动做成一条 `wip:` 提交，并在 `/tmp/<slug>-resume.md` 写下续做所需的意图、进度、已验证项和下一步。用户说继续做时不要暂停。

## Platforms

Codex、Claude Code 和 OpenCode 用同一过程。能派子代理就派独立工作者；不能派就自己做并写明。模型用 shipwright-setup 记下的角色模型。

## Disabled

下面三份默认不读。只有操作者明确启用多 PR 编排时才打开，而且仍然不合并。

- [orchestrate.md](references/orchestrate.md)：一个协调者分派多个 PR，读产物和 diff，不只读摘要。一个结论只管一个 SHA。
- [stack.md](references/stack.md)：堆叠 PR，停在已验证、可交给人的状态。
- [lanes.md](references/lanes.md)：十条实测通道。截图放 `/tmp/shipwright-<plan-id>/<short-sha>/laneNN-<slug>.png`。人审截图和 30–60 秒视频始终归 shipwright-signoff，不依赖本文件。
- [check-plan.mjs](scripts/check-plan.mjs) 是上游格式检查，默认不跑。它要求上游英文骨架里的宿主唤醒命令。[check_lanes.py](scripts/check_lanes.py) 不加 `--enable` 时只报告 disabled。

autopilot-full 不在本插件里。任何允许自己合并的句子都不要执行。

## Stop

退出条件成立，或确认是死胡同。停在可交给 shipwright-signoff 的版本。合并只走 shipwright-land，而且要另有授权。

## Handoff

回复退出条件、跑了几轮、留下什么、丢弃什么、条件现在是否成立。证据目录沿用 shipwright-build 的路径。
