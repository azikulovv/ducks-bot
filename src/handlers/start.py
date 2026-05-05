from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from bot.keyboards import main_menu_keyboard

router = Router(name=__name__)


HELP_TEXT = "\n".join(
    [
        "/events — ближайшие мероприятия",
        "/poker — мероприятия по покеру",
        "/darts — мероприятия по дартсу",
        "/billiards — мероприятия по бильярду",
        "/rating — рейтинг игроков",
        "/rules — правила клуба",
        "/feedback — отправить сообщение клубу",
        "/link <user_id> — связать Telegram с аккаунтом клуба",
    ]
)


@router.message(CommandStart())
async def start_command(message: Message) -> None:
    await message.answer(
        "Добро пожаловать в DUCK'S GameClub.",
        reply_markup=main_menu_keyboard(),
    )


@router.message(Command("help"))
async def help_command(message: Message) -> None:
    await message.answer(HELP_TEXT)

