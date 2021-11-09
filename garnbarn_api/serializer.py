import datetime
from enum import auto
from sys import platform
import time
from django.db import models
from django.db.models import fields, query_utils
from rest_framework import serializers
from rest_framework.relations import PKOnlyObject
from .models import Assignment, CustomUser, Tag
import math
from firebase_admin import auth


class TimestampField(serializers.Field):
    """Field for timestamp"""

    def to_representation(self, value):
        """Representation of timestamp in milisecond"""
        return math.floor(value.timestamp() * 1000)

    def to_internal_value(self, value):
        """Method for internal value

        Returns:
            Python's datetime format.
        """
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
    """Field for reminder time"""

    def to_internal_value(self, data):
        """Method for internal value

        Returns:
            A sorted list of reminder time, if incoming data
            is an empty list return None.
        """
        if data == []:
            return None
        data = super().to_internal_value(data)
        data.sort()
        return data


class TagIdField(serializers.Field):
    def to_representation(self, value):
        """Representation format of tag in Assignment serializer"""
        author = value.author.uid if value.author else None
        return {
            "id": value.id,
            "name": value.name,
            "author": author,
            "color": value.color,
            "reminderTime": value.reminder_time,
            "subscriber": value.subscriber
        }

    def to_internal_value(self, value):
        """Method for internal value"""
        try:
            tag_id_from_request = int(value)
            tag_object = Tag.objects.get(id=tag_id_from_request)
        except Tag.DoesNotExist:
            raise serializers.ValidationError("Tag not found")
        except ValueError:
            raise serializers.ValidationError("Tag id must be a number")
        except TypeError:
            raise serializers.ValidationError(
                "tagId must be able to be converted to an integer")
        return tag_object


class CustomUserSerializer(serializers.ModelSerializer):
    """Serializer for user object
    """

    class Meta:
        model = CustomUser
        fields = ['uid', 'line']

        read_only_fields = ['uid']

    def to_representation(self, obj):
        uid = obj.uid
        line_user_id = obj.line
        try:
            firebase_user = auth.get_user(uid)
        except auth.UserNotFoundError:
            raise serializers.ValidationError("User not found")
        displayName = firebase_user.display_name
        profileImage = firebase_user.photo_url
        platform = {}
        if line_user_id:
            platform["line"] = line_user_id

        primitive_repr = {}
        primitive_repr["displayName"] = displayName
        primitive_repr["profileImage"] = profileImage
        primitive_repr["platform"] = platform
        return primitive_repr


class TagSerializer(serializers.ModelSerializer):
    """Serializer for Tag

    template:
        {
            "id": 1,
            "name": "example_tag_name",
            "color": "example_color",
            "author": "user_id",
            "reminderTime": [
                1,
                2,
                3
            ]
            "subscriber": [
                "uid1",
                "uid2",
                "uid3"
            ]
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

        read_only_fields = ['author', 'id']


class AssignmentSerializer(serializers.ModelSerializer):
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
    tagId = TagIdField(source="tag", default=None, allow_null=True)

    class Meta:
        model = Assignment
        fields = ['id',
                  'author',
                  'tagId',
                  'name',
                  'dueDate',
                  'timestamp',
                  'description',
                  'reminderTime'
                  ]
        depth = 1

        read_only_fields = ['timestamp', 'author']

    def to_representation(self, obj):
        """Representation format of Assignment serializer"""
        primitive_repr = super(
            AssignmentSerializer, self).to_representation(obj)
        primitive_repr['tag'] = primitive_repr['tagId']
        del primitive_repr['tagId']
        return primitive_repr
