---
# trust.md — Traceable · Reviewed · Uncertainty-graded · Sourced · Transparent
# A portable, human- and machine-readable EPISTEMIC TRUST manifest
# Proposed convention (v0.2). Specification: https://github.com/Neuronautix/TRUST.md
# Reference implementation: https://neuronautix.com/trust.md
#
# HOW TO USE THIS TEMPLATE
# 1. Copy this file to the root of your repository/site as `trust.md`.
# 2. Replace every <PLACEHOLDER> with your project's values.
# 3. Fill in produced_by and governance honestly — especially the human/AI split.
# 4. Mark claims inline in your content so corpus/artifacts can be auto-derived.
# 5. Serve at https://yourdomain/trust.md.
# 6. Pair with fair.md for the full picture: FAIR posture + epistemic trust.
#
# Distinct from JournalList's trust.txt, which declares an organisation's TRUSTED
# RELATIONSHIPS. trust.md declares the EPISTEMIC STATUS of the content itself.
#
# Aligns with: W3C PROV/PAV, nanopublications, SEPIO (Monarch Initiative),
# Evidence & Conclusion Ontology (ECO), schema.org ClaimReview.

trust_md_version: "0.2"
title: "<Project Name> — Trust & Epistemic Provenance Declaration"
description: >
  How knowledge and inferences in this repository are produced, graded, and
  reviewed — and how confident the reader should be in them.
canonical: "<https://yourdomain/trust.md>"
license: "<Apache-2.0>"   # SPDX identifier for this document
companions:
  fair: "/fair.md"                          # FAIR posture companion (strongly recommended)
  inline_markup_spec: null                  # path to inline claim markup documentation, if any

# ── Who and what produces the knowledge (provenance of authorship) ──
# Maps to W3C PROV-O agents. At least one human MUST be listed.
produced_by:
  humans:
    - name: "<Full Name>"
      orcid: "<0000-0000-0000-0000>"   # strongly recommended
      role: "<author | domain reviewer | accountable signatory — list all that apply>"
      org: "<Institutional affiliation>"
    # Add more humans as needed
  agents:
    # List all AI/automated tools involved in producing content.
    # Use [] if no agents are involved.
    - name: "<AI system name and provider, e.g. 'Claude (Anthropic)'>"
      role: "<what the agent does, e.g. 'retrieval, drafting, summarisation'>"
      oversight: "<human-reviewed | human-in-the-loop | automated | none>"
    # oversight MUST be one of those four values.

# ── Governance ──
governance:
  source_of_truth: >
    <State what the authoritative record is. E.g.: "The human-approved record —
    not raw model output — is the source of truth.">
  no_fabricated_citations: true   # MUST be a boolean; set false only with explicit justification
  review_policy: >
    <Describe how claims are reviewed before publication. E.g.: "Every published
    claim is human-reviewed before publication.">
  correction_policy: >
    <Describe how errors are corrected. E.g.: "Errors are corrected in place with
    a dated note in the page changelog or git history.">
  conflict_of_interest: >
    <Disclose any commercial or personal interests that may influence content. If
    none, say so. E.g.: "No commercial interest in the subject matter.">

# ── The epistemic model ──
# Two independent axes per claim:
#   1. Category (what kind of statement)
#   2. Confidence (how well supported, 0–100)
# These are INDEPENDENT: a 'view' may be sincere but low in evidentiary trust;
# a 'hypothesis' can be well-motivated yet tentative.
epistemic_model:
  categories:
    # The five canonical categories are RECOMMENDED for interoperability.
    # You may adjust labels and definitions; keep IDs stable.
    - {id: "cited",      label: "Cited fact",            definition: "Directly supported by a cited source"}
    - {id: "consensus",  label: "Established consensus",  definition: "Widely accepted domain knowledge / standard definitions"}
    - {id: "inference",  label: "Inference",             definition: "Reasoned from one or more sources; not stated verbatim"}
    - {id: "hypothesis", label: "Hypothesis",            definition: "Forward-looking or speculative claim"}
    - {id: "view",       label: "<Author/Org> view",     definition: "Explicit interpretation, position, or normative conclusion"}  # ← Replace <Author/Org> with your project or organisation name (e.g. "Neuronautix view")
    # Add domain-specific categories here if needed, e.g.:
    # - {id: "model_output", label: "Model output", definition: "Produced by a computational model; not yet experimentally validated"}
  confidence_scale:
    type: "integer"
    range: [0, 100]
    independent_of_category: true   # MUST remain true per the specification
    bands:
      # Five bands are REQUIRED. Adjust meanings for your domain if needed.
      - {range: "90-100", label: "Very high",   meaning: "directly stated in a primary, peer-reviewed, or regulatory source"}
      - {range: "70-89",  label: "High",        meaning: "stated in a cited source, secondary or lightly interpreted"}
      - {range: "50-69",  label: "Moderate",    meaning: "reasonable inference, or consensus without a pinpoint citation"}
      - {range: "30-49",  label: "Tentative",   meaning: "plausible forward-looking claim with partial support"}
      - {range: "0-29",   label: "Speculative", meaning: "normative/opinion/vision with little direct evidence"}
  # encoding: describe how claims are marked inline (optional but recommended)
  # encoding:
  #   inline: 'HTML: <span class="claim" data-epi="cited" data-trust="85" data-refs="[1]">'
  #   reader_tooling: "<description of any tooling that renders the markup>"
  alignment:
    - "W3C PROV / PAV — provenance & authoring of assertions"
    - "Nanopublications — assertion + provenance + publication info"
    - "SEPIO (Scientific Evidence & Provenance Information Ontology)"
    - "Evidence & Conclusion Ontology (ECO)"
    - "schema.org ClaimReview"

