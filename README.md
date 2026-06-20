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
SQLITE_PATH=data/osintbase.db
POSTGRES_DSN=
REDIS_URL=
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
curl -X POST http://127.0.0.1:8000/workflows/human_review_v1/run \
  -H "Content-Type: application/json" \
  -d '{"run_id":"r1","content":"Needs review"}'
```

## 平台扩展能力

第二阶段已加入本地优先的扩展模块。默认实现不依赖外部服务，适合作为业务项目的可替换底座。

### RAG

- 模块：`app/rag/`
- 默认实现：`SimpleEmbeddingModel` + `InMemoryVectorStore`
- 示例插件：`plugins/tools/retrieval_tool.py`

业务可以先用内存向量库跑通检索流程，后续再把 `InMemoryVectorStore` 替换为 Chroma、FAISS、Milvus 或其他向量库。

### Memory

- 模块：`app/memory/`
- 默认实现：`InMemoryMemoryStore`
- 能力：session state、long-term memory、user profile

适合保存对话状态、长期偏好、用户画像等 Agent 上下文信息。生产环境可以替换为数据库或 Redis 实现。

### Tracing

- 模块：`app/observability/tracing.py`
- 入口：`trace_run()` 和 `configure_tracing()`
- 默认行为：`LANGSMITH_TRACING=false` 时 no-op

开启 LangSmith 时，配置 `.env`：

```bash
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your-key
```

### Evaluation

- 模块：`app/evaluation/`
- 支持：JSONL dataset、评分器、批量评估 CLI

示例命令：

```bash
python -m app.evaluation.cli examples/evaluation/sample.jsonl --field label
```

### Human-in-the-loop

- 示例 workflow：`plugins/workflows/human_review_workflow.py`
- workflow id：`human_review_v1`
- 行为：没有 approval 时返回 `pending`，传入 approval 后返回审核结果。

Pending 示例：

```bash
curl -X POST http://127.0.0.1:8000/workflows/human_review_v1/run \
  -H "Content-Type: application/json" \
  -d '{"run_id":"r1","content":"Needs review"}'
```

Resume 示例：

```bash
curl -X POST http://127.0.0.1:8000/workflows/human_review_v1/run \
  -H "Content-Type: application/json" \
  -d '{"run_id":"r1","content":"Needs review","approval":{"approved":true,"reviewer":"alice"}}'
```

### Persistence

- 模块：`app/persistence/`
- 默认实现：`SQLitePersistenceStore`
- 能力：run 记录、cache、queue

SQLite 用作默认本地持久化，Postgres 和 Redis 作为后续生产实现的替换方向。

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

- RAG：接入 Chroma、FAISS、Milvus 等真实向量库。
- Memory：增加数据库和 Redis 后端。
- Tracing：补充更细粒度的 LangSmith run metadata。
- Evaluation：增加 LLM-as-judge、回归评估报告和 CI 集成。
- Human-in-the-loop：接入真实审批 API、通知和恢复令牌。
- Persistence：增加 Postgres/Redis 生产实现。
