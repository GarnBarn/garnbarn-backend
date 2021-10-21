from django.contrib import admin
from rest_framework.decorators import api_view
from .models import Assignment, Tag


admin.site.register(Assignment)
admin.site.register(Tag)
