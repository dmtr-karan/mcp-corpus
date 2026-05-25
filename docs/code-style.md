# Code Style — mcp-corpus

## Purpose

This document records the coding style for the `mcp-corpus` repo.

The goal is not to create a complex framework. The goal is to keep the project easy to inspect, test, explain, and extend in small controlled slices.

## Core style

Prefer:

- small modules
- small functions
- explicit names
- test-first changes
- stable public behavior
- simple data structures until complexity justifies more structure

Avoid:

- large catch-all modules
- speculative abstractions
- excessive dependencies
- hidden side effects
- broad rewrites
- implementation before contract

## Module organization

Split by concern, not by vague role.

Good module boundaries may include:

- validation
- corpus filesystem operations
- fetching
- sidecar metadata
- search/discovery
- envelope/result shaping
- MCP server wrappers

Avoid a single large module that mixes validation, IO, fetching, search, sidecars, and MCP wrappers.

`server.py` should stay thin. It should expose MCP tools/resources and delegate real work to focused functions.

## MCP tools and resources

MCP tools should do actions.

Examples:

- save content
- fetch content
- list available summaries
- search saved summaries

MCP resources should expose readable context.

Example:

- `summary://{name}`

Tool docstrings are MCP-facing. They help the client/agent decide whether and how to use the tool.

Therefore, docstrings should be routing-complete but contract-light.

A good tool docstring should explain:

- what the tool does
- when to use it
- main side effects
- result shape

It should not duplicate every edge case and schema detail.

Example style:

    Save user-provided Markdown into the local corpus as source, sidecar, and summary files.
    Use this when the user wants to persist Markdown for later list/search/resource access.
    Returns a structured status envelope; full contract is documented in docs/tool-contracts.md.

Full contracts belong in:

- `docs/tool-contracts.md`
- tests
- fixtures or golden files where useful

## Docstrings and focused tests

Public or public-ish functions should have short docstrings that explain purpose, not the full contract.

Detailed behavior, edge cases, envelope shapes, and examples belong in `docs/tool-contracts.md`, tests, and fixtures where useful. Avoid long function docstrings that duplicate those contracts.

Test files should stay focused on the behavior named by the file. When a file starts mixing separate features, split the tests by feature so failures remain easy to scan and explain.

Prefer cleanup that preserves behavior and improves only organization or readability. For these cleanup slices, run the full test suite and confirm no production behavior changed.

## Structured returns

At the MCP boundary, use stable structured envelopes.

Example shape:

    {
      "status": "ok",
      "message": "...",
      "data": {...}
    }

For errors:

    {
      "status": "error",
      "error_code": "...",
      "message": "...",
      "data": {}
    }

Avoid scattering ad-hoc dictionary literals everywhere.

Internally, prefer dataclasses once return values become non-trivial.

For example, avoid unclear tuple returns like:

    return True, "", normalized_name, path

Prefer a named result object when multiple fields are used by the caller.

Example:

    NameValidationResult(
        ok=True,
        error_code=None,
        normalized_name="example"
    )

This makes callsites easier to read and tests easier to understand.

## Callsite clarity

A callsite is the place where a function is called.

Readable callsite:

    result = validate_name(name)

    if not result.ok:
        ...

Less readable callsite:

    ok, error, normalized_name, warning = validate_name(name)

If a caller needs several values from a function, consider a dataclass.

## Duck typing and protocols

Duck typing means code accepts any object that provides the behavior it needs.

The object does not need to inherit from a specific class.

For example, a function may accept any storage object with a `write(...)` method.

Protocols can make that expectation explicit for type checkers without forcing inheritance.

Use protocols only when there is a real interchangeable interface. Do not add them prematurely.

## Validation

A validator checks whether input is acceptable.

A pure validator:

- depends only on its input
- returns a result
- does not read files
- does not write files
- does not call the network
- does not use time, randomness, or global state

Examples:

- validate a safe corpus name
- validate a Markdown payload
- validate an allowlisted raw GitHub URL

Pure validators are good candidates for focused unit tests.

Property tests may be useful later when validation rules are stable and have clear invariants.

Example invariant:

