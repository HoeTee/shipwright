# Evidence

shipwright-test owns this file. Other skills link here and do not restate it.

The report and the progress page are HTML. Do not screenshot them. The product you changed (a page, a desktop window, a command's output) is run on the real surface, and that run leaves evidence. Raw files live in a temp directory until the task ends. Key screenshots and videos are uploaded as pull-request attachments. The links go in the plan's evidence appendix. Evidence never enters git history.

## Prove it on the real thing

Verify every output by checking the real thing. Do not infer from a proxy, a self-report, or "it compiles."

Unverified work has unknown correctness. Indirect checks (file mtimes, output freshness, a worker's summary, a cached screenshot) feel cheaper than looking. Acting on a wrong inference costs more than the check.

- Check that a process is alive by looking at the process, not at a derived flag.
- Read the actual value, not a cached or derived copy.
- When a check fails, suspect the observation method before you suspect the system.
- The strongest proof is a script that repeats the same comparison. Write it, run it, and keep the output where a reviewer can run it again.
- Keep the artifact where the human can see it. A decision trail for a large port is shipwright-trail. Screenshots and videos are not committed.

You skipped this when the only support is a proxy, when the screenshot is from another commit, or when a worker's summary is the whole proof.

## Where raw files live

```text
/tmp/shipwright-<plan>/
└─ <commit7>/
   ├─ index.md
   ├─ before-<slug>.png
   ├─ after-<slug>.png
   ├─ after-<slug>.aria.txt
   ├─ variant-a-<slug>.png
   ├─ baseline-<slug>.png
   ├─ diff-<slug>.png
   ├─ lane01-<slug>.png
   ├─ cli-<slug>.txt
   ├─ api-<slug>.json
   ├─ review.mp4
   └─ worker-<n>/
```

`<plan>` is the plan number. `<commit7>` is the first 7 characters of the commit under test. A new head gets a new directory, because a conclusion is valid for one commit. The directory is not in the repository.

`<slug>` is lowercase English words separated by hyphens. Kind is one of `before`, `after`, `variant-a`, `baseline`, `diff`, `lane01` through `lane10`, `review`.

`index.md` has one line per file: the file, what it proves, the command or the action, and the time in UTC+8.

Pair a screenshot with a same-name `.aria.txt` snapshot. A terminal transcript is `.txt`. A response body, a log, or a database state is `.json`.

A worker writes under `worker-<n>/` and reports that path plus the SHA. The parent opens the files before using them.

## Delivery

shipwright-ship uploads the key screenshots and videos to the pull-request description or a comment, after secrets and personal data are covered. An attachment is hard to delete later. A secret value never enters the evidence and never enters the pull request.

shipwright-recap embeds the same frames in the HTML result, so the page still shows them after the temp directory is deleted. Embed the bytes. Do not depend on the temp path remaining.

The plan's evidence appendix records the branch, the SHA, and each attachment link. It is a section of the plan, not a directory. With no pull request, copy the key frames to `.shipwright/evidence/<plan>/<commit7>/`, gitignore that directory, and write the local path in the appendix.

GitHub stores attachments at `github.com/user-attachments/…`. They are not in the repository and not in git history. They remain after merge. A private repository's attachments follow the repository's permissions. Gitee and plain Git use that platform's attachment feature. When it has none, use the gitignored directory above.

A cloud session's `/tmp` disappears with the session. Upload and embed before that.

## When it is required

1. A change the user can see or read: a bug fix has a before and an after, on the same screen, at the same step. A feature and a refactor have a real run.
2. A visual prototype: one frame per option.
3. A visual-parity move: a baseline frame first, then an image diff. A non-zero diff fails. Do not edit the baseline to pass.
4. A `verify-<app>` proof: the action and the result, plus an ARIA snapshot, and the frame shows which application it is. A side effect (a file, a row) is a separate text artifact.
5. A pull request that changes an interaction, before human review: the key frames plus a 30 to 60 second video. Stop at mergeable.
6. A pull-request description: attach a frame or a video when it proves a claim.
7. A multi-PR lane, off unless that plan is enabled: `laneNN-<slug>.png` per lane.

## When it is not

- An HTML report, progress page, or explainer this plugin generated. Check the renderer's exit code, the body, the embedded evidence, and the version. Do not screenshot the page.
- A library or backend change with no surface. Use the command output, the response body, the log, the exit code, or the database state. Store `.txt` or `.json`, and put the summary on the pull request.
- A docs or wording change. No live run.
- A frame that would contain a secret or personal data. Cover it first, or use text evidence.

## What counts

- Shot on this commit, this run. A cached frame or a frame from an older head does not count. A new head needs new evidence, unless the patch-id rule says the patch is the same.
- "Cannot tell" or "this is the wrong screen" is not a pass. Say so.
- Prefer a script over an eyeball: an image diff, or a diff of old and new output.
- A worker report with no evidence path or no SHA is sent back once. A second miss is a gap, not a pass.
- The reviewer opens the frame and the artifact. The implementer's summary is not enough.

## Retention

Keep `/tmp/shipwright-<plan>/` until the task ends: the pull request merges, or the task is closed. Do not delete it in the middle. Re-review and human review still need it.

shipwright-cleanup deletes the whole temp directory after the task ends. It does not delete pull-request attachments or `.shipwright/evidence/`. Before the task ends, cleanup removes instances and scratch only. Plans are never deleted.

## Capture

```python
import base64
from pathlib import Path

def save_evidence(page, plan: str, sha: str, kind: str, slug: str) -> Path:
    """kind: before / after / variant-a / baseline / diff / lane03 …"""
    folder = Path("/tmp") / f"shipwright-{plan}" / sha[:7]
    folder.mkdir(parents=True, exist_ok=True)
    png = folder / f"{kind}-{slug}.png"
    page.screenshot(path=png, full_page=True)
    (folder / f"{kind}-{slug}.aria.txt").write_text(page.locator("body").aria_snapshot())
    return png

def embed_for_report(png: Path) -> str:
    """Inline the frame so the HTML page survives deletion of the temp directory."""
    data = base64.b64encode(png.read_bytes()).decode()
    return f'<img alt="{png.stem}" src="data:image/png;base64,{data}">'
```
