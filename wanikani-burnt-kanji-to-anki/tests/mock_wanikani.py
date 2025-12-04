from functools import cached_property
from typing import Any

from attrs import define
from attrs import Factory
from falcon import App
from falcon import Request
from falcon import Response


@define
class KanjiPage:
    page_after_id: str | None
    next_page_after_id: str | None
    data: list[dict[str, Any]]


@define
class _KanjiSubjectResource:
    base_url: str
    kanji_pages: dict[str | None, KanjiPage] = Factory(dict)

    def on_get(self, req: Request, resp: Response) -> None:
        types = req.get_param("types")
        assert types == "kanji"

        hidden = req.get_param_as_bool("hidden")
        assert hidden is False

        page_after_id = req.get_param("page_after_id")
        page = self.kanji_pages[page_after_id]
        if page.next_page_after_id:
            next_page_url = f"{self.base_url}/subjects?types=kanji&hidden=false&page_after_id={page.next_page_after_id}"  # noqa: E501
        else:
            next_page_url = None

        resp.media = {
            "pages": {"next_url": next_page_url},
            "data": page.data,
        }


@define
class _AssignmentsResource:
    assignments: list[dict[str, Any]] = Factory(list)

    def on_get(self, req: Request, resp: Response) -> None:
        subject_types = req.get_param("subject_types")
        assert subject_types == "kanji"

        burned = req.get_param_as_bool("burned")
        assert burned is True

        hidden = req.get_param_as_bool("hidden")
        assert hidden is False

        resp.media = {"pages": {"next_url": None}, "data": self.assignments}


@define
class MockWaniKaniAPI:
    base_url: str

    _kanji_subject_resource: _KanjiSubjectResource = Factory(
        lambda self: _KanjiSubjectResource(self.base_url), takes_self=True
    )
    _assignments_resource: _AssignmentsResource = Factory(_AssignmentsResource)

    def add_kanji_page(self, page: KanjiPage) -> None:
        if (
            page.page_after_id in self._kanji_subject_resource.kanji_pages
        ):  # pragma: no cover
            raise ValueError("Page with specified page_after_id already exists")
        else:
            self._kanji_subject_resource.kanji_pages[page.page_after_id] = page

    def add_assignments(self, assignments: list[dict[str, Any]]) -> None:
        self._assignments_resource.assignments.extend(assignments)

    @cached_property
    def app(self) -> App:
        app = App()
        app.add_route("/subjects", self._kanji_subject_resource)
        app.add_route("/assignments", self._assignments_resource)
        return app
