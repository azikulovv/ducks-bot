from handlers.admin import admin_handlers
from handlers.common import common_handlers
from handlers.events import event_handlers
from handlers.feedback import feedback_handlers
from handlers.rating import rating_handlers


def all_handlers():
    return [
        *common_handlers(),
        *event_handlers(),
        *rating_handlers(),
        *feedback_handlers(),
        *admin_handlers(),
    ]
