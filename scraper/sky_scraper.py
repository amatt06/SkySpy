# sky_scraper.py

from scraper.navigation import Navigation


class SkyScraper:
    @staticmethod
    def store_flight_data():
        Navigation.navigate_to_google_flights()
