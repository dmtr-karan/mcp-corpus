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
