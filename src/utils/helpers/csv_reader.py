import csv
import random
from pathlib import Path

CSV_PATH = Path(__file__).resolve().parents[1] / "test_data" / "users.csv"

ROLE_TO_COLUMNS={
    "learner":("Learner Name","Learner Email", "Learner Password"),
    "trainer":("TP Name","TP Email", "TP Password"),
    "admin":("Admin Name","Admin Email","Admin Password")
}

def get_cred_from_csv(role:str):
    role = role.lower()
    if role not in ROLE_TO_COLUMNS:
        raise ValueError(f"\nUnsupported Role :{role}")


    name_col, email_col, pass_col = ROLE_TO_COLUMNS[role]  #unpack tuple

    users = []
    with open(CSV_PATH,newline="") as csvfile:
        reader=csv.DictReader(csvfile)

        for row in reader:
            name = (row.get(name_col) or "").strip()
            email = (row.get(email_col) or "").strip()
            password= (row.get(pass_col) or "" ).strip()

            if email and password:
                users.append({
                    "name": name,
                    "email": email,
                    "password": password
                })
    if not users:
        raise Exception(f"No credentials found for role: {role}")

    return users


def get_random_credentials_from_google_sheet(role: str):
    users=get_cred_from_csv(role)
    return random.choice(users)


def get_untried_emails(role, tried_emails: set, max_attempts=5):
    attempt = 0
    while attempt < max_attempts:
        user = get_random_credentials_from_google_sheet(role)

        if user["email"] not in tried_emails:
            return user
        attempt += 1
    raise Exception("\nNo untried user found after max attempts")

