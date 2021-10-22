from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import serializers, viewsets
from .serializer import AssignmentSerializer, TagSerializer

from .models import Assignment, Tag


class AssignmentViewset(viewsets.ModelViewSet):
    serializer_class = AssignmentSerializer

    def get_queryset(self):
        assignment = Assignment.objects.get_queryset().order_by('id')
        return assignment

    def create(self, request, *args, **kwargs):
        """Override create action."""

        assignment_data = request.data
        print(assignment_data)
        new_assignment = Assignment.objects.create(assignment_name=assignment_data["assignment_name"],
                                                   due_date=assignment_data["due_date"],
                                                   detail=assignment_data["detail"])
        new_assignment.save()
        serializer = AssignmentSerializer(new_assignment)
        return Response(serializer.data)


class TagViewset(viewsets.ModelViewSet):
    serializer_class = TagSerializer

    def get_queryset(self):
        tag = Tag.objects.all()
        return tag
