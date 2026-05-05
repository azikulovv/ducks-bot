from __future__ import annotations

import logging

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from api.client import ApiClient
from api.errors import ApiError, user_message_for_error
from api.models import GameType
from bot.callbacks import EventRegisterCallback
from bot.formatters import format_event
from bot.keyboards import event_registration_keyboard
from storage.user_links import UserLinkStorage

logger = logging.getLogger(__name__)
router = Router(name=__name__)


@router.message(Command("events"))
async def events_command(message: Message, api_client: ApiClient) -> None:
    await send_events(message, api_client)


@router.callback_query(lambda callback: callback.data == "events")
async def events_menu_callback(callback: CallbackQuery, api_client: ApiClient) -> None:
    await callback.answer()
    if isinstance(callback.message, Message):
        await send_events(callback.message, api_client)


@router.message(Command("poker"))
async def poker_events_command(message: Message, api_client: ApiClient) -> None:
    await send_events(message, api_client, game_type="poker")


@router.message(Command("darts"))
async def darts_events_command(message: Message, api_client: ApiClient) -> None:
    await send_events(message, api_client, game_type="darts")


@router.message(Command("billiards"))
async def billiards_events_command(message: Message, api_client: ApiClient) -> None:
    await send_events(message, api_client, game_type="billiards")


async def send_events(
    message: Message,
    api_client: ApiClient,
    game_type: GameType | None = None,
) -> None:
    try:
        response = await api_client.get_events(
            game_type=game_type, status="published", page=1, limit=10
        )
    except ApiError as exc:
        await message.answer(user_message_for_error(exc))
        return

    if not response.data:
        await message.answer("Ближайших мероприятий пока нет.")
        return

    for event in response.data:
        await message.answer(
            format_event(event),
            reply_markup=event_registration_keyboard(event.id),
        )


@router.callback_query(EventRegisterCallback.filter(F.event_id))
async def register_callback(
    callback: CallbackQuery,
    callback_data: EventRegisterCallback,
    api_client: ApiClient,
    user_links: UserLinkStorage,
) -> None:
    await callback.answer()
    if callback.from_user is None or callback.message is None:
        return

    backend_user_id = await user_links.get(callback.from_user.id)
    if backend_user_id is None:
        await callback.message.answer("Сначала свяжите Telegram с аккаунтом клуба: /link <user_id>")
        return

    try:
        await api_client.register_for_event(
            event_id=callback_data.event_id,
            user_id=backend_user_id,
        )
    except ApiError as exc:
        logger.info(
            "Event registration failed",
            extra={"telegram_user_id": callback.from_user.id, "api_error_code": exc.code},
        )
        await callback.message.answer(user_message_for_error(exc))
        return

    await callback.message.answer("Вы записаны на мероприятие.")
