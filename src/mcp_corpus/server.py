"""FastMCP server wiring for mcp-corpus."""

from fastmcp import FastMCP

from mcp_corpus.corpus import list_summaries, save_markdown

mcp = FastMCP("mcp-corpus")


@mcp.tool
def save_markdown_tool(name: str, markdown: str):
    """Save user-provided Markdown into the local corpus.

    Use this when the user wants to persist Markdown for later corpus access.
    Writes source, summary, and sidecar files. Returns a structured status
    envelope; full contract is documented in docs/tool-contracts.md.
    """
    return save_markdown(name, markdown)


@mcp.tool
def list_summaries_tool():
    """List saved summary names from the local corpus.

    Use this when the user needs to discover saved corpus summaries. Returns a
    structured status envelope; full contract is documented in docs/tool-contracts.md.
    """
    return list_summaries()


if __name__ == "__main__":
    mcp.run()
