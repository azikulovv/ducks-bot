from __future__ import annotations

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from api.client import ApiClient
from handlers import events, feedback, linking, ratings, rules, start
from storage.user_links import UserLinkStorage


def build_bot(token: str) -> Bot:
    return Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


def build_dispatcher(api_client: ApiClient, user_links: UserLinkStorage) -> Dispatcher:
    dispatcher = Dispatcher(storage=MemoryStorage())
    dispatcher["api_client"] = api_client
    dispatcher["user_links"] = user_links
    dispatcher.include_router(start.router)
    dispatcher.include_router(events.router)
    dispatcher.include_router(ratings.router)
    dispatcher.include_router(rules.router)
    dispatcher.include_router(feedback.router)
    dispatcher.include_router(linking.router)
    return dispatcher
