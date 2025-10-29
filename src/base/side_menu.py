import re

from playwright.async_api import expect

from src.base.base_page import BasePage
from abc import ABC, abstractmethod

from src.utils.helpers.logger import logger


class SideMenu(BasePage,ABC):
    #------LOCATORS-----

    def __init__(self,page):
        super().__init__(page)
        self.learners=page.get_by_role("button", name="Learners")
        self.courses=page.get_by_text("Courses")

    #------METHODS-----
    @abstractmethod
    async def navigate_to_courses(self):
        pass

    async def navigate_to_learner(self):
        """Navigating to Learners Page"""
        await self.learners.first.click()
        await expect(self.page).to_have_url(re.compile(r"/portal/learners$", re.IGNORECASE))
        logger.info(f"Navigated to : {self.page.url}")


