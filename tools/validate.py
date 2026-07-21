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
SUPPORTED_VERSIONS = ("0.1", "0.2", "0.3", "0.4")
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


def _resolve_local_ref(schema: dict[str, Any], root_schema: dict[str, Any]) -> dict[str, Any]:
    """Resolve a local JSON Pointer used by the bundled schemas."""
    reference = schema.get("$ref")
    if not isinstance(reference, str) or not reference.startswith("#/"):
        return schema
    target: Any = root_schema
    for token in reference[2:].split("/"):
        token = token.replace("~1", "/").replace("~0", "~")
        if not isinstance(target, dict) or token not in target:
            return schema
        target = target[token]
    return target if isinstance(target, dict) else schema


def _unknown_notices(
    instance: Any,
    schema: dict[str, Any],
    path: str = "",
    root_schema: dict[str, Any] | None = None,
) -> list[str]:
    """Report unknown nested keys without changing conformance status."""
    root_schema = schema if root_schema is None else root_schema
    schema = _resolve_local_ref(schema, root_schema)

    if isinstance(instance, list):
        item_schema = schema.get("items")
        if not isinstance(item_schema, dict):
            return []
        notices: list[str] = []
        for index, value in enumerate(instance):
            child_path = f"{path}[{index}]" if path else f"[{index}]"
            notices.extend(
                _unknown_notices(value, item_schema, child_path, root_schema)
            )
        return notices

    if not isinstance(instance, dict):
        return []

    known = schema.get("properties", {})
    if not isinstance(known, dict):
        known = {}
    additional = schema.get("additionalProperties", True)
    notices = []
    for key, value in instance.items():
        child_path = f"{path}.{key}" if path else key
        child_schema = known.get(key)
        if isinstance(child_schema, dict):
            notices.extend(
                _unknown_notices(value, child_schema, child_path, root_schema)
            )
            continue
        if isinstance(additional, dict):
            # Dynamic keys are defined by their value schema, for example
            # category distributions and additional companion paths.
            notices.extend(
                _unknown_notices(value, additional, child_path, root_schema)
            )
        elif not key.startswith("x_"):
            notices.append(f"unknown field ignored: {child_path}")
    return notices


def _parse_range(value: Any) -> tuple[int, int] | None:
    match = re.fullmatch(r"(\d+)-(\d+)", str(value))
    return (int(match.group(1)), int(match.group(2))) if match else None


def _check_support_model(
    data: dict[str, Any], errors: list[str], warnings: list[str]
) -> None:
    model = data.get("epistemic_model") or {}
    if not isinstance(model, dict):
        return
    bands = model.get("support_bands") or []
    if not isinstance(bands, list):
        return
    ids = tuple(band.get("id") for band in bands if isinstance(band, dict))
    if ids and ids != CANONICAL_BANDS:
        errors.append("epistemic_model.support_bands must use canonical ids in ascending support order")

    confidence = model.get("confidence_scale")
    ranges = [_parse_range(band.get("range")) for band in bands if isinstance(band, dict)]
    if isinstance(confidence, dict):
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


def _check_v03(data: dict[str, Any], errors: list[str], warnings: list[str], notices: list[str]) -> None:
    _check_support_model(data, errors, warnings)

    corpus = data.get("corpus") or {}
    if not isinstance(corpus, dict):
        corpus = {}
    if "average_trust" in corpus:
        notices.append("corpus.average_trust is deprecated; prefer band_distribution")
    distribution = corpus.get("band_distribution")
    total = corpus.get("total_claims")
    if isinstance(distribution, dict) and isinstance(total, int):
        counts = tuple(distribution.values())
        if all(isinstance(value, int) and not isinstance(value, bool) for value in counts) and sum(counts) != total:
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
    if isinstance(assessors, dict):
        humans = assessors.get("humans") or []
        agents = assessors.get("agents") or []
    else:
        humans = []
        agents = []
    if isinstance(status, str) and REVIEW_ORDER.get(status, 0) > 0:
        if not humans and not agents:
            errors.append("reviewed assessment requires an identifiable assessor")
        if not str(assessment.get("protocol", "")).strip():
            errors.append("reviewed assessment requires a non-empty protocol")
        if not assessment.get("date"):
            errors.append("reviewed assessment requires a date")
    if isinstance(status, str) and status in {"human-reviewed", "adjudicated"} and not humans:
        errors.append(f"{status} requires an identifiable human assessor")
    if status == "adjudicated":
        if not assessment.get("disagreement") or not assessment.get("resolution"):
            errors.append("adjudicated requires disagreement and resolution references")
    if assessment.get("unit") == "claim-evidence" and not (data.get("companions") or {}).get("claim_records"):
        errors.append("claim-evidence assessments require companions.claim_records")
    if assessment.get("independent_review") is True:
        produced_by = data.get("produced_by") or {}
        producers = _person_names(
            produced_by.get("humans") or []
            if isinstance(produced_by, dict)
            else []
        )
        reviewers = _person_names(humans)
        if not reviewers or reviewers <= producers:
            errors.append("independent_review requires a named human not listed in produced_by.humans")


