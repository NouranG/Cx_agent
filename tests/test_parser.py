from ingestion.scraper import WebScraper
from ingestion.parser import HTMLParser

scraper = WebScraper()
parser = HTMLParser()

html = scraper.download("https://www.att.com/support/")

markdown = parser.parse(html)

print(markdown[:2000])