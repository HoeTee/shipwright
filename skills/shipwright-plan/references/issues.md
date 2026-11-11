# Publish plans as issues

Source: improve `closing-the-loop.md`, the `--issues` section only. Dispatching an executor and reconciling the backlog belong to shipwright-build, shipwright-fix, and shipwright-reconcile. The founding rule still holds for this skill: planning writes `plans/` (or `advisor-plans/`). It does not edit source code.

`--issues` is a modifier on a planning invocation. The flag is the user's authorization to create issues. Never create them without it. Publishing is an external action. It is not implied by "write a plan."

1. Preflight. `gh auth status` succeeds and the repo has a GitHub remote. If either fails, write the plan files as normal and say why issues were skipped. On Gitee or a plain git remote, use that host's issue feature if the user named it. If the host has no issues, skip and say so.
2. Visibility check. `gh repo view --json visibility`. If the repo is **public**, warn the user that issues are publicly visible and get explicit confirmation before publishing any plan that describes a security vulnerability, a credential location, or another sensitive finding.
3. Show the list of titles about to become issues. Confirm once if someone is there to confirm.
4. Per plan: `gh issue create --title "<plan title>" --body-file <plan file>`. Labels: `shipwright` plus the category. Apply a label only if it exists or can be created without erroring. Skip labels rather than fail.
5. Record each issue URL in the plan's Status block (`- **Issue**: <url>`) and in the index.

The plan file remains the source of truth. The issue is distribution. The self-containment rule pays off here. The issue body needs no edits to make sense to whoever picks it up.

Do not put secret values in the issue body. A public issue cannot be unread.
