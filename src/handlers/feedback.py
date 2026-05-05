from __future__ import annotations

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from api.client import ApiClient
from api.errors import ApiError, user_message_for_error
from state.feedback import FeedbackState

router = Router(name=__name__)


@router.message(Command("feedback"))
async def feedback_command(message: Message, state: FSMContext) -> None:
    await start_feedback(message, state)


@router.callback_query(lambda callback: callback.data == "feedback")
async def feedback_menu_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    if isinstance(callback.message, Message):
        await start_feedback(callback.message, state)


async def start_feedback(message: Message, state: FSMContext) -> None:
    await state.set_state(FeedbackState.waiting_for_text)
    await message.answer("Напишите сообщение для клуба одним сообщением.")


@router.message(FeedbackState.waiting_for_text, F.text)
async def feedback_text(message: Message, state: FSMContext, api_client: ApiClient) -> None:
    text = message.text.strip() if message.text else ""
    if not text:
        await message.answer("Сообщение не должно быть пустым.")
        return

    user = message.from_user
    name_parts = []
    if user and user.first_name:
        name_parts.append(user.first_name)
    if user and user.username:
        name_parts.append(f"@{user.username}")
    name = " ".join(name_parts) or None

    try:
        await api_client.send_feedback(name=name, message=text)
    except ApiError as exc:
        await message.answer(user_message_for_error(exc))
        return

    await state.clear()
    await message.answer("Спасибо, сообщение отправлено.")
