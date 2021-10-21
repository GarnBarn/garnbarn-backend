from django.db.models import fields
from rest_framework import serializers
from garnbarn_api.models import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['tag_name', 'tag_id']