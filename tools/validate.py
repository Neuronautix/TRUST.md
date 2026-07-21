#!/usr/bin/env python3
"""Validate TRUST.md declarations using the schema for their declared version."""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys
from typing import Any

try:
    import yaml
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError as exc:  # pragma: no cover - exercised by installation only
    print(f"Dependency missing ({exc.name}). Run: pip install pyyaml jsonschema")
    raise SystemExit(2)


ROOT = Path(__file__).resolve().parents[1]
SUPPORTED_VERSIONS = ("0.1", "0.2", "0.3")
SCHEMAS = {
    version: ROOT / "schema" / f"v{version}" / "trust.schema.json"
    for version in SUPPORTED_VERSIONS
}
CANONICAL_BANDS = ("speculative", "tentative", "moderate", "high", "very-high")
REVIEW_ORDER = {
    "unreviewed": 0,
    "agent-reviewed": 1,
    "human-reviewed": 2,
    "adjudicated": 3,
}


def split_front_matter(text: str) -> tuple[str | None, str]:
    """Return YAML and prose sections from a Markdown front-matter document."""
    match = re.match(r"^-{3}[ \t]*\n(.*?)\n-{3}[ \t]*\n?(.*)", text.lstrip("\ufeff"), re.S)
    return (match.group(1), match.group(2)) if match else (None, text)


def _path(error: Any) -> str:
    return ".".join(str(part) for part in error.absolute_path) or "<root>"


def _schema(version: str) -> dict[str, Any]:
    with SCHEMAS[version].open(encoding="utf-8") as stream:
        return json.load(stream)


def _unknown_notices(instance: Any, schema: dict[str, Any], path: str = "") -> list[str]:
    """Report visible unknown keys without changing their conformance status."""
    if not isinstance(instance, dict) or schema.get("type") != "object":
        return []
    known = schema.get("properties", {})
    if isinstance(schema.get("additionalProperties"), dict) and not known:
        return []
    notices: list[str] = []
    for key, value in instance.items():
        child_path = f"{path}.{key}" if path else key
        if key not in known:
            if not key.startswith("x_"):
                notices.append(f"unknown field ignored: {child_path}")
            continue
        child_schema = known[key]
        if "$ref" not in child_schema:
            notices.extend(_unknown_notices(value, child_schema, child_path))
    return notices


def _parse_range(value: Any) -> tuple[int, int] | None:
    match = re.fullmatch(r"(\d+)-(\d+)", str(value))
    return (int(match.group(1)), int(match.group(2))) if match else None


