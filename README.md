# TRUST.md

**Traceable · Reviewed · Uncertainty-graded · Sourced · Transparent**

TRUST.md is a lightweight human- and machine-readable epistemic manifest for
knowledge repositories and websites.

**Status: v0.3.0 release candidate — proposed convention**

Version 0.3 makes five ordinal evidence-support bands primary, keeps 0–100 only
as an optional non-probabilistic refinement, separates four assessment
dimensions, and records who assessed what under which protocol.

## Minimal example

```yaml
---
trust_md_version: "0.3"
title: "My Project — Trust Declaration"
description: "How this repository's knowledge is produced and assessed."
canonical: "https://example.org/trust.md"
license: "CC-BY-4.0"
companions:
  fair: null
produced_by:
  humans:
    - {name: "Jane Smith", role: "author"}
  agents: []
governance:
  source_of_truth: "The human-approved repository record."
  no_fabricated_citations: true
  review_policy: "A named human reviews the declaration."
  correction_policy: "Corrections are recorded in version control."
  conflict_of_interest: "None declared."
epistemic_model:
  categories:
    - {id: "cited", label: "Cited fact", definition: "Directly supported by a cited source."}
  support_bands:
    - {id: "speculative", label: "Speculative", meaning: "Little or no direct support."}
    - {id: "tentative", label: "Tentative", meaning: "Limited support."}
    - {id: "moderate", label: "Moderate", meaning: "Partial or indirect support."}
    - {id: "high", label: "High", meaning: "Supported with minor interpretation."}
    - {id: "very-high", label: "Very high", meaning: "Direct and verifiable support."}
last_reviewed: "2026-07-21"
---

# My Project trust declaration

This prose explains the declaration to human readers.
```

No number, aggregate, claim graph, or independent review is required. Honest
repository-level adoption is conformant.

## The model

The statement category and assessment dimensions answer different questions:

| Field | Question |
|---|---|
| Category | What kind of statement is this? |
| Evidence support | How directly and strongly does evidence support it? |
| Review status | What review process actually occurred? |
| Calibration | Does the wording match the available evidence? |
| Source integrity | Do the citations exist, read accurately, and support the statement? |

Dimensions are never summed. Traceability is provenance, not a score. A low
result is not missing data, and agent agreement is not human validation.

See [MODEL.md](MODEL.md) for the normative semantics and [SPEC.md](SPEC.md) for
the file and validation contract.

## Adopt TRUST.md

1. Copy [TRUST.md](TRUST.md) to the root of your repository.
2. Fill in authorship and governance honestly.
3. Choose repository, artifact, claim, or externally stored claim–evidence
   assessment units.
4. Add dimensions and review provenance only when the facts are known.
5. Validate with `python tools/validate.py TRUST.md`.
6. Commit the canonical repository filename as `TRUST.md` and serve it at
   `/trust.md`.
7. Pair it with [FAIR.md](https://github.com/Neuronautix/FAIR.md) when useful.

Existing v0.1 and v0.2 files remain valid. Follow [MIGRATION.md](MIGRATION.md)
only when you are ready to declare v0.3 semantics.

## Schemas, validation, and examples

- Latest schema: [schema/trust.schema.json](schema/trust.schema.json)
- Frozen schemas: `schema/v0.1/`, `schema/v0.2/`, and `schema/v0.3/`
- Validator: `python tools/validate.py [path]`
- Conformance matrix: [CONFORMANCE.md](CONFORMANCE.md)
- Examples: [examples/](examples/)

The validator returns errors for violated MUST rules, warnings for recommended
quality checks, and notices for deprecations or ignored unknown fields.

## Scope

TRUST.md is an epistemic front door, not a replacement for W3C PROV,
nanopublications, SEPIO, ECO, evidence-management systems, or scientific peer
review. It is distinct from JournalList `trust.txt`, which describes trusted
organizational relationships.

## License

Apache-2.0. Copyright 2026 Damien Huzard / Neuronautix.
