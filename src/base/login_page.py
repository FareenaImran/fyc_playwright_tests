from src.base.base_page import BasePage
from src.locators.base_locators.login_locators import LoginLocators
from src.utils.helpers.common_checks import check_success_message, check_login_error_message
from src.utils.helpers.logger import logger


class LoginPage(BasePage):

    async def login(self,email,password):

        logger.info(f"\nNavigated to {self.page.url}")

        await self.page.locator(LoginLocators.EMAIL).fill(email)
        await self.page.locator(LoginLocators.PASSWORD).fill(password)
        self.logger.info(f"\nEntered Email:{email}")

        login_btn=self.page.locator(LoginLocators.LOGIN_BTN)

        if await login_btn.is_disabled():
            self.logger.info(f"Login Button is Disabled")
            return False

        await login_btn.click()

        await self.page.wait_for_load_state("domcontentloaded")
        await self.page.wait_for_load_state("networkidle")

        return  True







