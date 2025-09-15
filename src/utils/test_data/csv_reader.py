import csv
import os
import random
from io import StringIO
from pathlib import Path

import requests
from dotenv import load_dotenv


env_path = Path(__file__).resolve().parents[2] / "config" / ".env"
load_dotenv(dotenv_path=env_path)

csv_url = os.getenv("CSV_FILE_URL")
if not csv_url:
    raise ValueError("CSV_FILE_URL not found in .env")

ROLE_TO_COLUMNS={
    "learner":("Learner Name","Learner Email", "Learner Password"),
    "trainer":("TP Name","TP Email", "TP Password"),
    "admin":("Admin Name","Admin Email","Admin Password")
}

def get_cred_from_google_sheet(role:str):
    role = role.lower()
    if role not in ROLE_TO_COLUMNS:
        raise ValueError(f"\nUnsupported Role :{role}")

    csv_url = os.getenv("CSV_FILE_URL")
    if not csv_url:
        raise ValueError(f"\nCSV_FILE_URL not found in .env")

    response = requests.get(csv_url)
    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        print("Failed request:", response.status_code, response.text)
        raise
    lines = response.text.splitlines()

    header_keywords = ["Learner Email", "TP Email", "Admin Email"]
    header_row_index = None

    for i, line in enumerate(lines):
        if all(keyword in line for keyword in header_keywords):
            header_row_index = i
            break

    if header_row_index is None:
        raise Exception("Could not find header row for required columns")

    csvfile = StringIO("\n".join(lines[header_row_index:]))
    reader = csv.DictReader(csvfile)

    # Clean header fields (remove extra spaces)
    reader.fieldnames = [name.strip() if name else '' for name in reader.fieldnames]

    name_col, email_col, pass_col = ROLE_TO_COLUMNS[role]

    users = [
        {
            "name": row[name_col].strip(),
            "email": row[email_col].strip(),
            "password": row[pass_col].strip()
        }
        for row in reader if row.get(email_col) and row.get(pass_col)
    ]

    if not users:
        raise Exception(f"No credentials found in the CSV for role: {role}")

    return users


def get_random_credentials_from_google_sheet(role: str):
    users=get_cred_from_google_sheet(role)
    return random.choice(users)



def get_untried_emails(role, tried_emails: set, max_attempts=5):
    attempt = 0
    while attempt < max_attempts:
        user = get_random_credentials_from_google_sheet(role)

        if user["email"] not in tried_emails:
            return user
        attempt += 1
    raise Exception("\nNo untried user found after max attempts")

