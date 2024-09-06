from playwright.sync_api import sync_playwright
from flight_data_handler import FlightDataHandler
from scraper.dictionaries.nav_page_elements import navigation_selectors
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Navigation:
    LINK = (
        "https://www.google.com/travel/explore?tfs="
        "CBwQAxoOagwIAxIIL20vMDRqcGwaDnIMCAMSCC9tLzA0anBsQAFIAXACggENCP___________wEQAZgBAbIBBBgBIAE&tfu=GgA&gl=AU"
        "&curr=GBP&hl=en-GB")

    @classmethod
    def navigate_to_google_flights(cls):
        logger.info(f"Navigating to: {cls.LINK}")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()

            # Go to the Google Flights Explore page with the pre-set URL
            page.goto(cls.LINK, wait_until='networkidle')

            try:
                # Check for and accept cookies if the screen appears
                cookie_accept_button_selector = navigation_selectors['cookie_accept_button']
                if page.query_selector(cookie_accept_button_selector):
                    page.click(cookie_accept_button_selector)
                    logger.info("Accepted cookies.")

                # Determine the next month based on the current date
                current_month = datetime.now().month
                next_month_name = (datetime(1, current_month % 12 + 1, 1)).strftime('%B')

                # Open the date picker to select travel dates
                date_picker_button = navigation_selectors['date_picker_button']
                page.wait_for_selector(date_picker_button, timeout=10000)
                page.click(date_picker_button)

                # Select the next month in the date picker
                target_month_selector = navigation_selectors['target_month_button'](next_month_name)
                page.wait_for_selector(target_month_selector, timeout=60000)
                page.click(target_month_selector)
                logger.info(f"Selected month: {next_month_name}")

                # Add a small delay to ensure the page catches up after selecting the month
                page.wait_for_timeout(2000)

                # Click the "Done" button to confirm the date selection
                done_button_selector = navigation_selectors['done_button_selector']
                page.wait_for_selector(done_button_selector, timeout=60000)
                if page.is_visible(done_button_selector):
                    page.click(done_button_selector)
                    logger.info("Clicked 'Done' button.")
                else:
                    logger.warning("Done button not visible.")

                # Wait for the page to update with new flight data
                flight_data_selector = navigation_selectors['flight_data_selector']
                # page.wait_for_selector(flight_data_selector, timeout=60000)

                # Add delay to ensure all content is loaded
                page.wait_for_timeout(3000)

                # Extract destination names and prices for further processing
                destination_elements = page.query_selector_all(flight_data_selector)

                # Process the flight data using a separate handler
                handler = FlightDataHandler(page, destination_elements)
                handler.locate_data()

            except Exception as e:
                logger.error(f"An error occurred: {e}")

            finally:
                # Ensure the browser is closed after the task is completed
                browser.close()
                logger.info("Browser closed.")
