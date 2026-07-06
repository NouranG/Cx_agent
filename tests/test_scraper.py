from ingestion.scraper import WebScraper

scraper = WebScraper()

url = "https://www.att.com/support/"

html = scraper.download(url)

print(type(html))
print(len(html))
print(html[:500])