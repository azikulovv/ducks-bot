from __future__ import annotations

import logging

from telegram.ext import ContextTypes

from config import Settings
from db.repositories import EventRepository, RegistrationRepository, UserRepository
from services.event_service import format_event


logger = logging.getLogger(__name__)


class NotificationService:
    def __init__(
        self,
        events: EventRepository,
        registrations: RegistrationRepository,
        users: UserRepository,
    ) -> None:
        self.events = events
        self.registrations = registrations
        self.users = users

    async def send_new_event_broadcast(
        self,
        context: ContextTypes.DEFAULT_TYPE,
        settings: Settings,
        event_id: int,
    ) -> None:
        if not settings.broadcast_new_events:
            return
        event = self.events.get(event_id)
        if not event:
            return
        text = "Новое мероприятие клуба:\n\n" + format_event(event, settings.timezone)
        for user in self.users.list_all():
            try:
                await context.bot.send_message(chat_id=user.telegram_id, text=text)
            except Exception:
                logger.exception("Failed to broadcast event %s to user %s", event_id, user.telegram_id)

    async def send_24h_reminders(
        self,
        context: ContextTypes.DEFAULT_TYPE,
        settings: Settings,
    ) -> None:
        for event in self.events.due_for_24h_reminder():
            text = "Напоминание: мероприятие начнется примерно через 24 часа.\n\n"
            text += format_event(event, settings.timezone)
            telegram_ids = self.registrations.list_event_telegram_ids(event.id)
            for telegram_id in telegram_ids:
                try:
                    await context.bot.send_message(chat_id=telegram_id, text=text)
                except Exception:
                    logger.exception(
                        "Failed to send 24h reminder for event %s to user %s",
                        event.id,
                        telegram_id,
                    )
            self.events.mark_24h_reminded(event.id)
