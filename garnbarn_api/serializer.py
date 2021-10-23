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

        # error_message = {
        #     'assignment_name': {
        #         'required': 'This assigment requried a name.')
        #     }
        # }

    # def validate_detail(self, data):
    #     if 'detail' not in data:
    #         print('ok')
    #         raise serializers.ValidationError('Assignment needed a name.')
    #     # return data
    #         # print(data)
    #     return data