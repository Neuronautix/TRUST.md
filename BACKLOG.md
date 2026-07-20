# TRUST.md — Backlog (toward v0.3)

Small, independently mergeable items. Defect IDs (D1…) reference
`NEXT_VERSION_PLAN.md` §2; decision IDs (D-00x) reference `DECISIONS.md`.

**Priority:** P1 consistency/validator defects · P2 assessment units &
terminology · P3 separation of evidence support / uncertainty / review status ·
P4 backward-compatible schema evolution · P5 examples & migration ·
P6 interoperability tests.

**Size:** S (≤1 h) · M (≤ half day) · L (≤2 days).
**Agent-suitable:** whether an autonomous agent can complete it without
maintainer judgement (items touching scientific meaning are *No* or *With
review*).

---

## P1 — Consistency and validator defects

### B-001 — Fix band-coverage crash
- **Priority:** P1 · **Size:** S · **Agent-suitable:** Yes
- **Goal:** `check_band_coverage` never raises; bands not ending at 100 produce the W7 warning.
- **Scope:** `tools/validate.py:123` (`expected_start` → `expected_next`); regression test.
- **Non-goals:** any new validation semantics.
- **Dependencies:** none (B-003 for the test harness, or ship an inline test).
- **Acceptance:** bands `0-29/30-49/50-69/70-90` → warning "do not end at 100", exit code 0; no traceback.

### B-002 — Accept single-point bands
- **Priority:** P1 · **Size:** S · **Agent-suitable:** Yes
- **Goal:** `"100-100"` is a valid band (`lo == hi` allowed; only `lo > hi` malformed).
- **Scope:** `check_band_coverage`; SPEC §7 wording if it implies otherwise; tests.
- **Non-goals:** changing band-count rules.
- **Dependencies:** B-001.
- **Acceptance:** `0-99` + `100-100` → full coverage, no warnings; `50-40` still malformed.

### B-003 — Bootstrap pytest suite + fixtures
- **Priority:** P1 · **Size:** M · **Agent-suitable:** Yes
- **Goal:** `tests/` with fixture-driven cases per NEXT_VERSION_PLAN §10 items 1, 5, 6.
- **Scope:** pytest config; fixtures for pass/warn/error; helper that runs CLI *and* schema on every fixture and compares verdicts.
- **Non-goals:** v0.3 features; CI wiring (B-004).
- **Dependencies:** B-001, B-002.
- **Acceptance:** `pytest` green locally; a deliberately drifted fixture demonstrates the agreement check fails loudly.

### B-004 — CI: run schema + tests, dedupe example loop
- **Priority:** P1 · **Size:** S · **Agent-suitable:** Yes
- **Goal:** CI runs pytest and `jsonschema` validation of all examples; remove the duplicated reference-example step (D9).
- **Scope:** `.github/workflows/validate.yml`; pin `jsonschema` dependency.
- **Non-goals:** release automation.
- **Dependencies:** B-003.
- **Acceptance:** CI fails on either CLI or schema divergence; each example validated exactly once per method.

### B-005 — Fix README 30-second example (D3, D4, D6)
- **Priority:** P1 · **Size:** S · **Agent-suitable:** Yes
- **Goal:** README example is schema-valid and version-consistent.
- **Scope:** `TRUST_md_version` → `trust_md_version: "0.2"`; `average_` → `average_trust`; "complete v0.1 specification" → version-neutral wording; fix `examples/neuronautix.TRUST.md` link casing.
- **Non-goals:** casing policy (B-009); v0.3 content.
- **Acceptance:** extracted README front matter passes schema + CLI in a test (add to B-003 fixtures).

### B-006 — Purge v0.1 wording drift in template, example, validator (D4)
- **Priority:** P1 · **Size:** S · **Agent-suitable:** Yes
- **Goal:** every self-referential version string matches the file's declared version.
- **Scope:** template prose + changelog stub; example header/prose/changelog (add v0.2 entry); `validate.py` docstring and Rule 4 comment; SPEC §5.1 allowed-values list (`"0.1"` → `"0.1" | "0.2"`).
- **Non-goals:** new spec content.
- **Acceptance:** `grep -rn 'v0\.1'` returns only historical-changelog and back-compat-statement hits.

