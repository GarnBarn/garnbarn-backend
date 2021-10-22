from rest_framework import serializers
from .models import Assignment


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['id',
                  'tag',
                  'assignment_name',
                  'due_date',
                  'timestamp',
                  'detail'
                  ]
        depth = 1
