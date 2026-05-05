from __future__ import annotations

from db.repositories import FeedbackRepository


class FeedbackService:
    def __init__(self, feedback: FeedbackRepository) -> None:
        self.feedback = feedback

    def save(self, user_id: int, message: str, forwarded: bool) -> int:
        message = message.strip()
        if not 5 <= len(message) <= 2000:
            raise ValueError("Сообщение должно быть от 5 до 2000 символов")
        return self.feedback.create(user_id, message, forwarded)

    def mark_forwarded(self, user_id: int, message: str) -> None:
        self.feedback.mark_last_forwarded(user_id, message.strip())
