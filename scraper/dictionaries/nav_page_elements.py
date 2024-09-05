# nav_page_elements.py

# Selectors for navigating the various elements on the page
navigation_selectors = {
    'cookie_accept_button': 'button[aria-label="Accept all"]',
    'date_picker_button' : '.bWstqf',
    'done_button_selector': "#ow8 button:has-text('Done')",
    'target_month_button': lambda month_name: f"button:has-text('{month_name}')",
    'flight_data_selector': '.tsAU4e',
}
