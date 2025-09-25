import pytest

from src.pages.admin.add_new_tp.add_new_tp_steps import AddNewTP
from src.utils.helpers.common import login_and_verify_dashboard
from src.utils.helpers.logger import logger


@pytest.fixture
async def setup_new_tp(page):
    # Login
    await login_and_verify_dashboard(page, "admin")
    # Navigate to Training Partners
    await page.get_by_text("Training Partners").click()

    # Add New TP
    new_tp = page.get_by_role("button", name="Add New TP")
    await new_tp.wait_for(state="visible")
    await new_tp.click()
    logger.info(f"Navigated to : {page.url}")
    logger.info("\n-------Adding New TP--------\n")

    # Fill all three steps
    try:
        admin_tp = AddNewTP(page)
        tp_name = await admin_tp.add_new_tp()
        print(f"\nAdded TP [{tp_name}] successfully !!")
        return tp_name
    except Exception as e:
        raise Exception(f"Got Error while adding new TP {str(e)}")
