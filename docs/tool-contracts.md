# Tool Contracts

Tool and resource contracts are documented test-first as the project grows.

This file distinguishes between core filesystem functions and MCP tool wrappers.
Core functions may accept `corpus_dir` for tests and local use. MCP tool
wrappers do not expose `corpus_dir`; they use the default corpus directory and
delegate to the core functions.

## save_markdown(name, markdown, corpus_dir=None)

Purpose: save user-provided Markdown into the local corpus as source, summary, and sidecar files.

Behavior:

- Uses `corpus_dir` when provided; otherwise uses `DEFAULT_CORPUS_DIR`.
- Writes `sources/<normalized-name>.md`, `summaries/<normalized-name>.md`, and `sidecars/<normalized-name>.toml`.
- Preserves the source Markdown exactly.
- Writes a deterministic first/last-line summary.
- Writes sidecar fields `name` and `source_kind = "manual_md"`.
- Rejects invalid names, empty Markdown, and duplicate target files.

Success returns `status: "ok"` with normalized `name`, `source_path`, `summary_path`, and `sidecar_path`.

Errors return `status: "error"` with one of: `invalid_name`, `invalid_markdown`, `already_exists`.

### MCP wrapper: `save_markdown_tool(name, markdown)`

Exposes `save_markdown` through MCP.

- Delegates to `save_markdown(name, markdown)`.
- Does not expose `corpus_dir` at the MCP boundary.
- Returns the same structured envelope as the core function.

---

## list_summaries(corpus_dir=None)

Purpose: list saved summary names from the local corpus.

Inputs:

- `corpus_dir`: optional corpus directory. When omitted, uses `DEFAULT_CORPUS_DIR`.

Behavior:

- Reads Markdown files from `<corpus_dir>/summaries/*.md`.
- Returns file names without the `.md` suffix.
- Sorts names alphabetically.
- Ignores non-Markdown files.
- Returns an empty list when `corpus_dir` or `summaries/` does not exist.

Success envelope:

    {
      "status": "ok",
      "message": "Listed summaries.",
      "data": {"names": ["example"]}
    }

### MCP wrapper: `list_summaries_tool()`

Exposes `list_summaries` through MCP.

- Delegates to `list_summaries()`.
- Exposes no parameters at the MCP boundary.
- Returns the same structured envelope as the core function.

---

## read_summary(name, corpus_dir=None)

Purpose: read one saved summary from the local corpus.

Inputs:

- `name`: logical corpus item name. It is validated with the same name rules as
  `save_markdown`.
- `corpus_dir`: optional corpus directory. When omitted, uses `DEFAULT_CORPUS_DIR`.

Behavior:

- Rejects invalid names before building any path.
- Reads only `<corpus_dir>/summaries/<normalized-name>.md`.
- Returns Markdown content without exposing local filesystem paths.
- Returns `not_found` when the summary file does not exist.

Success envelope:

    {
      "status": "ok",
      "message": "Read summary.",
      "data": {"name": "example", "content": "# Example\n"}
    }

Errors return `status: "error"` with one of: `invalid_name`, `not_found`.
Error messages do not include local filesystem paths.

### MCP resource: `summary://{name}`

Exposes saved summaries as readable Markdown resources.

- `{name}` is a logical corpus item name, not a filesystem path.
- Delegates to `read_summary(name)`.
- Reuses the same name validation rules as corpus tools.
- Reads only `summaries/<normalized-name>.md` from the configured corpus directory.
- Does not expose `corpus_dir` at the MCP boundary.
- Success returns the summary Markdown content only.
- Invalid or missing summaries return a short path-free error string such as `invalid_name: ...` or `not_found: ...`.
- Local filesystem paths are not exposed in resource output.
