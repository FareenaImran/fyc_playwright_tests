import re

from playwright.async_api import expect

from src.base.side_menu import SideMenu
from src.utils.helpers.logger import logger


class AdminDashboard(SideMenu):

    async def navigate_to_courses(self):
        await expect(self.page.get_by_text("Courses")).to_be_visible()
        await self.page.get_by_text("Courses").click()
        await expect(self.page).to_have_url(re.compile(r"/courses$"))
        logger.info(f"\nNavigated to {self.page.url}")

    async def navigate_to_tp(self):
        await expect(self.page.get_by_text("Training Partners")).to_be_visible()
        await self.page.get_by_text("Training Partners").click()
        await expect(self.page).to_have_url(re.compile(r"/training-partners$"))
        logger.info(f"\nNavigated to {self.page.url}")
