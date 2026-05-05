from __future__ import annotations

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from api.models import GameType
from bot.callbacks import EventRegisterCallback, RatingCallback


def main_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Мероприятия", callback_data="events")
    builder.button(text="Рейтинг", callback_data="rating_menu")
    builder.button(text="Правила", callback_data="rules")
    builder.button(text="Feedback", callback_data="feedback")
    builder.adjust(2)
    return builder.as_markup()


def event_registration_keyboard(event_id: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Записаться",
        callback_data=EventRegisterCallback(event_id=event_id).pack(),
    )
    return builder.as_markup()


def rating_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    labels: dict[GameType, str] = {"poker": "Покер", "darts": "Дартс", "billiards": "Бильярд"}
    for game, label in labels.items():
        builder.button(text=label, callback_data=RatingCallback(game=game).pack())
    builder.adjust(3)
    return builder.as_markup()
