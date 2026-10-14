def test_save_document_writes_parsed_markdown(tmp_path, monkeypatch):
    import ingestion.ingest as ingest_module
    monkeypatch.setattr(ingest_module, "OUTPUT_DIR", tmp_path)
    monkeypatch.setattr(ingest_module.scraper, "download", lambda url: "<html>source</html>")
    monkeypatch.setattr(ingest_module.parser, "parse", lambda html: "# Parsed document")
    ingest_module.save_document("sample", "https://example.com/docs/router")
    output = tmp_path / "sample" / "router.md"
    assert output.exists()
    assert output.read_text(encoding="utf-8") == "# Parsed document"
