from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Request

router = APIRouter()


@router.get("/workflows")
def list_workflows(request: Request) -> list[dict[str, str]]:
    return request.app.state.container.workflows.list()


@router.post("/workflows/{workflow_id}/run")
def run_workflow(workflow_id: str, payload: dict[str, Any], request: Request):
    try:
        workflow = request.app.state.container.workflows.get(workflow_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Workflow not found: {workflow_id}") from exc
    return workflow.run(payload)

