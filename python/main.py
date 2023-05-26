import Settings
from RSSGetter import RSSGetter
from XMLParser import XMLParser

if __name__ == "__main__":
    rss_getter = RSSGetter(Settings.ZEIT_URL)
    rss_getter.save_to_file()

    # TODO: Split this into two Airflow tasks. Communicate filename via XCOM
    rss_filename = rss_getter.output_filename
    xml_parser = XMLParser(rss_filename)
    xml_parser.save_to_csv()
