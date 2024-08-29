# SkySpy

SkySpy is a Python project aimed at scraping flight data from the Google Flights website and providing users with weekly information on flight prices and insights. The project utilises web scraping techniques to gather data from the Google Flights search results page and presents it in a structured format. Future iterations plan to run this through AWS Lambda and DynamoDB, sending results via WhatsApp messages.

## Features

- Scrapes flight data from Google Flights
- Retrieves information such as flight prices, dates, and airlines
- Calculates insights on flight prices compared to typical prices
- Identifies the top 8 cheapest flights and the top 15 flights with the highest percentage discount from the usual cost

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/amatt06/SkySpy.git
   ```

2. Navigate to the project directory:

   ```bash
   cd SkySpy
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

To run the SkySpy scraper, execute the following command:

```bash
python scraper/sky_scraper.py
```

## Trello Board

Follow the progress of SkySpy on our Trello board. You can propose new features, track ongoing tasks, and stay up-to-date with project developments.

[Trello Board](https://trello.com/b/Hg6bh95o/skyspy)


## Disclaimer

This project is intended for educational and research purposes only. The web scraping functionality provided in this project is designed to demonstrate technical concepts and should not be used for commercial purposes or in a manner that violates the terms of service of any website.

Please note that scraping websites like Google Flights may violate their terms of service, and we strongly advise against using this project for scraping live data without proper authorisation. The authors of this project are not responsible for any misuse or legal consequences resulting from the use of this code.

If you require flight data for production or commercial purposes, we recommend using official APIs or data services that provide the data you need in compliance with applicable laws and regulations.
