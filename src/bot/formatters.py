from __future__ import annotations

from html import escape

from api.models import Event, GameType, RatingEntry

GAME_LABELS: dict[GameType, str] = {
    "poker": "Покер",
    "darts": "Дартс",
    "billiards": "Бильярд",
}


def format_event(event: Event) -> str:
    starts_at = event.starts_at.astimezone().strftime("%d.%m.%Y %H:%M")
    limit = str(event.participant_limit) if event.participant_limit is not None else "без лимита"
    description = event.description or "Описание не указано."
    location = event.location or "Место уточняется"
    return "\n".join(
        [
            f"<b>{escape(event.title)}</b>",
            f"Игра: {GAME_LABELS[event.game_type]}",
            f"Дата и время: {starts_at}",
            f"Место: {escape(location)}",
            f"Участники: {event.count.registrations} / {limit}",
            escape(description),
        ]
    )


def format_rating(game: GameType, entries: list[RatingEntry]) -> str:
    title = f"<b>Топ игроков: {GAME_LABELS[game]}</b>"
    if not entries:
        return f"{title}\n\nРейтинг пока пуст."

    lines = [title, ""]
    for index, entry in enumerate(entries, start=1):
        name = entry.user.name if entry.user and entry.user.name else f"Игрок {entry.user_id}"
        lines.append(f"{index}. {escape(name)} — {entry.points} очков")
    return "\n".join(lines)
