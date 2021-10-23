from django.db import models
import datetime
from django.utils import timezone


class Tag(models.Model):
    """Class that contain tags or subject of the users."""

    tag_name = models.CharField(max_length=20)

    def __str__(self):
        return self.tag_name


class Assignment(models.Model):
    """Contain data and detail about assignment"""

    # The assignment shouldn't get deleted when tag is deleted.
    tag = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True)
    assignment_name = models.CharField(max_length=50)
    due_date = models.DateTimeField('due date')
    timestamp = models.DateTimeField(auto_now_add=True)
    detail = models.CharField(max_length=200, default="")

    def __str__(self) -> str:
        return self.assignment_name
