from django.db import models
import datetime
from django.utils import timezone


class Assignment(models.Model):

    assignment_name = models.CharField(max_length=50)
    due_date = models.DateTimeField('due date', default=None)
    timestamp = models.DateTimeField(auto_now_add=True)
    detail = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.assignment_name


class Tag(models.Model):
    """Class that contain tags or subject of the users."""

    tag_name = models.CharField(max_length=20)

    def __str__(self):
        return self.tag_name
