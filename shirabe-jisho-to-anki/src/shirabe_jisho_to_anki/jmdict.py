from collections import defaultdict
from collections.abc import Iterator
from typing import Literal
from typing import Self

from attrs import define
from attrs import Factory
from lxml.etree import Element
from lxml.etree import iterparse

from .helpers import exactly_one
from .helpers import not_none


@define
class JMDict:
    """
    Parse and lookup entries in JMDict.

    JMDict's English-only translation can be downloaded from:
    https://www.edrdg.org/jmdict/j_jmdict.html
    """

    _entries: defaultdict[str, list[Entry]] = Factory(lambda: defaultdict(list))

    @classmethod
    def from_path(cls, path: str) -> Self:
        """Parse a JMDict XML file."""
        entries_map = defaultdict(list)

        for entry in _JMDictXMLParser.from_path(path).entries():
            for kanji_reading in entry.kanji_readings:
                entries_map[kanji_reading].append(entry)
            for kana_reading in entry.kana_readings:
                entries_map[kana_reading].append(entry)

        return cls(entries_map)

    def lookup(self, reading: str) -> list[Entry] | None:
        return self._entries.get(reading)


@define(kw_only=True)
class Entry:
    """A JMDict entry."""

    kanji_readings: list[str]
    kana_readings: list[str]
    senses: list[Sense]

    @classmethod
    def from_element(cls, element: Element) -> Self:
        kanji_readings: list[str] = []
        kana_readings: list[str] = []

        for kanji_element in element.findall("k_ele"):
            reading = not_none(exactly_one(kanji_element.findall("keb")).text)
            if cls._should_add_kanji_reading(
                {el.text for el in kanji_element.findall("ke_inf")}
            ):
                kanji_readings.append(reading)

        for kana_element in element.findall("r_ele"):
            reading = not_none(exactly_one(kana_element.findall("reb")).text)
            if cls._should_add_kana_reading(
                {el.text for el in kana_element.findall("re_inf")}
            ):
                kana_readings.append(reading)

        return cls(
            kanji_readings=kanji_readings,
            kana_readings=kana_readings,
            senses=[Sense.from_element(el) for el in element.findall("sense")],
        )

    @staticmethod
    def _should_add_kanji_reading(kanji_info: set[str | None]) -> bool:
        return not bool(
            kanji_info
            & {
                "word containing irregular kana usage",
                "word containing irregular kanji usage",
                "irregular okurigana usage",
                "word containing out-dated kanji or kanji usage",
                "rarely used kanji form",
                "search-only kanji form",
            }
        )

    @staticmethod
    def _should_add_kana_reading(kana_info: set[str | None]) -> bool:
        return not bool(
            kana_info
            & {
                "word containing irregular kana usage",
                "out-dated or obsolete kana usage",
                "rarely used kana form",
                "search-only kana form",
            }
        )


@define(kw_only=True)
class Sense:
    """The translational equivalent of a Japanese word."""

    parts_of_speech: list[str]
    meanings: list[str]

    @classmethod
    def from_element(cls, element: Element) -> Self:
        parts_of_speech = [not_none(el.text) for el in element.findall("pos")]
        meanings = [not_none(el.text) for el in element.findall("gloss")]
        return cls(parts_of_speech=parts_of_speech, meanings=meanings)


@define
class _JMDictXMLParser:
    parser: iterparse[tuple[Literal["end"], Element]]

    @classmethod
    def from_path(cls, path: str) -> Self:
        return cls(iterparse(path))

    def entries(self) -> Iterator[Entry]:
        for _event, element in self.parser:
            if element.tag == "entry":
                yield Entry.from_element(element)
