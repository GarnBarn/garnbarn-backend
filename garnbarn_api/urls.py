from django.conf.urls import url
from django.db.models import base
from django.urls.conf import include
from rest_framework.routers import DefaultRouter
from .views import AssignmentViewset, index

router = DefaultRouter()
router.register('assignment', AssignmentViewset, basename='assignment')

urlpatterns = [
    url("first", index),
    url('', include(router.urls))
]
