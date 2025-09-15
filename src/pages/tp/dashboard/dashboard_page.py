import re
from playwright.async_api import expect
from src.base.base_page import BasePage


class TPDashboardPage(BasePage):

   async def navigate_to_learner(self):
       await self.page.get_by_role("button",name="Learners").first.click()
       await expect(self.page).to_have_url(re.compile(r"/portal/learners$",re.IGNORECASE))


