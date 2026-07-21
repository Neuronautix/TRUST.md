---
# TRUST.md v0.3 template
#
# Every value marked REPLACE is a placeholder, not a real assertion. Optional
# assessment, dimensions, and corpus blocks are deliberately absent: add them
# only when the corresponding work has actually been performed.

trust_md_version: "0.3"
title: "REPLACE — Project Trust & Epistemic Provenance Declaration"
description: "REPLACE — Describe what knowledge and repository scope this declaration covers."
canonical: "https://example.invalid/trust.md"
license: "REPLACE-WITH-SPDX-ID"

companions:
  fair: null

produced_by:
  humans:
    - name: "REPLACE WITH ACCOUNTABLE HUMAN"
      role: "REPLACE WITH ROLE"
  agents: []

governance:
  source_of_truth: "REPLACE — Identify the authoritative record."
  no_fabricated_citations: true
  review_policy: "REPLACE — Describe the review actually performed."
  correction_policy: "REPLACE — Describe correction and versioning behavior."
  conflict_of_interest: "REPLACE — Declare relevant interests or state that none are declared."

epistemic_model:
  categories:
    - {id: "cited", label: "Cited fact", definition: "Directly supported by a cited source."}
    - {id: "consensus", label: "Established consensus", definition: "Widely accepted domain knowledge or a standard definition."}
    - {id: "inference", label: "Inference", definition: "Reasoned from one or more sources rather than stated verbatim."}
    - {id: "hypothesis", label: "Hypothesis", definition: "A forward-looking or speculative claim."}
    - {id: "view", label: "Author view", definition: "An explicit interpretation, position, or normative conclusion."}
  support_bands:
    - {id: "speculative", label: "Speculative", meaning: "Little or no direct evidentiary support."}
    - {id: "tentative", label: "Tentative", meaning: "Limited support with substantial interpretive distance."}
    - {id: "moderate", label: "Moderate", meaning: "Partial or indirect support from cited evidence."}
    - {id: "high", label: "High", meaning: "Cited evidence supports the claim with minor interpretation."}
    - {id: "very-high", label: "Very high", meaning: "Direct, verifiable support in primary evidence."}

limitations:
  - "Template values marked REPLACE are placeholders; this file is not a completed assessment."

# Replace with the date on which your completed declaration was reviewed.
last_reviewed: "2026-07-21"
---

# TRUST.md template — replace all placeholders

This is an unassessed template. It does not claim that a review occurred and it
does not contain assessment results, corpus statistics, or fictional reviewer
provenance. Replace every value marked `REPLACE`, describe the project for human
readers, and add optional assessment fields only when their provenance is real.
