from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


class DocumentationCrawler:

    def __init__(self, source: dict):

        self.name = source["name"]
        self.base_url = source["base_url"]
        self.allowed_prefixes = source["allowed_prefixes"]

    def crawl(self):

        response = requests.get(
            self.base_url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=30,
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")

        links = set()

        for tag in soup.find_all("a", href=True):

            href = tag["href"]

            full_url = urljoin(self.base_url, href)

            parsed = urlparse(full_url)

            # Only keep pages from the same website
            if parsed.netloc != urlparse(self.base_url).netloc:
                continue

            # Remove query strings and fragments
            clean_url = (
                parsed.scheme
                + "://"
                + parsed.netloc
                + parsed.path
            )

            # Keep only documentation pages
            if not parsed.path.startswith(self.allowed_prefixes):
                continue

            links.add(clean_url)

        return sorted(links)