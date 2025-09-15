import re
from playwright.async_api import expect
from src.base.base_page import BasePage
from src.utils.helpers.common_checks import get_success_message

class CourseDetailPage(BasePage):

    async  def change_status_to_approved(self):
        await expect(self.page).to_have_url(re.compile(r".*/portal/courses/details\?id=.*"))
        await self.page.get_by_role("button",name="Approve").click()
        await self.page.get_by_role("button",name="Yes, approve. I have verified details").click()
        is_approved=await get_success_message(self.page)
        if not is_approved:
            raise  Exception("Course did not approved successfully")
        await self.page.go_back()
        await expect(self.page).to_have_url(re.compile(r".*/portal/courses$"))


