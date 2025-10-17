import pytest

from src.pages.admin.admin_dashboard_page import AdminDashboard
from src.pages.admin.courses.course_detail_page import CourseDetailPage
from src.utils.helpers.common import view_course_details
from src.utils.helpers.common_checks import check_success_message, check_element_in_table
from src.utils.helpers.logger import logger


@pytest.mark.e2e
async def test_featured_tp_appears_on_home_page(page,login):

    """Test that when admin turn on featured partner
     then tp appears on home page """

    await login(page,"admin")

    menu=AdminDashboard(page)
    await menu.navigate_to_tp()

    await page.get_by_role("button",name="Approved").click()
    # find and open un-featured course
    logger.info("\nDoes Any TP have Feature value 'No'?")
    unchecked, row = await check_element_in_table(page, 'No', 10, "Approved")
    if not unchecked:
        pytest.skip("All TPs are already marked as featured course...Skipping Test")
    tp_name = await (await row.query_selector("td:nth-child(4)")).inner_text()
    s_no = await (await row.query_selector("td:nth-child(1)")).inner_text()

    # View TP details
    await (await row.query_selector("td:last-child button")).click()
    await view_course_details(page)

    # featured Tp
    logger.info(f"\nTurning ON featured button for {tp_name}")
    detail_page = CourseDetailPage(page)
    await detail_page.turn_on_featured_btn()

    #Succes Msg
    logger.info(f"\n{await check_success_message(page)}")

    #Navigate to Learner Portal
    await page.goto("https://beta.findyourcourses.org/")
    await page.wait_for_load_state("domcontentloaded")

    #Navigate to Featured TP list
    featured_tps_ele=page.locator("(//div[@aria-roledescription='carousel'])[2]//h3")
    await featured_tps_ele.first.scroll_into_view_if_needed()
    featured_tps=await featured_tps_ele.all_inner_texts()

    #Verify TP name
    assert tp_name in featured_tps,f"{tp_name} not found in featured TP's list"
    logger.info(f"\nVerified {tp_name} appears in featured TP's list")