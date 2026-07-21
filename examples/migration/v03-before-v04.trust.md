---
trust_md_version: "0.3"
title: "v0.3 declaration before explicit v0.4 migration"
description: "A singular repository assessment retained unchanged as migration input."
canonical: "https://example.org/migration/v03/trust.md"
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
  unit: "repository"
  review_status: "human-reviewed"
  assessed_by:
    humans:
      - name: "Example Reviewer"
        role: "reviewer"
    agents: []
  protocol: "Repository declaration review"
  date: "2026-07-21"
  independent_review: true
corpus:
  total_claims: 2
  average_trust: 80
  band_distribution: {speculative: 0, tentative: 0, moderate: 0, high: 1, very-high: 1}
  median_band: "high"
limitations:
  - "This source remains governed by the frozen v0.3 schema."
last_reviewed: "2026-07-21"
---

# Immutable migration input

This file is the unchanged v0.3 side of an explicit migration pair. It remains
valid under the frozen v0.3 schema. Its retained `average_trust` field produces
the documented deprecation notice and is not converted into a v0.4 aggregate.
