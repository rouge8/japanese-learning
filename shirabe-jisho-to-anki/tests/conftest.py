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
                misc=frozenset(),
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
                misc=frozenset(),
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
                misc=frozenset(),
            ),
            Sense(
                parts_of_speech=(
                    "Ichidan verb",
                    "transitive verb",
                ),
                meanings=("to give",),
                misc=frozenset(),
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
                misc=frozenset(),
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
                misc=frozenset(),
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
                misc=frozenset(),
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
                misc=frozenset(),
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
                misc=frozenset(),
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
                misc=frozenset(),
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
                misc=frozenset(),
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
                misc=frozenset(),
            ),
        ),
    )
