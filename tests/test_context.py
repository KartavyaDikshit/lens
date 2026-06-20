import json
import threading
import urllib.request
from http.server import HTTPServer

import pytest

from knitweb_lens import (
    LocalFilesAdapter,
    RLMHarness,
    answer_from_context,
    answer_markdown,
    context_bundle,
    session_from_context,
    session_markdown,
)
from knitweb_lens.server import make_handler


def test_context_bundle_round_trip_preserves_session(tmp_path):
    path = tmp_path / "note.md"
    path.write_text("Lens context bundles preserve citations and integer scores.", encoding="utf-8")

    session = RLMHarness().session("What preserves citations?", adapters=[LocalFilesAdapter([path])])
    bundle = context_bundle(session)
    rebuilt = session_from_context(json.loads(json.dumps(bundle)))

    assert bundle["format"] == "knitweb-lens-context"
    assert rebuilt.session_id == session.session_id
    assert rebuilt.citations == session.citations
    assert rebuilt.ranked_chunks[0].score == session.ranked_chunks[0].score


def test_answer_from_context_uses_saved_chunks(tmp_path):
    path = tmp_path / "note.md"
    path.write_text("Saved context can be answered without reading source files again.", encoding="utf-8")

    bundle = RLMHarness().export_context("What can be answered?", adapters=[LocalFilesAdapter([path])])
    path.unlink()
    answer = answer_from_context(bundle)

    assert "Saved context" in answer.text
    assert answer.citations


def test_context_markdown_rendering_contains_scores_and_citations(tmp_path):
    path = tmp_path / "note.md"
    path.write_text("Markdown rendering exposes citations.", encoding="utf-8")

    answer = RLMHarness().query("What exposes citations?", adapters=[LocalFilesAdapter([path])])

    assert "## Citations" in answer_markdown(answer)
    rendered = session_markdown(answer.session)
    assert "Score:" in rendered
    assert str(path) in rendered


def test_invalid_context_bundle_rejected():
    with pytest.raises(ValueError, match="not a Knitweb Lens"):
        session_from_context({"format": "other", "version": 1, "session": {}})


def test_http_interpret_accepts_context_bundle(tmp_path):
    path = tmp_path / "note.md"
    path.write_text("HTTP replay can answer from a context bundle.", encoding="utf-8")
    bundle = RLMHarness().export_context("What can replay?", adapters=[LocalFilesAdapter([path])])

    httpd = HTTPServer(("127.0.0.1", 0), make_handler([]))
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    try:
        body = json.dumps({"context": bundle, "include_context": True}).encode("utf-8")
        request = urllib.request.Request(
            f"http://127.0.0.1:{httpd.server_port}/interpret",
            data=body,
            headers={"content-type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=5) as response:
            payload = json.loads(response.read().decode("utf-8"))
    finally:
        httpd.shutdown()
        thread.join(timeout=5)

    assert "HTTP replay" in payload["text"]
    assert payload["context"]["format"] == "knitweb-lens-context"

