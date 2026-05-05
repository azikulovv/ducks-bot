from __future__ import annotations

from aiogram.filters.callback_data import CallbackData

from api.models import GameType


class EventRegisterCallback(CallbackData, prefix="event_register"):
    event_id: str


class RatingCallback(CallbackData, prefix="rating"):
    game: GameType
