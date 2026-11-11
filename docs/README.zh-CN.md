<div align="center">

[English](../README.md) · [日本語](README.ja.md) · [한국어](README.ko.md)

# Shipwright

**Shipwright 把一项编码任务从第一次查看带到人工合并决定。**

适用于 Codex、Claude Code 和 OpenCode 的插件

[![CI](https://github.com/HoeTee/shipwright/actions/workflows/ci.yml/badge.svg)](https://github.com/HoeTee/shipwright/actions/workflows/ci.yml)
[![Plugin](https://img.shields.io/badge/plugin-Codex%20%C2%B7%20Claude%20Code%20%C2%B7%20OpenCode-1f6feb)](../references/platforms.md)
[![MIT](https://img.shields.io/badge/license-MIT-lightgrey)](../LICENSE)

[安装](#安装并试用) · [流程](#工作流程) · [Skill](#核心-skill) · [示例](#示例) · [问答](#常见问题) · [指南](#仓库指南)

<code>claude plugin install shipwright --marketplace HoeTee/shipwright</code>

</div>

## 安装并试用

先安装插件。然后新开一个会话。

### Claude Code

下面这条命令需要 Claude Code 2.1.292 或更新版本。

```bash
claude plugin install shipwright --marketplace HoeTee/shipwright
```

也可以先加入 marketplace。然后再安装插件。

```bash
claude plugin marketplace add HoeTee/shipwright
claude plugin install shipwright@shipwright
```

在会话里运行这两条命令。

```text
/plugin marketplace add HoeTee/shipwright
/plugin install shipwright@shipwright
```

### Codex

```bash
codex plugin marketplace add HoeTee/shipwright
codex plugin add shipwright@shipwright
```

### OpenCode

把下面这项写入 `opencode.json`。

```json
{
  "skills": ["https://raw.githubusercontent.com/HoeTee/shipwright/main/skills/"]
}
```

保留末尾的斜杠。

### 要求

需要 Git。
HTML 报告需要 Node.js 20 或更新版本。
评测脚本需要 Python 3。
Skill 文件是 Markdown。

### 发起一项任务

发送这段提示。

```text
Use shipwright-flow.
The order list groups dates by UTC. Use the store time zone.
You may edit local files and run tests.
Do not push. Do not open a pull request. Do not merge.
```

| 代理 | 开始方式 |
| --- | --- |
| Codex | `$shipwright:shipwright-flow` |
| Claude Code | `/shipwright:shipwright-flow` |
| OpenCode | `@shipwright-flow` |

<p align="center">
  <img src="media/shipwright-hero.png" alt="任务，然后选择阶段、构建、审查，最后由人决定。" width="860">
</p>

<p align="center"><em>任务、阶段、构建、审查，然后由人决定。</em></p>

Shipwright 是一组 skill，用来完成一项编码任务。
每个 skill 只做一件事。
[shipwright-flow](../skills/shipwright-flow/SKILL.md) 记录目标、阶段、范围，以及你允许的操作。

你得到一份计划、一处代码改动，以及真实产品上的证据。
合并由人决定。
只有你允许 [shipwright-land](../skills/shipwright-land/SKILL.md) 时，代理才会合并。

## 工作流程

<p align="center">
  <img src="media/shipwright-workflow.png" alt="从任务经过审查，到 shipwright-land 的路径。">
</p>

<p align="center"><em>主路径。<a href="media/shipwright-workflow.svg">完整尺寸图</a> · <a href="showcase/shipwright-workflow.html">HTML 指南</a></em></p>

1. **选择阶段。** 运行 [shipwright-flow](../skills/shipwright-flow/SKILL.md)。它记录目标和你允许的操作。
2. **做这一阶段。** 读代码、找问题、写计划，或改代码。
3. **打开 pull request。** [shipwright-ship](../skills/shipwright-ship/SKILL.md) 跟进 CI。它不合并。
4. **审查有上限。** pull request 打开之后，[shipwright-fix](../skills/shipwright-fix/SKILL.md) 为每次 AI 审查计数。默认上限是 3。打开 pull request 之前的工作不计数。计数不清零。
5. **请人决定。** [shipwright-signoff](../skills/shipwright-signoff/SKILL.md) 准备人工包。[shipwright-land](../skills/shipwright-land/SKILL.md) 只在你允许之后合并。

小而清楚的改动可以从 [shipwright-build](../skills/shipwright-build/SKILL.md) 开始。
审计保持为审计，直到你要求写计划。

## 核心 skill

这八个 skill 是主路径。
[完整 skill 列表](skills.zh-CN.md) 列出全部 48 个 skill。

- **[shipwright-flow](../skills/shipwright-flow/SKILL.md)** 选择阶段、范围，以及你允许的操作。
- **[shipwright-plan](../skills/shipwright-plan/SKILL.md)** 写一份新代理可以执行的计划。
- **[shipwright-build](../skills/shipwright-build/SKILL.md)** 完成改动，并带回证据。
- **[shipwright-review](../skills/shipwright-review/SKILL.md)** 报告已核实的发现。它不改代码。
- **[shipwright-fix](../skills/shipwright-fix/SKILL.md)** 修复阻断项。它持有 AI 审查上限。
- **[shipwright-ship](../skills/shipwright-ship/SKILL.md)** 打开 pull request 并跟进 CI。它不合并。
- **[shipwright-signoff](../skills/shipwright-signoff/SKILL.md)** 为一个人准备审查包。
- **[shipwright-land](../skills/shipwright-land/SKILL.md)** 在非作者验证并且你允许之后，合并那个版本。

## 示例

订单列表按 UTC 给日期分组。
店铺使用自己的时区。
你允许本地编辑和测试。
你不允许推送、打开 pull request 或合并。

1. [shipwright-flow](../skills/shipwright-flow/SKILL.md) 记录这个范围。
2. [shipwright-diagnose](../skills/shipwright-diagnose/SKILL.md) 复现这个 bug。它不改代码。
3. [shipwright-build](../skills/shipwright-build/SKILL.md) 先加一个失败的测试，再修正分组。
4. [shipwright-review](../skills/shipwright-review/SKILL.md) 检查该 commit，并报告发现。

阻断项交给 [shipwright-fix](../skills/shipwright-fix/SKILL.md)。
[shipwright-diagnose](../skills/shipwright-diagnose/SKILL.md) 在[完整列表](skills.zh-CN.md)里。

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

<details>
<summary>Skill 用什么语言？</summary>

Skill 说明是中文。
路径、文件名和模板标题是英文。

</details>

## 仓库指南

| 路径 | 内容 |
| --- | --- |
| [skills/](../skills/) | 每个 skill 一个目录。每个 skill 有 `SKILL.md`。 |
| [skills.zh-CN.md](skills.zh-CN.md) | 全部 48 个 skill 的列表。 |
| [references/](../references/) | 范围、发现、证据和平台的共用规则。 |
| [references/principles/](../references/principles/) | 共用的设计原则。 |
| [showcase/shipwright-workflow.html](showcase/shipwright-workflow.html) | 工作流程的 HTML 指南。 |
| [scripts/render_html.mjs](../scripts/render_html.mjs) | 渲染 HTML 报告。需要 Node.js 20 或更新版本。 |
| [.claude-plugin/](../.claude-plugin/) | Claude Code 的 marketplace 和插件清单。 |
| [.codex-plugin/](../.codex-plugin/) | Codex 的插件清单。 |
| [CONTRIBUTING-skills.md](../CONTRIBUTING-skills.md) | 修改 skill 的规则。 |

## 理念

改动要小，也要完整。
做被要求的工作，包括调用方和检查。
不要加上没有人要求的工作。
这条规则来自 [Ponytail](https://github.com/DietrichGebert/ponytail)。

计划是 `plans/` 里的一份记录。
它包含笔记、命令、运行记录和证据。
这条规则来自 [improve](https://github.com/shadcn/improve)。

在真实产品上证明改动。
缓存的截图不是证据。
这条规则来自 [pstack](https://github.com/cursor/plugins/tree/main/pstack)。

AI 审查有上限。合并由人决定。
默认上限是 3，只有 [shipwright-fix](../skills/shipwright-fix/SKILL.md) 定义它。
计数从 pull request 打开时开始。
这条规则来自 [code-review-lifecycle](https://github.com/HoeTee/code-review-lifecycle-skill)。

重型工具在你要求之前保持关闭。
这些工具是 swarm、arena、autopilot，以及多 PR 计划。

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

[MIT](../LICENSE)。
改编过的文件保留它们自己的声明。
