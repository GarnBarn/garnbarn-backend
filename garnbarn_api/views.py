from django.db.models import query
from django.db.models.query import QuerySet
from django.http import request
from rest_framework.response import Response
from rest_framework import serializers, viewsets, status
from rest_framework import viewsets, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from garnbarn_api.serializer import AssignmentSerializer, CustomUserSerializer, TagSerializer
from .authentication import FirebaseAuthIDTokenAuthentication
from django.db.models import Q

from rest_framework.decorators import action, permission_classes

from datetime import datetime, date
from .models import Assignment, CustomUser, Tag


class AssignmentViewset(viewsets.ModelViewSet):
    authentication_classes = [FirebaseAuthIDTokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = AssignmentSerializer

    def get_queryset(self):
        user_data = self.request.user.uid
        
        if self.request.query_params.get('fromPresent') == "true":
            assignment = Assignment.objects.exclude(
                due_date__lt=date.today())
            assignment = assignment.exclude(due_date=None).order_by('due_date')
        else:
            assignment = Assignment.objects.get_queryset().filter(Q(author=user_data) | Q(tag__subscriber__icontains=user_data)).order_by('id')
        return assignment

    def create(self, request, *args, **kwargs):
        """ Create Assignment object.

        Returns:
            If the given data contain all
            requirements(assignment_name is included and due_date > now)
            , returns assignment's object in json.
            Else, returns bad request status
        """
        serializer = AssignmentSerializer(data=request.data)

        if not serializer.is_valid():
            # Response 400 if the request body is invalid
            return Response({
                'message': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        user_data = self.request.user.uid
        serializer.save(author=CustomUser(uid=user_data))

    def destroy(self, request, *args, **kwargs):
        """ Remove assignment with specified id.

        Returns:
            {} with 200 status code.
        """
        assignment = self.get_object()
        assignment.delete()

        return Response({}, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        """ Update data of a specified assignment

        Returns:
            Assignment's object in json.
        """
        serializer = AssignmentSerializer(
            instance=self.get_object(), data=request.data, partial=True)
        if not serializer.is_valid():
            # Response 400 if the request body is invalid
            return Response({
                'message': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        self.perform_update(serializer)
        return Response(self.get_object().get_json_data(), status=status.HTTP_200_OK)


class TagViewset(viewsets.ModelViewSet):
    authentication_classes = [FirebaseAuthIDTokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TagSerializer

    def get_queryset(self):
        user_data = self.request.user.uid
        tag = Tag.objects.get_queryset().filter(Q(author=user_data) | Q(subscriber__icontains=user_data)).order_by('id')
        return tag

    def create(self, request, *args, **kwargs):
        """Create Tag object.

        Returns:
            If the given data contain all
            requirements(tag id and name are included),
            return tag's object in json.
            Else, return bad request status
        """
        serializer = TagSerializer(data=request.data)

        if not serializer.is_valid():
            """Response 400 if the request body is invalid"""
            return Response({
                'message': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        user_data = self.request.user.uid
        serializer.save(author=CustomUser(uid=user_data))

    def destroy(self, request, *args, **kwargs):
        """Remove tag with specified id.

        Returns:
            {} with 200 status code.
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
        serializer = TagSerializer(
            instance=self.get_object(), data=data, partial=True)

        if not serializer.is_valid():
            """Response 400 if the request body is invaild."""
            return Response({
                'message': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        self.perform_update(serializer)
        return Response(self.get_object().get_json_data(), status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True,
            url_path="subscribe", url_name="subscribe")
    def subscribe(self, request, *args, **kwargs):
        tag = self.get_object()
        if not tag.subscriber:
            tag.subscriber = [request.user.uid]
        elif request.user.uid in tag.subscriber:
            return Response({
                "message": "User has already subscribed to this tag."
            }, status=status.HTTP_400_BAD_REQUEST)
        elif tag.subscriber:
            tag.subscriber.append(request.user.uid)
        tag.save()
        return Response({"message": f"user has subscribed to {tag.name}"}, status.HTTP_200_OK)

    @action(methods=['post', 'delete'], detail=True,
            url_path="unsubscribe", url_name="unsubscribe")
    def unsubscribe(self, request, *args, **kwargs):
        tag = self.get_object()
        if not tag.subscriber or request.user.uid not in tag.subscriber:
            return Response({
                "message": "User has not subscribe to this tag yet."
            }, status=status.HTTP_400_BAD_REQUEST)
        elif request.user.uid in tag.subscriber:
            tag.subscriber.remove(request.user.uid)
            if tag.subscriber == []:
                tag.subscriber = None
            tag.save()
            return Response({"message": f"user has un-subscribed to {tag.name}"}, status.HTTP_200_OK)
