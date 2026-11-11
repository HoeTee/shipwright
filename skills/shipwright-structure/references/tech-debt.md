<!--
Adapted from improve `references/audit-playbook.md` section 5 (MIT).
Copyright (c) 2026 shadcn
https://github.com/shadcn/improve
Sections 6 and 7 of that playbook belong to shipwright-audit
(deps.md and dx.md). They are not copied here.
-->

# Tech debt and architecture

- Duplication: the same logic re-implemented in 3+ places (search for near-identical functions or components); divergent copies that have drifted.
- Layering violations: UI importing from data-layer internals, circular dependencies, "utils" modules that became a junk drawer with high fan-in.
- Dead code: unexported and unused modules, feature flags fully rolled out but still branching, commented-out blocks with no explanation, dependencies in the manifest that are no longer imported.
- God objects and modules: files an order of magnitude larger than the repo median that everything touches; functions with double-digit parameters or deep conditional nesting.
- Inconsistent patterns: three ways of doing data fetching, error handling, or styling in the same repo. Pick the winner (the one the team converged on most recently) and plan the consolidation.
- Abstraction mismatches: premature abstractions with a single implementation, or missing abstractions where the same change always requires touching N files in lockstep.

Before calling code unused, search the whole tree, including tests, fixtures, config, and string or dynamic references. An empty direct-call search is one piece of evidence. It does not by itself prove the code can be deleted.

A `shortcut:` or older `ponytail:` comment that names its ceiling is a recorded deferral, not a structure finding, until the expected load crosses that ceiling. The ledger of those comments is shipwright-debt.
