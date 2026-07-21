import json
from pathlib import Path

import yaml

from jsonschema import Draft202012Validator

from tools.validate import SUPPORTED_VERSIONS, _median_band, split_front_matter, validate


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "minimal-v0.3.trust.md"
V01_FIXTURE = ROOT / "tests" / "fixtures" / "minimal-v0.1.trust.md"


def write_manifest(tmp_path, mutate):
    yaml_text, prose = split_front_matter(FIXTURE.read_text(encoding="utf-8"))
    data = yaml.safe_load(yaml_text)
    mutate(data)
    path = tmp_path / "TRUST.md"
    path.write_text(f"---\n{yaml.safe_dump(data, sort_keys=False)}---\n{prose}", encoding="utf-8")
    return path


def v04_data():
    yaml_text, _ = split_front_matter(FIXTURE.read_text(encoding="utf-8"))
    data = yaml.safe_load(yaml_text)
    data["trust_md_version"] = "0.4"
    data["epistemic_model"].pop("dimensions")
    data.pop("assessment")
    data.pop("corpus")
    data["subjects"] = [{
        "id": "subject-001",
        "type": "evidence-record",
        "identifier": "https://example.org/evidence/record-001",
        "version": "1.0",
    }]
    data["assessments"] = [{
        "series_id": "https://example.org/assessments/series-001",
        "id": "https://example.org/assessments/series-001/versions/1",
        "version": "1",
        "subject": "subject-001",
        "purpose": "Inclusion in a declared synthesis",
        "fitness_for_purpose": "suitable",
        "dimensions": {
            "evidence_support": "direct",
            "calibration": "matched",
            "source_integrity": "verified",
        },
        "assessed_by": {
            "humans": [{"name": "Example Reviewer", "role": "reviewer"}],
            "agents": [],
        },
        "protocol": {
            "identifier": "https://example.org/protocols/review",
            "version": "1.0",
        },
        "evidence_basis": [{
            "relation": "uses-qc-report",
            "identifier": "https://example.org/qc/report-001",
        }],
        "assessed_at": "2026-07-21T10:00:00Z",
        "review_status": "human-reviewed",
        "independence": "declared-independent",
        "status": "active",
        "limitations": [],
    }]
    return data


def write_v04_manifest(tmp_path, mutate=lambda data: None):
    _, prose = split_front_matter(FIXTURE.read_text(encoding="utf-8"))
    data = v04_data()
    mutate(data)
    path = tmp_path / "TRUST-v0.4.md"
    path.write_text(
        f"---\n{yaml.safe_dump(data, sort_keys=False)}---\n{prose}",
        encoding="utf-8",
    )
    return path


def test_v03_fixture_is_clean():
    errors, warnings, notices = validate(FIXTURE)
    assert errors == []
    assert warnings == []
    assert notices == []


def test_frozen_v02_reference_remains_valid():
    errors, _, _ = validate(ROOT / "examples" / "neuronautix.trust.md")
    assert errors == []


def test_frozen_v01_fixture_remains_valid():
    errors, warnings, notices = validate(V01_FIXTURE)
    assert errors == []
    assert warnings == []
    assert notices == []


def test_unknown_version_is_distinct(tmp_path):
    path = write_manifest(tmp_path, lambda data: data.update(trust_md_version="9.9"))
    errors, _, _ = validate(path)
    assert errors == ["unsupported version: 9.9"]


def test_version_must_be_quoted(tmp_path):
    text = FIXTURE.read_text(encoding="utf-8").replace('trust_md_version: "0.3"', "trust_md_version: 0.3")
    path = tmp_path / "TRUST.md"
    path.write_text(text, encoding="utf-8")
    errors, _, _ = validate(path)
    assert "trust_md_version must be a quoted string" in errors


def test_single_point_numeric_band_is_valid(tmp_path):
    def mutate(data):
        ranges = ["0-29", "30-49", "50-69", "70-99", "100-100"]
        for band, value in zip(data["epistemic_model"]["support_bands"], ranges):
            band["range"] = value

    errors, _, _ = validate(write_manifest(tmp_path, mutate))
    assert errors == []


def test_human_review_requires_human(tmp_path):
    def mutate(data):
        data["assessment"]["assessed_by"]["humans"] = []
        data["assessment"]["assessed_by"]["agents"] = [{
            "name": "ReviewBot", "role": "reviewer", "oversight": "automated"
        }]

    errors, _, _ = validate(write_manifest(tmp_path, mutate))
    assert "human-reviewed requires an identifiable human assessor" in errors


