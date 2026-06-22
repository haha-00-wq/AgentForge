from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    """健康检查接口。

    入参:
        无。

    出参:
        dict[str, str]: 固定返回 {"status": "ok"}。
    """
    return {"status": "ok"}
