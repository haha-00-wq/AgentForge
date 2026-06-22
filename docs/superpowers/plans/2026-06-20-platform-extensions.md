# Platform Extensions MVP Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add local-first RAG, Memory, Tracing, Evaluation, Human-in-the-loop, and Persistence extension points to AgentForge.

**Architecture:** Add focused platform modules under `app/` and plugin examples under `plugins/`. Default implementations stay in-memory or SQLite so tests and API usage work without external services. External providers remain configuration-backed extension points.

**Tech Stack:** Python 3.11, Pydantic v2, LangGraph, FastAPI, SQLite stdlib, Pytest.

---

### Task 1: Tests First

**Files:**
- Create: `tests/test_rag.py`
- Create: `tests/test_memory.py`
- Create: `tests/test_persistence.py`
- Create: `tests/test_tracing.py`
- Create: `tests/test_evaluation.py`
- Create: `tests/test_human_review_workflow.py`

- [ ] Write behavior tests for all six extensions.
- [ ] Run `conda run -n agentforge pytest tests/test_rag.py tests/test_memory.py tests/test_persistence.py tests/test_tracing.py tests/test_evaluation.py tests/test_human_review_workflow.py`.
- [ ] Confirm tests fail because modules are missing.

### Task 2: Platform Modules

**Files:**
- Create: `app/rag/*`
- Create: `app/memory/*`
- Create: `app/persistence/*`
- Modify: `app/observability/tracing.py`
- Modify: `app/evaluation/*`
- Modify: `app/protocol/schemas.py`

- [ ] Implement minimal local-first abstractions and defaults.
- [ ] Run focused tests until green.

### Task 3: Plugins And Loader

**Files:**
- Create: `plugins/tools/retrieval_tool.py`
- Create: `plugins/workflows/human_review_workflow.py`
- Modify: `app/core/plugin_loader.py`

- [ ] Register retrieval tool and human review workflow.
- [ ] Verify catalog tests still pass.

### Task 4: Docs And Verification

**Files:**
- Modify: `README.md`

- [ ] Document new extension modules and examples.
- [ ] Run full `conda run -n agentforge pytest`.
- [ ] Commit and push to `origin/main`.
