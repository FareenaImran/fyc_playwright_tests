import re
import pytest
from playwright.async_api import expect
from src.pages.admin.admin_dashboard_page import AdminDashboard
from src.pages.admin.courses.course_detail_page import CourseDetailPage
from src.utils.helpers.common import select_menu_option, get_row_text
from src.utils.helpers.common_checks import  check_ele_in_all_pages
from src.utils.helpers.logger import logger


@pytest.mark.admin
@pytest.mark.parametrize("role",["admin"])
async def test_change_course_status_from_under_review_to_approved(page,login,role):
    #Login
    await login(page,role)
    #Navigate to courses
    admin_dashboard=AdminDashboard(page)
    await admin_dashboard.navigate_to_courses()
    await page.wait_for_load_state("networkidle")

    while True:
        #Change course status from under review ro Approved
        await page.get_by_role("button",name="Under Review").click()
        #Get course name
        course_name=await get_row_text(page,3,row_no=0)
        if not course_name:
            break

        #View Details
        result= await select_menu_option(page,1,course_name)
        assert result is not None,f"Unable to select menu option :{result}"
        #Change course status to approve
        logger.info(f"\nApproving {course_name}")
        admin_courses=CourseDetailPage(page)
        await admin_courses.change_status_to_approved()
        #Go back to courses
        await page.go_back()
        await page.wait_for_selector("table > tbody",state="visible")
        await expect(page).to_have_url(re.compile(r".*/portal/courses$"))
        result= await get_row_text(page, 3,row_no=0)
        if result is None:
            break
        # Verify course exits in Approved
        await page.get_by_role("button",name="Approved").click()
        found,_=await check_ele_in_all_pages(page,course_name,3,"Approved")
        assert found, f"Did not get {course_name} in approved list"










