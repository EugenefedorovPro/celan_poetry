from django.db import models
from django.db.models import Q

# ------------------------------- Constants --------------------------------------------------------

NO_NAME_RUS = "нет названия на рус"
NO_NAME_UKR = "нема назви укр"
NO_NAME_ENG = "no name in eng"

NO_NOTES_RUS = "нет примечаний на рус"
NO_NOTES_UKR = "нема приміток укр"
NO_NOTES_ENG = "no notes in eng"


# ------------------------------- Collection -------------------------------------------------------


class Collection(models.Model):
    """
    Canonical/original collection data (e.g., German/original edition naming).
    Translations (multiple per language) live in CollectionTranslation.
    """

    name = models.CharField(
        max_length=255, blank=True, default=""
    )  # original name (DE or canonical)
    genre = models.CharField(max_length=255, blank=True, default="")
    is_real_celan_collection = models.CharField(max_length=255, blank=True, default="")
    year_publication = models.PositiveIntegerField(null=True, blank=True)
    number_verses = models.PositiveBigIntegerField(default=0)
    notes = models.TextField(blank=True, default="")  # original notes (canonical)

    def __str__(self):
        name = self.name or "no name"
        year = self.year_publication or "no year"
        return f"{name} - {year}"


class CollectionTranslation(models.Model):
    """
    Multiple translations per language are allowed.
    Use `is_preferred=True` to mark one preferred translation per (collection, lang).
    """

    LANG_CHOICES = [
        ("ru", "Russian"),
        ("uk", "Ukrainian"),
        ("en", "English"),
        # add more without schema changes
    ]

    collection = models.ForeignKey(
        Collection,
        on_delete=models.PROTECT,
        related_name="translations",
    )
    lang = models.CharField(max_length=8, choices=LANG_CHOICES)

    # Variant metadata (helps distinguish multiple translations in the same language)
    translator = models.CharField(max_length=255, blank=True, default="")  # person/team
    source = models.CharField(
        max_length=255, blank=True, default=""
    )  # edition/book/site
    year = models.PositiveIntegerField(null=True, blank=True)

    # Translated content (both can be present; often you want both)
    name = models.CharField(max_length=255, blank=True, default="")
    notes = models.TextField(blank=True, default="")

    # Optional preference flag (only one per collection+lang)
    is_preferred = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["collection", "lang"]),
            models.Index(fields=["lang", "translator"]),
            models.Index(fields=["collection", "lang", "is_preferred"]),
        ]
        # Avoid accidental exact-duplicate variants by metadata.
        constraints = [
            models.UniqueConstraint(
                fields=["collection", "lang", "translator", "source", "year"],
                name="uniq_collection_translation_variant_meta",
            ),
            # PostgreSQL supports partial unique constraints.
            # This enforces: at most one preferred translation per language per collection.
            models.UniqueConstraint(
                fields=["collection", "lang"],
                condition=Q(is_preferred=True),
                name="uniq_preferred_collection_translation_per_lang",
            ),
        ]

    def __str__(self):
        # Pretty fallback messages for admin list views
        if self.lang == "ru":
            nm = self.name or NO_NAME_RUS
            nt = self.notes or NO_NOTES_RUS
        elif self.lang == "uk":
            nm = self.name or NO_NAME_UKR
            nt = self.notes or NO_NOTES_UKR
        elif self.lang == "en":
            nm = self.name or NO_NAME_ENG
            nt = self.notes or NO_NOTES_ENG
        else:
            nm = self.name or "no name"
            nt = self.notes or "no notes"

        who = self.translator or self.source or "unknown"
        # keep it short
        notes_preview = (nt[:40] + "…") if len(nt) > 40 else nt
        return f"{self.get_lang_display()} – {who} – {nm} / {notes_preview}"


# ------------------------------- Verse ------------------------------------------------------------


class Verse(models.Model):
    """
    Canonical/original verse data (e.g., German/original title+text).
    Translations (multiple per language) live in VerseTranslation.
    """

    collection = models.ForeignKey(
        Collection,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="verses",
    )

    title = models.CharField(max_length=255, blank=True, default="")  # original title
    text = models.TextField(blank=True, default="")  # original text
    page = models.PositiveIntegerField(default=0)

    # If you want "unknown" rather than 0, consider null=True/blank=True.
    year_publication = models.PositiveIntegerField(default=0)
    year_writing = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title or (self.text[:15] if self.text else "Verse")


class VerseTranslation(models.Model):
    """
    Multiple translations per language are allowed.
    Use `is_preferred=True` to mark one preferred translation per (verse, lang).
    """

    LANG_CHOICES = [
        ("ru", "Russian"),
        ("uk", "Ukrainian"),
        ("en", "English"),
        # add more without schema changes
    ]

    verse = models.ForeignKey(
        Verse,
        on_delete=models.PROTECT,
        related_name="translations",
    )
    lang = models.CharField(max_length=8, choices=LANG_CHOICES)

    translator = models.CharField(max_length=255, blank=True, default="")
    source = models.CharField(max_length=255, blank=True, default="")
    year = models.PositiveIntegerField(null=True, blank=True)

    title = models.CharField(max_length=255, blank=True, default="")
    text = models.TextField(blank=True, default="")

    is_preferred = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["verse", "lang"]),
            models.Index(fields=["lang", "translator"]),
            models.Index(fields=["verse", "lang", "is_preferred"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["verse", "lang", "translator", "source", "year"],
                name="uniq_verse_translation_variant_meta",
            ),
            models.UniqueConstraint(
                fields=["verse", "lang"],
                condition=Q(is_preferred=True),
                name="uniq_preferred_verse_translation_per_lang",
            ),
        ]

    def __str__(self):
        if self.lang == "ru":
            ttl = self.title or NO_NAME_RUS
            txt = self.text or NO_NAME_RUS
        elif self.lang == "uk":
            ttl = self.title or NO_NAME_UKR
            txt = self.text or NO_NAME_UKR
        elif self.lang == "en":
            ttl = self.title or NO_NAME_ENG
            txt = self.text or NO_NAME_ENG
        else:
            ttl = self.title or "no title"
            txt = self.text or "no text"

        who = self.translator or self.source or "unknown"
        txt_preview = (txt[:40] + "…") if len(txt) > 40 else txt
        return f"{self.get_lang_display()} – {who} – {ttl} / {txt_preview}"
