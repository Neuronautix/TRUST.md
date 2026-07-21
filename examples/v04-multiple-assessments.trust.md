---
trust_md_version: "0.4"
title: "Multiple assessments of one evidence record"
description: "A neutral record with independent, conflicting, human-assisted, and agent-only assessments."
canonical: "https://example.org/examples/multiple-assessments/trust.md"
license: "CC-BY-4.0"
companions:
  fair: null
produced_by:
  humans:
    - name: "Example Publisher"
      role: "metadata publisher"
  agents: []
governance:
  source_of_truth: "The immutable subject and assessment-version records."
  no_fabricated_citations: true
  review_policy: "Each assessment retains its own protocol, purpose, basis, and assessors."
  correction_policy: "Corrections create append-only assessment versions."
  conflict_of_interest: "Assessment disagreements are retained without automatic adjudication."
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
  - series_id: "https://example.org/assessments/community-a"
    id: "https://example.org/assessments/community-a/versions/1"
    version: "1"
    subject: "subject-001"
    purpose: "Inclusion in synthesis S-001"
    fitness_for_purpose: "suitable"
    dimensions:
      evidence_support: "direct"
      calibration: "matched"
      source_integrity: "verified"
    assessed_by:
      humans:
        - name: "Reviewer A"
          role: "independent reviewer"
      agents: []
    protocol:
      identifier: "https://example.org/protocols/community-a"
      version: "2.0"
    evidence_basis:
      - relation: "uses-qc-report"
        identifier: "https://example.org/qc/record-001"
    assessed_at: "2026-07-21T09:00:00Z"
    review_status: "human-reviewed"
    independence: "declared-independent"
    status: "active"
    limitations:
      - "The assessment uses community A's inclusion criteria."
  - series_id: "https://example.org/assessments/community-b"
    id: "https://example.org/assessments/community-b/versions/1"
    version: "1"
    subject: "subject-001"
    purpose: "Inclusion in synthesis S-001"
    fitness_for_purpose: "not-suitable"
    dimensions:
      evidence_support: "partial"
      calibration: "overstated"
      source_integrity: "verified"
    assessed_by:
      humans:
        - name: "Reviewer B"
          role: "independent reviewer"
      agents: []
    protocol:
      identifier: "https://example.org/protocols/community-b"
      version: "1.3"
    evidence_basis:
      - relation: "checked-against"
        identifier: "https://example.org/checklists/community-b-001"
    assessed_at: "2026-07-21T09:15:00Z"
    review_status: "human-reviewed"
    independence: "declared-independent"
    status: "active"
    limitations:
      - "The protocol requires a measurement absent from the subject."
  - series_id: "https://example.org/assessments/exploratory-use"
    id: "https://example.org/assessments/exploratory-use/versions/1"
    version: "1"
    subject: "subject-001"
    purpose: "Exploratory visualization for planning"
    fitness_for_purpose: "conditionally-suitable"
    conditions:
      - "Display the documented missingness alongside every visualization."
    dimensions:
      evidence_support: "indirect"
      calibration: "matched"
      source_integrity: "partially-verified"
    assessed_by:
      humans:
        - name: "Reviewer C"
          role: "confirming reviewer"
      agents:
        - name: "Review Assistant"
          role: "evidence extraction assistant"
          oversight: "human-reviewed"
    protocol:
      identifier: "https://example.org/protocols/exploratory-use"
      version: "1.0"
    evidence_basis:
      - relation: "informed-by"
        identifier: "https://example.org/reports/missingness-001"
    assessed_at: "2026-07-21T09:30:00Z"
    review_status: "human-reviewed"
    independence: "declared-partially-independent"
    status: "active"
    limitations:
      - "Human confirmation covers this assessment version only."
  - series_id: "https://example.org/assessments/agent-screen"
    id: "https://example.org/assessments/agent-screen/versions/1"
    version: "1"
    subject: "subject-001"
    dimensions:
      evidence_support: "not-assessed"
      calibration: "not-assessed"
      source_integrity: "partially-verified"
    assessed_by:
      humans: []
      agents:
        - name: "Screening Agent"
          role: "automated source checker"
          oversight: "automated"
    protocol:
      identifier: "https://example.org/protocols/agent-screen"
      version: "1.0"
    evidence_basis:
      - relation: "checked-against"
        identifier: "https://example.org/source-register/record-001"
    assessed_at: "2026-07-21T09:45:00Z"
    review_status: "agent-reviewed"
    independence: "not-declared"
    status: "active"
    limitations:
      - "This agent-only screen is not human review."
last_reviewed: "2026-07-21"
---

# Multiple assessments remain separate

Communities A and B reach conflicting conclusions for the same purpose, while
another assessment concerns a different exploratory use. None is canonical,
and the declaration contains no aggregate across them. The final assessment is
explicitly agent-only and is not presented as human-reviewed.
