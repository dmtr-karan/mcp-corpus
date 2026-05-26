# Black-Box Client Verification

This note records a small black-box MCP client check for the current server
surface.

## Verified Setup

- Client: Codex CLI launched from `/tmp`
- Server registration: `mcp-corpus` configured in `~/.codex/config.toml`
- Server command: `.venv/bin/python -m mcp_corpus.server`
- Optional VS Code workspace configuration: `.vscode/mcp.json`

## Verified Tool

- `save_markdown_tool`

The tool was called through the MCP client and returned the same structured
envelope shape as the local `save_markdown` function.

## Verified Output

The tool created the expected corpus files under `~/Desktop/docs`:

- `sources/`
- `summaries/`
- `sidecars/`

## Current Scope

`save_markdown_tool` is the only currently documented MCP tool. `list_summaries`
remains a local filesystem function and is not exposed as an MCP tool in this
slice.
