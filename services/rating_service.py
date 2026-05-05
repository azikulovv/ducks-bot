from __future__ import annotations

from db.repositories import RatingRepository
from models.entities import GAME_LABELS, GAME_TYPES, GameType


class RatingService:
    def __init__(self, ratings: RatingRepository) -> None:
        self.ratings = ratings

    def format_top(self, game_type: GameType) -> str:
        if game_type not in GAME_TYPES:
            raise ValueError("Unknown game type")
        rows = self.ratings.top(game_type)
        if not rows:
            return f"Рейтинг {GAME_LABELS[game_type]} пока пуст."
        lines = [f"Рейтинг {GAME_LABELS[game_type]}:"]
        for index, row in enumerate(rows, start=1):
            name = f"@{row.username}" if row.username else str(row.telegram_id)
            lines.append(f"{index}. {name} — {row.points} очк., событий: {row.events_count}")
        return "\n".join(lines)
