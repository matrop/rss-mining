import pandas as pd
import xml.etree.ElementTree as ET
import os

from Settings import AirflowSettings, IngestionSettings

from datetime import datetime
from abc import ABC, abstractmethod
from typing import Dict, Any

# TODO: Build decorator for Attribute Error exception
# TODO: Research if it's better to pass settings object or individual settings


class XMLParser(ABC):
    def __init__(
        self,
        filepath: str,
        ingestionSettings: IngestionSettings,
        airflowSettings: AirflowSettings,
    ) -> None:
        self.input_filename = os.path.splitext(filepath.split("/")[-1])[0]

        splitted_input_filename = self.input_filename.split("T")[0].split("-")

        self.tree = ET.parse(filepath)
        self.root = self.tree.getroot()
        self.creation_timestamp = datetime.now()
        self.output_dir = os.path.join(
            airflowSettings.transformed_data_dir,
            ingestionSettings.ingestion_source_name,
            splitted_input_filename[0],
            splitted_input_filename[1],
            splitted_input_filename[2],
        )
        self.output_filename = os.path.join(
            self.output_dir,
            self.input_filename + ".csv",
        )

    def _convert_timestamp_to_iso(self, timestamp: str) -> str:
        return datetime.strptime(timestamp, "%a, %d %b %Y %H:%M:%S %z").isoformat()

    def get_article_title(self, rss_item):
        try:
            return rss_item.find("title").text.strip('"')
        except AttributeError:
            return None

    def get_article_link(self, rss_item):
        try:
            return rss_item.find("link").text
        except AttributeError:
            return None

    def get_article_description(self, rss_item):
        try:
            return rss_item.find("description").text.strip('"')
        except AttributeError:
            return None

    def get_article_category(self, rss_item):
        try:
            return rss_item.find("category").text
        except AttributeError:
            return None

    def get_article_timestamp(self, rss_item):
        try:
            return self._convert_timestamp_to_iso(rss_item.find("pubDate").text)
        except AttributeError:
            return None

    def get_article_guid(self, rss_item):
        try:
            return rss_item.find("guid").text
        except AttributeError:
            return None

    @abstractmethod
    def get_article_details(self, rss_item: ET.Element) -> Dict[str, Any]:
        """Fetches all information from a single RSS item and returns it as a dictionary

        Args:
            rss_item (ET.Element): RSS Feed Item as a Element Tree object

        Returns:
            Dict[str, Any]: RSS Feed Item fields extracted into a dictionary
        """
        pass

    def create_article_dataframe(self) -> pd.DataFrame:
        """Converts RSS Feed Items into a pandas dataframe

        Returns:
            pd.DataFrame: Dataframe containing structured data formerly contained in RSS Feed items
        """
        article_details = []

        for article in self.root[0].findall("item"):
            article_details.append(self.get_article_details(article))

        return pd.DataFrame(article_details)

    def clean_article_dataframe(self, article_df: pd.DataFrame) -> pd.DataFrame:
        return article_df.drop_duplicates(subset=["guid"])

    def save_to_csv(self):
        article_df = self.create_article_dataframe()

        cleaned_article_df = self.clean_article_dataframe(article_df)

        if not os.path.isdir(self.output_dir):
            os.makedirs(self.output_dir)

        print(f"Saving parsed RSS feed to csv | filename = {self.output_filename}")

        cleaned_article_df.to_csv(
            self.output_filename,
            sep="\t",
            header=False,
            index=False,
        )

        print("Saving finished!")
