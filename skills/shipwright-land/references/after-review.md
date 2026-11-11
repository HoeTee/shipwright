## After human review

CI 与 AI 审查可并行。人工最终检查核对已完成修复、验证与复审的版本，不逐项批准常规修复；要求修改时返回 AI 阶段并继承原轮次上限。按 [the human packet](../../shipwright-signoff/references/packet.md)交付材料，并等待用户明确结论。平台要求人类审批时由实际有资格的人完成，AI 不代替；调查单人账号的自审限制，避免配置不可满足的规则。

合并前再次读取当前 head、对应检查与人审范围。新提交影响结论时补验证并再次确认受影响部分；遵守平台对旧审批失效的实际规则。不要因一次历史“同意”批准以后所有提交。

合并后按 shipwright-deploy and shipwright-recover记录实际合并 commit 与后续状态。
