from ingestion.scraper import WebScraper


class FakeResponse:
    text = "<html>support page</html>"
    def raise_for_status(self):
        pass


def test_scraper_returns_html_and_uses_timeout(monkeypatch):
    import ingestion.scraper as scraper_module
    calls = {}
    def fake_get(url, **kwargs):
        calls["url"] = url
        calls.update(kwargs)
        return FakeResponse()
    monkeypatch.setattr(scraper_module.requests, "get", fake_get)
    html = WebScraper().download("https://example.com/support")
    assert html == "<html>support page</html>"
    assert calls["timeout"] == 30
    assert "User-Agent" in calls["headers"]
