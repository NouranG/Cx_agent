from ingestion.parser import HTMLParser


def test_parser_removes_navigation_and_scripts_and_converts_to_markdown():
    html = """
    <html><body>
      <nav>Navigation link</nav>
      <header>Site header</header>
      <script>alert('x')</script>
      <main><h1>Router help</h1><p>Restart your router.</p></main>
      <footer>Site footer</footer>
    </body></html>
    """
    result = HTMLParser().parse(html)
    assert "Router help" in result
    assert "Restart your router." in result
    assert "Navigation link" not in result
    assert "Site header" not in result
    assert "Site footer" not in result
    assert "alert(" not in result
