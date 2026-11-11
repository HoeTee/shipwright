# Evidence retention

Two cleanups get confused. Keep them apart.

## During the task

Cleanup of a verification run removes the instances and the scratch that run created. It does not remove the proof.

- Kill the process you started. Do not kill by process name.
- Remove temporary instances and scratch state.
- Proof stays where the verification skill named it. After cleanup, check that the proof is still there. A cleanup that eats the proof fails.
- On a failed attempt, run that same cleanup so a broken run does not leave processes and ports behind. The proof from the attempts you are keeping still stays.

A generated `verify-<app>` skill that was never executed is a draft, not a deliverable. The self-test runs launch, doctor, one mapped feature, capture, and cleanup, then checks the evidence is still at the named path.

## When the task ends

The task has ended when the pull request merges, or the task is closed.

Then delete the whole raw directory `/tmp/shipwright-<plan>/`, including every `<commit7>/` under it. shipwright-eval's run directories under `/tmp/shipwright-eval-<plan>/` go at the same time.

Do not delete:

- Pull-request attachments (`github.com/user-attachments/…` or the other platform's attachments).
- `.shipwright/evidence/<plan>/<commit7>/`, the key frames kept when there is no pull request.
- `plans/` and `plans/reports/`. The HTML result already embeds the frames it needs.
- `decisions.tsv`, unless the user asks. It is outside git by default and is not a temp screenshot directory.

Before the task ends, do not delete `/tmp/shipwright-<plan>/`. Re-review and human review still open those files.

A cloud session may lose `/tmp` when the session ends. That does not change the rule. The key frames have to be uploaded and embedded before the session goes away. See [evidence](../evidence.md).
