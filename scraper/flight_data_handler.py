import json
from scraper.dictionaries.flight_data_elements import element_selectors
from scraper.dictionaries.nav_page_elements import navigation_selectors

class FlightDataHandler:
    def __init__(self, page, destination_elements):
        self.page = page
        self.destination_elements = destination_elements
        self.price_data = []

    def extract_and_process_data(self):
        for destination_element in self.destination_elements:
            destination_name = destination_element.inner_text()
            price_element = destination_element.query_selector('[data-gs]')
            price = price_element.inner_text().replace('£', '') if price_element else "Price not available"
            if price == "Price not available":
                continue

            # Click on the destination to get detailed pricing information
            destination_element.click()

            # Wait for the detailed price section to be visible
            detailed_price_arrow = navigation_selectors['detailed_price_arrow']
            try:
                self.page.wait_for_selector(detailed_price_arrow, timeout=60000)
                detailed_price_arrow_element = self.page.query_selector(detailed_price_arrow)
                if detailed_price_arrow_element:
                    detailed_price_arrow_element.click()

                    # # Extract detailed pricing information
                    # detailed_price = element_selectors['detailed_price']
                    # self.page.wait_for_selector(detailed_price, timeout=60000)
                    # detailed_price_element = self.page.query_selector(detailed_price)
                    # detailed_price_info = detailed_price_element.inner_text() if detailed_price_element \
                    #     else "Detailed price information not available"
                    #
                    # # Extract the usual price range and calculate the percentage difference
                    # if "usually cost between" in detailed_price_info:
                    #     usual_price_range = detailed_price_info.split("usually cost between")[1].strip().split("–")
                    #     usual_low = float(usual_price_range[0].replace('£', '').strip())
                    #     usual_high = float(usual_price_range[1].replace('£', '').strip())
                    #     usual_average = (usual_low + usual_high) / 2
                    #
                    #     current_price = float(price)
                    #     percentage_difference = ((usual_average - current_price) / usual_average) * 100
                    #
                    #     self.price_data.append({
                    #         "destination": destination_name,
                    #         "price": current_price,
                    #         "percentage_cheaper": percentage_difference
                    #     })

                    # Go back to the list of destinations
                    back_button = navigation_selectors['back_button']
                    self.page.wait_for_selector(back_button, timeout=60000)
                    back_button = self.page.query_selector(back_button)
                    if back_button:
                        back_button.click()
                else:
                    print(f'Detailed price arrow not found for {destination_name}')
            except Exception as e:
                print(f'Error processing {destination_name}: {e}')

        # Sort the deals by percentage difference and price
        sorted_by_percentage = sorted(self.price_data, key=lambda x: x['percentage_cheaper'], reverse=True)[:15]
        sorted_by_price = sorted(self.price_data, key=lambda x: x['price'])[:8]

        # Save the top deals to a JSON file
        FlightDataHandler.save_data_to_json(sorted_by_percentage, sorted_by_price)

    # Overwrite JSON file to store monthly data.
    @staticmethod
    def save_data_to_json(sorted_by_percentage, sorted_by_price):
        data = {
            "top_deals_by_percentage": sorted_by_percentage,
            "top_deals_by_price": sorted_by_price
        }
        with open('flight_data/london_flight_data.json', 'w') as file:
            json.dump(data, file, indent=4)
