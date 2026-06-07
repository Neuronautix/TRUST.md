---
# trust.md — a portable, human- and machine-readable EPISTEMIC TRUST manifest
# Proposed convention (v0.1). Reference implementation: https://neuronautix.com/trust.md
#
# Distinct from JournalList's trust.txt, which declares an organisation's TRUSTED
# RELATIONSHIPS (memberships, ownership, vendors). trust.md instead declares the
# EPISTEMIC STATUS and CONFIDENCE of the knowledge a repository publishes: how it
# was produced (human / AI), how each claim is graded, how it is reviewed, and how
# trustworthy the corpus is — the repository-level companion to per-claim,
# inline epistemic markup (here: the "Trust Lens"; see /notes/EPISTEMIC-MARKUP.md).
#
# Aligns with established assertion/provenance vocabularies: W3C PROV, PAV,
# nanopublications (assertion + provenance + pubinfo), SEPIO (Monarch Initiative),
# the Evidence & Conclusion Ontology (ECO), and schema.org ClaimReview.

trust_md_version: "0.1"
title: "Neuronautix — Trust & Epistemic Provenance Declaration"
description: >
  How knowledge and inferences in this repository are produced, graded, and
  reviewed — and how confident the reader should be in them.
canonical: "https://neuronautix.com/trust.md"
license: "Apache-2.0"   # matching the DESIGN.md format this repo follows
companions:
  fair: "/fair.md"
  inline_markup_spec: "/notes/EPISTEMIC-MARKUP.md"

# ── Who and what produces the knowledge (provenance of authorship) ──
produced_by:
  humans:
    - name: "Damien Huzard, PhD"
      orcid: "0000-0003-4820-7951"
      role: "author, domain reviewer, accountable signatory"
      org: "Neuronautix"
  agents:
    - name: "Claude (Anthropic), via Claude Code"
      role: "retrieval, drafting, epistemic markup, summarisation"
      oversight: "human-reviewed"   # no agent output is published without human review

# ── Governance ──
governance:
  source_of_truth: >
    The human-approved record — not raw model output — is the source of truth.
    AI-assisted text is retrieval-grounded and verified before publication.
  no_fabricated_citations: true
  review_policy: >
    Every published claim is human-reviewed. Claims are tagged with an epistemic
    category and a 0–100 confidence score (see epistemic_model) that the reviewer
    can audit and adjust.
  correction_policy: >
    Errors are corrected in place with a note in the page's changelog / git
    history. Substantive corrections are dated.
  conflict_of_interest: >
    Neuronautix is a scientific consultancy. Promotional or normative statements
    are explicitly labelled as the 'view' category, not presented as cited fact.

# ── The epistemic model (mirrors the inline Trust Lens) ──
epistemic_model:
  categories:
    - {id: "cited",      label: "Cited fact",            definition: "Directly supported by a cited source"}
    - {id: "consensus",  label: "Established consensus",  definition: "Widely accepted domain knowledge / standard definitions"}
    - {id: "inference",  label: "Inference",             definition: "Reasoned from one or more sources; not stated verbatim"}
    - {id: "hypothesis", label: "Hypothesis",            definition: "Forward-looking or speculative claim"}
    - {id: "view",       label: "Neuronautix view",      definition: "Explicit interpretation, position, or normative conclusion"}
  confidence_scale:
    type: "integer"
    range: [0, 100]
    independent_of_category: true   # a 'view' may be sincere but low evidentiary trust
    bands:
      - {range: "90-100", label: "Very high",   meaning: "directly stated in a primary/peer-reviewed/regulatory source"}
      - {range: "70-89",  label: "High",        meaning: "stated in a cited source, secondary or lightly interpreted"}
      - {range: "50-69",  label: "Moderate",    meaning: "reasonable inference, or consensus without a pinpoint citation"}
      - {range: "30-49",  label: "Tentative",   meaning: "plausible forward-looking claim with partial support"}
      - {range: "0-29",   label: "Speculative", meaning: "normative/opinion/vision with little direct evidence"}
  encoding:
    inline: 'HTML spans: <span class="nnx-claim" data-epi="…" data-trust="0-100" data-claim-note="…" data-refs="…">'
    reader_tooling: "Trust Lens (assets/js/trust-lens.js) — toggleable highlight, color-blind-safe palette, per-note summary"
  alignment:
    - "W3C PROV / PAV — provenance & authoring of assertions"
    - "Nanopublications — assertion + provenance + publication info"
    - "SEPIO (Scientific Evidence & Provenance Information Ontology)"
    - "Evidence & Conclusion Ontology (ECO)"
    - "schema.org ClaimReview"

