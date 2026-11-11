<div align="center">

[English](../README.md) · **简体中文** · [日本語](README.ja.md) · [한국어](README.ko.md)

# Shipwright

面向 Codex、Claude Code 和 OpenCode 的全生命周期编码技能。

[HoeTee/shipwright](https://github.com/HoeTee/shipwright)

</div>

## 理念

Shipwright 把编码的整个生命周期放进一个插件。每项工作都落在某个阶段，并带一个或多个领域标签。

阶段 skill 只放过程：何时开始、交出什么、在哪里停下。领域 skill 只放知识：这个阶段要查什么。阶段 skill 去读领域 skill 里对应阶段的那一节，同一条规则只写一处。

五条规则把这条生命周期收在一起。

**最小的完整改动。** 把要求的事做完，包括它碰到的调用方和检查，不加没人要求的东西。来自 [Ponytail](https://github.com/DietrichGebert/ponytail)。

**计划是可以独立执行的记录。** 计划写给没看过那次对话的执行者。里面有真实代码摘录、命令、执行记录和证据附录。做完的计划留在 `plans/`。来自 [improve](https://github.com/shadcn/improve)。

**用真实产物证明。** 报告是 HTML 页面。产品行为用来自受验版本的证据展示。缓存的截图不算证据。来自 [pstack](https://github.com/cursor/plugins/tree/main/pstack)。

**AI 审查有上限，决定由人来做。** 开 PR 之后，每一次 AI 审查都计数。默认上限是 3，只定义在 `shipwright-fix`。人对这个 commit 做最后决定。沉默不算同意，agent 也不自己合并。来自 [code-review-lifecycle](https://github.com/HoeTee/code-review-lifecycle-skill)。

**重型编排默认关闭。** swarm、arena、autopilot 和多 PR 计划，等人明确要求才启用。平常的路径是一次走一个阶段。

## 主流程

## 为什么是一组聚焦的 skill

## 对比

## 安装

## 快速开始

## 常见问题

## 仓库指南

## 许可证
