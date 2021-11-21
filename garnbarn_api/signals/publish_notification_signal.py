import django.dispatch

from garnbarn_api.models import Assignment

notification_signal = django.dispatch.Signal(providing_args=["assignment_obj"])


def publish_notification_signal(assignment_obj: Assignment):
    """Send signal to notification handler."""
    notification_signal.send(sender="job_executed",
                             assignment_obj=assignment_obj)