def test_adjudication_requires_disagreement_and_resolution(tmp_path):
    path = write_manifest(tmp_path, lambda data: data["assessment"].update(review_status="adjudicated"))
    errors, _, _ = validate(path)
    assert "adjudicated requires disagreement and resolution references" in errors


def test_claim_evidence_records_are_external(tmp_path):
    path = write_manifest(tmp_path, lambda data: data["assessment"].update(unit="claim-evidence"))
    errors, _, _ = validate(path)
    assert "claim-evidence assessments require companions.claim_records" in errors


def test_conservative_even_median_uses_lower_band():
    assert _median_band({"tentative": 1, "high": 1}) == "tentative"


def test_wrong_median_is_an_error(tmp_path):
    path = write_manifest(tmp_path, lambda data: data["corpus"].update(median_band="moderate"))
    errors, _, _ = validate(path)
    assert any("conservative tie rule" in error for error in errors)


def test_unknown_standard_field_is_a_notice(tmp_path):
    path = write_manifest(tmp_path, lambda data: data.update(mispelled_field=True))
    errors, _, notices = validate(path)
    assert errors == []
    assert "unknown field ignored: mispelled_field" in notices


def test_unknown_nested_field_is_a_notice(tmp_path):
    def mutate(data):
        data["epistemic_model"]["support_bands"][0]["meening"] = "typo"

    errors, _, notices = validate(write_manifest(tmp_path, mutate))
    assert errors == []
    assert (
        "unknown field ignored: epistemic_model.support_bands[0].meening"
        in notices
    )


def test_private_nested_extension_is_not_a_notice(tmp_path):
    def mutate(data):
        data["epistemic_model"]["support_bands"][0]["x_ontology_term"] = "ECO:0000000"

    errors, _, notices = validate(write_manifest(tmp_path, mutate))
    assert errors == []
    assert notices == []


def test_deprecated_average_is_only_a_notice(tmp_path):
    path = write_manifest(tmp_path, lambda data: data["corpus"].update(average_trust=72))
    errors, _, notices = validate(path)
    assert errors == []
    assert "corpus.average_trust is deprecated; prefer band_distribution" in notices


def test_protocol_provenance_round_trips_without_type_loss():
    yaml_text, _ = split_front_matter(FIXTURE.read_text(encoding="utf-8"))
    original = yaml.safe_load(yaml_text)["assessment"]
    round_tripped = yaml.safe_load(yaml.safe_dump(original, sort_keys=False))
    assert round_tripped == original
    assert isinstance(round_tripped["independent_review"], bool)
    assert isinstance(round_tripped["date"], str)


def test_latest_schema_is_the_versioned_v04_schema():
    latest = json.loads((ROOT / "schema" / "trust.schema.json").read_text(encoding="utf-8"))
    versioned = json.loads((ROOT / "schema" / "v0.4" / "trust.schema.json").read_text(encoding="utf-8"))
    assert latest == versioned


def test_frozen_schema_ids_are_pinned_to_the_rc_distribution():
    for version in ("0.1", "0.2", "0.3"):
        schema = json.loads(
            (ROOT / "schema" / f"v{version}" / "trust.schema.json").read_text(
                encoding="utf-8"
            )
        )
        assert schema["$id"] == (
            "https://raw.githubusercontent.com/Neuronautix/TRUST.md/"
            f"v0.3.0-rc.1/schema/v{version}/trust.schema.json"
        )


def test_root_template_is_valid_and_contains_no_assessment_claims():
    template = ROOT / "TRUST.md"
    errors, warnings, notices = validate(template)
    assert errors == []
    assert warnings == []
    assert notices == []
    yaml_text, _ = split_front_matter(template.read_text(encoding="utf-8"))
    data = yaml.safe_load(yaml_text)
    assert "assessment" not in data
    assert "dimensions" not in data["epistemic_model"]
    assert "corpus" not in data


def test_v04_schema_is_valid_and_dispatch_is_exact(tmp_path):
    schema = json.loads(
        (ROOT / "schema" / "v0.4" / "trust.schema.json").read_text(
            encoding="utf-8"
        )
    )
    Draft202012Validator.check_schema(schema)
    errors, warnings, notices = validate(write_v04_manifest(tmp_path))
    assert errors == []
    assert warnings == []
    assert notices == []
    assert SUPPORTED_VERSIONS == ("0.1", "0.2", "0.3", "0.4")


