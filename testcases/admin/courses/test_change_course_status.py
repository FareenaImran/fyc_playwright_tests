import pytest

from src.pages.admin.courses.all_courses_page import CoursePage
from src.utils.helpers.common import navigate_to_courses, login_and_verify_dashboard
from src.utils.helpers.common_checks import  check_element_in_table


@pytest.mark.admin
@pytest.mark.parametrize("role",["admin"])
async def test_change_course_status_from_under_review_to_approved(page,role):
    #Login
    await login_and_verify_dashboard(page,role)
    #Navigate to courses
    await navigate_to_courses(page)
    admin=CoursePage(page)
    while True:
        #Change course status from under review ro Approved
        course_name=await admin.change_course_status_to_approved("Under Review")
        if not course_name:
            return None
        await page.get_by_role("button",name="Approved").click()
        #Verify course exits in Approved
        await check_element_in_table(page,course_name, 3, "Approved")









