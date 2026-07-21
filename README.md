# TRUST.md

**Traceable · Reviewed · Uncertainty-graded · Sourced · Transparent**

TRUST.md is a lightweight human- and machine-readable manifest for publishing
how evidence and contextual assessments were identified, produced, and
reviewed.

**Status: v0.4.0-rc.1 release candidate — experimental proposed convention**

TRUST.md v0.4 separates an evidence subject from assessments about that
subject. An evidence record can have zero, one, or many independently versioned
assessments. Different assessments may use different protocols or purposes and
may disagree; the format does not average or choose between them.

Conformance is not certification. A valid manifest does not establish that the
evidence is true, methodologically sound, independent, reproducible, or fit for
an undeclared use.

## Minimal v0.4 declaration

```yaml
---
trust_md_version: "0.4"
title: "My Project — Trust Declaration"
description: "The evidence subjects and any contextual assessments published here."
canonical: "https://example.org/trust.md"
license: "CC-BY-4.0"
companions: {fair: null}
produced_by:
  humans: [{name: "Jane Smith", role: "manifest author"}]
  agents: []
governance:
  source_of_truth: "The human-approved repository record."
  no_fabricated_citations: true
  review_policy: "Assessment review is declared per assessment."
  correction_policy: "Released assessments are corrected by new versions."
  conflict_of_interest: "None declared."
epistemic_model:
  categories:
    - {id: "cited", label: "Cited fact", definition: "Directly supported by a cited source."}
  support_bands:
    - {id: "speculative", label: "Speculative", meaning: "Little or no direct support."}
    - {id: "tentative", label: "Tentative", meaning: "Limited support."}
    - {id: "moderate", label: "Moderate", meaning: "Partial or indirect support."}
    - {id: "high", label: "High", meaning: "Support with minor interpretation."}
    - {id: "very-high", label: "Very high", meaning: "Direct and verifiable support."}
subjects:
  - id: "subject-001"
    type: "evidence-record"
    identifier: "https://example.org/evidence/record-001"
    version: "1.0"
assessments: []
last_reviewed: "2026-07-21"
---

# My Project trust declaration

This declaration identifies one evidence subject and publishes no assessment.
```

An empty or absent `assessments` collection makes no quality claim. When an
assessment is published, it identifies an immutable assessment version, its
subject, protocol, basis, assessors, review and independence declarations,
time, lifecycle state, limitations, and—when applicable—purpose-specific
fitness.

## Core model

- `subjects[]` identifies each exact evidence object by an explicit version or
  by an immutable snapshot and digest.
- `assessments[]` contains independently versioned, attributable assessments.
- `purpose` is optional for descriptive assessments and required for a
  `fitness_for_purpose` conclusion.
- Review status is provenance, not a quality dimension.
- Conflicting assessments coexist. There is no top-level aggregate across
  assessments.
- Assessment lifecycle is append-only: corrections and status changes create
  new versions in the same `series_id`.
- Citation, download, reuse, and popularity metrics are impact information and
  must not determine assessment dimensions or fitness.

See [MODEL.md](MODEL.md) for normative semantics, [SPEC.md](SPEC.md) for the
file contract, and [CONFORMANCE.md](CONFORMANCE.md) for the validation boundary.

## Adopt TRUST.md

1. Copy [TRUST.md](TRUST.md) to the repository root.
2. Replace every placeholder and identify at least one exact subject.
3. Leave `assessments` empty unless an attributable assessment actually
   exists.
4. For each assessment, identify its series, immutable version, subject,
   protocol version, assessors, date-time, review state, independence state,
   lifecycle state, basis where required, and limitations.
5. Run `python tools/validate.py TRUST.md`.
6. Commit the canonical filename as `TRUST.md` and serve it at `/trust.md`.

Existing v0.1, v0.2, and v0.3 files remain valid under their frozen schemas.
They are never reinterpreted as v0.4. Follow [MIGRATION.md](MIGRATION.md) only
when a human chooses to publish the additional v0.4 identity and provenance.

## Schemas, validation, and examples

- Latest schema: [schema/trust.schema.json](schema/trust.schema.json)
- Versioned schemas: `schema/v0.1/` through `schema/v0.4/`
- Validator guide: [VALIDATION.md](VALIDATION.md)
- Validator command: `python tools/validate.py [path]`
- Examples index: [examples/README.md](examples/README.md)
- Migration pair: `examples/migration/v03-before-v04.trust.md` and
  `examples/migration/v04-after-v03.trust.md`

The validator reports errors for violated requirements, warnings for
recommended checks, and notices for deprecations or ignored unknown fields. It
never rewrites or migrates a declaration.

## Scope

TRUST.md is an experimental publishing convention, not an authority or
certification program. It complements rather than replaces W3C PROV,
nanopublications, SEPIO, ECO, domain-specific evidence systems, or scientific
peer review. It is distinct from JournalList `trust.txt`, which describes
trusted organizational relationships.

## License and citation

Apache-2.0. Copyright 2026 Damien Huzard / Neuronautix. Citation metadata is in
[CITATION.cff](CITATION.cff).
