from pathlib import Path


def test_save_markdown_writes_files_and_ok_envelope(tmp_path):
    from mcp_corpus.corpus import save_markdown

    markdown = "\n\n# First line\n\nBody text\n\nFinal line\n\n"

    result = save_markdown("Note_1", markdown, tmp_path)

    source_path = tmp_path / "sources" / "Note_1.md"
    summary_path = tmp_path / "summaries" / "Note_1.md"
    sidecar_path = tmp_path / "sidecars" / "Note_1.toml"

    assert result == {
        "status": "ok",
        "message": "Saved Markdown item.",
        "data": {
            "name": "Note_1",
            "source_path": str(source_path),
            "summary_path": str(summary_path),
            "sidecar_path": str(sidecar_path),
        },
    }

    assert source_path.read_text(encoding="utf-8") == markdown
    assert summary_path.read_text(encoding="utf-8") == "# First line\n\nFinal line\n"
    assert 'name = "Note_1"' in sidecar_path.read_text(encoding="utf-8")


def test_save_markdown_rejects_unsafe_name_and_writes_nothing(tmp_path):
    from mcp_corpus.corpus import save_markdown

    result = save_markdown("../unsafe", "# Title\n", tmp_path)

    assert result == {
        "status": "error",
        "error_code": "invalid_name",
        "message": "Invalid corpus item name.",
        "data": {},
    }
    assert list(tmp_path.rglob("*")) == []


def test_save_markdown_rejects_empty_markdown_and_writes_nothing(tmp_path):
    from mcp_corpus.corpus import save_markdown

    result = save_markdown("Valid_Name", " \n\t\n", tmp_path)

    assert result == {
        "status": "error",
        "error_code": "invalid_markdown",
        "message": "Markdown content is empty.",
        "data": {},
    }
    assert list(tmp_path.rglob("*")) == []


def test_save_markdown_rejects_duplicate_name_without_overwriting(tmp_path):
    from mcp_corpus.corpus import save_markdown

    first = save_markdown("Duplicate", "# Original\n", tmp_path)
    source_path = Path(first["data"]["source_path"])

    result = save_markdown("Duplicate", "# Replacement\n", tmp_path)

    assert result == {
        "status": "error",
        "error_code": "already_exists",
        "message": "Corpus item already exists.",
        "data": {},
    }
    assert source_path.read_text(encoding="utf-8") == "# Original\n"


def test_save_markdown_summary_uses_single_line_when_first_and_last_match(tmp_path):
    from mcp_corpus.corpus import save_markdown

    result = save_markdown("Single_Line", "\nOnly line\n\n", tmp_path)

    summary_path = Path(result["data"]["summary_path"])
    assert summary_path.read_text(encoding="utf-8") == "Only line\n"


def test_validate_name_strips_whitespace_and_rejects_unsafe_names():
    from mcp_corpus.validation import validate_name

    valid = validate_name("  Report_1-2  ")

    assert valid.ok is True
    assert valid.normalized_name == "Report_1-2"

    for name in ["", "two words", "path/name", r"path\name", "../name", "name.md", "name!"]:
        result = validate_name(name)
        assert result.ok is False
        assert result.error_code == "invalid_name"
