---
name: shipwright-readme
description: "按仓库里的真实文件和实测写项目 README。用于：新写或改写项目 README 及其译文。不要用于：PR 描述和 commit 信息找 write。不要去别的仓库找参考。"
---

# shipwright-readme

## When to use

何时用：新写或改写项目 README，包括同一结构的译文。shipwright-flow 把这类任务交到这里。shipwright-write 发现整页是项目 README 时也交到这里。

何时不用：PR 描述、commit 信息、代码注释。那些用 shipwright-write 或 shipwright-comments。本 skill 不合并。

规则在这一页里，是完整的。不要打开别的仓库去抄 README。开 PR 前的核对清单在 [checklist](references/checklist.md)。清单和本页冲突时，以本页为准。

## Procedure

### Truth

1. 每条说法对得上一个仓库文件，或你这次测到的结果。对不上就删。
2. README 写了支持某个平台，安装就必须真能用。环境允许就跑一遍。跑不通就改到能用，或删掉这句支持。
3. 仓库缺这个平台要的文件时，补上那个文件，或删掉这句话。不要编造 manifest。
4. 不写 pending。不留占位。

### Layout

自上而下，只按这个顺序。

1. Header。居中。方图 logo 放在大标题旁边。一句短口号。徽章用 flat-square。
2. Hero。宽而矮。关键数字写在图上，字号大。图上的字垂直居中。少留空。手机上能读。
3. Workflow。横向卡片。一行挤不下就折成两行，不要挤在一行。每个阶段只出现一次。回路画成 `Review ⇄ Fix`。可以加一条短的循环 GIF，并放一张静态 PNG。GIF 不播时，图仍然能读。
4. 核心表。三列：你在做什么、哪条命令或哪个 skill、核心原则。表题用这篇 README 的语言，例如 `Core skills`。不要写成 `main path`。
5. Anatomy。放进一个代码块。先画一个方框，表示一份单元：frontmatter、各节、`references/`、`scripts/`。再画这个仓库的真实树，带数量。每一行都对得上一个真实文件。每行保持窄，手机上能读完。
6. Quick start。最先写一条最快的安装命令。然后每个其他平台单独一节，步骤写全。全文不要 `<details>`。
7. 证据节。英文标题用 `Evidence`。不要用 `Numbers`。译文用该语言里表示证据的词。
8. FAQ。用 Markdown 列表。每条是 `- **Question?** answer`。问题和回答用 README 的语言，写在同一条上。不要给每个问题单独标题。不要折叠。
9. Philosophy。最多 3 到 5 个主题。主题名用粗体。下面几句短的口语，带态度。译文也用口语。只写原则。不写出处，不点名谁说过。
10. 对照。用表代替空泛的 `Credits`。每一行写那个项目做什么、本项目多做什么。本项目放在最后一行。没法公平对照时，标题改成 `Built on`，一行一个项目。
11. 许可证一行。仓库是 MIT 时写成 `MIT © owner/repo`。`owner/repo` 换成这个仓库的所有者和仓库名。许可证文件不是 MIT 时，用文件里的名字，仍然一行。
12. 不要 `Repository guide`。不要 mermaid。

### Evidence

1. 只用这个仓库的真实数据。README 里放少数几个关键数字，和一两张主图。方法和每个任务的细节放进链接的报告。
2. 图上有一个大数字，再加一行，说明测的是什么。
3. 主图之外，可以再放一张交付了测试的运行占比图，以及一个真实的改前和改后。后者标明这是一个例子。没有这份数据就不放。
4. 样本量撑不住的统计删掉。一句实话能说清，就不要留一个难懂的原始分数。不要用别的项目的数字。

### Images

1. 图先写成 HTML，再用无头 Chromium 渲染成 PNG。本机已经装了 garden-skills 的 web-design-engineer 时，可以用它做设计。没装就自己写 HTML。不要把那个 skill 当成前提。
2. GIF 用 ffmpeg。所有图用同一套配色。
3. 字要大，空要少。alt 写上图里的数字。HTML 源文件留在图片旁边。

### Writing

1. 句子短，按字面写。写法按 ASD-STE100。Philosophy 除外，那一节用口语。
2. 每种译文用那种语言重写，结构和图与原文相同。路径、命令、文件名保持英文。
3. 删掉宣传和填充句。

### Deliver

1. 每一轮反馈一个 PR。CI 变绿之后由仓库所有者合并。
2. PR 描述列出改了什么、用了哪些数字、每个数字来自哪个文件。图片当产物附上。
3. 合并之后检查图片和链接在页面上能渲染。打不开就另开一轮修复，仍然一个 PR。

## Handoff

README 正文在这里写完。PR 描述和 commit 信息交给 shipwright-write。开 PR 交给 shipwright-ship。合并交给 shipwright-land，而且要有单独的合并授权。合并之后回到本 skill 做渲染检查。

## Stop

不打开别的仓库找 README 参考。不编造平台、manifest 或数字。不写 pending。不合并。
