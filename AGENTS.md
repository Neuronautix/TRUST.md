# AGENTS.md — TRUST.md convention

## Role and source of authority
TRUST.md is an independent, experimental **assessment/interchange convention**. The current v0.4 model is a release candidate; `SPEC.md` and `MODEL.md` are normative together. The repository does **not** own scientific evidence, certify its truth, determine the universal merit of a publication, or replace its source producer.

## Epistemic and provenance invariants
- Keep exact subject identities (version or immutable snapshot), assessment protocol/version, assessor roles, evidence/basis, review status, limitations and declared independence.
- Multiple assessments may conflict; keep them separate and historically immutable. No averaging into a universal trust score or inferring fitness without a declared purpose.
- Popularity, citations and impact are not proxies for evidential quality. Review status is not automatically scientific confirmation.
- Preserve three-valued and missing states (including *not assessed*) and distinguish structural conformance from scientific validation.
- Preserve exact version-specific field meaning; breaking normative changes need new version identifiers, coexistence/migration tests and attribution.
- Consumers such as ORAtlas may read pinned TRUST records, but cannot silently author, rewrite or reclassify source-native assessments.

## Before editing
Read `README.md`, `SPEC.md`, `MODEL.md`, `CONFORMANCE.md`, `VALIDATION.md`, `DECISIONS.md` and `schema/`.

## Checks
```bash
python -m pip install pyyaml jsonschema pytest
python tools/validate.py TRUST.md
python -m pytest -q
```
Add valid and invalid version-pinned fixtures for contract changes and keep older supported versions working as documented. These checks do not certify scientific correctness or assessor independence.
