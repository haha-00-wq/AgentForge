from __future__ import annotations

from fastapi import FastAPI

from app.api import routes_agents, routes_health, routes_knowledge, routes_tools, routes_workflows
from app.core.bootstrap import bootstrap


def create_app() -> FastAPI:
    """创建 FastAPI 应用。

    入参:
        无。

    出参:
        FastAPI: 已完成插件 bootstrap 和路由挂载的应用实例。
    """
    app = FastAPI(title="AgentForge", version="0.1.0")
    app.state.container = bootstrap()
    app.include_router(routes_health.router)
    app.include_router(routes_agents.router)
    app.include_router(routes_tools.router)
    app.include_router(routes_workflows.router)
    app.include_router(routes_knowledge.router)
    return app


app = create_app()
