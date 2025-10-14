import re
import pytest
from playwright.async_api import expect

from src.utils.helpers.common_checks import check_and_close_page_modal
from src.utils.helpers.logger import logger

@pytest.mark.parametrize("role",["learner","trainer","admin"])
async def test_logout(page,login,role):
    #Login
    await login(page,role)
    #close modal if any
    await check_and_close_page_modal(page)
    #logout
    await page.locator("//span[contains(text(),'Logout')]").click()
    #Verify
    await expect(page).to_have_url(re.compile(r".*(signin|login|org).*"))
    logger.info(f"Logout Successfully!! Navigated to {page.url}")
