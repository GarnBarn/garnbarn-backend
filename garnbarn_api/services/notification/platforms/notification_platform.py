from abc import abstractmethod

from garnbarn_api.models import CustomUser


class NotificationPlatform():

    def notify(self, assignment_obj):
        """Invoke notification_handler."""
        receiver = {assignment_obj.author}
        if assignment_obj.tag:
            tag_subscriber = assignment_obj.tag.subscriber
            subscriber = self._convert_subscriber_to_obj(tag_subscriber)
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
