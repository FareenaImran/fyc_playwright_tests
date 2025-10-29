from src.pages.admin.training_partners.admin_tp_page import AdminTPPage
from testcases.fixtures.tp_fixtures import setup_new_tp
from src.utils.helpers.common_checks import  check_element_in_table
from src.utils.helpers.logger import logger


async def test_add_new_tp(page,setup_new_tp):
    '''Add New TP By Admin'''

    #Add new tp
    tp_name=setup_new_tp

    logger.info("\n-------Verifying TP Name in table--------\n")

    #Navigate to 'Needs Attention'
    await page.get_by_text(AdminTPPage.NEEDS_ATTENTION).click()

    #Verify TP appears in "Needs Attention" status
    found_tp, row_data=await check_element_in_table(page,tp_name,4,AdminTPPage.NEEDS_ATTENTION)
    assert found_tp, f"TP {tp_name} should be in 'Needs Attention' but was not found"



