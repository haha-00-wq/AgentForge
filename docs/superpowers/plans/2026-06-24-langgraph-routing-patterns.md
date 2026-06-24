# LangGraph Routing Patterns Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add platform wrappers and examples for single-agent, conditional, agent-router, and parallel LangGraph workflows.

**Architecture:** Keep platform wrappers in `app/workflows/` and runnable business examples in `plugins/workflows/`. Use local deterministic agents so tests pass without external API keys.

**Tech Stack:** Python 3.11, LangGraph, Pydantic v2, Pytest.

---

### Task 1: Tests First

- [ ] Add tests for single, conditional, agent-router, and parallel workflows.
- [ ] Run focused tests and confirm missing modules fail.

### Task 2: Platform Builders

- [ ] Add `app/workflows/conditional.py`.
- [ ] Add `app/workflows/parallel.py`.
- [ ] Export helpers from `app/workflows/__init__.py`.

### Task 3: Business Examples

- [ ] Add `plugins/agents/router_agent.py`.
- [ ] Add `single_research_workflow.py`.
- [ ] Add `conditional_intel_workflow.py`.
- [ ] Add `agent_router_workflow.py`.
- [ ] Add `parallel_intel_workflow.py`.
- [ ] Register new plugins in `plugin_loader.py`.

### Task 4: Docs And Verification

- [ ] Update README workflow section.
- [ ] Run full pytest.
- [ ] Commit and push if verification passes.

