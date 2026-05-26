import inspect

from fastmcp import FastMCP
from fastmcp.resources import ResourceResult

from mcp_corpus import server


def test_server_exposes_fastmcp_app():
    assert isinstance(server.mcp, FastMCP)


def test_save_markdown_tool_signature_does_not_expose_corpus_dir():
    signature = inspect.signature(server.save_markdown_tool)

    assert list(signature.parameters) == ["name", "markdown"]


def test_save_markdown_tool_delegates_to_save_markdown(monkeypatch):
    expected = {
        "status": "ok",
        "message": "Saved Markdown item.",
        "data": {"name": "Note"},
    }
    calls = []

    def fake_save_markdown(name, markdown):
        calls.append((name, markdown))
        return expected

    monkeypatch.setattr(server, "save_markdown", fake_save_markdown)

    result = server.save_markdown_tool("Note", "# Title\n")

    assert result == expected
    assert calls == [("Note", "# Title\n")]


def test_list_summaries_tool_signature_does_not_expose_corpus_dir():
    signature = inspect.signature(server.list_summaries_tool)

    assert list(signature.parameters) == []


def test_list_summaries_tool_delegates_to_list_summaries(monkeypatch):
    expected = {
        "status": "ok",
        "message": "Listed summaries.",
        "data": {"names": ["alpha", "zeta"]},
    }
    calls = []

    def fake_list_summaries():
        calls.append(())
        return expected

    monkeypatch.setattr(server, "list_summaries", fake_list_summaries)

    result = server.list_summaries_tool()

    assert result == expected
    assert calls == [()]


def test_read_summary_resource_signature_does_not_expose_corpus_dir():
    signature = inspect.signature(server.read_summary_resource)

    assert list(signature.parameters) == ["name"]


def test_read_summary_resource_returns_summary_content(monkeypatch):
    calls = []

    def fake_read_summary(name):
        calls.append(name)
        return {
            "status": "ok",
            "message": "Read summary.",
            "data": {"name": "Note", "content": "# Note\n"},
        }

    monkeypatch.setattr(server, "read_summary", fake_read_summary)

    result = server.read_summary_resource("Note")

    assert isinstance(result, ResourceResult)
    assert len(result.contents) == 1
    assert result.contents[0].content == "# Note\n"
    assert result.contents[0].mime_type == "text/markdown"
    assert calls == ["Note"]


def test_read_summary_resource_returns_path_free_error_message(monkeypatch):
    def fake_read_summary(name):
        return {
            "status": "error",
            "error_code": "not_found",
            "message": "Summary not found.",
            "data": {},
        }

    monkeypatch.setattr(server, "read_summary", fake_read_summary)

    result = server.read_summary_resource("Missing")

    assert result == "not_found: Summary not found."
    assert "/" not in result
