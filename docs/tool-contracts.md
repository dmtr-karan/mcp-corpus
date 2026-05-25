# Tool Contracts

Tool and resource contracts will be documented test-first as the project grows.

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
