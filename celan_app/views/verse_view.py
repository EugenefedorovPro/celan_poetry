from rest_framework import generics
from celan_app.serializers.verse_serializer import VerseSerializer
from celan_app.models import Verse


class VerseView(generics.RetrieveAPIView):
    serializer_class = VerseSerializer
    queryset = Verse.objects.all()
    lookup_url_kwarg = "verse_id"

