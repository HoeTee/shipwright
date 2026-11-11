# Finding

One shape for every confirmed finding. Severity is only P0, P1, or P2. The leverage formula orders the work. It does not invent a fourth severity.

## Severity

Human review, the first pass, and a re-review use this table. When the project already has a severity scale, keep the project's level and write the mapping to this table. Do not use the mapping to lower the project's bar.

| Level | Meaning | Example |
| --- | --- | --- |
| P0 | On a supported, normal path, the result is catastrophic and must be handled now. | Startup unconditionally deletes user data. |
| P1 | A reachable path breaks a core function, an authorization check, or data safety, and should be fixed first. | An ordinary user can read another user's private record. |
| P2 | There is a real trigger and a real effect, but the blast is limited. It still needs a fix. | An empty list the project promised to support fails that operation. |

Grade by the actual effect and the trigger, not by the size of the diff, the number of reviewers, or a guess. A style preference or a simplification with no defect goes in a separate list of non-blocking suggestions. Do not invent a P2 to fill the table. An unconfirmed suspicion lists the missing evidence and is not a confirmed finding.

Sort P0, then P1, then P2. Open with the unsolved counts. Record fixed items, accepted residual risk, and false positives separately, keeping the original id and level, so they do not inflate the open counts. Zero findings still say `P0: 0 · P1: 0 · P2: 0`.

Each item has a title, file, line, and commit, the trigger, the actual consequence, the evidence and whether it was executed, a proposed fix, the status, and whether it blocks. Severity and the merge gate are separate fields. P0 and P1 block by default. Whether P2 blocks depends on the project rules and a recorded decision. A requirement the project already called mandatory is not skipped by labeling it P2. With no project decision, leave it open and give a recommendation. Do not accept the risk yourself.

Example of the counts: `unsolved P0: 0 · P1: 1 · P2: 0`, then the item. A fixed item is listed apart. Do not write only "two issues", do not count a fixed item as open, and do not hide an open P1 because CI is green.

## Record

```text
[P1] 下载接口没查订单归属      blocking: yes   domain: security   introduced
evidence:   api/orders.py:L88 @ e4f5a6b
            截图 after-download-leak.png（已贴进 PR #42 评论和结果页）
trigger:    用户 A 用自己的登录态请求 /orders/42/download，订单属于用户 B
impact:     A 拿到 B 的发票
effort: S   risk: LOW   confidence: HIGH（已运行复现）
fix:        load_order 之后比较 order.owner_id == user.id，不相等返回 403
status:     open
```

`introduced` means this change added it. `pre-existing` means it was already in a file this change touched. Do not blame the branch for old debt, and do not hide what the branch is building on.

For a person, render the same record in four parts: what it is, what goes wrong, how to fix it, and what happens if it stays.

## Fields the audit still fills

Every finding, from every category, comes back with these fields. They sit on the record above. They do not replace P0, P1, or P2.

```markdown
### [CATEGORY-NN] Short imperative title

- **Evidence**: `path/file.ts:123` — one sentence on what is there. Repeat per location. Two to five of the strongest locations. Note "and ~N similar sites" when it is widespread.
- **Impact**: What goes wrong, or what is being paid, because of this. Concrete: "every order-list render issues 1+N queries", not "suboptimal".
- **Effort**: S (hours) / M (about a day) / L (multi-day), for the fix, including tests.
- **Risk**: What the fix could break. LOW, MED, or HIGH, plus one line why.
- **Confidence**: HIGH (read the code, certain) / MED (strong signal, needs verification) / LOW (a smell, needs investigation). A LOW finding may be reported, and it gets an investigate plan, not a fix plan.
- **Fix sketch**: One to three sentences. Not the plan. Just enough to judge the effort honestly.
```

Direction findings use the same fields with two changes. Impact is who wants this and why now. Confidence is how grounded the evidence is, not certainty that it is the right product call. Strategy belongs to the maintainer. The advisor's job is a grounded option with an honest tradeoff. Effort estimates here are coarser, and the note says so. A selected direction becomes a design or spike plan, not a build-everything plan.

## Order

Order by leverage = impact ÷ effort, discounted by confidence and by the risk of the fix. Tiebreakers:

1. Anything that unblocks other findings (a verification baseline, characterization tests) floats up.
2. A HIGH-confidence security finding floats above a non-security finding with the same leverage.
3. Prefer a finding whose fix has a clean verification story.
4. "Not worth doing" is a valid verdict. Record it with one line, so the next run does not audit it again.

Vet a finding before it enters the table. Open the cited code yourself. Expect three failure classes: by-design behavior reported as a bug (honoring `https_proxy` is the normal proxy convention, and a tradeoff written in an ADR is settled), evidence that is real but attributed to the wrong file or line, and the same finding from two workers. Downgrade, correct, or reject. Record a rejection where the plan index keeps "Findings considered and rejected".
