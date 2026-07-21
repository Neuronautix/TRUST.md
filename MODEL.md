# TRUST.md v0.4 normative model

This document defines the semantic contract implemented by the v0.4 schema,
validator, examples, and specification. `V0.4_MODEL.md` preserves the accepted
design and decision record.

TRUST.md v0.4 is an experimental proposed convention. The key words **MUST**,
**MUST NOT**, **SHOULD**, and **MAY** are normative.

## Evidence subjects and assessments

An evidence subject and a trust assessment are distinct, independently
versioned objects. Subjects preserve identity, version, provenance, factual QC
information, and their own lifecycle outside TRUST.md. Assessments interpret
inspectable information under a declared protocol and context.

Every declaration MUST contain a non-empty `subjects` registry. Each subject
has a local `id`, a type, an absolute HTTP(S) identifier, and exactly one
identity constraint:

- a non-empty explicit `version`; or
- an immutable snapshot URL plus a SHA-256, SHA-384, or SHA-512 digest.

The registry may contain evidence with no assessment. Referencing or updating
an assessment MUST NOT mutate the subject.

## Plural assessment identity

`assessments` is optional and may be empty. Each assessment MUST identify:

- `series_id`, the stable assessment lineage;
- `id`, the immutable identifier for this released version;
- `version`, the version label;
- `subject`, a local subject-registry ID.

Assessment IDs and `(series_id, version)` pairs MUST be unique. Different
communities, purposes, protocols, or assessors MAY publish separate assessments
of the same subject. Conflicting assessments remain separate and inspectable;
storage order does not make one canonical.

## Dimensions and missing states

Standard assessment dimensions are evidence support, calibration, and source
integrity. Review status is provenance and MUST NOT appear as a dimension.
Dimensions are not summed, weighted, or converted into a universal score.

These states remain distinct:

- absent: no statement was made;
- `not-assessed`: the dimension was explicitly not assessed;
- `not-applicable`: it does not apply in the declared context;
- an ordinary low value such as `none`, `overstated`, or `unverified`: a real
  assessment result.

An optional integer `numeric_refinement` MAY refine an assessment from 0
through 100 only when `not_probability: true`. It is not a probability or
validated cardinal measurement.

## Purpose and fitness for purpose

A descriptive assessment MAY omit `purpose`. A `fitness_for_purpose`
conclusion MUST name its purpose and uses one of:

- `suitable`;
- `conditionally-suitable`;
- `not-suitable`;
- `not-assessed`;
- `not-applicable`.

`conditionally-suitable` requires explicit conditions. A conclusion for one
purpose MUST NOT imply suitability for another purpose.

## Protocol and assessment basis

Every assessment MUST identify an absolute protocol URL and a non-empty
protocol version. Domain-specific criteria belong in the linked protocol or an
`x_` extension, not in a universal TRUST.md rubric.

Basis relations use the small core vocabulary `informed-by`, `uses-qc-report`,
`checked-against`, and `derived-from`, or an `x_` relation. Every active reviewed
assessment MUST link at least one inspectable basis record. Conformance checks
the declaration, not whether the record is scientifically adequate.

## Provenance, review, and independence

Every assessment records human and automated assessors, an offset ISO 8601
`assessed_at` datetime, `review_status`, `independence`, status, and limitations.

Review status is `unreviewed`, `agent-reviewed`, `human-reviewed`, or
`adjudicated`. Agent agreement is not human review. Human-reviewed and
adjudicated states require identifiable human provenance; adjudication also
requires inspectable disagreement and resolution links.

Independence is a declared state: `not-declared`,
`declared-not-independent`, `declared-partially-independent`, or
`declared-independent`. A validator does not verify the declaration.

## Coexistence and aggregation

Assessments MAY coexist even when their conclusions conflict. TRUST.md does not
require automatic conflict detection or adjudication. Known disagreement
SHOULD be recorded in limitations or linked records.

A declaration MUST NOT publish a top-level aggregate across assessments. The
validator MUST NOT average, rank, reconcile, or select them. A summary is
permitted only inside one assessment with `scope: assessment` and the
population and protocol made explicit where needed.

## Append-only lifecycle

Released assessment versions are append-only. A correction or lifecycle event
creates a new immutable version in the same `series_id`, linking backward with
`supersedes`. The prior version remains discoverable. Supersession MUST remain
on the same subject and in the same series and MUST NOT form a cycle.

Lifecycle status is:

- `active`: the publisher's current assessment statement;
- `superseded`: a later assessment version replaces the prior one;
- `withdrawn`: removed from current use without necessarily asserting
  invalidity;
- `retracted`: explicitly repudiated by its publisher.

Superseded, withdrawn, and retracted lifecycle versions require a reason and a
backward link. Assessment lifecycle never changes the evidence subject's
lifecycle.

## Time and migration precision

Native v0.4 assessments use an offset datetime. A migrated v0.3 day is anchored
at `00:00:00Z` and declares `assessed_at_precision: date`, preserving that the
original time and timezone were unknown.

## Impact is not quality

Citations, downloads, reuse counts, prestige, and popularity MAY be published
as scoped impact metadata. They MUST NOT populate, modify, weight, or justify
quality dimensions or fitness conclusions.

## Validation boundary

Schema and CLI conformance validate structure, identifiers, required
provenance, and declared relationships. They do not:

- establish the truth of evidence;
- certify methodological quality or assessor competence;
- prove independence, reproducibility, or replication;
- validate downstream scientific conclusions;
- convert agent agreement into human review; or
- make TRUST.md an authority over evidence.

## Compatibility and extensions

Versions 0.1, 0.2, and 0.3 retain frozen schemas and semantics. Exact dispatch
uses the quoted `trust_md_version`; v0.3's singular `assessment` is not
reinterpreted as plural v0.4 `assessments`. Migration is explicit and never
automatic.

Unknown fields are ignored for conformance and reported as notices. Private
extensions SHOULD use `x_` and MUST NOT alter standard-field meaning.
