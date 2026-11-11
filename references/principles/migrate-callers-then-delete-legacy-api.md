# Migrate Callers Then Delete Legacy APIs

When: Use when introducing a new internal API while old callers still exist—migrate callers and delete the legacy API in one wave.

- Update tests to assert the new contract, and delete tests that only protect pre-refactor implementation details

**When this applies:**
- No external users depend on backward compatibility
- The project can absorb coordinated breaking changes
- The new API is part of a simplification or refactor initiative
