# Migrating from TRUST.md v0.3 to v0.4

Migration is explicit and user-directed. A declaration that remains on
`trust_md_version: "0.3"` continues to validate under the frozen v0.3 schema and
is never reinterpreted under v0.4 semantics.

The worked pair is:

- `examples/migration/v03-before-v04.trust.md` — unchanged v0.3 input;
- `examples/migration/v04-after-v03.trust.md` — explicit v0.4 result.

`V0.4_MIGRATION.md` preserves the accepted design record and detailed mapping.

## Migration procedure

1. Preserve the original v0.3 declaration and validate it as v0.3.
2. Identify every exact evidence subject. Supply an explicit version or an
   immutable snapshot URL and digest.
3. Create a stable assessment `series_id`, an immutable version-specific `id`,
   and a non-empty `version`.
4. Move the singular v0.3 assessment into one element of `assessments` without
   changing its meaning.
5. Supply an absolute protocol identifier and version.
6. Supply inspectable basis records for an active reviewed assessment.
7. Convert the v0.3 date to an offset datetime. If only a day was known, use
   `T00:00:00Z` and `assessed_at_precision: date`.
8. Confirm review, independence, and lifecycle declarations; do not infer
   them from scores, contributors, agents, or popularity.
9. Preserve legacy-only data as explicit migration metadata or safe `x_`
   extensions. Never silently drop it.
10. Validate the new file separately as v0.4. Do not overwrite the v0.3 input.

## Field mapping

| v0.3 | v0.4 treatment |
|---|---|
| singular `assessment` | One independently versioned item in `assessments[]` |
| `assessment.unit` | Subject `type`, reviewed and made exact by subject identity |
| implicit assessed object | Required local `subjects[]` entry |
| no immutable subject version | User supplies `version` or snapshot plus digest |
| no assessment identity | User supplies `series_id`, immutable `id`, and `version` |
| text `assessment.protocol` | User supplies protocol URL and version; retain legacy text as migration metadata |
| `assessment.assessed_by` | Retain human and agent provenance without promotion |
| `assessment.review_status` | Retain only as assessment provenance |
| `epistemic_model.dimensions.review_status` | Remove from dimensions; resolve inconsistencies manually |
| `assessment.independent_review: true` | `declared-independent`, still only a publisher declaration |
| absent or false independence | `not-declared` unless another state is explicitly declared |
| `assessment.date` | Offset `assessed_at`; day-only values use the precision marker |
| no `evidence_basis` | User supplies basis for active reviewed assessments |
| no purpose | Leave absent for descriptive assessment; supply before fitness |
| no lifecycle state | Use `active` only after publisher confirmation |
| v0.3 dimensions | Retain their values per assessment except review status |
| absent / `not-assessed` / `not-applicable` / assessed-low | Preserve exactly |
| optional numeric refinement | Preserve only as non-probabilistic assessment-scoped information |
| `corpus.average_trust` | Deprecated migration metadata; never a v0.4 aggregate |
| band distribution / median | Retain only in one assessment with population and protocol explicit |
| reuse or impact extensions | Keep as impact metadata, never quality input |

## Prohibited migration shortcuts

Migration MUST NOT:

- invent a fitness conclusion, purpose, basis, review, independence, or status;
- copy Computational Review TRUST or ORAtlas scores into TRUST.md;
- combine source-native and external assessments;
- average or reconcile multiple assessments;
- turn citations, downloads, reuse, prestige, or popularity into quality;
- mutate the referenced evidence object; or
- edit a released assessment version in place.

## Compatibility guarantees

- v0.1, v0.2, and v0.3 schemas remain frozen.
- Exact quoted-version dispatch controls semantics.
- Unknown fields and deprecations are reported as notices.
- Validators never perform automatic migration.
- A round trip through YAML preserves declared scalar and collection types.
