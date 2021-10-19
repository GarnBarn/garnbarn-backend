from django.db import models
import datetime
from django.utils import timezone

# Create your models here.


class Assignment(models.Model):

    assignment_name = models.CharField(max_length=200)
    due_date = models.DateTimeField('due date')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.assignment_name

    def get_assignment(self):
        pass

    def remove_assignment(self, pk):
        pass
