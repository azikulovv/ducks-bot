from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class BackendErrorPayload:
    code: str
    message: str
    details: dict[str, Any]


class ApiError(Exception):
    def __init__(self, status_code: int | None, payload: BackendErrorPayload | None) -> None:
        self.status_code = status_code
        self.payload = payload
        super().__init__(payload.message if payload else "Backend request failed")

    @property
    def code(self) -> str:
        if self.payload:
            return self.payload.code
        return "NETWORK_ERROR"


def user_message_for_error(error: ApiError) -> str:
    messages = {
        "VALIDATION_ERROR": "Проверьте данные и попробуйте еще раз.",
        "NOT_FOUND": "Данные не найдены.",
        "CONFLICT": "Вы уже записаны или лимит участников достигнут.",
        "UNAUTHORIZED": "Сервис временно недоступен для запроса.",
        "FORBIDDEN": "Недостаточно прав для выполнения действия.",
        "INTERNAL_SERVER_ERROR": "На стороне клуба произошла ошибка. Попробуйте позже.",
        "NETWORK_ERROR": "Не удалось связаться с сервисом клуба. Попробуйте позже.",
    }
    return messages.get(error.code, "Не удалось выполнить запрос. Попробуйте позже.")
