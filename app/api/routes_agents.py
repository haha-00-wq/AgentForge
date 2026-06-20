from __future__ import annotations

from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/agents")
def list_agents(request: Request) -> list[dict[str, str]]:
    return request.app.state.container.agents.list()

