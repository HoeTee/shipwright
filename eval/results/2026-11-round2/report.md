# Click round 2

16 real Click bug fixes. The same agent ran with Shipwright skills and with no skills. Each arm ran 2 times on each question.

The model was the session model. The questions are the round 1 bank. The third planned repeat was not started. A harder question set was not run.

## Result

Hidden tests passed 30 of 32 runs with skills and 30 of 32 runs with no skills. The difference is +0.000. The 95% interval is +0.000 to +0.000. That interval does not include a pass-rate advantage.

Python lines changed, tests excluded: the across-question ratio of medians is 0.566. The 95% interval is 0.426 to 0.730. The interval is below 1. The skills arm changed fewer Python lines. In percent, that is 43.4% fewer lines. The 95% interval is 27.0% to 57.4% fewer.

The median ratio is below 1 on 14 of 16 questions. The gap is larger than that question's own run-to-run spread on 6 of 16 questions.

The median run-to-run range in Python lines is 1.5 lines with skills and 4.5 lines with no skills. Hidden pass or fail did not flip inside an arm on 16 of 16 questions for skills and 16 of 16 for no skills.

The Click suite, with the flaky pager test removed, passed on the same runs as the hidden tests. The pager test failed on and off in this environment, including on trees that had passed it before. It is not in the pass rate.

The blind judge was not run again. New agent runs were stopped before judging. There is no round 2 win, loss, or tie count.

## What is conclusive

The pooled Python-line ratio is conclusive. Its 95% interval is below 1.

The hidden-test difference is not an advantage. Both arms passed the same questions.

The full suite does not add a separate result once the flaky pager test is set aside.

Judge scores are absent.

## Per question

Median Python lines are the middle run for that arm. Hidden cells are passes over runs.

| ID | Commit | Hidden skills | Hidden plain | Median lines skills | Median lines plain |
|---|---|---|---|---:|---:|
| q01 | c53d3732b9 | 2/2 | 2/2 | 30 | 52 |
| q02 | f67c2bb6c2 | 2/2 | 2/2 | 4 | 30 |
| q03 | f58ca3e814 | 2/2 | 2/2 | 4 | 20 |
| q04 | 82f377c547 | 2/2 | 2/2 | 6 | 12 |
| q05 | b7e5fd4cc7 | 2/2 | 2/2 | 28 | 28 |
| q06 | 7d05a59b9d | 2/2 | 2/2 | 24 | 50 |
| q07 | 0551bf5358 | 2/2 | 2/2 | 8 | 12 |
| q08 | a09c1c655e | 2/2 | 2/2 | 25 | 31 |
| q09 | 546f2851f4 | 0/2 | 0/2 | 6 | 22 |
| q10 | 91de59c6c8 | 2/2 | 2/2 | 8 | 8 |
| q11 | 1c20dc6e72 | 2/2 | 2/2 | 34 | 26 |
| q12 | a1235aacb1 | 2/2 | 2/2 | 8 | 12 |
| q13 | ac6a2acfdb | 2/2 | 2/2 | 2 | 3 |
| q14 | 4fd2fea0db | 2/2 | 2/2 | 29 | 36 |
| q15 | 70c673d37e | 2/2 | 2/2 | 16 | 22 |
| q16 | c326df95e9 | 2/2 | 2/2 | 8 | 14 |

## Method

Each question is a real Click bugfix commit. The agent saw the parent tree and a bug report. The official regression test was not in that tree. Scoring copied the agent's product files onto a clean parent tree, then restored the official tests from the fix commit.

Python lines are added and removed lines in `.py` files outside tests. Cache directories are not counted. A line count uses `diff -u` for files that exist on both sides.

The line ratio is the geometric mean of per-question median ratios. The interval resamples the 16 questions 5000 times. The pass-rate interval does the same for the difference in pass rate.

Arms alternated inside each repeat. Run 2 of the planned three repeats was not started. One other finished rerun is not in this sample. These totals use the original round and run 1.

Records for this round are the JSON files next to this report. Round 1 files were not changed.
