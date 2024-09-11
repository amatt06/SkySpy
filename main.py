# main.py

from scraper.sky_scraper import SkyScraper
from scraper.flight_data_handler import FlightDataHandler


def print_hi(name):
    print(f'Hi, {name}')


if __name__ == '__main__':
    # Create an instance of SkyScraper and call store_flight_data
    scraper = SkyScraper()
    scraper.store_flight_data()
