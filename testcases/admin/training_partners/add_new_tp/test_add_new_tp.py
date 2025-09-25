import pytest

from src.pages.admin.add_new_tp.add_new_tp_steps import AddNewTP
from src.utils.helpers.common import login_and_verify_dashboard
from src.utils.helpers.common_checks import  check_element_in_table
from src.utils.helpers.logger import logger


@pytest.mark.parametrize("role",["admin"])
async def test_add_new_tp(page,role):
    #Login
    await login_and_verify_dashboard(page,role)
    #Navigate to Training Partners
    await page.get_by_text("Training Partners").click()
    logger.info(f"Navigated to : {page.url}")

    #Add New TP
    new_tp=page.get_by_role("button" , name="Add New TP")
    await new_tp.wait_for(state="visible")
    await new_tp.click()
    logger.info(f"Navigated to : {page.url}")
    logger.info("\n-------Adding New TP--------\n")

    #Fill all three steps
    try:
        admin_tp=AddNewTP(page)
        tp_name=await admin_tp.add_new_tp()
        print(f"\nAdded TP [{tp_name}] successfully !!")
    except Exception as e:
        raise Exception(f"Got Error while adding new TP {str(e)}")

    logger.info("\n-------Verifying TP Name in table--------\n")
    #Navigate to 'Needs Attention'
    await page.get_by_text("Needs Attention").click()
    #Verify TP appears in "Needs Attention" status
    found_tp, row_data=await check_element_in_table(page,tp_name,4,"Needs Attention")
    assert found_tp, f"TP {tp_name} should be in 'Needs Attention' but was not found"