# ── Corpus-level trust profile (auto-derivable from inline markup) ──
corpus:
  notes_with_markup: 19
  total_claims: 440
  average_trust: 74
  category_distribution: {cited: 233, view: 97, inference: 85, consensus: 13, hypothesis: 12}

# ── Per-artifact trust profiles (machine-readable; derived from inline markup) ──
# avg = mean data-trust; dist = claim counts per category.
artifacts:
  - {path: "/notes/2026-05-namo-new-approach-methodology-ontology/",  claims: 40, avg: 88, dist: {cited: 36, inference: 3, view: 1}}
  - {path: "/notes/2026-05-nam-data-management-ind-submissions/",     claims: 29, avg: 83, dist: {cited: 22, inference: 4, view: 3}}
  - {path: "/notes/2026-05-llm-kg-metadata-architecture/",            claims: 43, avg: 81, dist: {cited: 38, consensus: 1, inference: 2, view: 2}}
  - {path: "/notes/2026-06-data-welfare-animal-welfare/",             claims: 25, avg: 80, dist: {cited: 15, consensus: 2, inference: 6, hypothesis: 1, view: 1}}
  - {path: "/notes/2026-05-after-the-knowledge-graph/",               claims: 46, avg: 78, dist: {cited: 21, consensus: 5, inference: 5, view: 15}}
  - {path: "/notes/2026-05-neuronautix-as-research-infrastructure/",  claims: 23, avg: 77, dist: {cited: 15, inference: 3, view: 5}}
  - {path: "/notes/2026-05-ai-ready-nam-data/",                       claims: 20, avg: 76, dist: {cited: 10, inference: 5, view: 5}}
  - {path: "/notes/2026-05-meet-the-founder-damien-huzard/",          claims: 15, avg: 76, dist: {cited: 12, view: 3}}
  - {path: "/notes/2026-05-fairscape-biocompute-nam-provenance/",     claims: 15, avg: 74, dist: {cited: 4, inference: 6, view: 5}}
  - {path: "/notes/2026-05-metadata-as-a-nam/",                       claims: 35, avg: 74, dist: {cited: 14, consensus: 2, inference: 9, view: 10}}
  - {path: "/notes/2026-05-data-first-fair-by-design/",               claims: 12, avg: 72, dist: {cited: 5, inference: 2, view: 5}}
  - {path: "/notes/2026-05-metadata-as-nam/",                         claims: 11, avg: 72, dist: {cited: 2, consensus: 3, inference: 3, view: 3}}
  - {path: "/notes/2026-05-schema-first-metadata-agent-nam/",         claims: 11, avg: 72, dist: {cited: 4, inference: 4, view: 3}}
  - {path: "/notes/2026-05-post-hoc-curation-fails-nam-platforms/",   claims: 15, avg: 70, dist: {cited: 6, inference: 5, view: 4}}
  - {path: "/notes/2026-05-linkml-preclinical-metadata/",             claims: 8,  avg: 68, dist: {cited: 4, inference: 2, view: 2}}
  - {path: "/notes/2026-05-nam-metadata-mandatory-qualification/",    claims: 21, avg: 68, dist: {cited: 7, inference: 10, view: 4}}
  - {path: "/notes/2026-05-human-loop-ai-ready-preclinical-data/",    claims: 11, avg: 59, dist: {cited: 4, inference: 3, view: 4}}
  - {path: "/notes/2026-05-nam-evidence-commons-tool-stack/",         claims: 34, avg: 55, dist: {cited: 7, inference: 10, hypothesis: 1, view: 16}}
  - {path: "/notes/2026-06-hcm-2050-vision/",                         claims: 26, avg: 54, dist: {cited: 7, inference: 3, hypothesis: 10, view: 6}}

limitations:
  - "Confidence scores are author/reviewer judgements, not statistical measures."
  - "Self-declared; not independently audited."
  - "A single 0–100 score currently conflates evidence strength and stated confidence (a planned second axis would separate them)."

last_reviewed: "2026-06-06"
---

# trust.md — Neuronautix Trust & Epistemic Provenance

This file declares **how much you should trust the knowledge in this repository,
and why**. It is the repository-level companion to the inline *Trust Lens* —
the per-claim epistemic markup readers can toggle on any note. The YAML block
above is machine-readable; this prose is for people.

