from django.db import models
import datetime
from django.utils import timezone

# Create your models here.


class Assignment(models.Model):

    assignment_name = models.CharField(max_length=50)
    due_date = models.DateTimeField('due date')
    timestamp = models.DateTimeField(auto_now_add=True)
    detail = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.assignment_name
