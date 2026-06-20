import json
from pathlib import Path

from knitweb_lens import JsonLdAdapter, LocalFilesAdapter, MappingRowsAdapter, RLMHarness, VectorResultsAdapter


def test_jsonld_adapter_preserves_cid_and_edges():
    doc = {
        "@graph": [
            {
                "id": "cid:b",
                "record": {"kind": "knowledge", "title": "Beta", "body": "Pulse fabric export"},
                "edges": [{"rel": "derived-from", "dst": "cid:a", "weight": 1}],
            }
        ]
    }

    chunks = tuple(JsonLdAdapter(doc).iter_chunks())

    assert len(chunks) == 1
    assert chunks[0].ref.cid == "cid:b"
    assert chunks[0].ref.relation_path == ("derived-from->cid:a",)
    assert chunks[0].text == "Beta\n\nPulse fabric export"


def test_local_files_adapter_chunks_markdown(tmp_path):
    path = tmp_path / "note.md"
    path.write_text("Lens reads Knitweb fabric and preserves citations.", encoding="utf-8")

    chunks = tuple(LocalFilesAdapter([path]).iter_chunks())

    assert len(chunks) == 1
    assert chunks[0].title == "note.md"
    assert chunks[0].ref.source_uri == str(path)
    assert chunks[0].ref.cid.startswith("local-chunk:")


def test_mapping_rows_adapter_accepts_graph_rows():
    rows = [
        {
            "id": "n1",
            "title": "Light graph",
            "text": "Graph rows can come from Neo4j or LightRAG.",
            "path": [{"rel": "supports", "dst": "n0"}],
        }
    ]

    chunk = tuple(MappingRowsAdapter(rows).iter_chunks())[0]

    assert chunk.ref.node_id == "n1"
    assert chunk.ref.relation_path == ("supports->n0",)


def test_vector_results_quantize_float_scores_to_integer_weight():
    chunks = tuple(
        VectorResultsAdapter(
            [{"id": "v1", "score": 0.812, "payload": {"text": "Vector hit", "cid": "cid:v"}}]
        ).iter_chunks()
    )

    assert chunks[0].weight == 812
    assert isinstance(chunks[0].weight, int)


def test_pulse_web_export_fixture_round_trips_into_cited_answer():
    fixture = Path(__file__).parent / "fixtures" / "pulse_web_export.json"
    doc = json.loads(fixture.read_text(encoding="utf-8"))

    adapter = JsonLdAdapter(doc, source_id="pulse-fixture", source_uri=str(fixture))
    answer = RLMHarness().query("What derives from recycled fiber?", adapters=[adapter])

    assert "recycled fiber" in answer.text.casefold()
    refs_by_cid = {ref.cid: ref for ref in answer.citations}
    assert "bafyfinisheditem" in refs_by_cid
    assert "bafyrootmaterial" in refs_by_cid
    assert refs_by_cid["bafyfinisheditem"].relation_path == ("derived-from->bafyrootmaterial",)
