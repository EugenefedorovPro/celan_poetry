import traceback
import os
import pprint
import re
import unicodedata

import ipdb
import pymupdf

from typing import NamedTuple
from celan_app.models import Verse

PATH_PDF = os.getenv("PATH_PDF")

COLLECTION_FONT_SIZE = 16.020000457763672
VERSE_TITLE_FONT_SIZE = 13.979999542236328
VERSE_LINE_FONT_SIZE = 10.5

class Poetry(NamedTuple):
    title: str
    text: list[str]
    page: int


class ParsePdf:

    def fetch_verses_names(self) -> list[str]:
        return list(Verse.objects.values_list("title", flat=True))

    def norm(self, s: str) -> str:
        if not s:
            return ""
        # normalize composed/decomposed unicode (ü, accents, etc.)
        s = unicodedata.normalize("NFC", s)
        return s.strip()

    def write_verses_to_db(self, all_poetry: list[Poetry]):
        for poem in all_poetry:
            pass

    def parse_pdf(self):
        verses_names = self.fetch_verses_names()
        doc = pymupdf.open(PATH_PDF)
        failed_pages: list[int] = []


        preserved_verse_title: str = ""
        current_poetry: Poetry = Poetry("", [], 0)
        all_poetry: list[Poetry] = []

        for i, page in enumerate(doc):
            try:
                blocks = page.get_text("dict")["blocks"]
                for block in blocks:
                    for line in block.get("lines", []):
                        # print(" - " * 30)
                        # pprint.pprint(line)
                        # print(" - " * 30)
                        for span in line.get("spans", []):
                            # parsing hits one of verse titles
                            current_verse_title = self.norm(span.get("text"))
                            if (
                                span.get("size")
                                and span.get("size") == VERSE_TITLE_FONT_SIZE
                                and current_verse_title in verses_names
                            ):
                                if current_verse_title != preserved_verse_title:
                                    all_poetry.append(current_poetry)
                                    current_poetry: Poetry = Poetry(current_verse_title, [], i)
                                    preserved_verse_title = current_verse_title

                            # parsing hits verse line
                            if (
                                span.get("font")
                                and span.get("size") == VERSE_LINE_FONT_SIZE
                                and self.norm(span.get("text"))
                            ):
                                verse_line = self.norm(span.get("text"))
                                bbox_bottom = span.get("bbox")
                                current_poetry.text.append(verse_line)

            except Exception as e:
                failed_pages.append(i)
                tb = traceback.print_exc(i)
                print(f"page = {i}")
                print(tb)
                continue

        return all_poetry
