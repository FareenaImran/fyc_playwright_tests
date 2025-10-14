import re
from playwright.async_api import expect
from src.base.base_page import BasePage
from src.utils.helpers.common_checks import check_success_message
from src.utils.helpers.logger import logger


class CourseDetailPage(BasePage):

    async  def change_status_to_approved(self):
        await expect(self.page).to_have_url(re.compile(r".*/portal/courses/details\?id=.*"))
        await self.page.get_by_role("button",name="Approve").click()
        await self.page.get_by_role("button",name="Yes, approve. I have verified details").click()
        is_approved=await check_success_message(self.page)
        if not is_approved:
            raise  Exception("Failed to change status")

    async def turn_on_featured_btn(self):
        await self.page.wait_for_timeout(3000)
        feature_btn = self.page.locator("//button[@role='switch']")
        await feature_btn.click()



