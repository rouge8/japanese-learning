from collections.abc import Iterator
import csv
import io
from typing import Self

from attrs import define


@define
class Bookmark:
    """A Shirabe Jisho bookmark."""

    kanji_reading: str | None
    kana_readings: list[str]

    @classmethod
    def all_from_csv(cls, fp: io.TextIOWrapper) -> Iterator[Self]:
        for row in csv.reader(fp):
            yield cls(row[0] or None, row[1].split(", "))
