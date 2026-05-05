from __future__ import annotations
import logging
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from config import settings
from services.container import ServiceContainer

logger = logging.getLogger(__name__)


def services(context: ContextTypes.DEFAULT_TYPE) -> ServiceContainer:
    return context.application.bot_data["services"]


async def ensure_registered(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_user:
        raise RuntimeError("Telegram user is missing in update")
    return services(context).users.ensure_user(update.effective_user)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await ensure_registered(update, context)
    text = (
        f"{settings.club_name}: бот игрового клуба.\n\n"
        "Команды:\n"
        "/events — ближайшие мероприятия\n"
        "/ratingpoker, /ratingdart, /ratingbill — рейтинги\n"
        "/rules — правила клуба\n"
        "/support — поддержка\n"
        "/feedback — оставить обратную связь"
    )
    await update.effective_message.reply_text(text)


async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await ensure_registered(update, context)
    await update.effective_message.reply_text(
        "Правила DUCK'S:\n"
        "1. Уважайте игроков, ведущих и персонал клуба.\n"
        "2. Приходите к началу мероприятия или предупредите поддержку об опоздании.\n"
        "3. Запись на событие персональная, передача места другому игроку согласуется с клубом.\n"
        "4. Спорные игровые ситуации решает ведущий или администратор.\n"
        "5. Агрессивное поведение, мошенничество и нарушение правил игры ведут к снятию с события."
    )


async def support(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await ensure_registered(update, context)
    await update.effective_message.reply_text(
        f"Поддержка {settings.club_name}:\n"
        f"Telegram: {settings.support_telegram}\n"
        f"Email: {settings.support_email}"
    )


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.exception("Unhandled Telegram update error", exc_info=context.error)
    if isinstance(update, Update) and update.effective_message:
        await update.effective_message.reply_text(
            "Произошла внутренняя ошибка. Администратор уже может увидеть ее в логах."
        )


def common_handlers():
    return [
        CommandHandler("start", start),
        CommandHandler("rules", rules),
        CommandHandler("support", support),
    ]
