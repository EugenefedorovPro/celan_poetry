import os
import pprint
import re
import traceback
from typing import NamedTuple
import unicodedata

import ipdb
import pymupdf

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

        import re
        import unicodedata

        # --- regexes ---
        _WS_RE = re.compile(r"[ \t\f\v]+")
        _SPACE_BEFORE_PUNCT_RE = re.compile(r"\s+([,.;:!?])")

        # --- character classes ---
        _INVISIBLES = {
            "\u200b",  # zero-width space
            "\ufeff",  # BOM
            "\u2060",  # word joiner
        }

        _NBSP = {
            "\u00a0",  # no-break space
            "\u202f",  # narrow no-break space
            "\u2007",  # figure space
        }

        # 1) Unicode normalization (composed characters: ü, é, etc.)
        s = unicodedata.normalize("NFC", s)

        # 2) Remove invisible / nuisance characters
        for ch in _INVISIBLES:
            s = s.replace(ch, "")
        s = s.replace("\u00ad", "")  # soft hyphen

        # 3) Normalize NBSP-like spaces
        for ch in _NBSP:
            s = s.replace(ch, " ")

        # 4) Normalize line endings
        s = s.replace("\r\n", "\n").replace("\r", "\n")

        # 5) Trim each line, keep line structure
        s = "\n".join(line.strip() for line in s.split("\n"))

        # 6) Collapse runs of horizontal whitespace
        s = _WS_RE.sub(" ", s)

        # 7) Remove space before punctuation
        s = _SPACE_BEFORE_PUNCT_RE.sub(r"\1", s)

        return s.strip()

    def write_verses_to_db(self, all_poetry: list[Poetry]):
        for poem in all_poetry:
            pass

    def extract_pdf(self):
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
                                    current_poetry: Poetry = Poetry(
                                        current_verse_title, [], i + 1
                                    )
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

    def write_to_db(self) -> list[Poetry]:
        poems = self.extract_pdf()
        lost_poems = []
        for poem in poems:
            # if poem.page == 3:
            #     ipdb.set_trace()
            verse = Verse.objects.filter(title=poem.title, page=poem.page).first()
            if not verse:
                lost_poems.append(poem)
                continue
            verse.text = "\n".join(poem.text)
            verse.save()
        return lost_poems

    def parse_pdf(self):
        self.write_to_db()
