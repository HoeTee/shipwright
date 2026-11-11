---
name: shipwright-build
description: "按计划改代码：派独立执行者，按任务类型走剧本，在对应界面实跑留证，收回报告。用于：有计划，或明确的小改动。不要用于：验收结果找 review 和 fix。"
---

# shipwright-build

何时用：已有 `plans/NNN-*.md`，或改动只有一两处而且做法已经清楚。
何时不用：验收执行结果交给 shipwright-review 和 shipwright-fix。本 skill 不推送、不开 PR、不合并，除非 Run record 里的授权原话写了那一项。

这里只规定怎么把计划做成代码并带回证据。领域检查读计划 Domains 里对应 skill 的执行阶段，不在这里复述。

## Inputs

简报里要有模式、授权、基线、候选、范围、领域标签和计划路径。没有计划、做法又不明显时，退回 shipwright-plan。

## Procedure

1. 核对计划依赖在 `plans/README.md` 里是 DONE。自己跑计划里的 drift check。范围内文件相对 `Planned at` 变了，就停，交给 shipwright-reconcile，不把过期摘录交出去。
2. 按任务类型只读一份剧本：
   - 修缺陷：[bugfix.md](references/bugfix.md)。先在真实界面复现，修完在同一界面、同一步骤复验。单元测试不能代替这次复验。失败用例先于修复进入历史。
   - 新行为：[feature.md](references/feature.md)。四项吞吐检查都要写；不适用的标 `n/a` 和原因。
   - 行为不变的结构调整：[refactor.md](references/refactor.md)。先钉住行为，再改结构。大改要有新旧输出比对或界面冒烟。
   - 慢：[perf.md](references/perf.md)。回复写基线、修后数字、差值和产物路径。
   剧本里的 how、why、architect、interrogate、Opening a PR、tdd 分别是 shipwright-how、shipwright-why、shipwright-architect、shipwright-interrogate、shipwright-ship、shipwright-test。原则名见 [principles](../../references/principles/README.md)，不要另抄。
3. 写代码前用 [code_map.py](scripts/code_map.py) 列出已有函数，能复用就复用。精简读 [shipwright-lean](../shipwright-lean/SKILL.md)，直到用户说 stop lean。迁移时先改调用方再删旧接口，原则是 migrate-callers-then-delete-legacy-api。
4. 领域标签指向哪份就读哪份的执行阶段：[bugs](../shipwright-bugs/SKILL.md)、[security](../shipwright-security/SKILL.md)、[test](../shipwright-test/SKILL.md)、[structure](../shipwright-structure/SKILL.md)、[perf](../shipwright-perf/SKILL.md)。
5. 派一名独立执行者。简报、前言和报告格式见 [dispatch.md](references/dispatch.md)。计划全文内联进简报。没有子代理时按同一前言自己做，并写明不是独立执行者。Codex 用 subagent 或云端代理，Claude Code 用 Agent 工具，OpenCode 用 task，子代理类型 general。模型用 shipwright-setup 记下的角色模型，没有就用当前会话的默认模型。
6. 在产品的真实界面留证。路径和命名用 [save_evidence.py](scripts/save_evidence.py)：`/tmp/shipwright-<计划编号>/<commit 前 7 位>/<种类>-<场景>`。种类是 before、after、variant-a、baseline、diff、lane01–lane10、review。没有界面时存命令输出、响应体或数据库状态。共享证据规则在 `references/evidence.md`，由 shipwright-test 维护；本 skill 只按那个路径存文件。密钥值不进证据。
7. 收回报告后自己重跑 done criteria，读完整 diff，核对范围。四步验收和 APPROVE / REVISE / BLOCK 属于 shipwright-fix。
8. 把实际跑过的命令、结果和时间写入计划 Run record 的 Verification evidence。开 PR 前的执行或修改，由 shipwright-fix 的计数脚本增加 Pre-PR iterations。这一列不是 AI 审查，上限也不在本 skill。

## Stop

计划里的 STOP、范围外文件、或同一步验证失败两次：停，按报告格式交回，不绕过障碍。

## Handoff

范围干净且 done criteria 已由你重跑通过：把候选 SHA、证据目录交给 shipwright-review。用户还没要求审查或开 PR 时，停在报告。
