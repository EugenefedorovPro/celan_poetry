import ipdb
import json
from celan_app.models import Verse

PATH = "pdf_files/corrections/celan_ai.json"


class FormatVerses:

    def format_verses(self) -> dict:
        with open(PATH, "r") as f:
            formated = json.loads(f.read())
        return formated

    def update_text(self):
        formated: dict = self.format_verses()
        lost_ids: list[int] = []
        for item in formated:
            item_page = item["page"]
            item_title = item["title"]
            verse = Verse.objects.filter(title=item_title, page=item_page).first()
            if not verse:
                lost_ids.append(item["id"])
                continue
            verse.text = item["text"]
            verse.save()
        print(f"number of lost_ids = {len(lost_ids)}")

    def update_dates(self):
        formated: dict = self.format_verses()
        lost_ids: list[int] = []
        for item in formated:
            item_page = item["page"]
            item_title = item["title"]
            verse = Verse.objects.filter(title=item_title, page=item_page).first()
            if not verse:
                lost_ids.append(item["id"])
                continue
            year_publication = item.get("year_publication") or 0
            year_writing = item.get("year_writing") or 0
            verse.year_writing = int(year_writing)
            verse.year_publication = int(year_publication)
            verse.save()
        print(f"number of lost_ids = {len(lost_ids)}")

    def update_text_rus(self):
        formated: dict = self.format_verses()
        lost_ids: list[int] = []
        for item in formated:
            item_page = item["page"]
            item_title = item["title"]
            verse = Verse.objects.filter(title=item_title, page=item_page).first()
            if not verse:
                lost_ids.append(item["id"])
                continue
            verse.text_rus = item.get("text_rus") or ""
            verse.save()
        print(f"number of lost_ids = {len(lost_ids)}")
