import pprint

from django.test import TestCase
import ipdb

from celan_app.models import Verse
from celan_app.utils.parse_toc import ParseToc
from celan_app.utils.parse_pdf  import ParsePdf
from celan_app.utils.parse_verse_page import ParseVersePage
from celan_app.utils.format_verses import FormatVerses


class TestFormatVerses(TestCase):

    def setUp(self):
        ParseToc().parse_toc()
        ParseVersePage().parse_verse_page()
        ParsePdf().parse_pdf()
        self.verse_id = 2
        self.test_verse_text = str(Verse.objects.get(pk = self.verse_id).text)

    def test_update_text(self):
        FormatVerses().update_text()

    def test_update_dates(self):
        FormatVerses().update_dates()



