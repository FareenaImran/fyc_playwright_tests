from src.pages.admin.admin_dashboard_page import AdminDashboard
from src.utils.helpers.common import  count_rows_in_all_pages, get_count
from src.utils.helpers.logger import logger

async def test_course_status_count(page,login):
    """
    Test that Course status count is correct
    """
    await login(page,"admin")
    #Navigate to Courses
    dashboard=AdminDashboard(page)
    await dashboard.navigate_to_courses()

    statuses=["All Courses","In Progress","Under Review", "Needs Attention", "Approved", "Live","Archived"]
    for status in statuses:
        #get button Count
        logger.info(f"\n-----Verifying Status: {status}------\n")
        status=page.get_by_role("button",name=status)
        button_count=await get_count(status)
        #Count rows in all pages
        total_rows=await count_rows_in_all_pages(page)
        #Verify button Count with actual no of rows present in table
        assert button_count==total_rows, (
            f"{status} Count {button_count} != Total Rows in Table {total_rows}"
        )

