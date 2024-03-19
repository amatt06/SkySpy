# navigation.py

from playwright.sync_api import sync_playwright


class Navigation:
    LINK = ("https://www.google.com/travel/explore?tfs"
            "=CBwQAxoOagwIAhIIL20vMDRqcGwaDnIMCAISCC9tLzA0anBsQAFIAXACggEECAMQAZgBAQ&tfu=GgA&tcfs"
            "=ChIKCC9tLzA0anBsGgZMb25kb24&curr=GBP")

    @classmethod
    def navigate_to_google_flights(cls):
        print(f"Navigating to: {cls.LINK}")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()

            page.goto(cls.LINK)

            # Wait for the destinations to load
            page.wait_for_selector('.tsAU4e')

            # Extract destination names and prices
            destination_elements = page.query_selector_all('.tsAU4e')
            for destination_element in destination_elements[:5]:  # Selecting the first 5 destinations
                destination_name = destination_element.inner_text()
                price_element = destination_element.query_selector('[data-gs]')
                price = price_element.inner_text() if price_element else "Price not available"

                print(f"Destination: {destination_name}, Price: {price}")

            # Close the browser
            browser.close()
