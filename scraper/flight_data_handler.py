# flight_data_handler.py

import json
import logging
import os

from scraper.dictionaries.flight_data_elements import element_selectors
from scraper.dictionaries.nav_page_elements import navigation_selectors

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FlightDataHandler:
    def __init__(self, page, destination_elements):
        self.page = page
        self.destination_elements = destination_elements
        self.price_data = []

    def locate_data(self):
        logging.info('Starting to locate data...')
        for destination_element in self.destination_elements:
            destination_name = destination_element.inner_text()
            price_element = destination_element.query_selector('[data-gs]')
            price = price_element.inner_text().replace('£', '') if price_element else "Price not available"

            if price == "Price not available":
                logging.warning(f'Price not available for destination: {destination_name}')
                continue

            logging.info(f'Found price {price} for destination: {destination_name}')

            # Click on the destination to get detailed pricing information
            destination_element.click()

            # Wait for the detailed price section to be visible
            if self.click_detailed_price_arrow():
                self.extract_detailed_pricing(destination_name, price)
            else:
                logging.warning(f'Skipping extraction for {destination_name} due to missing detailed price arrow.')

            # Go back to the list of destinations
            self.go_back_to_destination_list()

        self.sort_and_save_data()
        logging.info('Data extraction and processing complete.')

    def click_detailed_price_arrow(self):
        """Click on the detailed price arrow and return True if successful."""
        detailed_price_arrow_selector = navigation_selectors.get('detailed_price_arrow')
        if not detailed_price_arrow_selector:
            logging.error('Detailed price arrow selector not defined.')
            return False

        try:
            # Wait for the detailed price arrow to be present
            self.page.wait_for_selector(detailed_price_arrow_selector, timeout=60000)
            detailed_price_arrow_element = self.page.query_selector(detailed_price_arrow_selector)
            if detailed_price_arrow_element:
                detailed_price_arrow_element.click()
                logging.info('Clicked detailed price arrow.')
                return True
            else:
                logging.warning('Detailed price arrow element not found, skipping this destination.')
                return False
        except Exception as e:
            logging.error(f'Error clicking detailed price arrow: {e}')
            return False

    def extract_detailed_pricing(self, destination_name, price):
        """Extract detailed pricing information and calculate percentage difference."""
        try:
            detailed_price_selector = element_selectors.get('detailed_price')
            if not detailed_price_selector:
                logging.error('Detailed price selector not defined.')
                return

            self.page.wait_for_selector(detailed_price_selector, timeout=60000)
            detailed_price_element = self.page.query_selector(detailed_price_selector)
            detailed_price_info = detailed_price_element.inner_text() if detailed_price_element else "Detailed price information not available"

            # Log the raw detailed price info
            logging.info(f'Raw detailed price info for {destination_name}: {detailed_price_info}')

            # Adjust parsing logic for the new format
            if "usually cost between" in detailed_price_info:
                logging.info(f'Detailed price info for {destination_name}: {detailed_price_info}')
                try:
                    price_range = detailed_price_info.split("usually cost between")[1].strip().split("–")
                    usual_low = float(price_range[0].replace('£', '').strip()) if len(price_range) > 0 else 0
                    usual_high = float(price_range[1].replace('£', '').strip()) if len(price_range) > 1 else 0
                    usual_average = (usual_low + usual_high) / 2 if usual_high > 0 else 0

                    current_price = float(price)
                    percentage_difference = ((
                                                     usual_average - current_price) / usual_average) * 100 if usual_average > 0 else 0

                    self.price_data.append({
                        "destination": destination_name,
                        "price": current_price,
                        "percentage_cheaper": percentage_difference
                    })

                    logging.info(
                        f'Extracted data for {destination_name}: Price - {current_price}, Percentage cheaper - {percentage_difference:.2f}%')
                except ValueError as e:
                    logging.error(f'Error parsing detailed price info for {destination_name}: {e}')
            else:
                logging.warning(f'Detailed price information format not recognized for {destination_name}.')
        except Exception as e:
            logging.error(f'Error extracting pricing for {destination_name}: {e}')

    def go_back_to_destination_list(self):
        """Navigate back to the destination list after viewing detailed pricing."""
        try:
            back_button_selector = navigation_selectors.get('back_button')
            if not back_button_selector:
                logging.error('Back button selector not defined.')
                return

            self.page.wait_for_selector(back_button_selector, timeout=60000)
            back_button_element = self.page.query_selector(back_button_selector)
            if back_button_element:
                back_button_element.click()
                logging.info('Navigated back to destination list.')
            else:
                logging.warning('Back button element not found.')
        except Exception as e:
            logging.error(f'Error navigating back: {e}')

    def sort_and_save_data(self):
        """Sort the deals by percentage difference and price, then save to JSON."""
        sorted_by_percentage = sorted(self.price_data, key=lambda x: x['percentage_cheaper'], reverse=True)[:15]
        sorted_by_price = sorted(self.price_data, key=lambda x: x['price'])[:8]
        self.save_data_to_json(sorted_by_percentage, sorted_by_price)

    @staticmethod
    def save_data_to_json(sorted_by_percentage, sorted_by_price):
        """Save the sorted data to a JSON file."""
        data = {
            "top_deals_by_percentage": sorted_by_percentage,
            "top_deals_by_price": sorted_by_price
        }
        directory = './scraper/flight_data'
        if not os.path.exists(directory):
            os.makedirs(directory)
        file_path = os.path.join(directory, 'london_flight_data.json')
        try:
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)
            logging.info('Data saved to JSON file successfully.')
        except Exception as e:
            logging.error(f'Error saving test data to JSON file: {e}')
