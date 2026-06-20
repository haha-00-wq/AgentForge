# OSINTBase

OSINTBase 是一个基于 LangChain / LangGraph 的 OSINT 与情报分析 Agent 应用开发底座，目标是像若依之于 Spring Boot 一样，为 AI Agent 应用提供统一的工程结构、插件规范、工作流编排、模型接入、结构化协议和可测试业务示例。

## 项目定位

LangChain / LangGraph 是底座，本项目不是重写它们，而是在其上提供业务开发者可复制的工程模板：

- `app/`：平台核心能力，包括协议、注册表、Prompt、LLM 工厂、Workflow runner 和 API。
- `plugins/`：业务 Agent、Tool、Workflow 插件。
- `prompts/`：Prompt 模板文件。
- `examples/`：示例输入输出。
- `tests/`：自动化测试。
- `docs/`：架构、计划和后续文档。

## 快速启动

```bash
conda env create -f environment.yml
conda activate osintbase
cp .env.example .env
uvicorn app.main:app --reload
```

默认 `LLM_PROVIDER=mock`，没有真实 API key 也可以运行测试和示例 workflow。

## 环境变量

```bash
LLM_PROVIDER=mock
LLM_MODEL=mock-intel
OPENAI_API_KEY=
OPENAI_BASE_URL=
ANTHROPIC_API_KEY=
OLLAMA_BASE_URL=http://localhost:11434
OPENROUTER_API_KEY=
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
LANGSMITH_TRACING=false
LANGSMITH_API_KEY=
```

`LLM_PROVIDER` 可切换为 `openai`、`openrouter`、`anthropic` 或 `ollama`。真实 provider 的客户端依赖放在可选 extras 中，例如 `pip install -e ".[openai]"`。

## 和 LangChain / LangGraph 的关系

- LLM 接入通过 LangChain 标准 ChatModel 接口。
- Tool 可以从业务 Tool 适配为 LangChain `StructuredTool`。
- 复杂工作流通过 LangGraph `StateGraph` 编排。
- 平台层负责工程规范、插件组织、统一协议和 API 暴露。

## 示例业务场景

首个示例是情报分析流程：

```text
ResearchAgent -> AnalystAgent -> ReviewerAgent
```

输入一段事件文本后，ResearchAgent 提取实体和证据，AnalystAgent 生成结构化判断，ReviewerAgent 检查判断是否有证据支持。

## API 示例

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/agents
curl http://127.0.0.1:8000/tools
curl http://127.0.0.1:8000/workflows
curl -X POST http://127.0.0.1:8000/workflows/intel_analysis_v1/run \
  -H "Content-Type: application/json" \
  -d '{"event_text":"Acme Corp opened a new lab in Berlin on Monday."}'
```

## 如何新增 Agent

1. 在 `plugins/agents/` 下新增一个继承 `BaseAgent` 的类。
2. 声明 `agent_id`、`name`、`description`、输入输出 schema。
3. 在 `run(state)` 中返回 `AgentResult`。
4. 在 `app/core/plugin_loader.py` 注册该 Agent。
5. 为它添加 prompt、示例和测试。

## 如何新增 Tool

1. 在 `plugins/tools/` 下新增一个继承 `BaseTool` 的类。
2. 声明 `tool_id`、`name`、`description`、`args_schema`。
3. 在 `run(**kwargs)` 中返回 `ToolResult`。
4. 如需给 LangChain Agent 调用，使用 `app.tools.adapters.to_langchain_tool()`。
5. 在 `app/core/plugin_loader.py` 注册该 Tool。

## 如何新增 Workflow

1. 在 `plugins/workflows/` 下新增一个继承 `BaseWorkflow` 的类。
2. 声明 `workflow_id`、`name`、`description`。
3. 使用 LangGraph 或 `run_sequential_graph()` 组织节点。
4. 返回统一的 `WorkflowResult`。
5. 在 `app/core/plugin_loader.py` 注册该 Workflow。

## 运行测试

```bash
conda activate osintbase
pytest
```

或不激活环境：

```bash
conda run -n osintbase pytest
```

## 扩展路线图

- RAG：增加向量库抽象和检索插件。
- Memory：增加会话状态、长期记忆和用户画像存储。
- Tracing：接入 LangSmith run tracing。
- Evaluation：扩展数据集、评分器和批量评估 CLI。
- Human-in-the-loop：基于 LangGraph interrupt/resume 增加人工审核节点。
- Persistence：增加 SQLite/Postgres/Redis 支持运行状态、缓存和队列。
