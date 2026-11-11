# Investigation

Source: pstack `playbooks/investigation.md`. Read-only. The product is a cited explanation or a recommendation, not a code change. shipwright-diagnose links here when the request is an investigation rather than a live fault.

1. Route the "how does this run" part through shipwright-how. For a motivation question, also route through shipwright-why.
2. The throughput checkpoint stays one line: `throughput checkpoint: n/a, read-only investigation`.
3. Produce the how-shaped output (Overview, Key Concepts, How It Works, Where Things Live, Gotchas), or a recommendation with a tradeoffs table when the request is a choice between alternatives.
4. Run the wording pass in shipwright-write before the reply leaves. Keep conditions, evidence, and unknowns. Cut filler.

No PR, no CI babysitting, and no shipwright-architect, unless the investigation is the step before a code change. If it is, hand back and let shipwright-flow route to shipwright-diagnose or shipwright-build. Do not start that work here.

**Reply:** the investigation output. For "are we sure?" answers, include the real judgment and the reasons. Push back when the premise is wrong.

## Evidence

An investigation does not need a product screenshot unless the question is about behavior on a real surface. When it is, save the shot under `/tmp/shipwright-<plan-id>/<sha7>/` using the shared evidence rules (the file `references/evidence.md` is added separately). A shot of an HTML explainer does not count. If the surface cannot be judged, or the shot is the wrong surface, say so. That is not a pass.
