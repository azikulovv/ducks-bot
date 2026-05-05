from __future__ import annotations

import asyncio
import logging
from typing import Any, TypeVar

import httpx
from pydantic import BaseModel, TypeAdapter, ValidationError

from api.errors import ApiError, BackendErrorPayload
from api.models import (
    EventStatus,
    EventsResponse,
    FeedbackResponse,
    GameType,
    RatingResponse,
    Registration,
    RulesContent,
)

logger = logging.getLogger(__name__)
T = TypeVar("T", bound=BaseModel)


class ApiClient:
    def __init__(
        self,
        base_url: str,
        timeout_seconds: float,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self._owns_client = client is None
        self._client = client or httpx.AsyncClient(
            base_url=base_url.rstrip("/"),
            timeout=httpx.Timeout(timeout_seconds),
        )

    async def close(self) -> None:
        if self._owns_client:
            await self._client.aclose()

    async def get_events(
        self,
        *,
        page: int = 1,
        limit: int = 10,
        game_type: GameType | None = None,
        status: EventStatus | None = "published",
    ) -> EventsResponse:
        params: dict[str, Any] = {"page": page, "limit": limit}
        if game_type is not None:
            params["gameType"] = game_type
        if status is not None:
            params["status"] = status
        return await self._get("/events", EventsResponse, params=params)

    async def register_for_event(self, *, event_id: str, user_id: str) -> Registration:
        return await self._request_model(
            "POST",
            "/register",
            Registration,
            json={"eventId": event_id, "userId": user_id},
        )

    async def get_rating(self, game: GameType, *, page: int = 1, limit: int = 10) -> RatingResponse:
        return await self._get(
            f"/rating/{game}", RatingResponse, params={"page": page, "limit": limit}
        )

    async def get_rules(self) -> RulesContent:
        return await self._get("/rules", RulesContent)

    async def send_feedback(self, *, message: str, name: str | None = None) -> FeedbackResponse:
        payload: dict[str, str] = {"message": message}
        if name:
            payload["name"] = name
        return await self._request_model("POST", "/feedback", FeedbackResponse, json=payload)

    async def _get(
        self,
        path: str,
        model: type[T],
        *,
        params: dict[str, Any] | None = None,
    ) -> T:
        last_error: ApiError | None = None
        for attempt in range(3):
            try:
                return await self._request_model("GET", path, model, params=params)
            except ApiError as exc:
                last_error = exc
                if exc.status_code is not None and exc.status_code < 500:
                    raise
                if attempt < 2:
                    await asyncio.sleep(0.2 * (attempt + 1))
        if last_error is None:
            raise ApiError(None, None)
        raise last_error

    async def _request_model(
        self,
        method: str,
        path: str,
        model: type[T],
        **kwargs: Any,
    ) -> T:
        response = await self._request(method, path, **kwargs)
        try:
            return TypeAdapter(model).validate_python(response.json())
        except ValidationError:
            logger.exception("Backend response validation failed", extra={"path": path})
            raise ApiError(
                response.status_code,
                BackendErrorPayload("INTERNAL_SERVER_ERROR", "Invalid response", {}),
            )

    async def _request(self, method: str, path: str, **kwargs: Any) -> httpx.Response:
        try:
            response = await self._client.request(method, path, **kwargs)
        except httpx.HTTPError:
            logger.exception("Backend request failed", extra={"method": method, "path": path})
            raise ApiError(None, None)

        if response.is_success:
            return response

        payload = self._parse_error_payload(response)
        logger.error(
            "Backend returned error",
            extra={
                "method": method,
                "path": path,
                "status_code": response.status_code,
                "error_code": payload.code if payload else None,
                "error_message": payload.message if payload else None,
            },
        )
        raise ApiError(response.status_code, payload)

    @staticmethod
    def _parse_error_payload(response: httpx.Response) -> BackendErrorPayload | None:
        try:
            raw = response.json()
        except ValueError:
            return BackendErrorPayload("INTERNAL_SERVER_ERROR", response.text[:200], {})

        error = raw.get("error") if isinstance(raw, dict) else None
        if not isinstance(error, dict):
            return BackendErrorPayload("INTERNAL_SERVER_ERROR", "Backend error", {})
        code = error.get("code")
        message = error.get("message")
        details = error.get("details")
        return BackendErrorPayload(
            code=str(code or "INTERNAL_SERVER_ERROR"),
            message=str(message or "Backend error"),
            details=details if isinstance(details, dict) else {},
        )
