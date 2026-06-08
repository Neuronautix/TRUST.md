# Changelog — trust.md specification

All notable changes to the trust.md specification are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
This project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.1] — 2026-06-06

### Added

- Initial specification (SPEC.md) defining:
  - File location and discovery conventions (`/trust.md`, optional `/.well-known/trust.md` redirect)
  - YAML front-matter format with all required fields: `trust_md_version`, `title`, `description`, `canonical`, `license`, `companions`, `produced_by`, `governance`, `epistemic_model`, `last_reviewed`
  - Recommended fields: `corpus`, `artifacts`, `limitations`
  - `produced_by` structure: `humans` (at least one required) + `agents` (with `oversight` enum: `human-reviewed | human-in-the-loop | automated | none`)
  - `governance` fields: `source_of_truth`, `no_fabricated_citations`, `review_policy`, `correction_policy`, `conflict_of_interest`
  - Five canonical epistemic categories: `cited`, `consensus`, `inference`, `hypothesis`, `view`
  - 0–100 confidence scale with five canonical bands: Very high (90–100), High (70–89), Moderate (50–69), Tentative (30–49), Speculative (0–29)
  - Two-axis independence principle (category and confidence are independent)
  - Corpus and per-artifact profile structure
  - Validation rules and three conformance levels (Conformant, Recommended, Extended)
  - Scope distinction from JournalList trust.txt
  - Alignment table with W3C PROV/PAV, nanopublications, SEPIO, ECO, schema.org ClaimReview
- Template file (`trust.md`) with all fields as `<PLACEHOLDER>` values and inline comments
- Reference implementation example (`examples/neuronautix.trust.md`) — the Neuronautix knowledge base
- JSON Schema (draft 2020-12) for the YAML front matter (`schema/trust.schema.json`)
- README with lineage, 30-second example, and adoption instructions
- LICENSE (Apache-2.0)

[0.1]: https://github.com/Neuronautix/TRUST.md/releases/tag/v0.1