### B-007 — Release/tag hygiene (D5)
- **Priority:** P1 · **Size:** S · **Agent-suitable:** No (requires maintainer force-retag on GitHub)
- **Goal:** `v0.2` tag points at a tree that says v0.2; CHANGELOG links resolve.
- **Scope:** re-tag `v0.2` at `9e38fc6` (or document the discrepancy in the release notes if retagging is unwanted); create `v0.1` tag at `08f39e8`-era commit or drop the `[0.1]` link.
- **Non-goals:** publishing any new release.
- **Acceptance:** `git show v0.2:SPEC.md` says v0.2; no dead CHANGELOG links.

### B-008 — Reconcile scale-adjustability wording (D11)
- **Priority:** P1 · **Size:** S · **Agent-suitable:** With review
- **Goal:** README stops promising an adjustable scale the schema forbids.
- **Scope:** README step 3: bands' labels/meanings adjustable, range fixed at [0,100].
- **Acceptance:** README, SPEC, schema make identical claims about what may vary.

### B-009 — Canonical casing & discovery text (D7, decision D-008)
- **Priority:** P1 · **Size:** M · **Agent-suitable:** No (needs D-008 accepted)
- **Goal:** one documented rule for repo filename (`TRUST.md`), served path (`/trust.md`, case-insensitive recommended), discovery order; all prose aligned, coordinated with FAIR.md.
- **Scope:** SPEC §3, README, template comments.
- **Dependencies:** D-008 accepted.
- **Acceptance:** no remaining URL/filename casing contradictions (greppable).

## P2 — Assessment units and terminology

### B-014 — SPEC v0.3 draft: "assessment units" section
- **Priority:** P2 · **Size:** M · **Agent-suitable:** With review
- **Goal:** normative text for the four units (repository, artifact, claim, claim–evidence) per plan §6, incl. the external-records boundary and `companions.claim_records`.
- **Non-goals:** claim-record file format.
- **Dependencies:** D-003 accepted.
- **Acceptance:** each unit has: definition, where it lives, conformance impact; explicit "no per-citation assessment" rule.

### B-015 — SPEC v0.3 draft: principles section
- **Priority:** P2 · **Size:** M · **Agent-suitable:** With review
- **Goal:** the ten normative principles (plan §5.2) as spec text.
- **Dependencies:** none (text already agreed in plan).
- **Acceptance:** all ten present with MUST/MUST NOT phrasing; "not a probability" appears in SPEC, README, and template.

### B-016 — Rewrite band meanings (D10)
- **Priority:** P2 · **Size:** S · **Agent-suitable:** No (scientific meaning; needs maintainer + methodology input)
- **Goal:** band meanings describe evidence support only; no category vocabulary; independence claim becomes true.
- **Scope:** SPEC, template, README example, reference example.
- **Dependencies:** D-001 direction accepted.
- **Acceptance:** a `view` at 85 and a `cited` at 20 are both expressible without contradicting any band meaning.

## P3 — Separated dimensions

### B-017 — SPEC v0.3 draft: optional `dimensions` + `assessment` blocks
- **Priority:** P3 · **Size:** L · **Agent-suitable:** No (scientific meaning)
- **Goal:** normative text for `evidence_support`, `review_status`, `calibration`, and the `assessment` provenance block (plan §5.1), incl. missing-data semantics (D-004) and supersession.
- **Dependencies:** D-001, D-002, D-004, D-005 accepted.
- **Acceptance:** every enum value has a one-line definition; absent/not-assessed/not-applicable/lowest-level are four distinct documented states; agent agreement capped at `agent-reviewed`.

### B-018 — Deprecate `average_trust`; add distribution summaries
- **Priority:** P3 · **Size:** M · **Agent-suitable:** With review
- **Goal:** `corpus.band_distribution` + `corpus.median_band` specified; `average_trust` marked deprecated (still valid); validator emits deprecation notice.
- **Dependencies:** D-002 accepted.
- **Acceptance:** v0.3 example with distributions and no mean passes with zero warnings; v0.2 example with `average_trust` passes with a notice, not a warning.

## P4 — Backward-compatible schema evolution

### B-010 — Versioned schema layout
- **Priority:** P4 (enables P1 fixes to land cleanly) · **Size:** M · **Agent-suitable:** Yes
- **Goal:** `schema/v0.1/`, `schema/v0.2/`, `schema/v0.3/trust.schema.json`; frozen historical schemas; resolvable raw-URL `$id` (D12).
- **Acceptance:** validator selects schema by declared version; old examples validate against their own schema.

