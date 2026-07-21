---
trust_md_version: "0.1"
title: "Minimal TRUST.md v0.1 compatibility fixture"
description: "A compact declaration retained to protect v0.1 compatibility."
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
  confidence_scale:
    type: "integer"
    range: [0, 100]
    independent_of_category: true
    bands:
      - {range: "90-100", label: "Very high", meaning: "Direct support."}
      - {range: "70-89", label: "High", meaning: "Strong support."}
      - {range: "50-69", label: "Moderate", meaning: "Partial support."}
      - {range: "30-49", label: "Tentative", meaning: "Limited support."}
      - {range: "0-29", label: "Speculative", meaning: "Little direct support."}
limitations:
  - "Compatibility fixture only."
last_reviewed: "2026-07-21"
---

# Minimal v0.1 compatibility fixture

This file preserves an explicit declaration for frozen v0.1 regression tests.
