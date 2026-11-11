# Evidence

交给人看的报告和进度页是 HTML，不截图。被改动的产品本身（网页、桌面、命令行输出）必须在真实界面实跑留证。原始证据放临时目录，任务结束后由 shipwright-cleanup 清理。关键截图和视频上传为 PR 附件，链接记进计划的证据附录。证据不进 Git 历史。

这一份是证据规则的正文。共享文件 `references/evidence.md` 由原则组按这一份落盘。其他 skill 引用那一份。落盘前以这一份为准，不要在别的 skill 里再写一份。

看真实产物，不看代理信号。进程是否活着要直接看。读实际的值，不读缓存或派生结果。验证失败时，先怀疑观察方法。能写成可重复脚本的比对就写成脚本，把输出留下来给审查者重跑。缓存截图不算。产物给人看。一般不提交进仓库；大迁移需要事后审计时，由 shipwright-trail 记决定，证据本身仍按本节存放。原则 `prove-it-works` 见 [共享原则目录](../../../references/principles/README.md)。

## Layout

```text
/tmp/shipwright-<plan-id>/                 计划编号；不在仓库里，不提交 Git
└─ <sha7>/                                 受验 commit 前 7 位；新 head 要新证据
   ├─ index.md                             每条：文件、证明什么、命令或操作、时间（UTC+8）
   ├─ before-<slug>.png                    修复前，在真实界面复现
   ├─ after-<slug>.png                     修复后，同一界面同一步骤
   ├─ after-<slug>.aria.txt                同名 ARIA 快照，文字可检索
   ├─ variant-a-<slug>.png                 原型方案 A（方案 B 同理）
   ├─ baseline-<slug>.png                  视觉一致：基线
   ├─ diff-<slug>.png                      视觉一致：图像差异，非零即失败
   ├─ lane03-<slug>.png                    多 PR 实测通道（默认不启用）
   ├─ cli-<slug>.txt                       命令行改动：终端记录
   ├─ api-<slug>.json                      无界面改动：响应体、日志、数据库状态
   ├─ review.mp4                           改了交互：人审前 30–60 秒视频
   └─ worker-<n>/                          子代理各自的子目录，主控核对后挑选使用
```

一个 commit 一个目录，因为结论只对一个版本有效。

| 项 | 规则 |
| --- | --- |
| 文件名 | `<kind>-<slug>.<ext>`。种类：`before`、`after`、`variant-a`、`baseline`、`diff`、`lane01`–`lane10`、`review`。场景用小写英文加连字符 |
| 配套文件 | 同名 `.aria.txt`（ARIA 快照）、`.txt`（终端记录）、`.json`（响应体或数据库状态）。每个目录一个 `index.md` |
| 交付 | 能证明改动的关键截图和视频交给 shipwright-ship，上传到 PR 描述或评论，同时由 shipwright-recap 内嵌进 HTML 结果页 |
| 上传后存在哪 | Git 平台的附件存储（GitHub 为 `github.com/user-attachments/…`）。不在仓库里，不进 git 历史。PR 合并后仍在。私有仓库的附件按仓库权限访问。没有 GitHub 的平台（Gitee、纯 Git）用该平台的附件功能；没有附件功能时走下面的本地目录 |
| 先遮挡 | 附件上传后很难删除。上传前遮挡密钥和个人数据。密钥值不进证据，也不进 PR |
| 证据附录 | 计划文件末尾一节，写分支、SHA，以及每个附件链接。这是计划里的一节，不是文件夹 |
| 没有 PR 时 | 关键截图存 `.shipwright/evidence/<plan-id>/<sha7>/`。这个目录写进 `.gitignore`。附录记本地路径 |
| 子代理 | 写到同一目录下的 `worker-<n>/`。报告里给路径和 SHA。主控打开核对后再挑选使用 |
| 保留期 | 临时目录保留到任务结束：PR 合并，或任务关闭。中途不删，复审和人审都要用 |
| 清理 | shipwright-cleanup 在任务结束后删除整个 `/tmp/shipwright-<plan-id>/`。PR 附件和 `.shipwright/evidence/` 里的关键截图不删。平时的清理只删临时实例和草稿 |
| 云端 | 云端 agent 的 `/tmp` 会随会话消失。关键截图要及时上传为 PR 附件，并内嵌进结果页 |

## When evidence is required

1. 改动影响用户能看到的界面或输出时：修 bug 要修复前后各一张，在同一界面、同一步骤。新功能和重构要有实跑结果。
2. 视觉决策的原型：每个方案一张。
3. 视觉一致迁移：先建基线截图，再用图像差异比对。差异非零即失败。基线保持不动。见 [visual.md](visual.md)。
4. `verify-<app>` 每次证明：拍下操作和结果状态，配 ARIA 快照，画面里能看出是哪个应用。文件、数据行等副作用另存文本证据。
5. 改了交互的 PR，人审前：关键截图加 30–60 秒视频，交给人，停在可合并。shipwright-signoff 收这份材料。
6. PR 描述：截图或视频能证明某个说法时附上。
7. 多 PR 计划的实测通道（默认不启用）：每条通道一张 `laneNN-<slug>.png`。

## When evidence is not a screenshot

- shipwright 自己生成的 HTML 报告、进度页、讲解页：不截图。检查渲染退出码、正文、内嵌证据和版本。
- 没有可见界面的改动（库、后端逻辑）：用命令输出、响应体、日志、退出码、数据库状态作证据，存 `.txt` 或 `.json`，摘要贴进 PR。
- 只改文档或措辞：不需要实跑验证。
- 画面里有密钥或个人数据：先遮挡再拍，或改用文本证据。

## What counts

- 必须是这次 commit 实跑新拍的。缓存的、旧版本的截图不算。新 head 要新证据，除非 patch-id 规则判定补丁相同。
- 无法判断，或拍的不是对应界面，不算通过，要明确标出来。
- 能写脚本比对就用脚本：图像差异、新旧输出 diff。
- 子代理报告缺证据路径或 SHA：重派一次。再缺记为缺口，不算通过。
- 审查者要打开截图和产物本身，不只读执行者的摘要。
- 证据至少含：候选版本及实际运行版本或产物、环境、样本标识、任务编号、实际执行组件、终态，以及业务产物断言。
- 记录 commit、命令、环境、依赖、输入或夹具、结果、产物和限制。失败、超时、未运行和通过分开记录。
- 复用旧证据时，核对该任务曾真实通过、相关运行输入和环境契约相同，并记录等价依据和执行时间。

结果链接由 shipwright-recap 给：云端 agent 只给在线页面链接；连着本地项目的 agent 同时给 HTML 文件路径和在线链接。

## Capture helper

```python
import base64
from pathlib import Path

def save_evidence(page, plan: str, sha: str, kind: str, slug: str) -> Path:
    """kind: before / after / variant-a / baseline / diff / lane03 / review."""
    folder = Path("/tmp") / f"shipwright-{plan}" / sha[:7]
    folder.mkdir(parents=True, exist_ok=True)
    png = folder / f"{kind}-{slug}.png"
    page.screenshot(path=png, full_page=True)
    (folder / f"{kind}-{slug}.aria.txt").write_text(page.locator("body").aria_snapshot())
    return png

def embed_for_report(png: Path) -> str:
    """把截图内嵌进 HTML 结果页。临时目录删掉后报告照样能看。"""
    data = base64.b64encode(png.read_bytes()).decode()
    return f'<img alt="{png.stem}" src="data:image/png;base64,{data}">'
```
