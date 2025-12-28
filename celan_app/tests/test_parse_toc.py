import ipdb
from django.test import TestCase
from celan_app.utils.parse_toc import ParseToc
from celan_app.models import Collection, Verse

class TestParseToc(TestCase):

    def test_success(self):
        ParseToc().parse_toc()
        ipdb.set_trace()
