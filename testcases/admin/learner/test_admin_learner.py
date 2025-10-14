from src.utils.helpers.common import  count_rows_in_all_pages, get_count
from src.utils.helpers.logger import logger

async def test_learner_status_count(page,login):
    '''
    Test that Learners status count is correct
    '''
    await login(page,"admin")
    #Navigate to Learners
    await page.get_by_text("Learners").click()
    statuses=["All Learners","Activated","De Activated"]
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

