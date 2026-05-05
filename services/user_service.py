from __future__ import annotations

from telegram import User as TelegramUser

from db.repositories import UserRepository
from models.entities import User


class UserService:
    def __init__(self, users: UserRepository) -> None:
        self.users = users

    def ensure_user(self, telegram_user: TelegramUser) -> User:
        return self.users.upsert_telegram_user(
            telegram_id=telegram_user.id,
            username=telegram_user.username,
        )
