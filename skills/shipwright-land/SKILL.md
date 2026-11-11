---
name: shipwright-land
description: "合并：只合并非作者像用户一样验证过的版本，自下而上，核对 patch-id。用于：人审通过且授权合并。不要用于：没授权就停在可合并。"
---

# shipwright-land

何时用：shipwright-signoff 记下了人的通过结论，而且授权原文允许合并。
何时不用：没有合并授权。停在可合并，不要自作主张。

## Procedure

1. 先确定平台，GitHub 用 `gh`，能用 `origin pr` 且仓库能解析时用它，并在后面的操作里保持这个选择。不要求 Graphite。步骤全文见 [shipping.md](references/shipping.md)。
2. 每个 PR 由没写这份代码的人，像用户一样在真实界面跑一遍，给出 PASS、PASS+NOTES 或 FAIL。结论写在该 PR 上，并绑定补丁。绿色 CI 和机器人批准都不是这个结论。
3. 只合并从最底下开始、连续通过的那一段。上面通过、下面没通过的，要等。不依赖下面代码的 PR 可以改到主干上，但要先有新的结论。
4. 合并前用 [patch_id.py](scripts/patch_id.py) 比较结论里的 SHA 和当前 head。patch-id 相同，结论还在。不同则看是不是只有测试、文档或 lint 配置；代码变了就要新的结论和新的检查。`--allow-noise` 只放行测试、文档和 lint 配置的差异。
5. 自下而上，一次合并一个。合并命令返回后回读 PR 状态。进了队列不等于已经合并。父 PR 合并后，子 PR 改指向主干，用 `--force-with-lease` 推送，再按 patch-id 决定旧结论是否还有效。
6. 落地过程中不要改其他分支或基线。人审之后的版本变化见 [after-review.md](references/after-review.md)。新提交影响了已审核的结论，就要补验证并请人再看受影响的部分。

## Stop

这一段合并完，或碰到第一个没有 PASS / PASS+NOTES 的 PR。不要用管理员权限绕过保护，也不要默认删分支。

## Handoff

回复合并了哪些 PR、每个结论是谁给的、怎么确认已经合并、上面还缺什么。需要发布时交给 shipwright-deploy。合并后的计划状态交给 shipwright-reconcile。
