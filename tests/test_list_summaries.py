from mcp_corpus import config
from mcp_corpus.corpus import list_summaries


def test_list_summaries_returns_sorted_markdown_names(tmp_path):
    summaries_dir = tmp_path / "summaries"
    summaries_dir.mkdir()
    (summaries_dir / "zeta.md").write_text("Zeta\n", encoding="utf-8")
    (summaries_dir / "alpha.md").write_text("Alpha\n", encoding="utf-8")
    (summaries_dir / "notes.txt").write_text("Ignore me\n", encoding="utf-8")

    result = list_summaries(tmp_path)

    assert result == {
        "status": "ok",
        "message": "Listed summaries.",
        "data": {"names": ["alpha", "zeta"]},
    }


def test_list_summaries_returns_empty_list_when_directory_is_missing(tmp_path):
    assert list_summaries(tmp_path) == {
        "status": "ok",
        "message": "Listed summaries.",
        "data": {"names": []},
    }


def test_list_summaries_uses_default_corpus_dir_when_omitted(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "DEFAULT_CORPUS_DIR", tmp_path)
    summaries_dir = tmp_path / "summaries"
    summaries_dir.mkdir()
    (summaries_dir / "Default_Dir.md").write_text("Default\n", encoding="utf-8")

    assert list_summaries() == {
        "status": "ok",
        "message": "Listed summaries.",
        "data": {"names": ["Default_Dir"]},
    }
