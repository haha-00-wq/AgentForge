from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from app.persistence.models import QueueItem, RunRecord


class SQLitePersistenceStore:
    """SQLite 持久化默认实现。

    功能:
        保存 Workflow run 记录、简单缓存和轻量队列。
        适合本地运行和测试，生产环境可替换为 Postgres/Redis 实现。
    """

    def __init__(self, path: Path | str) -> None:
        """初始化 SQLite 存储。

        入参:
            path: SQLite 数据库文件路径。

        出参:
            无。会自动创建父目录和必要表。
        """
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        """创建 SQLite 连接。

        入参:
            无。

        出参:
            sqlite3.Connection: 指向当前数据库文件的连接。
        """
        return sqlite3.connect(self.path)

    def _initialize(self) -> None:
        """初始化数据库表。

        入参:
            无。

        出参:
            None。确保 runs、cache、queue 三张表存在。
        """
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS runs (
                    run_id TEXT PRIMARY KEY,
                    workflow_id TEXT NOT NULL,
                    status TEXT NOT NULL,
                    payload TEXT NOT NULL,
                    result TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS cache (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS queue (
                    item_id TEXT PRIMARY KEY,
                    payload TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )

    def save_run(self, run: RunRecord) -> None:
        """保存或覆盖 Workflow 运行记录。

        入参:
            run: RunRecord 运行记录模型。

        出参:
            None。
        """
        with self._connect() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO runs(run_id, workflow_id, status, payload, result, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    run.run_id,
                    run.workflow_id,
                    run.status,
                    json.dumps(run.payload, ensure_ascii=False),
                    json.dumps(run.result, ensure_ascii=False),
                    run.created_at.isoformat(),
                ),
            )

    def get_run(self, run_id: str) -> RunRecord:
        """读取 Workflow 运行记录。

        入参:
            run_id: 运行 ID。

        出参:
            RunRecord: 对应运行记录。

        异常:
            KeyError: run_id 不存在时抛出。
        """
        with self._connect() as conn:
            row = conn.execute(
                "SELECT run_id, workflow_id, status, payload, result, created_at FROM runs WHERE run_id = ?",
                (run_id,),
            ).fetchone()
        if row is None:
            raise KeyError(run_id)
        return RunRecord(
            run_id=row[0],
            workflow_id=row[1],
            status=row[2],
            payload=json.loads(row[3]),
            result=json.loads(row[4]),
            created_at=row[5],
        )

    def set_cache(self, key: str, value: dict[str, Any]) -> None:
        """写入缓存。

        入参:
            key: 缓存键。
            value: 可 JSON 序列化的字典值。

        出参:
            None。
        """
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO cache(key, value) VALUES (?, ?)",
                (key, json.dumps(value, ensure_ascii=False)),
            )

    def get_cache(self, key: str) -> dict[str, Any] | None:
        """读取缓存。

        入参:
            key: 缓存键。

        出参:
            dict[str, Any] | None: 命中时返回缓存值，未命中返回 None。
        """
        with self._connect() as conn:
            row = conn.execute("SELECT value FROM cache WHERE key = ?", (key,)).fetchone()
        return json.loads(row[0]) if row else None

    def enqueue(self, item: QueueItem) -> None:
        """写入队列任务。

        入参:
            item: QueueItem 队列项。

        出参:
            None。
        """
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO queue(item_id, payload, status, created_at) VALUES (?, ?, ?, ?)",
                (item.item_id, json.dumps(item.payload, ensure_ascii=False), item.status, item.created_at.isoformat()),
            )

    def dequeue(self) -> QueueItem | None:
        """取出一个 queued 队列任务并标记为 done。

        入参:
            无。

        出参:
            QueueItem | None: 有任务时返回队列项，无任务时返回 None。
        """
        with self._connect() as conn:
            row = conn.execute(
                "SELECT item_id, payload, status, created_at FROM queue WHERE status = ? ORDER BY created_at LIMIT 1",
                ("queued",),
            ).fetchone()
            if row is None:
                return None
            conn.execute("UPDATE queue SET status = ? WHERE item_id = ?", ("done", row[0]))
        return QueueItem(item_id=row[0], payload=json.loads(row[1]), status=row[2], created_at=row[3])
