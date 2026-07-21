# TRUST.md

**Traceable · Reviewed · Uncertainty-graded · Sourced · Transparent**

TRUST.md is an experimental human- and machine-readable convention for linking
exact evidence records to contextual, attributable, and versioned assessments.

**Current release:**
[`v0.4.0-rc.1`](https://github.com/Neuronautix/TRUST.md/releases/tag/v0.4.0-rc.1)
— release candidate

## Why TRUST.md?

Evidence does not possess one universal level of trust. The same record may be
assessed differently for different purposes, under different protocols, or by
different communities.

TRUST.md makes those differences explicit. It separates the evidence object
from assessments about that object, preserves who assessed what and how, and
allows conflicting assessments to remain visible without averaging or choosing
between them.

Conformance is not certification. A valid TRUST.md file does not establish
that evidence is true, methodologically sound, independent, reproducible, or
fit for an undeclared use.

## What v0.4 records

| Layer | What it identifies | Key rule |
|---|---|---|
| Evidence subject | The exact repository, artifact, claim, relation, or evidence record | It has an explicit version or immutable snapshot and digest |
| Assessment | A protocol-based interpretation by attributable humans or agents | It is independently identified, versioned, contextual, and append-only |
| Impact | Citations, downloads, or reuse | Impact must never determine quality or fitness |

One subject can have:

- **zero assessments**, making no quality claim;
- **one assessment**, describing one declared protocol and context; or
- **multiple assessments**, including independent or conflicting conclusions.

## Choose how far to adopt it

### 1. Identify evidence without assessing it

Register the exact subject and leave `assessments` empty. This is a valid and
honest starting point.

```yaml
subjects:
  - id: "subject-001"
    type: "evidence-record"
    identifier: "https://example.org/evidence/record-001"
    version: "1.0"
assessments: []
```

### 2. Publish one contextual assessment

Add an immutable assessment version identifying its subject, protocol,
assessors, basis, time, review and independence declarations, lifecycle state,
and limitations. A fitness conclusion also requires an explicit purpose.

See the [single-assessment example](examples/v04-single-assessment.trust.md).

### 3. Publish plural or conflicting assessments

Keep each assessment separate. TRUST.md does not select a canonical assessment,
calculate a universal trust score, or reconcile disagreement automatically.

See the
[multiple-assessment example](examples/v04-multiple-assessments.trust.md).

## Quick start

1. Copy the safe [v0.4 template](TRUST.md) to your repository root.
2. Replace every placeholder and identify at least one exact subject.
3. Add assessments only when their provenance and basis actually exist.
4. Install the validator dependencies:

   ```sh
   python -m pip install pyyaml jsonschema
   ```

5. Validate the declaration:

   ```sh
   python tools/validate.py TRUST.md
   ```

6. Commit it as `TRUST.md` and, when applicable, serve it at `/trust.md`.

<details>
<summary><strong>Complete minimal valid v0.4 declaration</strong></summary>

```yaml
---
trust_md_version: "0.4"
title: "My Project — Trust Declaration"
description: "The evidence subjects and contextual assessments published here."
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

</details>

## Semantic safeguards

- Review status is provenance, not a quality dimension.
- Dimensions are not summed, weighted, or collapsed into a universal score.
- Purpose is optional for descriptive assessments and mandatory for a
  fitness-for-purpose conclusion.
- Agent agreement is not human review.
- Independence is declared by the publisher, not proven by validation.
- Assessment corrections and lifecycle events create new immutable versions.
- Withdrawal or retraction of an assessment does not withdraw or retract its
  evidence subject.
- Citation, download, reuse, prestige, and popularity metrics cannot determine
  assessment dimensions or fitness.

## Examples

| Example | Demonstrates |
|---|---|
| [No assessment](examples/v04-no-assessment.trust.md) | An exact subject without an implied quality judgement |
| [Single assessment](examples/v04-single-assessment.trust.md) | A purpose-bound assessment with impact kept separate |
| [Multiple assessments](examples/v04-multiple-assessments.trust.md) | Independent, conflicting, human-assisted, and agent-only assessments |
| [Missing states](examples/v04-missing-states.trust.md) | Absent, not-assessed, not-applicable, and assessed-low values |
| [Lifecycle](examples/v04-lifecycle.trust.md) | Supersession, withdrawal, and retraction without changing the subject |
| [v0.3 → v0.4 migration](examples/migration/v04-after-v03.trust.md) | Explicit migration without invented conclusions |

See the complete [examples index](examples/README.md).

## Specification and tooling

- [Normative model](MODEL.md)
- [Formal specification](SPEC.md)
- [Migration guide](MIGRATION.md)
- [Conformance boundary](CONFORMANCE.md)
- [Validator guide](VALIDATION.md)
- [Latest JSON Schema](schema/trust.schema.json)
- [Citation metadata](CITATION.cff)

The validator reports errors for violated requirements, warnings for
recommended checks, and notices for deprecations or ignored unknown fields. It
never rewrites or migrates a declaration.

## Compatibility

Declarations using v0.1, v0.2, or v0.3 remain valid under their frozen schemas
and semantics. Exact quoted-version dispatch prevents them from being
reinterpreted as v0.4. Migration is always explicit and user-directed.

## Scope

TRUST.md is a publishing convention, not an authority or certification
program. It complements rather than replaces W3C PROV, nanopublications, SEPIO,
ECO, domain-specific evidence systems, and scientific peer review. It is
distinct from JournalList `trust.txt`, which describes trusted organizational
relationships.

## License and citation

Apache-2.0. Copyright 2026 Damien Huzard / Neuronautix. If you use TRUST.md,
please cite the exact release described in [CITATION.cff](CITATION.cff).
