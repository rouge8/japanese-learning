from pathlib import Path

from shirabe_jisho_to_anki.shirabe_jisho import Bookmark


class TestBookmark:
    def test_all_from_csv(self, tmp_path: Path) -> None:
        bookmarks_csv = tmp_path / "bookmarks.csv"
        bookmarks_csv.write_text('行く,いく\n,"パクパク, ぱくぱく"\n')

        with bookmarks_csv.open() as fp:
            assert list(Bookmark.all_from_csv(fp)) == [
                Bookmark("行く", ["いく"]),
                Bookmark(None, ["パクパク", "ぱくぱく"]),
            ]
