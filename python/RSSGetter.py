import requests
import os
from datetime import datetime

import Settings


class RSSGetter:
    def __init__(self, url: str) -> None:
        self.url = url
        self.output_filename = None

    def _get_xml_from_web(self) -> str:
        r = requests.get(self.url)

        if not r.ok:
            print(
                f"Error fetching XML data | URL = {self.url}  Status = {r.status_code}"
            )
            return

        return r.text

    def _generate_filename(self) -> str:
        iso_timestamp = datetime.now().isoformat(timespec="seconds").replace(":", "-")
        return iso_timestamp + ".xml"

    def save_to_file(self) -> None:
        xml = self._get_xml_from_web()
        filename = self._generate_filename()
        self.output_filename = os.path.join(Settings.RAW_DATA_DIR, filename)

        with open(self.output_filename, "wb") as file:
            file.write(xml.encode("utf-8"))

        print(f"Saved RSS file to raw directory | File = {self.output_filename}")
