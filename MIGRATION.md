# Migrating to TRUST.md v0.3

Version 0.3 is additive. A declaration that remains on `trust_md_version:
"0.1"` or `"0.2"` continues to validate under its frozen schema and does not
need to adopt v0.3 fields.

## Minimal migration

1. Change `trust_md_version` to `"0.3"`.
2. Keep the existing categories and confidence scale. Rewrite band meanings so
   that they describe evidence support only and do not encode statement type.
3. Treat each band label as primary and any 0–100 integer as an optional,
   non-probabilistic refinement.
4. Replace aggregate emphasis on `average_trust` with `band_distribution` and,
   optionally, `median_band`. You MAY retain `average_trust`; it produces a
   deprecation notice, not an error.
5. Add `assessment` provenance when declaring a completed review.
6. Add dimensions only when you can distinguish missing, `not-assessed`,
   `not-applicable`, and assessed low-support states.

## Field mapping

| v0.1/v0.2 | v0.3 treatment |
|---|---|
| `trust_md_version: "0.1" | "0.2"` | Set to `"0.3"` only after adopting this contract |
| `epistemic_model.confidence_scale.bands[]` | Move to `epistemic_model.support_bands[]`; use canonical lowercase hyphenated IDs. Keep only the optional integer refinement metadata under `confidence_scale` |
| Inline `data-trust="85"` | Still valid; SHOULD be accompanied by the band and MUST NOT be presented as a probability |
| `corpus.average_trust` | Deprecated but valid |
| No aggregate | Valid |
| `corpus.band_distribution` | Preferred counts by canonical band |
| `corpus.median_band` | Optional; conservative lower-band tie rule |
| `x_dimensions` | Rename to `dimensions` after values match the v0.3 vocabularies |
| `x_assessment` | Rename to `assessment` after provenance is complete |
| Claim–evidence extensions | Move to an external companion and reference it with `companions.claim_records` |

## Compatibility guarantees

- The v0.1 and v0.2 schemas are frozen copies of their released behavior.
- Validation dispatches solely on the quoted string `trust_md_version`.
- Unknown versions fail with an `unsupported version` error distinct from
  ordinary validation errors.
- Unknown fields in supported versions are notices, not errors.
- Deprecations are notices, not errors.
- No validator silently rewrites or upgrades a declaration.

## Review-state migration

Do not infer review status from numeric confidence, contributor roles, or agent
agreement. Start at `unreviewed` unless the required provenance exists.

- Use `agent-reviewed` when one or more agents performed the highest completed
  review and no human performed a documented review.
- Use `human-reviewed` only with an identifiable human assessor.
- Use `adjudicated` only when a disagreement and its human resolution are both
  documented and linked.

## Release sequencing

Adopt v0.3 first in a prerelease and verify schema, CLI, examples, and prose
against the same commit. Stable `v0.3.0` is appropriate only after those
artifacts agree exactly. Existing release tags MUST NOT be moved.
