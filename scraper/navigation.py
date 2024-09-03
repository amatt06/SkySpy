from playwright.sync_api import sync_playwright

from flight_data_handler import FlightDataHandler
from datetime import datetime


class Navigation:
    LINK = (
        "https://www.google.com/travel/explore?tfs="
        "CBwQAxoOagwIAxIIL20vMDRqcGwaDnIMCAMSCC9tLzA0anBsQAFIAXACggENCP___________wEQAZgBAbIBBBgBIAE&tfu=GgA&gl=AU"
        "&curr=GBP&hl=en-GB")

    @classmethod
    def navigate_to_google_flights(cls):
        print(f"Navigating to: {cls.LINK}")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()

            page.goto(cls.LINK, wait_until='networkidle')

            try:
                # Check for and accept cookies if the screen appears
                cookie_accept_button_selector = 'button[aria-label="Accept all"]'
                if page.query_selector(cookie_accept_button_selector):
                    page.click(cookie_accept_button_selector)
                    print("Accepted cookies.")

                # Get the month after the current one
                current_month = datetime.now().month
                next_month_name = (datetime(1, current_month % 12 + 1, 1)).strftime('%B')

                # Open the date picker
                date_picker_button_xpath = ('//*[@id="yDmH0d"]/c-wiz[2]/div/div[2]/div/c-wiz/div[2]/div/div/div['
                                            '1]/div[1]/section/div/div[1]/div[1]/div[1]/div[2]/div[2]/div/div/div['
                                            '1]/div/div/div/div[2]/div')
                page.click(f'xpath={date_picker_button_xpath}')

                # Select the target month
                target_month_selector = f"button:has-text('{next_month_name}')"
                page.wait_for_selector(target_month_selector, timeout=60000)
                page.click(target_month_selector)
                print(f"Selected month: {next_month_name}")

                # Add a delay to ensure the page catches up
                page.wait_for_timeout(2000)  # Wait for 2 seconds after selecting the month

                # Click the "Done" button using CSS selector
                done_button_selector = "#ow8 button:has-text('Done')"  # Update the selector if necessary
                page.wait_for_selector(done_button_selector, timeout=60000)
                if page.is_visible(done_button_selector):
                    page.click(done_button_selector)
                    print("Clicked 'Done' button.")
                else:
                    print("Done button not visible.")

                # Wait for the page to update after selecting the date
                page.wait_for_selector('.tsAU4e', timeout=60000)

                # Optionally, add a small delay to ensure content has loaded
                page.wait_for_timeout(3000)

                # Extract destination names and prices
                destination_elements = page.query_selector_all('.tsAU4e')

                handler = FlightDataHandler(page, destination_elements)
                handler.extract_and_process_data()

            except Exception as e:
                print(f"An error occurred: {e}")

            # Close the browser
            browser.close()
