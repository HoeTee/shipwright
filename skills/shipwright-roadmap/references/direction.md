# Direction

Source: improve audit playbook, category 9, and the `next` invocation. These are options, not bugs. They do not share a table with P0/P1/P2 defects.

## Grounding rule

Every suggestion must cite evidence from the repo. A suggestion that could apply to any project in the category ("add dark mode", "add AI") is noise, not a finding. Sources of grounded direction:

- **Unfinished intent.** TODO or FIXME clusters around one theme, feature flags never rolled out, stubbed or half-built modules, commented-out feature code, abandoned mid-feature work visible in git history.
- **Stated but undelivered.** README, docs, or roadmap promises with no corresponding code. CLI flags or config options that are no-ops. Issue templates for features that do not exist. A PRD or `PRODUCT.md` that names users, use cases, or a direction the code has not caught up to is the strongest signal. Prefer it over inferred intent. Never propose something a decision doc already rejected. Note the contradiction instead.
- **Surface asymmetries.** One-directional pairs (export without import, create without bulk-create, webhooks out but not in). Entities with CRUD minus one. A public API that internal code clearly needed and hand-rolled around.
- **The adjacent possible.** Capabilities the existing architecture makes disproportionately cheap: a plugin system one interface away, a public API one route file from the existing service layer, an integration the data model already supports.
- **Friction worth productizing.** Things users of this project evidently do by hand around it (visible in docs, examples, issues) that the project could absorb.

## Finding adaptations

Use the return shape in shipwright-audit's `references/subagent-brief.md`, with two changes. **Impact** is product or user value: who wants this and why now. **Confidence** reflects how grounded the evidence is, not certainty that it is the right call. Strategy belongs to the maintainer. The advisor's job is grounded options with honest trade-offs. Effort estimates here are coarser. Say so.

## What a selected item becomes

A plan for a selected direction finding is usually a design or spike plan: investigate, prototype, define the API, list open questions. It is not a build-everything plan. Scope it that way. shipwright-plan writes the file. An empirical fork goes to shipwright-prototype before the plan commits to a shape. A new module or interface goes to shipwright-architect.

## Experience

When implementation convenience conflicts with the user's delight, choose delight. That is principle `experience-first` in the shared principles directory. Do not restate it. The user is whoever consumes the work: the person at the screen, the colleague who imports a library, and the next engineer. Weigh their experience the same way. Ship less and ship it better. Prototype before committing. Tighten the core loop. A feature that does not serve that loop gets out of the way.

## Invocation

`next`, `features`, or `roadmap` means: recon, then this category only, in more depth. Four to six grounded suggestions, each with evidence, trade-offs, and a coarse effort estimate. An ordinary audit hands over at most two to four, after its defect table, and does not bury them under bugs.
