from pyreqwest.response import SyncResponse
from collections.abc import Iterable
import time
import typing

import attrs
import structlog
from pyreqwest.client import SyncClient, SyncClientBuilder

log = structlog.get_logger()


@attrs.define
class UnknownKanjiError(Exception):
    kanji: str


@attrs.frozen
class Kanji:
    id: int
    document_url: str
    characters: str
    meanings: list[str]
    readings: list[str]


_KANJI: dict[int, Kanji] = {}


@attrs.frozen
class WaniKaniAPIClient:
    api_key: str = attrs.field(repr=False)
    base_url: str = "https://api.wanikani.com/v2"
    client: SyncClient = attrs.Factory(lambda: SyncClientBuilder().build())

    def _request(
        self,
        path: str,
        params: dict[str, str] | None = None,
    ) -> SyncResponse:
        log.info("requesting", path=path, params=params)
        start = time.time()
        resp = (
            (
                self.client.get(f"{self.base_url}/{path}")
                .header("Wanikani-Revision", "20170710")
                .bearer_auth(self.api_key)
                .query(params or {})
            )
            .build()
            .send()
        )
        end = time.time()
        log.info(
            "requested",
            path=path,
            params=params,
            status_code=resp.status,
            duration=end - start,
        )
        resp.error_for_status()
        return resp

    def _paginated_request(
        self,
        path: str,
        params: dict[str, str] | None = None,
    ) -> Iterable[dict[str, typing.Any]]:
        next_url = path

        while next_url is not None:
            resp = self._request(next_url, params)
            resp = resp.json()

            next_url = resp["pages"]["next_url"]
            if next_url is not None:
                next_url = next_url.split(f"{self.base_url}/", 1)[1]
                # next_url contains the query parameters
                params = None

            yield from resp["data"]

    def load_kanji(self) -> None:
        """Load all Kanji into memory."""
        for kanji in self._paginated_request(
            "subjects",
            {"types": "kanji", "hidden": "false"},
        ):
            _KANJI[kanji["id"]] = Kanji(
                id=kanji["id"],
                document_url=kanji["data"]["document_url"],
                characters=kanji["data"]["characters"],
                meanings=[
                    meaning["meaning"]
                    for meaning in kanji["data"]["meanings"]
                    if meaning["accepted_answer"]
                ],
                readings=[
                    reading["reading"]
                    for reading in kanji["data"]["readings"]
                    if reading["primary"] or reading["accepted_answer"]
                ],
            )

    def burnt_kanji(self) -> Iterable[Kanji]:
        """
        Get all burnt Kanji.

        Must be called after loading the Kanji data into memory with
        :meth:`~.load_kanji`.
        """
        for assignment in self._paginated_request(
            "assignments",
            {"subject_types": "kanji", "burned": "true", "hidden": "false"},
        ):
            yield _KANJI[assignment["data"]["subject_id"]]

    def get_kanji(self, kanji: str) -> Kanji:
        """
        Look up an individual Kanji.

        Must be called after loading the Kanji data into memory with
        :meth:`~.load_kanji`.
        """
        try:
            return next(  # pragma: no branch
                k for k in _KANJI.values() if k.characters == kanji
            )
        except StopIteration as err:
            raise UnknownKanjiError(kanji) from err
