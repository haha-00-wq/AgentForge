# Platform Extensions MVP Design

## 背景

AgentForge 第一阶段已经具备 Agent、Tool、Workflow、Prompt、LLM 工厂、协议模型、FastAPI 和情报分析示例。第二阶段要把 README 路线图中的 RAG、Memory、Tracing、Evaluation、Human-in-the-loop 和 Persistence 加进平台层，但仍保持默认可本地运行、可测试、无外部服务强依赖。

## 设计原则

- 平台层先定义稳定抽象，默认实现使用内存或 SQLite。
- 业务插件通过 `plugins/` 接入新增能力，不直接依赖具体存储或外部服务。
- LangSmith、Postgres、Redis、真实向量库作为可配置扩展点，不作为默认测试依赖。
- 每个子系统都有最小测试覆盖，确保 clone 后无 API key 也能跑通。

## 子系统设计

### RAG

新增 `app/rag/`：

- `Document`：统一文档片段模型。
- `SimpleEmbeddingModel`：本地可测试的哈希词袋 embedding。
- `InMemoryVectorStore`：内存向量库，支持 add/search。
- `Retriever`：封装检索入口。

新增 `plugins/tools/retrieval_tool.py`，把 RAG 检索暴露为业务 Tool。

### Memory

新增 `app/memory/`：

- `SessionStateStore`：会话状态存取。
- `LongTermMemoryStore`：长期记忆追加和查询。
- `UserProfileStore`：用户画像 upsert/get。
- 默认 `InMemoryMemoryStore` 聚合三类能力。

### Persistence

新增 `app/persistence/`：

- `RunRecord`：运行记录模型。
- `CacheEntry`：缓存模型。
- `QueueItem`：队列模型。
- `SQLitePersistenceStore`：默认 SQLite 实现。

Postgres/Redis 暂以配置字段和抽象接口保留，不在 MVP 中引入驱动依赖。

### Tracing

增强 `app/observability/tracing.py`：

- `TraceContext`：记录 run_name、metadata、enabled。
- `trace_run()`：上下文管理器。LangSmith 关闭时本地 no-op；开启时设置 LangSmith 环境变量并保留扩展入口。

### Evaluation

扩展 `app/evaluation/`：

- `EvaluationCase`：评估用例模型。
- `load_jsonl_dataset()`：加载 JSONL dataset。
- `ExactMatchScorer` 和 `SupportedReviewScorer`。
- `run_batch_evaluation()`。
- `app/evaluation/cli.py` 提供 `python -m app.evaluation.cli <dataset>`。

### Human-in-the-loop

新增 `plugins/workflows/human_review_workflow.py`：

- 基于 LangGraph 节点组织人工审核流程。
- 首次运行没有 approval 时返回 `pending_approval`。
- 传入 `approval` 后返回 `approved` 或 `rejected`。

协议层状态扩展为 `success/error/pending`，避免 pending 审核被误标记为失败。

## 测试策略

- RAG：验证文档入库和检索排序。
- Retrieval Tool：验证业务 Tool 返回结构化检索结果。
- Memory：验证 session、长期记忆、用户画像。
- Persistence：验证 SQLite run/cache/queue。
- Tracing：验证关闭时 no-op、开启时上下文 metadata 可用。
- Evaluation：验证 dataset 加载、评分器和批量评估。
- HITL：验证 pending 和 approval 两条路径。

## 交付边界

本阶段不引入 Chroma、FAISS、Milvus、Postgres、Redis 的真实客户端依赖；只提供可替换接口、配置字段和本地默认实现。这样第二阶段仍然是可运行脚手架，而不是依赖外部基础设施的半成品。
