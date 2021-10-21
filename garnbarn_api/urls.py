from django.conf.urls import url
from django.urls.conf import include
from . import views
from rest_framework.routers import DefaultRouter
from .views import TagViewset

router = DefaultRouter()
router.register('tag', TagViewset, basename='tag')

urlpatterns = [
    url("first", views.index),
    url('', include(router.urls))
]