def test_v04_requires_subjects_but_allows_zero_assessments(tmp_path):
    errors, _, _ = validate(
        write_v04_manifest(tmp_path, lambda data: data.update(assessments=[]))
    )
    assert errors == []

    errors, _, _ = validate(
        write_v04_manifest(tmp_path, lambda data: data.pop("assessments"))
    )
    assert errors == []

    path = write_v04_manifest(tmp_path, lambda data: data.pop("subjects"))
    errors, _, _ = validate(path)
    assert any("subjects" in error and "required property" in error for error in errors)


def test_v04_subject_requires_exactly_one_identity_constraint(tmp_path):
    def no_version(data):
        data["subjects"][0].pop("version")

    errors, _, _ = validate(write_v04_manifest(tmp_path, no_version))
    assert errors

    def both(data):
        data["subjects"][0]["snapshot"] = {
            "identifier": "https://example.org/snapshots/record-001",
            "digest": {"algorithm": "sha-256", "value": "a" * 64},
        }

    errors, _, _ = validate(write_v04_manifest(tmp_path, both))
    assert errors


def test_v04_snapshot_digest_is_structurally_immutable(tmp_path):
    def snapshot(data):
        subject = data["subjects"][0]
        subject.pop("version")
        subject["snapshot"] = {
            "identifier": "https://example.org/snapshots/record-001",
            "digest": {"algorithm": "sha-256", "value": "a" * 64},
        }

    errors, _, _ = validate(write_v04_manifest(tmp_path, snapshot))
    assert errors == []

    def bad_digest(data):
        snapshot(data)
        data["subjects"][0]["snapshot"]["digest"]["value"] = "mutable"

    errors, _, _ = validate(write_v04_manifest(tmp_path, bad_digest))
    assert errors


def test_v04_subject_and_assessment_identities_are_unique(tmp_path):
    def duplicate(data):
        data["subjects"].append(dict(data["subjects"][0]))
        data["assessments"].append(dict(data["assessments"][0]))

    errors, _, _ = validate(write_v04_manifest(tmp_path, duplicate))
    assert any("subjects[1].id duplicates" in error for error in errors)
    assert any("assessments[1].id duplicates" in error for error in errors)
    assert any("duplicates series_id/version" in error for error in errors)


def test_v04_assessment_subject_must_resolve(tmp_path):
    def mutate(data):
        data["assessments"][0]["subject"] = "missing-subject"

    errors, _, _ = validate(write_v04_manifest(tmp_path, mutate))
    assert any("does not resolve" in error for error in errors)


def test_v04_fitness_requires_purpose_and_conditions(tmp_path):
    def no_purpose(data):
        data["assessments"][0].pop("purpose")

    errors, _, _ = validate(write_v04_manifest(tmp_path, no_purpose))
    assert any("purpose" in error and "required property" in error for error in errors)

    def conditional_without_conditions(data):
        data["assessments"][0]["fitness_for_purpose"] = "conditionally-suitable"

    errors, _, _ = validate(write_v04_manifest(tmp_path, conditional_without_conditions))
    assert any("conditions" in error and "required property" in error for error in errors)

    def descriptive(data):
        data["assessments"][0].pop("purpose")
        data["assessments"][0].pop("fitness_for_purpose")

    errors, _, _ = validate(write_v04_manifest(tmp_path, descriptive))
    assert errors == []


def test_v04_active_reviewed_assessment_requires_inspectable_basis(tmp_path):
    def mutate(data):
        data["assessments"][0].pop("evidence_basis")

    errors, _, _ = validate(write_v04_manifest(tmp_path, mutate))
    assert any("evidence_basis" in error and "required property" in error for error in errors)


def test_v04_basis_relations_are_core_or_explicit_extensions(tmp_path):
    def invalid(data):
        data["assessments"][0]["evidence_basis"][0]["relation"] = "popular-with"

    errors, _, _ = validate(write_v04_manifest(tmp_path, invalid))
    assert errors

    def extension(data):
        data["assessments"][0]["evidence_basis"][0]["relation"] = "x_domain-check"

    errors, _, _ = validate(write_v04_manifest(tmp_path, extension))
    assert errors == []


