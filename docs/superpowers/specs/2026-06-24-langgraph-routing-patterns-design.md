# LangGraph Routing Patterns Design

## 背景

当前 AgentForge 已覆盖顺序多 Agent workflow 和基础 human-in-the-loop 示例，但还缺少 LangGraph 常见编排模式：单 Agent 包装、条件分支、并行节点、Agent 决策路由。为了让业务开发者能按模板复制扩展，需要在平台层提供轻量封装，并在插件层提供可运行示例。

## 目标

- 增加条件分支封装，隐藏 `add_conditional_edges` 的样板代码。
- 增加并行 fan-out/fan-in 封装，演示多个节点并行写入不同 state key 后汇总。
- 增加单 Agent workflow 示例，作为最小业务入口。
- 增加 RouterAgent 示例，展示由 Agent 输出决定流程走向。
- 所有新增示例必须支持无真实 API key 的 mock/local 测试。

## 设计

### 平台封装

新增 `app/workflows/conditional.py`：

- `build_conditional_graph(state_schema, nodes, entrypoint, router, path_map)`。
- 用于构建带 router function 的 LangGraph。
- router 返回 path key，`path_map` 将 key 映射到目标节点或 END。

新增 `app/workflows/parallel.py`：

- `build_parallel_join_graph(state_schema, entrypoint, entry_node, parallel_nodes, join_node, finish_node)`。
- 先运行 entry 节点，再 fan-out 到多个并行节点，全部完成后进入 join 节点，最后 END。

### 业务示例

新增 `SingleResearchWorkflow`：

```text
ResearchAgent -> END
```

新增 `ConditionalIntelWorkflow`：

```text
ResearchAgent -> route
  needs_human_review -> HumanReviewWorkflow-like pending response
  analyze -> AnalystAgent -> ReviewerAgent
```

新增 `RouterAgent` 和 `AgentRouterWorkflow`：

```text
RouterAgent -> conditional edge
  analyze -> AnalystAgent
  human_review -> pending
  finish -> END
```

新增 `ParallelIntelWorkflow`：

```text
ResearchAgent
  -> entity_analysis
  -> risk_analysis
  -> source_check
join -> final result
```

## 测试

- 单 Agent workflow 返回 `single_research_v1` 和 `research` 数据。
- 条件 workflow 在普通输入下走分析分支，在包含 `needs human review` 的输入下返回 pending。
- Agent router workflow 根据 payload 中的 `route_hint` 走 analyze、human_review、finish。
- 并行 workflow 返回 entity/risk/source 三类分析，并在 join 结果中汇总。

## 边界

本阶段不引入真实异步任务队列，也不引入外部 LLM 决策。RouterAgent 采用可测试的规则/输入提示模拟 Agent 决策，后续可替换为真实 LLM structured output。

