# Click round 1

Verdict: inconclusive.

16 questions ran. Each question ran once with the shipwright skills and once with no shipwright skills. 32 runs finished. None were skipped. None crashed.

The hidden check passed 15 of 16 times with skills. It passed 15 of 16 times with no skills.

The full Click suite passed 15 of 16 times with skills. It passed 15 of 16 times with no skills. The only suite failures are the same hidden checks on question q09.

The sample is one run per arm. The procedure asks for five runs per arm. One run is too small to claim a difference.

## What was measured

Arm A had the shipwright skill pack. Arm B had no shipwright skills. Both arms used the same model and the same task text. The model was the session model, Grok 4.7.

The task was a bug report. The working tree was the parent of a real Click fix. The new regression check was not in that tree. Scoring put the tests from the fix commit back, kept the agent product code, and ran pytest 9.0.2 on Python 3.12.

A file-open log shows every skills run opened shipwright skill files. Every plain run opened none.

## Headline numbers

| Item | With skills | No skills |
|---|---:|---:|
| Questions run | 16 | 16 |
| Hidden checks passed | 15 | 15 |
| Full suite passed | 15 | 15 |
| Source lines changed | 262 | 444 |
| Judge wins | 8 | 2 |
| Judge ties | 6 | 6 |

The judge ties are 6. Those 6 are not wins for either arm.

On this single run, the skills arm changed fewer source lines on 13 of 16 questions. The across-question geometric mean of the line ratio (skills divided by plain) is 0.55. The 95% bootstrap interval across questions is 0.38 to 0.77. That interval does not contain 1.

The stats script returns `improved` if it treats one sample as exact. This report does not use that label. One run has no within-arm range. The gap cannot be checked against run-to-run noise.

15 questions passed the hidden check on both arms. Those questions do not prove a difference. q09 failed the hidden check on both arms.

## Judge

The judge was Composer 2.5. Claude, GPT, and Gemini were rejected by the host, so a different available family was used. The judge saw labels `patch-red` and `patch-blue` only.

Before the real packets, the judge scored a known-good patch and a known-bad patch. The good patch scored higher. The judge then scored the 16 packets.

The judge gave the skills arm 8 wins, the plain arm 2 wins, and 6 ties.

Two scores disagree with the hidden check:

- q03. The judge said the skills patch does not fix copy and deepcopy. The hidden check passed for both arms.
- q09. The judge said both patches fix the bug. The hidden check failed for both arms. The official Click commit passes that same check here.

The hidden check is the primary result. The judge scores stay as the judge wrote them.

## Per question

| ID | Click commit | Hidden skills | Hidden plain | Suite skills | Suite plain | Lines skills | Lines plain | Judge |
|---|---|---|---|---|---|---:|---:|---|
| q01 | c53d3732b98c764932e146c007146ad402acb229 | pass | pass | pass | pass | 47 | 50 | tie |
| q02 | f67c2bb6c2f055c1c7a57cd46c3697fc26a7742e | pass | pass | pass | pass | 4 | 49 | skills |
| q03 | f58ca3e81424a35626c8a475eb59ab95589008ce | pass | pass | pass | pass | 5 | 24 | plain |
| q04 | 82f377c547e1867d073f02bb8f476214d07e245b | pass | pass | pass | pass | 8 | 5 | skills |
| q05 | b7e5fd4cc7de70280eccd39f2bb956df617e5519 | pass | pass | pass | pass | 25 | 26 | tie |
| q06 | 7d05a59b9d46a415d85937630d1d812cf477f60a | pass | pass | pass | pass | 37 | 56 | skills |
| q07 | 0551bf53588ae87f462d336f24f853a156fefe3a | pass | pass | pass | pass | 8 | 13 | tie |
| q08 | a09c1c655eef3d43181eb46036b66cf058d72df4 | pass | pass | pass | pass | 19 | 39 | tie |
| q09 | 546f2851f414b07413777ebcae89b2c21a685252 | fail | fail | fail | fail | 5 | 37 | skills |
| q10 | 91de59c6c8abc8251e7af551cd4546cc964288af | pass | pass | pass | pass | 8 | 8 | tie |
| q11 | 1c20dc6e724cd5625faaa17b715ba928d44c08bf | pass | pass | pass | pass | 26 | 39 | skills |
| q12 | a1235aacb1be55dc66ddcfefbf64dec44b6ab54d | pass | pass | pass | pass | 7 | 13 | skills |
| q13 | ac6a2acfdb4550c35ce69ce54db502ba96c96324 | pass | pass | pass | pass | 2 | 2 | tie |
| q14 | 4fd2fea0db423d242aedcae0a5f664efe0a93484 | pass | pass | pass | pass | 37 | 45 | skills |
| q15 | 70c673d37eb91ba42a129be9037caf3ebed62f3e | pass | pass | pass | pass | 16 | 22 | skills |
| q16 | c326df95e9e3da0425360e030413f6a3ee25fdee | pass | pass | pass | pass | 8 | 16 | plain |

Question text and the parent commit are in `questions.json`. One JSON record per run is in `records/`.

## Seven questions

1. The limit on the pass rate is the size of these bugs. Both arms already pass 15 of 16 hidden checks. Skills were opened on every skills run.
2. Both arms used the same model, the same task text, and the same ban on a second agent and on a pull request. The host's own helper skills were present on both arms.
3. A pass-rate gap cannot exceed the share of questions where the skills can matter. Here that gap is 0.
4. 32 runs delivered code. 0 runs were skipped. q09 failed the check on both arms. The official commit passes that check in this environment.
5. Each arm ran once. Five runs are required before a gap can be compared with run-to-run noise. That comparison was not done.
6. The questions are real Click bugfix commits that add or change a regression check. They are small.
7. The skills arm opened skill files. The plain arm did not. The hidden check and the full suite ran on the agent product code plus the official tests.

## Time, steps, and tokens

The host did not report per-run time, step count, or token count.

Four batches of eight runs were in parallel. The wall clock from the batch start stamp to the next stamp is an upper bound, because it includes the pause before the next stamp:

| Batch | Questions | Upper bound seconds |
|---|---|---:|
| 1 | q01 to q04 | 694 |
| 2 | q05 to q08 | 549 |
| 3 | q09 to q12 | 433 |
| 4 | q13 to q16 | 636 |

## Caveats

The working tree had no git history. The agent was told to stay in that tree.

`shipwright-eval`, `shipwright-arena`, and `shipwright-skillsmith` were left out of the pack. Their text names an evaluation. The other shipwright skills were installed.

The bugfix skill says to open a pull request and to hand work to another agent. Both arms were told not to do those things, because this tree has no remote and the run had to stay in one place.

The full suite needs the `less` program for pager checks. It was installed before scoring. With `less` present, the official commit for the first question passes the suite: 2111 passed, 24 skipped.

Source lines do not count test files. Test lines are in the CSV.
