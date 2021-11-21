from garnbarn_api.services.notification.platforms.notification_platform import NotificationPlatform
from garnbarn_api.services.line import LineMessagingApiHelper
import logging

logger = logging.getLogger("notification")


class Line(NotificationPlatform):
    PLATFORM_NAME = "LINE"
    messaging_api = LineMessagingApiHelper()

    def notification_handler(self, assignment_obj, user_obj):
        """Send notification to user on LINE Platform."""
        if not user_obj.line:
            logger.warn(
                f"User {user_obj.uid} doesn't linked any LINE Account. Skipping sending the notification for the assignment {assignment_obj.id}")
            return
        self.messaging_api.send_assignment_notification(
            user_obj.line, assignment_obj)
