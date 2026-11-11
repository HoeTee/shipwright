# Why procedure

Source: pstack `why`. The host tooling map is removed. Dispatch is [../shipwright-how/references/hosts.md](../../shipwright-how/references/hosts.md). Confidence rules are [epistemics.md](epistemics.md). The review-shaped companion is [method.md](method.md).

Investigate the motivation and intent behind code. shipwright-how answers what it does. This skill answers what forces led to its shape.

## Operating posture

Careful and cautious. Prefer primary evidence. Put the tier in the same sentence as the claim. Investigators must not write product code. The synthesizer cites sources and spot-checks them.

## Workflow

1. **Frame** the question: whose decision, which surface, and what "why" means here (history, constraint, incident, or tradeoff). Anchor the code first so the search is about this version and these symbols, not a similar name.
2. **Pick sources** from [source-playbook.md](source-playbook.md) and the playbooks under [sources/](sources/). Use only systems the user has connected. Always include source control. Add [sources/incident-postmortem.md](sources/incident-postmortem.md) when the target looks defensive: null checks, retry, timeout, rate limit, feature flag, egress guard, or an out-of-memory handler.
3. **Fan out investigators**, one per source, with [investigator-prompt.md](investigator-prompt.md) plus that source's playbook. Investigators gather. They do not conclude. Dispatch them in one round. Repo archaeology uses git and the host's git client. Prefer a connected tracker over scraping. If a connector is missing or not authenticated, record the gap. The repeatable git commands are `scripts/code_archaeology.py`.
4. **Synthesize** with [synthesizer-prompt.md](synthesizer-prompt.md), after reading [epistemics.md](epistemics.md) in full. Lead with the best-supported motivation. List competing theories with their evidence. Do not pick the tidy story when the sources disagree.
5. **Output**: short answer first, then evidence with links or paths, then open questions. Keep the hedges. They are findings. Do not invent org history. If a source was not searched, say what could not be checked.

## Tiers

Every claim sits in one tier. The words and the tests are in [epistemics.md](epistemics.md). Do not collapse them.

| Tier | Chinese name in the reply | When |
| --- | --- | --- |
| Direct | 确证 | An author wrote the reason. Cite it. |
| Supported | 有支持 | Several indirect items converge. Cite each. |
| Inferred | 推断 | A reading the record does not state. Hedge it. |
| Speculative | 猜测 | A thin hypothesis. Other explanations fit as well. |
| Unknown | 未知 | The search happened and found nothing. Name the search. |

Code shows what it does, not why it exists. Never cite code as evidence of its own intent.

## Review use

For a review, also follow [method.md](method.md): separate why it was built that way, whether that is still reasonable, and whether the user set a new goal. A past reason does not authorize a redesign. Changing the design goes back to shipwright-flow.

## Domain handoff

Settled tradeoffs recorded in an ADR are a constraint for [shipwright-security](../../shipwright-security/SKILL.md) and [shipwright-structure](../../shipwright-structure/SKILL.md). This skill reports the record. It does not apply their checklists.

## Stop

Hand the cited answer back. Do not write code, do not open a plan, and do not start shipwright-architect. A hypothesis the user embedded in the question is a candidate, not a conclusion.
