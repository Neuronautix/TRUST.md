# trust.md — Formal Specification v0.2

**Status:** Proposed convention — v0.2
**Date:** 2026-06-08
**Author:** Damien Huzard, PhD (ORCID [0000-0003-4820-7951](https://orcid.org/0000-0003-4820-7951)), Neuronautix
**License:** Apache-2.0
**Reference implementation:** <https://neuronautix.com/trust.md>

---

## 1. Abstract

`trust.md` is a lightweight, human- and machine-readable epistemic trust
manifest placed at the root of a repository or website. It declares the
provenance of authorship (human/AI contributions and oversight), a grading
model for epistemic categories and confidence levels, and an honest aggregate
profile of the corpus's trust characteristics. It is a front door, not a
replacement, for formal assertion/provenance standards such as W3C PROV,
nanopublications, SEPIO, and ECO.

`trust.md` is the epistemic provenance companion to
[`fair.md`](https://github.com/Neuronautix/FAIR.md): fair.md asks *"can I find
and reuse this?"*; trust.md asks *"how much should I trust it, and why?"*.

---

## 2. Scope and motivation

`trust.md` is specifically designed for repositories that publish *knowledge*,
*analysis*, or *AI-assisted content* — anywhere the distinction between a
*cited fact*, a *reasoned inference*, an *author's position*, and a
*speculative hypothesis* matters to the reader.

### 2.1 Relationship to JournalList trust.txt

JournalList's `trust.txt` declares an organisation's trusted *relationships*
(memberships, ownership, financial links between publishers). `trust.md` is
explicitly distinct: it declares the *epistemic status of content* — what kind
of claims a repository makes and how well-supported they are. The name
similarity is intentional (same ergonomic convention — a well-known root file),
the scope is orthogonal.

### 2.2 Standards alignment

`trust.md` is a lightweight front door to the formal assertion/provenance stack:

| Standard | Alignment |
|---|---|
| **W3C PROV / PAV** | `produced_by` maps to PROV-O agents; `governance.source_of_truth` maps to pav:authoredBy / prov:wasAttributedTo |
| **Nanopublications** | trust.md's per-claim model (assertion + provenance + publication info) is a pragmatic, web-native cousin |
| **SEPIO** (Monarch Initiative) | Epistemic categories align with SEPIO's evidence typing; `produced_by.agents` aligns with SEPIO's agent model |
| **Evidence & Conclusion Ontology (ECO)** | Category IDs are designed to map to ECO terms |
| **schema.org ClaimReview** | Inline claim encoding is designed to support JSON-LD ClaimReview emission (planned) |
| **JournalList trust.txt** | Naming convention only; scope is orthogonal |

---

## 3. File location and discovery

### 3.1 Primary location

A conforming `trust.md` file MUST be placed at the root of the repository or
website and served at:

```
https://<domain>/trust.md
```

### 3.2 Optional well-known redirect

A server MAY additionally respond to:

```
https://<domain>/.well-known/trust.md
```

with a redirect (HTTP 301 or 302) to `https://<domain>/trust.md`.

### 3.3 Content-Type

When served over HTTP, the file SHOULD be served with Content-Type
`text/markdown; charset=utf-8`.

---

## 4. File format

A `trust.md` file is a **Markdown document with a YAML front-matter block**.

### 4.1 Structure

```
---
<YAML front matter>
---

<Markdown prose>
```

- The YAML front matter MUST be the first element of the file, enclosed by `---`
  delimiters.
- The prose section is REQUIRED and MUST provide a human-readable narrative
  expanding on the machine-readable front matter.
- Both sections MUST be present in a conforming file.

### 4.2 Encoding

The file MUST be encoded in UTF-8. Line endings SHOULD be LF (`\n`).

---

## 5. YAML front-matter specification

### 5.1 Required fields

#### `trust_md_version`

- **Type:** string
- **Required:** yes
- **Allowed values:** `"0.1"`
- **Description:** The version of the trust.md specification this file conforms to.

```yaml
trust_md_version: "0.1"
```

#### `title`

- **Type:** string
- **Required:** yes
- **Description:** A short, human-readable name for this trust declaration,
  typically `"<Project Name> — Trust & Epistemic Provenance Declaration"`.

```yaml
title: "My Project — Trust & Epistemic Provenance Declaration"
```

#### `description`

- **Type:** string
- **Required:** yes
- **Description:** A brief description of what this trust declaration covers.

```yaml
description: >
  How knowledge and inferences in this repository are produced, graded,
  and reviewed — and how confident the reader should be in them.
```

#### `canonical`

- **Type:** URI string
- **Required:** yes
- **Description:** The stable URL where this `trust.md` file is served.

```yaml
canonical: "https://myproject.example.org/trust.md"
```

#### `license`

- **Type:** string
- **Required:** yes
- **Description:** SPDX license identifier for this trust declaration document
  itself (not necessarily the same as the repository's content license).

```yaml
license: "Apache-2.0"
```

#### `companions`

- **Type:** mapping
- **Required:** yes
- **Description:** Paths to companion artifacts. At minimum, the `fair` key
  SHOULD be present. The `companions` object is REQUIRED; the `fair` value SHOULD be set but MAY be `null` if no `fair.md` exists yet.
- **Sub-fields:**

| Sub-field | Type | Required | Description |
|---|---|---|---|
| `fair` | string or null | recommended | Path to `fair.md` |
| `inline_markup_spec` | string or null | optional | Path to documentation describing the inline claim markup encoding |

Additional companion keys are permitted. Values MUST be root-relative path
strings (beginning with `/`) or `null`.

```yaml
companions:
  fair: "/fair.md"
  inline_markup_spec: "/notes/EPISTEMIC-MARKUP.md"
```

#### `produced_by`

- **Type:** mapping
- **Required:** yes
- **Description:** Declares the human and AI contributors to the knowledge in
  this repository. Maps to W3C PROV-O agents.
- **Sub-fields:**

| Sub-field | Type | Required | Description |
|---|---|---|---|
| `humans` | sequence | yes | At least one human contributor MUST be listed |
| `agents` | sequence | yes | AI/automated agents; use `[]` if none |

**Each `humans` entry:**

| Sub-field | Type | Required | Description |
|---|---|---|---|
| `name` | string | yes | Full name |
| `orcid` | string | recommended | ORCID iD in `0000-0000-0000-000X` format |
| `role` | string | yes | Role(s), e.g. `"author, domain reviewer, accountable signatory"` |
| `org` | string | recommended | Institutional affiliation |

**Each `agents` entry:**

| Sub-field | Type | Required | Description |
|---|---|---|---|
| `name` | string | yes | Name of the AI system or automated tool |
| `role` | string | yes | What the agent does (e.g. `"retrieval, drafting, summarisation"`) |
| `oversight` | string | yes | Human oversight level: `"human-reviewed"`, `"human-in-the-loop"`, `"automated"`, or `"none"` |

```yaml
produced_by:
  humans:
    - name: "Jane Smith"
      orcid: "0000-0000-0000-0001"
      role: "author, domain reviewer, accountable signatory"
      org: "University of Example"
  agents:
    - name: "Claude (Anthropic)"
      role: "retrieval, drafting, summarisation"
      oversight: "human-reviewed"
```

#### `governance`

- **Type:** mapping
- **Required:** yes
- **Description:** Declares the editorial policies that govern the reliability
  of the content.
- **Sub-fields:**

| Sub-field | Type | Required | Description |
|---|---|---|---|
| `source_of_truth` | string | yes | States what the authoritative record is (e.g. human approval vs. raw model output) |
| `no_fabricated_citations` | boolean | yes | Explicit commitment that citations are verified, not fabricated |
| `review_policy` | string | yes | Describes how claims are reviewed before publication |
| `correction_policy` | string | yes | Describes how errors are corrected after publication |
| `conflict_of_interest` | string | yes | Discloses any commercial or personal interests that may influence content |

```yaml
governance:
  source_of_truth: >
    The human-approved record — not raw model output — is the source of truth.
  no_fabricated_citations: true
  review_policy: "Every published claim is human-reviewed before publication."
  correction_policy: >
    Errors are corrected in place with a dated note in the page changelog or
    git history. Substantive corrections are announced.
  conflict_of_interest: "No commercial interest in the subject matter."
```

#### `epistemic_model`

- **Type:** mapping
- **Required:** yes
- **Description:** Defines the grading model used to mark and assess claims.
  Implements two independent axes: *category* (what kind of statement) and
  *confidence* (how well supported).

##### `epistemic_model.categories`

- **Type:** sequence of mappings
- **Required:** yes (at least one entry)
- **Description:** The epistemic category taxonomy. The reference implementation
  defines five canonical categories; implementers MAY use fewer or add custom
  ones, but the canonical five are RECOMMENDED for interoperability.

**Canonical categories (RECOMMENDED):**

| `id` | `label` | Definition |
|---|---|---|
| `cited` | Cited fact | Directly supported by a cited source |
| `consensus` | Established consensus | Widely accepted domain knowledge / standard definitions |
| `inference` | Inference | Reasoned from one or more sources; not stated verbatim |
| `hypothesis` | Hypothesis | Forward-looking or speculative claim |
| `view` | Author view | Explicit interpretation, position, or normative conclusion |

Each entry MUST have:

| Sub-field | Type | Required |
|---|---|---|
| `id` | string, no spaces | yes |
| `label` | string | yes |
| `definition` | string | yes |

```yaml
categories:
  - {id: "cited",      label: "Cited fact",           definition: "Directly supported by a cited source"}
  - {id: "consensus",  label: "Established consensus", definition: "Widely accepted domain knowledge"}
  - {id: "inference",  label: "Inference",            definition: "Reasoned from one or more sources; not stated verbatim"}
  - {id: "hypothesis", label: "Hypothesis",           definition: "Forward-looking or speculative claim"}
  - {id: "view",       label: "Author view",          definition: "Explicit interpretation or normative conclusion"}
```

##### `epistemic_model.confidence_scale`

- **Type:** mapping
- **Required:** yes
- **Description:** Defines the numerical confidence axis.
- **Sub-fields:**

| Sub-field | Type | Required | Description |
|---|---|---|---|
| `type` | string | yes | Data type of confidence values; MUST be `"integer"` |
| `range` | array of two integers | yes | `[min, max]`; MUST be `[0, 100]` |
| `independent_of_category` | boolean | yes | Whether category and confidence are independent axes; MUST be `true` |
| `bands` | sequence | yes | Human-interpretable bands dividing the 0–100 scale |

**Confidence bands** — each entry MUST have:

| Sub-field | Type | Description |
|---|---|---|
| `range` | string | e.g. `"90-100"` (inclusive) |
| `label` | string | Short label, e.g. `"Very high"` |
| `meaning` | string | Plain-language definition of what this score means |

**Canonical confidence bands (REQUIRED — do not reduce below 5 bands):**

| Range | Label | Meaning |
|---|---|---|
| 90–100 | Very high | Directly stated in a primary, peer-reviewed, or regulatory source |
| 70–89 | High | Stated in a cited source, secondary or lightly interpreted |
| 50–69 | Moderate | Reasonable inference, or consensus without a pinpoint citation |
| 30–49 | Tentative | Plausible forward-looking claim with partial support |
| 0–29 | Speculative | Normative/opinion/vision with little direct evidence |

> **Community consensus note:** The five band boundaries (90/70/50/30) are a proposed default chosen to cover the full 0–100 range in roughly equal steps. Feedback and domain-specific proposals for refining the thresholds are explicitly welcomed — open an issue with `band-consensus` label. The band labels and meanings may be adjusted by adopters for their domain; keep the count at five for interoperability.

##### `epistemic_model.encoding` (optional but recommended)

- **Type:** mapping
- **Description:** Describes how claims are marked up inline in the content.
  This enables the `corpus` and `artifacts` profiles to be derived
  programmatically.

| Sub-field | Type | Description |
|---|---|---|
| `inline` | string | The inline encoding syntax (e.g. HTML span attributes) |
| `reader_tooling` | string | Description of reader-facing tooling that renders the markup |

```yaml
encoding:
  inline: 'HTML spans: <span class="claim" data-epi="cited" data-trust="85" data-refs="[1]">'
  reader_tooling: "EpistemicLens.js — toggleable highlight overlay"
```

##### `epistemic_model.alignment` (optional)

- **Type:** sequence of strings
- **Description:** Formal standards to which the epistemic model aligns.

```yaml
alignment:
  - "W3C PROV / PAV — provenance and authoring of assertions"
  - "SEPIO (Scientific Evidence & Provenance Information Ontology)"
  - "Evidence & Conclusion Ontology (ECO)"
  - "schema.org ClaimReview"
```

#### `last_reviewed`

- **Type:** string
- **Required:** yes
- **Format:** ISO 8601 date: `YYYY-MM-DD`
- **Description:** Date when the maintainer last reviewed and confirmed the
  self-declaration is accurate.

```yaml
last_reviewed: "2026-06-06"
```

---

### 5.2 Recommended fields

These fields are RECOMMENDED — their absence SHOULD generate a validation
warning.

#### `corpus`

- **Type:** mapping
- **Recommended:** yes
- **Description:** Aggregate statistics for the marked corpus. Intended to be
  derivable automatically from inline claim markup. MUST be kept up to date
  with `last_reviewed`.
- **Sub-fields:**

| Sub-field | Type | Description |
|---|---|---|
| `notes_with_markup` | integer | Number of content items (notes, pages, articles) that contain inline claim markup |
| `total_claims` | integer | Total number of graded claims across the corpus |
| `average_trust` | integer or number | Mean confidence score across all marked claims (0–100) |
| `category_distribution` | mapping | Count of claims per category `id` |

```yaml
corpus:
  notes_with_markup: 19
  total_claims: 440
  average_trust: 74
  category_distribution: {cited: 233, view: 97, inference: 85, consensus: 13, hypothesis: 12}
```

#### `artifacts`

- **Type:** sequence of mappings
- **Recommended:** yes
- **Description:** Per-artifact trust profiles. Enables fine-grained auditing.
  Derivable automatically from inline markup. List SHOULD be ordered by
  `avg` descending (most evidence-dense first).
- **Each entry:**

| Sub-field | Type | Description |
|---|---|---|
| `path` | string | Root-relative path to the artifact |
| `claims` | integer | Total graded claims in this artifact |
| `avg` | integer or number | Mean confidence score |
| `dist` | mapping | Claim counts per category id |

```yaml
artifacts:
  - {path: "/notes/2026-05-example/", claims: 24, avg: 85, dist: {cited: 20, inference: 4}}
```

#### `limitations`

- **Type:** sequence of strings
- **Recommended:** yes
- **Description:** Honest disclosure of the known limitations of this trust
  declaration. Promotes intellectual honesty and helps readers calibrate.

```yaml
limitations:
  - "Confidence scores are author judgements, not statistical measures."
  - "Self-declared; not independently audited."
```

---

### 5.3 Optional fields

Additional YAML fields MAY be added. They MUST NOT conflict with the names
defined above. Custom fields SHOULD be namespaced (e.g. `x_myproject_field`).

---

## 6. Prose section

The Markdown prose section following the `---` closing delimiter SHOULD include:

1. A statement of what the trust declaration covers and why.
2. An explanation of how knowledge in the repository is produced (human/AI split,
   oversight model).
3. A description of the grading model in accessible language.
4. A corpus summary (headline figures from the `corpus` field, with
   interpretation — a low average may be a *feature* if the content is
   explicitly forward-looking).
5. The relationship to existing standards (Section 2.2).
6. How to adopt trust.md (for repositories that are themselves defining a
   convention).
7. A limitations section.
8. A changelog.

---

## 7. Validation rules

A `trust.md` file is considered **conformant** if:

1. The file is valid UTF-8.
2. The YAML front matter parses without errors.
3. All REQUIRED fields (Section 5.1) are present.
4. `trust_md_version` is `"0.1"` or `"0.2"` (0.x files are backward-compatible).
5. `produced_by.humans` contains at least one entry.
6. `produced_by.agents` is present (may be `[]`).
7. Each agent `oversight` value is one of: `human-reviewed`, `human-in-the-loop`,
   `automated`, `none`.
8. `governance.no_fabricated_citations` is a boolean.
9. `epistemic_model.categories` contains at least one entry with `id`, `label`,
   and `definition`.
10. `epistemic_model.confidence_scale.type` is `"integer"`.
11. `epistemic_model.confidence_scale.range` is `[0, 100]`.
12. `epistemic_model.confidence_scale.independent_of_category` is `true`.
13. `epistemic_model.confidence_scale.bands` contains at least five entries.
14. `last_reviewed` is a valid ISO 8601 date string in `YYYY-MM-DD` format.
15. The prose section is present and non-empty.

A **warning** (non-blocking) SHOULD be issued if:

- `corpus` is absent.
- `artifacts` is absent.
- `limitations` is absent or empty.
- Any `humans` entry lacks an `orcid`.
- The canonical five category IDs (`cited`, `consensus`, `inference`,
  `hypothesis`, `view`) are not all present.
- `corpus.average_trust` is outside the range 0–100.
- `epistemic_model.confidence_scale.bands` does not cover the full 0–100 range without gaps or overlaps (the schema cannot enforce contiguity; use the validator CLI).

---

## 8. Conformance

### 8.1 Levels

| Level | Requirements |
|---|---|
| **Conformant** | All validation rules in Section 7 pass |
| **Recommended** | Conformant + no warnings from Section 7 |
| **Extended** | Recommended + `artifacts` present + `epistemic_model.alignment` present + inline markup encoding documented |

### 8.2 Claiming conformance

A repository claiming trust.md conformance SHOULD include in its README or
documentation a statement such as:

> This repository provides a `trust.md` epistemic trust manifest conforming to
> the trust.md specification v0.2. See [trust.md](https://yourdomain/trust.md).

---

## 9. Relationship to existing standards

| Standard | Relationship |
|---|---|
| **W3C PROV / PAV** | `produced_by` is a lightweight rendering of PROV-O Agent/Activity patterns |
| **Nanopublications** | trust.md's per-claim two-axis model (category + confidence) mirrors the assertion/provenance/pubinfo nanopublication structure at corpus level |
| **SEPIO** | Epistemic category IDs align with SEPIO evidence types; can be extended with SEPIO term URIs |
| **ECO (Evidence & Conclusion Ontology)** | Category IDs (`cited`, `inference`, etc.) are designed to map to ECO codes |
| **schema.org ClaimReview** | Inline encoding (`data-epi`, `data-trust`) supports future emission as ClaimReview JSON-LD |
| **JournalList trust.txt** | Naming convention only; declares organisational trust relationships (orthogonal scope) |
| **fair.md** | Companion convention; trust.md's `companions.fair` links to it; fair.md's `companions.trust` links back |

---

## 10. Changelog

- **v0.2 (2026-06-08)** — additive improvements; backward-compatible with v0.1:
  - JSON Schema: enforce `confidence_scale.range` as exactly `[0, 100]` via
    `prefixItems`; tighten `companions` `additionalProperties` to root-relative
    paths; add `format: date` hint to `last_reviewed`; version `$id` to `v0.2`.
  - Added `tools/validate.py` — standalone Python validator implementing all 15
    MUST rules and 7 WARNING checks including confidence-band contiguity.
  - Added `.github/workflows/validate.yml` — CI that runs the validator against
    all `examples/` on every push and pull request.
  - Spec clarifications: `companions.fair` MUST/SHOULD language; community
    consensus note on confidence-band thresholds; contiguity warning in §7.
  - Fixed all internal URLs from `Neuronautix/trust-md` to `Neuronautix/TRUST.md`.
- **v0.1 (2026-06-06)** — initial specification, derived from the reference
  implementation at <https://neuronautix.com/trust.md>.
