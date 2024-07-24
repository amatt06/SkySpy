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

                # Store detailed price information
                price_data = []

                for destination_element in destination_elements:
                    destination_name = destination_element.inner_text()
                    price_element = destination_element.query_selector('[data-gs]')
                    price = price_element.inner_text().replace('£', '') if price_element else "Price not available"
                    if price == "Price not available":
                        continue

                    print(f"Destination: {destination_name}, Price: £{price}")

                    # Click on the destination to get detailed pricing information
                    destination_element.click()

                    # Wait for the detailed price information to load
                    detailed_price_button_xpath = '//*[@id="yDmH0d"]/c-wiz[2]/div/div[2]/div/c-wiz/div[2]/div/div/div[2]/div/div[4]/div[1]/div/div[2]/div[1]/div[1]/div/div/div/div/div[1]/div[3]/button'
                    page.wait_for_selector(f'xpath={detailed_price_button_xpath}', timeout=60000)
                    detailed_price_button = page.query_selector(f'xpath={detailed_price_button_xpath}')
                    if detailed_price_button:
                        detailed_price_button.click()
                    else:
                        print("Detailed price button not found.")
                        continue

                    # Extract detailed pricing information
                    detailed_price_xpath = '//*[@id="yDmH0d"]/c-wiz[2]/div/div[2]/div/c-wiz/div[2]/div/div/div[2]/div/div[4]/div[1]/div/div[2]/div[1]/div[1]/div/div/div/div/div[2]/div/div/div[2]'
                    page.wait_for_selector(f'xpath={detailed_price_xpath}', timeout=60000)
                    detailed_price_element = page.query_selector(f'xpath={detailed_price_xpath}')
                    detailed_price_info = detailed_price_element.inner_text() if detailed_price_element else "Detailed price information not available"

                    print(f"Detailed Price Info: {detailed_price_info}")

                    # Extract the usual price range and calculate the percentage difference
                    if "usually cost between" in detailed_price_info:
                        usual_price_range = detailed_price_info.split("usually cost between")[1].strip().split("–")
                        usual_low = float(usual_price_range[0].replace('£', '').strip())
                        usual_high = float(usual_price_range[1].replace('£', '').strip())
                        usual_average = (usual_low + usual_high) / 2

                        current_price = float(price)
                        percentage_difference = ((usual_average - current_price) / usual_average) * 100

                        price_data.append({
                            "destination": destination_name,
                            "price": current_price,
                            "percentage_cheaper": percentage_difference
                        })

                    # Go back to the list of destinations
                    back_button_xpath = '//*[@id="yDmH0d"]/c-wiz[2]/div/div[2]/div/c-wiz/div[2]/div/div/div[2]/div/div[2]/div[1]/button'
                    page.wait_for_selector(f'xpath={back_button_xpath}', timeout=60000)
                    back_button = page.query_selector(f'xpath={back_button_xpath}')
                    if back_button:
                        back_button.click()
                    else:
                        print("Back button not found.")
                        continue

                # Sort the deals by percentage difference and print the top 15
                sorted_deals = sorted(price_data, key=lambda x: x['percentage_cheaper'], reverse=True)[:15]
                print(f"\nTop 15 Deals:")
                for deal in sorted_deals:
                    print(f"Destination: {deal['destination']}")
                    print(f"Price: £{deal['price']}")
                    print(f"Percentage Cheaper: {deal['percentage_cheaper']:.2f}%\n")

            except Exception as e:
                print(f"An error occurred: {e}")

            # Close the browser
            browser.close()