def test_v04_protocol_identifier_and_version_are_required(tmp_path):
    def mutate(data):
        data["assessments"][0]["protocol"].pop("version")

    errors, _, _ = validate(write_v04_manifest(tmp_path, mutate))
    assert any("version" in error and "required property" in error for error in errors)


def test_v04_agent_only_is_not_human_reviewed(tmp_path):
    def mutate(data):
        assessment = data["assessments"][0]
        assessment["assessed_by"]["humans"] = []
        assessment["assessed_by"]["agents"] = [{
            "name": "ReviewBot",
            "role": "reviewer",
            "oversight": "automated",
        }]
        assessment["independence"] = "not-declared"

    errors, _, _ = validate(write_v04_manifest(tmp_path, mutate))
    assert any("humans" in error and "non-empty" in error for error in errors)


def test_v04_agent_only_can_be_declared_agent_reviewed(tmp_path):
    def mutate(data):
        assessment = data["assessments"][0]
        assessment["review_status"] = "agent-reviewed"
        assessment["assessed_by"]["humans"] = []
        assessment["assessed_by"]["agents"] = [{
            "name": "ReviewBot",
            "role": "reviewer",
            "oversight": "automated",
        }]
        assessment["independence"] = "not-declared"

    errors, _, _ = validate(write_v04_manifest(tmp_path, mutate))
    assert errors == []


def test_v04_declared_independence_needs_a_nonproducer_human(tmp_path):
    def mutate(data):
        data["assessments"][0]["assessed_by"]["humans"][0]["name"] = "Example Author"

    errors, _, _ = validate(write_v04_manifest(tmp_path, mutate))
    assert any("independence requires an identifiable assessor" in error for error in errors)

    def boolean_state(data):
        data["assessments"][0]["independence"] = True

    errors, _, _ = validate(write_v04_manifest(tmp_path, boolean_state))
    assert errors


def test_v04_review_status_is_not_a_dimension(tmp_path):
    def mutate(data):
        data["assessments"][0]["dimensions"]["review_status"] = "human-reviewed"

    errors, _, notices = validate(write_v04_manifest(tmp_path, mutate))
    assert any("not a v0.4 quality dimension" in error for error in errors)
    assert any("prohibited" in notice for notice in notices)


def test_v04_reuse_is_impact_not_a_dimension(tmp_path):
    def valid_impact(data):
        data["impact"] = {"reuse_count": 42}

    errors, _, _ = validate(write_v04_manifest(tmp_path, valid_impact))
    assert errors == []

    def invalid_dimension(data):
        data["assessments"][0]["dimensions"]["reuse_count"] = 42

    errors, _, _ = validate(write_v04_manifest(tmp_path, invalid_dimension))
    assert any("not a v0.4 quality dimension" in error for error in errors)

    def invalid_downloads(data):
        data["assessments"][0]["dimensions"]["downloads"] = 100

    errors, _, _ = validate(write_v04_manifest(tmp_path, invalid_downloads))
    assert any("dimensions.downloads is not a v0.4 quality dimension" in error for error in errors)


def test_v04_conflicting_assessments_coexist_without_aggregation(tmp_path):
    def mutate(data):
        second = yaml.safe_load(yaml.safe_dump(data["assessments"][0]))
        second.update({
            "series_id": "https://example.org/assessments/series-002",
            "id": "https://example.org/assessments/series-002/versions/1",
            "fitness_for_purpose": "not-suitable",
        })
        data["assessments"].append(second)

    errors, _, _ = validate(write_v04_manifest(tmp_path, mutate))
    assert errors == []

    def aggregate(data):
        data["corpus"] = {"average_trust": 72}

    errors, _, notices = validate(write_v04_manifest(tmp_path, aggregate))
    assert "v0.4 prohibits top-level aggregation across assessments" in errors
    assert any("corpus is a v0.3 field ignored" in notice for notice in notices)


def test_v04_supersession_requires_same_series_and_has_no_cycles(tmp_path):
    def cross_series(data):
        first = data["assessments"][0]
        second = yaml.safe_load(yaml.safe_dump(first))
        second.update({
            "series_id": "https://example.org/assessments/series-002",
            "id": "https://example.org/assessments/series-002/versions/2",
            "version": "2",
            "supersedes": first["id"],
        })
        data["assessments"].append(second)

    errors, _, _ = validate(write_v04_manifest(tmp_path, cross_series))
    assert any("same series_id" in error for error in errors)

    def cycle(data):
        first = data["assessments"][0]
        second = yaml.safe_load(yaml.safe_dump(first))
        second.update({
            "id": "https://example.org/assessments/series-001/versions/2",
            "version": "2",
            "supersedes": first["id"],
        })
        first["supersedes"] = second["id"]
        data["assessments"].append(second)

    errors, _, _ = validate(write_v04_manifest(tmp_path, cycle))
    assert any("supersession cycle" in error for error in errors)


