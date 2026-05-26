"""FastMCP server wiring for mcp-corpus."""

from fastmcp import FastMCP
from fastmcp.resources import ResourceContent, ResourceResult

from mcp_corpus.corpus import list_summaries, read_summary, save_markdown

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


@mcp.resource("summary://{name}", mime_type="text/markdown")
def read_summary_resource(name: str):
    """Read a saved summary as Markdown by corpus item name."""
    result = read_summary(name)
    if result["status"] == "ok":
        return ResourceResult(
            [
                ResourceContent(
                    result["data"]["content"],
                    mime_type="text/markdown",
                )
            ]
        )

    return f"{result['error_code']}: {result['message']}"


if __name__ == "__main__":
    mcp.run()
