from anki.decks import DeckId
import pytest

from shirabe_jisho_to_anki.anki import Card
from shirabe_jisho_to_anki.anki import Deck
from shirabe_jisho_to_anki.jmdict import Entry


class TestDeck:
    @pytest.fixture
    def deck(self) -> Deck:
        return Deck(
            DeckId(1),
            "Japanese",
            {
                "行きます / いきます",
                "上げる / あげる",
            },
        )

    @pytest.mark.parametrize("entry_fixture", ["iku_entry", "ageru_to_raise_entry"])
    def test_has_card_match(
        self, entry_fixture: str, deck: Deck, request: pytest.FixtureRequest
    ) -> None:
        entry: Entry = request.getfixturevalue(entry_fixture)
        assert deck.has_card(Card.from_jmdict_entry(entry)) is True

    def test_has_card_no_match(
        self, deck: Deck, ageru_to_deep_fry_entry: Entry
    ) -> None:
        assert deck.has_card(Card.from_jmdict_entry(ageru_to_deep_fry_entry)) is False


class TestCard:
    def test_from_jmdict_entry(self, aou_entry: Entry) -> None:
        card = Card.from_jmdict_entry(aou_entry)
        assert card.front == "会う / 逢う / あう"
        assert (
            card.back
            == "to meet; to encounter; to see\nto have an accident; "
            + "to have a bad experience"
        )

    def test_from_jmdict_entry_suru_verb(self, kouji_entry: Entry) -> None:
        card = Card.from_jmdict_entry(kouji_entry)
        assert card.front == "工事（する） / こうじ（する）"
        assert card.back == "construction work (n, v)"

    def test_from_jmdict_entry_no_kanji(self, debu_entry: Entry) -> None:
        card = Card.from_jmdict_entry(debu_entry)
        assert card.front == "デブ / でぶ"
        assert card.back == "fat; chubby"

    def test_search_terms_verb(self, ageru_to_deep_fry_entry: Entry) -> None:
        card = Card.from_jmdict_entry(ageru_to_deep_fry_entry)
        assert card.search_terms() == {"揚げる", "揚げます"}

    def test_search_terms_non_verb(self, tatemono_entry: Entry) -> None:
        card = Card.from_jmdict_entry(tatemono_entry)
        assert card.search_terms() == {"建物"}
