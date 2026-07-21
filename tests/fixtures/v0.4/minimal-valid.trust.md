---
trust_md_version: "0.4"
title: "Minimal valid v0.4 fixture"
description: "A versioned subject with no assessment."
canonical: "https://example.org/fixtures/minimal/trust.md"
license: "CC-BY-4.0"
companions: {fair: null}
produced_by:
  humans: [{name: "Fixture Author", role: "author"}]
  agents: []
governance:
  source_of_truth: "The fixture."
  no_fabricated_citations: true
  review_policy: "No assessment is claimed."
  correction_policy: "Create a new version."
  conflict_of_interest: "None declared."
epistemic_model:
  categories: [{id: "record", label: "Record", definition: "A recorded statement."}]
  support_bands:
    - {id: "speculative", label: "Speculative", meaning: "Little or no direct support."}
    - {id: "tentative", label: "Tentative", meaning: "Limited support."}
    - {id: "moderate", label: "Moderate", meaning: "Partial support."}
    - {id: "high", label: "High", meaning: "Strong support."}
    - {id: "very-high", label: "Very high", meaning: "Direct support."}
subjects:
  - id: "subject-001"
    type: "evidence-record"
    identifier: "https://example.org/evidence/fixture-001"
    version: "1.0"
assessments: []
last_reviewed: "2026-07-21"
---

# Minimal valid fixture

This fixture verifies that subjects remain representable without assessments.
