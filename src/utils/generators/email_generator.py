#Get random email
import csv
import random
import string
from pathlib import Path

USED_EMAILS_FILS=Path(__file__).resolve().parents[3]/"src"/"utils"/"storage"/"used_claimed_emails.csv"
#Generate email for claim profile
def get_random_email(tp_name):
    char=string.digits+string.ascii_lowercase
    suffix=''.join(random.choices(char,k=4))
    email=f"fyctest5401+{suffix}@gmail.com"

    #Ensure file exists
    USED_EMAILS_FILS.parent.mkdir(parents=True,exist_ok=True)

    #Append tp_name and email
    file_exits=USED_EMAILS_FILS.exists()
    with open(USED_EMAILS_FILS,"a",newline="") as f:
        writer=csv.writer(f)
        if not file_exits:
            writer.writerow(["email","tp_name"])
        writer.writerow([email,tp_name])

    return email