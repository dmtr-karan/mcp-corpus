# mcp-corpus

A small, public-safe corpus project for experimenting with MCP-style ingestion,
discovery, and readable resource workflows.

The project is intentionally early and boring. Today it provides tested local
filesystem functions for saving Markdown into a corpus layout and listing saved
summaries. The current MCP tools are wired through FastMCP.

## Current functions

The current behavior lives in `src/mcp_corpus/corpus.py`.

### `save_markdown(name, markdown, corpus_dir=None)`

Saves user-provided Markdown into a local corpus.

It writes:

- `sources/<name>.md`
- `summaries/<name>.md`
- `sidecars/<name>.toml`

The source Markdown is preserved exactly. The summary is deterministic and uses
the first and last non-empty lines. The sidecar records the normalized name and
`source_kind = "manual_md"`.

Returns a structured envelope with `status`, `message`, and `data`. Validation
errors use `status: "error"` and an `error_code`.

### `list_summaries(corpus_dir=None)`

Lists saved summary names from `<corpus_dir>/summaries/*.md`.

It returns names without the `.md` suffix, sorted alphabetically. Missing corpus
or summary directories return an empty list.

## Setup

Requires Python 3.12 or newer.

```bash
python -m venv .venv
.venv/bin/python -m pip install -e ".[dev]"
```

## Tests

When `.venv/` exists, run:

```bash
.venv/bin/python -m pytest
```

## MCP server

Run the local FastMCP server with:

```bash
.venv/bin/python -m mcp_corpus.server
```

Currently wired MCP tools:

- `save_markdown_tool(name, markdown)`
- `list_summaries_tool()`

The MCP tool wrappers use the default local corpus directory; they do not expose
`corpus_dir` at the MCP boundary.

`.vscode/mcp.json` may be used as optional VS Code workspace MCP configuration.

## Notes

- Full current behavior is documented in `docs/tool-contracts.md` and covered by
  tests.
