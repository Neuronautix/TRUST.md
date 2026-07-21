---
trust_md_version: "0.4"
title: "Append-only assessment lifecycle"
description: "Superseded, withdrawn, and retracted assessment lineages that leave evidence unchanged."
canonical: "https://example.org/examples/lifecycle/trust.md"
license: "CC-BY-4.0"
companions:
  fair: null
produced_by:
  humans:
    - name: "Example Publisher"
      role: "assessment publisher"
  agents: []
governance:
  source_of_truth: "The append-only assessment version chains."
  no_fabricated_citations: true
  review_policy: "Lifecycle records state publication history, not evidence validity."
  correction_policy: "No released assessment version is edited in place."
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
  - series_id: "https://example.org/assessments/supersession-series"
    id: "https://example.org/assessments/supersession-series/versions/1"
    version: "1"
    subject: "subject-001"
    assessed_by: {humans: [], agents: []}
    protocol:
      identifier: "https://example.org/protocols/descriptive"
      version: "1.0"
    assessed_at: "2026-07-20T08:00:00Z"
    review_status: "unreviewed"
    independence: "not-declared"
    status: "active"
    limitations: []
  - series_id: "https://example.org/assessments/supersession-series"
    id: "https://example.org/assessments/supersession-series/versions/2"
    version: "2"
    subject: "subject-001"
    assessed_by: {humans: [], agents: []}
    protocol:
      identifier: "https://example.org/protocols/descriptive"
      version: "1.0"
    assessed_at: "2026-07-21T08:00:00Z"
    review_status: "unreviewed"
    independence: "not-declared"
    status: "superseded"
    supersedes: "https://example.org/assessments/supersession-series/versions/1"
    lifecycle_reason: "This status-only version records that version 1 is replaced within this assessment series."
    limitations: []
  - series_id: "https://example.org/assessments/withdrawal-series"
    id: "https://example.org/assessments/withdrawal-series/versions/1"
    version: "1"
    subject: "subject-001"
    assessed_by: {humans: [], agents: []}
    protocol:
      identifier: "https://example.org/protocols/descriptive"
      version: "1.0"
    assessed_at: "2026-07-20T09:00:00Z"
    review_status: "unreviewed"
    independence: "not-declared"
    status: "active"
    limitations: []
  - series_id: "https://example.org/assessments/withdrawal-series"
    id: "https://example.org/assessments/withdrawal-series/versions/2"
    version: "2"
    subject: "subject-001"
    assessed_by: {humans: [], agents: []}
    protocol:
      identifier: "https://example.org/protocols/descriptive"
      version: "1.0"
    assessed_at: "2026-07-21T09:00:00Z"
    review_status: "unreviewed"
    independence: "not-declared"
    status: "withdrawn"
    supersedes: "https://example.org/assessments/withdrawal-series/versions/1"
    lifecycle_reason: "The declared use is no longer pursued; invalidity is not asserted."
    limitations: []
  - series_id: "https://example.org/assessments/retraction-series"
    id: "https://example.org/assessments/retraction-series/versions/1"
    version: "1"
    subject: "subject-001"
    assessed_by: {humans: [], agents: []}
    protocol:
      identifier: "https://example.org/protocols/descriptive"
      version: "1.0"
    assessed_at: "2026-07-20T10:00:00Z"
    review_status: "unreviewed"
    independence: "not-declared"
    status: "active"
    limitations: []
  - series_id: "https://example.org/assessments/retraction-series"
    id: "https://example.org/assessments/retraction-series/versions/2"
    version: "2"
    subject: "subject-001"
    assessed_by: {humans: [], agents: []}
    protocol:
      identifier: "https://example.org/protocols/descriptive"
      version: "1.0"
    assessed_at: "2026-07-21T10:00:00Z"
    review_status: "unreviewed"
    independence: "not-declared"
    status: "retracted"
    supersedes: "https://example.org/assessments/retraction-series/versions/1"
    lifecycle_reason: "The publisher explicitly repudiates the assessment conclusion."
    limitations: []
last_reviewed: "2026-07-21"
---

# Lifecycle belongs to assessments

Supersession, withdrawal, and retraction are append-only assessment events.
The subject remains identified by the same immutable version and acquires no
assessment lifecycle state.
