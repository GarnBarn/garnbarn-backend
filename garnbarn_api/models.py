from typing import Optional
from django.db import models
import datetime
from django.utils import timezone


class Tag(models.Model):
    """Tag or subject"""

    tag_name = models.CharField(max_length=20)

    def __str__(self):
        return self.tag_name


class Assignment(models.Model):
    """Data and detail about assignment"""

    # The assignment shouldn't get deleted when tag is deleted.
    tag = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True)

    assignment_name = models.CharField(max_length=50)
    due_date = models.DateTimeField(null=True, blank=True, default=None)
    timestamp = models.DateTimeField(auto_now_add=True)
    detail = models.CharField(
        max_length=200, null=True, blank=True, default=None)

    def __str__(self) -> str:
        return self.assignment_name