def _check_v03(data: dict[str, Any], errors: list[str], warnings: list[str], notices: list[str]) -> None:
    model = data.get("epistemic_model") or {}
    bands = model.get("support_bands") or []
    ids = tuple(band.get("id") for band in bands if isinstance(band, dict))
    if ids and ids != CANONICAL_BANDS:
        errors.append("epistemic_model.support_bands must use canonical ids in ascending support order")

    confidence = model.get("confidence_scale")
    ranges = [_parse_range(band.get("range")) for band in bands if isinstance(band, dict)]
    if confidence is not None:
        if any(item is None for item in ranges):
            errors.append("each support band needs a numeric range when confidence_scale is present")
        elif ranges:
            expected = 0
            for low, high in ranges:
                if low > high:
                    errors.append(f"single band has descending range: {low}-{high}")
                    break
                if low != expected:
                    errors.append(f"support-band ranges are not contiguous at {low}-{high}")
                    break
                expected = high + 1
            if expected != 101:
                errors.append("support-band ranges must cover 0-100 exactly")
        if confidence.get("not_probability") is not True:
            warnings.append("confidence_scale.not_probability should be true")

    corpus = data.get("corpus") or {}
    if "average_trust" in corpus:
        notices.append("corpus.average_trust is deprecated; prefer band_distribution")
    distribution = corpus.get("band_distribution")
    total = corpus.get("total_claims")
    if isinstance(distribution, dict) and isinstance(total, int):
        if sum(distribution.values()) != total:
            warnings.append("corpus.band_distribution counts do not sum to total_claims")
        expected_median = _median_band(distribution)
        if corpus.get("median_band") and corpus["median_band"] != expected_median:
            errors.append(
                f"corpus.median_band must be {expected_median!r} under the conservative tie rule"
            )

    assessment = data.get("assessment")
    if not isinstance(assessment, dict):
        return
    status = assessment.get("review_status")
    assessors = assessment.get("assessed_by") or {}
    humans = assessors.get("humans") or []
    agents = assessors.get("agents") or []
    if REVIEW_ORDER.get(status, 0) > 0:
        if not humans and not agents:
            errors.append("reviewed assessment requires an identifiable assessor")
        if not str(assessment.get("protocol", "")).strip():
            errors.append("reviewed assessment requires a non-empty protocol")
        if not assessment.get("date"):
            errors.append("reviewed assessment requires a date")
    if status in {"human-reviewed", "adjudicated"} and not humans:
        errors.append(f"{status} requires an identifiable human assessor")
    if status == "adjudicated":
        if not assessment.get("disagreement") or not assessment.get("resolution"):
            errors.append("adjudicated requires disagreement and resolution references")
    if assessment.get("unit") == "claim-evidence" and not (data.get("companions") or {}).get("claim_records"):
        errors.append("claim-evidence assessments require companions.claim_records")
    if assessment.get("independent_review") is True:
        producers = {
            person.get("name", "").strip().casefold()
            for person in (data.get("produced_by") or {}).get("humans", [])
        }
        reviewers = {
            person.get("name", "").strip().casefold()
            for person in humans
        }
        if not reviewers or reviewers <= producers:
            errors.append("independent_review requires a named human not listed in produced_by.humans")


def _median_band(distribution: dict[str, int]) -> str | None:
    """Return the lower-support middle band for an even-sized population."""
    count = sum(distribution.get(band, 0) for band in CANONICAL_BANDS)
    if not count:
        return None
    lower_position = (count - 1) // 2
    seen = 0
    for band in CANONICAL_BANDS:
        seen += distribution.get(band, 0)
        if lower_position < seen:
            return band
    return None


def validate(path: str | Path) -> tuple[list[str], list[str], list[str]]:
    """Return errors, warnings, and notices for one TRUST.md file."""
    errors: list[str] = []
    warnings: list[str] = []
    notices: list[str] = []
    path = Path(path)
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return [f"cannot read UTF-8 file: {exc}"], warnings, notices

    yaml_text, prose = split_front_matter(text)
    if yaml_text is None:
        return ["no YAML front matter found"], warnings, notices
    try:
        data = yaml.safe_load(yaml_text)
    except yaml.YAMLError as exc:
        return [f"YAML parse error: {exc}"], warnings, notices
    if not isinstance(data, dict):
        return ["front matter must be a mapping"], warnings, notices
    if not prose.strip():
        errors.append("human-readable Markdown prose is required")

    version = data.get("trust_md_version")
    if not isinstance(version, str):
        return errors + ["trust_md_version must be a quoted string"], warnings, notices
    if version not in SUPPORTED_VERSIONS:
        return errors + [f"unsupported version: {version}"], warnings, notices

    schema = _schema(version)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    for error in sorted(validator.iter_errors(data), key=lambda item: list(item.absolute_path)):
        errors.append(f"{_path(error)}: {error.message}")
    notices.extend(_unknown_notices(data, schema))

    if version == "0.3":
        _check_v03(data, errors, warnings, notices)
    return errors, warnings, notices


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if len(argv) > 1:
        print("Usage: python tools/validate.py [path/to/TRUST.md]", file=sys.stderr)
        return 2
    path = argv[0] if argv else "TRUST.md"
    errors, warnings, notices = validate(path)
    for label, messages in (("ERROR", errors), ("WARNING", warnings), ("NOTICE", notices)):
        for message in messages:
            print(f"[{label}] {message}")
    if errors:
        print(f"FAIL: {len(errors)} error(s), {len(warnings)} warning(s), {len(notices)} notice(s)")
        return 1
    print(f"PASS: {len(warnings)} warning(s), {len(notices)} notice(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
