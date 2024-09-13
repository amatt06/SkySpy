# main.py

import os
from scraper.sky_scraper import SkyScraper
import subprocess

if __name__ == '__main__':
    scraper = SkyScraper()
    scraper.store_flight_data()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    send_email_script = os.path.join(script_dir, 'courier/send_email.js')

    try:
        result = subprocess.run(['node', send_email_script], check=True, capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f'Error sending emails: {e.stderr}')