import ipdb
from rest_framework.response import Response
from rest_framework.views import APIView
from celan_app.serializers.verse_serializer import VerseSerializer
from celan_app.models import Verse
from pydantic import BaseModel
from typing import Literal

Lang = Literal["ru", "uk", "en"]


class VerseTranslationDTO(BaseModel):
    id: int
    lang: Lang
    lang_display: str
    title: str
    text: str
    translator: str
    source: str
    year: int | None


class WordDTO(BaseModel):
    id: int
    lemma: str
    freq: int
    neologism: bool


class WordTranslationDTO(BaseModel):
    id: int
    lemma: str
    word_id: int
    lang: Lang
    lang_display: str
    trans: str


class VerseDTO(BaseModel):
    id: int
    title: str
    text: str
    collection_name: str
    year_writing: int
    year_publication: int
    verse_translations: list[VerseTranslationDTO]
    words: list[WordDTO]
    word_translations: list[WordTranslationDTO]


class VerseView(APIView):

    def get(self, request, verse_id: int, *args, **kwargs):
        verse = Verse.objects.get(pk=verse_id)
        serializer = VerseSerializer(verse, context={"request": request})
        data = VerseDTO.model_validate(serializer.data)
        return Response(data.model_dump())
