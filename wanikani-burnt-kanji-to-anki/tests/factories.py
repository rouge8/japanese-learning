from collections.abc import Callable
from typing import ClassVar

from polyfactory import SyncPersistenceProtocol, Use
from polyfactory.factories.attrs_factory import AttrsFactory

from wanikani_burnt_kanji_to_anki.wanikani import _KANJI, Kanji


def make_sequence(start: int = 1) -> Callable[[], int]:
    count = start

    def next_val() -> int:
        nonlocal count
        val = count
        count += 1
        return val

    return next_val


id_sequence = make_sequence(1)
character_sequence = make_sequence(1)


class KanjiPersistenceHandler(SyncPersistenceProtocol[Kanji]):
    def save(self, data: Kanji) -> Kanji:
        _KANJI[data.id] = data
        return data

    def save_many(self, data: list[Kanji]) -> list[Kanji]:
        for d in data:
            _KANJI[d.id] = d
        return data


class KanjiFactory(AttrsFactory[Kanji]):
    __sync_persistence__ = KanjiPersistenceHandler

    id = Use(id_sequence)
    document_url = AttrsFactory.__faker__.url
    characters = Use(lambda: str(character_sequence()))
    meanings: ClassVar[list[str]] = [
        "meaning1",
        "meaning2",
    ]
    readings: ClassVar[list[str]] = [
        "readings1",
        "readings2",
    ]
