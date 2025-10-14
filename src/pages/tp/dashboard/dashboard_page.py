import re
from playwright.async_api import expect
from src.base.side_menu import SideMenu
from src.utils.helpers.common_checks import check_and_close_page_modal


class TPDashboardPage(SideMenu):


   #Navigate to courses
   async def navigate_to_courses(self):
        await check_and_close_page_modal(self.page)
        await self.page.get_by_role("button", name="Courses").first.click()
        await expect(self.page).to_have_url(re.compile(r".*/courses$"))
        print(f"Navigated to {self.page.url}")
        await check_and_close_page_modal(self.page)
        await self.page.wait_for_load_state("domcontentloaded")


