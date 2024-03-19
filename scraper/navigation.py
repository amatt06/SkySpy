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

            # Close the browser
            browser.close()
