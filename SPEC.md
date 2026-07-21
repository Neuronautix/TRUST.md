# TRUST.md formal specification v0.3

**Status:** release candidate · **Date:** 2026-07-21 · **License:** Apache-2.0

This specification defines the document shape and validation contract. The
semantic rules in [MODEL.md](MODEL.md) are normative and incorporated here by
reference.

## 1. Location and discovery

The canonical repository filename is `TRUST.md`. The canonical served path is
`/trust.md`. Consumers SHOULD attempt, in order:

1. `/trust.md`
2. `/TRUST.md`
3. `/.well-known/trust.md`, which SHOULD redirect to `/trust.md`

Servers SHOULD treat the path case-insensitively and SHOULD serve
`text/markdown; charset=utf-8`.

## 2. Document format

A declaration MUST be UTF-8 Markdown whose first element is YAML front matter
delimited by `---`. Non-empty human-readable prose MUST follow the closing
delimiter.

`trust_md_version` MUST be a quoted string. A validator MUST dispatch to the
schema for that exact version. Supported versions are `"0.1"`, `"0.2"`, and
`"0.3"`; any other value is an unsupported-version error.

## 3. Required common fields

| Field | Contract |
|---|---|
| `trust_md_version` | Exact supported version string |
| `title` | Non-empty human-readable title |
| `description` | Non-empty scope description |
| `canonical` | Absolute HTTP(S) URL, conventionally ending `/trust.md` |
| `license` | Non-empty license identifier for the declaration |
| `companions` | Mapping of root-relative paths or `null` |
| `produced_by.humans` | At least one named human with a role |
| `produced_by.agents` | Sequence, empty when no agents contributed |
| `governance` | Source of truth, citation, review, correction, and conflict policies |
| `epistemic_model` | Categories and the declared version's support model |
| `last_reviewed` | ISO `YYYY-MM-DD` date |

Each agent MUST provide `name`, `role`, and `oversight`, where oversight is
`human-reviewed`, `human-in-the-loop`, `automated`, or `none`. ORCID values,
when present, MUST match the canonical 16-character format.

Unknown fields MUST NOT cause conformance failure. Validators MUST ignore them
and emit a notice; private extensions SHOULD begin `x_`.

## 4. v0.3 epistemic model

`epistemic_model` MUST contain one or more `categories` and exactly five
`support_bands`, in ascending support order:

`speculative`, `tentative`, `moderate`, `high`, `very-high`.

Each category has `id`, `label`, and `definition`. Each band has `id`, `label`,
and `meaning`. Meanings MUST concern evidence support only and MUST NOT infer
support from statement type.

### 4.1 Optional numeric refinement

`confidence_scale` is optional. When present it MUST declare:

```yaml
type: "integer"
range: [0, 100]
independent_of_category: true
not_probability: true
```

Every support band then MUST have a contiguous inclusive `range`; together the
ranges MUST cover 0 through 100 exactly. A single-point range such as
`100-100` is valid. The integer is an ordinal refinement, not a probability.

### 4.2 Dimensions

`dimensions` is optional. Its standard fields and values are:

- `evidence_support`: `none | contested | partial | indirect | direct`
- `review_status`: `unreviewed | agent-reviewed | human-reviewed | adjudicated`
- `calibration`: `understated | matched | overstated`
- `source_integrity`: `unverified | partially-verified | verified`

Each dimension also permits `not-assessed` and `not-applicable`. An absent
dimension is distinct from both. `null` is invalid.

## 5. Assessment provenance

`assessment` is optional. When present it MUST include:

- `unit`: `repository | artifact | claim | claim-evidence`
- `review_status`
- `assessed_by.humans` and `assessed_by.agents`
- non-empty `protocol`
- ISO `date`

Any reviewed status requires an identifiable assessor, protocol, and date.
`human-reviewed` requires a human assessor. `adjudicated` additionally requires
`disagreement` and `resolution`. `independent_review: true` requires a named
human reviewer not listed in `produced_by.humans`.

For `unit: claim-evidence`, `companions.claim_records` MUST point to an external
record. The pointer does not import external scoring semantics into TRUST.md.

## 6. Summaries and artifacts

`corpus`, `artifacts`, and `limitations` are optional. No aggregate is
mandatory.

`band_distribution` contains non-negative counts by canonical band.
`median_band`, when present, MUST agree with the distribution. For an even
population whose central observations differ, the lower-support band wins.

`average_trust` is deprecated but valid. Validators emit a notice. Numeric
averages MUST NOT be described as probabilities or as validated cardinal
measurements.

Artifact entries MUST have a root-relative `path` and MAY report claim counts,
band summaries, and dimensions. Claim records MAY be summarized in an `x_`
extension or owned by a documented inline encoding.

## 7. Validation behavior

Conforming validators MUST:

1. reject invalid UTF-8, missing front matter, invalid YAML, or missing prose;
2. require a quoted supported version and dispatch to its frozen schema;
3. enforce JSON Schema draft 2020-12 including URI/date formats;
4. enforce v0.3 band ordering, optional numeric coverage, median, assessment,
   independence, adjudication, and external-relation rules;
5. distinguish errors, warnings, and notices;
6. never rewrite or migrate a declaration silently.

The reference validator exits 0 when there are no errors, 1 when errors exist,
and 2 for usage or missing dependencies.

## 8. Conformance levels

- **Conformant:** all MUST rules for the declared version pass.
- **Recommended:** Conformant, with no warnings, plus human-confirmed adherence
  to non-machine-checkable principles.
- **Extended:** Recommended, with dimensions or claim summaries, `assessment`
  provenance, and documented inline encoding.

See [CONFORMANCE.md](CONFORMANCE.md) for the machine/human review boundary.

## 9. Compatibility

Schemas under `schema/v0.1/` and `schema/v0.2/` are frozen. Version 0.3 is
additive; it does not reinterpret declarations that still declare an earlier
version. Deprecations and unknown fields are notices, not errors. Breaking
removal of legacy fields is deferred to a future v1.0. The distributed schema
identifiers are pinned to the immutable `v0.3.0-rc.1` release bundle; the URLs
become resolvable when that tag is published from verified merged `main`.
