from django.conf.urls import url
from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter
from garnbarn_api.views import AssignmentViewset, CustomUserViewset, TagViewset

router = DefaultRouter()
router.register('assignment', AssignmentViewset, basename='assignment')
router.register('tag', TagViewset, basename='tag')
router.register('account', CustomUserViewset, basename='account')

urlpatterns = [
    url('', include(router.urls))
]
