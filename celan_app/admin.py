from django.contrib import admin
from django.db import models
from django.forms import Textarea
from django.utils.html import format_html

from celan_app.models import (
    Collection,
    CollectionTranslation,
    Verse,
    VerseTranslation,
)


# ------------------------------- Inlines ----------------------------------------------------------


class CollectionTranslationInline(admin.TabularInline):
    model = CollectionTranslation
    extra = 0
    fields = ("lang", "name", "translator", "source", "year", "is_preferred", "notes")
    ordering = ("lang", "-is_preferred", "translator", "source")


class VerseTranslationInline(admin.TabularInline):
    model = VerseTranslation
    extra = 0
    fields = ("lang", "title", "translator", "source", "year", "is_preferred", "text")
    ordering = ("lang", "-is_preferred", "translator", "source")


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

    formfield_overrides = {
        models.TextField: {"widget": Textarea(attrs={"rows": 18, "cols": 120})},
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
        if not tr:
            return ""
        return tr.name or ""


# ------------------------------- Verse Admin ------------------------------------------------------


@admin.register(Verse)
class VerseAdmin(admin.ModelAdmin):
    list_display = (
        "collection",
        "title",
        "page",
        "text_preview",
        "preferred_ru_text_preview",
    )
    ordering = ("collection", "title")
    search_fields = ("title", "text")

    inlines = [VerseTranslationInline]

    formfield_overrides = {
        models.TextField: {"widget": Textarea(attrs={"rows": 24, "cols": 120})},
    }

    @admin.display(description="Text")
    def text_preview(self, obj: Verse):
        return format_html(
            '<div style="white-space: pre-wrap; max-width: 700px;">{}</div>',
            (obj.text or "")[:400],
        )

    @admin.display(description="Text (RU preferred)")
    def preferred_ru_text_preview(self, obj: Verse):
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

    def get_search_results(self, request, queryset, search_term):
        """
        Extends admin search to include translations:
        - VerseTranslation.title
        - VerseTranslation.text
        - VerseTranslation.translator/source (optional but useful)
        """
        queryset, use_distinct = super().get_search_results(
            request, queryset, search_term
        )

        if search_term:
            qs_trans = (
                Verse.objects.filter(translations__title__icontains=search_term)
                | Verse.objects.filter(translations__text__icontains=search_term)
                | Verse.objects.filter(translations__translator__icontains=search_term)
                | Verse.objects.filter(translations__source__icontains=search_term)
            )

            queryset = (queryset | qs_trans).distinct()
            use_distinct = True

        return queryset, use_distinct
