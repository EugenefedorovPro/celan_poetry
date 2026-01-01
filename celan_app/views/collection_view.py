from rest_framework.views import APIView
from rest_framework import generics
from celan_app.models import Collection
from celan_app.serializers.collection_serializer import CollectionSerializer



class CollectionView(generics.ListAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

