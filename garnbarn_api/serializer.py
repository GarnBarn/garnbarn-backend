from rest_framework import serializers
from .models import Assignment


class AssignmentSerializer(serializers.ModelSerializer):
    """Seriralizer for assignment's object

    Assignment:
            {
            "id": 1,
            "tag": {
                "id": 1,
                "tag_name": "example_tag_name"
            },
            "assignment_name": "example_assignment_name",
            "due_date": 1635336554,
            "timestamp": 1634904558,
            "detail": "example_detail"
            }
    """
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
