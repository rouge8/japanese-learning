from collections import Counter
from anki_extract_kanji.__main__ import unknown_kanji


def test_unknown_kanji() -> None:
    assert unknown_kanji(
        {"行", "有"},
        ["泊まる", "行く", "有る", "上", "上げる", "下", "下げる", "下ろす"],
    ) == Counter(["上", "上", "下", "下", "下", "泊"])
