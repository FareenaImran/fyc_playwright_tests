import pytest

from src.pages.admin.admin_dashboard_page import AdminDashboard
from src.pages.admin.courses.course_detail_page import CourseDetailPage
from src.pages.admin.courses.courses_info import CoursesInfo
from src.utils.helpers.common import view_course_detail
from src.utils.helpers.common_checks import check_success_message, check_element_in_table
from src.utils.helpers.logger import logger


@pytest.mark.admin
async def test_admin_can_enable_featured_course_via_toggle_showing_yes_in_table(page,login):

    """Test that turning on toggle button displays 'Yes' value in table"""

    await login(page,"admin")

    menu = AdminDashboard(page)
    await menu.navigate_to_courses()

    await page.get_by_role("button", name="Approved").click()


    #find and open un-featured course
    logger.info("\nDoes Any course have Feature value 'No'?")
    unchecked,row=await check_element_in_table(page,'No',11,"Approved")
    if not unchecked:
        pytest.skip("All Course are already marked as featured course...Skipping Test")
    course_name=await (await row.query_selector("td:nth-child(3)")).inner_text()
    s_no=await (await row.query_selector("td:nth-child(1)")).inner_text()

    #View Course details
    await view_course_detail(page,row)

    #featured course
    logger.info(f"\nTurning ON featured button for {course_name}")
    detail_page=CourseDetailPage(page)
    await detail_page.turn_on_featured_btn()

    #Verify success message
    logger.info(f"\n{await check_success_message(page)}")

    #Verify Table Output
    await page.go_back()
    featured=await page.locator(f"tr:has(td:nth-child(1):text-is('{s_no}')) td:nth-child(11)").inner_text()
    assert featured=='Yes',f"Got 'No' in featured column"

    logger.info(f"\nVerified !! {course_name} have '{featured}' in featured column\n")
