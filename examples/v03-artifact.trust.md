---
trust_md_version: "0.3"
title: "Artifact-level TRUST.md v0.3 example"
description: "A repository declaration with one assessed document."
canonical: "https://example.org/trust.md"
license: "CC-BY-4.0"
companions:
  fair: null
produced_by:
  humans:
    - name: "Example Author"
      role: "author"
  agents: []
governance:
  source_of_truth: "The human-approved repository record."
  no_fabricated_citations: true
  review_policy: "A named human reviews the declaration."
  correction_policy: "Corrections are recorded in version control."
  conflict_of_interest: "None declared."
epistemic_model:
  categories:
    - id: "cited"
      label: "Cited fact"
      definition: "Directly supported by a cited source."
  support_bands:
    - {id: "speculative", label: "Speculative", meaning: "Little or no direct support.", range: "0-29"}
    - {id: "tentative", label: "Tentative", meaning: "Limited support.", range: "30-49"}
    - {id: "moderate", label: "Moderate", meaning: "Partial or indirect support.", range: "50-69"}
    - {id: "high", label: "High", meaning: "Supported with minor interpretation.", range: "70-89"}
    - {id: "very-high", label: "Very high", meaning: "Direct and verifiable support.", range: "90-100"}
  confidence_scale:
    type: "integer"
    range: [0, 100]
    independent_of_category: true
    not_probability: true
  dimensions:
    evidence_support: "direct"
    review_status: "human-reviewed"
    calibration: "matched"
    source_integrity: "verified"
assessment:
  unit: "artifact"
  review_status: "human-reviewed"
  assessed_by:
    humans:
      - name: "Example Reviewer"
        role: "reviewer"
    agents: []
  protocol: "TRUST.md v0.3 declaration review"
  date: "2026-07-21"
  independent_review: true
corpus:
  notes_with_markup: 2
  total_claims: 4
  category_distribution: {cited: 4}
  band_distribution: {speculative: 0, tentative: 0, moderate: 1, high: 1, very-high: 2}
  median_band: "high"
artifacts:
  - path: "/reports/example-review.md"
    claims: 4
    band_distribution: {speculative: 0, tentative: 0, moderate: 1, high: 1, very-high: 2}
    median_band: "high"
    dimensions:
      evidence_support: "direct"
      review_status: "human-reviewed"
      calibration: "matched"
      source_integrity: "verified"
limitations:
  - "Self-declared metadata."
last_reviewed: "2026-07-21"
---

# Artifact-level declaration

The assessment applies to `/reports/example-review.md`; the repository-level
metadata supplies its governance and provenance context.
