from mcp_corpus.validation import validate_name


def test_validate_name_strips_whitespace_and_rejects_unsafe_names():
    valid = validate_name("  Report_1-2  ")

    assert valid.ok is True
    assert valid.normalized_name == "Report_1-2"

    for name in ["", "two words", "path/name", r"path\name", "../name", "name.md", "name!"]:
        result = validate_name(name)
        assert result.ok is False
        assert result.error_code == "invalid_name"
