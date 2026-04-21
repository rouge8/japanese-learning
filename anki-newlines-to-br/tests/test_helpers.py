import pytest

from anki_newlines_to_br.helpers import not_none


class TestNotNone:
    def test_not_none(self) -> None:
        assert not_none(1) == 1

    def test_not_none_is_none(self) -> None:
        with pytest.raises(AssertionError):
            not_none(None)
