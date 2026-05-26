"""FastMCP server wiring for mcp-corpus."""

from fastmcp import FastMCP

from mcp_corpus.corpus import save_markdown

mcp = FastMCP("mcp-corpus")


@mcp.tool
def save_markdown_tool(name: str, markdown: str):
    """Save user-provided Markdown into the local corpus.

    Use this when the user wants to persist Markdown for later corpus access.
    Writes source, summary, and sidecar files. Returns a structured status
    envelope; full contract is documented in docs/tool-contracts.md.
    """
    return save_markdown(name, markdown)


if __name__ == "__main__":
    mcp.run()
