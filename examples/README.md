# TRUST.md examples

Examples demonstrate serialization and validation behavior. They are not
scientific endorsements or certified assessments.

## v0.4 examples

| File | Demonstrates |
|---|---|
| `v04-no-assessment.trust.md` | An exact evidence subject with zero assessments |
| `v04-single-assessment.trust.md` | One purpose-bound assessment and impact metadata isolated from quality |
| `v04-multiple-assessments.trust.md` | Multiple independent and conflicting assessments, multiple purposes, human-assisted and agent-only provenance |
| `v04-missing-states.trust.md` | Absent, not-assessed, not-applicable, and assessed-low states |
| `v04-lifecycle.trust.md` | Append-only supersession, withdrawal, and retraction without changing the subject |

The multiple-assessment example is deliberately neutral: it retains
disagreement without averaging, ranking, or adjudicating a canonical result.

## Migration examples

| File | Demonstrates |
|---|---|
| `migration/v03-before-v04.trust.md` | Unchanged frozen v0.3 input |
| `migration/v04-after-v03.trust.md` | Explicit one-assessment v0.4 result with supplied identity, protocol, basis, time precision, and legacy population metadata |
| `migration/v02-before.trust.md` | Historical v0.2 input |
| `migration/v03-after.trust.md` | Historical v0.2-to-v0.3 result |

The v0.3 migration input intentionally retains deprecated `average_trust` and
therefore emits its documented notice. No migration is automatic.

## Historical examples

Files beginning `v03-` demonstrate frozen v0.3 behavior. The
`neuronautix.trust.md` and `dimensions-preview.trust.md` files preserve earlier
version behavior and context. Exact version dispatch prevents newer semantics
from changing them.

Intentionally invalid v0.4 cases and valid round-trip fixtures live in
`tests/fixtures/v0.4/` so public examples remain clean.
