import re
from typing import Self

from anki.collection import Collection
from anki.decks import DeckId
from attrs import define
from attrs import field

from .helpers import not_none
from .jmdict import Entry as JMDictEntry


@define
class Deck:
    _collection: Collection = field(repr=False)
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
        return cls(collection, deck["id"], name, notes)

    def has_card(self, card: Card) -> bool:
        """
        Whether a card already exists in a deck, as defined by the card's
        search terms.
        """
        return any(
            re.search(rf"\b{term}", note)
            for term in card.search_terms()
            for note in self.notes
        )


@define(kw_only=True)
class Card:
    """An Anki card."""

    _entry: JMDictEntry = field(alias="entry")
    front: str
    back: str

    def search_terms(self) -> set[str]:
        """Search terms to use when matching existing cards."""
        return set(self._entry.kanji_readings) or set(self._entry.kana_readings)

    @classmethod
    def from_jmdict_entry(cls, entry: JMDictEntry) -> Self:
        front = ""
        if entry.kanji_readings:
            front += " / ".join(entry.kanji_readings)
        if front:
            front += " / "
        front += " / ".join(entry.kana_readings)

        back_lines = ["; ".join(sense.meanings) for sense in entry.senses]

        return cls(entry=entry, front=front, back="\n".join(back_lines))
