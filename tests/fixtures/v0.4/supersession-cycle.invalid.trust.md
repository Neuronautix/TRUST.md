---
trust_md_version: "0.4"
title: "Supersession cycle"
description: "An intentionally invalid append-only lifecycle fixture."
canonical: "https://example.org/fixtures/supersession-cycle/trust.md"
license: "CC-BY-4.0"
companions: {fair: null}
produced_by: {humans: [{name: "Fixture Author", role: "author"}], agents: []}
governance:
  source_of_truth: "The fixture."
  no_fabricated_citations: true
  review_policy: "No review is claimed."
  correction_policy: "Supersession must be acyclic."
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
  - {id: "subject-001", type: "evidence-record", identifier: "https://example.org/evidence/fixture", version: "1"}
assessments:
  - series_id: "https://example.org/assessments/cycle"
    id: "https://example.org/assessments/cycle/versions/1"
    version: "1"
    subject: "subject-001"
    assessed_by: {humans: [], agents: []}
    protocol: {identifier: "https://example.org/protocols/fixture", version: "1"}
    assessed_at: "2026-07-21T10:00:00Z"
    review_status: "unreviewed"
    independence: "not-declared"
    status: "active"
    supersedes: "https://example.org/assessments/cycle/versions/2"
    limitations: []
  - series_id: "https://example.org/assessments/cycle"
    id: "https://example.org/assessments/cycle/versions/2"
    version: "2"
    subject: "subject-001"
    assessed_by: {humans: [], agents: []}
    protocol: {identifier: "https://example.org/protocols/fixture", version: "1"}
    assessed_at: "2026-07-21T11:00:00Z"
    review_status: "unreviewed"
    independence: "not-declared"
    status: "active"
    supersedes: "https://example.org/assessments/cycle/versions/1"
    limitations: []
last_reviewed: "2026-07-21"
---

# Invalid fixture

Each assessment version supersedes the other, creating a cycle.
