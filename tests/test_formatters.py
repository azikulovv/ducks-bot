from __future__ import annotations

from datetime import UTC, datetime

from api.models import Event, RatingEntry, RatingUser, RegistrationCount
from bot.formatters import format_event, format_rating


def test_format_event_contains_required_fields() -> None:
    event = Event(
        id="evt_1",
        title="Friday Poker Night",
        description="Texas Hold'em community event.",
        gameType="poker",
        startsAt=datetime(2026, 5, 8, 10, 0, tzinfo=UTC),
        endsAt=None,
        location="DUCK'S GameClub main hall",
        participantLimit=24,
        pointsForParticipation=10,
        status="published",
        _count=RegistrationCount(registrations=3),
    )

    text = format_event(event)

    assert "Friday Poker Night" in text
    assert "Игра: Poker" in text
    assert "Участники: 3 / 24" in text


def test_format_rating_numbers_players() -> None:
    entry = RatingEntry(
        id="rating_1",
        userId="user_1",
        gameType="poker",
        points=120,
        user=RatingUser(id="user_1", email="player@example.test", name="Demo Player"),
    )

    assert "1. Demo Player — 120 очков" in format_rating("poker", [entry])
