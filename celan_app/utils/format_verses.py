import json

PATH = "pdf_files/corrections/celan_corrected_from_pdf.json"


class FormatVerses:

    def format_verses(self):
        with open(PATH, "r") as f:
            formated_text = json.loads(f.read())


