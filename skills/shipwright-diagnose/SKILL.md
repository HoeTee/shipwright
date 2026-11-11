---
name: shipwright-diagnose
description: "在真实界面复现问题、定位根因，只读不修。用于：有 bug 或异常现象。不要用于：根因已知要修找 build。"
---

# shipwright-diagnose

何时用：有 bug 或异常现象，要在真实界面复现并找到根因。
何时不用：根因已经知道、要修，用 shipwright-build。只想弄清一块代码怎么运作用 [shipwright-how](../shipwright-how/SKILL.md)。只读调查、还没有故障现象时，走 how 的 [investigation.md](../shipwright-how/references/investigation.md)。

本 skill 只读。不写修复，不提交，不开 PR。

## Steps

1. 在用户真正碰到的界面上自己复现。页面、桌面应用或命令行，哪一个是故障界面就用哪一个。对方叫你「你来复现」也不能改成只让对方操作。只有把这个界面驱到走不下去、并写明具体原因时，才请对方补一步。复现不出来就收紧条件或加观测，直到它出现。步骤和证据文件名在 [reproduce.md](references/reproduce.md)。
2. 对原因做二分。先用 shipwright-how 看受影响的子系统，用 shipwright-why 看回归历史，列出候选，再用运行证据逐个排除。每轮切掉剩余空间最大的那一块。程序状态看不清时加观测，读运行中的记录。不猜。活进程走 [runtime-forensics.md](references/runtime-forensics.md)。已经有 trace、profile 或堆快照时走 [trace-forensics.md](references/trace-forensics.md)，不重跑那份固定产物。大文件先用 [trace_to_sqlite.py](scripts/trace_to_sqlite.py) 装进 sqlite，再查询。
3. 用运行证据确认活下来的那一个机制，精确到 `file:line`。确认之前不交给别人去设计修复。

派工见 [hosts.md](../shipwright-how/references/hosts.md)。大产物的解析留在执行者那边，主线只留缩小后的发现。原则名是 `guard-the-context-window`。

## Evidence

可见界面把复现存到 `/tmp/shipwright-<plan-id>/<sha7>/before-<slug>.png`，能取 ARIA 快照时加同名 `.aria.txt`。命令行或接口存 `.txt` 或 `.json`。密钥先遮挡。无法判断，或拍的不是这个界面，不算通过，要明说。单元测试不能代替这次复现。什么才算数写在共享的 `references/evidence.md`（另写）。

吞吐检查点一行：`throughput checkpoint: n/a, read-only diagnosis`。取证时把 diagnosis 换成 `read-only forensics`。

## Stop

回复写清：坏在哪、活下来的机制、运行证据、源码位置、产物路径。把修复交给 shipwright-build。修复前后要在同一界面、同一步骤再验，那是 build 的事。跨函数边界的设计也在离开本 skill 之后才走 shipwright-architect。结果页交给 shipwright-recap。
