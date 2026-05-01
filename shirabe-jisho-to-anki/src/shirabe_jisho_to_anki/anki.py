import re
from typing import Self

from anki.collection import Collection
from anki.decks import DeckId
from anki.models import NotetypeDict
from attrs import define
from attrs import field
from attrs import frozen

from .helpers import not_none
from .jmdict import Entry as JMDictEntry
from .jp_helpers import has_kanji


@define
class Deck:
    """An Anki deck."""

    _collection: Collection
    _model: NotetypeDict
    deck_id: DeckId
    name: str
    notes: set[str]

    @classmethod
    def from_name(cls, collection: Collection, name: str) -> Self:
        deck = not_none(collection.decks.by_name(name))
        deck_id = deck["id"]
        notes = {
            collection.get_card(cid).note().fields[0]
            for cid in collection.decks.cids(deck_id)
        }
        model = not_none(collection.models.by_name("Basic (and reversed card)"))
        return cls(collection, model, deck["id"], name, notes)

    def has_note(self, new_note: Note) -> bool:
        """
        Whether a note already exists in a deck, as defined by the note's
        search terms.
        """
        for note in self.notes:
            if has_kanji(note):
                for term in new_note.kanji_search_terms():
                    if re.search(rf"\b{term}\b", note):
                        return True
            else:
                for term in new_note.kana_search_terms():
                    if re.search(rf"\b{term}\b", note):
                        return True
        return False

    def add_note(self, new_note: Note, tag: str) -> None:
        """Add a new Note to the deck."""
        anki_note = self._collection.new_note(self._model)
        anki_note.fields[0] = new_note.front
        anki_note.fields[1] = new_note.back
        anki_note.add_tag(tag)
        self._collection.add_note(anki_note, self.deck_id)


@frozen(kw_only=True)
class Note:
    """An Anki note."""

    _entry: JMDictEntry = field(alias="entry")
    front: str
    back: str

    def kanji_search_terms(self) -> set[str]:
        """Search terms based on Kanji readings to use when matching existing notes."""
        masu_forms = self._entry.kanji_masu_forms() or set()
        return set(self._entry.kanji_readings) | masu_forms

    def kana_search_terms(self) -> set[str]:
        """
        Search terms based on Kana readings to use when matching existing notes.

        Note that we don't use the Kana readings when Kanji readings exist
        because they will match many more unrelated notes. For example:

        揚げる / あげる

        would also match:

        挙げる / あげる

        and:

        上げる / あげる
        """
        if self._entry.kanji_readings:
            return set()
        masu_forms = self._entry.kana_masu_forms() or set()
        return set(self._entry.kana_readings) | masu_forms

    @classmethod
    def from_jmdict_entry(cls, entry: JMDictEntry) -> Self:
        is_noun_with_suru_verb = entry.is_noun_with_suru_verb()

        def format_reading(reading: str) -> str:
            if is_noun_with_suru_verb:
                return f"{reading}（する）"
            else:
                return reading

        def format_meaning(meaning: str) -> str:
            if is_noun_with_suru_verb:
                return f"{meaning} (n, v)"
            else:
                return meaning

        front = ""
        if entry.kanji_readings:
            front += " / ".join(
                format_reading(reading) for reading in entry.kanji_readings
            )
        if front:
            front += " / "
        front += " / ".join(format_reading(reading) for reading in entry.kana_readings)

        back_lines = [
            "; ".join(format_meaning(meaning) for meaning in sense.meanings)
            for sense in entry.senses
        ]

        return cls(entry=entry, front=front, back="<br>".join(back_lines))
