# main.py

from scraper.sky_scraper import SkyScraper
import subprocess

if __name__ == '__main__':
    # Create an instance of SkyScraper and call store_flight_data
    # scraper = SkyScraper()
    # scraper.store_flight_data()

    # Call the Node.js script to send emails
    try:
        result = subprocess.run(['node', 'courier/send_email.js'], check=True, capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f'Error sending emails: {e.stderr}')