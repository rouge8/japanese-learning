from collections.abc import Sequence
from typing import Self

from anki.collection import Collection
from anki.decks import DeckId
from anki.models import NotetypeDict
from anki.notes import Note
from attrs import define

from .helpers import not_none


@define
class Deck:
    """An Anki deck."""

    _collection: Collection
    _model: NotetypeDict
    deck_id: DeckId
    name: str
    notes: Sequence[Note]

    @classmethod
    def from_name(cls, collection: Collection, name: str) -> Self:
        deck = not_none(collection.decks.by_name(name))
        deck_id = deck["id"]
        notes_by_id = {}
        for cid in collection.decks.cids(deck_id):
            note = collection.get_card(cid).note()
            if not_none(note.id) not in notes_by_id:
                notes_by_id[note.id] = note

        notes = list(notes_by_id.values())
        model = not_none(collection.models.by_name("Basic (and reversed card)"))
        return cls(collection, model, deck["id"], name, notes)

    def replace_newlines(self, note: Note) -> None:
        """Replace newlines with HTML `<br>` elements in the note's reverse side."""
        note.fields[1] = note.fields[1].replace("\n", "<br>")
        self._collection.update_note(note)
