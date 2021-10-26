from typing import Optional
from django.db import models
import datetime
from django.utils import timezone
import math


class Tag(models.Model):
    """Tag or subject"""

    name = models.CharField(max_length=20)
    color = models.CharField(max_length=10, null=True,
                             blank=True, default=None)

    def get_json_data(self):
        return {
            "id": self.id,
            "name": self.name,
            "color": self.color,
        }

    def __str__(self):
        return self.name


class Assignment(models.Model):
    """Data and detail about assignment"""

    # The assignment shouldn't get deleted when tag is deleted.
    tag = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True)

    assignment_name = models.CharField(max_length=50)
    due_date = models.DateTimeField(null=True, blank=True, default=None)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.CharField(
        max_length=1000, null=True, blank=True, default=None)

    def get_json_data(self):
        # Convert timestamp from second to miliseconds base.
        timestamp = self.timestamp.timestamp() * 1000 if self.timestamp else None
        due_date = self.due_date.timestamp() * 1000 if self.due_date else None
        tag = self.tag.get_json_data() if self.tag else None
        return {
            "id": self.id,
            "name": self.assignment_name,
            "tag": tag,
            "description": self.description,
            "timestamp": math.floor(timestamp),
            "dueDate": math.floor(due_date),
        }

    def __str__(self) -> str:
        return self.assignment_name
