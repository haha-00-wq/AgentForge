from __future__ import annotations

from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/tools")
def list_tools(request: Request) -> list[dict[str, str]]:
    """列出已注册 Tool。

    入参:
        request: FastAPI 请求对象，从 request.app.state.container 读取注册表。

    出参:
        list[dict[str, str]]: Tool 元信息列表。
    """
    return request.app.state.container.tools.list()
