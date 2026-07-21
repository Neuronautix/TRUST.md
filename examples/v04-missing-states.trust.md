---
trust_md_version: "0.4"
title: "Missing and assessed-low states"
description: "Absent, not-assessed, not-applicable, and assessed-low dimensions remain distinct."
canonical: "https://example.org/examples/missing-states/trust.md"
license: "CC-BY-4.0"
companions:
  fair: null
produced_by:
  humans:
    - name: "Example Publisher"
      role: "assessment publisher"
  agents: []
governance:
  source_of_truth: "The explicit assessment records."
  no_fabricated_citations: true
  review_policy: "Missing states are never inferred from low values."
  correction_policy: "Corrections create new versions."
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
  - series_id: "https://example.org/assessments/absent-dimension"
    id: "https://example.org/assessments/absent-dimension/versions/1"
    version: "1"
    subject: "subject-001"
    dimensions:
      source_integrity: "verified"
    assessed_by: {humans: [], agents: []}
    protocol: {identifier: "https://example.org/protocols/state-demo", version: "1.0"}
    assessed_at: "2026-07-21T08:00:00Z"
    review_status: "unreviewed"
    independence: "not-declared"
    status: "active"
    limitations:
      - "Evidence support is absent and makes no statement."
  - series_id: "https://example.org/assessments/not-assessed"
    id: "https://example.org/assessments/not-assessed/versions/1"
    version: "1"
    subject: "subject-001"
    dimensions:
      evidence_support: "not-assessed"
      calibration: "not-assessed"
      source_integrity: "not-assessed"
    assessed_by: {humans: [], agents: []}
    protocol: {identifier: "https://example.org/protocols/state-demo", version: "1.0"}
    assessed_at: "2026-07-21T08:15:00Z"
    review_status: "unreviewed"
    independence: "not-declared"
    status: "active"
    limitations: []
  - series_id: "https://example.org/assessments/not-applicable"
    id: "https://example.org/assessments/not-applicable/versions/1"
    version: "1"
    subject: "subject-001"
    purpose: "A use to which calibration does not apply"
    fitness_for_purpose: "not-applicable"
    dimensions:
      evidence_support: "not-applicable"
      calibration: "not-applicable"
      source_integrity: "verified"
    assessed_by: {humans: [], agents: []}
    protocol: {identifier: "https://example.org/protocols/state-demo", version: "1.0"}
    assessed_at: "2026-07-21T08:30:00Z"
    review_status: "unreviewed"
    independence: "not-declared"
    status: "active"
    limitations: []
  - series_id: "https://example.org/assessments/assessed-low"
    id: "https://example.org/assessments/assessed-low/versions/1"
    version: "1"
    subject: "subject-001"
    dimensions:
      evidence_support: "none"
      calibration: "overstated"
      source_integrity: "unverified"
    assessed_by: {humans: [], agents: []}
    protocol: {identifier: "https://example.org/protocols/state-demo", version: "1.0"}
    assessed_at: "2026-07-21T08:45:00Z"
    review_status: "unreviewed"
    independence: "not-declared"
    status: "active"
    limitations:
      - "These are assessed results, not defaults for missing data."
last_reviewed: "2026-07-21"
---

# Four different statements

An absent dimension says nothing. `not-assessed` and `not-applicable` are
explicit missing states. `none`, `overstated`, and `unverified` are ordinary
assessed results and must not be interpreted as missing.
