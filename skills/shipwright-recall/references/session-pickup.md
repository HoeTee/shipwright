# Session pickup

Source: pstack `playbooks/session-pickup.md`. Use this when one specific prior chat is the thing to resume. A sweep across recent chats is [procedure.md](procedure.md).

You own the resume point. Read the prior trail. Do not redo it.

1. Locate the prior trail. A local transcript in the active workspace's session directory (paths in [procedure.md](procedure.md)), a cloud-agent URL, or a pushed branch. Read the metadata overview and the last messages first, then scan back for the decision points. Parse a long transcript in an independent worker and keep the reduced timeline in the main thread. That is principle `guard-the-context-window` in the shared principles directory. Do not glob across every project's directory. That crosses workspace boundaries and reads private chats from unrelated projects.
2. Reconstruct operational state. The branch and worktree, what already landed (`git log`, `git diff` against the base), the open todos, the decisions made. The prior trail is authoritative input. Resist the bias to re-derive it.
3. Diff done against pending. Compare what shipped with what was planned. Name the resume point. Do not re-run the prior repro or redo completed work. A "let me verify from scratch" pass means you are treating the trail as untrustworthy when it is authoritative.
4. Route the remaining work to the matching skill and pick the verdict: continue the execution, ship a finished recommendation, ratify or override a prior conclusion, or postmortem a failed run. This playbook ends here. The routed skill owns the rest.
5. Verify the inherited claims against the original goal on the real artifact. That is principle `prove-it-works`. A passing prior self-report is not the proof. The shared evidence rules live in `references/evidence.md`, which is added separately. A new head needs new evidence unless the patch-id rule in shipwright-land says the patch is the same.

**Reply:** where the prior agent stopped, what you inherited versus redid (ideally nothing redone), the resume point, and the outcome.
