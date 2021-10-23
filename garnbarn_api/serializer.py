import datetime
from django.db.models import fields
from rest_framework import serializers
from .models import Assignment, Tag


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
            "detail": "example_detail"
            }
    """
    name = serializers.CharField(source='assignment_name')
    dueDate = serializers.DateTimeField(source='due_date')

    class Meta:
        model = Assignment
        fields = ['id',
                  'tag',
                  'name',
                  'dueDate',
                  'timestamp',
                  'detail'
                  ]
        depth = 1

        extra_kwargs = {"assignment_name": {"error_messages": {
            "required": "This assigment requried a name."}}}

    def is_published(self):
        if self.data.get('due_date'):
            due_date = self.data.get('due_date')
            current_time = datetime.datetime.now().timestamp()
            if due_date < current_time:
                return False
        return True
