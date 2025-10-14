from config.config_loader import ADMIN_URL,LEARNER_URL, TP_URL
from src.base.login_page import LoginPage
from src.utils.helpers.csv_reader import get_cred_from_csv
from src.utils.helpers.logger import logger


async def login_with_credentials(page, role: str, email: str, password: str):
    if role == "learner":
        await page.goto(LEARNER_URL + "/signin")
    elif role == "trainer":
        await page.goto(TP_URL + "/login")
    elif role == "admin":
        await page.goto(ADMIN_URL)
    else:
        raise ValueError(f"Unsupported role: {role}")

    await page.wait_for_load_state("domcontentloaded")
    await page.wait_for_load_state("networkidle")

    login_page = LoginPage(page)
    return await login_page.login(email, password)


async def login_by_name_or_email(page,role: str,name):
    users = get_cred_from_csv(role)

    for user in users:
        if user["name"].lower()==name.lower() or user["email"]==name.lower():
            await login_with_credentials(page,role=role,email=user["email"],password=user["password"])
            return user["name"],user["email"],user["password"]
    raise Exception(f"No user found with '{name}' for role '{role}'")







