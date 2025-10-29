import pytest

from src.pages.admin.admin_dashboard_page import AdminDashboard
from src.utils.helpers.common import  count_rows_in_all_pages, get_count
from src.utils.helpers.logger import logger

@pytest.mark.smoke_checklist
async def test_tp_status_count(page,login):
    """
    Test that All TPs  status count is correct
    """
    await login(page,"admin")

    #Navigate to TP
    menu=AdminDashboard(page)
    await menu.navigate_to_tp()

    statuses=["All TPs","In Progress","Up for review","Needs Attention","Approved","Unpublished"]
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

