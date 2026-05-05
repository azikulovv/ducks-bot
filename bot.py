from __future__ import annotations

import logging

from telegram import BotCommand
from telegram.ext import Application, ContextTypes


from config import settings
from db.database import Database
from handlers import all_handlers
from handlers.common import error_handler
from services.container import build_services
from utils.logging import setup_logging

logger = logging.getLogger(__name__)


async def reminder_job(context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.application.bot_data["services"].notifications.send_24h_reminders(
        context, settings
    )


async def post_init(application: Application) -> None:
    await application.bot.set_my_commands(
        [
            BotCommand("start", "Регистрация и главное меню"),
            BotCommand("events", "Ближайшие мероприятия"),
            BotCommand("ratingpoker", "Рейтинг по покеру"),
            BotCommand("ratingdart", "Рейтинг по дартсу"),
            BotCommand("ratingbill", "Рейтинг по бильярду"),
            BotCommand("rules", "Правила клуба"),
            BotCommand("support", "Контакты поддержки"),
            BotCommand("feedback", "Обратная связь"),
        ]
    )


def build_application() -> Application:
    db = Database(settings.database_path)
    db.init_schema()

    application = Application.builder().token(settings.bot_token).post_init(post_init).build()
    application.bot_data["services"] = build_services(db)

    for handler in all_handlers():
        application.add_handler(handler)
    application.add_error_handler(error_handler)

    if application.job_queue:
        application.job_queue.run_repeating(reminder_job, interval=600, first=30)
    else:
        logger.warning("JobQueue is unavailable; install python-telegram-bot[job-queue]")
    return application


def main() -> None:
    setup_logging(settings.log_level)
    logger.info("Starting DUCK'S Telegram bot")
    application = build_application()
    application.run_polling(
        allowed_updates=["message", "callback_query"],
        drop_pending_updates=True,
    )


if __name__ == "__main__":
    main()
