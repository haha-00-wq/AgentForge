from __future__ import annotations

from fastapi import FastAPI

from app.api import routes_agents, routes_health, routes_tools, routes_workflows
from app.core.bootstrap import bootstrap


def create_app() -> FastAPI:
    app = FastAPI(title="AgentForge", version="0.1.0")
    app.state.container = bootstrap()
    app.include_router(routes_health.router)
    app.include_router(routes_agents.router)
    app.include_router(routes_tools.router)
    app.include_router(routes_workflows.router)
    return app


app = create_app()
