from src.base.base_page import BasePage
from src.locators.base_locators.login_locators import LoginLocators


class LoginPage(BasePage):

    async def login(self,email,password):
        await self.page.locator(LoginLocators.EMAIL).fill(email)
        await self.page.locator(LoginLocators.PASSWORD).fill(password)
        self.logger.info(f"\nEntered Email:{email}")

        login_btn=self.page.locator(LoginLocators.LOGIN_BTN)
        if await login_btn.is_disabled():
            self.logger.info(f"Login Button is Disabled")
            return False

        await login_btn.click()
        self.logger.info(f"Clicked On Login Button")

        return  True