### B-011 — Single severity source of truth (D8a–D8g)
- **Priority:** P4 · **Size:** L · **Agent-suitable:** With review
- **Goal:** every rule has exactly one severity, identical in SPEC table, schema, and CLI; CLI gains the schema-only checks (or explicitly delegates by running the schema itself).
- **Scope:** decide per-rule: string-typed version (schema wins), ORCID format (warning in CLI, pattern kept), `average_trust` bounds (pick one severity), band-range charset (pick hyphen-only or accept en-dash in both).
- **Dependencies:** B-003, B-010.
- **Acceptance:** the B-003 agreement test passes over the full fixture corpus.

### B-012 — Extensibility fix: remove `additionalProperties: false` (D8c)
- **Priority:** P4 · **Size:** S · **Agent-suitable:** Yes
- **Goal:** category entries, artifact entries, `confidence_scale`, `produced_by` accept unknown keys (e.g. `eco:`); known keys stay typed.
- **Dependencies:** B-010.
- **Acceptance:** fixture with `eco: "ECO:0000204"` on a category passes schema + CLI.

### B-013 — Unknown-version and unknown-field policy in validator
- **Priority:** P4 · **Size:** M · **Agent-suitable:** Yes
- **Goal:** distinct "unsupported version" error; must-ignore for unknown fields with info-level notice; `x_` prefix documented.
- **Dependencies:** D-009 accepted; B-010.
- **Acceptance:** plan §10 test families 3 and 11 pass.

## P5 — Examples and migration

### B-019 — Back-compat fixture corpus from git history
- **Priority:** P5 · **Size:** S · **Agent-suitable:** Yes
- **Goal:** the exact v0.1- and v0.2-era example files preserved as permanent fixtures.
- **Acceptance:** plan §10 family 9 passes.

### B-020 — v0.3 worked example without numeric aggregate
- **Priority:** P5 · **Size:** M · **Agent-suitable:** With review
- **Goal:** `examples/` entry using categories + dimensions, no `data-trust`-style numbers, no `average_trust`.
- **Dependencies:** B-017, B-018.
- **Acceptance:** passes with zero warnings; referenced from README.

### B-021 — MIGRATION.md (v0.2 → v0.3)
- **Priority:** P5 · **Size:** M · **Agent-suitable:** With review
- **Goal:** "no mandatory edits" statement; opt-in checklist; before/after pairs doubling as fixtures (plan §10 family 10).
- **Dependencies:** B-017, B-018.
- **Acceptance:** every pair validates; doc linked from README and CHANGELOG.

### B-025 — Maintain the dimensions-preview example
- **Priority:** P5 · **Size:** S · **Agent-suitable:** Yes
- **Goal:** `examples/dimensions-preview.trust.md` (v0.2-conformant via `x_` extension fields) stays green in CI and in sync with the D-012 dimension vocabulary; promoted to a native v0.3 example when B-017 lands.
- **Scope:** the example file; CI already covers it via the `examples/*` loop.
- **Non-goals:** spec or schema changes; inventing real assessment data (all numbers stay labelled illustrative).
- **Dependencies:** D-012 direction; supersedes nothing; feeds B-020.
- **Acceptance:** CLI exit 0 with zero warnings; schema-valid; every dimension level used at least once, incl. `not-assessed` vs `not-applicable` vs absent.

## P6 — Interoperability

### B-022 — TRUST-Knowledge mapping doc
- **Priority:** P6 · **Size:** M · **Agent-suitable:** No (cross-repo semantics)
- **Goal:** written mapping: template's `TRUST_score`/rubric → `assessment.protocol` + `review_status`; explicit "scores are not copied into `confidence`" rule.
- **Acceptance:** doc reviewed by the template's maintainer; no equivalence claimed beyond the mapping.

### B-023 — PROV mapping sketch (non-normative)
- **Priority:** P6 · **Size:** M · **Agent-suitable:** With review
- **Goal:** non-normative appendix mapping `produced_by`/`assessed_by` to prov:Agent/prov:Activity; spec wording downgraded to "informed by" until then.
- **Acceptance:** appendix exists or all "aligns with PROV" claims are softened — no third state.

### B-024 — Export round-trip test (protocol preservation)
- **Priority:** P6 · **Size:** M · **Agent-suitable:** Yes
- **Goal:** test that a serialised export of TRUST.md fields carries `trust_md_version` + `assessment.protocol`, so a consumer (e.g. ORAtlas, when public) cannot silently reinterpret fields as native criteria.
- **Dependencies:** B-017.
- **Acceptance:** plan §10-adjacent test asserting protocol identifiers survive export.
