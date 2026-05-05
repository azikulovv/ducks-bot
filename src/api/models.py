from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

GameType = Literal["poker", "darts", "billiards"]
EventStatus = Literal["draft", "published", "cancelled", "completed"]


class PageMeta(BaseModel):
    total: int
    page: int
    limit: int
    pages: int


class RegistrationCount(BaseModel):
    registrations: int = 0


class Event(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str
    title: str
    description: str | None = None
    game_type: GameType = Field(alias="gameType")
    starts_at: datetime = Field(alias="startsAt")
    ends_at: datetime | None = Field(default=None, alias="endsAt")
    location: str | None = None
    participant_limit: int | None = Field(default=None, alias="participantLimit")
    points_for_participation: int = Field(default=0, alias="pointsForParticipation")
    status: EventStatus
    count: RegistrationCount = Field(default_factory=RegistrationCount, alias="_count")


class EventsResponse(BaseModel):
    data: list[Event]
    meta: PageMeta


class Registration(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str
    user_id: str = Field(alias="userId")
    event_id: str = Field(alias="eventId")
    status: str
    created_at: datetime = Field(alias="createdAt")
    cancelled_at: datetime | None = Field(default=None, alias="cancelledAt")


class RatingUser(BaseModel):
    id: str
    email: str | None = None
    name: str | None = None


class RatingEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str
    user_id: str = Field(alias="userId")
    game_type: GameType = Field(alias="gameType")
    points: int
    user: RatingUser | None = None


class RatingResponse(BaseModel):
    data: list[RatingEntry]
    meta: PageMeta


class RulesContent(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str
    key: str
    title: str
    body: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class FeedbackResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str
    user_id: str | None = Field(default=None, alias="userId")
    name: str | None = None
    email: str | None = None
    message: str
    created_at: datetime = Field(alias="createdAt")
