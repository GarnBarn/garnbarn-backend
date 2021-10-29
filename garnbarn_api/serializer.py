import datetime
from enum import auto
import time
from django.db import models
from django.db.models import fields
from rest_framework import serializers
from rest_framework.relations import PKOnlyObject
from .models import Assignment, Tag
import math


class TimestampField(serializers.Field):
    def to_representation(self, value):
        return math.floor(value.timestamp() * 1000)

    def to_internal_value(self, value):
        try:
            value = int(value)
        except ValueError:
            raise serializers.ValidationError(
                "The timestamp must be an integer")
        if len(str(value)) != 13:
            raise serializers.ValidationError(
                "The timestamp must be in the milisecond format")
        # Convert the value to Second based timestamp and floor down
        date_converted = datetime.datetime.fromtimestamp(
            math.floor(value/1000))
        return date_converted


class TagIdField(serializers.Field):
    def to_representation(self, value):
        return {
            "id": value.id,
            "name": value.name,
            "color": value.color
        }

    def to_internal_value(self, value):
        try:
            tag_id_from_request = int(value)
            tag_object = Tag.objects.get(id=tag_id_from_request)
        except Tag.DoesNotExist:
            raise serializers.ValidationError("Tag not found")
        except ValueError:
            raise serializers.ValidationError("Tag id must be a number")
        return tag_object


class CreateAssignmentApiSerializer(serializers.ModelSerializer):
    """Serializer for Create Assignment API

    template:
            {
            "name": "example_assignment_name",
            "dueDate": 1635336554,
            "description": "example_detail",
            "tagId": 1
            }
    """
    name = serializers.CharField(source='assignment_name')
    dueDate = TimestampField(source='due_date', default=None)
    timestamp = TimestampField(default=None)

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


class UpdateAssignmentApiSerializer(serializers.ModelSerializer):
    """Serializer for Update API
    """
    name = serializers.CharField(source='assignment_name', required=False)
    dueDate = TimestampField(source='due_date', default=None)
    tagId = TagIdField(source='tag')

    class Meta:
        model = Assignment
        fields = ['id',
                  'tagId',
                  'name',
                  'dueDate',
                  'description'
                  ]
        depth = 1

        read_only_fields = ['tagId', ]


class CreateTagApiSerializer(serializers.ModelSerializer):
    """Serializer for Create Tag API

    template:
        {
            "id": 1
            "name": "example_tag_name"
            "color": "example_color"
        }
    """
    class Meta:
        model = Tag
        fields = ['id',
                'name',
                'color'
                ]
        depth = 1


class UpdateTagApiSerializer(serializers.ModelSerializer):
    """Serializer for the Update Tag API"""
    class Meta:
        model = Tag
        fields = ['id',
                'name',
                'color'
                ]
        depth = 1
