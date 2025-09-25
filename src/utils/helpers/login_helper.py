from config.config_loader import ADMIN_URL,LEARNER_URL, TP_URL
from src.base.login_page import LoginPage


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

    login_page = LoginPage(page)
    return await login_page.login(email, password)





