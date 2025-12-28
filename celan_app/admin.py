from django.contrib import admin

from celan_app.models import Collection, Verse


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "genre",
        "is_real_celan_collection",
        "year_publication",
        "number_verses",
        "notes",
    ]
    ordering = ["year_publication", "name"]


@admin.register(Verse)
class VerseAdmin(admin.ModelAdmin):
    list_display = ["collection", "title", "text"]
    ordering = ["collection", "title"]