def test_v04_supersession_cannot_switch_subject(tmp_path):
    def mutate(data):
        data["subjects"].append({
            "id": "subject-002",
            "type": "evidence-record",
            "identifier": "https://example.org/evidence/record-002",
            "version": "1.0",
        })
        first = data["assessments"][0]
        second = yaml.safe_load(yaml.safe_dump(first))
        second.update({
            "id": "https://example.org/assessments/series-001/versions/2",
            "version": "2",
            "subject": "subject-002",
            "supersedes": first["id"],
        })
        data["assessments"].append(second)

    errors, _, _ = validate(write_v04_manifest(tmp_path, mutate))
    assert any("supersedes must reference the same subject" in error for error in errors)


def test_v04_external_supersession_target_is_a_warning(tmp_path):
    def mutate(data):
        data["assessments"][0]["supersedes"] = (
            "https://elsewhere.example/assessments/series-001/versions/0"
        )

    errors, warnings, _ = validate(write_v04_manifest(tmp_path, mutate))
    assert errors == []
    assert any("not locally inspectable" in warning for warning in warnings)


def test_v04_nonactive_lifecycle_version_requires_link_and_reason(tmp_path):
    def mutate(data):
        data["assessments"][0]["status"] = "retracted"

    errors, _, _ = validate(write_v04_manifest(tmp_path, mutate))
    assert any("supersedes" in error and "required property" in error for error in errors)
    assert any("lifecycle_reason" in error and "required property" in error for error in errors)


def test_v04_lifecycle_state_does_not_change_subject(tmp_path):
    def mutate(data):
        first = data["assessments"][0]
        withdrawn = yaml.safe_load(yaml.safe_dump(first))
        withdrawn.update({
            "id": "https://example.org/assessments/series-001/versions/2",
            "version": "2",
            "status": "withdrawn",
            "supersedes": first["id"],
            "lifecycle_reason": "No longer used for the declared purpose.",
        })
        data["assessments"].append(withdrawn)

    data_path = write_v04_manifest(tmp_path, mutate)
    errors, _, _ = validate(data_path)
    assert errors == []
    yaml_text, _ = split_front_matter(data_path.read_text(encoding="utf-8"))
    data = yaml.safe_load(yaml_text)
    assert "status" not in data["subjects"][0]


def test_v04_datetime_requires_offset_and_preserves_migrated_precision(tmp_path):
    def no_offset(data):
        data["assessments"][0]["assessed_at"] = "2026-07-21T10:00:00"

    errors, _, _ = validate(write_v04_manifest(tmp_path, no_offset))
    assert errors

    def migrated(data):
        assessment = data["assessments"][0]
        assessment["assessed_at"] = "2026-07-21T00:00:00Z"
        assessment["assessed_at_precision"] = "date"

    errors, _, _ = validate(write_v04_manifest(tmp_path, migrated))
    assert errors == []


def test_v04_singular_assessment_is_ignored_but_cannot_coexist(tmp_path):
    def singular_only(data):
        data["assessment"] = {"unit": "repository"}
        data.pop("assessments")

    errors, _, notices = validate(write_v04_manifest(tmp_path, singular_only))
    assert errors == []
    assert any("assessment is a v0.3 field ignored" in notice for notice in notices)

    def both(data):
        data["assessment"] = {"unit": "repository"}

    errors, _, _ = validate(write_v04_manifest(tmp_path, both))
    assert "v0.4 cannot combine singular assessment with plural assessments" in errors


def test_v04_numeric_refinement_is_nonprobabilistic(tmp_path):
    def mutate(data):
        data["assessments"][0]["numeric_refinement"] = {
            "value": 85,
            "not_probability": False,
        }

    errors, _, _ = validate(write_v04_manifest(tmp_path, mutate))
    assert errors


