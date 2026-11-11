# Reproduce and locate

Source: pstack `playbooks/bug-fix.md`, steps 1 and 2 only. Steps 3 through 6 (plan the fix, verify the fix on the same surface, commit the failing repro first, open the PR) belong to shipwright-build. This skill stops when the mechanism is confirmed.

Be scientific. Every later line of a fix has to trace to runtime evidence. A belt-and-suspenders change that "might help" is a hypothesis, not a diagnosis. When evidence refutes a hypothesis, drop what it motivated. Do not ship a guess from this skill. This skill ships nothing.

## Step 1. Reproduce on the real surface

Reproduce it yourself on the matching surface, even when a debug or instrumentation note says to ask the user to reproduce. The surface is the one the user actually hits: the page, the desktop app, or the CLI.

Ask the user only with a stated, specific reason that surface cannot be reached, and only after driving it as far as it goes. If it will not reproduce directly, synthesize the trigger, tighten the conditions, or instrument until it fires.

Save the repro under `/tmp/shipwright-<plan-id>/<sha7>/before-<slug>.png` when the surface is visible, plus a same-named `.aria.txt` snapshot when the surface has one. A CLI or API fault saves the terminal record or response body as `.txt` or `.json` instead. The shared rules for what counts live in `references/evidence.md`, added separately. Mask secrets before any shot. An inconclusive result, or a shot of the wrong surface, is not a pass. Say so. A unit test does not mean the bug has been seen.

## Step 2. Binary-search the cause

Form the candidate hypotheses, then rule them out until one survives. Seed them with shipwright-how over the affected subsystem and shipwright-why for the regression history.

Each pass, take the split that cuts the most remaining problem space, get runtime evidence, and eliminate. When program state is unclear, add instrumentation or logging and read it as the code runs. Do not guess. If the hunt is long, write the next split down and keep going. Do not wait on a person for a reversible read.

Confirm the surviving mechanism with runtime evidence before anyone plans a fix. If that later fix would cross a function boundary, the handoff says so. shipwright-architect is not run here.

## Throughput

One line: `throughput checkpoint: n/a, read-only diagnosis`.

## Reply

What is broken, the surviving mechanism, the runtime evidence, and the `file:line`. No fix unless the user separately routes to shipwright-build. Paste the repro output verbatim.
