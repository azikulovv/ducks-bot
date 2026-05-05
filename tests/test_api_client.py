from __future__ import annotations

import httpx
import pytest

from api.client import ApiClient
from api.errors import ApiError


@pytest.mark.asyncio
async def test_get_events_sends_expected_query_params() -> None:
    seen_request: httpx.Request | None = None

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal seen_request
        seen_request = request
        return httpx.Response(
            200,
            json={
                "data": [],
                "meta": {"total": 0, "page": 1, "limit": 10, "pages": 0},
            },
        )

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(base_url="http://backend.test/api", transport=transport) as http:
        client = ApiClient("http://backend.test/api", 10, client=http)
        response = await client.get_events(game_type="poker")

    assert response.data == []
    assert seen_request is not None
    assert seen_request.url.path == "/api/events"
    assert dict(seen_request.url.params) == {
        "page": "1",
        "limit": "10",
        "gameType": "poker",
        "status": "published",
    }


@pytest.mark.asyncio
async def test_api_error_parses_backend_error_code() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            409,
            json={"error": {"code": "CONFLICT", "message": "Already registered", "details": {}}},
        )

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(base_url="http://backend.test/api", transport=transport) as http:
        client = ApiClient("http://backend.test/api", 10, client=http)
        with pytest.raises(ApiError) as exc_info:
            await client.register_for_event(event_id="evt_1", user_id="user_1")

    assert exc_info.value.code == "CONFLICT"


@pytest.mark.asyncio
async def test_get_requests_are_retried_on_server_errors() -> None:
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        if calls == 1:
            return httpx.Response(
                500,
                json={"error": {"code": "INTERNAL_SERVER_ERROR", "message": "Retry", "details": {}}},
            )
        return httpx.Response(
            200,
            json={
                "data": [],
                "meta": {"total": 0, "page": 1, "limit": 10, "pages": 0},
            },
        )

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(base_url="http://backend.test/api", transport=transport) as http:
        client = ApiClient("http://backend.test/api", 10, client=http)
        response = await client.get_events()

    assert response.data == []
    assert calls == 2


@pytest.mark.asyncio
async def test_post_requests_are_not_retried() -> None:
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        return httpx.Response(
            500,
            json={"error": {"code": "INTERNAL_SERVER_ERROR", "message": "No retry", "details": {}}},
        )

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(base_url="http://backend.test/api", transport=transport) as http:
        client = ApiClient("http://backend.test/api", 10, client=http)
        with pytest.raises(ApiError):
            await client.register_for_event(event_id="evt_1", user_id="user_1")

    assert calls == 1
