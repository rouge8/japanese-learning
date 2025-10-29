import re

from anki.collection import Collection
import click


@click.command()
@click.option(
    "--collection",
    "collection_path",
    type=click.Path(exists=True, dir_okay=False),
    required=True,
    help="Path to the Anki collection file",
)
@click.option(
    "--vocab-deck",
    "vocab_deck_name",
    required=True,
    help="Name of the deck containing vocabulary cards",
)
@click.option(
    "--kanji-deck",
    "kanji_deck_name",
    required=True,
    help="Name of the deck containing Kanji cards",
)
def main(collection_path: str, vocab_deck_name: str, kanji_deck_name: str) -> None:
    """
    Find "unknown" kanji in an Anki collection.

    An "unknown" kanji is one that is present in the vocabulary deck but not the
    kanji deck.

    The vocabulary deck is expected to contain the Japanese text in its first
    field and the kanji deck is expected to contain the kanji to study in its
    first field.
    """
    collection = Collection(collection_path)

    vocab_deck = collection.decks.by_name(vocab_deck_name)
    assert vocab_deck is not None

    kanji_deck = collection.decks.by_name(kanji_deck_name)
    assert kanji_deck is not None

    known_kanji = {
        collection.get_card(cid).note().fields[0]
        for cid in collection.decks.cids(kanji_deck["id"])
    }

    new_kanji: set[str] = set()
    for cid in collection.decks.cids(vocab_deck["id"]):
        note_text = collection.get_card(cid).note().fields[0]

        for match in re.finditer(r"[\u4E00-\u9FFF]", note_text):
            found_kanji = match.group()
            if found_kanji not in known_kanji:
                new_kanji.add(found_kanji)

    for nk in sorted(new_kanji):
        print(nk)


if __name__ == "__main__":
    main()
