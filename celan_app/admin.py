# celan_app/admin.py

from django.contrib import admin
from django.db import models
from django.forms import Textarea
from django.utils.html import format_html

from celan_app.models import (
    Collection,
    CollectionTranslation,
    Verse,
    VerseTranslation,
    Word,
    WordTranslation,
    VerseWord,
)

# ------------------------------- Shared widgets ---------------------------------------------------

WIDGET_TEXTAREA_BIG = Textarea(attrs={"rows": 18, "cols": 120})
WIDGET_TEXTAREA_MED = Textarea(attrs={"rows": 12, "cols": 120})
WIDGET_TEXTAREA_VERSE = Textarea(attrs={"rows": 24, "cols": 120})


# ------------------------------- Inlines ----------------------------------------------------------


class CollectionTranslationInline(admin.TabularInline):
    model = CollectionTranslation
    extra = 0
    fields = ("lang", "name", "is_preferred", "notes")
    ordering = ("lang", "-is_preferred")

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

    formfield_overrides = {
        models.TextField: {"widget": WIDGET_TEXTAREA_BIG},
    }


class WordTranslationInline(admin.TabularInline):
    model = WordTranslation
    extra = 0
    fields = ("lang", "trans", "is_preferred", "created_at")
    readonly_fields = ("created_at",)
    ordering = ("lang", "-is_preferred", "trans")

    formfield_overrides = {
        models.TextField: {"widget": WIDGET_TEXTAREA_MED},
    }


class VerseWordInlineInVerse(admin.TabularInline):
    """
    Edit per-verse word frequencies directly on Verse admin page.
    """

    model = VerseWord
    extra = 0
    fields = ("word", "freq")
    autocomplete_fields = ("word",)
    ordering = ("-freq",)


class VerseWordInlineInWord(admin.TabularInline):
    """
    Edit verse links + per-verse frequency directly on Word admin page.
    """

    model = VerseWord
    extra = 0
    fields = ("verse", "freq")
    autocomplete_fields = ("verse",)
    ordering = ("verse",)


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


@admin.register(Verse)
class VerseAdmin(admin.ModelAdmin):
    list_display = (
        "collection",
        "title",
        "page",
        "text_preview",
        "preferred_ru_text_preview",
        "lemmas_preview",
    )
    ordering = ("collection", "title")
    search_fields = ("title", "text")
    inlines = [VerseTranslationInline, VerseWordInlineInVerse]

    formfield_overrides = {
        models.TextField: {"widget": WIDGET_TEXTAREA_VERSE},
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
            obj.verse_translations.filter(lang="ru", is_preferred=True).first()
            or obj.verse_translations.filter(lang="ru").first()
        )
        if not tr:
            return ""
        return format_html(
            '<div style="white-space: pre-wrap; max-width: 700px;">{}</div>',
            (tr.text or "")[:400],
        )

    @admin.display(description="Lemmas")
    def lemmas_preview(self, obj: Verse):
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

    @admin.display(description="forms_by_lemma")
    def neologisms_preview(self, obj: Verse):
        data = obj.forms_by_lemma or {}
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
        Extend Verse admin search to include VerseTranslation fields.
        """
        queryset, use_distinct = super().get_search_results(
            request, queryset, search_term
        )

        if search_term:
            qs_trans = Verse.objects.filter(
                models.Q(verse_translations__title__icontains=search_term)
                | models.Q(verse_translations__text__icontains=search_term)
                | models.Q(verse_translations__translator__icontains=search_term)
                | models.Q(verse_translations__source__icontains=search_term)
            )
            queryset = (queryset | qs_trans).distinct()
            use_distinct = True

        return queryset, use_distinct


# ------------------------------- Word Admin -------------------------------------------------------

@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ("lemma", "freq", "neologism", "translations_preview")
    ordering = ("lemma",)
    search_fields = ("lemma", "word_translations__trans")
    list_filter = ("neologism",)
    inlines = [WordTranslationInline, VerseWordInlineInWord]

    fieldsets = (
        ("Core", {
            "fields": ("lemma", "freq", "neologism"),
        }),
        ("Linguistic data", {
            "fields": ("forms", "quotes"),
            "classes": ("collapse",),  # optional but useful
        }),
    )

    # Better widget for JSON
    formfield_overrides = {
        models.JSONField: {
            "widget": Textarea(attrs={"rows": 8, "cols": 80}),
        },
    }

    @admin.display(description="Translations")
    def translations_preview(self, obj: Word):
        qs = obj.word_translations.all().order_by(
            "lang", "-is_preferred", "trans"
        )[:6]
        return ", ".join(
            f"{t.lang}:{t.trans}" for t in qs if t.trans
        )


# ------------------------------- Through model admin ---------------------------------------------


@admin.register(VerseWord)
class VerseWordAdmin(admin.ModelAdmin):
    list_display = ("word", "verse", "freq")
    ordering = ("verse", "-freq")
    search_fields = ("word__lemma", "verse__title")
    autocomplete_fields = ("word", "verse")


# ------------------------------- WordTranslation admin -------------------------------------------


@admin.register(WordTranslation)
class WordTranslationAdmin(admin.ModelAdmin):
    list_display = (
        "word",
        "lang",
        "trans",
        "is_preferred",
        "created_at",
    )
    ordering = ("word", "lang", "-is_preferred", "trans")
    search_fields = ("word__lemma", "trans")
    list_filter = ("lang", "is_preferred")
    readonly_fields = ("created_at",)

    formfield_overrides = {
        models.TextField: {"widget": WIDGET_TEXTAREA_MED},
    }
