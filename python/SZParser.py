from XMLParser import XMLParser
from bs4 import BeautifulSoup
from datetime import timezone, datetime


class SZParser(XMLParser):
    def __init__(self, filepath: str):
        super().__init__(filepath)

    def get_article_details(self, rss_item):
        return {
            "guid": self.get_article_guid(rss_item),
            "title": self.get_article_title(rss_item),
            "link": self.get_article_link(rss_item),
            "description": self.get_article_description(rss_item),
            "timestamp": self.get_article_timestamp(rss_item),
        }

    def get_article_creator(self, rss_item):
        try:
            return rss_item.find("dc:creator").text
        except AttributeError:
            return None

    def get_article_description(self, rss_item):
        try:
            raw_description = rss_item.find("description").text

            soup = BeautifulSoup(raw_description, "html.parser")
            return soup.find_all("p")[-1].get_text()
        except AttributeError:
            return None

    def _convert_timestamp_to_iso(self, timestamp: str) -> str:
        return (
            datetime.strptime(timestamp, "%a, %d %b %Y %H:%M:%S %Z")
            .replace(tzinfo=timezone.utc)
            .isoformat()
        )