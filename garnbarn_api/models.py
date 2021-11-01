from typing import Optional
from django.db import models
import datetime
from django.db.models.deletion import CASCADE, SET_NULL
from django.utils import timezone
import math
import uuid

from rest_framework import serializers


class CustomUser(models.Model):
    """Information of the User."""
    uid = models.CharField(max_length=40, primary_key=True, default='Unknown')
    name = models.CharField(max_length=20)
    line = models.CharField(max_length=64, null=True, blank=True)

    def get_json_data(self):
        return {
            "uid": self.uid,
            "name": self.name,
            "line": self.line
        }

    def __str__(self):
        return self.name

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
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    assignment_name = models.CharField(max_length=50)
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
