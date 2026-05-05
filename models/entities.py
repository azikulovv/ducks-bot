from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


GameType = str
GAME_TYPES: tuple[GameType, ...] = ("poker", "dart", "bill")

GAME_LABELS: dict[GameType, str] = {
    "poker": "Покер",
    "dart": "Дартс",
    "bill": "Бильярд",
}


@dataclass(frozen=True)
class User:
    id: int
    telegram_id: int
    username: str | None
    registered_at: datetime


@dataclass(frozen=True)
class Event:
    id: int
    title: str
    game_type: GameType
    starts_at: datetime
    location: str
    description: str
    capacity: int | None
    created_by: int
    is_active: bool


@dataclass(frozen=True)
class RatingRow:
    telegram_id: int
    username: str | None
    points: int
    events_count: int
