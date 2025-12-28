import json

import ipdb

from celan_app.models import Collection, Verse


PATH_PDF = "pdf_files/celan_collections_enriched.json"


class ParseToc:

    def get_toc(self):
        with open(PATH_PDF, "r") as f:
            data = json.loads(f.read())
        return data

    def parse_toc(self):
        data = self.get_toc()

        for item in data:
            current_collection = Collection.objects.create(
                name=item["Collection"],
                genre=item["Genre"],
                is_real_celan_collection=item["Real Celan Collection"],
                year_publication=item["Year of publication"],
                number_verses=item["Number of verses in collection"],
                notes=item["Notes"],
            )

            verse_instances = []
            for verse_title in item["Verses"]:
                verse_instances.append(
                    Verse(
                        collection=current_collection,
                        title=verse_title,
                    )
                )

            Verse.objects.bulk_create(verse_instances)

