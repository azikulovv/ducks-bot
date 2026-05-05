from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from storage.user_links import UserLinkStorage

router = Router(name=__name__)


@router.message(Command("link"))
async def link_command(message: Message, user_links: UserLinkStorage) -> None:
    if message.from_user is None:
        return
    parts = (message.text or "").split(maxsplit=1)
    if len(parts) != 2 or not parts[1].strip():
        await message.answer("Укажите user id аккаунта клуба: /link <user_id>")
        return

    backend_user_id = parts[1].strip()
    await user_links.set(message.from_user.id, backend_user_id)
    await message.answer(
        "Telegram привязан к аккаунту клуба.\n\n"
        "Для production используйте безопасную привязку через одноразовый код или backend endpoint."
    )
