from knitweb_lens import LocalFilesAdapter, RLMHarness, evaluate_session


def test_query_attaches_integer_reliability_report(tmp_path):
    path = tmp_path / "note.md"
    path.write_text("Lens preserves provenance citations for grounded answers.", encoding="utf-8")

    answer = RLMHarness().query("What preserves provenance citations?", adapters=[LocalFilesAdapter([path])])

    assert answer.reliability is not None
    assert isinstance(answer.reliability["confidence"], int)
    assert answer.reliability["abstained"] is False
    assert answer.reliability["citation_count"] == 1


def test_unrelated_query_abstains_with_low_confidence(tmp_path):
    path = tmp_path / "note.md"
    path.write_text("Lens preserves provenance citations.", encoding="utf-8")

    answer = RLMHarness().query("quantum weather banana", adapters=[LocalFilesAdapter([path])])

    assert answer.reliability["abstained"] is True
    assert answer.reliability["confidence"] < 25
    assert "Insufficient grounded support" in answer.text


def test_empty_session_abstains():
    session = RLMHarness().session("anything", adapters=[])
    report = evaluate_session(session)

    assert report.abstained is True
    assert report.confidence == 0
    assert report.reason == "no cited chunks available"


def test_min_confidence_range_is_validated():
    session = RLMHarness().session("anything", adapters=[])

    try:
        evaluate_session(session, min_confidence=101)
    except ValueError as exc:
        assert "between 0 and 100" in str(exc)
    else:
        raise AssertionError("expected ValueError")

