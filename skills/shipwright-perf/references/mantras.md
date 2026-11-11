<!--
Adapted from the pstack performance-issue playbook.
The seven mantras, the stop rule, and the reply contract are assigned
to shipwright-perf. The surrounding procedure (baseline capture, delegation,
artifact parse, opening the PR) is assigned to shipwright-build
`references/perf.md` and is not duplicated here.
-->

# Performance mantras

You own the measurement story. Tie every fix to a measurement. Reading the source is not a measurement.

Do not claim a performance ceiling without running it first. Vet the baseline, and each later number, with [Benchmark checklist](benchmark-checklist.md). Principle [explain-the-number](../../../references/principles/explain-the-number.md) is the shared rule for any number you are about to trust: write the decision first, name the limiter, and keep the run count and the spread with the number.

Try the mantras in order, cheapest first:

1. Don't do it. Stop work whose result nothing uses rather than cheapening it.
2. Do it, but don't do it again.
3. Do it less.
4. Do it later.
5. Do it when they're not looking.
6. Do it concurrently.
7. Do it cheaper.

When an earlier mantra meets the target, stop.

For sustained improvement of one metric against a target, use [Hillclimb](hillclimb.md). A one-off fix stays on this list.

## Reply

The reply carries the baseline number, the post-fix number, the delta, and the artifact path. "Inconclusive" or a measurement of the wrong surface is not a pass. Flag it.

`scripts/summarize_runs.py` turns alternating runs into a median, a range, and a verdict of faster, slower, no measurable difference, or inconclusive.
