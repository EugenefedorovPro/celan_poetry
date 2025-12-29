import pprint

from django.test import TestCase
import ipdb

from celan_app.models import Verse
from celan_app.utils.parse_toc import ParseToc
from celan_app.utils.parse_verse_page import ParseVersePage


class TestVersePage(TestCase):

    def setUp(self) -> None:
        ParseToc().parse_toc()

    def test_dupes(self):
        verse_page = ParseVersePage()
        dupes_titles = verse_page.find_dupes_in_verse_titles()
        pprint.pprint(dupes_titles)

    def test_write_to_db(self):
        verse_page = ParseVersePage()
        verse_page.write_singles_to_db()
        pages = [item for item in Verse.objects.values_list("page", flat=True)]
        print(pages)
        ipdb.set_trace()

    def test_find_pages_of_dupes(self):
        verse_page = ParseVersePage()
        pages = verse_page.find_pages_of_dupes()
        pprint.pprint(pages)

    def test_write_dupes(self):
        verse_page = ParseVersePage()
        verses_pks = verse_page.write_dupes_to_db()
        titles_pages = list(
            Verse.objects.filter(pk__in=verses_pks).values_list("title", "page")
        )
        pprint.pprint(titles_pages)
        pages = list(
            Verse.objects.filter(pk__in=verses_pks).values_list("page", flat=True)
        )
        self.assertFalse(0 in pages)

    def test_parse_verse_page(self):
        verse_page = ParseVersePage()
        verse_page.parse_verse_page()
        ipdb.set_trace()

