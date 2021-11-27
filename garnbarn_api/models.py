from django.db import models
import math


class CustomUser(models.Model):
    """Information of the User."""
    uid = models.CharField(max_length=40, primary_key=True)
    line = models.CharField(max_length=64, null=True, blank=True)

    def get_json_data(self):
        return {
            "uid": self.uid,
            "line": self.line
        }

    def __str__(self):
        return self.uid

    @property
    def is_anonymous(self):
        """
        Always return False. This is a way of comparing User objects to
        anonymous users.
        """
        return False

    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True


class Tag(models.Model):
    """Tag or subject"""

    name = models.CharField(max_length=20)
    color = models.CharField(max_length=10, null=True,
                             blank=True, default=None)
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, blank=True, null=True, default=None)
    reminder_time = models.JSONField(blank=True, null=True, default=None)
    subscriber = models.JSONField(blank=True, null=True, default=None)
    secret_key_totp = models.CharField(blank=True, null=True, max_length=40)

    def get_json_data(self):
        author = self.author.uid if self.author else None
        return {
            "id": self.id,
            "name": self.name,
            "author": author,
            "color": self.color,
            "reminderTime": self.reminder_time,
            "subscriber": self.subscriber
        }

    def __str__(self):
        return self.name


class Assignment(models.Model):
    """Data and detail about assignment"""

    # The assignment shouldn't get deleted when tag is deleted.
    tag = models.ForeignKey(Tag, on_delete=models.SET_NULL,
                            null=True, blank=True, default=None)
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, blank=True, null=True, default=None)
    assignment_name = models.CharField(max_length=100)
    due_date = models.DateTimeField(null=True, blank=True, default=None)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.CharField(
        max_length=1000, null=True, blank=True, default=None)
    reminder_time = models.JSONField(blank=True, null=True, default=None)

    def get_json_data(self):
        # Convert timestamp from second to miliseconds base.
        timestamp = math.floor(self.timestamp.timestamp()
                               * 1000) if self.timestamp else None
        due_date = math.floor(self.due_date.timestamp() *
                              1000) if self.due_date else None
        tag = self.tag.get_json_data() if self.tag else None
        author = self.author.uid if self.author else None
        return {
            "id": self.id,
            "author": author,
            "name": self.assignment_name,
            "tag": tag,
            "description": self.description,
            "timestamp": timestamp,
            "dueDate": due_date,
            "reminderTime": self.reminder_time
        }

    def __str__(self) -> str:
        return self.assignment_name
