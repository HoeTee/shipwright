---
title: Click round 1
subtitle: 16 bugfix questions. One run with shipwright skills. One run with no shipwright skills.
author:
date: 2026-11-11
version: round1
source: Hidden checks and the Click suite on the agent code. Judge scores on anonymous diffs.
scope: pallets/click bugfix commits. Parent tree. Official tests restored at score time.
lang: en
template: sheet
theme: blueprint
mode: light
cols: 1
---

## A Key chart

Source lines changed in product code. Test files are not in these bars. Lower is smaller.

```chart bar
| Skills | Plain
q01 | 47 | 50
q02 | 4 | 49
q03 | 5 | 24
q04 | 8 | 5
q05 | 25 | 26
q06 | 37 | 56
q07 | 8 | 13
q08 | 19 | 39
q09 | 5 | 37
q10 | 8 | 8
q11 | 26 | 39
q12 | 7 | 13
q13 | 2 | 2
q14 | 37 | 45
q15 | 16 | 22
q16 | 8 | 16
```

On this single run the skills arm changed fewer source lines on 13 of 16 questions. The across-question ratio is 0.55. The 95% interval across questions is 0.38 to 0.77. There is no second run, so this gap is not a claim of a win.

## B Verdict

```callout
Verdict: inconclusive. Hidden checks passed 15 of 16 times in each arm. One run per arm is too small to claim a difference.
```

| Item | With skills | No skills |
|---|---:|---:|
| Questions run | 16 | 16 |
| Hidden checks passed | 15 | 15 |
| Full suite passed | 15 | 15 |
| Source lines | 262 | 444 |
| Judge wins | 8 | 2 |
| Judge ties | 6 | 6 |

The full suite failed only where the hidden check failed. That was question q09, on both arms.

## C Pass and judge

```chart bar
| Skills | Plain
Hidden checks passed | 15 | 15
Full suite passed | 15 | 15
Judge wins | 8 | 2
```

Judge ties: 6. Ties are not in the win bars.

The judge was Composer 2.5. A known-good patch scored above a known-bad patch before these 16 packets. The judge did not know which arm was which.

## D Per question

| ID | Commit | Hidden skills | Hidden plain | Lines skills | Lines plain | Judge |
|---|---|---|---|---:|---:|---|
| q01 | c53d3732b9 | pass | pass | 47 | 50 | tie |
| q02 | f67c2bb6c2 | pass | pass | 4 | 49 | skills |
| q03 | f58ca3e814 | pass | pass | 5 | 24 | plain |
| q04 | 82f377c547 | pass | pass | 8 | 5 | skills |
| q05 | b7e5fd4cc7 | pass | pass | 25 | 26 | tie |
| q06 | 7d05a59b9d | pass | pass | 37 | 56 | skills |
| q07 | 0551bf5358 | pass | pass | 8 | 13 | tie |
| q08 | a09c1c655e | pass | pass | 19 | 39 | tie |
| q09 | 546f2851f4 | fail | fail | 5 | 37 | skills |
| q10 | 91de59c6c8 | pass | pass | 8 | 8 | tie |
| q11 | 1c20dc6e72 | pass | pass | 26 | 39 | skills |
| q12 | a1235aacb1 | pass | pass | 7 | 13 | skills |
| q13 | ac6a2acfdb | pass | pass | 2 | 2 | tie |
| q14 | 4fd2fea0db | pass | pass | 37 | 45 | skills |
| q15 | 70c673d37e | pass | pass | 16 | 22 | skills |
| q16 | c326df95e9 | pass | pass | 8 | 16 | plain |

Full commit ids are in `questions.json`.

## E Checks versus judge

```callout
q03: the judge said the skills patch misses copy and deepcopy. The hidden check passed for both arms.
```

```callout
q09: the judge said both patches fix the bug. The hidden check failed for both arms. The official commit passes that check here.
```

The hidden check is the primary result. Judge text is unchanged.

## F Limits

One run per arm. The procedure asks for five. Pass rates match, so these questions do not show a quality gap.

15 questions passed on both arms. Those questions do not prove a difference.

The host did not report tokens, steps, or a per-run timer.

Both arms already had the host helper skills. Only the shipwright pack was added on one arm. The eval skill was not in that pack.
