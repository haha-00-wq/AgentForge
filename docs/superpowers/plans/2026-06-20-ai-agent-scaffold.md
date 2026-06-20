# AI Agent Scaffold Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a minimum viable LangChain/LangGraph-based AI Agent application scaffold with pluginized agents, tools, workflows, prompts, API routes, tests, and documentation.

**Architecture:** The scaffold separates platform code under `app/` from business plugins under `plugins/`. Platform modules provide registries, protocol schemas, prompt rendering, model factory, LangChain tool adapters, and a LangGraph-backed workflow runner. The first business example is an intelligence analysis workflow implemented as three agents and one sample tool.

**Tech Stack:** Python 3.11+, FastAPI, Pydantic v2, LangChain, LangGraph, Uvicorn, Pytest, python-dotenv.

---

### Task 1: Project Metadata And Tests

**Files:**
- Create: `pyproject.toml`
- Create: `environment.yml`
- Create: `.env.example`
- Create: `tests/test_agents.py`
- Create: `tests/test_tools.py`
- Create: `tests/test_workflows.py`
- Create: `tests/test_api.py`

- [x] **Step 1: Write failing tests**

Tests assert the desired public behavior before platform modules exist.

- [x] **Step 2: Run tests to verify they fail**

Run: `pytest`
Expected: import failures for missing `app` and `plugins` modules.

### Task 2: Platform Core

**Files:**
- Create: protocol, registries, base classes, prompt store, LLM factory, plugin loader, tracing stub.

- [x] **Step 1: Implement minimal platform interfaces**

Expose stable base classes and registry APIs used by plugins and tests.

- [x] **Step 2: Run focused tests**

Run: `pytest tests/test_agents.py tests/test_tools.py`
Expected: pass after plugins are present.

### Task 3: Business Plugins And Workflow

**Files:**
- Create: `plugins/agents/*.py`
- Create: `plugins/tools/search_tool.py`
- Create: `plugins/workflows/intel_analysis_workflow.py`
- Create: prompt and example JSON files.

- [x] **Step 1: Implement mock-runnable intelligence analysis plugins**

Agents produce structured results without a real API key by default.

- [x] **Step 2: Run workflow tests**

Run: `pytest tests/test_workflows.py`
Expected: pass with LangGraph sequential execution.

### Task 4: FastAPI And Documentation

**Files:**
- Create: `app/main.py`
- Create: `app/api/routes_*.py`
- Create: `README.md`

- [x] **Step 1: Implement base routes**

Expose `/health`, `/agents`, `/tools`, `/workflows`, and workflow execution.

- [x] **Step 2: Run API tests and full suite**

Run: `pytest`
Expected: all tests pass.

