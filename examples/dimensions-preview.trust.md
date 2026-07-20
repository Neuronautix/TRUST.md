---
# trust.md — dimensions preview example
#
# PURPOSE: a worked preview of the multidimensional assessment model proposed
# for v0.3 (NEXT_VERSION_PLAN.md §5.1, DECISIONS.md D-012). This file is FULLY
# CONFORMANT TO v0.2 as published: every proposed structure is carried in
# `x_`-namespaced extension fields per SPEC.md §5.3, so it validates against
# the current schema and CLI unchanged.
#
# WHAT IT DEMONSTRATES
#   1. Band meanings rewritten to describe EVIDENCE SUPPORT ONLY (defect D10
#      fix): no category vocabulary, so a 'view' can legitimately score 95 and
#      a 'cited' claim can score 20 — the axes are actually independent.
#   2. The proposed dimensions: evidence_support, review_status, calibration,
#      source_integrity — typed ordinal/state vocabularies, NEVER summed.
#   3. Traceability realised as the x_assessment provenance block (recorded,
#      not scored).
#   4. Missing-data semantics: absent ≠ not-assessed ≠ not-applicable ≠ lowest
#      level (D-004).
#   5. Aggregation without means: a band distribution and a median band
#      alongside the (deprecation-proposed) average_trust.
#
# ALL NUMBERS IN THIS FILE ARE ILLUSTRATIVE. They describe a fictional
# project ("Aurora Field Notes") and are NOT real assessment data.

trust_md_version: "0.2"
title: "Aurora Field Notes — Trust & Epistemic Provenance Declaration (dimensions preview)"
description: >
  Illustrative trust manifest for a fictional knowledge base, previewing the
  multidimensional assessment model proposed for trust.md v0.3 via
  x_-namespaced extension fields. Conformant to v0.2.
canonical: "https://aurora.example.org/trust.md"
license: "CC-BY-4.0"
companions:
  fair: null                       # allowed: no fair.md exists yet
  inline_markup_spec: "/notes/EPISTEMIC-MARKUP.md"

produced_by:
  humans:
    - name: "Ada Example"          # fictional person for this worked example
      orcid: "0000-0000-0000-0001" # illustrative, format-valid placeholder
      role: "author, domain reviewer, accountable signatory"
      org: "Aurora Collective (fictional)"
  agents:
    - name: "Claude (Anthropic)"
      role: "retrieval, drafting, epistemic markup"
      oversight: "human-reviewed"

governance:
  source_of_truth: >
    The human-approved record — not raw model output — is the source of truth.
  no_fabricated_citations: true
  review_policy: >
    Every published claim is reviewed; the review level reached is recorded
    per claim as review_status (see x_dimensions) rather than implied.
  correction_policy: >
    Errors are corrected in place with a dated note; superseded assessments
    remain retrievable via git history.
  conflict_of_interest: "None; fictional demonstration project."

epistemic_model:
  categories:
    - {id: "cited",      label: "Cited fact",            definition: "Directly supported by a cited source"}
    - {id: "consensus",  label: "Established consensus",  definition: "Widely accepted domain knowledge / standard definitions"}
    - {id: "inference",  label: "Inference",             definition: "Reasoned from one or more sources; not stated verbatim"}
    - {id: "hypothesis", label: "Hypothesis",            definition: "Forward-looking or speculative claim"}
    - {id: "view",       label: "Aurora view",           definition: "Explicit interpretation, position, or normative conclusion"}
  confidence_scale:
    type: "integer"
    range: [0, 100]
    independent_of_category: true
    # Band meanings describe evidence support ONLY (proposed D10 fix): no
    # category words, so category and confidence are genuinely independent.
    bands:
      - {range: "90-100", label: "Very high",   meaning: "direct, verifiable support in a primary source"}
      - {range: "70-89",  label: "High",        meaning: "supported by cited sources with minor interpretation"}
      - {range: "50-69",  label: "Moderate",    meaning: "partial or indirect support from cited sources"}
      - {range: "30-49",  label: "Tentative",   meaning: "limited support; substantial interpretive distance"}
      - {range: "0-29",   label: "Speculative", meaning: "little or no direct evidentiary support"}
  encoding:
    inline: >
      HTML spans: <span class="claim" data-epi="cited" data-band="high"
      data-support="direct" data-review="human-reviewed"
      data-integrity="verified" data-refs="[1]">. The legacy numeric
      data-trust attribute remains valid; the band is primary.
    reader_tooling: "None yet; attributes are consumed by the corpus statistics script."
  alignment:
    - "W3C PROV / PAV — provenance & authoring of assertions (informal mapping)"
    - "Evidence & Conclusion Ontology (ECO) — mapping table pending"

