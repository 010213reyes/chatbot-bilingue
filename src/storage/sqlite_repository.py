"""Persistencia mínima en SQLite para usuarios e interacciones."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional


class SQLiteUserRepository:
    """Repositorio SQL ligero para usuarios e historial de uso."""

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = self._resolve_db_path(db_path or "data/chatbot.sqlite3")
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._connection = sqlite3.connect(str(self.db_path))
        self._connection.row_factory = sqlite3.Row
        self._initialize()

    def _resolve_db_path(self, db_path: str) -> Path:
        path = Path(db_path)
        if not path.is_absolute():
            project_root = Path(__file__).resolve().parents[2]
            return project_root / path
        return path

    def _initialize(self) -> None:
        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                name TEXT,
                language_level TEXT DEFAULT 'A1',
                created_at TEXT NOT NULL,
                metadata TEXT DEFAULT '{}'
            )
            """
        )
        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS user_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                event_type TEXT NOT NULL,
                payload TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            )
            """
        )
        self._connection.commit()

    def register_user(
        self,
        user_id: str,
        name: Optional[str] = None,
        language_level: str = "A1",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        payload = metadata or {}
        self._connection.execute(
            """
            INSERT INTO users (user_id, name, language_level, created_at, metadata)
            VALUES (?, ?, ?, datetime('now'), ?)
            ON CONFLICT(user_id) DO UPDATE SET
                name = excluded.name,
                language_level = excluded.language_level,
                metadata = excluded.metadata
            """,
            (user_id, name, language_level, json.dumps(payload, ensure_ascii=False)),
        )
        self._connection.commit()
        return self.get_user(user_id)

    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        row = self._connection.execute(
            "SELECT * FROM users WHERE user_id = ?",
            (user_id,),
        ).fetchone()
        if row is None:
            return None
        return {
            "user_id": row["user_id"],
            "name": row["name"],
            "language_level": row["language_level"],
            "created_at": row["created_at"],
            "metadata": self._safe_json_load(row["metadata"]),
        }

    def list_users(self) -> List[Dict[str, Any]]:
        rows = self._connection.execute(
            "SELECT * FROM users ORDER BY created_at ASC"
        ).fetchall()
        return [self._row_to_user(row) for row in rows]

    def record_interaction(
        self,
        user_id: str,
        payload: Dict[str, Any],
        event_type: str = "interaction",
    ) -> Dict[str, Any]:
        self._connection.execute(
            """
            INSERT INTO user_history (user_id, event_type, payload, created_at)
            VALUES (?, ?, ?, datetime('now'))
            """,
            (user_id, event_type, json.dumps(payload, ensure_ascii=False)),
        )
        self._connection.commit()
        row = self._connection.execute(
            "SELECT * FROM user_history WHERE user_id = ? ORDER BY id DESC LIMIT 1",
            (user_id,),
        ).fetchone()
        return self._row_to_history(row)

    def get_user_history(self, user_id: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        query = "SELECT * FROM user_history WHERE user_id = ? ORDER BY id ASC"
        params: List[Any] = [user_id]
        if limit is not None:
            query += " LIMIT ?"
            params.append(limit)
        rows = self._connection.execute(query, params).fetchall()
        return [self._row_to_history(row) for row in rows]

    def _row_to_user(self, row: sqlite3.Row) -> Dict[str, Any]:
        return {
            "user_id": row["user_id"],
            "name": row["name"],
            "language_level": row["language_level"],
            "created_at": row["created_at"],
            "metadata": self._safe_json_load(row["metadata"]),
        }

    def _row_to_history(self, row: sqlite3.Row) -> Dict[str, Any]:
        data = self._safe_json_load(row["payload"])
        result = {
            "id": row["id"],
            "user_id": row["user_id"],
            "event_type": row["event_type"],
            "created_at": row["created_at"],
        }
        if isinstance(data, dict):
            result.update(data)
        return result

    def _safe_json_load(self, value: Optional[str]) -> Dict[str, Any]:
        if not value:
            return {}
        try:
            data = json.loads(value)
            return data if isinstance(data, dict) else {}
        except json.JSONDecodeError:
            return {}

    def close(self) -> None:
        if self._connection:
            self._connection.close()
            self._connection = None

    def __enter__(self) -> "SQLiteUserRepository":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()
