from django.db.models import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from celan_app.models import Verse, VerseTranslation, Word, WordTranslation


class WordSerializer(serializers.ModelSerializer):

    class Meta:
        model = Word
        fields = (
            "id",
            "lemma",
            "freq",
            "neologism",
        )


class WordTranslationSerializer(serializers.ModelSerializer):
    lang_display = serializers.CharField(source="get_lang_display", read_only=True)
    lemma = serializers.CharField(source="word.lemma", read_only=True)
    word_id = serializers.IntegerField(source="word.id", read_only=True)

    class Meta:
        model = WordTranslation
        fields = (
            "id",
            "lemma",
            "word_id",
            "lang",
            "lang_display",
            "trans",
        )


class VerseTranslationSerializer(serializers.ModelSerializer):
    lang_display = serializers.CharField(source="get_lang_display", read_only=True)

    class Meta:
        model = VerseTranslation
        fields = (
            "id",
            "lang",
            "lang_display",
            "title",
            "text",
            "translator",
            "source",
            "year",
        )


class VerseSerializer(ModelSerializer):
    collection_name = serializers.CharField(
        source="collection.name",
        read_only=True,
    )

    verse_translations = VerseTranslationSerializer(
        many=True,
        read_only=True,
    )

    words = WordSerializer(
        many=True,
        read_only=True,
    )

    word_translations = serializers.SerializerMethodField()

    def get_word_translations(self, verse):
        qs = WordTranslation.objects.filter(word__in=verse.words.all())
        return WordTranslationSerializer(qs, many=True, context=self.context).data

    class Meta:
        model = Verse
        fields = (
            "id",
            "title",
            "text",
            "collection_name",
            "year_writing",
            "year_publication",
            "verse_translations",
            "words",
            "word_translations",
        )
