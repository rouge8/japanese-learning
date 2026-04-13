import csv
import io

import click

from .jmdict import JMDict


@click.command()
@click.option("--shirabe-jisho-csv", type=click.File("r"), required=True)
@click.option(
    "--jmdict-xml", type=click.Path(exists=True, dir_okay=False), required=True
)
def main(shirabe_jisho_csv: io.TextIOWrapper, jmdict_xml: str) -> None:
    """
    Sync a CSV export from Shirabe Jisho to an Anki deck, checking for existing
    cards.
    """
    shirabe_jisho_words = []
    for row in csv.reader(shirabe_jisho_csv):
        if row[0]:
            # The entry has a single Kanji reading
            shirabe_jisho_words.append(row[0])
        else:
            # The entry has one or more Kana readings
            shirabe_jisho_words.extend(row[1].split(", "))

    jmdict = JMDict.from_path(jmdict_xml)

    for word in shirabe_jisho_words:
        print(word, jmdict.lookup(word))