def _replace_notice(notices: list[str], old: str, new: str) -> None:
    """Replace one generic ignored-field notice with a specific diagnostic."""
    if old in notices:
        notices.remove(old)
    if new not in notices:
        notices.append(new)


def _person_names(people: Any) -> set[str]:
    """Return normalized, non-empty names from structurally valid people."""
    if not isinstance(people, list):
        return set()
    names: set[str] = set()
    for person in people:
        if not isinstance(person, dict):
            continue
        name = person.get("name")
        if isinstance(name, str) and name.strip():
            names.add(name.strip().casefold())
    return names


def _check_v04(
    data: dict[str, Any], errors: list[str], warnings: list[str], notices: list[str]
) -> None:
    """Enforce v0.4 relationships that JSON Schema cannot express locally."""
    _check_support_model(data, errors, warnings)

    model = data.get("epistemic_model") or {}
    if isinstance(model, dict) and "dimensions" in model:
        _replace_notice(
            notices,
            "unknown field ignored: epistemic_model.dimensions",
            "epistemic_model.dimensions is a v0.3 field ignored in v0.4; "
            "put dimensions on each assessment",
        )

    if "assessment" in data:
        _replace_notice(
            notices,
            "unknown field ignored: assessment",
            "assessment is a v0.3 field ignored in v0.4; use plural assessments",
        )
        if "assessments" in data:
            errors.append("v0.4 cannot combine singular assessment with plural assessments")

    if "corpus" in data:
        _replace_notice(
            notices,
            "unknown field ignored: corpus",
            "corpus is a v0.3 field ignored in v0.4; use assessment-scoped summary or impact",
        )
        errors.append("v0.4 prohibits top-level aggregation across assessments")

    subjects = data.get("subjects") or []
    if not isinstance(subjects, list):
        subjects = []
    subject_ids: set[str] = set()
    for index, subject in enumerate(subjects):
        if not isinstance(subject, dict):
            continue
        subject_id = subject.get("id")
        if not isinstance(subject_id, str):
            continue
        if subject_id in subject_ids:
            errors.append(f"subjects[{index}].id duplicates {subject_id!r}")
        subject_ids.add(subject_id)

    assessments = data.get("assessments") or []
    if not isinstance(assessments, list):
        assessments = []
    assessment_ids: set[str] = set()
    series_versions: set[tuple[str, str]] = set()
    by_id: dict[str, dict[str, Any]] = {}
    for index, assessment in enumerate(assessments):
        if not isinstance(assessment, dict):
            continue
        assessment_id = assessment.get("id")
        series_id = assessment.get("series_id")
        version = assessment.get("version")
        if isinstance(assessment_id, str):
            if assessment_id in assessment_ids:
                errors.append(f"assessments[{index}].id duplicates {assessment_id!r}")
            assessment_ids.add(assessment_id)
            by_id[assessment_id] = assessment
        if isinstance(series_id, str) and isinstance(version, str):
            identity = (series_id, version)
            if identity in series_versions:
                errors.append(
                    f"assessments[{index}] duplicates series_id/version {identity!r}"
                )
            series_versions.add(identity)
            if assessment_id == series_id:
                errors.append(
                    f"assessments[{index}].id must identify a version, not equal series_id"
                )

        subject = assessment.get("subject")
        if isinstance(subject, str) and subject not in subject_ids:
            errors.append(
                f"assessments[{index}].subject does not resolve to subjects[].id: {subject!r}"
            )

        status = assessment.get("review_status")
        assessors = assessment.get("assessed_by") or {}
        if isinstance(assessors, dict):
            raw_humans = assessors.get("humans") or []
            raw_agents = assessors.get("agents") or []
            humans = raw_humans if isinstance(raw_humans, list) else []
            agents = raw_agents if isinstance(raw_agents, list) else []
        else:
            humans = []
            agents = []
        if isinstance(status, str) and REVIEW_ORDER.get(status, 0) > 0 and not humans and not agents:
            errors.append(f"assessments[{index}] reviewed assessment requires an identifiable assessor")

        independence = assessment.get("independence")
        if isinstance(independence, str) and independence in {
            "declared-partially-independent",
            "declared-independent",
        }:
            producers = data.get("produced_by") or {}
            if isinstance(producers, dict):
                producer_names = _person_names(
                    producers.get("humans") or []
                ) | _person_names(
                    producers.get("agents") or []
                )
            else:
                producer_names = set()
            assessor_names = _person_names(humans) | _person_names(agents)
            if not assessor_names or not (assessor_names - producer_names):
                errors.append(
                    f"assessments[{index}].independence requires an identifiable "
                    "assessor not listed in produced_by"
                )

        dimensions = assessment.get("dimensions") or {}
        if isinstance(dimensions, dict):
            for forbidden in (
                "review_status",
                "reuse_count",
                "citations",
                "downloads",
                "popularity",
            ):
                if forbidden not in dimensions:
                    continue
                path = f"assessments[{index}].dimensions.{forbidden}"
                _replace_notice(
                    notices,
                    f"unknown field ignored: {path}",
                    f"{path} is prohibited and does not affect assessment dimensions",
                )
                errors.append(f"{path} is not a v0.4 quality dimension")

        summary = assessment.get("summary") or {}
        if isinstance(summary, dict) and "average_trust" in summary:
            errors.append(
                f"assessments[{index}].summary.average_trust is prohibited; "
                "v0.4 has no scalar aggregate"
            )
        if isinstance(summary, dict):
            distribution = summary.get("band_distribution")
            median = summary.get("median_band")
            if isinstance(distribution, dict) and median:
                expected_median = _median_band(distribution)
                if median != expected_median:
                    errors.append(
                        f"assessments[{index}].summary.median_band must be "
                        f"{expected_median!r} under the conservative tie rule"
                    )

        if "date" in assessment:
            _replace_notice(
                notices,
                f"unknown field ignored: assessments[{index}].date",
                f"assessments[{index}].date is deprecated and ignored; use assessed_at",
            )
        if assessment.get("assessed_at_precision") == "date":
            assessed_at = assessment.get("assessed_at")
            if isinstance(assessed_at, str) and not assessed_at.endswith("T00:00:00Z"):
                errors.append(
                    f"assessments[{index}] date precision requires a T00:00:00Z serialization anchor"
                )

    edges: dict[str, str] = {}
    warned_targets: set[str] = set()
    for index, assessment in enumerate(assessments):
        if not isinstance(assessment, dict):
            continue
        source = assessment.get("id")
        target = assessment.get("supersedes")
        if not isinstance(source, str) or not isinstance(target, str):
            continue
        if source == target:
            errors.append(f"assessments[{index}].supersedes cannot reference itself")
            continue
        if target not in by_id:
            if target not in warned_targets:
                warnings.append(
                    f"supersession target is not locally inspectable: {target}"
                )
                warned_targets.add(target)
            continue
        if assessment.get("series_id") != by_id[target].get("series_id"):
            errors.append(
                f"assessments[{index}].supersedes must reference the same series_id"
            )
        if assessment.get("subject") != by_id[target].get("subject"):
            errors.append(
                f"assessments[{index}].supersedes must reference the same subject"
            )
        edges[source] = target

    reported_cycle_nodes: set[str] = set()
    for start in edges:
        seen: set[str] = set()
        current = start
        while current in edges:
            if current in seen:
                cycle_nodes = seen - reported_cycle_nodes
                if cycle_nodes:
                    errors.append(
                        f"supersession cycle detected at assessment {current!r}"
                    )
                    reported_cycle_nodes.update(seen)
                break
            seen.add(current)
            current = edges[current]


def _median_band(distribution: Any) -> str | None:
    """Return the lower-support middle band for an even-sized population."""
    if not isinstance(distribution, dict):
        return None
    counts: dict[str, int] = {}
    for band in CANONICAL_BANDS:
        value = distribution.get(band, 0)
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            return None
        counts[band] = value
    count = sum(counts.values())
    if not count:
        return None
    lower_position = (count - 1) // 2
    seen = 0
    for band in CANONICAL_BANDS:
        seen += counts[band]
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
    notices.extend(_unknown_notices(data, schema, root_schema=schema))

    if version == "0.3":
        _check_v03(data, errors, warnings, notices)
    elif version == "0.4":
        _check_v04(data, errors, warnings, notices)
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
