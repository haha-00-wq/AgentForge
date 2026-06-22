from __future__ import annotations

from typing import Any


def render_prompt(template: str, variables: dict[str, Any]) -> str:
    """渲染 Prompt 字符串模板。

    入参:
        template: 包含 {变量名} 占位符的模板字符串。
        variables: 替换占位符的变量字典。

    出参:
        str: format 后的 Prompt 文本。
    """
    return template.format(**variables)
