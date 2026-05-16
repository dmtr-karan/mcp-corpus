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

## Session handoff workflow

At session start:

- Read `AGENTS.md`.
- Read `docs/code-style.md`.
- Read `docs/tool-contracts.md` when the task touches public behavior, tool contracts, resources, or docs.
- Read `.codex/current-state.md` if it exists.
- Report current branch, git status summary, test command and latest test result if available, current task, and next recommended step.
- Do not edit files during startup unless explicitly asked.

At session end:

- Offer to create or update `.codex/current-state.md`.
- When updating it, include:
  - current branch
  - git status summary
  - test command and result
  - completed work
  - next recommended step
  - unresolved decisions or assumptions
  - suggested next-session prompt

Keep handoff notes concise, factual, and local to the current repo state.

## Testing rules

- Prefer behavior/contract tests over implementation-detail tests.
- Use fixtures or golden files when they make expected behavior clearer.
- Use real temporary filesystem directories for filesystem behavior.
- Mock only external boundaries such as network calls.
- Do not mock internal helpers just to make tests pass.
- Add property tests only when validators or parsers have stable rules worth checking across many generated inputs.
- When a project-local `.venv/` exists, run tests with `.venv/bin/python -m pytest` instead of relying on system Python or an activated shell.

## Git workflow rules

- Never commit, push, merge, rebase, or reset unless explicitly instructed.
- Never delete branches. If branch cleanup seems useful, mention it only as a human/manual follow-up.
- Do not rewrite history unless explicitly instructed and the risk has been stated.
- Do not push unless explicitly instructed.

Suggest creating a new branch when a change is non-trivial, risky, experimental, or logically separate from the current work.

Do not create a branch unless explicitly instructed.

When suggesting a branch, propose a concise name such as:

- `feature/<short-name>`
- `test/<short-name>`
- `docs/<short-name>`
- `chore/<short-name>`

Prefer small commits aligned to one logical slice.

Use concise conventional commit messages such as:

- `chore:`
- `docs:`
- `test:`
- `feat:`
- `fix:`
- `refactor:`

Before any commit:

- show `git status`
- summarize staged changes
- confirm no unrelated files are staged

Do not stage unrelated files.

After committing:

- show the commit hash
- show clean/dirty status

For merges, rebases, resets, or any history-affecting operation, require explicit confirmation.

Before proposing a merge, rebase, reset, or history rewrite, state the risk and a safer alternative if one exists.

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
