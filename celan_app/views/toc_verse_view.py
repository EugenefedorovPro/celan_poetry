from rest_framework import generics
from celan_app.serializers.toc_verse_serializer import TocVerseSerializer
from celan_app.models import Verse, Collection
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404


class TocVerseView(generics.ListAPIView):
    serializer_class = TocVerseSerializer

    def get_queryset(self) -> QuerySet[Verse]:
        collection = get_object_or_404(Collection, pk=self.kwargs["collection_pk"])
        return Verse.objects.filter(collection=collection).order_by("page", "id")
