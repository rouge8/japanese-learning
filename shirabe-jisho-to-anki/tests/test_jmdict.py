import pytest

from shirabe_jisho_to_anki.jmdict import Entry
from shirabe_jisho_to_anki.jmdict import JMDict
from shirabe_jisho_to_anki.shirabe_jisho import Bookmark


class TestJMDict:
    def test_lookup_all_kanji_reading_match(self) -> None:
        jmdict = JMDict()
        assert False

    def test_lookup_all_kanji_reading_no_match(self) -> None:
        jmdict = JMDict()
        assert False

    def test_lookup_all_kana_reading_match(self) -> None:
        jmdict = JMDict()
        assert False

    def test_lookup_all_kana_reading_no_match(self) -> None:
        jmdict = JMDict()
        assert False

    def test_lookup_best_match(self) -> None:
        jmdict = JMDict()
        assert False

    def test_lookup_best_no_match(self) -> None:
        jmdict = JMDict()
        assert False

    def test_lookup_best_multiple_candidates_one_match(self) -> None:
        jmdict = JMDict()
        assert False

    def test_lookup_best_multiple_candidates_multiple_entries(self) -> None:
        jmdict = JMDict()
        assert False


class TestEntry:
    def test_masu_forms_ichidan_verb(self, ageru_to_deep_fry_entry: Entry) -> None:
        assert ageru_to_deep_fry_entry.masu_forms() == {"揚げます"}

    def test_masu_forms_godan_verb(self, aou_entry: Entry) -> None:
        assert aou_entry.masu_forms() == {"会います", "逢います"}

    def test_masu_forms_suru_verb(self, muda_ni_suru_entry: Entry) -> None:
        assert muda_ni_suru_entry.masu_forms() == {"無駄にします"}

    def test_masu_forms_non_verb(self, tatemono_entry: Entry) -> None:
        assert tatemono_entry.masu_forms() == None

    @pytest.mark.parametrize(
        "entry_fixture, expected", [("kouji_entry", True), ("tatemono_entry", False)]
    )
    def test_is_noun_with_suru_verb(
        self, entry_fixture: str, expected: bool, request: pytest.FixtureRequest
    ) -> None:
        entry: Entry = request.getfixturevalue(entry_fixture)
        assert entry.is_noun_with_suru_verb() is expected
