from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import serializers, viewsets
from .serializer import AssignmentSerializer

from .models import Assignment, Tag


class AssignmentViewset(viewsets.ModelViewSet):
    serializer_class = AssignmentSerializer
    queryset = Assignment.objects.get_queryset().order_by('id')

    def create(self, request, *args, **kwargs):
        assignment_data = request.data
        new_assignment = Assignment.objects.create(assignment_name=assignment_data["assignment_name"],
                                                   due_date=assignment_data["due_date"],
                                                   detail=assignment_data["detail"],
                                                   tag=Tag.objects.get(
                                                       id=assignment_data["tag"])
                                                   )
        new_assignment.save()
        serializer = AssignmentSerializer(new_assignment)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        assignment = self.get_object()
        assignment.delete()

        return Response({"message": "Item has been deleted"})

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
