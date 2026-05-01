from collections import defaultdict
from collections.abc import Iterator
import itertools
from typing import Literal
from typing import Self

from attrs import define
from attrs import Factory
from attrs import frozen
from lxml.etree import Element
from lxml.etree import iterparse

from .helpers import exactly_one
from .helpers import not_none
from .jp_helpers import godan_verb_to_masu_form
from .shirabe_jisho import Bookmark


@define
class EntryNotFound(Exception):
    """No entries were found for a Bookmark."""

    bookmark: Bookmark


@define
class MultipleEntriesForBookmark(Exception):
    """Multiple entries for a Bookmark could not be narrowed down."""

    bookmark: Bookmark
    entries: list[Entry]


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

    def lookup_all(self, bookmark: Bookmark) -> list[Entry]:
        """Lookup all entries for a Bookmark."""
        if bookmark.kanji_reading:
            entries = set(self._entries.get(bookmark.kanji_reading) or [])
        else:
            entries = set(
                itertools.chain.from_iterable(
                    {
                        entry
                        for entry in (self._entries.get(reading) or [])
                        # Filter out entries with Kanji readings because the
                        # bookmark doesn't have a Kanji reading
                        if not entry.kanji_readings
                    }
                    for reading in bookmark.kana_readings
                )
            )
        return [e for e in entries if e.senses]

    def lookup_best(self, bookmark: Bookmark) -> Entry:
        """Lookup the "best" entry for a Bookmark."""
        entries = self.lookup_all(bookmark)
        if not entries:
            raise EntryNotFound(bookmark)
        elif len(entries) == 1:
            return entries[0]
        else:
            candidates = [
                e for e in entries if set(bookmark.kana_readings) & set(e.kana_readings)
            ]
            if len(candidates) > 1:
                raise MultipleEntriesForBookmark(bookmark, candidates)
            return candidates[0]


@frozen(kw_only=True)
class Entry:
    """A JMDict entry."""

    kanji_readings: tuple[str, ...]
    kana_readings: tuple[str, ...]
    senses: tuple[Sense, ...]

    def kanji_masu_forms(self) -> set[str] | None:
        """'masu' forms of the Kanji readings, if the entry is a verb."""
        return self._masu_forms(self.kanji_readings)

    def kana_masu_forms(self) -> set[str] | None:
        """'masu' forms of the Kana readings, if the entry is a verb."""
        return self._masu_forms(self.kana_readings)

    def _masu_forms(self, readings: tuple[str, ...]) -> set[str] | None:
        """'masu' forms of the given readings, if the entry is a verb."""
        if "ichidan verb" in self._parts_of_speech:
            return {reading[:-1] + "ます" for reading in readings}
        elif any(pos.startswith("godan verb") for pos in self._parts_of_speech):
            return {godan_verb_to_masu_form(reading) for reading in readings}
        # "suru verb - included" or "suru verb - special class"
        elif any(pos.startswith("suru verb") for pos in self._parts_of_speech):
            return {reading[:-2] + "します" for reading in readings}
        else:
            return None

    def is_noun_with_suru_verb(self) -> bool:
        """Whether or not the entry is a noun that takes the auxiliary verb suru."""
        return (
            "noun or participle which takes the aux. verb suru" in self._parts_of_speech
        )

    @property
    def _parts_of_speech(self) -> set[str]:
        parts_of_speech = itertools.chain.from_iterable(
            sense.parts_of_speech for sense in self.senses
        )
        return {pos.lower() for pos in parts_of_speech}

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

        senses = (Sense.from_element(el) for el in element.findall("sense"))
        senses = (s for s in senses if cls._should_add_sense(s))

        return cls(
            kanji_readings=tuple(kanji_readings),
            kana_readings=tuple(kana_readings),
            senses=tuple(senses),
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
            }
        )

    @staticmethod
    def _should_add_kana_reading(kana_info: set[str | None]) -> bool:
        return not bool(
            kana_info
            & {
                "word containing irregular kana usage",
                "out-dated or obsolete kana usage",
            }
        )

    @staticmethod
    def _should_add_sense(sense: Sense) -> bool:
        return not bool(sense.misc & {"archaic", "character"})


@frozen(kw_only=True)
class Sense:
    """The translational equivalent of a Japanese word."""

    parts_of_speech: tuple[str, ...]
    meanings: tuple[str, ...]
    misc: frozenset[str] = Factory(frozenset)

    @classmethod
    def from_element(cls, element: Element) -> Self:
        parts_of_speech = tuple(not_none(el.text) for el in element.findall("pos"))
        meanings = tuple(not_none(el.text) for el in element.findall("gloss"))
        misc = frozenset(not_none(el.text) for el in element.findall("misc"))
        return cls(parts_of_speech=parts_of_speech, meanings=meanings, misc=misc)


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
