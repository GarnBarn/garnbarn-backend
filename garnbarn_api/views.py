from rest_framework.response import Response
from rest_framework import viewsets, status
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
        data = request.data
        serializer = self.serializer_class(data=data)
        message = 'Assignment could not be created with received data'

        if serializer.is_valid(raise_exception=True):
            assignment_object = Assignment(**serializer.validated_data)

            # add tag to assignment by giving the tag's id
            try:
                assignment_object.tag = Tag.objects.get(id=request.data["tag"])
            except Tag.DoesNotExist:
                return Response({
                    'message': "Tag's ID not found"
                }, status=status.HTTP_400_BAD_REQUEST)

            assignment_object.save()

            assignment_serializer = AssignmentSerializer(assignment_object)
            return Response(assignment_serializer.data, status=status.HTTP_200_OK)

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

        assignment_object.assignment_name = data.get(
            "name", assignment_object.assignment_name)
        assignment_object.due_date = data.get(
            "dueDate", assignment_object.due_date)
        assignment_object.detial = data.get(
            "description", assignment_object.description)

        assignment_object.save()

        serializer = AssignmentSerializer(assignment_object)
        return Response(serializer.data, status=status.HTTP_200_OK)
