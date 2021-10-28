from django.contrib import admin
from rest_framework.decorators import api_view
from .models import Assignment, CustomUser, Tag


admin.site.register(Assignment)
admin.site.register(Tag)
admin.site.register(CustomUser)
