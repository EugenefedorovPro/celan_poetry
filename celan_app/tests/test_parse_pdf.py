from django.test import TestCase
import ipdb

from celan_app.utils.parse_pdf import ParsePdf
from celan_app.utils.parse_toc import ParseToc


class TestParsePdf(TestCase):

    def setUp(self):
        ParseToc().parse_toc()

    def test_success(self):
        parse = ParsePdf()
        verses_names = parse.fetch_verses_names()
        ipdb.set_trace()
