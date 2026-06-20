from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from app.persistence.models import QueueItem, RunRecord


class SQLitePersistenceStore:
    def __init__(self, path: Path | str) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.path)

    def _initialize(self) -> None:
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
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO cache(key, value) VALUES (?, ?)",
                (key, json.dumps(value, ensure_ascii=False)),
            )

    def get_cache(self, key: str) -> dict[str, Any] | None:
        with self._connect() as conn:
            row = conn.execute("SELECT value FROM cache WHERE key = ?", (key,)).fetchone()
        return json.loads(row[0]) if row else None

    def enqueue(self, item: QueueItem) -> None:
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO queue(item_id, payload, status, created_at) VALUES (?, ?, ?, ?)",
                (item.item_id, json.dumps(item.payload, ensure_ascii=False), item.status, item.created_at.isoformat()),
            )

    def dequeue(self) -> QueueItem | None:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT item_id, payload, status, created_at FROM queue WHERE status = ? ORDER BY created_at LIMIT 1",
                ("queued",),
            ).fetchone()
            if row is None:
                return None
            conn.execute("UPDATE queue SET status = ? WHERE item_id = ?", ("done", row[0]))
        return QueueItem(item_id=row[0], payload=json.loads(row[1]), status=row[2], created_at=row[3])

