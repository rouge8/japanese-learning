import pytest
from pytest_unordered import unordered

from shirabe_jisho_to_anki.jmdict import Entry
from shirabe_jisho_to_anki.jmdict import EntryNotFound
from shirabe_jisho_to_anki.jmdict import JMDict
from shirabe_jisho_to_anki.jmdict import MultipleEntriesForBookmark
from shirabe_jisho_to_anki.jmdict import Sense
from shirabe_jisho_to_anki.shirabe_jisho import Bookmark

EMPTY_SENSES = (Sense(parts_of_speech=(), meanings=(), misc=frozenset()),)


class TestJMDict:
    @pytest.fixture
    def jmdict(self) -> JMDict:
        entries = [
            Entry(
                kanji_readings=("kanji1",),
                kana_readings=("kana1",),
                senses=EMPTY_SENSES,
            ),
            Entry(
                kanji_readings=(),
                kana_readings=("kana1",),
                senses=EMPTY_SENSES,
            ),
            Entry(
                kanji_readings=("kanji1",),
                kana_readings=("kana2",),
                senses=EMPTY_SENSES,
            ),
            Entry(
                kanji_readings=("kanji2",),
                kana_readings=("kana2",),
                senses=EMPTY_SENSES,
            ),
            Entry(
                kanji_readings=("kanji3",),
                kana_readings=("kana2",),
                senses=EMPTY_SENSES,
            ),
            Entry(
                kanji_readings=("kanji_with_no_senses",),
                kana_readings=("kana2",),
                senses=(),
            ),
            Entry(
                kanji_readings=(),
                kana_readings=("kana_with_no_senses",),
                senses=(),
            ),
            Entry(
                kanji_readings=(),
                kana_readings=("パック",),
                senses=(
                    Sense(
                        parts_of_speech=("noun",),
                        meanings=("pack", "packet", "carton"),
                        misc=frozenset(),
                    ),
                ),
            ),
            Entry(
                kanji_readings=(),
                kana_readings=("パック",),
                senses=(
                    Sense(
                        parts_of_speech=("noun",),
                        meanings=("puck",),
                        misc=frozenset(),
                    ),
                ),
            ),
        ]
        jmdict = JMDict()

        for entry in entries:
            for kanji_reading in entry.kanji_readings:
                jmdict._entries[kanji_reading].append(entry)
            for kana_reading in entry.kana_readings:
                jmdict._entries[kana_reading].append(entry)
        return jmdict

    def test_lookup_all_kanji_reading_match(self, jmdict: JMDict) -> None:
        """If a bookmark has a Kanji reading, its Kana readings are ignored."""
        assert jmdict.lookup_all(Bookmark("kanji1", ["kana2"])) == unordered(
            [
                Entry(
                    kanji_readings=("kanji1",),
                    kana_readings=("kana1",),
                    senses=EMPTY_SENSES,
                ),
                Entry(
                    kanji_readings=("kanji1",),
                    kana_readings=("kana2",),
                    senses=EMPTY_SENSES,
                ),
            ]
        )

    def test_lookup_all_kanji_reading_no_match(self, jmdict: JMDict) -> None:
        """If a bookmark has a Kanji reading, its Kana readings are ignored."""
        assert jmdict.lookup_all(Bookmark("unknown_kanji", ["kana2"])) == []

    def test_lookup_all_kanji_reading_no_senses_excluded(self, jmdict: JMDict) -> None:
        """Entries with no Senses are excluded."""
        assert jmdict.lookup_all(Bookmark("kanji_with_no_senses", ["kana2"])) == []

    def test_lookup_all_kana_reading_match(self, jmdict: JMDict) -> None:
        """
        A bookmark with only Kana readings returns Entries with only Kana
        readings.
        """
        assert jmdict.lookup_all(Bookmark(None, ["kana1"])) == [
            Entry(
                kanji_readings=(),
                kana_readings=("kana1",),
                senses=EMPTY_SENSES,
            ),
        ]

    def test_lookup_all_kana_reading_no_match(self, jmdict: JMDict) -> None:
        assert jmdict.lookup_all(Bookmark(None, ["unknown_kana"])) == []

    def test_lookup_all_kana_reading_no_senses_excluded(self, jmdict: JMDict) -> None:
        """Entries with no Senses are excluded."""
        assert jmdict.lookup_all(Bookmark(None, ["kana_with_no_senses"])) == []

    def test_lookup_best_match(self, jmdict: JMDict) -> None:
        """If there is only one match, return it regardless of Kana."""
        bookmark = Bookmark("kanji3", ["unknown_kana"])
        assert len(jmdict.lookup_all(bookmark)) == 1
        assert jmdict.lookup_best(bookmark) == Entry(
            kanji_readings=("kanji3",),
            kana_readings=("kana2",),
            senses=EMPTY_SENSES,
        )

    def test_lookup_best_no_match(self, jmdict: JMDict) -> None:
        with pytest.raises(EntryNotFound):
            jmdict.lookup_best(Bookmark("unknown_kanji", ["unknown_kana"]))

    def test_lookup_best_multiple_candidates_one_match(self, jmdict: JMDict) -> None:
        """
        If multiple entries are found, the best match is the one with
        overlapping Kana readings.
        """
        bookmark = Bookmark("kanji1", ["kana1"])
        assert len(jmdict.lookup_all(bookmark)) > 1
        assert jmdict.lookup_best(bookmark) == Entry(
            kanji_readings=("kanji1",),
            kana_readings=("kana1",),
            senses=EMPTY_SENSES,
        )

    def test_lookup_best_multiple_candidates_multiple_entries(
        self, jmdict: JMDict
    ) -> None:
        with pytest.raises(MultipleEntriesForBookmark):
            jmdict.lookup_best(Bookmark(None, ["パック"]))


class TestEntry:
    def test_masu_forms_ichidan_verb(self, ageru_to_deep_fry_entry: Entry) -> None:
        assert ageru_to_deep_fry_entry.masu_forms() == {"揚げます"}

    def test_masu_forms_godan_verb(self, aou_entry: Entry) -> None:
        assert aou_entry.masu_forms() == {"会います", "逢います"}

    def test_masu_forms_suru_verb(self, muda_ni_suru_entry: Entry) -> None:
        assert muda_ni_suru_entry.masu_forms() == {"無駄にします"}

    def test_masu_forms_non_verb(self, tatemono_entry: Entry) -> None:
        assert tatemono_entry.masu_forms() is None

    @pytest.mark.parametrize(
        "entry_fixture, expected", [("kouji_entry", True), ("tatemono_entry", False)]
    )
    def test_is_noun_with_suru_verb(
        self, entry_fixture: str, expected: bool, request: pytest.FixtureRequest
    ) -> None:
        entry: Entry = request.getfixturevalue(entry_fixture)
        assert entry.is_noun_with_suru_verb() is expected