# ── Proposed v0.3 dimension vocabularies (x_-namespaced; see D-012) ──
# Each dimension means ONE thing and is never summed with the others.
# Missing-data semantics (D-004): an ABSENT dimension on a claim means "not
# assessed, no statement made"; the explicit value "not-assessed" means
# "considered and deliberately not assessed"; "not-applicable" means the
# dimension does not apply to that claim; the lowest level ("none",
# "unreviewed", "unverified") is an assessment RESULT, never a default.
x_dimensions:
  evidence_support:
    definition: "How directly and strongly cited sources support the claim."
    levels: [direct, indirect, partial, contested, none]
    states: [not-assessed, not-applicable]
  review_status:
    definition: "Highest review actually performed on the claim. Agreement among multiple agents caps at agent-reviewed (agreement is not validation)."
    levels: [unreviewed, agent-reviewed, human-reviewed, adjudicated]
  calibration:
    definition: "Whether the claim's wording matches the available evidence."
    levels: [understated, matched, overstated]
    states: [not-assessed]
  source_integrity:
    definition: "Citation integrity ONLY: cited sources exist, are quoted accurately, and support the claim. Never a judgement of venue or author prestige."
    levels: [verified, partially-verified, unverified]
    states: [not-applicable]   # e.g. views/hypotheses that cite nothing
  x_note_traceability: >
    Traceability is deliberately NOT a scored dimension: it is realised as the
    x_assessment provenance block below (assessor, protocol, date,
    supersession). You record traceability; you do not grade it.

# ── Proposed v0.3 assessment provenance block (x_-namespaced) ──
x_assessment:
  unit: "repository"               # repository | artifact | claim | claim-evidence
  protocol: "TRUST.md v0.3 draft dimensions — NEXT_VERSION_PLAN.md §5.1 (this repo)"
  assessed_by:
    humans:
      - name: "Ada Example"
        orcid: "0000-0000-0000-0001"
        role: "assessor"
    agents:
      - name: "Claude (Anthropic)"
        role: "first-pass dimension tagging"
        oversight: "human-reviewed"
  date: "2026-07-20"
  supersedes: null                 # no earlier assessment of this corpus
  independent_review: false        # self-declaration (principle 10)

corpus:
  notes_with_markup: 2
  total_claims: 24
  average_trust: 71                # valid in v0.2; proposed DEPRECATED in v0.3
                                   # (mean of ordinal judgements) — prefer the
                                   # distribution and median below
  category_distribution: {cited: 10, consensus: 3, inference: 6, hypothesis: 2, view: 3}
  x_band_distribution:             # proposed v0.3 replacement summary: counts, no means
    very-high: 6
    high: 8
    moderate: 6
    tentative: 3
    speculative: 1
  x_median_band: "high"

# Standard v0.2 artifact profiles (schema forbids extra keys inside entries —
# defect D8c — so the dimensional profiles live in x_dimension_profiles below).
artifacts:
  - {path: "/notes/2026-07-aurora-survey/",   claims: 14, avg: 78, dist: {cited: 7, consensus: 2, inference: 3, view: 2}}
  - {path: "/notes/2026-07-aurora-outlook/",  claims: 10, avg: 61, dist: {cited: 3, consensus: 1, inference: 3, hypothesis: 2, view: 1}}

