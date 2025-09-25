from src.utils.helpers.csv_reader import get_cred_from_csv
from src.utils.helpers.login_helper import login_with_credentials


async def login_by_name(page,role: str,name):
    users = get_cred_from_csv(role)
    for user in users:
        if user["name"].lower()==name.lower():
            await login_with_credentials(
                page,
                role=role,
                email=user["email"],
                password=user["password"]
            )
            return user["name"],user["email"],user["password"]
    raise Exception(f"No user found with name '{name}' for role '{role}'")
