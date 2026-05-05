from __future__ import annotations

from html import escape

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from api.client import ApiClient
from api.errors import ApiError, user_message_for_error

router = Router(name=__name__)


@router.message(Command("rules"))
async def rules_command(message: Message, api_client: ApiClient) -> None:
    await send_rules(message, api_client)


@router.callback_query(lambda callback: callback.data == "rules")
async def rules_menu_callback(callback: CallbackQuery, api_client: ApiClient) -> None:
    await callback.answer()
    if isinstance(callback.message, Message):
        await send_rules(callback.message, api_client)


async def send_rules(message: Message, api_client: ApiClient) -> None:
    try:
        rules = await api_client.get_rules()
    except ApiError as exc:
        await message.answer(user_message_for_error(exc))
        return
    await message.answer(f"<b>{escape(rules.title)}</b>\n\n{escape(rules.body)}")
