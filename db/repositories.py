from __future__ import annotations

from datetime import datetime, timedelta, timezone
import sqlite3

from db.database import Database
from models.entities import Event, GAME_TYPES, GameType, RatingRow, User


def _dt(value: str) -> datetime:
    return datetime.fromisoformat(value)


def _event(row: sqlite3.Row) -> Event:
    return Event(
        id=row["id"],
        title=row["title"],
        game_type=row["game_type"],
        starts_at=_dt(row["starts_at"]),
        location=row["location"],
        description=row["description"],
        capacity=row["capacity"],
        created_by=row["created_by"],
        is_active=bool(row["is_active"]),
    )


class UserRepository:
    def __init__(self, db: Database) -> None:
        self.db = db

    def upsert_telegram_user(self, telegram_id: int, username: str | None) -> User:
        now = datetime.now(timezone.utc).isoformat()
        with self.db.connect() as conn:
            conn.execute(
                """
                INSERT INTO users (telegram_id, username, registered_at)
                VALUES (?, ?, ?)
                ON CONFLICT(telegram_id) DO UPDATE SET username = excluded.username
                """,
                (telegram_id, username, now),
            )
            row = conn.execute(
                "SELECT * FROM users WHERE telegram_id = ?", (telegram_id,)
            ).fetchone()
        return User(row["id"], row["telegram_id"], row["username"], _dt(row["registered_at"]))

    def list_all(self) -> list[User]:
        with self.db.connect() as conn:
            rows = conn.execute("SELECT * FROM users ORDER BY registered_at").fetchall()
        return [
            User(r["id"], r["telegram_id"], r["username"], _dt(r["registered_at"])) for r in rows
        ]


