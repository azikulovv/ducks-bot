from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from api.client import ApiClient
from api.errors import ApiError, user_message_for_error
from bot.callbacks import RatingCallback
from bot.formatters import format_rating
from bot.keyboards import rating_keyboard

router = Router(name=__name__)


@router.message(Command("rating"))
async def rating_command(message: Message) -> None:
    await message.answer("Выберите игру:", reply_markup=rating_keyboard())


@router.callback_query(lambda callback: callback.data == "rating_menu")
async def rating_menu_callback(callback: CallbackQuery) -> None:
    await callback.answer()
    if callback.message:
        await callback.message.answer("Выберите игру:", reply_markup=rating_keyboard())


@router.callback_query(RatingCallback.filter())
async def rating_callback(
    callback: CallbackQuery,
    callback_data: RatingCallback,
    api_client: ApiClient,
) -> None:
    await callback.answer()
    if callback.message is None:
        return
    try:
        response = await api_client.get_rating(callback_data.game, page=1, limit=10)
    except ApiError as exc:
        await callback.message.answer(user_message_for_error(exc))
        return
    await callback.message.answer(format_rating(callback_data.game, response.data))
