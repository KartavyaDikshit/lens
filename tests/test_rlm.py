from knitweb_lens import LocalFilesAdapter, RLMHarness


def test_harness_returns_cited_offline_answer(tmp_path):
    path = tmp_path / "fabric.md"
    path.write_text(
        "Lens is an interpret layer. It preserves provenance citations for Pulse records.",
        encoding="utf-8",
    )

    answer = RLMHarness().query("What preserves provenance?", adapters=[LocalFilesAdapter([path])])

    assert "provenance" in answer.text.casefold()
    assert answer.citations
    assert answer.session.session_id.startswith("lens-session:")


def test_harness_budget_prunes_context(tmp_path):
    path = tmp_path / "long.txt"
    path.write_text("alpha " * 500, encoding="utf-8")

    session = RLMHarness().session(
        "alpha",
        adapters=[LocalFilesAdapter([path])],
        max_chunks=1,
        budget_chars=40,
    )

    assert len(session.ranked_chunks) == 1
    assert session.used_chars <= 40

