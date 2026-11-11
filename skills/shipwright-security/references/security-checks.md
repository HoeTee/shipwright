<!--
Adapted from improve `references/audit-playbook.md` section 2 (MIT).
Copyright (c) 2026 shadcn
https://github.com/shadcn/improve
Kept as defensive maintenance. No demonstration strings were added.
-->

# Security checks

Review only what is directly supported by code evidence. Keep findings framed as defensive maintenance: identify the code pattern, explain the production impact, and describe the remediation. Keep plans at the level of code changes, configuration changes, and tests. Do not include runnable demonstration strings or step-by-step misuse details.

Describe the safer API or the validation boundary. Do not provide a runnable example of the unsafe pattern.

**Handling rule:** never copy a secret value into a finding, plan, screenshot, or reply. Those files get committed or uploaded. Reference the `file:line` and credential type only ("Stripe live key at `config.ts:12`"), and the fix sketch always includes rotation, not just removal (a committed secret is burned even after deletion). Mask secrets and personal data before any screenshot is taken or uploaded.

**By-design is not a finding:** standard platform conventions are intentional behavior. Honoring `https_proxy` / `NO_PROXY`, reading `~/.netrc`, an explicitly local dev tool shelling out to configured package managers. A tradeoff explicitly recorded in an ADR or decision doc is likewise settled, not a finding. Flag these only when the implementation adds risk beyond the convention or the documented decision itself. A stale ADR is itself a finding: if the code has drifted from what the decision doc says, report the decision drift (the doc or the code is wrong; either way the team should know). Do not use the doc to suppress that drift.

- Credential hygiene: hardcoded keys, tokens, or passwords, credentials in committed `.env` files, credentials logged or persisted in event or history stores. Findings should name only the credential type and location, then recommend removal, rotation, and a safer configuration path.
- Data crossing into interpreters or privileged APIs: SQL or shell operations assembled from request data, HTML sinks fed by user-controlled content, dynamic execution APIs used with runtime input, or filesystem paths derived from request data. Describe the safer API or validation boundary. Parameterized queries, argument arrays, structured APIs, and an allowlist at the boundary are the usual safer shapes. Do not provide runnable examples.
- Access control: endpoints or server actions that lack server-side identity checks, authorization enforced only in the client, object access by ID without ownership or tenant checks, or missing request-authenticity checks on state-changing routes.
- Input contracts: API boundaries that trust request bodies without schema validation, file upload handling without clear type, size, and storage constraints, or broad object assignment from request data into persistence models.
- Dependency posture: run the ecosystem's audit command (`npm audit`, `pip-audit`, `cargo audit`) in read-only mode. Report only critical or high advisories that affect reachable runtime code or build and distribution paths. Avoid low-signal audit noise. `scripts/filter_advisories.py` keeps critical and high rows from the tool's JSON and drops lower severities.
- Production configuration: overly broad CORS where credentials are allowed, missing response-hardening headers (for example CSP) where sensitive browser surfaces exist, cookies missing appropriate `HttpOnly` / `Secure` / `SameSite` attributes, or debug or verbose behavior enabled in production configuration.
- Data minimization: personal data or sensitive operational data in logs, stack traces returned to clients, or internal error details exposed through API responses.

Validation sits at the boundary (principle `boundary-discipline`). Inside the system, trust the typed values. A `shortcut:` comment does not exempt a security check, a data-integrity check, or a project requirement.
