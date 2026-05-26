# mcp-corpus

A small, public-safe corpus project for experimenting with MCP-style ingestion,
discovery, and readable resource workflows.

The project is intentionally early and boring. Today it provides tested local
filesystem functions for saving Markdown into a corpus layout, listing saved
summaries, and reading saved summaries. The current MCP surface is wired through
FastMCP.

## Current status

Current milestone: local Markdown corpus with two FastMCP tools and one readable
summary resource.

Implemented MCP tools:

- `save_markdown_tool(name, markdown)`
- `list_summaries_tool()`

Implemented MCP resource:

- `summary://{name}`

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

### `read_summary(name, corpus_dir=None)`

Reads one saved summary from `<corpus_dir>/summaries/<name>.md` after validating
`name` as a logical corpus item name. It returns summary content without local
filesystem paths.

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

Currently wired MCP resource:

- `summary://{name}`

The MCP-facing wrappers use the default local corpus directory; they do not
expose `corpus_dir` at the MCP boundary.

`.vscode/mcp.json` may be used as optional VS Code workspace MCP configuration.

Client support for MCP features can vary. Some clients may expose tools,
resources, and file attachments differently, so attachment-to-tool workflows may
depend on the MCP client being used.

## Notes

- Full current behavior is documented in `docs/tool-contracts.md` and covered by
  tests.
