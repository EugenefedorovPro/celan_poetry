from rest_framework.serializers import ModelSerializer
from celan_app.models import Collection


class CollectionSerializer(ModelSerializer):
    class Meta:
        model = Collection
        fields = (
            "pk",
            "name",
            "genre",
            "is_real_celan_collection",
            "year_publication",
            "number_verses",
            "notes",
        )

