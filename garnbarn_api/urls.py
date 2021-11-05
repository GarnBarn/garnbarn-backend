from django.conf.urls import url
from django.urls.conf import include
from rest_framework.routers import DefaultRouter
from .views import AssignmentViewset, TagViewset

router = DefaultRouter()
router.register('assignment', AssignmentViewset, basename='assignment')
router.register('tag', TagViewset, basename='tag')

urlpatterns = [
    url('', include(router.urls))
]
