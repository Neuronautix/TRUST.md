# TRUST.md v0.3 normative model

This document defines the semantic contract implemented by the v0.3 schema,
validator, examples, and specification. The decision record in `DECISIONS.md`
explains why these choices were made.

The key words **MUST**, **MUST NOT**, **SHOULD**, and **MAY** are normative.

## Assessment units

An assessment declares exactly one `unit`:

- `repository` — the declaration as a whole; this is the default.
- `artifact` — one document or other repository artifact.
- `claim` — one identified claim. The manifest MAY summarize these records,
  while the inline encoding owns the individual records.
- `claim-evidence` — one claim–evidence relation. These records MUST remain in
  an external companion referenced by `companions.claim_records`; TRUST.md does
  not define citation-level scoring.

A claim assessment attaches to the claim and MUST NOT be copied automatically
to its citations or claim–evidence relations. Repository-only adoption remains
fully conformant.

## Ordinal evidence-support bands

The five bands are the primary assessment semantics, ordered from least to
most support:

1. `speculative` — little or no direct evidentiary support.
2. `tentative` — limited support with substantial interpretive distance.
3. `moderate` — partial or indirect support from cited evidence.
4. `high` — cited evidence supports the claim with minor interpretation.
5. `very-high` — direct, verifiable support in primary evidence.

An optional integer from 0 through 100 MAY refine a judgement inside its band.
It is an ordinal author or assessor judgement, **not a probability**, a
percentage chance of truth, or a cardinal measurement. Categories and support
bands are independent.

`band_distribution` is the preferred corpus summary. `median_band` MAY be
reported; when an even population has different central bands, it MUST use the
lower-support band. `average_trust` remains valid for compatibility but is
deprecated. No aggregate is required.

## Dimensions

Dimensions MUST NOT be summed or treated as compensatory scores.

| Dimension | Values, low to high where ordered | Meaning |
|---|---|---|
| `evidence_support` | `none`, `contested`, `partial`, `indirect`, `direct` | How directly and strongly evidence supports the statement |
| `review_status` | `unreviewed`, `agent-reviewed`, `human-reviewed`, `adjudicated` | Highest review process actually completed |
| `calibration` | `understated`, `matched`, `overstated` | Whether wording matches the available evidence; not a claim that the scale itself is calibrated |
| `source_integrity` | `unverified`, `partially-verified`, `verified` | Citation existence, accuracy, and support; never author, institution, or venue prestige |

Traceability is recorded in `assessment` provenance and is not scored.
Robustness and transferability require external expert appraisal and are not
core dimensions; a declaration MAY reference such a protocol or use an `x_`
extension.

## Missing data

These four states MUST remain distinct:

- An absent field means no assessment and makes no statement.
- `not-assessed` means the dimension was considered and deliberately not
  assessed.
- `not-applicable` means the dimension does not apply to the declared unit.
- The lowest ordinary value (`none`, `unreviewed`, or `unverified`) is a real
  assessment result and MUST NOT be used as a missing-value default.

`null` is not an assessment value. It remains valid only in fields that
explicitly allow it, such as companion pointers and `supersedes`.

## Review provenance

An `assessment` records `unit`, `review_status`, `assessed_by`, `protocol`, and
`date`. Any status above `unreviewed` MUST have a non-empty assessor, protocol,
and timestamp/date.

`human-reviewed` requires an identifiable human assessor. Multiple agents can
reach only `agent-reviewed`. `adjudicated` requires an identifiable human
adjudicator, a documented disagreement, and a `resolution` reference.

If `independent_review` is true, at least one named human reviewer MUST be
independent of every contributor named in `produced_by.humans`. The declaration
is responsible for the truth of that assertion; validators check only the
declarable identity condition.

## Extensibility and casing

Unknown fields MUST be ignored for conformance and reported as notices.
Private extensions SHOULD use an `x_` prefix. Extension fields MUST NOT change
the meaning of standard fields.

The canonical repository filename is `TRUST.md`. The canonical web path is
`/trust.md`; discovery order is `/trust.md`, `/TRUST.md`, then a redirect from
`/.well-known/trust.md`.

## Conformance

- **Conformant:** all MUST rules for the declared version pass.
- **Recommended:** Conformant with no warnings and all declarable obligations
  of the ten principles satisfied.
- **Extended:** Recommended, plus dimensions or claim summaries, an
  `assessment` provenance block, and a documented inline encoding.

Machine validators enforce only testable obligations. Scientific validity,
reviewer competence, and truthfulness remain human responsibilities.
