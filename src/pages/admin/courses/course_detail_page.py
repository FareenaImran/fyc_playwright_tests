import re
from playwright.async_api import expect
from src.base.base_page import BasePage
from src.utils.helpers.common_checks import check_success_message


class CourseDetailPage(BasePage):
    # ------ LOCATORS ------
    def __init__(self,page):
        super().__init__(page)
        self.approve_btn=page.get_by_role("button",name="Approve")
        self.confirm_approve_btn=page.get_by_role("button",name="Yes, approve. I have verified details")
        self.feature_btn = page.locator("//button[@role='switch']")

    # ------ METHODS ------
    async  def change_status_to_approved(self):
        """Changing Status to Approved"""
        await expect(self.page).to_have_url(re.compile(r".*/portal/courses/details\?id=.*"))
        await self.approve_btn.click()
        await self.confirm_approve_btn.click()
        is_approved=await check_success_message(self.page)
        if not is_approved:
            raise  Exception("Failed to change status")

    async def turn_on_featured_btn(self):
        """Turning On Featured Button"""
        await self.page.wait_for_timeout(3000)
        await self.feature_btn.click()