- names containing `/` or `\` are always invalid
- empty names are always invalid
- non-allowlisted URLs are always rejected

Do not add property tests before the validator rules are stable.

## Testing style

Tests should prove behavior, not implementation details.

Prefer testing:

- returned envelope shape
- files written
- duplicate handling
- validation failures
- resource output
- search/list behavior
- controlled network failure behavior

Avoid tests that only prove internal helper calls.

Use real temporary directories for filesystem behavior.

Use fixtures/golden files when exact expected output matters.

Possible fixture pattern:

    tests/fixtures/save_markdown/
      basic.md
      expected_success_envelope.json
      expected_sidecar.toml
      expected_summary.md

Golden files should be used when they make the contract clearer, not as busywork.

When a project-local `.venv/` exists, prefer `.venv/bin/python -m pytest` for reproducible test runs.

## Mocking

Mock only external boundaries.

Good boundaries to mock:

- network calls
- external APIs
- current time
- randomness
- slow optional dependencies

For example, when testing URL fetching, mock the network call such as `urlopen`.

Do not mock internal helpers such as:

- `validate_name`
- `write_sidecar`
- `build_summary`

Mocking internal helpers can make tests pass without proving the real behavior.

In pytest, `monkeypatch` can temporarily replace an external function during a test.

Use it to avoid real network calls, not to bypass the project’s own logic.

## Documentation style

Keep public docs concise.

README should explain:

- what this project is
- what MCP pattern it demonstrates
- how to run tests
- how to run or inspect the server once implemented

Detailed behavior contracts belong in `docs/tool-contracts.md`.

Flow diagrams may live in `docs/flows.md` once the flows exist.

Black-box client verification notes may live in `docs/black-box-client-verification.md` once there is something real to verify.

Avoid long historical development notes in the public repo.

## Documentation audiences

Separate human-facing documentation from agent/session memory.

Human-facing documentation is for developers, reviewers, and future readers. It should be concise, complete, and easy to scan. It should explain what the project does, how to run it, how it is structured, and how to verify it.

Agent/session memory is for preserving planning context, audit notes, implementation history, rejected options, and step-by-step handoff information. It may be longer and may duplicate some context if that helps future agent sessions.

Keep agent/session memory out of the main human documentation path.

Suggested layout:

- `README.md` — short project overview and quickstart
- `docs/architecture.md` — current architecture, not history
- `docs/tool-contracts.md` — stable public tool/resource contracts
- `docs/demo.md` or `docs/verification.md` — how to verify the current project
- `agent-notes/` — audit reports, implementation plans, session notes, historical reasoning, migration notes

Do not put long chronological development logs, agent handoff blocks, or design-history dumps in the main README or primary docs.

## Dependency style

Start with minimal dependencies.

Add a dependency only when it clearly improves the project.

Before adding one, state:

- why it is needed
- whether stdlib is enough
- whether it affects runtime or tests only

Prefer lazy imports for heavy or optional dependencies that are not needed by most code paths.

## Git style

Keep Git operations small, explicit, and easy to review.

Do not commit, push, merge, rebase, reset, or rewrite history unless the user explicitly asks for that operation.

Never delete branches. If branch cleanup would be useful, mention it as a manual follow-up only.

Suggest a new branch when work is non-trivial, risky, experimental, or logically separate from the current work, but do not create one without explicit instruction.

Suggested branch name patterns:

- `feature/<short-name>`
- `test/<short-name>`
- `docs/<short-name>`
- `chore/<short-name>`

Prefer small commits that match one logical slice.

Use concise conventional commit messages, for example:

- `docs: add git workflow rules`
- `test: cover duplicate corpus names`
- `fix: handle missing summary files`

Before committing, show `git status`, summarize staged changes, and avoid staging unrelated files.

After committing, report the commit hash and whether the working tree is clean or dirty.

For merge, rebase, reset, or other history-affecting operations, require explicit confirmation first. State the risk and a safer alternative when one exists.

## Development rhythm

Use small slices.

For each slice:

1. Define behavior.
2. Suggest missing cases.
3. Approve test scope.
4. Write failing tests.
5. Implement minimum code.
6. Run tests.
7. Review diff.
8. Commit.

The agent may suggest cases, but the human decides scope.

This is controlled agent-assisted TDD, not free-form vibe coding.
