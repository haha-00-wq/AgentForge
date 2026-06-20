from __future__ import annotations

from typing import Any


def render_prompt(template: str, variables: dict[str, Any]) -> str:
    return template.format(**variables)

