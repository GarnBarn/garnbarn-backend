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
        """ Create Assignment object.

        Returns:
            If the given data contain all
            requirements(assignment_name is included and due_date > now)
            , returns assignment's object in json.
            Else, returns bad request status
        """
        serializer = self.serializer_class(data=request.data)
        message = 'Assignment could not be created with received data'

        if serializer.is_valid(raise_exception=True) and serializer.is_published():
            assignment_object = Assignment.objects.create(
                **serializer.validated_data)
            # add tag to assignment by giving the tag's id
            try:
                assignment_object.tag = Tag.objects.get(id=request.data["tag"])
            except Tag.DoesNotExist:
                return Response({
                    'message': "Tag's ID not found"
                }, status=status.HTTP_400_BAD_REQUEST)

            assignment_object.save()

            assignment_serializer = AssignmentSerializer(assignment_object)
            return Response(assignment_serializer.data, status=status.HTTP_201_CREATED)

        if not serializer.is_published():
            message = 'Invalid due date'

        return Response({
            'message': message
        }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """ Remove assignment with specified id.

        Returns:
            Response message telling which assignment has been deleted.
        """
        assignment = self.get_object()
        assignment.delete()

        return Response({}, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        """ Update data of a specified assignment

        Returns:
            Assignment's object in json.
        """
        assignment_object = self.get_object()
        data = request.data

        try:
            tag = Tag.objects.get(tag_name=data["tag_name"])
            assignment_object.tag = tag
        except KeyError:
            pass

        assignment_object.assignment_name = data.get(
            "name", assignment_object.assignment_name)
        assignment_object.due_date = data.get(
            "dueDate", assignment_object.due_date)
        assignment_object.detial = data.get(
            "detial", assignment_object.detail)

        assignment_object.save()

        serializer = AssignmentSerializer(assignment_object)
        return Response(serializer.data, status=status.HTTP_200_OK)
