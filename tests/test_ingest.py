from ingestion.scraper import WebScraper
from ingestion.parser import HTMLParser

scraper = WebScraper()
parser = HTMLParser()

html = scraper.download(
    "https://www.att.com/support/"
)

markdown = parser.parse(html)

with open(
    "test.md",
    "w",
    encoding="utf8"
) as f:
    f.write(markdown)

print("Done")