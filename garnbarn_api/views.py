from functools import partial
from django.db.models.query import QuerySet
from rest_framework.decorators import action, authentication_classes
from rest_framework.response import Response
from rest_framework import serializers, viewsets, status
from rest_framework import viewsets, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from garnbarn_api.serializer import AssignmentSerializer, CustomUserSerializer, TagSerializer
from .authentication import FirebaseAuthIDTokenAuthentication

from datetime import datetime, date
from .models import Assignment, CustomUser, Tag


# class PermissionsPerMethodMixin(object):
#     def get_permissions(self):
#         """
#         Allows overriding default permissions with @permission_classes
#         """
#         view = getattr(self, self.action)
#         if hasattr(view, 'permission_classes'):
#             print('_____________')
#             return [permission_class() for permission_class in view.permission_classes]
#         return super().get_permissions()





class CustomUserViewset(viewsets.ModelViewSet):
#     # permission_classes = [IsAdminUser]
#     permission_classes = [FirebaseAuthIDTokenAuthentication]
#     serializer_class = CustomUserSerializer

    def get_queryset(self):
        user = CustomUser.objects.all()
        return user

#     @action(detail=False, methods=['POST'])
#     @permission_classes((AllowAny,))
#     def create_user(self, request, *args, **kwargs):
#         """Create User object"""
#         # firebase_auth = FirebaseAuthIDTokenAuthentication()
#         # user = firebase_auth.authenticate_credentials(request)
#         # print(user)
#         # print(request.data)
#         # serializer = CustomUserSerializer(data=request.data)
#         # decoded_token = auth.verify_id_token(key)
#         # permission_classes = [IsAuthenticated]

#         if not serializer.is_valid():
#             # Response 400 if the request body is invalid.
#             return Response({
#                 'message': serializer.errors
#             }, status=status.HTTP_400_BAD_REQUEST)

#         self.perform_create(serializer)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def destroy(self, request, *args, **kwargs):
#         """ Remove user with specified user id.

#         Returns:
#             {} with 200 status code.
#         """
#         user = self.get_object()
#         user.delete()
#         return Response({}, status=status.HTTP_200_OK)

#     def partial_update(self, request, *args, **kwargs):
#         """ Update data of a specified user

#         Returns:
#             User's object in json.
#         """
#         serializer = CustomUser(
#             isinstance=self.get_object(), data=request.data, partial=True)
#         if not serializer.is_valid():
#             return Response({
#                 'message': serializer.errors
#             }, status=status.HTTP_400_BAD_REQUEST)

#         self.perform_update(serializer)
#         return Response(self.get_object().get_json_data(), status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True)
    def get_user_api(self, request, *args, **kwarg):
        pass

    @action(methods=['get'], detail=True)
    def get_link(self, request, *args, **kwarg):
        pass

    @action(methods=['patch'], detail=True)
    def un_link(self, access_token):
        pass

    @action(methods=['get'], detail=True,
        url_path='account', url_name='account')
    def verify_line_access_token(self, access_token):
        pass


class AssignmentViewset(viewsets.ModelViewSet):
    authentication_classes = [FirebaseAuthIDTokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = AssignmentSerializer

    def get_queryset(self):
        if self.request.query_params.get('fromPresent') == "true":
            assignment = Assignment.objects.exclude(
                due_date__lt=date.today())
            assignment = assignment.exclude(due_date=None).order_by('due_date')
        else:
            assignment = Assignment.objects.get_queryset().order_by('id')
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
        serializer.save()

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
        tag = Tag.objects.get_queryset().order_by('id')
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
        serializer.save()

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
        serializer = TagSerializer(
            instance=self.get_object(), data=data, partial=True)

        if not serializer.is_valid():
            """Response 400 if the request body is invaild."""
            return Response({
                'message': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        self.perform_update(serializer)
        return Response(self.get_object().get_json_data(), status=status.HTTP_200_OK)
