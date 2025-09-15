import pytest

from src.pages.admin.courses.all_courses_page import CoursePage
from src.utils.helpers.common_checks import login_and_verify_dashboard, navigate_to_courses, check_element_in_table


@pytest.mark.admin
@pytest.mark.parametrize("role",["admin"])
async def test_change_course_status_from_under_review_to_approved(page,role):
    await login_and_verify_dashboard(page,role)
    await navigate_to_courses(page)
    admin=CoursePage(page)
    while True:
        course_name=await admin.change_course_status_to_approved("Under Review")
        if not course_name:
            return None
        await page.get_by_role("button",name="Approved").click()
        await check_element_in_table(page,course_name, 3, "Approved")









