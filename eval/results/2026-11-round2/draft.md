---
title: Click round 2
subtitle: 2 runs per arm. 16 Click bug fixes. Skills against no skills.
author:
date: 2026-11-12
version: round2
source: Hidden tests on the agent code. Python line counts from the diffs.
scope: The round 1 Click questions. No harder set.
lang: en
template: sheet
theme: blueprint
mode: light
cols: 1
---

## A Key chart

Python lines changed. The plain arm is set to 100. The skills bar is the across-question ratio times 100. Lower is smaller.

```chart bar
| Lines
Plain | 100
Skills | 56.6
```

The ratio is 0.566. The 95% interval is 0.426 to 0.730. That is 43.4% fewer Python lines, with an interval of 27.0% to 57.4% fewer.

Hidden tests passed 30 of 32 runs on each arm.

## B What counted

```callout
The line ratio is conclusive. The hidden-test pass rate is the same on both arms. The blind judge was not run in this round.
```

The gap clears the run-to-run spread on 6 of 16 questions. The pooled interval is still below 1 because 14 of 16 question medians are lower with skills.
