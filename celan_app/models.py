# celan_app/models.py

from django.db import models
from django.db.models import PROTECT, Q

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

    name = models.CharField(max_length=255, blank=True, default="")
    genre = models.CharField(max_length=255, blank=True, default="")
    is_real_celan_collection = models.CharField(max_length=255, blank=True, default="")
    year_publication = models.PositiveIntegerField(null=True, blank=True)
    number_verses = models.PositiveBigIntegerField(default=0)
    notes = models.TextField(blank=True, default="")  # canonical/original notes

    def __str__(self) -> str:
        name = self.name or "no name"
        year = self.year_publication if self.year_publication is not None else "no year"
        return f"{name} - {year}"


class CollectionTranslation(models.Model):
    """
    Multiple translations per language are allowed.
    Use is_preferred=True to mark one preferred translation per (collection, lang).
    """

    LANG_CHOICES = [
        ("ru", "Russian"),
        ("uk", "Ukrainian"),
        ("en", "English"),
    ]

    collection = models.ForeignKey(
        Collection,
        on_delete=models.PROTECT,
        related_name="translations",
    )
    lang = models.CharField(max_length=8, choices=LANG_CHOICES)

    # Translated content
    name = models.CharField(max_length=255, blank=True, default="")
    notes = models.TextField(blank=True, default="")

    is_preferred = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["collection", "lang"]),
            models.Index(fields=["collection", "lang", "is_preferred"]),
        ]
        constraints = [
            # Prevent exact duplicate variants by metadata (optional but useful)
            models.UniqueConstraint(
                fields=["collection", "lang"],
                name="uniq_collection_lang",
            ),
            # At most one preferred translation per collection+lang
            models.UniqueConstraint(
                fields=["collection", "lang"],
                condition=Q(is_preferred=True),
                name="uniq_preferred_collection_per_lang",
            ),
        ]

    def __str__(self) -> str:
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

        notes_preview = (nt[:40] + "…") if len(nt) > 40 else nt
        return f"{self.get_lang_display()} – {nm} / {notes_preview}"


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

    title = models.CharField(max_length=255, blank=True, default="")
    text = models.TextField(blank=True, default="")
    page = models.PositiveIntegerField(default=0)

    lemmas = models.JSONField(default=dict, blank=True)
    forms_by_lemma = models.JSONField(default=dict, blank=True)


    year_publication = models.PositiveIntegerField(default=0)
    year_writing = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return self.title or (self.text[:15] if self.text else "Verse")


class VerseTranslation(models.Model):
    """
    Multiple translations per language are allowed.
    Use is_preferred=True to mark one preferred translation per (verse, lang).
    """

    LANG_CHOICES = [
        ("ru", "Russian"),
        ("uk", "Ukrainian"),
        ("en", "English"),
    ]

    verse = models.ForeignKey(
        Verse,
        on_delete=models.PROTECT,
        related_name="verse_translations",
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

    def __str__(self) -> str:
        if self.lang == "ru":
            ttl = self.title or NO_NAME_RUS
            txt = self.text or NO_NOTES_RUS
        elif self.lang == "uk":
            ttl = self.title or NO_NAME_UKR
            txt = self.text or NO_NOTES_UKR
        elif self.lang == "en":
            ttl = self.title or NO_NAME_ENG
            txt = self.text or NO_NOTES_ENG
        else:
            ttl = self.title or "no title"
            txt = self.text or "no text"

        who = self.translator or self.source or "unknown"
        txt_preview = (txt[:40] + "…") if len(txt) > 40 else txt
        return f"{self.get_lang_display()} – {who} – {ttl} / {txt_preview}"


# ------------------------------- Word / VerseWord -------------------------------------------------


class Word(models.Model):
    lemma = models.CharField(max_length=255, default="")
    # freq of lemma across all verses in db (global freq)
    freq = models.PositiveIntegerField(default=0)
    neologism = models.BooleanField(default=False)

    # IMPORTANT: explicit through model so we can store per-verse frequency.
    # We bind through="VerseWord", which maps to existing table celan_app_verseword.
    verse = models.ManyToManyField(
        Verse,
        through="VerseWord",
        related_name="words",
        blank=True,
    )

    forms = models.JSONField(default=dict, blank=True)
    quotes = models.JSONField(default=dict, blank=True)

    def __str__(self) -> str:
        return f"{self.lemma}: {self.freq}"


class VerseWord(models.Model):
    """
    Join table between Verse and Word with per-verse word frequency.

    IMPORTANT:
    Your DB already has the table named 'celan_app_verseword', so we pin it using db_table
    to avoid Django expecting 'celan_app_wordverse'.
    """

    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    verse = models.ForeignKey(Verse, on_delete=models.CASCADE)

    freq = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "celan_app_verseword"
        constraints = [
            models.UniqueConstraint(fields=["verse", "word"], name="uniq_word_per_verse"),
        ]
        indexes = [
            models.Index(fields=["verse", "word"]),
            models.Index(fields=["word", "verse"]),
        ]

    def __str__(self) -> str:
        return f"{self.word.lemma} in verse {self.verse_id}: {self.freq}"


class WordTranslation(models.Model):
    LANG_CHOICES = [
        ("ru", "Russian"),
        ("uk", "Ukrainian"),
        ("en", "English"),
    ]

    word = models.ForeignKey(Word, on_delete=PROTECT, related_name="word_translations")
    lang = models.CharField(max_length=8, choices=LANG_CHOICES)

    trans = models.TextField(default="", blank=True)

    is_preferred = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["word", "lang"]),
            models.Index(fields=["lang", "trans"]),
            models.Index(fields=["word", "lang", "is_preferred"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["word", "lang"],
                condition=Q(is_preferred=True),
                name="uniq_preferred_word_translation_per_lang",
            ),
        ]

    def __str__(self) -> str:
        return self.trans or "no translation"
