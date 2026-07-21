from pathlib import Path

import yaml

from tools.validate import _median_band, split_front_matter, validate


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "minimal-v0.3.trust.md"


def write_manifest(tmp_path, mutate):
    yaml_text, prose = split_front_matter(FIXTURE.read_text(encoding="utf-8"))
    data = yaml.safe_load(yaml_text)
    mutate(data)
    path = tmp_path / "TRUST.md"
    path.write_text(f"---\n{yaml.safe_dump(data, sort_keys=False)}---\n{prose}", encoding="utf-8")
    return path


def test_v03_fixture_is_clean():
    errors, warnings, notices = validate(FIXTURE)
    assert errors == []
    assert warnings == []
    assert notices == []


def test_frozen_v02_reference_remains_valid():
    errors, _, _ = validate(ROOT / "examples" / "neuronautix.trust.md")
    assert errors == []


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
