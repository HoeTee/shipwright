# Vet, prioritize, confirm

Source: improve, Phase 3. Workers over-report. The main agent opens the cited code.

## Three failure classes

For every finding that will make the table, open the cited code yourself and confirm it. Expect three failure classes:

- **By-design behavior** reported as a bug or a vulnerability. Honoring `https_proxy` flagged as SSRF is the standard proxy convention. A tradeoff explicitly recorded in an ADR or decision doc from recon is settled, not a finding. A stale ADR is itself a finding: if the code has drifted from the decision doc, report the drift. Do not use the doc to suppress it.
- **Mis-attributed evidence.** The finding is real and the file or line is wrong.
- **Duplicates** across workers.

Downgrade, correct, or reject. Record rejections in the index's "Findings considered and rejected" section so they are not re-audited next run. The index shape is shipwright-plan's [index template](../../shipwright-plan/references/index.md).

## Ordering

Present the vetted findings ordered by leverage: impact ÷ effort, discounted by confidence and by the risk of the fix. The repeatable sort is `scripts/rank_findings.py`. Tiebreakers, in order:

1. Anything that unblocks other findings (a verification baseline, characterization tests) floats up.
2. Security findings with HIGH confidence float above equivalent-leverage non-security findings.
3. Prefer findings whose fix has a clean verification story.
4. "Not worth doing" is a valid verdict. Record it with one line of reasoning.

Severity in the table is only P0, P1, or P2. The canonical record is [finding.md](../../../references/finding.md). Workers return the shape in [subagent-brief.md](subagent-brief.md). P0 is a disaster in normal use. P1 breaks a core function, permission, or data on a reachable path. P2 is a real defect with limited impact. P0 and P1 block by default. Whether P2 blocks depends on the project's rules. A suggestion with no actual defect is a non-blocking note. Do not force it into P2.

## Direction is not a row in this table

Direction findings are options for the maintainer. Do not rank "build a plugin system" against "fix the N+1". Hand them to shipwright-roadmap after the table. Two to four grounded suggestions is the audit's cap when roadmap is not the requested product. A `next` / `features` / `roadmap` invocation is roadmap's job, not a deeper audit table.

## What you ask the user

Ask which findings become plans. Default suggestion: the top 3–5, plus anything they flag. Also surface dependency ordering, for example "characterization tests for module X must land before the refactor of X."

Wait for the selection. Do not write 30 plans nobody asked for. If nobody is available to choose, shipwright-plan writes plans for the top 3–5 by leverage and records that default in `plans/README.md`.

## Plain-language rendering

When a person will read the report, render each vetted finding in the four parts from [quick.md](quick.md): what this is, the problem, the fix, and what happens if we skip it. Keep the P0/P1/P2 record. The four parts are the rendering, not a second severity scale. Empty groups are omitted.
