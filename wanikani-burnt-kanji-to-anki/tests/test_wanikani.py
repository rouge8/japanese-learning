import faker
import pytest

from wanikani_burnt_kanji_to_anki.wanikani import _KANJI
from wanikani_burnt_kanji_to_anki.wanikani import Kanji
from wanikani_burnt_kanji_to_anki.wanikani import UnknownKanjiError
from wanikani_burnt_kanji_to_anki.wanikani import WaniKaniAPIClient

from .factories import KanjiFactory
from .mock_wanikani import KanjiPage
from .mock_wanikani import MockWaniKaniAPI


class TestWaniKaniAPIClient:
    def test_load_kanji(
        self,
        api_client: WaniKaniAPIClient,
        faker: faker.Faker,
        mock_wanikani: MockWaniKaniAPI,
    ) -> None:
        assert not _KANJI, "Kanji cache has already been populated!"

        kanji = [
            {
                "id": faker.random_int(),
                "object": "kanji",
                "data": {
                    "document_url": faker.url(),
                    "characters": faker.pystr(),
                    "meanings": [
                        {
                            "meaning": faker.word(),
                            "primary": faker.pybool(),
                            "accepted_answer": faker.pybool(),
                        }
                        for _ in range(faker.random_int(min=1, max=3))
                    ],
                    "readings": [
                        {
                            "type": faker.word(),
                            "primary": faker.pybool(),
                            "reading": faker.pystr(),
                            "accepted_answer": faker.pybool(),
                        }
                        for _ in range(faker.random_int(min=1, max=5))
                    ],
                },
            }
            for _ in range(faker.random_int(min=3, max=10))
        ]
        expected_kanji = {
            k["id"]: Kanji(
                id=k["id"],
                document_url=k["data"]["document_url"],
                characters=k["data"]["characters"],
                meanings=[
                    meaning["meaning"]
                    for meaning in k["data"]["meanings"]
                    if meaning["accepted_answer"]
                ],
                readings=[
                    reading["reading"]
                    for reading in k["data"]["readings"]
                    if reading["primary"] or reading["accepted_answer"]
                ],
            )
            for k in kanji
        }

        mock_wanikani.add_kanji_page(KanjiPage(None, "12345", [kanji[0]]))
        mock_wanikani.add_kanji_page(KanjiPage("12345", None, kanji[1:]))

        api_client.load_kanji()
        assert _KANJI == expected_kanji

    def test_burnt_kanji(
        self,
        api_client: WaniKaniAPIClient,
        faker: faker.Faker,
        mock_wanikani: MockWaniKaniAPI,
    ) -> None:
        expected_kanji = KanjiFactory.create_batch(faker.random_int(min=3, max=10))

        assignments = [
            {
                "id": faker.random_int(),
                "object": "assignment",
                "data": {"subject_id": kanji.id},
            }
            for kanji in expected_kanji
        ]

        mock_wanikani.add_assignments(assignments)

        assert list(api_client.burnt_kanji()) == expected_kanji

    def test_get_kanji(self, api_client: WaniKaniAPIClient) -> None:
        random_kanji = KanjiFactory.create_batch(5)

        for kanji in random_kanji:
            assert api_client.get_kanji(kanji.characters) == kanji

    def test_get_kanji_unknown_kanji(self, api_client: WaniKaniAPIClient) -> None:
        random_kanji = KanjiFactory.create()

        with pytest.raises(UnknownKanjiError):
            api_client.get_kanji(random_kanji.characters + "OHNO")
