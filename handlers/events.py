from __future__ import annotations

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackQueryHandler, CommandHandler, ContextTypes

from config import settings
from handlers.common import ensure_registered, services
from models.entities import GAME_LABELS, GAME_TYPES
from services.event_service import format_event


def _filters_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Все", callback_data="events:all"),
                InlineKeyboardButton("Покер", callback_data="events:poker"),
            ],
            [
                InlineKeyboardButton("Дартс", callback_data="events:dart"),
                InlineKeyboardButton("Бильярд", callback_data="events:bill"),
            ],
        ]
    )


def _event_keyboard(event_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton("Записаться", callback_data=f"register:{event_id}")]]
    )


async def events_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await ensure_registered(update, context)
    game_type = context.args[0].lower() if context.args else None
    if game_type and game_type not in GAME_TYPES:
        await update.effective_message.reply_text(
            "Фильтр должен быть одним из: poker, dart, bill."
        )
        return
    await update.effective_message.reply_text(
        "Выберите тип мероприятий:", reply_markup=_filters_keyboard()
    )
    await _send_events(update, context, game_type)


async def events_filter_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await ensure_registered(update, context)
    raw_type = query.data.split(":", 1)[1]
    game_type = None if raw_type == "all" else raw_type
    await _send_events(update, context, game_type)


async def _send_events(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    game_type: str | None,
) -> None:
    events = services(context).events.list_future(game_type)
    target = update.effective_chat.id
    if not events:
        label = "всех типов" if not game_type else GAME_LABELS[game_type]
        await context.bot.send_message(target, f"Будущих мероприятий ({label}) пока нет.")
        return
    for event in events:
        await context.bot.send_message(
            chat_id=target,
            text=format_event(event, settings.timezone),
            reply_markup=_event_keyboard(event.id),
        )


async def register_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    user = await ensure_registered(update, context)
    event_id = int(query.data.split(":", 1)[1])
    try:
        created, event = services(context).events.register(user.id, event_id)
    except ValueError as exc:
        await query.message.reply_text(str(exc))
        return
    if not created:
        await query.message.reply_text("Вы уже записаны на это мероприятие.")
        return
    await query.message.reply_text(f"Запись подтверждена: {event.title}.")


def event_handlers():
    return [
        CommandHandler("events", events_command),
        CallbackQueryHandler(events_filter_callback, pattern=r"^events:(all|poker|dart|bill)$"),
        CallbackQueryHandler(register_callback, pattern=r"^register:\d+$"),
    ]
