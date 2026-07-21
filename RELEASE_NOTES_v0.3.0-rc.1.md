# TRUST.md v0.3.0-rc.1

This release candidate implements the accepted v0.3 semantic decisions while
preserving v0.1 and v0.2 declarations under frozen schemas.

The central change is honesty about measurement: the five evidence-support
bands are primary. A 0–100 value is optional, ordinal, and explicitly not a
probability. No aggregate is required, and the legacy mean is deprecated in
favor of a band distribution and conservative median.

Four dimensions now remain separate: evidence support, review status,
calibration of wording to evidence, and citation integrity. They are never
summed. Assessment provenance records the unit, assessor, protocol, date, and
independence; human review and adjudication have enforceable declarable
requirements.

## Compatibility

- Existing `"0.1"` and `"0.2"` files continue to validate unchanged.
- Unknown fields and `average_trust` are notices, not errors.
- No file is migrated automatically.
- Existing tags must remain immutable.

## Review this candidate

1. Run `pip install pyyaml jsonschema pytest`.
2. Run `pytest -q`.
3. Validate every example with `python tools/validate.py <file>`.
4. Compare `MODEL.md`, `SPEC.md`, the v0.3 schema, CLI behavior, examples, and
   this release note for exact agreement.
5. Report semantic disagreements before a stable `v0.3.0` release.

This release candidate establishes structural conformance, not scientific
validation. Human scientific assessment remains a separate process.