# ── Per-artifact dimensional profiles (proposed v0.3; counts per level) ──
# Counts in each dimension sum to the artifact's claim count.
x_dimension_profiles:
  - path: "/notes/2026-07-aurora-survey/"
    evidence_support: {direct: 7, indirect: 3, partial: 3, none: 1}
    source_integrity: {verified: 9, partially-verified: 1, not-applicable: 4}
    review_status:    {human-reviewed: 12, agent-reviewed: 2}
    calibration:      {matched: 11, overstated: 2, not-assessed: 1}
  - path: "/notes/2026-07-aurora-outlook/"
    evidence_support: {direct: 3, indirect: 2, partial: 2, contested: 1, none: 2}
    source_integrity: {verified: 4, unverified: 2, not-applicable: 4}
    review_status:    {human-reviewed: 4, agent-reviewed: 3, adjudicated: 1, unreviewed: 2}
    calibration:      {matched: 6, understated: 1, not-assessed: 3}
    # calibration was assessed for only 7 of 10 claims here; the other 3 are
    # explicitly "not-assessed". Claims where calibration is simply ABSENT in
    # the inline markup are a different state again and are not counted.

limitations:
  - "All figures are illustrative demonstration data for a fictional project, not real assessments."
  - "Confidence values and dimension levels are assessor judgements, not statistical measures, and are NOT probabilities that claims are true."
  - "Self-declared; independent_review is false and no external audit has occurred."
  - "The x_-prefixed blocks preview a proposed v0.3 model that is not yet part of the specification."

last_reviewed: "2026-07-20"
---

# trust.md — Aurora Field Notes (dimensions preview)

This example previews the **multidimensional assessment model proposed for
trust.md v0.3** while remaining a fully conformant **v0.2** file: every
proposed structure is carried in `x_`-namespaced extension fields, which the
current specification explicitly permits (SPEC.md §5.3).

**Everything here describes a fictional project. All numbers are
illustrative.**

## What replaces the single score — and what doesn't

Nothing is removed. The 0–100 confidence value remains valid, but this file
treats the **band** as the primary semantic (the integer is a refinement
inside a band) and adds four typed dimensions, each meaning exactly one thing:

| Dimension | Question it answers | Values |
|---|---|---|
| `evidence_support` | How directly do the cited sources support this claim? | direct · indirect · partial · contested · none |
| `review_status` | What is the highest review actually performed? | unreviewed · agent-reviewed · human-reviewed · adjudicated |
| `calibration` | Does the wording match the evidence? | understated · matched · overstated |
| `source_integrity` | Are the citations real, accurate, and supporting? | verified · partially-verified · unverified |

**They are never summed.** There is no formula in which transparency points
offset missing evidence — the "aurora-outlook" note above shows two claims
with `evidence_support: none` and they stay visible as exactly that,
regardless of how well-reviewed the note is. **Traceability is recorded, not
scored:** the `x_assessment` block names the assessor, the protocol, and the
date, and says whether the assessment is independent (here: no — this is a
self-declaration).

## What the values are not

- **Not probabilities.** `avg: 78` does not mean "78% likely true". It is an
  ordinal author judgement about evidence support, bucketed into five bands.
- **Not scores for people or venues.** `source_integrity` is citation
  integrity — whether the quoted sources say what the text claims — never a
  rating of the journal, laboratory, or author that produced them.
- **Not validation by agreement.** The agent tagged dimensions first and a
  human reviewed them; had three agents agreed with each other instead, the
  review status would still cap at `agent-reviewed`.

## Missing-data states, shown deliberately

The "aurora-outlook" profile distinguishes four things v0.2 collapses:
three claims are **explicitly `not-assessed`** for calibration (considered,
deliberately skipped); four claims are **`not-applicable`** for source
integrity (they cite nothing, being views/hypotheses); two claims are
**`unverified`** (checked and found wanting — a result, not a default); and
anything simply **absent** from the inline markup makes no statement at all.

## Aggregation without means

`average_trust: 71` is kept because v0.2 requires it, with its proposed v0.3
replacements alongside: `x_band_distribution` (counts per band — the honest
summary of ordinal data) and `x_median_band: high`. A reader who wants one
takeaway gets the median band; a reader who wants the truth gets the
distribution.

## Changelog

- **2026-07-20** — initial dimensions-preview example accompanying
  NEXT_VERSION_PLAN.md and DECISIONS.md D-012.