class EventRepository:
    def __init__(self, db: Database) -> None:
        self.db = db

    def create(
        self,
        title: str,
        game_type: GameType,
        starts_at: datetime,
        location: str,
        description: str,
        capacity: int | None,
        created_by: int,
    ) -> Event:
        if game_type not in GAME_TYPES:
            raise ValueError("Unsupported game type")
        with self.db.connect() as conn:
            cur = conn.execute(
                """
                INSERT INTO events
                    (title, game_type, starts_at, location, description, capacity, created_by)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    title,
                    game_type,
                    starts_at.astimezone(timezone.utc).isoformat(),
                    location,
                    description,
                    capacity,
                    created_by,
                ),
            )
            row = conn.execute("SELECT * FROM events WHERE id = ?", (cur.lastrowid,)).fetchone()
        return _event(row)

    def list_future(self, game_type: GameType | None = None) -> list[Event]:
        now = datetime.now(timezone.utc).isoformat()
        params: list[object] = [now]
        query = "SELECT * FROM events WHERE is_active = 1 AND starts_at > ?"
        if game_type:
            query += " AND game_type = ?"
            params.append(game_type)
        query += " ORDER BY starts_at ASC"
        with self.db.connect() as conn:
            rows = conn.execute(query, params).fetchall()
        return [_event(row) for row in rows]

    def get(self, event_id: int) -> Event | None:
        with self.db.connect() as conn:
            row = conn.execute(
                "SELECT * FROM events WHERE id = ? AND is_active = 1", (event_id,)
            ).fetchone()
        return _event(row) if row else None

    def deactivate(self, event_id: int) -> bool:
        with self.db.connect() as conn:
            cur = conn.execute(
                "UPDATE events SET is_active = 0 WHERE id = ? AND is_active = 1",
                (event_id,),
            )
        return cur.rowcount > 0

    def due_for_24h_reminder(self) -> list[Event]:
        now = datetime.now(timezone.utc)
        start = now.isoformat()
        end = (now + timedelta(hours=24)).isoformat()
        with self.db.connect() as conn:
            rows = conn.execute(
                """
                SELECT * FROM events
                WHERE is_active = 1
                  AND reminder_24h_sent_at IS NULL
                  AND starts_at BETWEEN ? AND ?
                ORDER BY starts_at
                """,
                (start, end),
            ).fetchall()
        return [_event(row) for row in rows]

    def mark_24h_reminded(self, event_id: int) -> None:
        with self.db.connect() as conn:
            conn.execute(
                "UPDATE events SET reminder_24h_sent_at = ? WHERE id = ?",
                (datetime.now(timezone.utc).isoformat(), event_id),
            )


class RegistrationRepository:
    def __init__(self, db: Database) -> None:
        self.db = db

    def register(self, user_id: int, event_id: int, game_type: GameType) -> bool:
        with self.db.connect() as conn:
            event_row = conn.execute(
                "SELECT capacity FROM events WHERE id = ? AND is_active = 1 AND starts_at > ?",
                (event_id, datetime.now(timezone.utc).isoformat()),
            ).fetchone()
            if not event_row:
                raise ValueError("Event is not available")
            existing = conn.execute(
                "SELECT 1 FROM registrations WHERE user_id = ? AND event_id = ?",
                (user_id, event_id),
            ).fetchone()
            if existing:
                return False
            if event_row["capacity"] is not None:
                count = conn.execute(
                    "SELECT COUNT(*) AS c FROM registrations WHERE event_id = ?",
                    (event_id,),
                ).fetchone()["c"]
                if count >= event_row["capacity"]:
                    raise ValueError("Event capacity is full")
            try:
                conn.execute(
                    "INSERT INTO registrations (user_id, event_id) VALUES (?, ?)",
                    (user_id, event_id),
                )
            except sqlite3.IntegrityError:
                return False
            conn.execute(
                """
                INSERT INTO ratings (user_id, game_type, points, events_count, updated_at)
                VALUES (?, ?, 1, 1, ?)
                ON CONFLICT(user_id, game_type) DO UPDATE SET
                    points = points + 1,
                    events_count = events_count + 1,
                    updated_at = excluded.updated_at
                """,
                (user_id, game_type, datetime.now(timezone.utc).isoformat()),
            )
        return True

    def list_event_users(self, event_id: int) -> list[sqlite3.Row]:
        with self.db.connect() as conn:
            return conn.execute(
                """
                SELECT u.telegram_id, u.username, r.registered_at
                FROM registrations r
                JOIN users u ON u.id = r.user_id
                WHERE r.event_id = ?
                ORDER BY r.registered_at
                """,
                (event_id,),
            ).fetchall()

    def list_event_telegram_ids(self, event_id: int) -> list[int]:
        with self.db.connect() as conn:
            rows = conn.execute(
                """
                SELECT u.telegram_id
                FROM registrations r
                JOIN users u ON u.id = r.user_id
                WHERE r.event_id = ?
                """,
                (event_id,),
            ).fetchall()
        return [row["telegram_id"] for row in rows]


class RatingRepository:
    def __init__(self, db: Database) -> None:
        self.db = db

    def top(self, game_type: GameType, limit: int = 20) -> list[RatingRow]:
        with self.db.connect() as conn:
            rows = conn.execute(
                """
                SELECT u.telegram_id, u.username, r.points, r.events_count
                FROM ratings r
                JOIN users u ON u.id = r.user_id
                WHERE r.game_type = ?
                ORDER BY r.points DESC, r.events_count DESC, u.username ASC
                LIMIT ?
                """,
                (game_type, limit),
            ).fetchall()
        return [
            RatingRow(row["telegram_id"], row["username"], row["points"], row["events_count"])
            for row in rows
        ]


class FeedbackRepository:
    def __init__(self, db: Database) -> None:
        self.db = db

    def create(self, user_id: int, message: str, forwarded: bool) -> int:
        with self.db.connect() as conn:
            cur = conn.execute(
                """
                INSERT INTO feedback (user_id, message, forwarded_to_admin)
                VALUES (?, ?, ?)
                """,
                (user_id, message, int(forwarded)),
            )
        return int(cur.lastrowid)

    def mark_last_forwarded(self, user_id: int, message: str) -> None:
        with self.db.connect() as conn:
            conn.execute(
                """
                UPDATE feedback
                SET forwarded_to_admin = 1
                WHERE id = (
                    SELECT id FROM feedback
                    WHERE user_id = ? AND message = ?
                    ORDER BY created_at DESC, id DESC
                    LIMIT 1
                )
                """,
                (user_id, message),
            )
