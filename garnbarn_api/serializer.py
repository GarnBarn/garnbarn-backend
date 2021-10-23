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

        extra_kwargs = {"assignment_name": {"error_messages": {
            "required": "This assigment requried a name."}}}

    def is_published(self):
        if self.data.get('due_date') > self.data.get('timestamp'):
            return True
