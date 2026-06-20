from __future__ import annotations

from app.protocol import EvaluationResult, WorkflowResult


def evaluate_supported_review(case_id: str, result: WorkflowResult) -> EvaluationResult:
    supported = bool(result.data.get("review", {}).get("supported"))
    return EvaluationResult(
        case_id=case_id,
        status="success" if supported else "error",
        score=1.0 if supported else 0.0,
        details={"supported": supported},
    )

