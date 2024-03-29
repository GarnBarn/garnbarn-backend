from functools import partial
from django.db.models import query
from django.db.models.query import QuerySet
from requests.api import request
from rest_framework.decorators import action, authentication_classes
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework import serializers, viewsets, status
from rest_framework import viewsets, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.views import APIView
from garnbarn_api.serializer import AssignmentSerializer, CustomUserSerializer, TagSerializer
from garnbarn_api.authentication import FirebaseAuthIDTokenAuthentication
from rest_framework.decorators import action, permission_classes, api_view
from garnbarn_api.services.line import LineLoginPlatformHelper, LineApiError
import json
import pyotp
from django.db.models import Q

from datetime import datetime, date
from .models import Assignment, CustomUser, Tag


class CustomUserViewset(viewsets.ModelViewSet):
    authentication_classes = [FirebaseAuthIDTokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CustomUserSerializer

    def get_queryset(self):
        uid = self.request.query_params.get('uid', None)
        if uid:
            try:
                user = CustomUser.objects.get(uid=uid)
            except CustomUser.DoesNotExist:
                return None
        else:
            user = CustomUser.objects.get(uid=self.request.user.uid)
        return user

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset is None:
            return Response({"message": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)

    @action(methods=['POST'], detail=False,
            url_path="link", url_name="account-link")
    def link(self, request, *args, **kwarg):
        uid = request.user.uid
        try:
            request_payload = json.loads(request.body)
        except json.JSONDecodeError:
            return Response({
                "message": "The body contain invalid json format."
            }, status=status.HTTP_400_BAD_REQUEST)
        if request_payload.get("platform") != "line":
            return Response({
                "message": "You didn't specify the platform or the platform you specify is not supported."
            }, status=status.HTTP_400_BAD_REQUEST)
        if not request_payload.get("credential"):
            return Response({
                "message": "No credential provided"
            }, status=status.HTTP_400_BAD_REQUEST)

        # Check if user already linked with LINE
        if request.user.line:
            return Response({
                "message": "User already linked the account with LINE"
            }, status=status.HTTP_400_BAD_REQUEST)
        check_list = ["code", "clientId", "redirectUri"]
        for item in check_list:
            if not request_payload["credential"].get(item):
                return Response({
                    "message": f"To link account with LINE, Field `{item}` in credential is required"
                })
        credential = request_payload["credential"]
        line_login = LineLoginPlatformHelper()
        try:
            line_login.verify_login_code(
                credential["code"], credential["redirectUri"], credential["clientId"])
            line_profile = line_login.get_user_profile()
        except LineApiError as e:
            return Response(e.line_error_object, status=status.HTTP_400_BAD_REQUEST)
        request.user.line = line_profile["userId"]
        request.user.save()
        return Response({}, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False,
            url_path='unlink', url_name='unlink')
    def unlink(self, request):
        try:
            request_payload = json.loads(request.body)
        except json.JSONDecodeError:
            return Response({
                "message": "The body contain invalid json format."
            }, status=status.HTTP_400_BAD_REQUEST)
        if request_payload.get("platform") != "line":
            return Response({
                "message": "You didn't specify the platform or the platform you specify is not supported."
            }, status=status.HTTP_400_BAD_REQUEST)
        if not request.user.line:
            return Response({
                "message": "User is not linked the LINE account"
            }, status=status.HTTP_400_BAD_REQUEST)
        request.user.line = None
        request.user.save()
        return Response({}, status=status.HTTP_200_OK)


class AssignmentViewset(viewsets.ModelViewSet):
    authentication_classes = [FirebaseAuthIDTokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = AssignmentSerializer

    def get_queryset(self):
        user_data = self.request.user.uid

        if self.request.query_params.get('fromPresent') == "true":
            assignment = Assignment.objects.get_queryset().filter(
                Q(author=user_data) | Q(tag__subscriber__icontains=user_data) | Q(tag__author=user_data))
            assignment = assignment.exclude(
                due_date__lt=date.today())
            assignment = assignment.exclude(due_date=None).order_by('due_date')
        else:
            assignment = Assignment.objects.get_queryset().filter(
                Q(author=user_data) | Q(tag__subscriber__icontains=user_data) | Q(tag__author=user_data)).order_by('id')
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
        response = Response(serializer.data, status=status.HTTP_201_CREATED)
        location_id = serializer.data.get('id')
        response['Location'] = f"{request.path}" + f"{location_id}"
        return response

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
        tag = Tag.objects.get_queryset().filter(Q(author=user_data) | Q(
            subscriber__icontains=user_data)).order_by('id')
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
        random_secret_key = pyotp.random_base32()
        self.perform_create(serializer, random_secret_key)
        response_data = serializer.data
        response_data["secretKeyTotp"] = random_secret_key
        response = Response(response_data, status=status.HTTP_201_CREATED)
        location_id = serializer.data.get('id')
        response['Location'] = f"{request.path}" + f"{location_id}"
        return response

    def perform_create(self, serializer, secret_key):
        user_data = self.request.user.uid
        serializer.save(author=CustomUser(uid=user_data),
                        secret_key_totp=secret_key)

    def destroy(self, request, *args, **kwargs):
        """Remove tag with specified id.

        Returns:
            {} with 200 status code.
        """
        user_data = self.request.user.uid
        tag = self.get_object()
        if str(tag.author) == str(user_data):
            tag.delete()
            return Response({}, status=status.HTTP_200_OK)
        else:
            return Response({
                'message': "Only Tag's author can delete the tag"
            }, status=status.HTTP_400_BAD_REQUEST)

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
        tag = Tag.objects.get_queryset().get(id=self.kwargs.get('pk'))

        try:
            request_json = json.loads(request.body)
        except json.JSONDecodeError:
            return self.response_bad_request("The invalid json is passed in the body.")
        if not request_json.get("code"):
            return self.response_bad_request("The field `code` is required in the json body.")

        otp_code = request_json["code"]
        if not tag.secret_key_totp or tag.secret_key_totp == "":
            return self.response_bad_request("This Tag doesn't contain the key that required for the verification process. Please re-create the tag.")
        if not pyotp.TOTP(tag.secret_key_totp).verify(otp_code):
            return self.response_bad_request("You enter an incorrect subscribe code.")
        if not tag.author:
            return self.response_bad_request("This Tag doesn't contain the author that required for the verification process. Please re-create the tag.")
        if request.user.uid == tag.author.uid:
            return self.response_bad_request("You can't subscribe to your own tag.")

        if not tag.subscriber:
            tag.subscriber = [request.user.uid]
        elif request.user.uid in tag.subscriber:
            return self.response_bad_request("User has already subscribed to this tag.")
        elif tag.subscriber:
            tag.subscriber.append(request.user.uid)
        tag.save()
        return Response({"message": f"user has subscribed to tag id {tag.id}"}, status.HTTP_200_OK)

    @action(methods=['post', 'delete'], detail=True,
            url_path="unsubscribe", url_name="unsubscribe")
    def unsubscribe(self, request, *args, **kwargs):
        tag = Tag.objects.get_queryset().get(id=self.kwargs.get('pk'))

        if not tag.subscriber or request.user.uid not in tag.subscriber:
            return Response({
                "message": "User has not subscribe to this tag yet."
            }, status=status.HTTP_400_BAD_REQUEST)
        elif request.user.uid in tag.subscriber:
            tag.subscriber.remove(request.user.uid)
            if tag.subscriber == []:
                tag.subscriber = None
            tag.save()
            return Response({"message": f"user has un-subscribed from tag id {tag.id}"}, status.HTTP_200_OK)

    def response_bad_request(self, message):
        return Response({
            "message": message
        }, status=status.HTTP_400_BAD_REQUEST)
