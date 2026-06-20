import json

from knitweb_lens.cli import main


def test_cli_query_json(tmp_path, capsys):
    path = tmp_path / "note.md"
    path.write_text("Lens cites source chunks.", encoding="utf-8")

    code = main(["query", "What cites source chunks?", str(path), "--json"])

    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["citations"]
    assert payload["session"]["ranked_chunks"]

