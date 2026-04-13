import pytest

from shirabe_jisho_to_anki.jp_helpers import godan_verb_to_masu_form


@pytest.mark.parametrize(
    "verb, expected",
    [
        ("遊ぶ", "遊びます"),
        ("泳ぐ", "泳ぎます"),
        ("行く", "行きます"),
        ("頼む", "頼みます"),
        ("死ぬ", "死にます"),
        ("参る", "参ります"),
        ("話す", "話します"),
        ("建つ", "建ちます"),
        ("歌う", "歌います"),
    ],
)
def test_godan_verb_to_masu_form(verb: str, expected: str) -> None:
    assert godan_verb_to_masu_form(verb) == expected


def test_godan_verb_to_masu_form_noun() -> None:
    with pytest.raises(ValueError):
        godan_verb_to_masu_form("建物")
