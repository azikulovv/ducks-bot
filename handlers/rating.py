from __future__ import annotations

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from handlers.common import ensure_registered, services


async def rating_poker(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await ensure_registered(update, context)
    await update.effective_message.reply_text(services(context).ratings.format_top("poker"))


async def rating_dart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await ensure_registered(update, context)
    await update.effective_message.reply_text(services(context).ratings.format_top("dart"))


async def rating_bill(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await ensure_registered(update, context)
    await update.effective_message.reply_text(services(context).ratings.format_top("bill"))


def rating_handlers():
    return [
        CommandHandler("ratingpoker", rating_poker),
        CommandHandler("ratingdart", rating_dart),
        CommandHandler("ratingbill", rating_bill),
    ]
