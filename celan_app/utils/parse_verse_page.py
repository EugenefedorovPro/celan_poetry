import json
from typing import TypedDict

from django.db.models import QuerySet
import ipdb

from celan_app.models import Verse


class VersePage(TypedDict):
    title: str
    page: int


PATH = "pdf_files/celan_verses_pages.json"


class ParseVersePage:

    def fetch_from_pdf(self) -> list[VersePage]:
        with open(PATH, "r") as f:
            data = json.loads(f.read())

        return data

    def find_dupes_in_verse_titles(self) -> list[str]:
        verse_titles: Queryset[str] = Verse.objects.values_list("title", flat=True)
        dupes = []
        uniques = []
        for title in verse_titles:
            if title in uniques:
                dupes.append(title)
            else:
                uniques.append(title)
        return dupes

    def write_singles_to_db(self):
        verse_page = self.fetch_from_pdf()
        dupes = self.find_dupes_in_verse_titles()
        for item in verse_page:
            # exclude duplicated titles of verses
            if item["title"] not in dupes:
                verse = Verse.objects.filter(title=item["title"]).first()
                if not verse:
                    continue
                verse.page = item["page"]
                verse.save()

    def find_pages_of_dupes(self) -> dict[str, list[int]]:
        verse_page: list[VersePage] = self.fetch_from_pdf()
        dupes = self.find_dupes_in_verse_titles()
        page = {}
        for dupe in dupes:
            for item in verse_page:
                if item["title"] == dupe:
                    page.setdefault(dupe, set()).add(item["page"])
        return page

        # {'Die Ewigkeit': [20, 195, 278, 20, 195, 278],
        #  'Die Welt': [69, 296],
        #  'Einmal': [170, 219],
        #  'Heimkehr': [55, 346],
        #  'Herbst': [310, 359],
        #  'Ich weiß': [40, 325],
        #  'Komm': [196, 291],
        #  'Landschaft': [23, 147, 346, 23, 147, 346],
        #  'Wandlung': [321, 362]}

        # [{'title': 'Ein Lied in der Wüste', 'page': 3}, 
        # {'title': 'Nachts ist dein Leib', 'page': 3}]

    def write_dupes_to_db(self) -> list[int]:
        verse_page = self.fetch_from_pdf()
        title_pages = self.find_pages_of_dupes()
        changed_verses_pk = []
        for title, pages in title_pages.items():
            verses = Verse.objects.filter(title = title)
            if len(pages) != len(verses):
                raise ValueError("len(pages) != len(verses)")
            for page, verse in zip(pages, verses):
                verse.page = page
                verse.save()
                changed_verses_pk.append(verse.pk)
        return changed_verses_pk

    def parse_verse_page(self):
        self.write_singles_to_db()
        self.write_dupes_to_db()
