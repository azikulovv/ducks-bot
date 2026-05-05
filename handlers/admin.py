from __future__ import annotations

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters

from config import settings
from handlers.common import ensure_registered, services
from models.entities import GAME_LABELS, GAME_TYPES
from services.event_service import format_event, parse_event_datetime
from zoneinfo import ZoneInfo

TITLE, GAME, STARTS_AT, LOCATION, DESCRIPTION, CAPACITY = range(6)


def _is_admin(user_id: int | None) -> bool:
    return bool(user_id and user_id in settings.admin_ids)


async def _deny(update: Update) -> None:
    await update.effective_message.reply_text("Команда доступна только администраторам.")


async def admin_add_event(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if not _is_admin(update.effective_user.id if update.effective_user else None):
        await _deny(update)
        return ConversationHandler.END
    await ensure_registered(update, context)
    context.user_data["new_event"] = {}
    await update.effective_message.reply_text("Название мероприятия:")
    return TITLE


async def add_title(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    title = (update.effective_message.text or "").strip()
    if not 3 <= len(title) <= 120:
        await update.effective_message.reply_text("Название должно быть от 3 до 120 символов.")
        return TITLE
    context.user_data["new_event"]["title"] = title
    await update.effective_message.reply_text("Тип игры: poker, dart или bill")
    return GAME


async def add_game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    game_type = (update.effective_message.text or "").strip().lower()
    if game_type not in GAME_TYPES:
        await update.effective_message.reply_text("Введите один из типов: poker, dart, bill")
        return GAME
    context.user_data["new_event"]["game_type"] = game_type
    await update.effective_message.reply_text("Дата и время: YYYY-MM-DD HH:MM")
    return STARTS_AT


async def add_starts_at(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        starts_at = parse_event_datetime(update.effective_message.text or "", settings.timezone)
    except ValueError as exc:
        await update.effective_message.reply_text(str(exc))
        return STARTS_AT
    context.user_data["new_event"]["starts_at"] = starts_at
    await update.effective_message.reply_text("Место проведения:")
    return LOCATION


async def add_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    location = (update.effective_message.text or "").strip()
    if not 2 <= len(location) <= 120:
        await update.effective_message.reply_text("Локация должна быть от 2 до 120 символов.")
        return LOCATION
    context.user_data["new_event"]["location"] = location
    await update.effective_message.reply_text("Описание. Если описания нет, отправьте '-'.")
    return DESCRIPTION


async def add_description(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    description = (update.effective_message.text or "").strip()
    context.user_data["new_event"]["description"] = "" if description == "-" else description
    await update.effective_message.reply_text("Лимит мест числом. Если лимита нет, отправьте '-'.")
    return CAPACITY


async def add_capacity(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    raw = (update.effective_message.text or "").strip()
    capacity = None
    if raw != "-":
        try:
            capacity = int(raw)
        except ValueError:
            await update.effective_message.reply_text("Введите положительное число или '-'.")
            return CAPACITY
        if capacity <= 0:
            await update.effective_message.reply_text("Лимит должен быть положительным.")
            return CAPACITY

    admin = await ensure_registered(update, context)
    payload = context.user_data["new_event"]
    try:
        event = services(context).events.create_event(
            title=payload["title"],
            game_type=payload["game_type"],
            starts_at=payload["starts_at"],
            location=payload["location"],
            description=payload["description"],
            capacity=capacity,
            created_by=admin.id,
        )
    except ValueError as exc:
        await update.effective_message.reply_text(str(exc))
        return ConversationHandler.END

    await update.effective_message.reply_text(
        "Мероприятие создано:\n\n" + format_event(event, settings.timezone)
    )
    await services(context).notifications.send_new_event_broadcast(context, settings, event.id)
    context.user_data.pop("new_event", None)
    return ConversationHandler.END


async def admin_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.pop("new_event", None)
    await update.effective_message.reply_text("Админ-действие отменено.")
    return ConversationHandler.END


async def admin_delete_event(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not _is_admin(update.effective_user.id if update.effective_user else None):
        await _deny(update)
        return
    if not context.args:
        await update.effective_message.reply_text("Использование: /admin_delete_event <event_id>")
        return
    try:
        event_id = int(context.args[0])
    except ValueError:
        await update.effective_message.reply_text("event_id должен быть числом.")
        return
    deleted = services(context).events.delete_event(event_id)
    await update.effective_message.reply_text(
        "Мероприятие удалено." if deleted else "Активное мероприятие не найдено."
    )


async def admin_registrations(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not _is_admin(update.effective_user.id if update.effective_user else None):
        await _deny(update)
        return
    if not context.args:
        await update.effective_message.reply_text("Использование: /admin_registrations <event_id>")
        return
    try:
        event_id = int(context.args[0])
    except ValueError:
        await update.effective_message.reply_text("event_id должен быть числом.")
        return
    rows = services(context).events.event_registrations(event_id)
    text = "\n".join(rows) if rows else "Записей на это мероприятие пока нет."
    await update.effective_message.reply_text(text)


async def admin_events(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not _is_admin(update.effective_user.id if update.effective_user else None):
        await _deny(update)
        return
    events = services(context).events.list_future()
    if not events:
        await update.effective_message.reply_text("Будущих мероприятий нет.")
        return
    lines = []
    for event in events:
        lines.append(
            f"ID {event.id}: {event.title} / {GAME_LABELS[event.game_type]} / "
            f"{event.starts_at.astimezone(ZoneInfo(settings.timezone)).strftime('%d.%m.%Y %H:%M')}"
        )
    await update.effective_message.reply_text("\n".join(lines))


def admin_handlers():
    return [
        ConversationHandler(
            entry_points=[CommandHandler("admin_add_event", admin_add_event)],
            states={
                TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_title)],
                GAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_game)],
                STARTS_AT: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_starts_at)],
                LOCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_location)],
                DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_description)],
                CAPACITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_capacity)],
            },
            fallbacks=[CommandHandler("cancel", admin_cancel)],
        ),
        CommandHandler("admin_delete_event", admin_delete_event),
        CommandHandler("admin_registrations", admin_registrations),
        CommandHandler("admin_events", admin_events),
    ]
