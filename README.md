# trust.md

A lightweight, human- and machine-readable **epistemic trust manifest** that you
drop at the root of any repository or website. One file tells readers — and
machines — how the knowledge in a project was produced, how each claim is graded,
and how much confidence to place in it.

**Status: v0.2 — proposed convention**

> Companion convention: [fair.md](https://github.com/Neuronautix/FAIR.md) — declares the FAIR
> posture (Findable, Accessible, Interoperable, Reusable) of the data a
> repository holds.

---

## 30-second example

```yaml
---
trust_md_version: "0.1"
title: "My Project — Trust & Epistemic Provenance Declaration"
description: >
  How knowledge in this repository is produced, graded, and reviewed.
canonical: "https://myproject.example.org/trust.md"
license: "CC-BY-4.0"
companions:
  fair: "/fair.md"

produced_by:
  humans:
    - name: "Jane Smith"
      orcid: "0000-0000-0000-0001"
      role: "author, domain reviewer, accountable signatory"
      org: "University of Example"
  agents: []

governance:
  source_of_truth: >
    The human-approved record — not raw model output — is the source of truth.
  no_fabricated_citations: true
  review_policy: "Every published claim is human-reviewed."
  correction_policy: "Errors are corrected in place with a dated note."
  conflict_of_interest: "No commercial interest in the subject matter."

epistemic_model:
  categories:
    - {id: "cited",      label: "Cited fact",           definition: "Directly supported by a cited source"}
    - {id: "consensus",  label: "Established consensus", definition: "Widely accepted domain knowledge"}
    - {id: "inference",  label: "Inference",            definition: "Reasoned from one or more sources"}
    - {id: "hypothesis", label: "Hypothesis",           definition: "Forward-looking or speculative claim"}
    - {id: "view",       label: "Author view",          definition: "Interpretation or normative conclusion"}
  confidence_scale:
    type: "integer"
    range: [0, 100]
    independent_of_category: true
    bands:
      - {range: "90-100", label: "Very high",   meaning: "stated in a primary or peer-reviewed source"}
      - {range: "70-89",  label: "High",        meaning: "stated in a cited source, lightly interpreted"}
      - {range: "50-69",  label: "Moderate",    meaning: "reasonable inference or consensus"}
      - {range: "30-49",  label: "Tentative",   meaning: "plausible claim with partial support"}
      - {range: "0-29",   label: "Speculative", meaning: "opinion or vision with little direct evidence"}

corpus:
  notes_with_markup: 5
  total_claims: 120
  average_trust: 72
  category_distribution: {cited: 65, inference: 30, view: 20, consensus: 3, hypothesis: 2}

artifacts:
  - {path: "/notes/2026-05-example/", claims: 24, avg: 85, dist: {cited: 20, inference: 4}}

limitations:
  - "Confidence scores are author judgements, not statistical measures."
  - "Self-declared; not independently audited."

last_reviewed: "2026-06-06"
---

# trust.md — My Project Trust Declaration

This file declares how much you should trust the knowledge in this repository
and why ...
```

---

## Why trust.md?

Scientific writing — and now AI-assisted scientific writing — mixes *cited fact*,
*reasoned inference*, *forward-looking hypothesis*, and *the author's own
position*, usually with no visible distinction between them. As large language
models help draft more of the literature, the question **"what kind of statement
is this, and how confident is the author?"** becomes urgent and, today, largely
unanswerable from the page itself.

`trust.md` answers it at the level of the whole repository:

- **Provenance of authorship** — which parts are human-written, which are
  AI-assisted, and what oversight applies.
- **A grading model** — five epistemic categories and a 0–100 confidence scale.
- **A corpus profile** — honest aggregate statistics, derivable directly from
  inline claim markup.

### What trust.md is NOT

`trust.md` is deliberately *distinct from* JournalList's **`trust.txt`**, which
declares an organisation's trusted *relationships* (memberships, ownership,
vendors). `trust.md` is about the *epistemic status of the content itself* — what
kind of claims it makes and how well-supported they are.

### Lineage

`trust.md` draws on a rich lineage of assertion and provenance vocabularies:

- **W3C PROV / PAV** — provenance and authoring of assertions; trust.md's
  `produced_by` block maps to PROV-O agents and activities.
- **Nanopublications** — the assertion + provenance + publication-info pattern;
  trust.md's per-claim model is a pragmatic, web-native cousin.
- **SEPIO (Monarch Initiative)** — Scientific Evidence and Provenance Information
  Ontology; the epistemic category model aligns with SEPIO's evidence typing.
- **Evidence & Conclusion Ontology (ECO)** — formal evidence modelling; ECO codes
  are a natural extension of trust.md's category IDs.
- **schema.org ClaimReview** — a path to emit each graded claim as harvestable
  JSON-LD; trust.md's inline encoding is designed with this in mind.
- **JournalList trust.txt** — the naming inspiration; explicitly distinct in scope.

---

## Reference implementation

The canonical `trust.md` for the Neuronautix knowledge base lives at:

**<https://neuronautix.com/trust.md>**

A copy is included in this repository as
[`examples/neuronautix.trust.md`](examples/neuronautix.trust.md).

---

## How to adopt trust.md

1. **Copy** [`trust.md`](trust.md) (the template in this repo) to the root of
   your repository or website.
2. **Fill in** `produced_by` and `governance` honestly — especially the human/AI
   split and the review policy.
3. **Adopt the `epistemic_model`** (or your own). The five categories and the
   0–100 scale can be adjusted for your domain; keep the structure stable so
   validators can parse it.
4. **Mark claims inline** in your content using the encoding defined in
   `epistemic_model.encoding` — so the `corpus` and `artifacts` profiles can be
   derived automatically rather than manually asserted.
5. **Serve** the file at `https://yourdomain/trust.md`.
6. **Pair it with [`fair.md`](https://github.com/Neuronautix/FAIR.md)** — trust.md covers *how
   trustworthy* the content is; fair.md covers *how findable and reusable* it is.
7. **Review** periodically and update `last_reviewed`.

---

## Formal specification

See [`SPEC.md`](SPEC.md) for the complete v0.1 specification, including all
field definitions, the epistemic model, governance fields, corpus/artifact
profiles, validation rules, and conformance requirements.

A JSON Schema for the YAML front matter is at
[`schema/trust.schema.json`](schema/trust.schema.json).

---

## Contributing

This is a proposed convention, not yet a standard. Feedback, issues, and pull
requests are welcome:

- Open an issue to discuss extensions to the epistemic model (additional
  categories, second confidence axis) or alignment with ECO/SEPIO/nanopubs.
- Submit a PR with a worked `examples/` entry to show trust.md in a new domain.
- Reference the formal spec in SPEC.md when proposing changes — keep changes
  backward-compatible within the 0.x series.

The convention follows [Semantic Versioning](https://semver.org/): patch releases
for clarifications, minor releases for additive changes, major releases for
breaking changes.

---

## License

Apache-2.0. See [`LICENSE`](LICENSE).

Copyright 2026 Damien Huzard / Neuronautix.
