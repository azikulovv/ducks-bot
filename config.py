from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os

from dotenv import load_dotenv


load_dotenv()


def _required(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Environment variable {name} is required")
    return value


def _parse_int_set(raw: str | None) -> set[int]:
    if not raw:
        return set()
    values: set[int] = set()
    for item in raw.split(","):
        item = item.strip()
        if not item:
            continue
        try:
            values.add(int(item))
        except ValueError as exc:
            raise RuntimeError(f"Invalid integer value in admin list: {item}") from exc
    return values


@dataclass(frozen=True)
class Settings:
    bot_token: str
    admin_ids: set[int]
    admin_chat_id: int | None
    database_path: Path
    timezone: str
    club_name: str
    support_telegram: str
    support_email: str
    broadcast_new_events: bool
    log_level: str

    @classmethod
    def from_env(cls) -> "Settings":
        admin_chat = os.getenv("ADMIN_CHAT_ID")
        return cls(
            bot_token=_required("BOT_TOKEN"),
            admin_ids=_parse_int_set(os.getenv("ADMIN_IDS")),
            admin_chat_id=int(admin_chat) if admin_chat else None,
            database_path=Path(os.getenv("DATABASE_PATH", "data/ducks_bot.sqlite3")),
            timezone=os.getenv("TIMEZONE", "Asia/Almaty"),
            club_name=os.getenv("CLUB_NAME", "DUCK'S"),
            support_telegram=os.getenv("SUPPORT_TELEGRAM", "@ducks_support"),
            support_email=os.getenv("SUPPORT_EMAIL", "support@example.com"),
            broadcast_new_events=os.getenv("BROADCAST_NEW_EVENTS", "true").lower()
            in {"1", "true", "yes", "on"},
            log_level=os.getenv("LOG_LEVEL", "INFO"),
        )


settings = Settings.from_env()
