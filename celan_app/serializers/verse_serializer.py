from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from celan_app.models import Verse


class VerseSerializer(ModelSerializer):
    collection_name = serializers.CharField(
        source="collection.name",
        read_only=True,
    )

    class Meta:
        model = Verse
        fields = ("id", "title", "text", "collection_name")
