from playwright.sync_api import sync_playwright


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
                date_picker_button_xpath = ('//*[@id="yDmH0d"]/c-wiz[2]/div/div[2]/div/c-wiz/div[2]/div/div/div['
                                            '1]/div[1]/section/div/div[1]/div[1]/div[1]/div[2]/div[2]/div/div/div['
                                            '1]/div/div/div/div[2]/div')
                page.click(f'xpath={date_picker_button_xpath}')
                month_button_xpath = ('//*[@id="ow78"]/div[2]/div/div[2]/div/div[3]/span/div/div[2]/div[1]/span['
                                      '3]/span/span/button')
                page.wait_for_selector(f'xpath={month_button_xpath}', timeout=60000)
                month_button = page.query_selector(f'xpath={month_button_xpath}')
                if month_button:
                    month_button.click()
                else:
                    print("Month button not found.")
                    return

                done_button_xpath = '//*[@id="ow78"]/div[2]/div/div[3]/div[1]/button'
                page.wait_for_selector(f'xpath={done_button_xpath}', timeout=60000)
                done_button = page.query_selector(f'xpath={done_button_xpath}')
                if done_button:
                    done_button.click()
                else:
                    print("Done button not found.")
                    return

                # Wait for the page to update after selecting the date
                page.wait_for_selector('.tsAU4e', timeout=60000)  # Adjust the selector as needed

                # Optionally, add a small delay to ensure content has loaded
                page.wait_for_timeout(3000)  # Wait for 3 seconds (adjust as needed)

                # Extract destination names and prices
                destination_elements = page.query_selector_all('.tsAU4e')

                # Sort destinations by price
                destination_elements.sort(
                    key=lambda element: float(element.query_selector('[data-gs]').inner_text().replace('£', '')))

                # Select the cheapest 5 destinations
                for destination_element in destination_elements[:5]:
                    destination_name = destination_element.inner_text()
                    price_element = destination_element.query_selector('[data-gs]')
                    price = price_element.inner_text() if price_element else "Price not available"

                    print(f"Destination: {destination_name}, Price: {price}")

            except Exception as e:
                print(f"An error occurred: {e}")

            # Close the browser
            browser.close()
