import datetime
from enum import auto
import time
from django.db import models
from django.db.models import fields, query_utils
from rest_framework import serializers
from rest_framework.relations import PKOnlyObject
from .models import Assignment, CustomUser, Tag
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


class ReminderTimeField(serializers.ListField):
    def to_internal_value(self, data):
        if data == []:
            return None
        data = super().to_internal_value(data)
        data.sort()
        return data


class TagIdField(serializers.Field):
    def to_representation(self, value):
        return {
            "id": value.id,
            "name": value.name,
            "author": value.author,
            "color": value.color,
            "reminderTime": value.reminder_time
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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['uid', 'name', 'line']

        read_only_fields = ['uid']


class CreateTagApiSerializer(serializers.ModelSerializer):
    """Serializer for Create Tag API

    template:
        {
            "id": 1
            "name": "example_tag_name"
            "color": "example_color"
        }
    """
    reminderTime = ReminderTimeField(source='reminder_time', default=None,
                                     child=serializers.IntegerField()
                                     )
    author = serializers.PrimaryKeyRelatedField(
        source='author.uid', read_only=True, default=None)
    subscriber = serializers.ListField(default=None,
                                       child=serializers.CharField()
                                       )

    class Meta:
        model = Tag
        fields = ['id',
                  'name',
                  'author',
                  'color',
                  'reminderTime',
                  'subscriber'
                  ]
        depth = 1

        read_only_fields = ['author']


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
    author = serializers.PrimaryKeyRelatedField(
        source='author.uid', read_only=True, default=None)
    reminderTime = ReminderTimeField(source='reminder_time', default=None,
                                     child=serializers.IntegerField()
                                     )
    tag = CreateTagApiSerializer(default=None)

    class Meta:
        model = Assignment
        fields = ['id',
                  'author',
                  'tag',
                  'name',
                  'dueDate',
                  'timestamp',
                  'description',
                  'reminderTime'
                  ]
        depth = 1

        read_only_fields = ['timestamp', 'author']


class UpdateAssignmentApiSerializer(serializers.ModelSerializer):
    """Serializer for Update API
    """
    name = serializers.CharField(source='assignment_name', required=False)
    dueDate = TimestampField(source='due_date', default=None)
    tagId = TagIdField(source='tag')
    reminderTime = ReminderTimeField(source='reminder_time', default=None,
                                     child=serializers.IntegerField()
                                     )

    class Meta:
        model = Assignment
        fields = ['id',
                  'tagId',
                  'name',
                  'dueDate',
                  'description',
                  'reminderTime'
                  ]
        depth = 1

        read_only_fields = ['tagId', ]


class UpdateTagApiSerializer(serializers.ModelSerializer):
    """Serializer for the Update Tag API"""
    reminderTime = ReminderTimeField(source='reminder_time', default=None,
                                     child=serializers.IntegerField()
                                     )
    subscriber = serializers.ListField(default=None,
                                       child=serializers.CharField()
                                       )

    class Meta:
        model = Tag
        fields = ['id',
                  'name',
                  'author',
                  'color',
                  'reminderTime',
                  'subscriber'
                  ]
        depth = 1
        read_only_fields = ['author']


class CustomUserSerializer(serializers.ModelSerializer):
    """Serializer for user object
    """
    class Meta:
        model = CustomUser
        fields = '__all__'

        read_only_fields = ['uid', ]
