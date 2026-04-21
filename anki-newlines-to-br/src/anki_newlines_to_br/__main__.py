from anki.collection import Collection
import click
from structlog.stdlib import get_logger

from .anki import Deck

logger = get_logger()


@click.command()
@click.option(
    "--anki-collection",
    "anki_collection_path",
    type=click.Path(exists=True, dir_okay=False),
    required=True,
    help="Path to the Anki collection file",
)
@click.option(
    "--anki-deck",
    "anki_deck_name",
    required=True,
    help="Name of the destination Anki deck",
)
@click.option(
    "--dry-run/--no-dry-run",
    default=True,
    help="When True, don't actually update notes",
)
def main(
    *,
    anki_collection_path: str,
    anki_deck_name: str,
    dry_run: bool,
) -> None:
    """Replace newlines with HTML `<br>` tags in note backs."""
    anki_collection = Collection(anki_collection_path)
    anki_deck = Deck.from_name(anki_collection, anki_deck_name)

    for note in anki_deck.notes:
        log = logger.bind(note_id=note.id)
        if "\n" in note.fields[1]:
            if not dry_run:
                log.info("Replacing newlines in note", original_back=note.fields[1])
                anki_deck.replace_newlines(note)
            else:
                log.info(
                    "Would replace newlines in note",
                    back=note.fields[1],
                )
