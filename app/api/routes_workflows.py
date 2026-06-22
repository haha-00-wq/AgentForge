from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Request

router = APIRouter()


@router.get("/workflows")
def list_workflows(request: Request) -> list[dict[str, str]]:
    """列出已注册 Workflow。

    入参:
        request: FastAPI 请求对象，从 request.app.state.container 读取注册表。

    出参:
        list[dict[str, str]]: Workflow 元信息列表。
    """
    return request.app.state.container.workflows.list()


@router.post("/workflows/{workflow_id}/run")
def run_workflow(workflow_id: str, payload: dict[str, Any], request: Request):
    """运行指定 Workflow。

    入参:
        workflow_id: 路径参数，目标 Workflow 的唯一标识。
        payload: 请求体，作为 Workflow.run(payload) 的输入。
        request: FastAPI 请求对象，用于访问 workflow 注册表。

    出参:
        WorkflowResult: 指定 Workflow 的结构化执行结果。

    异常:
        HTTPException(404): workflow_id 未注册时返回。
    """
    try:
        workflow = request.app.state.container.workflows.get(workflow_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Workflow not found: {workflow_id}") from exc
    return workflow.run(payload)
