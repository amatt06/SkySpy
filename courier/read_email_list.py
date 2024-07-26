# read_email_list.py

import csv
import os
from typing import List, Dict

SENSITIVE_DATA_DIR = '../sensitive_data'


def get_contacts_from_csv(file_name: str = 'email_list.csv') -> List[Dict[str, str]]:
    contact_list = []
    file_path = os.path.join(SENSITIVE_DATA_DIR, file_name)
    try:
        with open(file_path, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                email = row.get('email', '').strip()
                first_name = row.get('first_name', '').strip()
                contact_list.append({
                    "email": email,
                    "first_name": first_name
                })
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return contact_list
