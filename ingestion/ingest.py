from pathlib import Path

from ingestion.sources import SOURCES
from ingestion.crawler import DocumentationCrawler
from ingestion.scraper import WebScraper
from ingestion.parser import HTMLParser

OUTPUT_DIR = Path("knowledge_base")

scraper = WebScraper()
parser = HTMLParser()


def save_document(source_name, url):

    html = scraper.download(url)

    markdown = parser.parse(html)

    folder = OUTPUT_DIR / source_name
    folder.mkdir(parents=True, exist_ok=True)

    filename = url.rstrip("/").split("/")[-1]

    if not filename:
        filename = "index"

    filename += ".md"

    with open(
    folder / filename,
    "w",
    encoding="utf-8"
) as f:
        f.write(markdown)

    print(f"Saved {source_name}/{filename}")


def main():

    for source in SOURCES:

        print(f"\n=== Crawling {source['name']} ===")

        crawler = DocumentationCrawler(source)

        urls = crawler.crawl()

        print(f"Found {len(urls)} pages")

        for url in urls:

            try:
                save_document(source["name"], url)

            except Exception as e:

                print(f"Failed: {url}")
                print(e)


if __name__ == "__main__":
    main()