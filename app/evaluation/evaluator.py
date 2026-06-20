from __future__ import annotations

from typing import Protocol

from app.evaluation.datasets import EvaluationCase
from app.protocol import EvaluationResult, WorkflowResult


class Scorer(Protocol):
    def score(self, case: EvaluationCase) -> EvaluationResult:
        """Score one evaluation case."""


class ExactMatchScorer:
    def __init__(self, field: str) -> None:
        self.field = field

    def score(self, case: EvaluationCase) -> EvaluationResult:
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
    def score(self, case: EvaluationCase) -> EvaluationResult:
        supported = bool(case.actual.get("review", {}).get("supported"))
        return EvaluationResult(
            case_id=case.case_id,
            status="success" if supported else "error",
            score=1.0 if supported else 0.0,
            details={"supported": supported},
        )


def run_batch_evaluation(cases: list[EvaluationCase], scorer: Scorer) -> list[EvaluationResult]:
    return [scorer.score(case) for case in cases]


def evaluate_supported_review(case_id: str, result: WorkflowResult) -> EvaluationResult:
    supported = bool(result.data.get("review", {}).get("supported"))
    return EvaluationResult(
        case_id=case_id,
        status="success" if supported else "error",
        score=1.0 if supported else 0.0,
        details={"supported": supported},
    )
