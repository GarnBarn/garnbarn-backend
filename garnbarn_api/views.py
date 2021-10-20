from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import render, get_object_or_404
from django.views import generic

from .models import Assignment, Tag


@api_view()
@permission_classes([AllowAny])
def index(request):
    return Response({"message": "request recieved"})
