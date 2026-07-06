import re

from bs4 import BeautifulSoup
from markdownify import markdownify


class HTMLParser:

    def parse(self, html):

        soup = BeautifulSoup(html, "lxml")

        # Remove unwanted HTML elements
        for tag in soup([
            "script",
            "style",
            "header",
            "footer",
            "nav",
            "aside",
        ]):
            tag.decompose()

        # Convert HTML to Markdown
        markdown = markdownify(str(soup))

        # -------------------------
        # Markdown cleanup
        # -------------------------

        # Remove Markdown images
        markdown = re.sub(r"!\[.*?\]\(.*?\)", "", markdown)

        # Remove repeated "Sign in" lines
        markdown = re.sub(r"(?im)^sign in\s*$", "", markdown)

        # Collapse multiple blank lines
        markdown = re.sub(r"\n{3,}", "\n\n", markdown)

        # Remove extra spaces
        markdown = re.sub(r"[ \t]+", " ", markdown)

        return markdown.strip()