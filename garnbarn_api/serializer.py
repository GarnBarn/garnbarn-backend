from rest_framework import serializers
from .models import Assignment, Tag


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['id',
                  'assignment_name',
                  'due_date',
                  'timestamp',
                  'detail'
                  ]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['tag_name', 'tag_id']
