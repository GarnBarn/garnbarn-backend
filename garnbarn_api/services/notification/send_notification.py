from django.dispatch.dispatcher import receiver
from garnbarn_api.services.notification.platforms.notification_platform import NotificationPlatform
from garnbarn_api.services.notification.platforms.line import Line
from garnbarn_api.signals.publish_notification_signal import notification_signal


notifier = NotificationPlatform.__subclasses__()


@receiver(notification_signal)
def send_notification(sender, assignment_obj, **kwargs):
    """Receive signals when an assignment is created or updated,
    then invoke all platform notifier methods.
    """
    for platform in notifier:
        temp = platform()
        temp.notify(assignment_obj)
