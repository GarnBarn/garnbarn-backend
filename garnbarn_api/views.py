from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import serializers, viewsets
from .serializer import AssignmentSerializer

from .models import Assignment, Tag


@api_view()
@permission_classes([AllowAny])
def index(request):
    return Response({"message": "request recieved"})


class AssignmentViewset(viewsets.ModelViewSet):
    serializer_class = AssignmentSerializer

    def get_queryset(self):
        assignment = Assignment.objects.all()
        return assignment

    def retrieve(self, request, *args, **kwargs):
        """This method filter the data inside ModelViewset."""
        params = kwargs
        assignment = Assignment.objects.filter(assignment_name=params['pk'])
        serializer = AssignmentSerializer(assignment)
        return Response(serializer.data)
