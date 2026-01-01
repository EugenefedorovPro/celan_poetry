from django.contrib import admin

from celan_app.models import Collection, Verse
from django.db import models
from django.forms import Textarea
from django.utils.html import format_html


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
    list_display = ["collection", "title", "page", "text_preview"]
    ordering = ["collection", "title"]
    search_fields = ["title", "text"]

    # 1) Change form: comfortable textarea (newlines + blank lines are preserved)
    formfield_overrides = {
        models.TextField: {"widget": Textarea(attrs={"rows": 24, "cols": 120})},
    }

    # 2) List view: render newlines (HTML normally collapses them)
    @admin.display(description="Text")
    def text_preview(self, obj):
        return format_html(
            '<div style="white-space: pre-wrap; max-width: 700px;">{}</div>',
            (obj.text or "")[:400],
        )
