
from src.base.base_page import BasePage
from src.pages.admin.courses.course_detail_page import CourseDetailPage
from src.utils.helpers.common_checks import check_success_message, get_rows


class CoursePage(BasePage):



    async def change_course_status_to_approved(self, status):

        await self.page.get_by_role("button", name=status).click()
        count, rows = await get_rows(self.page)
        if count == 0:
            print("No Records Found in Table !")
            return None
        row = rows.nth(0)
        while True:
            try:
                text=await row.locator("td").nth(2).inner_text()
                print(f"Changing Status of {text}")
                action_btn = row.locator("button[aria-haspopup='menu']").first
                await action_btn.scroll_into_view_if_needed()
                await action_btn.click()
                view_details_btn = self.page.get_by_text("View Details")
                await view_details_btn.nth(0).click()

                course_detail=CourseDetailPage(self.page)
                await course_detail.change_status_to_approved()

                return  text

            except Exception as e:
                raise Exception(f"Error Processing Row... {str(e)}")





