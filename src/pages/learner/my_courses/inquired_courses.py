from src.base.base_page import BasePage
from src.pages.learner.dashboard_page import DashboardPage


class InquiredCourses(BasePage):

   #Get Recent inquiry from inquired courses
    async def get_recent_inquiry(self,column):
        dashboard=DashboardPage(self.page)
        await dashboard.navigate_to_my_courses()

        await self.page.get_by_text("Inquired Courses").click()

        msg=await self.get_column_text(column)

        return msg

