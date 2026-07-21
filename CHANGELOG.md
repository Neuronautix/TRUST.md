# Changelog — trust.md specification

All notable changes to the trust.md specification are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
This project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.4.0-rc.1] — 2026-07-21

### Added

- A required subject registry supporting evidence with zero, one, or multiple
  independently versioned assessments.
- Stable assessment series and version IDs, exact subject identity, versioned
  protocols, basis links, purpose-scoped fitness, attributable assessors,
  declared independence, and append-only lifecycle records.
- Coexistence of conflicting assessments without automatic adjudication or
  top-level aggregation.
- Frozen v0.4 schema, exact dispatch, semantic validation, public examples,
  invalid fixtures, provenance round-trip coverage, and an explicit v0.3-to-v0.4
  migration pair.
- Citation metadata, examples index, validator guide, and release-candidate
  notes.

### Changed

- Evidence subjects and assessments are now distinct objects.
- Review status is assessment provenance rather than a quality dimension.
- Assessment time uses an offset ISO datetime; migrated day-only values retain
  precision with `assessed_at_precision: date`.
- The root template now identifies an exact placeholder subject and publishes
  an empty assessment collection.

### Compatibility

- v0.1, v0.2, and v0.3 schemas and semantics remain frozen.
- v0.3 singular assessments are not reinterpreted under plural v0.4 semantics.
- Migration remains explicit and never rewrites the source declaration.

### Safety boundary

- Conformance does not certify evidence, methodological quality, independence,
  reproducibility, or scientific conclusions.
- Citation, download, reuse, prestige, and popularity metrics cannot determine
  assessment dimensions or fitness conclusions.

## [0.3.0-rc.1] — 2026-07-21

### Added

- Primary five-band ordinal evidence-support model and four non-compensatory
  dimensions.
- Assessment-unit, missing-data, review-provenance, adjudication, and
  independence semantics.
- Frozen v0.1/v0.2 schemas, a v0.3 schema, and version-dispatch validation.
- Repository, artifact, ordinal-only, extended, missing-state, migration, and
  external relation examples.
- Normative model, migration guide, and conformance matrix.

### Changed

- The 0–100 integer is now an optional non-probabilistic refinement within an
  ordinal band.
- `band_distribution` is the preferred summary; no aggregate is mandatory.
- Canonical casing is `TRUST.md` in repositories and `/trust.md` on the web.

### Deprecated

- `corpus.average_trust` remains valid but produces a notice.

### Fixed

- Validator crash for incomplete band coverage and rejection of valid
  single-point bands such as `100-100`.
- Schema/CLI version, format, extension, and CI drift.
- Invalid README example, stale v0.1/v0.2 wording, casing, and links.
- Root template no longer contains fictional review provenance or assessment
  results that could be copied as real declarations.
- Versioned schema identifiers are pinned to the immutable rc.1 distribution,
  and unknown-field notices now traverse nested objects and arrays.
- Added an explicit v0.1 fixture and regression test.

## [0.2] — 2026-06-08

### Added

- `tools/validate.py` — standalone Python 3 validator (requires only PyYAML) implementing all 15 MUST rules and 7 WARNING checks from SPEC.md §7, including confidence-band contiguity. Exit code 1 on errors, 0 on warnings-only or clean pass.
- `.github/workflows/validate.yml` — CI workflow that installs PyYAML and runs the validator against all `examples/*.trust.md` on every push and pull request.
- `.gitignore` — excludes `.claude/` tooling artefacts and Python `__pycache__`.

### Changed

- JSON Schema (`schema/trust.schema.json`):
  - `$id` corrected to `Neuronautix/TRUST.md` and versioned to `/blob/v0.2/`.
  - `confidence_scale.range`: now uses `prefixItems` with `const: 0` / `const: 100` to strictly enforce `[0, 100]`.
  - `companions.additionalProperties`: now validates additional companion keys as root-relative paths or `null` (was `true`).
  - `last_reviewed`: added `"format": "date"` hint alongside the regex pattern.
- SPEC.md:
  - Version bumped to v0.2; date updated to 2026-06-08.
  - Validation rule 4: accepts `"0.1"` or `"0.2"` (0.x backward compatibility).
  - §5.1 `companions`: clarified that the object is REQUIRED but `fair` MAY be `null`.
  - §5.1 confidence scale: added community consensus note on band thresholds.
  - §7: added contiguity warning for `confidence_scale.bands`.
- README: status updated to v0.2.
- Template (`TRUST.md`): `trust_md_version` updated to `"0.2"`.

### Fixed

- All internal URLs corrected from `Neuronautix/trust-md` (hyphen) to `Neuronautix/TRUST.md` (dot) across `TRUST.md`, `README.md`, `SPEC.md`, `CHANGELOG.md`, and `schema/trust.schema.json`.
- `FAIR.md` companion link in `README.md` changed from a relative monorepo path to the correct absolute URL `https://github.com/Neuronautix/FAIR.md`.

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

[0.2]: https://github.com/Neuronautix/TRUST.md/releases/tag/v0.2
[0.1]: https://github.com/Neuronautix/TRUST.md/releases/tag/v0.1
[0.3.0-rc.1]: https://github.com/Neuronautix/TRUST.md/releases/tag/v0.3.0-rc.1
[0.4.0-rc.1]: https://github.com/Neuronautix/TRUST.md/releases/tag/v0.4.0-rc.1
