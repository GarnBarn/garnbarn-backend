from garnbarn_api.services.notification.platforms.notification_platform import NotificationPlatform
import logging

logger = logging.getLogger("notification")


class Line(NotificationPlatform):

    def notification_handler(self, assignment_obj, user_obj):
        try:
            # TODO: Send notifiation
            print(f"This is {assignment_obj} of {user_obj}")
            pass
        except:
            logger.warning("Notification can't be sent.")
