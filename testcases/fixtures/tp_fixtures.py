import pytest
from src.pages.admin.training_partners.admin_tp_page import AdminTPPage
from src.utils.helpers.logger import logger


@pytest.fixture
async def setup_new_tp(page,login):
    # Login
    await login(page,"admin")

    # Navigate to Training Partners
    await page.get_by_text("Training Partners").click()

    # Add New TP
    new_tp = page.get_by_role("button", name="Add New TP")
    await new_tp.wait_for(state="visible")
    await new_tp.click()
    logger.info(f"Navigated to : {page.url}")
    logger.info("\n-------Adding New TP--------")

    # Fill all three steps
    try:
        admin_tp = AdminTPPage(page)
        tp_name = await admin_tp.add_new_tp()
        print(f"\nAdded TP '{tp_name}' Successfully !!")
        return tp_name
    except:
        raise Exception(f"\nGot Error while adding new TP")
