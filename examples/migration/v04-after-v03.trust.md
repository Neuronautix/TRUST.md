---
trust_md_version: "0.4"
title: "v0.4 declaration after explicit migration"
description: "The v0.3 repository assessment migrated into one versioned assessment."
canonical: "https://example.org/migration/v04/trust.md"
license: "CC-BY-4.0"
companions:
  fair: null
produced_by:
  humans:
    - name: "Example Author"
      role: "author"
  agents: []
governance:
  source_of_truth: "The immutable v0.3 source and the user-supplied migration records."
  no_fabricated_citations: true
  review_policy: "A named human reviews the declaration."
  correction_policy: "Assessment corrections create append-only versions."
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
subjects:
  - id: "subject-001"
    type: "repository"
    identifier: "https://example.org/migration/v03/trust.md"
    version: "v0.3-source"
assessments:
  - series_id: "https://example.org/assessments/migrated-repository-review"
    id: "https://example.org/assessments/migrated-repository-review/versions/1"
    version: "1"
    subject: "subject-001"
    dimensions:
      evidence_support: "direct"
      calibration: "matched"
      source_integrity: "verified"
    assessed_by:
      humans:
        - name: "Example Reviewer"
          role: "reviewer"
      agents: []
    protocol:
      identifier: "https://example.org/protocols/repository-declaration-review"
      version: "1.0"
    evidence_basis:
      - relation: "informed-by"
        identifier: "https://example.org/migration/v03/trust.md"
    assessed_at: "2026-07-21T00:00:00Z"
    assessed_at_precision: "date"
    review_status: "human-reviewed"
    independence: "declared-independent"
    status: "active"
    summary:
      scope: "assessment"
      band_distribution: {speculative: 0, tentative: 0, moderate: 0, high: 1, very-high: 1}
      median_band: "high"
    limitations:
      - "The source recorded only day precision for the assessment date."
x_migration:
  source: "https://example.org/migration/v03/trust.md"
  source_version: "0.3"
  legacy_protocol_text: "Repository declaration review"
  legacy_average_trust: 80
  legacy_summary_population:
    unit: "claims"
    count: 2
    source_scope: "corpus"
  supplied_fields:
    - "subject version"
    - "assessment identifiers"
    - "protocol identifier and version"
    - "evidence basis"
limitations:
  - "Migration preserved the v0.3 source rather than rewriting it."
last_reviewed: "2026-07-21"
---

# Explicit migration result

The singular v0.3 assessment becomes one item in `assessments`. Review status
moves to provenance, dimensions become assessment-scoped, and the day-only date
retains its original precision. The copied distribution records its original
two-claim corpus population explicitly. No fitness conclusion was invented.
