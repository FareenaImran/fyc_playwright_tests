
from src.base.base_page import BasePage
from src.pages.admin.courses.course_detail_page import CourseDetailPage


class CoursePage(BasePage):

    async def get_rows(self):
        rows = self.page.locator("table > tbody > tr")
        count = await rows.count()
        if count==1:
            record=await rows.nth(0).locator("td").nth(0).inner_text()
            if record.strip()=="No records found":
                return 0,rows

        return count,rows

    async def change_course_status_to_approved(self, status):

        await self.page.get_by_role("button", name=status).click()
        count, rows = await self.get_rows()
        if count == 0:
            print("No Course left to Approve !")
            return None
        row = rows.nth(0)
        while True:
            try:
                course_name=await row.locator("td").nth(2).inner_text()
                print(f"Approving Course : {course_name}")
                action_btn = row.locator("button[aria-haspopup='menu']").first
                await action_btn.scroll_into_view_if_needed()
                await action_btn.click()
                view_details_btn = self.page.get_by_text("View Details")
                await view_details_btn.nth(0).click()
                course_detail=CourseDetailPage(self.page)
                await course_detail.change_status_to_approved()
                return  course_name

            except Exception as e:
                raise Exception(f"Error Processing Row... {str(e)}")





