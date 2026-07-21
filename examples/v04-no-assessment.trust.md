---
trust_md_version: "0.4"
title: "Evidence record without an assessment"
description: "A neutral evidence record that has not yet been assessed."
canonical: "https://example.org/examples/no-assessment/trust.md"
license: "CC-BY-4.0"
companions:
  fair: null
produced_by:
  humans:
    - name: "Example Publisher"
      role: "metadata publisher"
  agents: []
governance:
  source_of_truth: "The identified evidence record and its immutable version."
  no_fabricated_citations: true
  review_policy: "Assessments are published only when attributable."
  correction_policy: "Corrections create new immutable records."
  conflict_of_interest: "None declared."
epistemic_model:
  categories:
    - id: "observation"
      label: "Observation"
      definition: "A recorded observation in the identified evidence object."
  support_bands:
    - {id: "speculative", label: "Speculative", meaning: "Little or no direct support."}
    - {id: "tentative", label: "Tentative", meaning: "Limited support."}
    - {id: "moderate", label: "Moderate", meaning: "Partial or indirect support."}
    - {id: "high", label: "High", meaning: "Support with minor interpretation."}
    - {id: "very-high", label: "Very high", meaning: "Direct and verifiable support."}
subjects:
  - id: "subject-001"
    type: "evidence-record"
    identifier: "https://example.org/evidence/record-001"
    version: "1.0"
assessments: []
limitations:
  - "No trust assessment has been published for this subject."
last_reviewed: "2026-07-21"
---

# Evidence without an assessment

The subject registry stands on its own. An empty assessment collection means
that this declaration makes no assessment, not that the evidence was assessed
as low quality.
