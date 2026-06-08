#!/usr/bin/env python3
"""Validate a trust.md file against the trust.md specification v0.1.

Usage:
    python tools/validate.py [path/to/trust.md]

If no path is given, defaults to TRUST.md in the current working directory.

Exit codes:
    0 — all MUST rules pass (warnings may still be present)
    1 — one or more MUST rules fail (errors found)
    2 — script usage/dependency error
"""

import sys
import re
import datetime

try:
    import yaml
except ImportError:
    print("PyYAML required: pip install pyyaml")
    sys.exit(2)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

REQUIRED_FIELDS = [
    "trust_md_version",
    "title",
    "description",
    "canonical",
    "license",
    "companions",
    "produced_by",
    "governance",
    "epistemic_model",
    "last_reviewed",
]

VALID_OVERSIGHT_VALUES = {"human-reviewed", "human-in-the-loop", "automated", "none"}

CANONICAL_CATEGORY_IDS = {"cited", "consensus", "inference", "hypothesis", "view"}


def _get(obj, *keys, default=None):
    """Safely drill into nested dicts/lists by key sequence."""
    cur = obj
    for k in keys:
        if isinstance(cur, dict):
            cur = cur.get(k, default)
        else:
            return default
    return cur


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

def split_front_matter(text):
    """Return (yaml_text, prose_text) by splitting on --- delimiters.

    Returns (None, text) if no valid front matter block is found.
    """
    # Front matter must start at the very beginning (ignoring optional BOM)
    pattern = re.compile(r"^-{3}[ \t]*\n(.*?)\n-{3}[ \t]*\n?(.*)", re.DOTALL)
    m = pattern.match(text.lstrip("﻿"))
    if not m:
        return None, text
    return m.group(1), m.group(2)


# ---------------------------------------------------------------------------
# Band coverage helper
# ---------------------------------------------------------------------------

