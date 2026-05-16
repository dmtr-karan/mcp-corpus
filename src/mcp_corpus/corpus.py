"""Filesystem operations for the local corpus."""

from pathlib import Path

from mcp_corpus.envelopes import error, ok
from mcp_corpus.validation import validate_name


def save_markdown(name, markdown, corpus_dir):
    name_result = validate_name(name)
    if not name_result.ok:
        return error("invalid_name", "Invalid corpus item name.")

    if not markdown.strip():
        return error("invalid_markdown", "Markdown content is empty.")

    corpus_path = Path(corpus_dir)
    normalized_name = name_result.normalized_name
    source_path = corpus_path / "sources" / f"{normalized_name}.md"
    summary_path = corpus_path / "summaries" / f"{normalized_name}.md"
    sidecar_path = corpus_path / "sidecars" / f"{normalized_name}.toml"

    if source_path.exists() or summary_path.exists() or sidecar_path.exists():
        return error("already_exists", "Corpus item already exists.")

    source_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    sidecar_path.parent.mkdir(parents=True, exist_ok=True)

    source_path.write_text(markdown, encoding="utf-8")
    summary_path.write_text(_build_summary(markdown), encoding="utf-8")
    sidecar_path.write_text(f'name = "{normalized_name}"\n', encoding="utf-8")

    return ok(
        "Saved Markdown item.",
        {
            "name": normalized_name,
            "source_path": str(source_path),
            "summary_path": str(summary_path),
            "sidecar_path": str(sidecar_path),
        },
    )


def _build_summary(markdown):
    lines = [line.strip() for line in markdown.splitlines() if line.strip()]
    first_line = lines[0]
    last_line = lines[-1]

    if first_line == last_line:
        return f"{first_line}\n"

    return f"{first_line}\n\n{last_line}\n"
