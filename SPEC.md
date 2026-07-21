# TRUST.md formal specification v0.4

**Status:** release candidate; experimental proposed convention · **Date:**
2026-07-21 · **License:** Apache-2.0

This specification defines the v0.4 document and validation contract. The
semantics in [MODEL.md](MODEL.md) are normative and incorporated by reference.

## 1. Location and document format

The canonical repository filename is `TRUST.md`; the canonical served path is
`/trust.md`. Consumers SHOULD try `/trust.md`, `/TRUST.md`, then
`/.well-known/trust.md`. Servers SHOULD use `text/markdown; charset=utf-8`.

A declaration MUST be UTF-8 Markdown beginning with YAML front matter between
`---` delimiters. Non-empty prose MUST follow. `trust_md_version` MUST be a
quoted string. Exact dispatch supports `"0.1"`, `"0.2"`, `"0.3"`, and `"0.4"`;
another value is an unsupported-version error.

## 2. Common fields

Every v0.4 declaration requires:

| Field | Contract |
|---|---|
| `trust_md_version` | Exactly `"0.4"` |
| `title`, `description` | Non-empty human-readable strings |
| `canonical` | Absolute HTTP(S) URL |
| `license` | Non-empty declaration license identifier |
| `companions` | Mapping of root-relative paths or `null` |
| `produced_by` | At least one named human; zero or more attributable agents |
| `governance` | Source-of-truth, citation, review, correction, and conflict policies |
| `epistemic_model` | Categories and five ordered support bands |
| `subjects` | Non-empty subject registry |
| `last_reviewed` | ISO `YYYY-MM-DD` date |

Agents require `name`, `role`, and `oversight`. ORCID values use the canonical
16-character form. Unknown fields do not fail conformance; validators report a
notice. Private extensions SHOULD use `x_`.

## 3. Epistemic model

`epistemic_model` contains one or more categories and exactly five ascending
support bands: `speculative`, `tentative`, `moderate`, `high`, `very-high`.
Meanings concern evidence support and do not infer support from category.

An optional confidence scale declares integer range `[0, 100]`, category
independence, and `not_probability: true`. If band ranges are present, they
cover 0–100 contiguously.

## 4. Subject registry

Each `subjects[]` item requires:

- a locally unique `id`;
- `type`: a standard type or an `x_` extension;
- an absolute HTTP(S) `identifier`;
- exactly one of a non-empty `version` or a `snapshot` containing an immutable
  URL and validated digest.

`subjects` has at least one item. `assessments` may be absent or empty, so an
evidence object with no assessment remains representable.

## 5. Assessments

Each `assessments[]` item requires:

- unique absolute `series_id` and version-specific `id` plus non-empty
  `version`;
- `subject`, resolving to exactly one local subject;
- `assessed_by.humans` and `assessed_by.agents` arrays;
- absolute protocol `identifier` and non-empty protocol `version`;
- offset ISO 8601 `assessed_at`;
- `review_status`, declared `independence`, lifecycle `status`, and
  `limitations`.

The `(series_id, version)` pair is unique. Version-specific IDs are immutable.
An optional `purpose` scopes interpretation. `fitness_for_purpose` requires
`purpose`; `conditionally-suitable` also requires non-empty `conditions`.

Standard dimensions are `evidence_support`, `calibration`, and
`source_integrity`. `review_status`, citations, downloads, reuse, popularity,
or other impact metrics are prohibited as dimensions. Missing-state values are
`not-assessed` and `not-applicable`; absence and assessed-low values remain
different states.

An optional `numeric_refinement` is an integer from 0 through 100 with
`not_probability: true`.

## 6. Basis, provenance, and review

Basis entries require a relation and absolute identifier and may specify a
version. Core relations are `informed-by`, `uses-qc-report`, `checked-against`,
and `derived-from`; extensions begin `x_`.

An active assessment above `unreviewed` requires at least one basis record.
`human-reviewed` requires a named human. `adjudicated` requires a named human,
plus disagreement and resolution URLs. `agent-reviewed` may not be presented as
human review.

Independence values are declarations, not verified booleans. The validator
checks structural provenance but cannot establish actual independence or
review quality.

## 7. Lifecycle and coexistence

Lifecycle states are `active`, `superseded`, `withdrawn`, and `retracted`.
Every non-active lifecycle version requires `supersedes` and
`lifecycle_reason`. A local supersession link resolves to the same `series_id`
and subject, points backward to an existing assessment version, and forms no
cycle. External immutable backward links may be declared but cannot be fully
verified locally.

Conflicting assessments are valid and remain separate. A top-level `corpus` or
other aggregate across assessments is prohibited. `summary` may occur only
inside one assessment and must declare `scope: assessment`.

## 8. Impact and extensions

Top-level `impact` may contain non-negative citation, download, or reuse counts
with an offset measurement time and source. Impact data and extension metrics
must not influence dimensions or fitness conclusions.

Extensions preserve domain-specific information but do not change the
normative meaning of standard fields.

## 9. Validation behavior

A conforming validator MUST:

1. reject invalid UTF-8, front matter, YAML, or missing prose;
2. require a quoted supported version and dispatch exactly;
3. enforce JSON Schema draft 2020-12 and format checks;
4. enforce subject identity, assessment identity, provenance, purpose,
   lifecycle, supersession, aggregation, and impact boundaries;
5. distinguish errors, warnings, deprecation notices, and ignored-field
   notices;
6. remain type-safe on structurally invalid input; and
7. never rewrite or migrate a declaration.

The reference CLI exits 0 with no errors, 1 with errors, and 2 for usage or
missing dependencies. See [VALIDATION.md](VALIDATION.md).

## 10. Conformance and compatibility

Passing validation establishes structural conformance only. It is not evidence
certification and does not validate scientific conclusions. The matrix in
[CONFORMANCE.md](CONFORMANCE.md) identifies machine and human obligations.

Schemas under `schema/v0.1/`, `schema/v0.2/`, and `schema/v0.3/` are frozen.
They retain their released meanings. v0.4 is dispatched only for declarations
that explicitly quote `trust_md_version: "0.4"`. Schema identifiers for v0.4
are pinned to the immutable `v0.4.0-rc.1` distribution and become resolvable
only after that tag is created from verified merged `main`.