def check_band_coverage(bands):
    """Check that bands contiguously cover [0, 100].

    Each band is expected to have a ``range`` key like "0-20" or "0–20".
    Returns a list of problem strings (empty means OK).
    """
    problems = []
    parsed = []
    dash_re = re.compile(r"^(\d+)\s*[-–]\s*(\d+)$")
    for band in bands:
        r = _get(band, "range")
        if r is None:
            problems.append(f"Band missing 'range' key: {band}")
            continue
        m = dash_re.match(str(r).strip())
        if not m:
            problems.append(f"Cannot parse band range: {r!r}")
            continue
        lo, hi = int(m.group(1)), int(m.group(2))
        if lo >= hi:
            problems.append(f"Band range lo >= hi: {r!r}")
            continue
        parsed.append((lo, hi))

    if not parsed:
        return problems

    # Sort and check contiguous coverage of [0, 100]
    parsed.sort()
    if parsed[0][0] != 0:
        problems.append(f"Bands do not start at 0 (first start: {parsed[0][0]})")
    # Bands use inclusive integer ranges: [0,29] and [30,49] are contiguous
    # because 30 == 29 + 1. Check expected_start + 1 for the next lo.
    expected_next = parsed[0][0]
    for lo, hi in parsed:
        if lo > expected_next:
            problems.append(
                f"Gap in confidence bands: {expected_next}-{lo - 1} not covered"
            )
        elif lo < expected_next:
            problems.append(f"Overlap in confidence bands at {lo}-{hi}")
        expected_next = hi + 1
    if expected_next - 1 != 100:
        problems.append(f"Bands do not end at 100 (last end: {expected_start})")

    return problems


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate(path):
    errors = []
    warnings = []

    def err(msg):
        errors.append(msg)

    def warn(msg):
        warnings.append(msg)

    # ------------------------------------------------------------------
    # Rule 1: File is valid UTF-8
    # ------------------------------------------------------------------
    try:
        with open(path, "rb") as f:
            raw = f.read()
        text = raw.decode("utf-8")
        print("[OK]    Rule 1: File is valid UTF-8")
    except FileNotFoundError:
        err(f"File not found: {path}")
        print(f"[ERROR] Rule 1: File not found: {path}")
        # Cannot continue without the file
        return errors, warnings
    except UnicodeDecodeError as exc:
        err(f"File is not valid UTF-8: {exc}")
        print(f"[ERROR] Rule 1: File is not valid UTF-8: {exc}")
        return errors, warnings

    # ------------------------------------------------------------------
    # Rule 2: YAML front matter parses without errors
    # ------------------------------------------------------------------
    yaml_text, prose = split_front_matter(text)

    if yaml_text is None:
        err("No YAML front matter found (expected opening and closing '---')")
        print("[ERROR] Rule 2: No YAML front matter block found")
        data = {}
    else:
        try:
            data = yaml.safe_load(yaml_text) or {}
            print("[OK]    Rule 2: YAML front matter parses without errors")
        except yaml.YAMLError as exc:
            err(f"YAML parse error: {exc}")
            print(f"[ERROR] Rule 2: YAML parse error: {exc}")
            data = {}

    # ------------------------------------------------------------------
    # Rule 3: All required fields present
    # ------------------------------------------------------------------
    missing = [f for f in REQUIRED_FIELDS if f not in data]
    if missing:
        err(f"Missing required fields: {', '.join(missing)}")
        print(f"[ERROR] Rule 3: Missing required fields: {', '.join(missing)}")
    else:
        print("[OK]    Rule 3: All required fields present")

    # ------------------------------------------------------------------
    # Rule 4: trust_md_version == "0.1"
    # ------------------------------------------------------------------
    version = data.get("trust_md_version")
    if str(version) in ("0.1", "0.2"):
        print(f"[OK]    Rule 4: trust_md_version == \"{version}\"")
    else:
        err(f"trust_md_version must be \"0.1\" or \"0.2\", got: {version!r}")
        print(f"[ERROR] Rule 4: trust_md_version must be \"0.1\" or \"0.2\", got: {version!r}")

    # ------------------------------------------------------------------
    # Rule 5: produced_by.humans has at least one entry
    # ------------------------------------------------------------------
    humans = _get(data, "produced_by", "humans", default=None)
    if isinstance(humans, list) and len(humans) >= 1:
        print("[OK]    Rule 5: produced_by.humans has at least one entry")
    else:
        err("produced_by.humans must have at least one entry")
        print("[ERROR] Rule 5: produced_by.humans must have at least one entry")

    # ------------------------------------------------------------------
    # Rule 6: produced_by.agents is present (can be empty list)
    # ------------------------------------------------------------------
    produced_by = data.get("produced_by", {})
    if isinstance(produced_by, dict) and "agents" in produced_by:
        print("[OK]    Rule 6: produced_by.agents is present")
    else:
        err("produced_by.agents must be present (may be an empty list)")
        print("[ERROR] Rule 6: produced_by.agents must be present (may be empty list)")

    # ------------------------------------------------------------------
    # Rule 7: Each agent oversight is one of valid values
    # ------------------------------------------------------------------
    agents = _get(data, "produced_by", "agents", default=[])
    if not isinstance(agents, list):
        agents = []
    invalid_oversight = []
    for agent in agents:
        if isinstance(agent, dict):
            oversight = agent.get("oversight")
            if oversight not in VALID_OVERSIGHT_VALUES:
                invalid_oversight.append(
                    f"{agent.get('name', '<unnamed>')!r}: {oversight!r}"
                )
    if invalid_oversight:
        err(
            "Agent oversight values invalid: "
            + "; ".join(invalid_oversight)
            + f". Must be one of: {', '.join(sorted(VALID_OVERSIGHT_VALUES))}"
        )
        print(
            "[ERROR] Rule 7: Invalid agent oversight value(s): "
            + "; ".join(invalid_oversight)
        )
    else:
        print("[OK]    Rule 7: All agent oversight values are valid")

    # ------------------------------------------------------------------
    # Rule 8: governance.no_fabricated_citations is a boolean
    # ------------------------------------------------------------------
    nfc = _get(data, "governance", "no_fabricated_citations", default=None)
    if isinstance(nfc, bool):
        print("[OK]    Rule 8: governance.no_fabricated_citations is a boolean")
    else:
        err(
            f"governance.no_fabricated_citations must be a boolean, got: {nfc!r}"
        )
        print(
            f"[ERROR] Rule 8: governance.no_fabricated_citations must be a boolean, got: {nfc!r}"
        )

    # ------------------------------------------------------------------
    # Rule 9: epistemic_model.categories has >= 1 entry with id/label/definition
    # ------------------------------------------------------------------
    categories = _get(data, "epistemic_model", "categories", default=None)
    cat_ok = False
    if isinstance(categories, list) and len(categories) >= 1:
        all_valid = all(
            isinstance(c, dict) and "id" in c and "label" in c and "definition" in c
            for c in categories
        )
        if all_valid:
            cat_ok = True
            print(
                "[OK]    Rule 9: epistemic_model.categories has at least one entry "
                "with id, label, definition"
            )
        else:
            err(
                "Each epistemic_model.categories entry must have 'id', 'label', "
                "and 'definition'"
            )
            print(
                "[ERROR] Rule 9: One or more epistemic_model.categories entries "
                "missing id/label/definition"
            )
    else:
        err(
            "epistemic_model.categories must have at least one entry"
        )
        print(
            "[ERROR] Rule 9: epistemic_model.categories must have at least one entry"
        )

    # ------------------------------------------------------------------
    # Rule 10: epistemic_model.confidence_scale.type == "integer"
    # ------------------------------------------------------------------
    cs_type = _get(data, "epistemic_model", "confidence_scale", "type", default=None)
    if cs_type == "integer":
        print("[OK]    Rule 10: epistemic_model.confidence_scale.type == \"integer\"")
    else:
        err(
            f"epistemic_model.confidence_scale.type must be \"integer\", got: {cs_type!r}"
        )
        print(
            f"[ERROR] Rule 10: epistemic_model.confidence_scale.type must be \"integer\", "
            f"got: {cs_type!r}"
        )

    # ------------------------------------------------------------------
    # Rule 11: epistemic_model.confidence_scale.range == [0, 100]
    # ------------------------------------------------------------------
    cs_range = _get(
        data, "epistemic_model", "confidence_scale", "range", default=None
    )
    if cs_range == [0, 100]:
        print("[OK]    Rule 11: epistemic_model.confidence_scale.range == [0, 100]")
    else:
        err(
            f"epistemic_model.confidence_scale.range must be [0, 100], got: {cs_range!r}"
        )
        print(
            f"[ERROR] Rule 11: epistemic_model.confidence_scale.range must be [0, 100], "
            f"got: {cs_range!r}"
        )

    # ------------------------------------------------------------------
    # Rule 12: epistemic_model.confidence_scale.independent_of_category is True
    # ------------------------------------------------------------------
    cs_ind = _get(
        data,
        "epistemic_model",
        "confidence_scale",
        "independent_of_category",
        default=None,
    )
    if cs_ind is True:
        print(
            "[OK]    Rule 12: epistemic_model.confidence_scale.independent_of_category "
            "is True"
        )
    else:
        err(
            "epistemic_model.confidence_scale.independent_of_category must be true "
            f"(boolean), got: {cs_ind!r}"
        )
        print(
            f"[ERROR] Rule 12: epistemic_model.confidence_scale.independent_of_category "
            f"must be true, got: {cs_ind!r}"
        )

    # ------------------------------------------------------------------
    # Rule 13: epistemic_model.confidence_scale.bands has >= 5 entries
    # ------------------------------------------------------------------
    bands = _get(
        data, "epistemic_model", "confidence_scale", "bands", default=None
    )
    if isinstance(bands, list) and len(bands) >= 5:
        print(
            f"[OK]    Rule 13: epistemic_model.confidence_scale.bands has "
            f"{len(bands)} entries (>= 5)"
        )
    else:
        count = len(bands) if isinstance(bands, list) else 0
        err(
            f"epistemic_model.confidence_scale.bands must have at least 5 entries, "
            f"got: {count}"
        )
        print(
            f"[ERROR] Rule 13: epistemic_model.confidence_scale.bands must have >= 5 "
            f"entries, got: {count}"
        )

    # ------------------------------------------------------------------
    # Rule 14: last_reviewed matches YYYY-MM-DD and is a valid calendar date
    # ------------------------------------------------------------------
    last_reviewed = data.get("last_reviewed")
    date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    if last_reviewed is not None and date_pattern.match(str(last_reviewed)):
        try:
            datetime.date.fromisoformat(str(last_reviewed))
            print(f"[OK]    Rule 14: last_reviewed is a valid date ({last_reviewed})")
        except ValueError:
            err(
                f"last_reviewed '{last_reviewed}' is not a valid calendar date"
            )
            print(
                f"[ERROR] Rule 14: last_reviewed '{last_reviewed}' is not a valid "
                "calendar date"
            )
    else:
        err(
            f"last_reviewed must match YYYY-MM-DD, got: {last_reviewed!r}"
        )
        print(
            f"[ERROR] Rule 14: last_reviewed must match YYYY-MM-DD, got: {last_reviewed!r}"
        )

    # ------------------------------------------------------------------
    # Rule 15: Prose section (after closing ---) is present and non-empty
    # ------------------------------------------------------------------
    if prose is not None and prose.strip():
        print("[OK]    Rule 15: Prose section is present and non-empty")
    else:
        err("Prose section after closing '---' is absent or empty")
        print("[ERROR] Rule 15: Prose section after closing '---' is absent or empty")

    # ==================================================================
    # WARNING checks
    # ==================================================================

    # W1: corpus field is absent
    if "corpus" not in data:
        warn("'corpus' field is absent (recommended)")
        print("[WARN]  W1: 'corpus' field is absent (recommended)")
    else:
        print("[OK]    W1: 'corpus' field is present")

    # W2: artifacts field is absent
    if "artifacts" not in data:
        warn("'artifacts' field is absent (recommended)")
        print("[WARN]  W2: 'artifacts' field is absent (recommended)")
    else:
        print("[OK]    W2: 'artifacts' field is present")

    # W3: limitations is absent or empty
    limitations = data.get("limitations")
    if not limitations:
        warn("'limitations' is absent or empty (recommended)")
        print("[WARN]  W3: 'limitations' is absent or empty (recommended)")
    else:
        print("[OK]    W3: 'limitations' is present and non-empty")

    # W4: any humans entry lacks orcid
    if isinstance(humans, list):
        missing_orcid = [
            h.get("name", "<unnamed>")
            for h in humans
            if isinstance(h, dict) and not h.get("orcid")
        ]
        if missing_orcid:
            warn(
                f"Human(s) missing orcid (strongly recommended): "
                + ", ".join(str(n) for n in missing_orcid)
            )
            print(
                f"[WARN]  W4: Human(s) missing orcid: "
                + ", ".join(str(n) for n in missing_orcid)
            )
        else:
            print("[OK]    W4: All human entries have orcid")

    # W5: not all canonical five category IDs present
    if isinstance(categories, list):
        present_ids = {
            c["id"] for c in categories if isinstance(c, dict) and "id" in c
        }
        missing_cat_ids = CANONICAL_CATEGORY_IDS - present_ids
        if missing_cat_ids:
            warn(
                f"Not all canonical category IDs present; missing: "
                + ", ".join(sorted(missing_cat_ids))
            )
            print(
                f"[WARN]  W5: Missing canonical category IDs: "
                + ", ".join(sorted(missing_cat_ids))
            )
        else:
            print("[OK]    W5: All five canonical category IDs present")

    # W6: corpus.average_trust (if present) is outside 0–100
    avg_trust = _get(data, "corpus", "average_trust", default=None)
    if avg_trust is not None:
        try:
            at_val = float(avg_trust)
            if not (0 <= at_val <= 100):
                warn(
                    f"corpus.average_trust is outside [0, 100]: {avg_trust}"
                )
                print(
                    f"[WARN]  W6: corpus.average_trust is outside [0, 100]: {avg_trust}"
                )
            else:
                print(f"[OK]    W6: corpus.average_trust is within [0, 100] ({avg_trust})")
        except (TypeError, ValueError):
            warn(
                f"corpus.average_trust could not be interpreted as a number: {avg_trust!r}"
            )
            print(
                f"[WARN]  W6: corpus.average_trust could not be interpreted as a number: "
                f"{avg_trust!r}"
            )

    # W7: confidence bands do not contiguously cover [0, 100]
    if isinstance(bands, list) and len(bands) > 0:
        band_problems = check_band_coverage(bands)
        if band_problems:
            for p in band_problems:
                warn(f"Confidence band coverage: {p}")
            print(
                "[WARN]  W7: Confidence bands do not contiguously cover [0, 100]: "
                + "; ".join(band_problems)
            )
        else:
            print("[OK]    W7: Confidence bands contiguously cover [0, 100]")

    return errors, warnings


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "TRUST.md"

    print(f"Validating: {path}")
    print("-" * 60)

    errors, warnings = validate(path)

    print("-" * 60)
    status = "FAIL" if errors else "PASS"
    print(
        f"{len(errors)} error(s), {len(warnings)} warning(s) — {status}"
    )

    if errors:
        print("\nErrors:")
        for e in errors:
            print(f"  [ERROR] {e}")

    if warnings:
        print("\nWarnings:")
        for w in warnings:
            print(f"  [WARN]  {w}")

    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
