---
trust_md_version: "0.4"
title: "Provenance round-trip fixture"
description: "A type-sensitive assessment provenance record."
canonical: "https://example.org/fixtures/provenance/trust.md"
license: "CC-BY-4.0"
companions: {fair: null}
produced_by:
  humans: [{name: "Fixture Author", role: "author"}]
  agents: []
governance:
  source_of_truth: "The fixture."
  no_fabricated_citations: true
  review_policy: "Adjudication is human-attributable."
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
  - id: "subject-snapshot"
    type: "evidence-record"
    identifier: "https://example.org/evidence/fixture-snapshot"
    snapshot:
      identifier: "https://example.org/snapshots/fixture-snapshot"
      digest:
        algorithm: "sha-256"
        value: "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
assessments:
  - series_id: "https://example.org/assessments/roundtrip"
    id: "https://example.org/assessments/roundtrip/versions/1"
    version: "1"
    subject: "subject-snapshot"
    purpose: "Round-trip conformance testing"
    fitness_for_purpose: "conditionally-suitable"
    conditions: ["Preserve every declared scalar and collection type."]
    dimensions:
      evidence_support: "partial"
      calibration: "matched"
      source_integrity: "verified"
    numeric_refinement: {value: 60, not_probability: true}
    assessed_by:
      humans:
        - name: "Fixture Reviewer"
          role: "adjudicator"
          orcid: "0000-0002-1825-0097"
      agents:
        - name: "Fixture Agent"
          role: "assistant"
          oversight: "human-reviewed"
    protocol:
      identifier: "https://example.org/protocols/roundtrip"
      version: "1.0"
    evidence_basis:
      - relation: "derived-from"
        identifier: "https://example.org/basis/roundtrip"
        version: "1"
    assessed_at: "2026-07-21T11:00:00+02:00"
    assessed_at_precision: "datetime"
    review_status: "adjudicated"
    independence: "declared-partially-independent"
    status: "active"
    disagreement: "https://example.org/disagreements/roundtrip"
    resolution: "https://example.org/resolutions/roundtrip"
    summary:
      scope: "assessment"
      band_distribution: {speculative: 0, tentative: 0, moderate: 1, high: 1, very-high: 0}
      median_band: "moderate"
    limitations: ["This fixture demonstrates structure, not scientific validity."]
    x_protocol_parameters:
      threshold: 0.75
      enabled: true
      labels: ["alpha", "beta"]
last_reviewed: "2026-07-21"
---

# Provenance round trip

The parsed front matter must serialize and parse again without type loss.
