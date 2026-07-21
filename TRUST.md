---
# TRUST.md v0.4 template
#
# Every REPLACE value is a placeholder, not a real-world assertion. This
# template identifies a reserved example subject and publishes zero
# assessments. Add an assessment only after the work and provenance exist.

trust_md_version: "0.4"
title: "REPLACE — Project Trust and Epistemic Provenance Declaration"
description: "REPLACE — Describe the evidence scope covered by this declaration."
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
  review_policy: "REPLACE — Describe how assessment review is declared."
  correction_policy: "REPLACE — Describe append-only correction and versioning."
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

subjects:
  - id: "subject-001"
    type: "evidence-record"
    identifier: "https://example.invalid/evidence/REPLACE"
    version: "REPLACE-WITH-EXACT-VERSION"

assessments: []

limitations:
  - "Template values marked REPLACE are placeholders; this file publishes no assessment."

# Replace with the date on which the completed declaration was reviewed.
last_reviewed: "2026-07-21"
---

# TRUST.md v0.4 template — replace all placeholders

This template is deliberately unassessed. It contains no assessment result,
fitness conclusion, review claim, independence claim, impact metric, or
fictional reviewer. Replace every `REPLACE` value, identify the exact evidence
subject, and add independently versioned assessments only when their protocol,
basis, assessors, time, lifecycle, and limitations are real and inspectable.
