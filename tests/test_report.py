import json

import pytest
from pydantic import ValidationError

import app
from models import ResearchReport

VALID = {
    "title": "  intro to GPT-4 and NASA's AI  ",
    "executive_summary": " Short summary. ",
    "key_findings": [" one ", "two", "   ", "three"],
    "conclusion": " Done. ",
}


def test_cleanup_keeps_casing_and_drops_blank_findings():
    r = ResearchReport.model_validate(VALID)
    assert r.title == "intro to GPT-4 and NASA's AI"
    assert r.key_findings == ["one", "two", "three"]
    assert r.conclusion == "Done."


@pytest.mark.parametrize(
    "findings",
    [["a", "b"], ["a", "  ", " "], ["a", "b", "c", "d", "e", "f"]],
)
def test_findings_must_be_3_to_5_after_cleanup(findings):
    with pytest.raises(ValidationError):
        ResearchReport.model_validate({**VALID, "key_findings": findings})


def test_empty_title_rejected():
    with pytest.raises(ValidationError):
        ResearchReport.model_validate({**VALID, "title": "   "})


class FakeResponse:
    def __init__(self, body):
        self._body = body

    def raise_for_status(self):
        pass

    def json(self):
        return {"response": json.dumps(self._body)}


def test_generate_report_sends_schema_and_timeout(monkeypatch):
    sent = {}

    def fake_post(url, json, timeout):
        sent.update(url=url, payload=json, timeout=timeout)
        return FakeResponse(VALID)

    monkeypatch.setattr(app.requests, "post", fake_post)
    report = app.generate_report("AI", "context")

    assert sent["payload"]["format"] == ResearchReport.model_json_schema()
    assert sent["timeout"] == app.REQUEST_TIMEOUT_S
    assert report.key_findings == ["one", "two", "three"]


def test_search_error_is_raised_not_passed_to_llm(monkeypatch):
    class Boom:
        def text(self, *a, **k):
            raise RuntimeError("rate limited")

    monkeypatch.setattr(app, "DDGS", Boom)
    with pytest.raises(app.SearchError):
        app.search_web("anything")


def test_empty_search_results_raise(monkeypatch):
    class Empty:
        def text(self, *a, **k):
            return []

    monkeypatch.setattr(app, "DDGS", Empty)
    with pytest.raises(app.SearchError):
        app.search_web("anything")


def test_format_markdown():
    md = app.format_markdown(ResearchReport.model_validate(VALID))
    assert md.startswith("# intro to GPT-4")
    assert "- one\n" in md and "## Conclusion" in md
