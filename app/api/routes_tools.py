from __future__ import annotations

from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/tools")
def list_tools(request: Request) -> list[dict[str, str]]:
    return request.app.state.container.tools.list()

