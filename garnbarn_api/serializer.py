import datetime
from enum import auto
import time
from rest_framework import serializers
from .models import Assignment, Tag


class TimestampField(serializers.Field):
    def to_representation(self, value):
        return int(value.timestamp())

    def to_internal_value(self, value):
        return datetime.datetime.fromtimestamp(int(value))


class AssignmentSerializer(serializers.ModelSerializer):
    """Seriralizer for Assignment's object

    template:
            {
            "id": 1,
            "tag": {
                "id": 1,
                "tag_name": "example_tag_name"
            },
            "name": "example_assignment_name",
            "dueDate": 1635336554,
            "timestamp": 1634904558,
            "description": "example_detail"
            }
    """
    name = serializers.CharField(source='assignment_name')
    dueDate = TimestampField(source='due_date', default=None)

    class Meta:
        model = Assignment
        fields = ['id',
                  'tag',
                  'name',
                  'dueDate',
                  'timestamp',
                  'description'
                  ]
        depth = 1

        read_only_fields = ['timestamp']
