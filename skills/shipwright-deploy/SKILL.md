---
name: shipwright-deploy
description: "部署画像、发布、目标环境验收。用于：合并后需要发布。不要用于：线上出问题找 recover。"
---

# shipwright-deploy

何时用：PR 已经合并，而且这个变更需要发布到目标环境。
何时不用：线上出了问题用 shipwright-recover。不是每个合并都要发布。关闭未合并的 PR 不进入这里。

## Procedure

1. 记下 PR、合并 commit、对应检查、人工结论和恢复说明。先核对实际合并结果的检查，不要无故把全部测试再跑一遍。
2. 按 [deployment.md](references/deployment.md) 区分管理方式、容器运行时、构建产物和操作客户端。本机有 Docker 不证明目标用 Docker。先查现有手册，再请用户确认目标环境和交付方式。已确认且没变的，直接复用。
3. 发布差异要求改镜像、启动、路径、配置或代码时，先回到开发分支和 PR，走完 CI、审查和人工终审，再交付。本地通过不等于已经部署。
4. 按 [delivery.md](references/delivery.md) 把发布关联到确切 commit、版本、产物和配置。目标上的实际版本、关键业务路径和产物分别留证。开发通过、平台发布、安装包交出去，都不等于目标已经验收。
5. 当前访问不了目标时，写出操作者要跑的命令和预期结果，标成待部署或待验收。没有回传就不要写成已经完成。
6. 构建和部署适配这一层的通过条件读 shipwright-test。业务上「这就是要的」由人在目标环境确认。

## Stop

目标环境的版本和关键路径有证据，或明确写出还缺哪一次验收。不要把恢复旧版本和这次发布写进同一步。

## Handoff

出问题或拿到运行日志时交给 shipwright-recover。计划状态交给 shipwright-reconcile。