def test_v04_assessment_summary_is_scoped_and_median_is_conservative(tmp_path):
    def valid(data):
        data["assessments"][0]["summary"] = {
            "scope": "assessment",
            "band_distribution": {"tentative": 1, "high": 1},
            "median_band": "tentative",
        }

    errors, _, _ = validate(write_v04_manifest(tmp_path, valid))
    assert errors == []

    def invalid(data):
        valid(data)
        data["assessments"][0]["summary"]["median_band"] = "high"

    errors, _, _ = validate(write_v04_manifest(tmp_path, invalid))
    assert any("conservative tie rule" in error for error in errors)


def test_v04_unknown_nested_field_is_an_ignored_field_notice(tmp_path):
    def mutate(data):
        data["assessments"][0]["protocol"]["versoin"] = "typo"

    errors, _, notices = validate(write_v04_manifest(tmp_path, mutate))
    assert errors == []
    assert (
        "unknown field ignored: assessments[0].protocol.versoin" in notices
    )


def test_v04_semantic_checks_return_errors_for_malformed_nodes(tmp_path):
    def malformed_model(data):
        data["epistemic_model"] = "not-a-mapping"

    def malformed_distribution(data):
        data["assessments"][0]["summary"] = {
            "scope": "assessment",
            "band_distribution": {"high": "many"},
            "median_band": "high",
        }

    def malformed_status(data):
        data["assessments"][0]["review_status"] = ["human-reviewed"]

    def malformed_collections(data):
        data["subjects"] = "not-an-array"
        data["assessments"] = {"not": "an-array"}

    for mutate in (
        malformed_model,
        malformed_distribution,
        malformed_status,
        malformed_collections,
    ):
        errors, _, _ = validate(write_v04_manifest(tmp_path, mutate))
        assert errors


def test_v04_independence_requires_a_nonblank_string_name(tmp_path):
    def blank_name(data):
        data["assessments"][0]["assessed_by"]["humans"][0]["name"] = " "

    errors, _, _ = validate(write_v04_manifest(tmp_path, blank_name))
    assert any("independence requires an identifiable assessor" in error for error in errors)

    def nonstring_name(data):
        data["assessments"][0]["assessed_by"]["humans"][0]["name"] = 42

    errors, _, _ = validate(write_v04_manifest(tmp_path, nonstring_name))
    assert errors


def load_front_matter(path):
    yaml_text, _ = split_front_matter(path.read_text(encoding="utf-8"))
    return yaml.safe_load(yaml_text)


def test_v04_public_examples_are_clean():
    examples = sorted((ROOT / "examples").glob("v04-*.trust.md"))
    examples.append(ROOT / "examples" / "migration" / "v04-after-v03.trust.md")
    assert {path.name for path in examples} == {
        "v04-after-v03.trust.md",
        "v04-lifecycle.trust.md",
        "v04-missing-states.trust.md",
        "v04-multiple-assessments.trust.md",
        "v04-no-assessment.trust.md",
        "v04-single-assessment.trust.md",
    }
    for path in examples:
        errors, warnings, notices = validate(path)
        assert (errors, warnings, notices) == ([], [], []), path


def test_v04_examples_cover_plural_contextual_assessment_cases():
    data = load_front_matter(
        ROOT / "examples" / "v04-multiple-assessments.trust.md"
    )
    assessments = data["assessments"]
    assert len(assessments) == 4
    assert {item["subject"] for item in assessments} == {"subject-001"}
    assert assessments[0]["purpose"] == assessments[1]["purpose"]
    assert {
        assessments[0]["fitness_for_purpose"],
        assessments[1]["fitness_for_purpose"],
    } == {"suitable", "not-suitable"}
    assert assessments[2]["purpose"] != assessments[0]["purpose"]
    assert assessments[2]["review_status"] == "human-reviewed"
    assert assessments[2]["assessed_by"]["humans"]
    assert assessments[2]["assessed_by"]["agents"]
    assert assessments[3]["review_status"] == "agent-reviewed"
    assert assessments[3]["assessed_by"]["humans"] == []
    assert "corpus" not in data


def test_v04_no_assessment_and_impact_examples_do_not_imply_quality():
    no_assessment = load_front_matter(
        ROOT / "examples" / "v04-no-assessment.trust.md"
    )
    assert no_assessment["subjects"]
    assert no_assessment["assessments"] == []

    single = load_front_matter(
        ROOT / "examples" / "v04-single-assessment.trust.md"
    )
    assert single["x_reuse_metrics"]["reuse_count"] == 12
    assert "reuse_count" not in single["assessments"][0]["dimensions"]


