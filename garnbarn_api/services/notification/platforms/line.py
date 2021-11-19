from garnbarn_api.services.notification.platforms.notification_platform import NotificationPlatform
from garnbarn_api.services.line import LineMessagingApiHelper
import logging

logger = logging.getLogger("notification")


class Line(NotificationPlatform):
    PLATFORM_NAME = "LINE"
    messaging_api = LineMessagingApiHelper()

    def notification_handler(self, assignment_obj, user_obj):
        self.messaging_api.send_assignment_notification(
            user_obj.line, assignment_obj)
