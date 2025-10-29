from src.base.base_page import BasePage
from src.utils.helpers.logger import logger


class LoginPage(BasePage):
    def __init__(self,page):
        super().__init__(page)
        self.email = "#email"
        self.password="#password"
        self.login_btn="//button[@type='submit']"

    async def login(self,email,password):

        logger.info(f"\nNavigated to {self.page.url}")

        await self.page.locator(self.email).fill(email)
        await self.page.locator(self.password).fill(password)
        self.logger.info(f"\nEntered Email:{email}")

        login_btn=self.page.locator(self.login_btn)

        if await login_btn.is_disabled():
            self.logger.info(f"Login Button is Disabled")
            return False

        await login_btn.click()

        await self.page.wait_for_load_state("domcontentloaded")
        await self.page.wait_for_load_state("networkidle")

        return  True







