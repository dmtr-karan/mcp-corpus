"""Pure validation helpers."""

from dataclasses import dataclass
import re


_VALID_NAME = re.compile(r"^[A-Za-z0-9_-]+$")


@dataclass(frozen=True)
class NameValidationResult:
    ok: bool
    normalized_name: str | None = None
    error_code: str | None = None


def validate_name(name):
    normalized_name = name.strip()

    if not normalized_name or not _VALID_NAME.fullmatch(normalized_name):
        return NameValidationResult(ok=False, error_code="invalid_name")

    return NameValidationResult(ok=True, normalized_name=normalized_name)
