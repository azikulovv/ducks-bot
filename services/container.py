from __future__ import annotations

from dataclasses import dataclass

from db.database import Database
from db.repositories import (
    EventRepository,
    FeedbackRepository,
    RatingRepository,
    RegistrationRepository,
    UserRepository,
)
from services.event_service import EventService
from services.feedback_service import FeedbackService
from services.notification_service import NotificationService
from services.rating_service import RatingService
from services.user_service import UserService


@dataclass(frozen=True)
class ServiceContainer:
    users: UserService
    events: EventService
    ratings: RatingService
    feedback: FeedbackService
    notifications: NotificationService


def build_services(db: Database) -> ServiceContainer:
    user_repo = UserRepository(db)
    event_repo = EventRepository(db)
    reg_repo = RegistrationRepository(db)
    rating_repo = RatingRepository(db)
    feedback_repo = FeedbackRepository(db)

    return ServiceContainer(
        users=UserService(user_repo),
        events=EventService(event_repo, reg_repo),
        ratings=RatingService(rating_repo),
        feedback=FeedbackService(feedback_repo),
        notifications=NotificationService(event_repo, reg_repo, user_repo),
    )
