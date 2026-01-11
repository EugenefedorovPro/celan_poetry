import ipdb
import json
from django.test import TestCase
from django.urls import reverse
from celan_app.views.verse_view import VerseDTO
from rest_framework.response import Response

PATH = "celan_app/tests/views/verse_view_test.json"


class TestVerseView(TestCase):
    fixtures = ["todesfuge.json"]

    def write_test_file(self, path: str, data: dict) -> None:
        with open(path, "w") as f:
            f.write(json.dumps(data))

    def read_test_file(self, path) -> dict:
        with open(path, "r") as f:
            return json.loads(f.read())

    def test_success(self):
        # path("verse/<int:verse_id>/", VerseView.as_view(), name="verse"),
        url = reverse("verse", kwargs={"verse_id": "13377"})
        response: Response = self.client.get(url)
        actual_data: VerseDTO = response.data
        self.assertEqual(response.status_code, 200)

        # self.write_file(PATH, response.data)

        expected_data = self.read_test_file(PATH)
        print("\n")
        print(actual_data.keys())
        self.assertEqual(expected_data, actual_data)
