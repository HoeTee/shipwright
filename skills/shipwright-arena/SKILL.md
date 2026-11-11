---
name: shipwright-arena
description: "N 个候选做同一件事，评出底稿再嫁接长处。用于：一次做容易定错形状的产物。不要用于：切片并行找 swarm。"
---

# shipwright-arena

## When to use

何时用：一次做成容易把形状定死，需要几份独立候选再合成。

何时不用：按切片分头查。那是 shipwright-swarm。

## Procedure

先列六个阶段：Frame、Fan out、Cross-judge、Pick、Graft、Verify。全文在 [Arena procedure](../../references/arena/procedure.md)。

1. Frame。每个候选收到同一份任务，任务就是契约。另写 3 到 6 条可打分的标准，只给挑选的人看，不给候选。选手来自设置文件的 `arena runners` 行。每个候选有自己的 worktree，或 `/tmp/arena-<slug>/candidate-<n>/`。
2. Fan out。同一轮派出去。简报含任务、共享材料路径、自己的输出路径，以及考虑过并否决了什么。掉线一个就用剩下的，并记下来。没有并行能力就逐个做，并写明不是并行。
3. Cross-judge。候选都写完之后，从 `arena cross-judge pool` 里挑一个与父模型不同家族的只读评委。评委按路径标签打分，并推荐一份底稿。评不起来就跳过，并写明，然后自己选底稿。
4. Pick。自己把每份候选读完，按标准逐条打分，再和评委对照。一致就确认。不一致就先读两边的理由：不是评委偏了，就是标准含糊。打成平手时选边界更干净或接口更小的那份。
5. Graft。每份落选候选通常只取一两处长处，手工折进底稿，保持一个心智模型。大家收敛成同一形状就采用它，不必嫁接。差得太远就回到 Frame，不要取平均。
6. Verify。合成结果照常验证，见 [Evidence](../../references/evidence.md)。验证发现 arena 漏了的问题，就重做 Frame，或回到 Graft。不要把问题盖住。

## Output

一份合成产物，外加短注：底稿是哪份、为什么、评委结论或跳过了评委、每处嫁接来自哪份候选、否决了什么、有没有收敛或掉线、验证结果。

shipwright-eval 在同时比较多个版本时借用这里的并行和异族评委。评测步骤仍由 shipwright-eval 写。
