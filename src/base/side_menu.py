import re

from playwright.async_api import expect

from src.base.base_page import BasePage
from abc import ABC, abstractmethod

from src.utils.helpers.logger import logger


class SideMenu(BasePage,ABC):


    #Navigate to courses
    @abstractmethod
    async def navigate_to_courses(self):
        pass

    #Navigate to learners
    async def navigate_to_learner(self):
        await self.page.get_by_role("button", name="Learners").first.click()
        await expect(self.page).to_have_url(re.compile(r"/portal/learners$", re.IGNORECASE))
        logger.info(f"Navigated to : {self.page.url}")


