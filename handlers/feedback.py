from __future__ import annotations

import logging

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters

from config import settings
from handlers.common import ensure_registered, services


logger = logging.getLogger(__name__)
WAITING_MESSAGE = 1


async def feedback_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await ensure_registered(update, context)
    await update.effective_message.reply_text("Напишите сообщение для администрации клуба.")
    return WAITING_MESSAGE


async def feedback_receive(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = await ensure_registered(update, context)
    text = update.effective_message.text or ""
    try:
        services(context).feedback.save(user.id, text, False)
    except ValueError as exc:
        await update.effective_message.reply_text(str(exc))
        return WAITING_MESSAGE

    forwarded = False
    if settings.admin_chat_id:
        try:
            name = f"@{update.effective_user.username}" if update.effective_user.username else user.telegram_id
            await context.bot.send_message(
                chat_id=settings.admin_chat_id,
                text=f"Feedback от {name}:\n\n{text}",
            )
            forwarded = True
        except Exception:
            logger.exception("Failed to forward feedback to admin chat")
    if forwarded:
        services(context).feedback.mark_forwarded(user.id, text)
    await update.effective_message.reply_text("Спасибо. Сообщение передано администрации.")
    return ConversationHandler.END


async def feedback_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.effective_message.reply_text("Обратная связь отменена.")
    return ConversationHandler.END


def feedback_handlers():
    return [
        ConversationHandler(
            entry_points=[CommandHandler("feedback", feedback_start)],
            states={
                WAITING_MESSAGE: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, feedback_receive)
                ]
            },
            fallbacks=[CommandHandler("cancel", feedback_cancel)],
        )
    ]
