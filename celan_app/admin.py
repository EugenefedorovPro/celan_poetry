# celan_app/admin.py

from django.contrib import admin
from django.db import models
from django.forms import Textarea
from django.utils.html import format_html
from celan_app.models import Collection, CollectionTranslation, Verse, VerseTranslation


# ------------------------------- Shared widgets ---------------------------------------------------

WIDGET_TEXTAREA_BIG = Textarea(attrs={"rows": 18, "cols": 120})
WIDGET_TEXTAREA_MED = Textarea(attrs={"rows": 12, "cols": 120})
WIDGET_TEXTAREA_VERSE = Textarea(attrs={"rows": 24, "cols": 120})


# ------------------------------- Inlines ----------------------------------------------------------


class CollectionTranslationInline(admin.TabularInline):
    model = CollectionTranslation
    extra = 0
    fields = ("lang", "name", "translator", "source", "year", "is_preferred", "notes")
    ordering = ("lang", "-is_preferred", "translator", "source")

    # lets you see/edit full notes in the inline
    formfield_overrides = {
        models.TextField: {"widget": WIDGET_TEXTAREA_MED},
    }


class VerseTranslationInline(admin.StackedInline):
    """
    StackedInline is much better for long translation texts.
    """

    model = VerseTranslation
    extra = 0
    fields = ("lang", "title", "translator", "source", "year", "is_preferred", "text")
    ordering = ("lang", "-is_preferred", "translator", "source")

    # THIS is the main fix: full translation text is visible/editable
    formfield_overrides = {
        models.TextField: {"widget": WIDGET_TEXTAREA_BIG},
    }


# ------------------------------- Collection Admin -------------------------------------------------


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "year_publication",
        "genre",
        "is_real_celan_collection",
        "number_verses",
        "notes_preview",
        "preferred_ru_name",
    )
    ordering = ("year_publication", "name")
    search_fields = ("name", "notes")
    inlines = [CollectionTranslationInline]

    # full-size textarea for Collection.notes on the change form
    formfield_overrides = {
        models.TextField: {"widget": WIDGET_TEXTAREA_BIG},
    }

    @admin.display(description="Notes")
    def notes_preview(self, obj: Collection):
        return format_html(
            '<div style="white-space: pre-wrap; max-width: 700px;">{}</div>',
            (obj.notes or "")[:300],
        )

    @admin.display(description="Name (RU preferred)")
    def preferred_ru_name(self, obj: Collection):
        tr = (
            obj.translations.filter(lang="ru", is_preferred=True).first()
            or obj.translations.filter(lang="ru").first()
        )
        return (tr.name or "") if tr else ""


# ------------------------------- Verse Admin ------------------------------------------------------


# assuming these already exist in your file:
# from .models import Verse, VerseTranslation
# from .admin_inlines import VerseTranslationInline
# WIDGET_TEXTAREA_VERSE = ...


@admin.register(Verse)
class VerseAdmin(admin.ModelAdmin):
    list_display = (
        "collection",
        "title",
        "page",
        "text_preview",
        "preferred_ru_text_preview",
        "lemmas_preview",
        "neologisms_preview",
    )
    ordering = ("collection", "title")
    search_fields = ("title", "text")
    inlines = [VerseTranslationInline]

    # full-size textarea for Verse.text on the change form
    formfield_overrides = {
        models.TextField: {"widget": WIDGET_TEXTAREA_VERSE},
    }

    @admin.display(description="Text")
    def text_preview(self, obj: "Verse"):
        return format_html(
            '<div style="white-space: pre-wrap; max-width: 700px;">{}</div>',
            (obj.text or "")[:400],
        )

    @admin.display(description="Text (RU preferred)")
    def preferred_ru_text_preview(self, obj: "Verse"):
        tr = (
            obj.translations.filter(lang="ru", is_preferred=True).first()
            or obj.translations.filter(lang="ru").first()
        )
        if not tr:
            return ""
        return format_html(
            '<div style="white-space: pre-wrap; max-width: 700px;">{}</div>',
            (tr.text or "")[:400],
        )

    @admin.display(description="Lemmas")
    def lemmas_preview(self, obj: "Verse"):
        """
        Keep it short:
        - if dict: show number of keys + a few sample keys
        - if list: show length + first items
        """
        data = obj.lemmas or {}
        if isinstance(data, dict):
            keys = list(data.keys())
            sample = ", ".join(map(str, keys[:8]))
            suffix = "…" if len(keys) > 8 else ""
            return f"{len(keys)} keys: {sample}{suffix}" if keys else ""
        if isinstance(data, list):
            sample = ", ".join(map(str, data[:8]))
            suffix = "…" if len(data) > 8 else ""
            return f"{len(data)} items: {sample}{suffix}" if data else ""
        return str(data)[:120]

    @admin.display(description="Neologisms")
    def neologisms_preview(self, obj: "Verse"):
        data = obj.neologisms or {}
        if isinstance(data, dict):
            keys = list(data.keys())
            sample = ", ".join(map(str, keys[:8]))
            suffix = "…" if len(keys) > 8 else ""
            return f"{len(keys)} keys: {sample}{suffix}" if keys else ""
        if isinstance(data, list):
            sample = ", ".join(map(str, data[:8]))
            suffix = "…" if len(data) > 8 else ""
            return f"{len(data)} items: {sample}{suffix}" if data else ""
        return str(data)[:120]

    def get_search_results(self, request, queryset, search_term):
        """
        Extends admin search to include translations:
        - VerseTranslation.title
        - VerseTranslation.text
        - VerseTranslation.translator/source
        """
        queryset, use_distinct = super().get_search_results(
            request, queryset, search_term
        )

        if search_term:
            qs_trans = Verse.objects.filter(
                models.Q(translations__title__icontains=search_term)
                | models.Q(translations__text__icontains=search_term)
                | models.Q(translations__translator__icontains=search_term)
                | models.Q(translations__source__icontains=search_term)
            )
            queryset = (queryset | qs_trans).distinct()
            use_distinct = True

        return queryset, use_distinct
