from abc import ABC, abstractmethod
from django.dispatch import receiver

from garnbarn_api.signals.publish_notification_signal import notification_signal
from garnbarn_api.models import CustomUser


class NotificationPlatform(ABC):

    # @receiver(notification_signal)
    def notify(self, sender, assignment_obj, **kwargs):
        """Invoke notification_handler."""
        subscriber = self._convert_subscriber_to_obj(
            assignment_obj.tag.subscriber)
        receiver = set(assignment_obj.author)
        receiver = receiver.union(subscriber)

        for user in receiver:
            self.notification_handler(assignment_obj, user)

    @abstractmethod
    def notification_handler(self, assignment_obj, user_obj):
        pass

    @staticmethod
    def _convert_subscriber_to_obj(subscriber):
        """Covert user's id in tag subscriber to user object.

        Args:
            subscriber (list): List of subscriber's uid.

        Returns:
            (set): List of subscriber objects.
        """
        subscriber_obj_list = {}
        for user_id in subscriber:
            user = CustomUser.objects.get(uid=user_id)
            subscriber_obj_list.add(user)
        return subscriber_obj_list


# @receiver(notification_signal)
# def test(sender, assignment_obj, **kwargs):
#     print(f"This is {assignment_obj.assignment_name}")


class Line(NotificationPlatform):
    def notification_handler(self, assignment_obj, user_obj):
        print(f"This is {assignment_obj} of {user_obj}")
