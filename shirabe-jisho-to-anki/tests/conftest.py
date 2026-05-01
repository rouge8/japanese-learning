# Resolve circular imports by importing the Anki collection early
from anki.collection import Collection  # noqa: F401
import pytest

from shirabe_jisho_to_anki.jmdict import Entry
from shirabe_jisho_to_anki.jmdict import Sense


@pytest.fixture
def iku_entry() -> Entry:
    return Entry(
        kanji_readings=("行く",),
        kana_readings=("いく",),
        senses=(
            Sense(
                parts_of_speech=(
                    "Godan verb - Iku/Yuku special class",
                    "intransitive verb",
                ),
                meanings=(
                    "to go",
                    "to move (towards)",
                    "to head (towards)",
                    "to leave (for)",
                ),
            ),
            Sense(
                parts_of_speech=(
                    "Godan verb - Iku/Yuku special class",
                    "intransitive verb",
                ),
                meanings=(
                    "to move through",
                    "to travel across",
                    "to walk along (e.g. a road)",
                ),
            ),
        ),
    )


@pytest.fixture
def ageru_to_raise_entry() -> Entry:
    return Entry(
        kanji_readings=("上げる",),
        kana_readings=("あげる",),
        senses=(
            Sense(
                parts_of_speech=(
                    "Ichidan verb",
                    "transitive verb",
                ),
                meanings=("to raise", "to elevate"),
            ),
            Sense(
                parts_of_speech=(
                    "Ichidan verb",
                    "transitive verb",
                ),
                meanings=("to give",),
            ),
        ),
    )


@pytest.fixture
def ageru_to_deep_fry_entry() -> Entry:
    return Entry(
        kanji_readings=("揚げる",),
        kana_readings=("あげる",),
        senses=(
            Sense(
                parts_of_speech=(
                    "to deep-fry",
                    "to make deep-fried food",
                ),
                meanings=("to raise", "to elevate"),
            ),
            Sense(
                parts_of_speech=(
                    "Ichidan verb",
                    "transitive verb",
                ),
                meanings=(
                    "to launch (fireworks, etc.)",
                    "to hoise (e.g. a flag)",
                ),
            ),
        ),
    )


@pytest.fixture
def tatemono_entry() -> Entry:
    return Entry(
        kanji_readings=("建物",),
        kana_readings=("たてもの",),
        senses=(
            Sense(
                parts_of_speech=("noun",),
                meanings=("building",),
            ),
        ),
    )


@pytest.fixture
def kouji_entry() -> Entry:
    return Entry(
        kanji_readings=("工事",),
        kana_readings=("こうじ",),
        senses=(
            Sense(
                parts_of_speech=(
                    "noun or participle which takes the aux. verb suru",
                    "transitive verb",
                ),
                meanings=("construction work",),
            ),
        ),
    )


@pytest.fixture
def aou_entry() -> Entry:
    return Entry(
        kanji_readings=("会う", "逢う"),
        kana_readings=("あう",),
        senses=(
            Sense(
                parts_of_speech=(
                    "Godan verb with 'u' ending",
                    "intransitive verb",
                ),
                meanings=(
                    "to meet",
                    "to encounter",
                    "to see",
                ),
            ),
            Sense(
                parts_of_speech=(
                    "Godan verb with 'u' ending",
                    "intransitive verb",
                ),
                meanings=(
                    "to have an accident",
                    "to have a bad experience",
                ),
            ),
        ),
    )


@pytest.fixture
def debu_entry() -> Entry:
    return Entry(
        kanji_readings=(),
        kana_readings=("デブ", "でぶ"),
        senses=(
            Sense(
                parts_of_speech=(
                    "noun",
                    "adjective",
                ),
                meanings=(
                    "fat",
                    "chubby",
                ),
            ),
        ),
    )


@pytest.fixture
def muda_ni_suru_entry() -> Entry:
    return Entry(
        kanji_readings=("無駄にする",),
        kana_readings=("むだにする",),
        senses=(
            Sense(
                parts_of_speech=("suru verb - included",),
                meanings=(
                    "to render futile",
                    "to bring to naught",
                    "to waste",
                    "to not make good use of",
                ),
            ),
        ),
    )


@pytest.fixture
def nomeru_to_be_able_to_drink_entry() -> Entry:
    return Entry(
        kanji_readings=("飲める",),
        kana_readings=("のめる",),
        senses=(
            Sense(
                parts_of_speech=("ichidan verb",),
                meanings=("to be able to drink",),
            ),
            Sense(
                parts_of_speech=("ichidan verb",),
                meanings=("to be worth drinking",),
            ),
        ),
    )


@pytest.fixture
def nomeru_to_fall_forward_entry() -> Entry:
    return Entry(
        kanji_readings=(),
        kana_readings=("のめる",),
        senses=(
            Sense(
                parts_of_speech=("godan verb with 'ru' ending", "intransitive verb"),
                meanings=("to fall forward (of a person)", "to tumble forward"),
            ),
        ),
    )
