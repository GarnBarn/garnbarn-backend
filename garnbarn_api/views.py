from django.db.models.query import QuerySet
from rest_framework.response import Response
from rest_framework import serializers, viewsets, status
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
import garnbarn_api.serializer as garnbarn_serializer
from .authentication import FirebaseAuthIDTokenAuthentication
from datetime import datetime

from .models import Assignment, Tag


class AssignmentViewset(viewsets.ModelViewSet):
    authentication_classes = [FirebaseAuthIDTokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = garnbarn_serializer.GetAssignmentApiSerializer

    def get_queryset(self):
        if self.request.query_params.get('fromPresent') == "true":
            data = Assignment.objects.exclude(
                due_date__lt=datetime.now()).order_by('due_date')
        else:
            data = Assignment.objects.get_queryset().order_by('id')
        return data

    def create(self, request, *args, **kwargs):
        """ Create Assignment object.

        Returns:
            If the given data contain all
            requirements(assignment_name is included and due_date > now)
            , returns assignment's object in json.
            Else, returns bad request status
        """
        data = request.data
        serializer = garnbarn_serializer.CreateAssignmentApiSerializer(
            data=data)

        if not serializer.is_valid():
            # Response 400 if the request body is invalid
            return Response({
                'message': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        assignment_object = Assignment(**serializer.validated_data)

        tag_id_from_request = request.data.get("tagId")
        if tag_id_from_request is not None:
            # Check the tagId is founded in the database. If not, Response 400.
            try:
                tag_id_from_request = int(tag_id_from_request)
                assignment_object.tag = Tag.objects.get(id=tag_id_from_request)
            except Tag.DoesNotExist:
                return Response({
                    'message': "Tag's ID not found"
                }, status=status.HTTP_400_BAD_REQUEST)
            except ValueError:
                return Response({
                    'message': "tagId must be able to be converted to an integer"
                }, status=status.HTTP_400_BAD_REQUEST)

        assignment_object.save()
        return Response(assignment_object.get_json_data(), status=status.HTTP_200_OK)

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
        data = request.data
        serializer = garnbarn_serializer.UpdateAssignmentApiSerializer(
            instance=self.get_object(), data=data, partial=True)
        if not serializer.is_valid():
            # Response 400 if the request body is invalid
            return Response({
                'message': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        self.perform_update(serializer)
        return Response(self.get_object().get_json_data(), status=status.HTTP_200_OK)


class TagViewset(viewsets.ModelViewSet):
    serializer_class = garnbarn_serializer.CreateTagApiSerializer
    queryset = Tag.objects.get_queryset().order_by('id')

    def create(self, request, *args, **kwargs):
        """Create Tag object.

        Returns:
            If the given data contain all
            requirements(tag id and name are included),
            return tag's object in json.
            Else, return bad request status
        """
        data = request.data
        serializer = garnbarn_serializer.CreateTagApiSerializer(data=data)

        if not serializer.is_valid():
            """Response 400 if the request body is invalid"""
            return Response({
                'message': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        tag_object = Tag(**serializer.validated_data)
        tag_object.save()
        return Response(tag_object.get_json_data(), status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """Remove tag with specified id.

        Returns:
            Response message telling which tag has been deleted.
        """
        tag = self.get_object()
        tag.delete()

        return Response({}, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        """Update data of the specified tag

        Returns:
            Tag's object in json.
        """
        data = request.data
        serializer = garnbarn_serializer.UpdateTagApiSerializer(
            instance=self.get_object(), data=data, partial=True)

        if not serializer.is_valid():
            """Response 400 if the request body is invaild."""
            return Response({
                'message': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        self.perform_update(serializer)
        return Response(self.get_object().get_json_data(), status=status.HTTP_200_OK)
