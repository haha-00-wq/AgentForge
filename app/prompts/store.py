from __future__ import annotations

from pathlib import Path
from typing import Any

from app.prompts.renderer import render_prompt


class PromptStore:
    def __init__(self, root: Path | str = "prompts") -> None:
        self.root = Path(root)

    def load(self, domain: str, name: str) -> str:
        path = self.root / domain / f"{name}.md"
        return path.read_text(encoding="utf-8")

    def render(self, domain: str, name: str, variables: dict[str, Any]) -> str:
        return render_prompt(self.load(domain, name), variables)

