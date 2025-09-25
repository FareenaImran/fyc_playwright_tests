from gc import get_count

import pytest

from src.base.base_page import BasePage
from src.utils.helpers.common import login_and_verify_dashboard
from src.utils.helpers.logger import logger

'''
Test All TPs Count
'''


async def test_tp_status_count(page):
    await login_and_verify_dashboard(page,"admin")
    #Navigate to TP
    await page.get_by_text("Training Partners").click()
    statuses=["All TPs","In Progress","Up for review","Needs Attention","Approved","Unpublished"]
    for status in statuses:
        #get button Count
        logger.info(f"\n-----Verifying Status: {status}------\n")
        status=page.get_by_role("button",name=status)
        admin_tp=BasePage(page)
        button_count=await admin_tp.get_count(status)
        #Count rows in all pages
        total_rows=await admin_tp.count_rows_in_all_pages()
        #Verify button Count with actual no of rows present in table
        assert button_count==total_rows, (
            f"{status} Count {button_count} != Total Rows in Table {total_rows}"
        )

