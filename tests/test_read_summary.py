import pytest

from mcp_corpus.corpus import read_summary


def test_read_summary_returns_existing_summary_content(tmp_path):
    summaries_dir = tmp_path / "summaries"
    summaries_dir.mkdir()
    (summaries_dir / "Note_1.md").write_text("# Note\n\nBody\n", encoding="utf-8")

    result = read_summary("Note_1", tmp_path)

    assert result == {
        "status": "ok",
        "message": "Read summary.",
        "data": {"name": "Note_1", "content": "# Note\n\nBody\n"},
    }


@pytest.mark.parametrize(
    "name",
    ["../x", "a/b", ".ssh", "/tmp/x", "..%2Fx", "summary://x"],
)
def test_read_summary_rejects_invalid_names_before_path_building(tmp_path, name):
    result = read_summary(name, tmp_path)

    assert result == {
        "status": "error",
        "error_code": "invalid_name",
        "message": "Invalid corpus item name.",
        "data": {},
    }
    assert str(tmp_path) not in repr(result)


def test_read_summary_returns_not_found_without_path_for_missing_summary(tmp_path):
    result = read_summary("Missing", tmp_path)

    assert result == {
        "status": "error",
        "error_code": "not_found",
        "message": "Summary not found.",
        "data": {},
    }
    assert str(tmp_path) not in repr(result)
