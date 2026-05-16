# AGENTS.md — mcp-corpus

## Project purpose

This is a small personal public MCP corpus project.

The repo should remain:

- small
- clean
- boring
- tested
- easy to explain
- public-safe
- not overbuilt

The project demonstrates MCP tool/resource workflows around corpus ingestion, discovery, and readable resources.

## Hard constraints

- Do not introduce private, company-specific, or prior prototype-specific context.
- Do not add RAG, vector indexing, deployment, auth, remote hosting, or broad client support unless explicitly requested.
- Do not add dependencies without a short justification.
- Do not create extra modules before they are useful.
- Do not implement beyond the approved slice.
- Do not silently change project structure, tool names, contracts, or public behavior.

## Required development workflow

For every development slice, follow this process.

### 1. Restate the slice first

Before editing files, restate:

- requested behavior
- expected inputs
- expected outputs
- side effects
- failure cases
- explicit out-of-scope items

If any of these are missing, stop and produce a proposed contract instead of implementing.

### 2. Suggest missing cases before writing tests

Before writing or changing tests, suggest missing cases and classify them as:

- must-have for this slice
- nice-to-have later
- out of scope

Wait for approval unless the user explicitly asks you to proceed directly.

### 3. Tests before implementation

Write or update tests before production code.

For each slice:

- define expected behavior first
- add tests for approved cases
- run tests
- confirm they fail for the expected reason
- only then implement production code

### 4. Minimal implementation

Implement only enough code to satisfy the approved tests.

Avoid:

- broad refactors
- speculative abstractions
- extra features
- hidden behavior changes
- large rewrites

### 5. Report and stop

After each slice, report:

- files changed
- commands run
- test results
- any unresolved issue or assumption

Then stop.

## Testing rules

- Prefer behavior/contract tests over implementation-detail tests.
- Use fixtures or golden files when they make expected behavior clearer.
- Use real temporary filesystem directories for filesystem behavior.
- Mock only external boundaries such as network calls.
- Do not mock internal helpers just to make tests pass.
- Add property tests only when validators or parsers have stable rules worth checking across many generated inputs.

## MCP design rules

- Keep `server.py` thin: MCP wrappers only.
- Tool docstrings must be routing-complete but contract-light.
- Full schemas, edge cases, examples, and error codes belong in docs and tests.
- Use stable structured result envelopes at the MCP boundary.
- Prefer typed internal results, such as dataclasses, when return values become non-trivial.
- Convert internal results to dictionaries only at the MCP boundary when needed.
- Tools perform actions.
- Resources expose readable context.

## Style rules

- Split modules by concern, not by vague role.
- Keep functions short and explicit.
- Prefer clear names over clever abstractions.
- Avoid one large `tools.py`-style module.
- Keep README and public docs concise.
- Do not duplicate long contracts in both docstrings and docs.
- Lazy-import heavy or optional dependencies only where needed.
