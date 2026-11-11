# Interaction gate

This gate is always on for a change a person can see or operate. It does not depend on the disabled multi-PR lane plan.

Before merge, and only after technical checks are green:

1. Key screenshots of the changed interaction, taken on this candidate. Mask secrets and personal data before upload.
2. A 30 to 60 second video of the same interaction.
3. Put both in the PR description or a PR comment, and in the HTML packet.
4. Record the attachment URLs in the plan's evidence appendix, with the branch and the full SHA.
5. Stop at merge-ready. Wait for the person's verdict. Silence is not approval.

A change with no interaction writes `Review gate: none` and does not invent a video.

When there is no PR, copy the key screenshots to `.shipwright/evidence/<plan>/<sha7>/`, which stays gitignored, and record those local paths in the appendix.

Raw files in `/tmp/shipwright-<plan>/<sha7>/` stay until the task ends. Cleanup removes that directory later. PR attachments and the gitignored copies stay.
