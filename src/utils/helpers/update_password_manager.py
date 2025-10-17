import json
from pathlib import Path

JSON_PATH=Path(__file__).resolve().parents[1] /"storage"/"update_password_emails.json"


def get_cred_from_json(role):
    with open(JSON_PATH,"r") as file:
        data=json.load(file)
        return data["UPDATE_PASSWORD_DATA"][role]

def save_new_password_in_json_file(role,new_password):
    """Read Update password data from JSON"""
    try:
        with open(JSON_PATH,"r") as file:
            data=json.load(file)
    except FileNotFoundError:
        raise  Exception(f"Unable to get file {JSON_PATH}")
    except json.JSONDecodeError as e:
        raise Exception(f"Unable to parse json data {str(e)}")

    if "UPDATE_PASSWORD_DATA" not in data:
        raise Exception("'UPDATE_PASSWORD_DATA' is missing")

    if role not in data['UPDATE_PASSWORD_DATA']:
        raise Exception(f"Role {role} not found in file")

    data['UPDATE_PASSWORD_DATA'][role]["password"]=new_password

    with open(JSON_PATH,"w") as file:
        json.dump(data,file,indent=4)

    return data['UPDATE_PASSWORD_DATA'][role]



