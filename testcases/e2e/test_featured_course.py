import pytest
from src.pages.admin.admin_dashboard_page import AdminDashboard
from src.pages.admin.courses.course_detail_page import CourseDetailPage
from src.pages.admin.courses.course_page import AdminCoursePage
from src.pages.learner.learner_home_page import LearnerHomePage
from src.utils.helpers.common import view_course_details
from src.utils.helpers.common_checks import check_success_message, check_element_in_table
from src.utils.helpers.logger import logger


@pytest.mark.e2e
async def test_featured_course_appears_on_home_page(page,login):

    """Test that when admin turn on featured course
     then course appears on home page """

    await login(page, "admin")

    menu = AdminDashboard(page)
    await menu.navigate_to_courses()

    await page.get_by_role("button", name=AdminCoursePage.APPROVED_TAB).click()

    # find and open un-featured course
    logger.info("\nDoes Any course have Feature value 'No'?")
    unchecked, row = await check_element_in_table(page, 'No', 11, "Approved")
    if not unchecked:
        pytest.skip("All Course are already marked as featured course...Skipping Test")
    course_name = await (await row.query_selector("td:nth-child(3)")).inner_text()

    # View Course details
    await (await row.query_selector("td:last-child button")).click()
    await view_course_details(page)

    # featured course
    logger.info(f"\nTurning ON featured button for {course_name}")
    detail_page = CourseDetailPage(page)
    await detail_page.turn_on_featured_btn()

    # Verify success message
    logger.info(f"\n{await check_success_message(page)}")

    #Navigate to Learner Portal
    await page.goto("https://beta.findyourcourses.org/")
    await page.wait_for_load_state("domcontentloaded")

    #Navigate to Featured Course list
    featured_course_ele=page.locator(LearnerHomePage.FEATURED_COURSE_NAME)
    await featured_course_ele.first.scroll_into_view_if_needed()
    featured_tps=await featured_course_ele.all_inner_texts()

    #Verify Course name
    assert course_name in featured_tps,f"{course_name} not found in featured Course's list"
    logger.info(f"\nVerified {course_name} appears in featured Course's list")