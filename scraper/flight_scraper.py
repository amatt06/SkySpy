from playwright.sync_api import sync_playwright


def navigate_to_google_flights():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Navigate to Google Flights
        page.goto('https://www.google.com/travel/flights')

        # Close the browser
        browser.close()


if __name__ == "__main__":
    navigate_to_google_flights()
