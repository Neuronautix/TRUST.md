# TRUST.md v0.4.0-rc.1

This release candidate introduces an experimental proposed convention for
publishing contextual, attributable, and independently versioned assessments
of exact evidence subjects.

Its central rule is that an evidence record and a trust assessment are
different objects. One subject may have zero, one, or many assessments.
Assessments from different communities, purposes, protocols, or assessors may
coexist and disagree. TRUST.md does not average, rank, reconcile, or select
them.

## Included in v0.4

- Required subject registry with an explicit version or immutable snapshot and
  digest.
- Stable assessment series, immutable version-specific IDs, and versions.
- Optional descriptive purpose and purpose-required fitness conclusions.
- Versioned protocol and inspectable assessment-basis links.
- Attributable human and agent provenance, review status, and declared
  independence states.
- Append-only active, superseded, withdrawn, and retracted lifecycle records.
- Explicit separation of withdrawal or retraction of an assessment from the
  lifecycle of its subject.
- Coexisting conflicting assessments without top-level aggregation.
- Explicit v0.3-to-v0.4 migration with day-to-datetime precision preservation.
- Impact metadata that is prohibited from influencing quality dimensions.
- Public examples, compatibility fixtures, and stable invalid-case diagnostics.

## Compatibility

- v0.1, v0.2, and v0.3 schemas remain frozen.
- Exact quoted-version dispatch prevents reinterpretation under v0.4.
- The v0.3 singular assessment remains a v0.3 construct.
- No validator silently rewrites or migrates a declaration.
- Deprecated and unknown fields use notices rather than silent loss.

## Review this candidate

1. Install `pyyaml`, `jsonschema`, and `pytest`.
2. Run `python -m pytest -q`.
3. Run `python tools/validate.py TRUST.md`.
4. Validate the public examples and compare MODEL.md, SPEC.md, MIGRATION.md,
   CONFORMANCE.md, the v0.4 schema, validator behavior, and examples.
5. Report semantic or interoperability concerns before a stable v0.4 release.

## Validation boundary

Conformance validates structure, required provenance, identifiers, and
declared relationships. It does not certify evidence, methodological quality,
reviewer competence, independence, reproducibility, replication, or downstream
scientific conclusions. Agent agreement is not human review. TRUST.md is not an
authority that grants trust.

The immutable `v0.4.0-rc.1` tag must be created only after this preparation PR
is merged and merged-main CI succeeds. The tag must point to that verified main
commit and must not be moved.
