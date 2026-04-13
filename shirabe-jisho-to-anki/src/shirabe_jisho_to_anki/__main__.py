import io

from anki.collection import Collection
import click
from structlog.stdlib import get_logger

from .anki import Deck
from .anki import Note
from .jmdict import EntryNotFound
from .jmdict import JMDict
from .jmdict import MultipleEntriesForBookmark
from .shirabe_jisho import Bookmark

logger = get_logger()


@click.command()
@click.option(
    "--shirabe-jisho-csv",
    type=click.File("r"),
    required=True,
    help="Path to a Shirabe Jisho bookmarks CSV file",
)
@click.option(
    "--jmdict-xml",
    type=click.Path(exists=True, dir_okay=False),
    required=True,
    help="Path to a JMDict English-only XML file",
)
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
@click.option("--anki-tag", required=True, help="Tag to apply to the new notes in Anki")
@click.option(
    "--dry-run/--no-dry-run",
    default=True,
    help="When True, don't actually create new notes",
)
def main(
    *,
    shirabe_jisho_csv: io.TextIOWrapper,
    jmdict_xml: str,
    anki_collection_path: str,
    anki_deck_name: str,
    anki_tag: str,
    dry_run: bool,
) -> None:
    """
    Sync a CSV export from Shirabe Jisho to an Anki deck, checking for existing
    notes.
    """
    anki_collection = Collection(anki_collection_path)
    anki_deck = Deck.from_name(anki_collection, anki_deck_name)

    jmdict = JMDict.from_path(jmdict_xml)

    for bookmark in Bookmark.all_from_csv(shirabe_jisho_csv):
        try:
            jmdict_entry = jmdict.lookup_best(bookmark)
        except EntryNotFound:
            logger.error("Bookmark not found in JMDict", bookmark=bookmark)
            continue
        except MultipleEntriesForBookmark:
            logger.error(
                "Multiple entries found in JMDict that could not be narrowed down",
                bookmark=bookmark,
            )
            continue

        note = Note.from_jmdict_entry(jmdict_entry)
        if anki_deck.has_note(note):
            logger.info("Note for bookmark already exists", bookmark=bookmark)
        else:
            if not dry_run:
                logger.info("Creating note for bookmark", bookmark=bookmark)
                anki_deck.add_note(note, anki_tag)
            else:
                logger.info(
                    "Would create note for bookmark",
                    bookmark=bookmark,
                    front=note.front,
                    back=note.back,
                )
