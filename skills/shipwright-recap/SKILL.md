---
name: shipwright-recap
description: "每次结果都出一份 HTML（lifecycle 渲染器，截图内嵌），维护固定进度页；按链接规则给链接。用于：任何要交给你看的结果。不要用于：找回旧会话找 recall。"
---

# shipwright-recap

## When to use

何时用：任何要交给用户看的结果。聊天里给结论，同时给 HTML 页面。

何时不用：找回上一会话的决定。那是 shipwright-recall。普通工具旁白不逐条生成页面。

## Two outputs

聊天先写完结论、依据、限制和待办，让用户不打开页面也能判断。然后再给链接。不要只回「页面已更新」。

页面用仓库根目录的渲染器，需要 Node.js 20 或更新版本。缺运行环境或渲染失败时说明缺什么，聊天结果照常给。

```sh
node scripts/render_html.mjs render draft.md -o answer.html --no-open
node scripts/render_html.mjs patch answer.html --panel A --from panel.md --no-open
```

进度页用同一套排版。状态源是 JSON，脚本只渲染快照，不监听 PR，也不替用户批准：

```sh
python scripts/render_progress.py task.progress.json --output task.html
```

同一任务反复更新同一份 HTML 和同一份状态源。计划的结果页是 `plans/reports/<计划文件名>.html`。新任务才换路径。草稿、组件和署名见 [HTML explainer](../../references/recap/html-explainer.md)。进度、卡点和状态词见 [Progress](../../references/recap/progress-interaction.md)。

默认紧凑浅色图纸（sheet / blueprint / light），保留原版页眉、字号、表格和自动布局，隐藏工具栏。随包渲染器的默认署名保持不变。用户要改整行署名时才传 `--footer`。不要改 `scripts/`。

## Links

连着本地项目的会话：同时给 HTML 文件路径和在线页面链接。

云端会话：只给在线页面链接。本地路径用户打不开。

## Evidence in the page

本插件生成的说明页、进度页和审查报告不截图。检查渲染退出码、正文、内嵌证据和版本。

被改动的产品界面可以截图。把帧内嵌进 HTML，这样 [cleanup](../shipwright-cleanup/SKILL.md) 删掉临时目录后页面仍能看。证据怎么存见 [Evidence](../../references/evidence.md)。

## Catch-up

用户要追赶这次对话、或要一份正在等他决定的清单时，按 [Catch-up](../../references/recap/ketchup.md) 写：先说等他做什么，再给已经拍下的画面，再列他能做的决定和你的建议。这一轮只读，不改代码、不发帖。用白话，不堆哈希和命令，除非他要靠那个采取动作。
