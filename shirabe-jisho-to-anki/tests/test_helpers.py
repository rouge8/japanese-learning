import pytest

from shirabe_jisho_to_anki.helpers import exactly_one
from shirabe_jisho_to_anki.helpers import not_none


class TestNotNone:
    def test_not_none(self) -> None:
        assert not_none(1) == 1

    def test_not_none_is_none(self) -> None:
        with pytest.raises(AssertionError):
            not_none(None)


class TestExactlyOne:
    def test_exactly_one(self) -> None:
        assert exactly_one([1]) == 1

    def test_zero(self) -> None:
        with pytest.raises(AssertionError):
            exactly_one([])

    def test_many(self) -> None:
        with pytest.raises(AssertionError):
            exactly_one([1, 2])
