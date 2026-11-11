# Effort levels

Source: improve, Phase 2. Default is `standard`. The user sets it with a `quick` or `deep` keyword anywhere in the invocation. It composes with a focus: `quick security`, `deep` plus the issues flag on shipwright-plan.

| | `quick` | `standard` (default) | `deep` |
| --- | --- | --- | --- |
| Coverage | Recon hotspots only: highest-churn, highest-criticality code | Hotspot-weighted, key packages | Whole repo, every package |
| Workers | 0–1 (sweep directly when feasible) | ≤4 concurrent | ≤8 concurrent, one per category |
| Breadth | medium | very thorough for correctness and security, medium for the rest | very thorough everywhere |
| Categories | bugs, security, test | all nine | all nine |
| Findings | top ~6, HIGH-confidence only | full table | full table, including LOW-confidence investigate items |

`quick` uses [quick.md](quick.md) for the pass and the plain-language rendering. `standard` and `deep` use the category routing in [procedure.md](procedure.md).

Whatever the level, say in the final report what was not audited. On a large monorepo even `deep` scopes workers to packages, not the root.

Every finding needs evidence (`file:line`), impact, effort (S/M/L), risk of the fix itself, and confidence. No vibes-only findings. "Probably has N+1 queries somewhere" is not a finding. `orders/api.py:142 issues one query per order item inside a loop` is.