It is a **proposed convention (v0.1)**, with this repository as its reference
implementation.

## Why trust.md?

Scientific writing — and now AI-assisted scientific writing — mixes *cited
fact*, *reasoned inference*, *forward-looking hypothesis*, and *the author's
own position*, usually with no visible distinction between them. As large
language models help draft more of the literature, the question "**what kind of
statement is this, and how confident is the author?**" becomes urgent and, today,
largely unanswerable from the page itself.

`trust.md` answers it at the level of the whole repository:

- **Provenance of authorship** — which parts are human-written, which are
  AI-assisted, and what oversight applies.
- **A grading model** — five epistemic categories and a 0–100 confidence scale.
- **A corpus profile** — honest aggregate statistics, derivable directly from
  the inline markup.

It is deliberately *distinct from* JournalList's **`trust.txt`**, which declares
an organisation's trusted *relationships* (memberships, ownership). trust.md is
about the *epistemic status of the content itself*.

## How knowledge here is produced

This repository is authored by a human domain expert (Damien Huzard, PhD) with
AI assistance (Claude, via Claude Code) for retrieval, drafting, and epistemic
markup. The governing rule is simple: **the human-approved record, not raw model
output, is the source of truth.** AI-assisted text is retrieval-grounded and
verified before publication; fabricated citations are not permitted. Promotional
or normative statements — unavoidable for a consultancy — are explicitly tagged
as the *view* category rather than dressed up as fact.

## The grading model

Every marked claim carries two independent axes:

1. **Category** (*what kind of statement*): `cited` · `consensus` · `inference` ·
   `hypothesis` · `view`.
2. **Confidence** (*how well supported*): an integer **0–100**, bucketed into five
   bands from *Speculative* to *Very high*.

These are independent: a *view* can be sincerely held but low in evidentiary
trust; a *hypothesis* can be well-motivated yet tentative. The same model is
encoded inline (`data-epi` + `data-trust` on each claim) and rendered by the
Trust Lens; see **[`/notes/EPISTEMIC-MARKUP.md`](/notes/EPISTEMIC-MARKUP.md)**.

## Corpus trust profile

As of the last review, the marked corpus is:

- **19 notes · 440 graded claims · average confidence 74 / 100.**
- **Category mix:** 53% cited · 22% Neuronautix view · 19% inference · 3%
  consensus · 3% hypothesis.

The most evidence-dense notes (e.g. the NAMO and IND-submission notes) average
**88** and **83**; the explicitly forward-looking ones — the *HCM 2050 vision*
(avg 54, ten hypotheses) and the *NAM Evidence Commons* build-plan (avg 55,
sixteen *views*) — score lowest **by design**. A low average here is a feature:
it tells the reader the piece is a position or a prediction, not a literature
report. The per-artifact table in the YAML above makes this auditable.

## Relationship to existing standards

trust.md is a lightweight *front door*, not a competitor, to the formal
assertion/provenance stack:

- **W3C PROV / PAV** — provenance and authoring of assertions.
- **Nanopublications** — the assertion + provenance + publication-info pattern;
  trust.md's per-claim model is a pragmatic, web-native cousin.
- **SEPIO** (Monarch Initiative — the same project behind NAMO, which this repo
  documents) and the **Evidence & Conclusion Ontology (ECO)** — formal evidence
  and assertion modelling.
- **schema.org `ClaimReview`** — a path to emit each graded claim as harvestable
  JSON-LD (planned).

## How to adopt trust.md

1. Copy this file to your repo / site root as `trust.md`; serve it at
   `https://yourdomain/trust.md`.
2. Fill in `produced_by` and `governance` honestly — especially the
   human/AI split and the review policy.
3. Adopt the `epistemic_model` (or your own), and mark claims inline so the
   `corpus` and `artifacts` profiles can be generated automatically rather than
   asserted.
4. Pair it with **[`/fair.md`](/fair.md)** so a reader gets both halves: *can I
   find and reuse this?* (FAIR) and *how much should I trust it?* (trust).

## Limitations

- Confidence scores are expert judgements, not statistical measures.
- This is a self-declaration, not an independent audit.
- The single 0–100 score currently blends *evidence strength* and *stated
  confidence*; a planned second axis would separate them.

## Changelog

- **v0.1 (2026-06-06)** — first draft of the trust.md convention and this
  reference implementation, derived from the repository's inline Trust Lens
  markup.
