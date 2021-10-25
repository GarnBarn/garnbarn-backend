import datetime
from enum import auto
import time
from django.db import models
from django.db.models import fields
from rest_framework import serializers
from rest_framework.relations import PKOnlyObject
from .models import Assignment, Tag


class TimestampField(serializers.Field):
    def to_representation(self, value):
        return int(value.timestamp())

    def to_internal_value(self, value):
        return datetime.datetime.fromtimestamp(int(value))


class AssignmentSerializer(serializers.ModelSerializer):
    """Serializer for Assignment's object

    template:
            {
            "id": 1,
            "tag": {
                "id": 1,
                "name": "example_tag_name"
                "color": "example_color"
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