# ── Corpus-level trust profile ──
# Derive these numbers from your inline markup. Keep them in sync with last_reviewed.
# If you do not yet use inline markup, omit this block or use placeholder zeros.
corpus:
  notes_with_markup: 0         # number of content items with inline claim markup
  total_claims: 0              # total graded claims across the corpus
  average_trust: 0             # mean confidence score (0–100)
  category_distribution:       # claim counts per category id
    cited: 0
    consensus: 0
    inference: 0
    hypothesis: 0
    view: 0

# ── Per-artifact trust profiles ──
# One entry per content item. Ordered by avg descending (most evidence-dense first).
# Derive from inline markup; update with each publication.
# Remove this block if you have no marked claims yet.
artifacts: []
# Example entry:
# artifacts:
#   - {path: "/notes/2026-05-example/", claims: 24, avg: 85, dist: {cited: 20, inference: 4}}

limitations:
  - "<Confidence scores are author judgements, not statistical measures.>"
  - "<Self-declared; not independently audited.>"
  # Add any domain-specific or methodology-specific limitations here.

last_reviewed: "<YYYY-MM-DD>"
---

# trust.md — <Project Name> Trust & Epistemic Provenance

This file declares **how much you should trust the knowledge in this repository,
and why**. The YAML block above is machine-readable; this prose is for people.

It is a **proposed convention (v0.1)**, with the Neuronautix knowledge base as
its reference implementation. See the [trust.md specification](https://github.com/Neuronautix/TRUST.md)
and the [reference implementation](https://neuronautix.com/trust.md).

## Why trust.md?

<!-- Replace this section with a short narrative explaining why epistemic
     transparency matters for your specific repository and audience. -->

## How knowledge here is produced

<!-- Describe the human/AI production model for your repository. Who writes?
     What role, if any, do automated tools play? What oversight applies?
     Be specific — vague governance statements are less useful. -->

## The grading model

Every marked claim carries two independent axes:

1. **Category** (*what kind of statement*): `cited` · `consensus` · `inference` ·
   `hypothesis` · `view` (see `epistemic_model.categories` above for definitions).
2. **Confidence** (*how well supported*): an integer **0–100**, bucketed into five
   bands from *Speculative* to *Very high*.

These are independent: a *view* can be sincerely held but low in evidentiary
trust; a *hypothesis* can be well-motivated yet tentative.

## Corpus trust profile

<!-- Summarise the corpus statistics when you have them. Interpret the numbers:
     a low average is not a failure if the content is explicitly forward-looking.
     Example:
     "As of the last review: N notes · M graded claims · average confidence X / 100."
     "Category mix: X% cited · Y% view · Z% inference." -->

## Relationship to existing standards

trust.md is a lightweight *front door*, not a competitor, to the formal
assertion/provenance stack:

- **W3C PROV / PAV** — provenance and authoring of assertions.
- **Nanopublications** — the assertion + provenance + publication-info pattern.
- **SEPIO** (Monarch Initiative) and the **Evidence & Conclusion Ontology (ECO)** —
  formal evidence and assertion modelling.
- **schema.org `ClaimReview`** — a path to emit each graded claim as harvestable
  JSON-LD.

## How to adopt trust.md

See the [trust.md specification](https://github.com/Neuronautix/TRUST.md) and
pair this file with a **[`/fair.md`](/fair.md)** so readers get both halves:
*can I find and reuse this?* (FAIR) and *how much should I trust it?* (trust).

## Limitations

<!-- List known limitations of this self-declaration.
     Honest limitations improve credibility. -->

## Changelog

- **v0.1 (<YYYY-MM-DD>)** — initial trust.md for this repository.
