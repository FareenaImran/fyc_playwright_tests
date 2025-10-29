import re

from playwright.async_api import expect

from src.base.base_page import BasePage


class MyCoursesPage(BasePage):

    INQUIRED_COURSES="Inquired Courses"

    def __init__(self,page):
        super().__init__(page)
        self.course_names=page.locator("//p[normalize-space()='Applied Courses']/following-sibling::div//h3")
        self.back_to_my_courses=page.get_by_role("button",name="Back to My Courses")
        self.applied_courses=page.locator("//p[normalize-space()='Applied to Courses']")

    # Get applied courses name
    async def get_applied_courses(self):
        applied_courses = await self.course_names.all_inner_texts()
        total = len(applied_courses)
        assert total != 0, "No Course found in Applied Courses"
        return applied_courses

    async def verify_enrollment_appears_in_applied_courses(self, course_name):
        await self.back_to_my_courses.wait_for(state="visible")
        await self.back_to_my_courses.click()
        await expect(self.page).to_have_url(re.compile(r"/portal/courses$"))
        await self.applied_courses.click()
        my_courses = MyCoursesPage(self.page)
        applied_courses = await my_courses.get_applied_courses()
        print(f"\nList of Applied Courses\n{applied_courses}")
        if course_name in applied_courses:
            print(f"\nFound [{course_name}] in applied courses !! ")
            course_detail = self.page.locator(f"//h3[normalize-space()='{course_name}']/parent::div")
            return await course_detail.inner_text()
        return None