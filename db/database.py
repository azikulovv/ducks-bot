from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
import sqlite3
from typing import Iterator


class Database:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    @contextmanager
    def connect(self) -> Iterator[sqlite3.Connection]:
        conn = sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("PRAGMA journal_mode = WAL")
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def init_schema(self) -> None:
        with self.connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    telegram_id INTEGER NOT NULL UNIQUE,
                    username TEXT,
                    registered_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    game_type TEXT NOT NULL CHECK (game_type IN ('poker', 'dart', 'bill')),
                    starts_at TEXT NOT NULL,
                    location TEXT NOT NULL,
                    description TEXT NOT NULL DEFAULT '',
                    capacity INTEGER CHECK (capacity IS NULL OR capacity > 0),
                    created_by INTEGER NOT NULL,
                    is_active INTEGER NOT NULL DEFAULT 1,
                    reminder_24h_sent_at TEXT,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (created_by) REFERENCES users(id)
                );

                CREATE TABLE IF NOT EXISTS registrations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    event_id INTEGER NOT NULL,
                    registered_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE (user_id, event_id),
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE
                );

                CREATE TABLE IF NOT EXISTS ratings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    game_type TEXT NOT NULL CHECK (game_type IN ('poker', 'dart', 'bill')),
                    points INTEGER NOT NULL DEFAULT 0,
                    events_count INTEGER NOT NULL DEFAULT 0,
                    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE (user_id, game_type),
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                );

                CREATE TABLE IF NOT EXISTS feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    message TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    forwarded_to_admin INTEGER NOT NULL DEFAULT 0,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                );

                CREATE INDEX IF NOT EXISTS idx_events_starts_at ON events(starts_at);
                CREATE INDEX IF NOT EXISTS idx_events_type ON events(game_type);
                CREATE INDEX IF NOT EXISTS idx_registrations_event ON registrations(event_id);
                CREATE INDEX IF NOT EXISTS idx_ratings_type_points ON ratings(game_type, points DESC);
                """
            )
