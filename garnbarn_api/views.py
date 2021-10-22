from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import serializers, viewsets, status
from .serializer import AssignmentSerializer

from .models import Assignment, Tag


class AssignmentViewset(viewsets.ModelViewSet):
    serializer_class = AssignmentSerializer
    queryset = Assignment.objects.get_queryset().order_by('id')

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            Assignment.objects.create(**serializer.validated_data)
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'Bad Request',
            'message': 'Assignment could not be created with received data'
        }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        assignment = self.get_object()
        assignment_name = assignment.assignment_name
        assignment.delete()

        return Response({"message": "Assignment:" + assignment_name + " has been deleted"})

    def update(self, request, *args, **kwargs):
        assignment_object = self.get_object()
        data = request.data
        tag = Tag.objects.get(tag_name=data["tag_name"])

        assignment_object.tag = tag
        assignment_object.assignment_name = data["assignment_name"]
        assignment_object.due_date = data["due_date"]
        assignment_object.detail = data["detail"]

        assignment_object.save()

        serializer = AssignmentSerializer(assignment_object)
        return Response(serializer.data)