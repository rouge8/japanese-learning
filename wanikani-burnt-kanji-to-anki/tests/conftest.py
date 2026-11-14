from collections.abc import Generator

import httpx2
import pytest

from wanikani_burnt_kanji_to_anki.wanikani import WaniKaniAPIClient

from .mock_wanikani import MockWaniKaniAPI


@pytest.fixture
def base_url() -> str:
    return "http://wanikani-testserver"


@pytest.fixture
def mock_wanikani(base_url: str) -> MockWaniKaniAPI:
    return MockWaniKaniAPI(base_url)


@pytest.fixture
def api_client(
    base_url: str, mock_wanikani: MockWaniKaniAPI
) -> Generator[WaniKaniAPIClient]:
    """A WaniKaniAPIClient"""

    transport = httpx2.WSGITransport(mock_wanikani.app)
    with httpx2.Client(transport=transport) as client:
        yield WaniKaniAPIClient(
            "fake-key",
            base_url=base_url,
            client=client,
        )


@pytest.fixture(autouse=True)
def reset_kanji_cache() -> None:
    """Reset the Kanji cache between tests."""
    from wanikani_burnt_kanji_to_anki.wanikani import _KANJI

    _KANJI.clear()
