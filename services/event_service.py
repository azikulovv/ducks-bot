from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

from db.repositories import EventRepository, RegistrationRepository
from models.entities import Event, GAME_LABELS, GAME_TYPES, GameType


class EventService:
    def __init__(
        self,
        events: EventRepository,
        registrations: RegistrationRepository,
    ) -> None:
        self.events = events
        self.registrations = registrations

    def list_future(self, game_type: GameType | None = None) -> list[Event]:
        if game_type and game_type not in GAME_TYPES:
            raise ValueError("Unknown game type")
        return self.events.list_future(game_type)

    def create_event(
        self,
        title: str,
        game_type: GameType,
        starts_at: datetime,
        location: str,
        description: str,
        capacity: int | None,
        created_by: int,
    ) -> Event:
        title = title.strip()
        location = location.strip()
        description = description.strip()
        if not 3 <= len(title) <= 120:
            raise ValueError("Название должно быть от 3 до 120 символов")
        if game_type not in GAME_TYPES:
            raise ValueError("Тип игры: poker, dart или bill")
        if starts_at <= datetime.now(starts_at.tzinfo):
            raise ValueError("Дата события должна быть в будущем")
        if not 2 <= len(location) <= 120:
            raise ValueError("Локация должна быть от 2 до 120 символов")
        if capacity is not None and capacity <= 0:
            raise ValueError("Лимит мест должен быть положительным числом")
        return self.events.create(
            title, game_type, starts_at, location, description, capacity, created_by
        )

    def register(self, user_id: int, event_id: int) -> tuple[bool, Event]:
        event = self.events.get(event_id)
        if not event:
            raise ValueError("Событие не найдено или уже недоступно")
        created = self.registrations.register(user_id, event.id, event.game_type)
        return created, event

    def delete_event(self, event_id: int) -> bool:
        return self.events.deactivate(event_id)

    def event_registrations(self, event_id: int) -> list[str]:
        rows = self.registrations.list_event_users(event_id)
        return [
            f"{i}. @{row['username']}" if row["username"] else f"{i}. {row['telegram_id']}"
            for i, row in enumerate(rows, start=1)
        ]


def format_event(event: Event, tz_name: str) -> str:
    local_dt = event.starts_at.astimezone(ZoneInfo(tz_name))
    capacity = f"\nМест: {event.capacity}" if event.capacity else ""
    description = f"\n{event.description}" if event.description else ""
    return (
        f"{event.title}\n"
        f"Игра: {GAME_LABELS[event.game_type]}\n"
        f"Дата: {local_dt:%d.%m.%Y %H:%M}\n"
        f"Место: {event.location}"
        f"{capacity}"
        f"{description}"
    )


def parse_event_datetime(value: str, tz_name: str) -> datetime:
    try:
        naive = datetime.strptime(value.strip(), "%Y-%m-%d %H:%M")
    except ValueError as exc:
        raise ValueError("Дата должна быть в формате YYYY-MM-DD HH:MM") from exc
    return naive.replace(tzinfo=ZoneInfo(tz_name))
