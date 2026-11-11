---
name: shipwright-setup
description: "本机配置：每个角色用什么模型，Git 平台怎么接。用于：首次安装或换模型。不要用于：项目规则文件找 rules。"
---

# shipwright-setup

## When to use

何时用：第一次安装，或要换某个角色的模型，或要核对本机 Git 平台能不能用。

何时不用：仓库的 `AGENTS.md`、`CLAUDE.md`、`REVIEW.md` 交给 shipwright-rules。AI 审查上限不在这里，数字只写在 shipwright-fix。

## Models

按 [Model settings](../../references/setup/models.md) 做完这些步，不要跳过检测。

1. 列出本会话能交给独立 worker 的模型 slug。检测不到就请用户贴一份。没确认过的 slug 不写入。`inherit-parent` 和 `auto` 始终合法，表示沿用当前对话的模型。
2. 读已有设置。没有就用参考里的默认表。表外的旧角色行删掉。
3. 用一个选择题问预算，选项原样是 `unlimited — max reasoning`、`large — xhigh reasoning`、`medium — high reasoning`、`small — medium reasoning`。没有旧文件时说明 `large` 就是默认。
4. 按预算改每个真实 slug 的力度档。结果不在已检测列表里时，用同一家族里不超过目标力度的最高可用 slug，否则标成待选。别名不动。
5. 展示每个角色。面板角色是列表，列表长度就是 worker 数。`arena cross-judge pool` 只从与父模型不同的家族里按顺序挑一个评委，别名永不做评委。
6. 用户确认后整文件覆盖写入。Claude Code 写 `~/.claude/rules/shipwright-models.md`。Codex 和 OpenCode 写 `~/.agents/shipwright-models.md`。不要写只对某一家生效的 frontmatter。
7. 告诉用户写了哪个文件。Claude Code 从新会话起加载。Codex 和 OpenCode 要在选模型时自己读那份文件。

## Git host

接着按 [Platforms](../../references/platforms.md) 核对接入。平台从 remote、项目资料或用户说明里认，认不出再问。只读对应的 GitHub 或 Gitee 一节。工具、登录、仓库、PR、CI 分开验证。推送成功不能代替其余四项。凭据只记引用，不记值。已有连接就复用，缺了才安装。

## Optional offers

项目还不能像用户一样操作真实界面时，可以问一次要不要 shipwright-verify-create。还没有形式化验证时，可以问一次要不要 shipwright-prove-create。用户拒绝就停下，不要再推。
