from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


class EvaluationCase(BaseModel):
    """评估用例模型。

    入参字段:
        case_id: 用例唯一标识。
        input: 被评估对象的输入。
        expected: 期望输出或标签。
        actual: 实际输出或标签，默认空字典。
    """

    case_id: str
    input: dict[str, Any] = Field(default_factory=dict)
    expected: dict[str, Any] = Field(default_factory=dict)
    actual: dict[str, Any] = Field(default_factory=dict)


def load_json_case(path: Path | str) -> dict[str, Any]:
    """加载单个 JSON 用例文件。

    入参:
        path: JSON 文件路径。

    出参:
        dict[str, Any]: JSON 文件反序列化后的字典。
    """
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_jsonl_dataset(path: Path | str) -> list[EvaluationCase]:
    """加载 JSONL 评估数据集。

    入参:
        path: JSONL 文件路径。每一行应能解析为 EvaluationCase。

    出参:
        list[EvaluationCase]: 评估用例列表。
    """
    cases: list[EvaluationCase] = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.strip():
            cases.append(EvaluationCase.model_validate(json.loads(line)))
    return cases
