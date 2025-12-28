import os
import pprint

import ipdb
import pymupdf

from celan_app.models import Verse

PATH_PDF = os.getenv("PATH_PDF")

COLLECTION_FONT_SIZE = 16.020000457763672
VERSE_TITLE_FONT_SIZE = 13.979999542236328
VERSE_LINE_FONT_SIZE = 10.5



class ParsePdf:

    def fetch_verses_names(self) -> list[str]:
        return list(Verse.objects.values_list("title", flat=True))

    def parse_pdf(self):
        doc = pymupdf.open(PATH_PDF)
        collection_titles = []
        verse_titles: list[str] = []
        verse_lines: list[str] = []
        failed_pages: list[str] = []
        for i, page in enumerate(doc):
            if i > 2:
                return
            try:
                blocks = page.get_text("dict")["blocks"]
                print(blocks)
                for block in blocks:
                    for line in block.get("lines", []):
                        for span in line.get("spans", []):
                            if (
                                span.get("font")
                                and span.get("size") == COLLECTION_FONT_SIZE
                            ):
                                collection_titles.append(span.get("text"))
                            if (
                                span.get("font")
                                and span.get("size") == VERSE_TITLE_FONT_SIZE
                            ):
                                verse_titles.append(span.get("text"))
                            if (
                                span.get("font")
                                and span.get("size") == VERSE_LINE_FONT_SIZE
                            ):
                                verse_lines.append(span.get("text"))
            except:
                failed_pages.append(i)
                continue

        pprint.pprint(f"collection_titles = {collection_titles}")
        pprint.pprint(f"verse_titles = {verse_titles}")
        pprint.pprint(f"failed pages = {failed_pages}")
