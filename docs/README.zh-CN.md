<h1 align="center">Shipwright</h1>

<p align="center">
  <em>Shipwright 把一项编码任务从第一次查看到人工合并决定。</em>
</p>

<p align="center">
  <a href="https://github.com/HoeTee/shipwright/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/HoeTee/shipwright/ci.yml?style=flat-square&label=CI" alt="CI"></a>
  <a href="https://github.com/HoeTee/shipwright/releases/tag/v1.0.0"><img src="https://img.shields.io/badge/release-v1.0.0-111111?style=flat-square" alt="发行版 v1.0.0"></a>
  <a href="../references/platforms.md"><img src="https://img.shields.io/badge/works%20with-Codex%20%C2%B7%20Claude%20Code%20%C2%B7%20OpenCode-111111?style=flat-square" alt="适用于 Codex、Claude Code 和 OpenCode"></a>
  <a href="../LICENSE"><img src="https://img.shields.io/badge/license-MIT-111111?style=flat-square" alt="MIT 许可证"></a>
</p>

<p align="center">
  <sub><a href="../README.md">English</a> &middot; <a href="README.ja.md">日本語</a> &middot; <a href="README.ko.md">한국어</a></sub>
</p>

<p align="center">
  <img src="media/shipwright-hero.png" width="880" alt="Python 行数少 43%。通过率相同：30/32 对 30/32。">
</p>

<p align="center">
  <sub>16 个真实的 Click 缺陷修复。同一个代理分别带 skill 和不带 skill 运行。每个臂 2 次。<a href="#数字">数字</a>。</sub>
</p>

<p align="center">
  <img src="media/shipwright-workflow.png" alt="任务、计划、构建、审查与修复、交付，然后人工合并。">
</p>

| 你在做什么 | Skill | 关键原则 |
| --- | --- | --- |
| 开始一项任务 | [shipwright-flow](../skills/shipwright-flow/SKILL.md) | 记录阶段，以及你允许的操作。 |
| 写计划 | [shipwright-plan](../skills/shipwright-plan/SKILL.md) | 写一份新代理可以执行的计划。 |
| 做改动 | [shipwright-build](../skills/shipwright-build/SKILL.md) | 从真实产品带回证据。 |
| 检查改动 | [shipwright-review](../skills/shipwright-review/SKILL.md) | 报告发现。不改代码。 |
| 修复阻断项 | [shipwright-fix](../skills/shipwright-fix/SKILL.md) | 持有 AI 审查上限。 |
| 打开 pull request | [shipwright-ship](../skills/shipwright-ship/SKILL.md) | 跟进 CI。不合并。 |
| 准备审查包 | [shipwright-signoff](../skills/shipwright-signoff/SKILL.md) | 由一个人阅读这份包。 |
| 合并 | [shipwright-land](../skills/shipwright-land/SKILL.md) | 非作者验证并且你允许之后才合并。 |

[完整 skill 列表](skills.zh-CN.md) 列出全部 48 个 skill。

## 快速开始

最快的安装是一条命令。
它需要 Claude Code 2.1.292 或更新版本。

```bash
claude plugin install shipwright --marketplace HoeTee/shipwright
```

HTML 报告需要 Node.js 20 或更新版本。
评测脚本需要 Python 3。

<details>
<summary>Claude Code</summary>

安装之后新开一个会话。
然后运行 `/shipwright:shipwright-flow`。

</details>

<details>
<summary>Codex</summary>

```bash
codex plugin marketplace add HoeTee/shipwright
codex plugin add shipwright@shipwright
```

新开一个线程。
然后调用 `$shipwright:shipwright-flow`。

</details>

<details>
<summary>OpenCode</summary>

把下面这项写入 `opencode.json`。
保留末尾的斜杠。

```json
{
  "skills": ["https://raw.githubusercontent.com/HoeTee/shipwright/main/skills/"]
}
```

然后请求 `@shipwright-flow`。

</details>

发送这段提示。

```text
Use shipwright-flow.
The order list groups dates by UTC. Use the store time zone.
You may edit local files and run tests.
Do not push. Do not open a pull request. Do not merge.
```

## 数字

<p align="center">
  <img src="../eval/results/2026-11-round2/chart.png" width="880" alt="Click 第二轮。无 skill 为 100。有 skill 为 56.6。隐藏测试两边都是 30/32。">
</p>

有 skill 时，Python 行数比同一个无 skill 的代理少 43%。
隐藏测试两边都通过 30/32 次。通过率相同。
95% 区间是少 27% 到 57%。[报告](../eval/results/2026-11-round2/report.md) 写有方法和限制。

## 常见问题

<details>
<summary>安装会开始工作吗？</summary>

安装只加入 skill。
新会话才开始任务。

</details>

<details>
<summary>代理会合并吗？</summary>

[shipwright-ship](../skills/shipwright-ship/SKILL.md) 在 pull request 可以合并时停下。
[shipwright-land](../skills/shipwright-land/SKILL.md) 只在你允许之后合并。

</details>

<details>
<summary>审查上限在哪里？</summary>

默认上限是 3。
只有 [shipwright-fix](../skills/shipwright-fix/SKILL.md) 定义它。
计数从 pull request 打开时开始。
打开之前的工作不计数。
沉默不是批准。

</details>

<details>
<summary>证据放在哪里？</summary>

证据放在 `/tmp/shipwright-<plan-id>/<short-sha>/`。
缓存的截图不是证据。

</details>

## 理念

改动要小而完整，并且不加没有人要求的工作。

`plans/` 里的计划记录笔记、命令、运行记录和证据。

在真实产品上证明改动，缓存截图不是证据。

AI 审查的默认上限是 3，合并由人决定。

swarm、arena、autopilot 和多 PR 计划在你要求之前保持关闭。

## 来源与对比

Shipwright 保留四个想法。

| 来源 | Shipwright 保留的部分 |
| --- | --- |
| [Ponytail](https://github.com/DietrichGebert/ponytail) | [shipwright-lean](../skills/shipwright-lean/SKILL.md)，以及 [shipwright-debt](../skills/shipwright-debt/SKILL.md) 里的 shortcut 账本 |
| [pstack](https://github.com/cursor/plugins/tree/main/pstack) | 共用的 verify 一对和 prove 一对 |
| [improve](https://github.com/shadcn/improve) | [shipwright-audit](../skills/shipwright-audit/SKILL.md) 和计划模板 |
| [code-review-lifecycle](https://github.com/HoeTee/code-review-lifecycle-skill) | [shipwright-fix](../skills/shipwright-fix/SKILL.md) 里的审查上限，以及 [shipwright-signoff](../skills/shipwright-signoff/SKILL.md) 里的人工包 |

Ponytail 公布的是它自己的测量。
那些数字不是 Shipwright 的结果。

## 反馈与贡献

在 [Issues](https://github.com/HoeTee/shipwright/issues) 报告问题。
在 [pull requests](https://github.com/HoeTee/shipwright/pulls) 提交改动。
编辑 skill 之前，先读 [CONTRIBUTING-skills.md](../CONTRIBUTING-skills.md)。

## 许可证

MIT © HoeTee/shipwright
