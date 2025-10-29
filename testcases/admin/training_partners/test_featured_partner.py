import pytest

from src.pages.admin.admin_dashboard_page import AdminDashboard
from src.pages.admin.courses.course_detail_page import CourseDetailPage
from src.pages.admin.training_partners.admin_tp_page import AdminTPPage
from src.utils.helpers.common import get_row_text, select_menu_option, view_course_details
from src.utils.helpers.common_checks import check_success_message, check_element_in_table
from src.utils.helpers.logger import logger


@pytest.mark.admin
async def test_admin_can_enable_featured_partner_via_toggle_showing_yes_in_table(page,login):

    """Test that turning on toggle button displays 'Yes' value in table"""

    await login(page, "admin")

    menu = AdminDashboard(page)
    await menu.navigate_to_tp()

    await page.get_by_role("button", name=AdminTPPage.APPROVED).click()

    # find and open un-featured tp
    logger.info("\nDoes Any tp have Feature value 'No'?")
    unchecked, row = await check_element_in_table(page, 'No', 10, "Approved")
    if not unchecked:
        pytest.skip("All TPs are already marked as featured tp...Skipping Test")
    tp_name = await (await row.query_selector("td:nth-child(4)")).inner_text()
    s_no = await (await row.query_selector("td:nth-child(1)")).inner_text()

    # View Course details
    await (await row.query_selector("td:last-child button")).click()
    await view_course_details(page)

    # featured course
    logger.info(f"\nTurning ON featured button for {tp_name}")
    detail_page = CourseDetailPage(page)
    await detail_page.turn_on_featured_btn()

    # Verify success message
    logger.info(f"\n{await check_success_message(page)}")

    # Verify Table Output
    await page.go_back()
    featured = await page.locator(f"tr:has(td:nth-child(1):text-is('{s_no}')) td:nth-child(10)").inner_text()
    assert featured == 'Yes', f"Got 'No' in featured column"

    logger.info(f"\nVerified !! {tp_name} have '{featured}' in featured column\n")


