from __future__ import annotations

from pathlib import Path
from typing import Any

from app.prompts.renderer import render_prompt


class PromptStore:
    """Prompt 文件仓库。

    功能:
        统一从 prompts/<domain>/<name>.md 加载 Prompt，并用变量渲染模板。
    """

    def __init__(self, root: Path | str = "prompts") -> None:
        """初始化 PromptStore。

        入参:
            root: Prompt 根目录，默认是项目下的 prompts。

        出参:
            无。
        """
        self.root = Path(root)

    def load(self, domain: str, name: str) -> str:
        """读取 Prompt 模板文件。

        入参:
            domain: Prompt 领域目录，例如 intel。
            name: Prompt 文件名，不包含 .md 后缀，例如 research。

        出参:
            str: Prompt 模板原文。
        """
        path = self.root / domain / f"{name}.md"
        return path.read_text(encoding="utf-8")

    def render(self, domain: str, name: str, variables: dict[str, Any]) -> str:
        """渲染 Prompt 模板。

        入参:
            domain: Prompt 领域目录。
            name: Prompt 文件名，不包含 .md 后缀。
            variables: 用于 str.format 的变量字典。

        出参:
            str: 渲染后的 Prompt 文本。
        """
        return render_prompt(self.load(domain, name), variables)
