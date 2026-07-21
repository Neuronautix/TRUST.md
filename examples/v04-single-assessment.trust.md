---
trust_md_version: "0.4"
title: "One contextual assessment"
description: "A neutral evidence record linked to one purpose-bound assessment."
canonical: "https://example.org/examples/single-assessment/trust.md"
license: "CC-BY-4.0"
companions:
  fair: null
produced_by:
  humans:
    - name: "Example Publisher"
      role: "metadata publisher"
  agents: []
governance:
  source_of_truth: "The versioned evidence and assessment records."
  no_fabricated_citations: true
  review_policy: "Human review requires named provenance and an inspectable basis."
  correction_policy: "Assessment corrections create append-only versions."
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
assessments:
  - series_id: "https://example.org/assessments/series-001"
    id: "https://example.org/assessments/series-001/versions/1"
    version: "1"
    subject: "subject-001"
    purpose: "Inclusion in a declared evidence synthesis"
    fitness_for_purpose: "suitable"
    dimensions:
      evidence_support: "direct"
      calibration: "matched"
      source_integrity: "verified"
    numeric_refinement:
      value: 85
      not_probability: true
    assessed_by:
      humans:
        - name: "Reviewer One"
          role: "reviewer"
      agents: []
    protocol:
      identifier: "https://example.org/protocols/synthesis-review"
      version: "1.0"
    evidence_basis:
      - relation: "uses-qc-report"
        identifier: "https://example.org/qc/record-001"
    assessed_at: "2026-07-21T10:00:00Z"
    review_status: "human-reviewed"
    independence: "declared-independent"
    status: "active"
    limitations:
      - "Suitability applies only to the declared synthesis."
x_reuse_metrics:
  reuse_count: 12
  measured_at: "2026-07-21T10:05:00Z"
  source: "https://example.org/metrics/record-001"
last_reviewed: "2026-07-21"
---

# A contextual assessment

This assessment is suitable only for its declared synthesis. The reuse-count
extension is impact metadata and does not contribute to any assessment
dimension.
