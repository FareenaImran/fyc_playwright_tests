import re

from playwright.async_api import expect

from src.base.side_menu import SideMenu
from src.utils.helpers.logger import logger


class AdminDashboard(SideMenu):
    
    def __init__(self,page):
        super().__init__(page)
        self.tp_option=page.get_by_text("Training Partners")


    async def navigate_to_courses(self):
        await expect(self.courses).to_be_visible()
        await self.courses.click()
        await expect(self.page).to_have_url(re.compile(r"/courses$"))
        logger.info(f"\nNavigated to {self.page.url}")

    async def navigate_to_tp(self):
        await expect(self.tp_option).to_be_visible()
        await self.tp_option.click()
        await expect(self.page).to_have_url(re.compile(r"/training-partners$"))
        logger.info(f"\nNavigated to {self.page.url}")
