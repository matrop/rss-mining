import requests
import os
from datetime import datetime

from Settings import AirflowSettings, IngestionSettings


class RSSGetter:
    def __init__(
        self, ingestionSettings: IngestionSettings, airflowSettings: AirflowSettings
    ) -> None:
        self.ingestionSettings = ingestionSettings
        self.airflowSettings = airflowSettings
        self.creation_timestamp = datetime.now()
        self.output_filename = None
        self.output_dir = os.path.join(
            self.airflowSettings.raw_data_dir,
            self.ingestionSettings.ingestion_source_name,
            str(self.creation_timestamp.year),
            str(self.creation_timestamp.month).zfill(2),
            str(self.creation_timestamp.day).zfill(2),
        )
        self.filename = self._generate_filename()
        self.output_filename = os.path.join(
            self.output_dir,
            self.filename,
        )

    def _get_xml_from_web(self) -> str:
        r = requests.get(self.ingestionSettings.rss_feed_url)

        if not r.ok:
            print(
                f"Error fetching XML data | URL = {self.ingestionSettings.rss_feed_url}  Status = {r.status_code}"
            )
            return

        return r.text

    def _generate_filename(self) -> str:
        iso_timestamp = self.creation_timestamp.isoformat(timespec="seconds").replace(
            ":", "-"
        )
        return iso_timestamp + ".xml"

    def save_to_file(self) -> None:
        xml = self._get_xml_from_web()

        if not os.path.isdir(self.output_dir):
            os.makedirs(self.output_dir)

        with open(self.output_filename, "wb") as file:
            file.write(xml.encode("utf-8"))

        print(f"Saved RSS file to raw directory | File = {self.output_filename}")