def test_v04_lifecycle_examples_leave_subjects_unchanged():
    data = load_front_matter(ROOT / "examples" / "v04-lifecycle.trust.md")
    assert "status" not in data["subjects"][0]
    assert {item["status"] for item in data["assessments"]} == {
        "active",
        "superseded",
        "withdrawn",
        "retracted",
    }
    for item in data["assessments"]:
        if item["status"] in {"superseded", "withdrawn", "retracted"}:
            assert item["supersedes"]
            assert item["lifecycle_reason"]
    supersession = data["assessments"][1]
    assert supersession["series_id"] in supersession["supersedes"]
    assert "within this assessment series" in supersession["lifecycle_reason"]


def test_v04_missing_state_example_preserves_four_meanings():
    data = load_front_matter(ROOT / "examples" / "v04-missing-states.trust.md")
    assessments = data["assessments"]
    assert "evidence_support" not in assessments[0]["dimensions"]
    assert assessments[1]["dimensions"]["evidence_support"] == "not-assessed"
    assert assessments[2]["dimensions"]["evidence_support"] == "not-applicable"
    assert assessments[3]["dimensions"]["evidence_support"] == "none"


def test_v03_to_v04_migration_pair_is_explicit_and_meaning_preserving():
    before_path = ROOT / "examples" / "migration" / "v03-before-v04.trust.md"
    after_path = ROOT / "examples" / "migration" / "v04-after-v03.trust.md"
    before = load_front_matter(before_path)
    after = load_front_matter(after_path)

    errors, warnings, notices = validate(before_path)
    assert errors == []
    assert warnings == []
    assert notices == [
        "corpus.average_trust is deprecated; prefer band_distribution"
    ]
    assert validate(after_path) == ([], [], [])
    assert before["trust_md_version"] == "0.3"
    assert after["trust_md_version"] == "0.4"
    assert len(after["assessments"]) == 1
    migrated = after["assessments"][0]
    assert migrated["review_status"] == before["assessment"]["review_status"]
    assert migrated["assessed_by"] == before["assessment"]["assessed_by"]
    assert migrated["assessed_at"] == f'{before["assessment"]["date"]}T00:00:00Z'
    assert migrated["assessed_at_precision"] == "date"
    assert "review_status" not in migrated["dimensions"]
    assert after["x_migration"]["legacy_average_trust"] == 80
    population = after["x_migration"]["legacy_summary_population"]
    assert population == {
        "unit": "claims",
        "count": before["corpus"]["total_claims"],
        "source_scope": "corpus",
    }
    assert sum(migrated["summary"]["band_distribution"].values()) == population[
        "count"
    ]


def test_v04_valid_fixtures_and_provenance_round_trip():
    fixture_dir = ROOT / "tests" / "fixtures" / "v0.4"
    valid = sorted(fixture_dir.glob("*-valid.trust.md"))
    assert {path.name for path in valid} == {
        "minimal-valid.trust.md",
        "provenance-roundtrip-valid.trust.md",
    }
    for path in valid:
        assert validate(path) == ([], [], [])

    original = load_front_matter(
        fixture_dir / "provenance-roundtrip-valid.trust.md"
    )["assessments"][0]
    round_tripped = yaml.safe_load(yaml.safe_dump(original, sort_keys=False))
    assert round_tripped == original
    assert isinstance(round_tripped["numeric_refinement"]["value"], int)
    assert isinstance(round_tripped["numeric_refinement"]["not_probability"], bool)
    assert isinstance(round_tripped["x_protocol_parameters"]["threshold"], float)
    assert isinstance(round_tripped["x_protocol_parameters"]["labels"], list)


def test_v04_invalid_fixture_diagnostics_are_stable():
    fixture_dir = ROOT / "tests" / "fixtures" / "v0.4"
    expected = {
        "malformed-subject-identifier.invalid.trust.md": "does not match '^https?://'",
        "missing-protocol-version.invalid.trust.md": "'version' is a required property",
        "mutable-subject-no-version.invalid.trust.md": "is not valid under any of the given schemas",
        "supersession-cycle.invalid.trust.md": "supersession cycle detected",
    }
    assert {path.name for path in fixture_dir.glob("*.invalid.trust.md")} == set(expected)
    for name, diagnostic in expected.items():
        errors, _, _ = validate(fixture_dir / name)
        assert any(diagnostic in error for error in errors), name
