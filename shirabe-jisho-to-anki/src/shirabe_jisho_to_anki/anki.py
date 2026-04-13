import re
from typing import Self

from anki.collection import Collection
from anki.decks import DeckId
from attrs import define
from attrs import field
from attrs import frozen

from .helpers import not_none
from .jmdict import Entry as JMDictEntry


@define
class Deck:
    """An Anki deck."""

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
        return cls(deck["id"], name, notes)

    def has_card(self, card: Card) -> bool:
        """
        Whether a card already exists in a deck, as defined by the card's
        search terms.
        """
        return any(
            re.search(rf"\b{term}\b", note)
            for term in card.search_terms()
            for note in self.notes
        )


@frozen(kw_only=True)
class Card:
    """An Anki card."""

    _entry: JMDictEntry = field(alias="entry")
    front: str
    back: str

    def search_terms(self) -> set[str]:
        """Search terms to use when matching existing cards."""
        masu_forms = self._entry.masu_forms() or set()
        # Note that we don't use the kana readings because they will match many
        # more unrelated cards. For example:
        #
        # 揚げる / あげる
        #
        # would also match:
        #
        # 挙げる / あげる
        #
        # and:
        #
        # 上げる / あげる
        return set(self._entry.kanji_readings) | masu_forms

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

        return cls(entry=entry, front=front, back="\n".join(back_lines))
