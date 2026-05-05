from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramAPIError
from aiogram.types import BotCommand, ErrorEvent

from api.client import ApiClient
from bot.factory import build_bot, build_dispatcher
from config.settings import get_settings
from logging_config.setup import setup_logging
from storage.user_links import UserLinkStorage

logger = logging.getLogger(__name__)


async def set_commands(bot: Bot) -> None:
    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Главное меню"),
            BotCommand(command="help", description="Список команд"),
            BotCommand(command="events", description="Ближайшие мероприятия"),
            BotCommand(command="poker", description="Мероприятия по покеру"),
            BotCommand(command="darts", description="Мероприятия по дартсу"),
            BotCommand(command="billiards", description="Мероприятия по бильярду"),
            BotCommand(command="rating", description="Рейтинг игроков"),
            BotCommand(command="rules", description="Правила клуба"),
            BotCommand(command="feedback", description="Отправить сообщение клубу"),
            BotCommand(command="link", description="Связать аккаунт клуба"),
        ]
    )


async def run() -> None:
    settings = get_settings()
    setup_logging(settings.log_level)

    api_client = ApiClient(str(settings.api_base_url), settings.api_timeout_seconds)
    user_links = UserLinkStorage(settings.user_links_path)
    bot = build_bot(settings.telegram_bot_token)
    dispatcher: Dispatcher = build_dispatcher(api_client, user_links)

    @dispatcher.errors()
    async def unknown_error_handler(event: ErrorEvent) -> bool:
        logger.error(
            "Unhandled bot error",
            exc_info=event.exception,
            extra={"update": repr(event.update)},
        )
        return True

    try:
        await set_commands(bot)
        logger.info("Starting DUCK'S Telegram bot")
        await dispatcher.start_polling(bot, allowed_updates=dispatcher.resolve_used_update_types())
    except TelegramAPIError:
        logger.exception("Telegram API error")
        raise
    finally:
        logger.info("Shutting down DUCK'S Telegram bot")
        await api_client.close()
        await bot.session.close()


def main() -> None:
    asyncio.run(run())


if __name__ == "__main__":
    main()
