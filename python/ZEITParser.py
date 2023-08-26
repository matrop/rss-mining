from XMLParser import XMLParser


class ZEITParser(XMLParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_article_details(self, rss_item):
        return {
            "guid": self.get_article_guid(rss_item),
            "title": self.get_article_title(rss_item),
            "link": self.get_article_link(rss_item),
            "description": self.get_article_description(rss_item),
            "category": self.get_article_category(rss_item),
            "creators": self.get_article_creators(rss_item),
            "timestamp": self.get_article_timestamp(rss_item),
        }

    def _convert_guid(self, guid: str) -> str:
        return guid.strip("{}").replace("urn", "").replace("uuid", "").replace(":", "")

    def get_article_guid(self, rss_item):
        try:
            return self._convert_guid(rss_item.find("guid").text)
        except AttributeError:
            return None

    def get_article_creators(self, rss_item):
        creator_namespace = "{http://purl.org/dc/elements/1.1/}"
        try:
            full_creator_string = rss_item.find(creator_namespace + "creator").text
            creators = full_creator_string.split(" - ")[-1].strip()
            if creators == "":
                return "No author"
            return creators
        except AttributeError:
            return None
