from django.test import TestCase
import ipdb

from celan_app.utils.parse_pdf import ParsePdf
from celan_app.utils.parse_toc import ParseToc
from celan_app.utils.parse_verse_page import ParseVersePage
from celan_app.models import Collection, Verse


class TestParsePdf(TestCase):

    def setUp(self):
        ParseToc().parse_toc()
        ParseVersePage().parse_verse_page()

    def test_extract_pdf(self):
        parse = ParsePdf()
        verses = parse.extract_pdf()

    def test_parse_pdf(self):
        parse = ParsePdf()
        lost_poems = parse.parse_pdf()
        ipdb.set_trace()

