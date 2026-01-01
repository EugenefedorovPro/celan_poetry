from rest_framework.serializers import ModelSerializer
from celan_app.models import Verse


class TocVerseSerializer(ModelSerializer):
    class Meta:
        model = Verse
        fields = ("id", "title")
