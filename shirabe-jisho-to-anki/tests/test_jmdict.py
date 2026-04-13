import pytest

from shirabe_jisho_to_anki.jmdict import Entry
from shirabe_jisho_to_anki.jmdict import JMDict


class TestJMDict:
    def test_lookup_all_kanji_reading_match(self) -> None:
        assert False

    def test_lookup_all_kanji_reading_no_match(self) -> None:
        assert False

    def test_lookup_all_kana_reading_match(self) -> None:
        assert False

    def test_lookup_all_kana_reading_no_match(self) -> None:
        assert False

    def test_lookup_best_match(self) -> None:
        assert False

    def test_lookup_best_no_match(self) -> None:
        assert False

    def test_lookup_best_multiple_candidates_one_match(self) -> None:
        assert False

    def test_lookup_best_multiple_candidates_multiple_entries(self) -> None:
        assert False


class TestEntry:
    def test_masu_forms_ichidan_verb(self) -> None:
        assert False

    def test_masu_forms_godan_verb(self) -> None:
        assert False

    def test_masu_forms_suru_verb(self) -> None:
        assert False

    def test_is_noun_with_suru_verb(self) -> None:
        assert False
