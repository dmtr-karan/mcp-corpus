import inspect

from fastmcp import FastMCP

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


def test_list_summaries_tool_is_not_wired_yet():
    assert not hasattr(server, "list_summaries_tool")
