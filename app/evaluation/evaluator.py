from __future__ import annotations

from typing import Protocol

from app.evaluation.datasets import EvaluationCase
from app.protocol import EvaluationResult, WorkflowResult


class Scorer(Protocol):
    """评分器协议。

    功能:
        约束所有评分器必须提供 score(case) 方法。
    """

    def score(self, case: EvaluationCase) -> EvaluationResult:
        """评估单个用例。

        入参:
            case: EvaluationCase 评估用例。

        出参:
            EvaluationResult: 评分结果。
        """


class ExactMatchScorer:
    """字段精确匹配评分器。

    功能:
        比较 case.expected[field] 和 case.actual[field] 是否完全相等。
    """

    def __init__(self, field: str) -> None:
        """初始化评分器。

        入参:
            field: 要比较的字段名。

        出参:
            无。
        """
        self.field = field

    def score(self, case: EvaluationCase) -> EvaluationResult:
        """评估单个用例。

        入参:
            case: EvaluationCase，需在 expected 和 actual 中包含目标字段。

        出参:
            EvaluationResult: 相等时 score=1.0，否则 score=0.0。
        """
        expected = case.expected.get(self.field)
        actual = case.actual.get(self.field)
        matched = expected == actual
        return EvaluationResult(
            case_id=case.case_id,
            status="success" if matched else "error",
            score=1.0 if matched else 0.0,
            details={"field": self.field, "expected": expected, "actual": actual},
        )


class SupportedReviewScorer:
    """证据支持性评分器。

    功能:
        检查 case.actual.review.supported 是否为真。
    """

    def score(self, case: EvaluationCase) -> EvaluationResult:
        """评估单个 review 结果。

        入参:
            case: EvaluationCase，actual 中应包含 review.supported。

        出参:
            EvaluationResult: supported 为真时 score=1.0，否则 score=0.0。
        """
        supported = bool(case.actual.get("review", {}).get("supported"))
        return EvaluationResult(
            case_id=case.case_id,
            status="success" if supported else "error",
            score=1.0 if supported else 0.0,
            details={"supported": supported},
        )


def run_batch_evaluation(cases: list[EvaluationCase], scorer: Scorer) -> list[EvaluationResult]:
    """批量运行评估。

    入参:
        cases: 评估用例列表。
        scorer: 实现 Scorer 协议的评分器。

    出参:
        list[EvaluationResult]: 每个用例的评分结果。
    """
    return [scorer.score(case) for case in cases]


def evaluate_supported_review(case_id: str, result: WorkflowResult) -> EvaluationResult:
    """评估 WorkflowResult 中的 review.supported 字段。

    入参:
        case_id: 评估用例 ID。
        result: WorkflowResult，通常来自 intel_analysis_v1。

    出参:
        EvaluationResult: review.supported 为真时 score=1.0，否则 score=0.0。
    """
    supported = bool(result.data.get("review", {}).get("supported"))
    return EvaluationResult(
        case_id=case_id,
        status="success" if supported else "error",
        score=1.0 if supported else 0.0,
        details={"supported": supported},
    )
