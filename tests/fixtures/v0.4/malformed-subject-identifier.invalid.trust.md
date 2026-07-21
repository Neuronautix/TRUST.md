---
trust_md_version: "0.4"
title: "Malformed subject identifier"
description: "An intentionally invalid v0.4 fixture."
canonical: "https://example.org/fixtures/invalid-subject/trust.md"
license: "CC-BY-4.0"
companions: {fair: null}
produced_by: {humans: [{name: "Fixture Author", role: "author"}], agents: []}
governance:
  source_of_truth: "The fixture."
  no_fabricated_citations: true
  review_policy: "No assessment is claimed."
  correction_policy: "Create a new version."
  conflict_of_interest: "None declared."
epistemic_model:
  categories: [{id: "record", label: "Record", definition: "A record."}]
  support_bands:
    - {id: "speculative", label: "Speculative", meaning: "Low."}
    - {id: "tentative", label: "Tentative", meaning: "Limited."}
    - {id: "moderate", label: "Moderate", meaning: "Partial."}
    - {id: "high", label: "High", meaning: "Strong."}
    - {id: "very-high", label: "Very high", meaning: "Direct."}
subjects:
  - {id: "subject-001", type: "evidence-record", identifier: "mutable local path", version: "1"}
assessments: []
last_reviewed: "2026-07-21"
---

# Invalid fixture

The subject identifier is not an absolute HTTP(S) URI.
